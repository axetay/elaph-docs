# Manual Enrichment Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform the screenshot gallery into a real user manual with logical hierarchy, Claude-generated descriptions/workflows/field explanations, and cross-hyperlinks between related pages.

**Architecture:** Three new scripts work together: `hierarchy.py` defines the logical page groupings for each app; `enrich_manifest.py` calls the Claude API (Haiku) to generate descriptions, step-by-step workflows, and field explanations for each page, writing an enriched JSON manifest; `generate_docs.py` is updated to read enriched manifests, emit nested MkDocs nav sections, render rich page templates, and inject "Related Pages" cross-links from hierarchy siblings.

**Tech Stack:** Python 3.11+, `anthropic` SDK (Haiku 4.5), `mkdocs-material`, existing `.venv/`

---

## Pre-flight

The `.venv/` already has all dependencies except `anthropic`. The `.env` file already has `ZOHO_EMAIL`/`ZOHO_PASSWORD` — the Anthropic API key must also be in `.env`:

```
ANTHROPIC_API_KEY=sk-ant-...
```

All commands run from the repo root. Use `.venv/bin/python3` for all Python invocations.

---

### Task 1: Page Hierarchy Definition

**Files:**
- Create: `scripts/hierarchy.py`

**Step 1: Create `scripts/hierarchy.py`**

```python
"""
Defines the logical section groupings for each app's pages.
Used by enrich_manifest.py and generate_docs.py.
"""

GARAGE_HIERARCHY = [
    {
        "section": "Overview",
        "pages": ["Fleet Management Dashboard"],
    },
    {
        "section": "Maintenance Management",
        "description": "Create and track vehicle maintenance orders, repairs, and service history.",
        "pages": [
            "Maintenance Order",
            "All Maintenance Orders",
            "Repair Maintenance This Month",
            "Repair Details",
            "All Repair Details",
        ],
    },
    {
        "section": "Spare Parts",
        "description": "Manage spare parts inventory, stock levels, transactions, and requests.",
        "pages": [
            "All Spare Parts",
            "Spare Part Stock",
            "All Spare Part Stocks",
            "Spare Part Transactions",
            "All Spare Part Transactions",
            "Request Spare Parts",
            "Request Spare Parts Report",
        ],
    },
    {
        "section": "Procurement",
        "description": "Raise and track purchase orders for parts and supplies.",
        "pages": [
            "Purchase Orders",
            "All Purchase Orders",
            "Auto PO Items",
            "All Auto PO Items",
        ],
    },
    {
        "section": "Fuel Management",
        "description": "Record fuel consumption, analyse vehicle fuel efficiency, and track costs.",
        "pages": [
            "Fuel Control",
            "All Fuel Controls",
            "Fuel Entries",
            "All Fuel Entries",
            "Fuel \u2013 Vehicle Performance Summary",
            "Worst Vehicles Report",
            "Cost Per KM",
        ],
    },
    {
        "section": "Fleet & Drivers",
        "description": "Manage vehicle records, driver profiles, and driver KPI evaluations.",
        "pages": [
            "Vehicles",
            "All Vehicles",
            "Vehicles Summary Report",
            "All Drivers",
            "Driver KPI Evaluation",
            "All Driver Kpi Evaluations",
        ],
    },
    {
        "section": "Vehicle Fleet Reports",
        "description": "Per-vehicle detailed reports grouped by fleet category (M1–M4).",
        "pages": [
            "M1 Truck Report",
            "M1 Flat Bed Trailer Report",
            "M1 Boxed Trailer Report",
            "M1 Reefer Trailer Report",
            "M2 Truck Report",
            "M2 Flat Bed Trailer Report",
            "M2 Boxed Trailer Report",
            "M2 Reefer Trailer Report",
            "M3 Truck Report",
            "M3 Flat Bed Trailer Report",
            "M3 Boxed Trailer Report",
            "M3 Reefer Trailer Report",
            "M4 Truck Report",
            "M4 Flat Bed Trailer Report",
            "M4 Boxed Trailer Report",
            "M4 Reefer Trailer Report",
        ],
    },
    {
        "section": "Automation",
        "description": "Configure automation rules that trigger actions based on system events.",
        "pages": [
            "Automation Control",
            "All Automation Controls",
        ],
    },
]

TRUCKING_HIERARCHY = [
    {
        "section": "Overview",
        "pages": ["UGO Trucking Dashboard"],
    },
    {
        "section": "Job Orders",
        "description": "Create and manage trucking job orders across all transport types.",
        "pages": [
            "Job Orders",
            "All Job Orders",
            "Import / Export Job Orders",
            "Domestic Job Orders",
            "Subcontractor Job Orders",
            "Cross Border Job Orders",
        ],
    },
    {
        "section": "Shipments",
        "description": "Record shipment details linked to job orders for each transport type.",
        "pages": [
            "Shipment Details",
            "All Shipment Details",
            "Domestic Shipment Details",
            "All Domestic Shipment Details",
            "Subcontractor Shipment Details",
            "All Subcontractor Shipment Details",
            "Cross Border Shipment Details",
            "All Cross Border Shipment Details",
        ],
    },
    {
        "section": "Finance",
        "description": "Manage driver cash advances, expense settlements, and wage records.",
        "pages": [
            "Cash Advance Requests & Settlements",
            "All Cash Advance Requests & Settlements",
            "Open Cash Advances",
            "Unsettled Cash Advances",
            "Driver Expenses & Wages Form",
            "Driver Expenses & Wages Form Report",
            "Driver Unpaid Summary",
        ],
    },
    {
        "section": "Master Data",
        "description": "Reference data for clients, vendors, locations, routes, and port representatives.",
        "pages": [
            "Port Representatives Master Data Report",
            "Clients Master Data Report",
            "Vendors Master Data Report",
            "All Locations Master Data",
            "Routes Master Data",
            "Routes Master Data Report",
            "Driver Trip Allowances Master Data",
            "Driver Trip Allowances Master Data Report",
        ],
    },
]

HIERARCHIES = {
    "garage": GARAGE_HIERARCHY,
    "trucking": TRUCKING_HIERARCHY,
}
```

**Step 2: Verify no syntax errors**

```bash
.venv/bin/python3 -c "import sys; sys.path.insert(0,'scripts'); from hierarchy import HIERARCHIES; print('OK —', sum(len(g['pages']) for g in HIERARCHIES['garage']), 'garage pages,', sum(len(g['pages']) for g in HIERARCHIES['trucking']), 'trucking pages')"
```

Expected: `OK — 48 garage pages, 30 trucking pages`

**Step 3: Commit**

```bash
git add scripts/hierarchy.py
git commit -m "feat: define page hierarchy for garage and trucking apps"
```

---

### Task 2: Claude API Enrichment Script

**Files:**
- Create: `scripts/enrich_manifest.py`
- Modify: `requirements.txt` (add `anthropic`)
- Modify: `.env.example` (add `ANTHROPIC_API_KEY`)

**Step 1: Add anthropic to requirements and install**

Add to `requirements.txt`:
```
anthropic>=0.40.0
```

Install:
```bash
.venv/bin/pip install anthropic 2>&1 | tail -3
```

Expected: `Successfully installed anthropic-...`

**Step 2: Add ANTHROPIC_API_KEY to `.env.example`**

```
ZOHO_EMAIL=your@email.com
ZOHO_PASSWORD=yourpassword
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Step 3: Create `scripts/enrich_manifest.py`**

```python
"""
Enriches a crawler manifest with Claude-generated descriptions, workflows,
and field explanations.

Usage:
    python scripts/enrich_manifest.py --manifest scripts/garage_manifest.json \
        --module garage --out scripts/garage_manifest_enriched.json
    python scripts/enrich_manifest.py --manifest scripts/trucking_manifest.json \
        --module trucking --out scripts/trucking_manifest_enriched.json
"""

import argparse
import json
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
import anthropic

sys.path.insert(0, str(Path(__file__).parent))
from hierarchy import HIERARCHIES

load_dotenv()

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5-20251001"

APP_NAMES = {
    "garage": "U-Go Garage Maintenance System",
    "trucking": "U-Go Trucking Management System",
}

SYSTEM = (
    "You are a technical writer producing user manuals for a logistics company. "
    "Write in plain, direct English for operations staff, not developers. "
    "Always respond with valid JSON only — no markdown fences."
)


def enrich_page(page: dict, module: str, section: str) -> dict:
    fields_text = "\n".join(
        f"  - {f['label']} ({f['type']}, {'required' if f['required'] else 'optional'})"
        for f in page.get("fields", [])[:30]
    ) or "  (no form fields)"

    buttons = ", ".join(page.get("buttons", [])[:15]) or "(none)"
    cols = ", ".join(page.get("table_columns", [])[:15]) or "(none)"

    prompt = f"""App: {APP_NAMES[module]}
Section: {section}
Page: {page['name']}

Form fields:
{fields_text}

Buttons: {buttons}
Table columns: {cols}

Return a JSON object with exactly these keys:
{{
  "description": "2-3 sentences: what this page does, who uses it, and when in their workflow",
  "how_to_use": ["step 1", "step 2", "..."],
  "field_descriptions": {{"Field Label": "what to enter and why"}},
  "tips": ["tip 1", "tip 2"]
}}

Rules:
- how_to_use: 4-7 concrete steps for the most common task on this page
- field_descriptions: only fields needing explanation (skip self-evident ones like 'Date')
- tips: 1-2 practical notes about common mistakes or important things to know
- Write for a logistics operations user, not a developer"""

    resp = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    text = resp.content[0].text.strip()
    return json.loads(text)


def enrich_manifest(manifest_path: str, module: str, out_path: str) -> None:
    with open(manifest_path) as f:
        manifest = json.load(f)

    hierarchy = HIERARCHIES[module]
    page_section = {name: g["section"] for g in hierarchy for name in g["pages"]}

    enriched = []
    total = len(manifest["pages"])

    for i, page in enumerate(manifest["pages"]):
        section = page_section.get(page["name"], "General")
        print(f"  [{i+1}/{total}] {page['name']} ({section})")
        try:
            extra = enrich_page(page, module, section)
        except Exception as e:
            print(f"    WARN: {e} — using fallback")
            extra = {
                "description": f"This page manages {page['name'].lower()} records.",
                "how_to_use": ["Open this page from the sidebar.", "Review or enter the required information.", "Save your changes."],
                "field_descriptions": {},
                "tips": [],
            }
        enriched.append({**page, **extra})
        time.sleep(0.1)

    out = {**manifest, "pages": enriched}
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved: {out_path} ({total} pages)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--module", required=True, choices=["garage", "trucking"])
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    enrich_manifest(args.manifest, args.module, args.out)
```

**Step 4: Verify syntax**

```bash
.venv/bin/python3 -c "import ast; ast.parse(open('scripts/enrich_manifest.py').read()); print('Syntax OK')"
```

Expected: `Syntax OK`

**Step 5: Commit**

```bash
git add scripts/enrich_manifest.py requirements.txt .env.example
git commit -m "feat: add Claude API enrichment script for manifest pages"
```

---

### Task 3: Run Enrichment — Garage App

**Step 1: Add ANTHROPIC_API_KEY to .env**

Ensure `.env` contains:
```
ANTHROPIC_API_KEY=sk-ant-...
```

**Step 2: Run enrichment**

```bash
.venv/bin/python3 scripts/enrich_manifest.py \
  --manifest scripts/garage_manifest.json \
  --module garage \
  --out scripts/garage_manifest_enriched.json
```

Expected: 48 lines of `[N/48] Page Name (Section)`, then `Saved: scripts/garage_manifest_enriched.json`

**Step 3: Spot-check output**

```bash
.venv/bin/python3 -c "
import json
m = json.load(open('scripts/garage_manifest_enriched.json'))
p = m['pages'][0]
print('Page:', p['name'])
print('Description:', p.get('description','MISSING'))
print('Steps:', len(p.get('how_to_use',[])))
print('Fields described:', len(p.get('field_descriptions',{})))
print('Tips:', len(p.get('tips',[])))
"
```

Expected: description present, 4-7 steps, some field descriptions.

**Step 4: Add to .gitignore (enriched manifests are generated artifacts)**

Add to `.gitignore`:
```
scripts/garage_manifest_enriched.json
scripts/trucking_manifest_enriched.json
```

---

### Task 4: Run Enrichment — Trucking App

**Step 1: Run enrichment**

```bash
.venv/bin/python3 scripts/enrich_manifest.py \
  --manifest scripts/trucking_manifest.json \
  --module trucking \
  --out scripts/trucking_manifest_enriched.json
```

Expected: 30 lines of progress, then saved message.

**Step 2: Verify**

```bash
.venv/bin/python3 -c "
import json
m = json.load(open('scripts/trucking_manifest_enriched.json'))
print(f'{len(m[\"pages\"])} pages enriched')
missing = [p['name'] for p in m['pages'] if not p.get('description')]
print('Missing description:', missing or 'none')
"
```

Expected: `30 pages enriched`, `Missing description: none`

---

### Task 5: Update generate_docs.py — Hierarchy, Rich Content, Cross-links

**Files:**
- Modify: `scripts/generate_docs.py`

Replace the entire file with the following:

```python
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
        if page.get("fields"):
            field_descriptions = page.get("field_descriptions", {})
            lines.append("## Form Fields\n")
            lines.append("| Field | Description | Type | Required |")
            lines.append("|-------|-------------|------|----------|")
            for f in page["fields"]:
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

    # Build page lookup
    page_lookup = {p["name"]: p for p in manifest["pages"]}

    # Build hierarchy-aware nav
    hierarchy = HIERARCHIES[module]
    page_section = {name: g["section"] for g in hierarchy for name in g["pages"]}

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
```

**Step 2: Verify syntax**

```bash
.venv/bin/python3 -c "import ast; ast.parse(open('scripts/generate_docs.py').read()); print('Syntax OK')"
```

Expected: `Syntax OK`

**Step 3: Commit**

```bash
git add scripts/generate_docs.py
git commit -m "feat: update doc generator — hierarchy nav, enriched content, cross-links"
```

---

### Task 6: Regenerate Docs and Verify Both Sites

**Step 1: Generate garage docs from enriched manifest**

```bash
.venv/bin/python3 scripts/generate_docs.py \
  --manifest scripts/garage_manifest_enriched.json \
  --module garage
```

Expected: 48 files written, `Updated nav in garage/mkdocs.yml (8 sections)`

**Step 2: Generate trucking docs from enriched manifest**

```bash
.venv/bin/python3 scripts/generate_docs.py \
  --manifest scripts/trucking_manifest_enriched.json \
  --module trucking
```

Expected: 30 files written, `Updated nav in trucking/mkdocs.yml (5 sections)`

**Step 3: Build both sites strictly**

```bash
cd garage && ../.venv/bin/mkdocs build --strict 2>&1 | grep -E "INFO|ERROR|Aborted"
cd ../trucking && ../.venv/bin/mkdocs build --strict 2>&1 | grep -E "INFO|ERROR|Aborted"
```

Expected: `INFO - Documentation built!` for both, no errors.

**Step 4: Spot-check a page in browser**

Serve garage:
```bash
cd garage && ../.venv/bin/mkdocs serve --dev-addr 127.0.0.1:8001 &
```

Open `http://127.0.0.1:8001`. Verify:
- Nav shows nested sections (Overview, Maintenance Management, Spare Parts, etc.)
- A page like "Maintenance Order" has a Description paragraph, numbered How to Use steps, Form Fields table with descriptions, Related Pages links to sibling pages in Maintenance Management.

**Step 5: Commit**

```bash
git add garage/docs/ trucking/docs/ garage/mkdocs.yml trucking/mkdocs.yml .gitignore
git commit -m "feat: regenerate manual with hierarchy, enriched content, and cross-links"
```

---

## Troubleshooting

**`json.JSONDecodeError` from enrich_manifest.py:**
Claude occasionally wraps JSON in markdown fences. The script strips ` ```json ` fences. If it still fails, check `resp.content[0].text` — add a `print(text)` before `json.loads(text)` temporarily.

**`anthropic.AuthenticationError`:**
Check that `ANTHROPIC_API_KEY` is set correctly in `.env`.

**Nav pages missing from build:**
If `mkdocs build --strict` reports a nav file not found, that page name in the hierarchy doesn't match the manifest. Run:
```bash
python3 -c "import json; m=json.load(open('scripts/garage_manifest_enriched.json')); print([p['name'] for p in m['pages']])"
```
and cross-check with `hierarchy.py`.

**Related pages linking to wrong path:**
All pages are in `end-users/` flat. Cross-links are relative (`sibling-slug.md`, not `../end-users/sibling-slug.md`) because both source and target are in the same directory.
