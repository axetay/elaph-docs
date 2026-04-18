"""
Blurs all numbers in screenshot images so sensitive figures are not
visible in the published documentation.

Uses Tesseract OCR to locate text regions, then applies a Gaussian blur
to any region whose text is purely numeric (digits, commas, dots, currency
symbols, percentages).

Usage:
    # Mask all screenshots for both modules
    python3 scripts/mask_numbers.py

    # Mask one module only
    python3 scripts/mask_numbers.py --module garage
    python3 scripts/mask_numbers.py --module trucking

    # Dry run — report what would be masked without modifying files
    python3 scripts/mask_numbers.py --dry-run

Requires: pip install pytesseract Pillow
          brew install tesseract        (macOS)
          apt install tesseract-ocr     (Ubuntu)
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import pytesseract
    from PIL import Image, ImageFilter, ImageDraw
except ImportError:
    print("Missing dependencies. Run: pip install pytesseract Pillow")
    sys.exit(1)

# Matches tokens that are purely numeric in nature:
# plain integers, decimals, comma-separated thousands, currency amounts,
# percentages, phone-like digit strings
NUMBER_RE = re.compile(
    r"""^
    [\$£€¥]?          # optional leading currency symbol
    [\d]{1,3}         # first digit group
    ([,\.\s]\d+)*     # optional further groups separated by , . or space
    [%]?              # optional trailing percent
    $""",
    re.VERBOSE,
)

BLUR_RADIUS = 10
MIN_CONFIDENCE = 40   # tesseract confidence threshold (0-100)
PADDING = 2           # extra pixels around each detected region


def is_numeric_token(text: str) -> bool:
    t = text.strip()
    if not t:
        return False
    # Also match plain digit strings that may include separators
    return bool(NUMBER_RE.match(t)) or t.isdigit()


def mask_image(img_path: Path, dry_run: bool = False) -> int:
    """Blur all numeric regions in img_path. Returns number of regions masked."""
    img = Image.open(img_path).convert("RGB")
    width, height = img.size

    try:
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    except Exception as e:
        print(f"  [WARN] OCR failed for {img_path.name}: {e}")
        return 0

    masked = 0
    for i, text in enumerate(data["text"]):
        if not is_numeric_token(text):
            continue
        conf = int(data["conf"][i])
        if conf < MIN_CONFIDENCE:
            continue

        x = max(0, data["left"][i] - PADDING)
        y = max(0, data["top"][i] - PADDING)
        w = data["width"][i] + PADDING * 2
        h = data["height"][i] + PADDING * 2
        x2 = min(width, x + w)
        y2 = min(height, y + h)

        if w <= 0 or h <= 0:
            continue

        if not dry_run:
            region = img.crop((x, y, x2, y2))
            blurred = region.filter(ImageFilter.GaussianBlur(radius=BLUR_RADIUS))
            img.paste(blurred, (x, y))

        masked += 1

    if masked > 0 and not dry_run:
        img.save(img_path)

    return masked


def process_module(module: str, dry_run: bool) -> None:
    screenshots_dir = Path(f"{module}/docs/assets/screenshots")
    if not screenshots_dir.exists():
        print(f"  [SKIP] {screenshots_dir} not found")
        return

    images = sorted(screenshots_dir.glob("*.png")) + sorted(screenshots_dir.glob("*.jpg"))
    if not images:
        print(f"  [SKIP] No images in {screenshots_dir}")
        return

    total = 0
    for img_path in images:
        count = mask_image(img_path, dry_run=dry_run)
        if count:
            label = "(dry run)" if dry_run else "masked"
            print(f"  {img_path.name}: {count} region(s) {label}")
        total += count

    print(f"  {module}: {len(images)} images processed, {total} numeric regions {'found' if dry_run else 'blurred'}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", choices=["garage", "trucking"], help="Process one module only")
    parser.add_argument("--dry-run", action="store_true", help="Report without modifying files")
    args = parser.parse_args()

    modules = [args.module] if args.module else ["garage", "trucking"]
    mode = "DRY RUN — " if args.dry_run else ""
    print(f"{mode}Masking numbers in screenshots...")

    for module in modules:
        process_module(module, dry_run=args.dry_run)

    print("Done.")


if __name__ == "__main__":
    main()
