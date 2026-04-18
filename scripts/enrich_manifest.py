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
