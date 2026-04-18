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


def relative_screenshot_path(screenshot_abs: str, module: str) -> str:
    """Convert absolute screenshot path to relative path from docs/ dir."""
    path = Path(screenshot_abs)
    try:
        return "../" + str(path.relative_to(f"{module}/docs"))
    except ValueError:
        return path.name


def generate_page_doc(page: dict, module: str, section: str) -> str:
    """Generate Markdown content for a single app page."""
    lines = [f"# {page['name']}\n"]

    if page.get("screenshot"):
        rel = relative_screenshot_path(page["screenshot"], module)
        lines.append(f"![{page['name']} screenshot]({rel})\n")

    lines.append(f"**URL:** `{page['url']}`\n")

    if page.get("headings"):
        lines.append("## Page Sections\n")
        for h in page["headings"]:
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

    end_user_pages = []
    admin_pages = []

    for page in manifest["pages"]:
        slug = slugify(page["name"])
        name_lower = page["name"].lower()
        is_admin = any(k in name_lower for k in ["admin", "setting", "config", "manage user", "user management", "permission"])
        section = "admin" if is_admin else "end-users"

        content = generate_page_doc(page, module, section)
        out_path = docs_dir / section / f"{slug}.md"
        out_path.write_text(content)
        print(f"  Written: {out_path}")

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
