#!/usr/bin/env python3
"""MiniMax Text-to-Speech generation — uses form-data (application/x-www-form-urlencoded)"""

import argparse
import os
import requests
from pathlib import Path

API_BASE = os.environ.get("MINIMAX_API_HOST", "https://api.minimaxi.com")
ENDPOINT = f"{API_BASE}/v1/t2a_v2"

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

def generate(text: str, output: str, voice: str = "female-shaonu", emotion: str = "neutral",
             speed: float = 1.0, pitch: float = 0, volume: float = 1.0,
             sample_rate: int = 32000, bitrate: int = 128000):

    api_key = get_api_key()
    headers = {"Authorization": f"Bearer {api_key}"}

    # TTS API requires form-data (application/x-www-form-urlencoded), NOT JSON
    form_data = {
        "model": "speech-2.8-hd",
        "text": text,
        "voice_id": voice,
        "stream": "false",
        "speed": str(speed),
        "pitch": str(pitch),
        "volume": str(volume),
        "emotion": emotion,
        "sample_rate": str(sample_rate),
        "bitrate": str(bitrate),
        "output_format": "hex"
    }

    resp = requests.post(ENDPOINT, headers=headers, data=form_data, timeout=30)
    data = resp.json()

    base_resp = data.get("base_resp", {})
    if base_resp.get("status_code", 0) != 0:
        raise SystemExit(f"API Error [{base_resp.get('status_code')}]: {base_resp.get('status_msg')}")

    # Audio is returned as hex string under data.audio
    audio_hex = data.get("data", {}).get("audio", "")
    if not audio_hex:
        raise SystemExit("No audio data returned from API")

    audio_bytes = bytes.fromhex(audio_hex)

    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    with open(output, "wb") as f:
        f.write(audio_bytes)

    print(f"Saved TTS to {output} ({len(audio_bytes)} bytes)")

def main():
    p = argparse.ArgumentParser(description="MiniMax TTS generation")
    p.add_argument("text", help="Text to synthesize")
    p.add_argument("-o", "--output", required=True, help="Output MP3 file path")
    p.add_argument("--voice", default="female-tianmei", help="Voice ID")
    p.add_argument("--emotion", default="neutral", help="Emotion: happy, sad, angry, anxious, neutral")
    p.add_argument("--speed", type=float, default=1.0, help="Speed (0.5-2.0)")
    p.add_argument("--pitch", type=float, default=0, help="Pitch (-12 to 12)")
    p.add_argument("--volume", type=float, default=1.0, help="Volume (0.1-10)")
    p.add_argument("--sample-rate", type=int, default=32000, help="Sample rate (default 32000)")
    p.add_argument("--bitrate", type=int, default=128000, help="Bitrate (default 128000)")
    args = p.parse_args()

    generate(args.text, args.output, args.voice, args.emotion, args.speed, args.pitch, args.volume, args.sample_rate, args.bitrate)

if __name__ == "__main__":
    main()