"""
Converts an enriched crawler manifest into MkDocs-compatible Markdown files
with hierarchy-based nav, rich content, and cross-hyperlinks.

Usage:
    python scripts/generate_docs.py \
        --manifest scripts/garage_manifest_enriched.json --module garage
    python scripts/generate_docs.py \
        --manifest scripts/trucking_manifest_enriched.json --module trucking

Falls back gracefully if manifest is not enriched (missing description/how_to_use).
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hierarchy import HIERARCHIES


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text


def relative_screenshot_path(screenshot_abs: str) -> str:
    return f"../assets/screenshots/{Path(screenshot_abs).name}"


def is_empty_page(page: dict) -> bool:
    return (
        len(page.get("fields", [])) == 0
        and len(page.get("table_columns", [])) == 0
        and len(page.get("headings", [])) == 0
    )


def is_user_visible_field(f: dict) -> bool:
    label = f.get("label", "")
    if f.get("type") == "hidden":
        return False
    if label.startswith("zc-"):
        return False
    if label.startswith("SF("):
        return False
    if "::" in label:
        return False
    return True


def build_noise_headings(manifest: dict, threshold: int = 3) -> set:
    from collections import Counter
    counts: Counter = Counter()
    for page in manifest["pages"]:
        for h in page.get("headings", []):
            counts[h["text"]] += 1
    return {text for text, count in counts.items() if count > threshold}


def build_related_links(page_name: str, module: str, slug_map: dict) -> list[tuple[str, str]]:
    """Return [(name, relative_md_path)] for pages in the same hierarchy section."""
    hierarchy = HIERARCHIES[module]
    for group in hierarchy:
        if page_name in group["pages"]:
            related = []
            for sibling in group["pages"]:
                if sibling != page_name and sibling in slug_map:
                    related.append((sibling, f"{slug_map[sibling]}.md"))
            return related
    return []


def generate_page_doc(
    page: dict,
    module: str,
    section: str,
    noise_headings: set,
    slug_map: dict,
) -> str:
    lines = [f"# {page['name']}\n"]

    # Screenshot
    if page.get("screenshot"):
        rel = relative_screenshot_path(page["screenshot"])
        lines.append(f"![{page['name']} screenshot]({rel})\n")

    # Description (enriched)
    if page.get("description"):
        lines.append(f"{page['description']}\n")

    lines.append(f"**URL:** `{page['url']}`\n")

    # Empty state notice
    if is_empty_page(page):
        lines.append("> **Note:** This page had no records at the time of documentation.")
        lines.append("> The layout and available actions will appear once data is added.\n")
    else:
        # How to use (enriched)
        if page.get("how_to_use"):
            lines.append("## How to Use\n")
            for i, step in enumerate(page["how_to_use"], 1):
                lines.append(f"{i}. {step}")
            lines.append("")

        # Page sections (headings, noise-filtered)
        clean_headings = [h for h in page.get("headings", []) if h["text"] not in noise_headings]
        if clean_headings:
            lines.append("## Page Sections\n")
            for h in clean_headings:
                lines.append(f"- {h['text']}")
            lines.append("")

        # Form fields with enriched descriptions
        visible_fields = [f for f in page.get("fields", []) if is_user_visible_field(f)]
        if visible_fields:
            field_descriptions = page.get("field_descriptions", {})
            lines.append("## Form Fields\n")
            lines.append("| Field | Description | Type | Required |")
            lines.append("|-------|-------------|------|----------|")
            for f in visible_fields:
                desc = field_descriptions.get(f["label"], "")
                required = "Yes" if f.get("required") else "No"
                lines.append(f"| {f['label']} | {desc} | {f['type']} | {required} |")
            lines.append("")

        # Table columns
        if page.get("table_columns"):
            lines.append("## Table Columns\n")
            for col in page["table_columns"]:
                lines.append(f"- {col}")
            lines.append("")

        # Actions
        if page.get("buttons"):
            lines.append("## Actions\n")
            for btn in page["buttons"]:
                lines.append(f"- **{btn}**")
            lines.append("")

        # Tips (enriched)
        if page.get("tips"):
            lines.append("## Tips\n")
            for tip in page["tips"]:
                lines.append(f"- {tip}")
            lines.append("")

    # Related pages (cross-links)
    related = build_related_links(page["name"], module, slug_map)
    if related:
        lines.append("## Related Pages\n")
        for name, path in related:
            lines.append(f"- [{name}]({path})")
        lines.append("")

    # Workflow stub
    lines.append("## Common Workflows\n")
    lines.append("_Add step-by-step workflows specific to your organisation here._\n")

    return "\n".join(lines)


def generate_docs(manifest_path: str, module: str) -> None:
    with open(manifest_path) as f:
        manifest = json.load(f)

    docs_dir = Path(f"{module}/docs")
    end_users_dir = docs_dir / "end-users"
    admin_dir = docs_dir / "admin"
    end_users_dir.mkdir(parents=True, exist_ok=True)
    admin_dir.mkdir(parents=True, exist_ok=True)

    noise_headings = build_noise_headings(manifest)
    if noise_headings:
        print(f"  Filtering {len(noise_headings)} noise headings")

    # Build slug map: page_name -> slug (filename without .md)
    slug_map = {p["name"]: slugify(p["name"]) for p in manifest["pages"]}

    # Identify admin pages
    admin_keywords = ["admin", "setting", "config", "manage user", "user management", "permission"]

    # Write all page docs
    for page in manifest["pages"]:
        name_lower = page["name"].lower()
        is_admin = any(k in name_lower for k in admin_keywords)
        section = "admin" if is_admin else "end-users"

        content = generate_page_doc(page, module, section, noise_headings, slug_map)
        out_path = docs_dir / section / f"{slug_map[page['name']]}.md"
        out_path.write_text(content)
        flag = " [EMPTY]" if is_empty_page(page) else ""
        print(f"  Written: {out_path}{flag}")

    # Write admin overview stub if missing
    admin_overview = admin_dir / "overview.md"
    if not admin_overview.exists():
        admin_overview.write_text("# Admin Overview\n\nThis section covers administrative functions.\n")

    # Build nav — nested by hierarchy section
    hierarchy = HIERARCHIES[module]
    nav_lines = ["nav:"]
    nav_lines.append("  - Home: index.md")

    for group in hierarchy:
        section_pages = [name for name in group["pages"] if name in slug_map]
        if not section_pages:
            continue
        nav_lines.append(f"  - {group['section']}:")
        for name in section_pages:
            slug = slug_map[name]
            nav_lines.append(f"      - '{name}': end-users/{slug}.md")

    nav_lines.append("  - Admin:")
    nav_lines.append("      - Overview: admin/overview.md")

    # Update mkdocs.yml nav
    mkdocs_path = Path(f"{module}/mkdocs.yml")
    mkdocs_content = mkdocs_path.read_text()
    new_nav = "\n".join(nav_lines) + "\n"
    if "nav:" in mkdocs_content:
        mkdocs_content = re.sub(r"nav:.*", new_nav, mkdocs_content, flags=re.DOTALL)
    else:
        mkdocs_content += "\n" + new_nav
    mkdocs_path.write_text(mkdocs_content)

    print(f"Updated nav in {mkdocs_path} ({len(hierarchy)} sections)")
    print(f"Done: {len(manifest['pages'])} pages documented.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--module", required=True, choices=["garage", "trucking"])
    args = parser.parse_args()
    generate_docs(args.manifest, args.module)
