#!/usr/bin/env python3
"""MiniMax Image Generation CLI (model: image-01).

Translates ``scripts/image/generate_image.sh`` to idiomatic Python.
Imports shared helpers from ``_common.py``.

Usage:
    python minimax_image.py --prompt "A cat on a rooftop at sunset" --output cat.png
    python minimax_image.py --mode i2i --prompt "A girl reading" --ref-image face.jpg --output girl.png
    python minimax_image.py --prompt "Mountain landscape" --aspect-ratio 16:9 -n 3 --output landscape.png
"""

import argparse
import base64
import mimetypes
import sys
from pathlib import Path

from _common import api_request, download_file, ensure_dir, get_api_host, get_api_key

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_MODEL = "image-01"
API_PATH = "/v1/image_generation"

PROMPT_MAX_LENGTH = 1500
IMAGE_COUNT_MIN = 1
IMAGE_COUNT_MAX = 9
DIMENSION_MIN = 512
DIMENSION_MAX = 2048

VALID_ASPECT_RATIOS = {"1:1", "16:9", "4:3", "3:2", "2:3", "3:4", "9:16", "21:9"}

VALID_MODES = {"t2i", "i2i"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def image_to_data_url(path: str) -> str:
    """Read a local image file and return a ``data:`` URI with base64 content."""
    file_path = Path(path)
    if not file_path.is_file():
        print(f"Error: Image not found: {path}", file=sys.stderr)
        sys.exit(1)

    mime_type, _ = mimetypes.guess_type(str(file_path))
    if not mime_type:
        mime_type = "image/jpeg"

    with open(file_path, "rb") as fh:
        b64_content = base64.b64encode(fh.read()).decode("ascii")

    return f"data:{mime_type};base64,{b64_content}"


def resolve_image(input_value: str) -> str:
    """Return *input_value* as-is if it is a URL or data URI, otherwise convert local file."""
    if not input_value:
        return ""
    if input_value.startswith(("http://", "https://", "data:")):
        return input_value
    return image_to_data_url(input_value)


def build_payload(args: argparse.Namespace) -> dict:
    """Construct the JSON request body from parsed CLI arguments."""
    payload = {
        "model": DEFAULT_MODEL,
        "prompt": args.prompt,
        "response_format": "url",
        "n": args.n,
        "prompt_optimizer": args.prompt_optimizer,
        "aigc_watermark": args.aigc_watermark,
    }

    if args.aspect_ratio:
        payload["aspect_ratio"] = args.aspect_ratio
    if args.width:
        payload["width"] = args.width
    if args.height:
        payload["height"] = args.height
    if args.seed is not None:
        payload["seed"] = args.seed

    if args.mode == "i2i":
        if not args.ref_image:
            print("Error: --ref-image is required for i2i mode", file=sys.stderr)
            sys.exit(1)
        img_url = resolve_image(args.ref_image)
        payload["subject_reference"] = [
            {"type": "character", "image_file": img_url}
        ]

    return payload


def parse_output_path(output: str, index: int, total: int) -> Path:
    """Derive the output file path, appending ``_N`` suffix when multiple images."""
    path = Path(output)
    if total <= 1:
        return path

    stem = path.stem
    suffix = path.suffix
    return path.with_name(f"{stem}_{index}{suffix}")


def save_base64_images(b64_list: list[str], output: str) -> None:
    """Decode base64 image data and write each to disk."""
    total = len(b64_list)
    for i, b64_data in enumerate(b64_list, start=1):
        out_path = parse_output_path(output, i, total)
        ensure_dir(out_path.parent)
        image_bytes = base64.b64decode(b64_data)
        with open(out_path, "wb") as fh:
            fh.write(image_bytes)
        print(f"Image saved to: {out_path}")


def save_url_images(url_list: list[str], output: str, no_download: bool) -> None:
    """Download or print each image URL."""
    total = len(url_list)
    if no_download:
        for i, url in enumerate(url_list, start=1):
            print(f"Image URL {i}: {url}")
        print("Use without --no-download to save files automatically.")
        return

    for i, url in enumerate(url_list, start=1):
        out_path = parse_output_path(output, i, total)
        print(f"URL {i}: {url}")
        download_file(url, out_path)
        print(f"Image downloaded to: {out_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="minimax_image",
        description="MiniMax Image Generation CLI (model: image-01)",
    )

    parser.add_argument("--prompt", required=True, help="Image description (max 1500 chars)")
    parser.add_argument("--mode", choices=VALID_MODES, default="t2i",
                        help="Generation mode: t2i (default) or i2i")
    parser.add_argument("--aspect-ratio", dest="aspect_ratio",
                        choices=sorted(VALID_ASPECT_RATIOS),
                        help="Aspect ratio: 1:1, 16:9, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9")
    parser.add_argument("--width", type=int,
                        help=f"Custom width in pixels ({DIMENSION_MIN}-{DIMENSION_MAX}, multiple of 8)")
    parser.add_argument("--height", type=int,
                        help=f"Custom height in pixels ({DIMENSION_MIN}-{DIMENSION_MAX}, multiple of 8)")
    parser.add_argument("-n", "--count", dest="n", type=int, default=1,
                        help=f"Number of images to generate ({IMAGE_COUNT_MIN}-{IMAGE_COUNT_MAX}, default: 1)")
    parser.add_argument("--seed", type=int, default=None,
                        help="Random seed for reproducibility")
    parser.add_argument("--prompt-optimizer", dest="prompt_optimizer",
                        action="store_true", default=False,
                        help="Enable automatic prompt optimization")
    parser.add_argument("--ref-image", dest="ref_image",
                        help="Character reference image (local file or URL, i2i mode)")
    parser.add_argument("--no-download", dest="no_download",
                        action="store_true", default=False,
                        help="Don't download, just print URL(s)")
    parser.add_argument("--aigc-watermark", dest="aigc_watermark",
                        action="store_true", default=False,
                        help="Add AIGC watermark to generated images")
    parser.add_argument("-o", "--output", required=True, help="Output file path")

    return parser


def validate_args(args: argparse.Namespace) -> None:
    """Validate CLI arguments beyond what argparse checks."""
    if len(args.prompt) > PROMPT_MAX_LENGTH:
        print(f"Error: prompt exceeds {PROMPT_MAX_LENGTH} characters", file=sys.stderr)
        sys.exit(1)

    if not (IMAGE_COUNT_MIN <= args.n <= IMAGE_COUNT_MAX):
        print(f"Error: -n must be between {IMAGE_COUNT_MIN} and {IMAGE_COUNT_MAX}", file=sys.stderr)
        sys.exit(1)

    for dim_name, dim_value in [("width", args.width), ("height", args.height)]:
        if dim_value is not None:
            if dim_value < DIMENSION_MIN or dim_value > DIMENSION_MAX:
                print(
                    f"Error: --{dim_name} must be between {DIMENSION_MIN} and {DIMENSION_MAX}",
                    file=sys.stderr,
                )
                sys.exit(1)
            if dim_value % 8 != 0:
                print(f"Error: --{dim_name} must be a multiple of 8", file=sys.stderr)
                sys.exit(1)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    validate_args(args)

    api_key = get_api_key()
    api_host = get_api_host()
    api_url = f"{api_host}{API_PATH}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = build_payload(args)

    print(f"Mode: {args.mode}")
    print(f"Model: {DEFAULT_MODEL}")
    print(f"Generating {args.n} image(s)...")

    data = api_request("POST", api_url, headers=headers, json_body=payload)

    success_count = data.get("metadata", {}).get("success_count", 0)
    failed_count = data.get("metadata", {}).get("failed_count", 0)
    print(f"Success: {success_count}, Failed: {failed_count}")

    ensure_dir(Path(args.output).parent)

    response_format = "url"
    if response_format == "base64":
        b64_list = data.get("data", {}).get("image_base64", [])
        if not b64_list:
            print("Error: No image data in response", file=sys.stderr)
            sys.exit(1)
        save_base64_images(b64_list, args.output)
    else:
        url_list = data.get("data", {}).get("image_urls", [])
        if not url_list:
            print("Error: No image URLs in response", file=sys.stderr)
            sys.exit(1)
        save_url_images(url_list, args.output, args.no_download)

    print("Done!")


if __name__ == "__main__":
    main()
