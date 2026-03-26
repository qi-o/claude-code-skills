#!/usr/bin/env python3
"""MiniMax Image generation (text-to-image and image-to-image)"""

import argparse
import base64
import os
import sys
import requests
from pathlib import Path

API_BASE = os.environ.get("MINIMAX_API_HOST", "https://api.minimax.io")
ENDPOINT = f"{API_BASE}/v1/image_generation"

def get_api_key():
    key = os.environ.get("MINIMAX_API_KEY")
    if not key:
        f = Path(__file__).resolve()
        env_path = f.parents[3] / "env.d" / "minimax.env"
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("MINIMAX_API_KEY="):
                    return line.split("=", 1)[1].strip()
        raise SystemExit("MINIMAX_API_KEY not set. Set env var or create ~/.claude/env.d/minimax.env")
    return key

def generate(prompt: str, output: str, ratio: str = "1:1", n: int = 1,
             subject_ref: str = "", subject_type: str = "character"):

    api_key = get_api_key()
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": "image-01",
        "prompt": prompt,
        "aspect_ratio": ratio,
        "n": n,
        "response_format": "url",
        "prompt_optimizer": True
    }

    # Add subject reference for i2i mode
    if subject_ref:
        with open(subject_ref, "rb") as f:
            ref_b64 = base64.b64encode(f.read()).decode()
        payload["subject_reference"] = [{"type": subject_type, "image": ref_b64}]

    resp = requests.post(ENDPOINT, headers=headers, json=payload)
    data = resp.json()

    base_resp = data.get("base_resp", {})
    if base_resp.get("status_code", 0) != 0:
        raise SystemExit(f"API Error [{base_resp.get('status_code')}]: {base_resp.get('status_msg')}")

    data_obj = data.get("data", {})
    # Handle both {"image_urls": [...]} and [{"url": ...}] formats
    images = data_obj.get("image_urls", data_obj) if isinstance(data_obj, dict) else data_obj
    if not images:
        raise SystemExit("No images returned")

    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)

    for i, img_entry in enumerate(images):
        # img_entry may be a string URL or {"url": "..."} dict
        img_url = img_entry if isinstance(img_entry, str) else img_entry.get("url", "")
        if not img_url:
            continue
        img_resp = requests.get(img_url)
        suffix = f"_{i}" if n > 1 else ""
        out_path = output.replace(".png", f"{suffix}.png").replace(".jpg", f"{suffix}.jpg")
        with open(out_path, "wb") as f:
            f.write(img_resp.content)
        print(f"Saved image to {out_path}")

def main():
    p = argparse.ArgumentParser(description="MiniMax Image generation")
    p.add_argument("--prompt", required=True, help="Image description (max 1500 chars)")
    p.add_argument("-o", "--output", required=True, help="Output image path")
    p.add_argument("--ratio", default="1:1", help="Aspect ratio: 1:1, 16:9, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9")
    p.add_argument("-n", type=int, default=1, help="Number of images (1-9)")
    p.add_argument("--subject-ref", default="", help="Reference image for i2i mode")
    p.add_argument("--subject-type", default="character", help="Subject reference type")
    args = p.parse_args()

    generate(args.prompt, args.output, args.ratio, args.n, args.subject_ref, args.subject_type)

if __name__ == "__main__":
    main()