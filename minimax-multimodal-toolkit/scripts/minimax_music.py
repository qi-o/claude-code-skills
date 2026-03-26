#!/usr/bin/env python3
"""MiniMax Music generation"""

import argparse
import os
import requests
from pathlib import Path

API_BASE = os.environ.get("MINIMAX_API_HOST", "https://api.minimax.io")
ENDPOINT = f"{API_BASE}/v1/music_generation"

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

def generate(prompt: str, output: str, instrumental: bool = False,
            lyrics: str = "", lyrics_optimizer: bool = False,
            download: bool = False):

    api_key = get_api_key()
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": "music-2.5+",
        "prompt": prompt,
        "is_instrumental": instrumental,
        "lyrics": lyrics,
        "lyrics_optimizer": lyrics_optimizer,
        "output_format": "url"
    }

    resp = requests.post(ENDPOINT, headers=headers, json=payload)
    data = resp.json()

    base_resp = data.get("base_resp", {})
    if base_resp.get("status_code", 0) != 0:
        raise SystemExit(f"API Error [{base_resp.get('status_code')}]: {base_resp.get('status_msg')}")

    music_url = data.get("music_url", "")

    if download or not music_url.startswith("http"):
        print(f"Music URL: {music_url}")
        print(f"Output path: {output}")
    else:
        # Download the file
        audio_resp = requests.get(music_url)
        os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
        with open(output, "wb") as f:
            f.write(audio_resp.content)
        print(f"Saved music to {output} ({len(audio_resp.content)} bytes)")

def main():
    p = argparse.ArgumentParser(description="MiniMax Music generation")
    p.add_argument("--prompt", required=True, help="Music style/mood description (max 2000 chars)")
    p.add_argument("-o", "--output", required=True, help="Output file path")
    p.add_argument("--instrumental", action="store_true", help="Generate instrumental (no lyrics)")
    p.add_argument("--lyrics", default="", help="Song lyrics with structure tags")
    p.add_argument("--lyrics-optimizer", action="store_true", help="Optimize lyrics")
    p.add_argument("--download", action="store_true", help="Download audio file")
    args = p.parse_args()

    generate(args.prompt, args.output, args.instrumental, args.lyrics, args.lyrics_optimizer, args.download)

if __name__ == "__main__":
    main()