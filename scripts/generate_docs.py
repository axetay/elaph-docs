"""
Converts a crawler JSON manifest into MkDocs-compatible Markdown files
and updates mkdocs.yml nav.

Usage:
    python scripts/generate_docs.py --manifest scripts/garage_manifest.json --module garage
    python scripts/generate_docs.py --manifest scripts/trucking_manifest.json --module trucking
"""

import argparse
import json
import re
from pathlib import Path


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text


def relative_screenshot_path(screenshot_abs: str) -> str:
    """Return path to screenshot relative to any docs sub-directory (e.g. end-users/)."""
    path = Path(screenshot_abs)
    # screenshots live at <module>/docs/assets/screenshots/<file>.png
    # markdown files live at <module>/docs/<section>/<file>.md
    # so relative path is always ../assets/screenshots/<file>.png
    return f"../assets/screenshots/{path.name}"


def is_empty_page(page: dict) -> bool:
    return (
        len(page.get("fields", [])) == 0
        and len(page.get("table_columns", [])) == 0
        and len(page.get("headings", [])) == 0
    )


def build_noise_headings(manifest: dict, threshold: int = 3) -> set:
    """Return heading texts that appear on more than `threshold` pages — UI chrome, not content."""
    from collections import Counter
    counts: Counter = Counter()
    for page in manifest["pages"]:
        for h in page.get("headings", []):
            counts[h["text"]] += 1
    return {text for text, count in counts.items() if count > threshold}


def generate_page_doc(page: dict, module: str, section: str, noise_headings: set | None = None) -> str:
    """Generate Markdown content for a single app page."""
    lines = [f"# {page['name']}\n"]

    if page.get("screenshot"):
        rel = relative_screenshot_path(page["screenshot"])
        lines.append(f"![{page['name']} screenshot]({rel})\n")

    lines.append(f"**URL:** `{page['url']}`\n")

    if is_empty_page(page):
        lines.append("> **Note:** This page had no records at the time of crawling.")
        lines.append("> The layout and available actions will appear once data is added.\n")
        lines.append("## Common Workflows\n")
        lines.append("_Document step-by-step workflows for this page here._\n")
        return "\n".join(lines)

    clean_headings = [h for h in page.get("headings", []) if h["text"] not in (noise_headings or set())]
    if clean_headings:
        lines.append("## Page Sections\n")
        for h in clean_headings:
            lines.append(f"- {h['text']}")
        lines.append("")

    if page.get("fields"):
        lines.append("## Form Fields\n")
        lines.append("| Field | Type | Required |")
        lines.append("|-------|------|----------|")
        for f in page["fields"]:
            required = "Yes" if f.get("required") else "No"
            lines.append(f"| {f['label']} | {f['type']} | {required} |")
        lines.append("")

    if page.get("table_columns"):
        lines.append("## Table Columns\n")
        for col in page["table_columns"]:
            lines.append(f"- {col}")
        lines.append("")

    if page.get("buttons"):
        lines.append("## Actions\n")
        for btn in page["buttons"]:
            lines.append(f"- **{btn}**")
        lines.append("")

    lines.append("## Common Workflows\n")
    lines.append("_Document step-by-step workflows for this page here._\n")

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
        print(f"  Filtering {len(noise_headings)} noise headings: {sorted(noise_headings)}")

    end_user_pages = []
    admin_pages = []

    for page in manifest["pages"]:
        slug = slugify(page["name"])
        name_lower = page["name"].lower()
        is_admin = any(k in name_lower for k in ["admin", "setting", "config", "manage user", "user management", "permission"])
        section = "admin" if is_admin else "end-users"

        content = generate_page_doc(page, module, section, noise_headings)
        out_path = docs_dir / section / f"{slug}.md"
        out_path.write_text(content)
        flag = " [EMPTY]" if is_empty_page(page) else ""
        print(f"  Written: {out_path}{flag}")

        rel_path = f"{section}/{slug}.md"
        if is_admin:
            admin_pages.append({page["name"]: rel_path})
        else:
            end_user_pages.append({page["name"]: rel_path})

    admin_overview = admin_dir / "overview.md"
    if not admin_overview.exists():
        admin_overview.write_text("# Admin Overview\n\nThis section covers administrative functions.\n")

    mkdocs_path = Path(f"{module}/mkdocs.yml")
    mkdocs_content = mkdocs_path.read_text()

    nav_lines = ["nav:"]
    nav_lines.append("  - Home: index.md")
    nav_lines.append("  - End Users:")
    for p in end_user_pages:
        for name, path in p.items():
            nav_lines.append(f"      - '{name}': {path}")
    nav_lines.append("  - Admin:")
    nav_lines.append("      - Overview: admin/overview.md")
    for p in admin_pages:
        for name, path in p.items():
            nav_lines.append(f"      - '{name}': {path}")

    new_nav = "\n".join(nav_lines) + "\n"
    if "nav:" in mkdocs_content:
        mkdocs_content = re.sub(r"nav:.*", new_nav, mkdocs_content, flags=re.DOTALL)
    else:
        mkdocs_content += "\n" + new_nav

    mkdocs_path.write_text(mkdocs_content)
    print(f"Updated nav in {mkdocs_path}")
    print(f"Done: {len(manifest['pages'])} pages documented.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--module", required=True, choices=["garage", "trucking"])
    args = parser.parse_args()
    generate_docs(args.manifest, args.module)
