# User Manual Generation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Use Playwright to crawl two Zoho Creator apps, capture screenshots and UI structure, then generate a full MkDocs + Material documentation site for each module in the same repo.

**Architecture:** A Python Playwright crawler visits every page in each app, saves screenshots, and writes a JSON manifest. A doc generator reads the manifest and emits structured Markdown. MkDocs + Material renders the Markdown into a searchable HTML site. Two independent MkDocs sites live under `garage/` and `trucking/` in the same repo.

**Tech Stack:** Python 3.11+, `playwright` (Python), `mkdocs`, `mkdocs-material`, `beautifulsoup4`, `Pillow`

---

## Pre-flight: Authentication Note

Both apps are hosted on Zoho Creator and may require a Zoho login. Before running any crawler task:
- Open the app URL in a browser manually and confirm whether it loads without login or requires authentication.
- If login is required, the crawler will need to authenticate first (Task 4 covers this).
- If the app is publicly accessible, skip the auth step in Task 4.

---

### Task 1: Repo Structure & Shared Dependencies

**Files:**
- Create: `requirements.txt`
- Create: `garage/docs/index.md`
- Create: `trucking/docs/index.md`
- Create: `.gitignore`

**Step 1: Create directory skeleton**

```bash
mkdir -p garage/docs/assets/screenshots
mkdir -p garage/docs/end-users
mkdir -p garage/docs/admin
mkdir -p trucking/docs/assets/screenshots
mkdir -p trucking/docs/end-users
mkdir -p trucking/docs/admin
mkdir -p scripts
```

**Step 2: Create `requirements.txt`**

```
mkdocs>=1.5.3
mkdocs-material>=9.5.0
playwright>=1.43.0
beautifulsoup4>=4.12.0
Pillow>=10.0.0
```

**Step 3: Create `.gitignore`**

```
__pycache__/
*.pyc
.venv/
site/
garage/site/
trucking/site/
scripts/garage_manifest.json
scripts/trucking_manifest.json
```

**Step 4: Create `garage/docs/index.md`**

```markdown
# U-Go Garage Maintenance — User Manual

Welcome to the U-Go Garage Maintenance documentation.

## Sections

- [End Users](end-users/dashboard.md) — Day-to-day operations guide
- [Administrators](admin/overview.md) — System management guide
```

**Step 5: Create `trucking/docs/index.md`**

```markdown
# U-Go Trucking Management System — User Manual

Welcome to the U-Go Trucking Management System documentation.

## Sections

- [End Users](end-users/dashboard.md) — Day-to-day operations guide
- [Administrators](admin/overview.md) — System management guide
```

**Step 6: Install dependencies**

```bash
pip install -r requirements.txt
playwright install chromium
```

Expected: All packages install without error.

**Step 7: Commit**

```bash
git add .
git commit -m "feat: scaffold repo structure and dependencies"
```

---

### Task 2: MkDocs Config — Garage Module

**Files:**
- Create: `garage/mkdocs.yml`

**Step 1: Create `garage/mkdocs.yml`**

```yaml
site_name: U-Go Garage Maintenance — User Manual
site_description: Complete user manual for the U-Go Garage Maintenance application
docs_dir: docs
site_dir: site

theme:
  name: material
  palette:
    - scheme: default
      primary: blue
      accent: blue
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - search.suggest
    - search.highlight
    - content.tabs.link

plugins:
  - search

nav:
  - Home: index.md
  - End Users:
      - end-users/dashboard.md
  - Admin:
      - admin/overview.md
```

**Step 2: Verify config parses**

```bash
cd garage && mkdocs build --strict 2>&1 | head -20
```

Expected: Build succeeds or fails only on missing nav files (not config errors).

**Step 3: Commit**

```bash
cd ..
git add garage/mkdocs.yml
git commit -m "feat: add MkDocs config for garage module"
```

---

### Task 3: MkDocs Config — Trucking Module

**Files:**
- Create: `trucking/mkdocs.yml`

**Step 1: Create `trucking/mkdocs.yml`**

```yaml
site_name: U-Go Trucking Management System — User Manual
site_description: Complete user manual for the U-Go Trucking Management System
docs_dir: docs
site_dir: site

theme:
  name: material
  palette:
    - scheme: default
      primary: teal
      accent: teal
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - search.suggest
    - search.highlight
    - content.tabs.link

plugins:
  - search

nav:
  - Home: index.md
  - End Users:
      - end-users/dashboard.md
  - Admin:
      - admin/overview.md
```

**Step 2: Commit**

```bash
git add trucking/mkdocs.yml
git commit -m "feat: add MkDocs config for trucking module"
```

---

### Task 4: Playwright Crawler Script

**Files:**
- Create: `scripts/crawl.py`

**Step 1: Create `scripts/crawl.py`**

```python
"""
Crawls a Zoho Creator app with Playwright.
Captures screenshots and extracts page structure into a JSON manifest.

Usage:
    python scripts/crawl.py --app garage --url "https://..." --out scripts/garage_manifest.json
    python scripts/crawl.py --app trucking --url "https://..." --out scripts/trucking_manifest.json

If the app requires Zoho login, set env vars:
    ZOHO_EMAIL=your@email.com
    ZOHO_PASSWORD=yourpassword
"""

import argparse
import json
import os
import re
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, TimeoutError as PWTimeout


SCREENSHOT_BASE = {
    "garage": "garage/docs/assets/screenshots",
    "trucking": "trucking/docs/assets/screenshots",
}


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text


def login_if_required(page: Page, url: str) -> None:
    """Attempt Zoho login if credentials are provided and login page is shown."""
    email = os.environ.get("ZOHO_EMAIL")
    password = os.environ.get("ZOHO_PASSWORD")
    if not email or not password:
        return

    page.goto(url, wait_until="networkidle", timeout=30000)
    if "accounts.zoho.com" in page.url or "login" in page.url.lower():
        print("Login page detected — authenticating...")
        page.fill("input[name='LOGIN_ID']", email)
        page.click("button#nextbtn")
        page.wait_for_timeout(1500)
        page.fill("input[name='PASSWORD']", password)
        page.click("button#nextbtn")
        page.wait_for_load_state("networkidle", timeout=20000)
        print("Login complete.")


def extract_page_data(page: Page, url: str, name: str, screenshot_dir: Path) -> dict:
    """Extract structured data from the current page state."""
    slug = slugify(name)
    screenshot_path = screenshot_dir / f"{slug}.png"
    page.screenshot(path=str(screenshot_path), full_page=True)
    print(f"  Screenshot: {screenshot_path}")

    # Extract form fields
    fields = page.evaluate("""() => {
        const inputs = [...document.querySelectorAll('input, select, textarea')];
        return inputs.map(el => ({
            label: el.labels?.[0]?.innerText?.trim() || el.placeholder || el.name || el.id || '',
            type: el.tagName.toLowerCase() === 'select' ? 'dropdown' : (el.type || el.tagName.toLowerCase()),
            required: el.required,
            name: el.name || el.id || ''
        })).filter(f => f.label);
    }""")

    # Extract buttons
    buttons = page.evaluate("""() => {
        return [...document.querySelectorAll('button, input[type=submit], a[role=button], [class*=btn]')]
            .map(el => el.innerText?.trim() || el.value || '')
            .filter(t => t.length > 0 && t.length < 80);
    }""")

    # Extract table column headers
    table_columns = page.evaluate("""() => {
        return [...document.querySelectorAll('th, [class*=column-header], [class*=col-header]')]
            .map(el => el.innerText?.trim())
            .filter(t => t && t.length > 0);
    }""")

    # Extract section headings
    headings = page.evaluate("""() => {
        return [...document.querySelectorAll('h1,h2,h3,h4,[class*=section-title],[class*=form-title]')]
            .map(el => ({ level: el.tagName?.toLowerCase() || 'h3', text: el.innerText?.trim() }))
            .filter(h => h.text && h.text.length > 0 && h.text.length < 120);
    }""")

    return {
        "name": name,
        "slug": slug,
        "url": url,
        "screenshot": str(screenshot_path),
        "headings": headings,
        "fields": fields,
        "buttons": list(set(buttons)),
        "table_columns": list(set(table_columns)),
    }


def get_nav_links(page: Page) -> list[dict]:
    """Extract navigation links from the app shell."""
    links = page.evaluate("""() => {
        const selectors = [
            'nav a', '[class*=nav] a', '[class*=menu] a', '[class*=sidebar] a',
            '[class*=tab] a', 'ul.pages a', 'a[href*="#Page"]'
        ];
        const seen = new Set();
        const results = [];
        for (const sel of selectors) {
            for (const el of document.querySelectorAll(sel)) {
                const href = el.href || '';
                const text = el.innerText?.trim() || el.title || '';
                if (text && href && !seen.has(href)) {
                    seen.add(href);
                    results.push({ text, href });
                }
            }
        }
        return results;
    }""")
    return links


def crawl_app(app: str, start_url: str, out_path: str) -> None:
    screenshot_dir = Path(SCREENSHOT_BASE[app])
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    manifest = {"app": app, "pages": []}
    visited_urls = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False for auth visibility
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # Authenticate if needed
        login_if_required(page, start_url)

        # Navigate to start
        print(f"Navigating to start URL: {start_url}")
        page.goto(start_url, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(3000)  # Let SPA settle

        # Discover nav links from entry page
        nav_links = get_nav_links(page)
        print(f"Discovered {len(nav_links)} navigation links")

        # Always document the entry/dashboard page first
        entry_data = extract_page_data(page, page.url, "Dashboard", screenshot_dir)
        manifest["pages"].append(entry_data)
        visited_urls.add(page.url)

        # Visit each nav link
        to_visit = [l for l in nav_links if l["href"] not in visited_urls]
        for link in to_visit:
            if link["href"] in visited_urls:
                continue
            try:
                print(f"Visiting: {link['text']} — {link['href']}")
                page.goto(link["href"], wait_until="networkidle", timeout=20000)
                page.wait_for_timeout(2000)
                current_url = page.url
                if current_url in visited_urls:
                    continue
                visited_urls.add(current_url)

                page_data = extract_page_data(page, current_url, link["text"], screenshot_dir)
                manifest["pages"].append(page_data)

                # Check for sub-navigation that appeared after clicking
                sub_links = get_nav_links(page)
                for sub in sub_links:
                    if sub["href"] not in visited_urls:
                        to_visit.append(sub)

            except PWTimeout:
                print(f"  Timeout on {link['href']} — skipping")
            except Exception as e:
                print(f"  Error on {link['href']}: {e} — skipping")

        browser.close()

    with open(out_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nManifest saved: {out_path} ({len(manifest['pages'])} pages)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", required=True, choices=["garage", "trucking"])
    parser.add_argument("--url", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    crawl_app(args.app, args.url, args.out)
```

**Step 2: Verify script syntax**

```bash
python -c "import ast; ast.parse(open('scripts/crawl.py').read()); print('Syntax OK')"
```

Expected: `Syntax OK`

**Step 3: Commit**

```bash
git add scripts/crawl.py
git commit -m "feat: add Playwright crawler script"
```

---

### Task 5: Doc Generator Script

**Files:**
- Create: `scripts/generate_docs.py`

**Step 1: Create `scripts/generate_docs.py`**

```python
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
    # e.g. garage/docs/assets/screenshots/dashboard.png -> ../assets/screenshots/dashboard.png
    try:
        return "../" + str(path.relative_to(f"{module}/docs"))
    except ValueError:
        return path.name


def generate_page_doc(page: dict, module: str, section: str) -> str:
    """Generate Markdown content for a single app page."""
    lines = [f"# {page['name']}\n"]

    # Screenshot
    if page.get("screenshot"):
        rel = relative_screenshot_path(page["screenshot"], module)
        lines.append(f"![{page['name']} screenshot]({rel})\n")

    lines.append(f"**URL:** `{page['url']}`\n")

    # Headings / sections found on page
    if page.get("headings"):
        lines.append("## Page Sections\n")
        for h in page["headings"]:
            lines.append(f"- {h['text']}")
        lines.append("")

    # Form fields
    if page.get("fields"):
        lines.append("## Form Fields\n")
        lines.append("| Field | Type | Required |")
        lines.append("|-------|------|----------|")
        for f in page["fields"]:
            required = "Yes" if f.get("required") else "No"
            lines.append(f"| {f['label']} | {f['type']} | {required} |")
        lines.append("")

    # Table columns
    if page.get("table_columns"):
        lines.append("## Table Columns\n")
        for col in page["table_columns"]:
            lines.append(f"- {col}")
        lines.append("")

    # Buttons / actions
    if page.get("buttons"):
        lines.append("## Actions\n")
        for btn in page["buttons"]:
            lines.append(f"- **{btn}**")
        lines.append("")

    # Stub workflow section
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
        # Heuristic: pages with "admin", "setting", "config", "user management" go to admin
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

    # Write overview stubs if missing
    admin_overview = admin_dir / "overview.md"
    if not admin_overview.exists():
        admin_overview.write_text("# Admin Overview\n\nThis section covers administrative functions.\n")

    # Update mkdocs.yml nav
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

    # Replace existing nav block
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
```

**Step 2: Verify script syntax**

```bash
python -c "import ast; ast.parse(open('scripts/generate_docs.py').read()); print('Syntax OK')"
```

Expected: `Syntax OK`

**Step 3: Commit**

```bash
git add scripts/generate_docs.py
git commit -m "feat: add doc generator script"
```

---

### Task 6: Crawl Garage App

**Files:**
- Writes to: `garage/docs/assets/screenshots/`
- Writes to: `scripts/garage_manifest.json`

**Step 1: Run the crawler (set credentials if login is needed)**

```bash
# If login is required:
# export ZOHO_EMAIL="your@email.com"
# export ZOHO_PASSWORD="yourpassword"

python scripts/crawl.py \
  --app garage \
  --url "https://creatorapp.zoho.com/m.fahmy_ugologistics/u-go-garage-maintenance?frameorigin=https://one.zoho.com#Page:Fleet_Management_Dashboard" \
  --out scripts/garage_manifest.json
```

Expected: A browser window opens, visits each page, closes. `scripts/garage_manifest.json` exists with `pages` array.

**Step 2: Verify manifest**

```bash
python -c "
import json
m = json.load(open('scripts/garage_manifest.json'))
print(f'Pages found: {len(m[\"pages\"])}')
for p in m['pages']:
    print(f'  - {p[\"name\"]} ({len(p[\"fields\"])} fields, {len(p[\"buttons\"])} buttons)')
"
```

Expected: At least 3-5 pages listed with fields/buttons data.

**Step 3: Verify screenshots exist**

```bash
ls garage/docs/assets/screenshots/
```

Expected: Multiple `.png` files, one per page.

**Step 4: Commit screenshots and manifest reference**

```bash
git add garage/docs/assets/screenshots/
git add scripts/garage_manifest.json
git commit -m "feat: add garage app crawl results and screenshots"
```

---

### Task 7: Crawl Trucking App

**Files:**
- Writes to: `trucking/docs/assets/screenshots/`
- Writes to: `scripts/trucking_manifest.json`

**Step 1: Run the crawler**

```bash
python scripts/crawl.py \
  --app trucking \
  --url "https://creatorapp.zoho.com/m.fahwy_ugologistics/u-go-trucking-management-system?frameorigin=https://one.zoho.com" \
  --out scripts/trucking_manifest.json
```

Expected: Browser visits all pages. `scripts/trucking_manifest.json` created.

**Step 2: Verify manifest**

```bash
python -c "
import json
m = json.load(open('scripts/trucking_manifest.json'))
print(f'Pages found: {len(m[\"pages\"])}')
for p in m['pages']:
    print(f'  - {p[\"name\"]} ({len(p[\"fields\"])} fields, {len(p[\"buttons\"])} buttons)')
"
```

**Step 3: Commit**

```bash
git add trucking/docs/assets/screenshots/
git add scripts/trucking_manifest.json
git commit -m "feat: add trucking app crawl results and screenshots"
```

---

### Task 8: Generate Markdown Docs

**Step 1: Generate docs for garage**

```bash
python scripts/generate_docs.py --manifest scripts/garage_manifest.json --module garage
```

Expected: Markdown files created in `garage/docs/end-users/` and `garage/docs/admin/`. `garage/mkdocs.yml` nav updated.

**Step 2: Generate docs for trucking**

```bash
python scripts/generate_docs.py --manifest scripts/trucking_manifest.json --module trucking
```

Expected: Markdown files created in `trucking/docs/end-users/` and `trucking/docs/admin/`.

**Step 3: Commit**

```bash
git add garage/docs/ trucking/docs/ garage/mkdocs.yml trucking/mkdocs.yml
git commit -m "feat: generate markdown docs from crawl manifests"
```

---

### Task 9: Build & Verify Both Sites

**Step 1: Build garage site**

```bash
cd garage && mkdocs build --strict 2>&1
```

Expected: `INFO - Documentation built!` with no errors. `garage/site/` directory created.

**Step 2: Serve garage site to verify locally**

```bash
cd garage && mkdocs serve &
```

Open `http://127.0.0.1:8000` — verify nav, screenshots, and search work.

**Step 3: Build trucking site**

```bash
cd trucking && mkdocs build --strict 2>&1
```

Expected: `INFO - Documentation built!` with no errors.

**Step 4: Fix any broken nav references**

If build fails with `Config value 'nav': The page ... is not found`, the nav references a file that wasn't generated. Check the file exists:

```bash
ls garage/docs/end-users/
ls garage/docs/admin/
```

Add any missing stub files:

```bash
echo "# Page Name\n\n_Documentation coming soon._" > garage/docs/end-users/missing-page.md
```

Re-run `mkdocs build --strict` until clean.

**Step 5: Commit site build artifacts (optional)**

```bash
# Only commit if you want to version the built site
# Generally skip this — build on deploy instead
```

---

### Task 10: GitHub Actions Deployment (Optional)

**Files:**
- Create: `.github/workflows/deploy.yml`

**Step 1: Create `.github/workflows/deploy.yml`**

```yaml
name: Deploy Docs

on:
  push:
    branches: [main]

jobs:
  deploy-garage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: cd garage && mkdocs gh-deploy --force --remote-branch gh-pages-garage

  deploy-trucking:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: cd trucking && mkdocs gh-deploy --force --remote-branch gh-pages-trucking
```

**Step 2: Commit**

```bash
git add .github/
git commit -m "feat: add GitHub Actions deployment for both doc sites"
```

---

## Troubleshooting

**App loads a blank page / SPA not rendering:**
- Increase `wait_for_timeout` in `crawl.py` from 3000ms to 5000ms
- Try `wait_until="domcontentloaded"` instead of `networkidle`

**Login page keeps appearing after login:**
- Check `ZOHO_EMAIL` / `ZOHO_PASSWORD` env vars are set correctly
- Run with `headless=False` (already the default) to watch the login flow

**Nav links not discovered:**
- Add new selectors to the `selectors` list in `get_nav_links()` by inspecting the app's HTML in DevTools

**Screenshots are blank/white:**
- Increase the `wait_for_timeout` after `page.goto()` to allow the SPA to render

**mkdocs build fails on nav:**
- Run `generate_docs.py` again after fixing the manifest
- Or manually create stub `.md` files for any missing pages
