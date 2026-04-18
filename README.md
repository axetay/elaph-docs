# elaph-docs

Auto-generated user manuals for U-Go Zoho Creator apps, built with Playwright,
Claude AI, and MkDocs Material. The pipeline crawls the live apps, captures
screenshots, enriches each page with AI-generated descriptions and workflows,
and publishes two documentation sites to GitHub Pages.

**Live docs:** https://axetay.github.io/elaph-docs/

---

## How it works

The pipeline has four stages that run in sequence:

```
Zoho Creator app
      │
      ▼
scripts/crawl.py            →  scripts/<module>_manifest.json
                                (screenshots, fields, buttons, table columns)
      │
      ▼
scripts/enrich_manifest.py  →  scripts/<module>_manifest_enriched.json
                                (+ descriptions, workflows, field explanations)
      │
      ▼
scripts/filter_fields.py    →  scripts/<module>_manifest_enriched.json
                                (fields filtered to screenshot-visible only)
      │
      ▼
scripts/generate_docs.py    →  <module>/docs/**/*.md + <module>/mkdocs.yml
      │
      ▼
mkdocs build                →  deployed to GitHub Pages on push to main
```

Two modules are built from the same pipeline:

| Module | App |
|---|---|
| `garage/` | U-Go Garage Maintenance System |
| `trucking/` | U-Go Trucking Management System |

---

## Setup

### Prerequisites

- Python 3.11+
- Tesseract OCR (`brew install tesseract` on macOS,
  `apt install tesseract-ocr` on Ubuntu)

### Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### Configure credentials

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
ZOHO_EMAIL=your@email.com
ZOHO_PASSWORD=yourpassword
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

`.env` is gitignored — never commit it.

---

## Update workflow

Use this guide to decide which steps to run when the docs need updating.

### When the Zoho app UI changes

Run this when pages are added, removed, renamed, or their fields change.

**Step 1: Crawl the live app**

```bash
python3 scripts/crawl.py \
    --app garage \
    --url "https://creatorapp.zoho.com/m.fahmy_ugologistics/u-go-garage-maintenance" \
    --out scripts/garage_manifest.json

python3 scripts/crawl.py \
    --app trucking \
    --url "https://creatorapp.zoho.com/m.fahmy_ugologistics/u-go-trucking-management-system" \
    --out scripts/trucking_manifest.json
```

Screenshots are saved to `<module>/docs/assets/screenshots/`.

**Step 2: Enrich with Claude**

```bash
python3 scripts/enrich_manifest.py \
    --manifest scripts/garage_manifest.json \
    --module garage \
    --out scripts/garage_manifest_enriched.json

python3 scripts/enrich_manifest.py \
    --manifest scripts/trucking_manifest.json \
    --module trucking \
    --out scripts/trucking_manifest_enriched.json
```

Uses `claude-haiku-4-5-20251001`. Reads `ANTHROPIC_API_KEY` from `.env`.

**Step 3: Filter fields to screenshot-visible only**

```bash
python3 scripts/filter_fields.py \
    --manifest scripts/garage_manifest_enriched.json \
    --out scripts/garage_manifest_enriched.json

python3 scripts/filter_fields.py \
    --manifest scripts/trucking_manifest_enriched.json \
    --out scripts/trucking_manifest_enriched.json
```

**Step 4: Regenerate docs**

```bash
python3 scripts/generate_docs.py \
    --manifest scripts/garage_manifest_enriched.json \
    --module garage

python3 scripts/generate_docs.py \
    --manifest scripts/trucking_manifest_enriched.json \
    --module trucking
```

**Step 5: Commit and push**

```bash
git add scripts/ garage/docs/ trucking/docs/
git commit -m "docs: regenerate from updated crawl"
git push origin main
```

Pushing to `main` triggers the GitHub Actions workflow, which builds and
deploys both sites automatically.

---

### When only the content needs refreshing

Run this when the app UI hasn't changed but you want fresher AI-generated
descriptions or workflows. Skip the crawl step and start from step 2 above,
using the existing `*_manifest.json` files.

---

### When regenerating from saved manifests

The enriched manifests are committed to the repo. If you only need to rebuild
the Markdown and sites without crawling or spending API tokens:

```bash
python3 scripts/generate_docs.py \
    --manifest scripts/garage_manifest_enriched.json \
    --module garage

python3 scripts/generate_docs.py \
    --manifest scripts/trucking_manifest_enriched.json \
    --module trucking
```

Preview locally before pushing:

```bash
mkdocs serve -f garage/mkdocs.yml    # http://127.0.0.1:8000
mkdocs serve -f trucking/mkdocs.yml  # http://127.0.0.1:8000
```

---

### When adding or reordering pages

Page groupings and sidebar order are defined in `scripts/hierarchy.py`. Each
module has a list of sections, and each section has an ordered list of page
names (exactly as they appear in the manifest).

```python
HIERARCHIES = {
    "garage": [
        {
            "section": "Fuel Management",
            "pages": ["Fuel Control", "All Fuel Controls", ...],
        },
        ...
    ],
    "trucking": [...],
}
```

After editing `hierarchy.py`, run the regenerate step (step 4 above). The
`mkdocs.yml` nav is rewritten automatically.

---

## Masking numbers in screenshots

The CI workflow automatically blurs numeric regions in screenshots before
publishing to avoid exposing sensitive figures. To run this locally:

```bash
# Blur all screenshots in-place
python3 scripts/mask_numbers.py

# Preview which regions would be blurred without modifying files
python3 scripts/mask_numbers.py --dry-run

# One module only
python3 scripts/mask_numbers.py --module garage
```

---

## GitHub Pages deployment

Docs are deployed automatically on every push to `main` via
`.github/workflows/deploy-docs.yml`. The workflow:

1. Masks numbers in all screenshots
2. Builds both MkDocs sites
3. Deploys them under a shared root with a landing page

To enable GitHub Pages for the first time:

1. Go to **Settings → Pages** in the GitHub repo.
2. Set **Source** to **GitHub Actions**.
3. Push to `main` — the workflow builds and publishes both sites.

Published URLs:

- https://axetay.github.io/elaph-docs/ (landing page)
- https://axetay.github.io/elaph-docs/garage/
- https://axetay.github.io/elaph-docs/trucking/

---

## Project structure

```
.
├── scripts/
│   ├── crawl.py                        # Playwright crawler
│   ├── enrich_manifest.py              # Claude API enrichment
│   ├── filter_fields.py                # Claude vision field filter
│   ├── generate_docs.py                # Markdown + nav generator
│   ├── hierarchy.py                    # Page groupings and sidebar order
│   ├── mask_numbers.py                 # Screenshot number blurring
│   ├── garage_manifest.json            # Raw crawl output (garage)
│   ├── garage_manifest_enriched.json   # AI-enriched manifest (garage)
│   ├── trucking_manifest.json          # Raw crawl output (trucking)
│   └── trucking_manifest_enriched.json # AI-enriched manifest (trucking)
├── garage/
│   ├── mkdocs.yml
│   └── docs/
│       ├── index.md
│       ├── assets/screenshots/
│       └── <section>/<page>.md
├── trucking/
│   └── (same structure)
├── index.html                          # Root landing page
├── requirements.txt
├── .env.example
└── .github/workflows/deploy-docs.yml
```

---

## Manifest format

Each manifest is a JSON object `{ "pages": [...] }`. A raw page entry looks
like this:

```json
{
  "name": "Fuel Entries",
  "url": "https://...",
  "screenshot": "garage/docs/assets/screenshots/fuel-entries.png",
  "fields": [
    { "label": "Vehicle", "type": "select", "required": true }
  ],
  "table_columns": ["Date", "Vehicle", "Litres", "Cost"],
  "buttons": ["Add", "Export"],
  "headings": [{ "tag": "h2", "text": "Fuel Entries" }]
}
```

After enrichment and field filtering, each page gains:

```json
{
  "description": "Record fuel consumption for a specific vehicle.",
  "how_to_use": ["Step 1: Select the vehicle.", "Step 2: Enter litres."],
  "field_descriptions": { "Vehicle": "The truck being refuelled." },
  "tips": ["Cross-check with the vehicle logbook before submitting."]
}
```
