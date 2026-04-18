"""
Uses Claude vision to compare each page's screenshot against its field list
and keeps only fields that are actually visible in the screenshot.

Reads an enriched manifest, updates the 'fields' and 'field_descriptions'
keys for each page that has a screenshot, and writes the result.

Usage:
    python3 scripts/filter_fields.py \
        --manifest scripts/garage_manifest_enriched.json \
        --out scripts/garage_manifest_enriched.json

    python3 scripts/filter_fields.py \
        --manifest scripts/trucking_manifest_enriched.json \
        --out scripts/trucking_manifest_enriched.json
"""

import argparse
import base64
import json
import time
from pathlib import Path

from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5-20251001"


def encode_image(path: str) -> tuple[str, str]:
    data = Path(path).read_bytes()
    ext = Path(path).suffix.lower().lstrip(".")
    media_type = "image/png" if ext == "png" else "image/jpeg"
    return base64.standard_b64encode(data).decode(), media_type


def visible_fields(page: dict) -> tuple[list[dict], int]:
    fields = page.get("fields", [])
    if not fields or not page.get("screenshot"):
        return fields, 0

    screenshot_path = page["screenshot"]
    if not Path(screenshot_path).exists():
        return fields, 0

    labels = [f["label"] for f in fields]
    labels_json = json.dumps(labels)

    b64, media_type = encode_image(screenshot_path)

    prompt = (
        "This is a screenshot of a web application page.\n\n"
        f"Below is the full list of field labels extracted from the page HTML:\n{labels_json}\n\n"
        "Return a JSON array containing ONLY the labels that are genuinely visible "
        "as labelled form inputs in the screenshot — input boxes, dropdowns, date pickers, "
        "checkboxes, text areas. Exclude anything not visible as a labelled field. "
        "Use the exact spelling from the input list. Respond with a JSON array only."
    )

    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=512,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": b64,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }],
        )
        text = resp.content[0].text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        visible = set(json.loads(text))
        filtered = [f for f in fields if f["label"] in visible]
        removed = len(fields) - len(filtered)
        return filtered, removed
    except Exception as e:
        print(f"    WARN: vision call failed — {e}")
        return fields, 0


def filter_manifest(manifest_path: str, out_path: str) -> None:
    with open(manifest_path) as f:
        manifest = json.load(f)

    pages = manifest["pages"]
    total_removed = 0

    for i, page in enumerate(pages):
        original_count = len(page.get("fields", []))
        if original_count == 0:
            print(f"  [{i+1}/{len(pages)}] {page['name']} — no fields, skipped")
            continue

        filtered, removed = visible_fields(page)
        pages[i]["fields"] = filtered

        kept_labels = {f["label"] for f in filtered}
        if page.get("field_descriptions"):
            pages[i]["field_descriptions"] = {
                k: v for k, v in page["field_descriptions"].items()
                if k in kept_labels
            }

        total_removed += removed
        print(f"  [{i+1}/{len(pages)}] {page['name']} — kept {len(filtered)}/{original_count} fields{f' (-{removed})' if removed else ''}")
        time.sleep(0.1)

    with open(out_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nDone. {total_removed} non-visible fields removed. Saved: {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    filter_manifest(args.manifest, args.out)
