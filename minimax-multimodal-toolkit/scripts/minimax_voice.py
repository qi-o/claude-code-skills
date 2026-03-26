#!/usr/bin/env python3
"""MiniMax Voice Clone and Voice Design"""

import argparse
import os
import sys
import requests
from pathlib import Path

API_BASE = os.environ.get("MINIMAX_API_HOST", "https://api.minimax.io")

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

def clone_voice(audio_path: str, voice_id: str):
    api_key = get_api_key()
    headers = {"Authorization": f"Bearer {api_key}"}

    with open(audio_path, "rb") as f:
        files = {"file": (os.path.basename(audio_path), f.read(), "audio/mpeg")}
        data = {"voice_id": voice_id}
        resp = requests.post(f"{API_BASE}/v1/voice_clone", headers=headers, data=data, files=files)

    result = resp.json()
    base_resp = result.get("base_resp", {})
    if base_resp.get("status_code", 0) != 0:
        raise SystemExit(f"API Error: {base_resp.get('status_msg')}")

    print(f"Voice cloned successfully. Voice ID: {voice_id}")

def design_voice(description: str, voice_id: str):
    api_key = get_api_key()
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {"description": description, "voice_id": voice_id}
    resp = requests.post(f"{API_BASE}/v1/voice_design", headers=headers, json=payload)

    result = resp.json()
    base_resp = result.get("base_resp", {})
    if base_resp.get("status_code", 0) != 0:
        raise SystemExit(f"API Error: {base_resp.get('status_msg')}")

    print(f"Voice designed successfully. Voice ID: {voice_id}")

def merge_audio(files: list, output: str):
    import wave
    import glob

    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)

    with wave.open(output, "wb") as out_wav:
        for i, f in enumerate(files):
            with wave.open(f, "rb") as w:
                if i == 0:
                    out_wav.setnchannels(w.getnchannels())
                    out_wav.setsampwidth(w.getsampwidth())
                    out_wav.setframerate(w.getframerate())
                out_wav.writeframes(w.readframes(w.getnframes()))

    print(f"Merged {len(files)} files to {output}")

def main():
    p = argparse.ArgumentParser(description="MiniMax Voice Clone and Design")
    sub = p.add_subparsers(dest="cmd")

    clone = sub.add_parser("clone", help="Clone a voice from audio sample")
    clone.add_argument("audio", help="Audio file path (mp3/wav)")
    clone.add_argument("--voice-id", required=True, help="Target voice ID")

    design = sub.add_parser("design", help="Design a custom voice from description")
    design.add_argument("description", help="Voice description")
    design.add_argument("--voice-id", required=True, help="Target voice ID")

    merge = sub.add_parser("merge", help="Merge multiple audio files")
    merge.add_argument("files", nargs="+", help="Audio files to merge")
    merge.add_argument("-o", "--output", required=True, help="Output file path")

    args = p.parse_args()

    if args.cmd == "clone":
        clone_voice(args.audio, args.voice_id)
    elif args.cmd == "design":
        design_voice(args.description, args.voice_id)
    elif args.cmd == "merge":
        merge_audio(args.files, args.output)
    else:
        p.print_help()

if __name__ == "__main__":
    main()