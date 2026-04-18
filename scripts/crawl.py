"""
Crawls a Zoho Creator app with Playwright.
Captures screenshots and extracts page structure into a JSON manifest.

Usage:
    python scripts/crawl.py --app garage --url "https://..." --out scripts/garage_manifest.json
    python scripts/crawl.py --app trucking --url "https://..." --out scripts/trucking_manifest.json

Credentials are loaded from a .env file in the repo root:
    ZOHO_EMAIL=your@email.com
    ZOHO_PASSWORD=yourpassword
"""

import argparse
import json
import os
import re
import time
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page, TimeoutError as PWTimeout

load_dotenv()

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

    fields = page.evaluate("""() => {
        const inputs = [...document.querySelectorAll('input, select, textarea')];
        return inputs.map(el => ({
            label: el.labels?.[0]?.innerText?.trim() || el.placeholder || el.name || el.id || '',
            type: el.tagName.toLowerCase() === 'select' ? 'dropdown' : (el.type || el.tagName.toLowerCase()),
            required: el.required,
            name: el.name || el.id || ''
        })).filter(f => f.label);
    }""")

    buttons = page.evaluate("""() => {
        return [...document.querySelectorAll('button, input[type=submit], a[role=button], [class*=btn]')]
            .map(el => el.innerText?.trim() || el.value || '')
            .filter(t => t.length > 0 && t.length < 80);
    }""")

    table_columns = page.evaluate("""() => {
        return [...document.querySelectorAll('th, [class*=column-header], [class*=col-header]')]
            .map(el => el.innerText?.trim())
            .filter(t => t && t.length > 0);
    }""")

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
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        login_if_required(page, start_url)

        print(f"Navigating to start URL: {start_url}")
        page.goto(start_url, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(3000)

        nav_links = get_nav_links(page)
        print(f"Discovered {len(nav_links)} navigation links")

        entry_data = extract_page_data(page, page.url, "Dashboard", screenshot_dir)
        manifest["pages"].append(entry_data)
        visited_urls.add(page.url)

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
