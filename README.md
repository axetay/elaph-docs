# elaph-docs

Auto-generated user manuals for U-Go Zoho Creator apps, built with Playwright, Claude AI, and MkDocs Material.

**Live docs:** https://axetay.github.io/elaph-docs/

## Overview

Two documentation sites are generated from this repo:

| Module | App | Theme |
|--------|-----|-------|
| `garage/` | U-Go Garage Maintenance | Blue |
| `trucking/` | U-Go Trucking Management System | Teal |

### Pipeline

```
Zoho Creator app
      │
      ▼
scripts/crawl.py          →  scripts/<module>_manifest.json
      │                       (screenshots, fields, buttons, table columns)
      ▼
scripts/enrich_manifest.py →  scripts/<module>_manifest_enriched.json
      │                        (+ Claude descriptions, workflows, field explanations)
      ▼
scripts/generate_docs.py   →  <module>/docs/**/*.md  +  <module>/mkdocs.yml
      │
      ▼
mkdocs build               →  <module>/site/
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure credentials

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```env
ZOHO_EMAIL=your@email.com
ZOHO_PASSWORD=yourpassword
ANTHROPIC_API_KEY=sk-ant-...
```

`.env` is gitignored — never commit it.

---

## Regenerating docs from saved manifests

The enriched manifests are already committed, so you can regenerate the Markdown and rebuild the sites **without crawling or spending API tokens**:

```bash
# Garage
python3 scripts/generate_docs.py \
    --manifest scripts/garage_manifest_enriched.json \
    --module garage
mkdocs build -f garage/mkdocs.yml

# Trucking
python3 scripts/generate_docs.py \
    --manifest scripts/trucking_manifest_enriched.json \
    --module trucking
mkdocs build -f trucking/mkdocs.yml
```

Preview locally:

```bash
mkdocs serve -f garage/mkdocs.yml    # http://127.0.0.1:8000
mkdocs serve -f trucking/mkdocs.yml  # http://127.0.0.1:8000
```

---

## Re-crawling (when the app changes)

Run the crawler against the live Zoho app to produce a fresh raw manifest:

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

---

## Re-enriching with Claude (when content needs refreshing)

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

After enriching, commit the updated manifest files so future developers don't need to re-enrich.

---

## Adding or reordering pages

Page groupings and sidebar order are defined in `scripts/hierarchy.py`:

```python
HIERARCHIES = {
    "garage": [...],
    "trucking": [...],
}
```

Each entry is a dict with a `section` name and a list of `pages` (exact page names as they appear in the manifest). After editing, regenerate docs — the nav in `mkdocs.yml` is rewritten automatically.

---

## GitHub Pages deployment

Docs are deployed automatically on every push to `main` via `.github/workflows/deploy-docs.yml`.

To enable it the first time:
1. Go to **Settings → Pages** in the GitHub repo
2. Set **Source** to **GitHub Actions**
3. Merge this branch to `main` — the workflow will build and publish both sites

Published URLs:
- https://axetay.github.io/elaph-docs/garage/
- https://axetay.github.io/elaph-docs/trucking/

---

## Project structure

```
.
├── scripts/
│   ├── crawl.py                      # Playwright crawler
│   ├── enrich_manifest.py            # Claude API enrichment
│   ├── generate_docs.py              # Markdown + nav generator
│   ├── hierarchy.py                  # Page groupings for both apps
│   ├── garage_manifest.json          # Raw crawl output (garage)
│   ├── garage_manifest_enriched.json # AI-enriched manifest (garage)
│   ├── trucking_manifest.json        # Raw crawl output (trucking)
│   └── trucking_manifest_enriched.json
├── garage/
│   ├── mkdocs.yml
│   └── docs/
│       ├── index.md
│       ├── assets/screenshots/
│       ├── end-users/               # One .md per page
│       └── admin/
├── trucking/
│   └── (same structure)
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Manifest format

Each manifest is a JSON object `{ "pages": [...] }`. A raw page entry:

```json
{
  "name": "Fuel Entries",
  "url": "https://...",
  "screenshot": "/abs/path/to/fuel-entries.png",
  "fields": [
    { "label": "Vehicle", "type": "select", "required": true }
  ],
  "table_columns": ["Date", "Vehicle", "Litres", "Cost"],
  "buttons": ["Add", "Export"],
  "headings": [{ "tag": "h2", "text": "Fuel Entries" }]
}
```

After enrichment, each page gains:

```json
{
  "description": "...",
  "how_to_use": ["Step 1 ...", "Step 2 ..."],
  "field_descriptions": { "Vehicle": "Select the truck being refuelled." },
  "tips": ["..."]
}
```
