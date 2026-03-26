#!/usr/bin/env python3
"""MiniMax Voice CLI -- Voice cloning, voice design, and environment checks.

Subcommands extracted from generate_voice.sh (bash).  TTS, voice listing,
merging, and conversion are handled by ``minimax_tts.py`` instead.

Usage:
    python minimax_voice.py clone audio_sample.mp3 --voice-id my-voice
    python minimax_voice.py design "A warm female narrator voice" --voice-id narrator
    python minimax_voice.py check-env
"""

import argparse
import sys
from pathlib import Path

import requests

# Allow running as ``python scripts/minimax_voice.py`` from the project root
# *or* from the scripts directory itself.
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from _common import (
    ensure_dir,
    get_api_host,
    get_api_key,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_DESIGN_PREVIEW = "This is a preview of the designed voice."
UPLOAD_TIMEOUT = 120


# ---------------------------------------------------------------------------
# Voice clone
# ---------------------------------------------------------------------------

def _upload_audio_file(file_path, api_key, api_host):
    """Upload an audio file for voice cloning via multipart/form-data.

    Returns the ``file_id`` extracted from the API response.
    """
    url = f"{api_host}/v1/files/upload"
    headers = {"Authorization": f"Bearer {api_key}"}

    with open(file_path, "rb") as fh:
        try:
            resp = requests.post(
                url,
                headers=headers,
                files={"file": (Path(file_path).name, fh)},
                data={"purpose": "voice_clone"},
                timeout=UPLOAD_TIMEOUT,
            )
        except requests.RequestException as exc:
            print(f"Error: upload failed: {exc}", file=sys.stderr)
            sys.exit(1)

    if resp.status_code >= 400:
        print(f"Error: API returned HTTP {resp.status_code}", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        sys.exit(1)

    try:
        data = resp.json()
    except (ValueError, Exception):
        print("Error: upload response is not valid JSON.", file=sys.stderr)
        sys.exit(1)

    base_resp = data.get("base_resp", {})
    if base_resp.get("status_code", 0) != 0:
        code = base_resp.get("status_code")
        msg = base_resp.get("status_msg", "Unknown error")
        raise SystemExit(f"API Error [{code}]: {msg}")

    file_id = (
        data.get("file", {}).get("file_id")
        or data.get("file_id")
        or ""
    )
    if not file_id:
        print("Error: upload succeeded but no file_id was returned.",
              file=sys.stderr)
        sys.exit(1)

    return file_id


def cmd_clone(args):
    """Clone a voice from an audio sample (10s-5min)."""
    audio_file = args.audio_file
    voice_id = args.voice_id

    if not audio_file:
        print("Error: audio file is required.", file=sys.stderr)
        print("Usage: minimax_voice.py clone audio.mp3 --voice-id my-voice",
              file=sys.stderr)
        sys.exit(1)

    audio_path = Path(audio_file).resolve()
    if not audio_path.is_file():
        print(f"Error: audio file not found: {audio_file}", file=sys.stderr)
        sys.exit(1)

    if not voice_id:
        print("Error: --voice-id is required.", file=sys.stderr)
        sys.exit(1)

    print(f"Cloning voice from: {audio_path}")
    print(f"Voice ID: {voice_id}")

    api_key = get_api_key()
    api_host = get_api_host()

    # Step 1: Upload audio
    file_id = _upload_audio_file(audio_path, api_key, api_host)
    print(f"File uploaded: {file_id}")

    # Step 2: Create voice clone
    url = f"{api_host}/v1/voice_clone"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {"voice_id": voice_id, "file_id": file_id}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
    except requests.RequestException as exc:
        print(f"Error: voice clone request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    if resp.status_code >= 400:
        print(f"Error: API returned HTTP {resp.status_code}", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        sys.exit(1)

    try:
        data = resp.json()
    except (ValueError, Exception):
        print("Error: voice clone response is not valid JSON.", file=sys.stderr)
        sys.exit(1)

    base_resp = data.get("base_resp", {})
    if base_resp.get("status_code", 0) != 0:
        code = base_resp.get("status_code")
        msg = base_resp.get("status_msg", "Unknown error")
        raise SystemExit(f"API Error [{code}]: {msg}")

    print(f"Voice cloned successfully: {voice_id}")


# ---------------------------------------------------------------------------
# Voice design
# ---------------------------------------------------------------------------

def cmd_design(args):
    """Create a custom voice from a text description."""
    description = args.description
    voice_id = args.voice_id

    if not description:
        print("Error: description is required.", file=sys.stderr)
        print(
            'Usage: minimax_voice.py design "A warm female voice" --voice-id narrator',
            file=sys.stderr,
        )
        sys.exit(1)

    preview_text = DEFAULT_DESIGN_PREVIEW

    print(f'Designing voice from: "{description}"')
    if voice_id:
        print(f"Voice ID: {voice_id}")

    api_key = get_api_key()
    api_host = get_api_host()

    url = f"{api_host}/v1/voice_design"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {"prompt": description, "preview_text": preview_text}
    if voice_id:
        payload["voice_id"] = voice_id

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
    except requests.RequestException as exc:
        print(f"Error: voice design request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    if resp.status_code >= 400:
        print(f"Error: API returned HTTP {resp.status_code}", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        sys.exit(1)

    try:
        data = resp.json()
    except (ValueError, Exception):
        print("Error: voice design response is not valid JSON.", file=sys.stderr)
        sys.exit(1)

    base_resp = data.get("base_resp", {})
    if base_resp.get("status_code", 0) != 0:
        code = base_resp.get("status_code")
        msg = base_resp.get("status_msg", "Unknown error")
        raise SystemExit(f"API Error [{code}]: {msg}")

    actual_voice_id = voice_id or data.get("voice_id", "unknown")
    print(f"Voice designed: {actual_voice_id}")

    # Save trial audio if the API returned one
    trial_audio = data.get("trial_audio", "")
    if trial_audio:
        output_name = f"{actual_voice_id}_preview.mp3"
        try:
            audio_bytes = bytes.fromhex(trial_audio)
        except ValueError:
            print("Warning: trial_audio is not valid hex, skipping preview.",
                  file=sys.stderr)
            return

        output_path = Path(output_name).resolve()
        ensure_dir(output_path.parent)
        output_path.write_bytes(audio_bytes)
        size = output_path.stat().st_size
        print(f"Preview saved to: {output_path} ({size} bytes)")


# ---------------------------------------------------------------------------
# Check environment
# ---------------------------------------------------------------------------

def cmd_check_env(_args):
    """Quick check that MINIMAX_API_KEY and MINIMAX_API_HOST are configured."""
    load_env_called = False

    try:
        api_key = get_api_key()
        load_env_called = True
    except SystemExit:
        print("  MINIMAX_API_KEY: NOT SET")
        print("  Set it with: export MINIMAX_API_KEY='your-key'")
        print("  Or add it to ~/.claude/env.d/minimax.env")
        return

    api_host = get_api_host()
    key_preview = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 10 else "***"
    print(f"  MINIMAX_API_KEY: {key_preview}")
    print(f"  MINIMAX_API_HOST: {api_host}")
    print("  Environment OK")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _add_clone_parser(subparsers):
    parser = subparsers.add_parser(
        "clone", help="Clone voice from audio sample (10s-5min)",
    )
    parser.add_argument(
        "audio_file", nargs="?", default="",
        help="Path to audio sample file",
    )
    parser.add_argument(
        "--voice-id", required=True,
        help="Voice ID to assign to the cloned voice",
    )
    parser.set_defaults(func=cmd_clone)


def _add_design_parser(subparsers):
    parser = subparsers.add_parser(
        "design", help="Create a custom voice from a text description",
    )
    parser.add_argument(
        "description", nargs="?", default="",
        help="Voice description (e.g. 'A warm female narrator voice')",
    )
    parser.add_argument(
        "--voice-id", required=True,
        help="Voice ID to assign to the designed voice",
    )
    parser.set_defaults(func=cmd_design)


def _add_check_env_parser(subparsers):
    parser = subparsers.add_parser(
        "check-env", help="Quick check for API key and host",
    )
    parser.set_defaults(func=cmd_check_env)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="minimax_voice.py",
        description=(
            "MiniMax Voice CLI -- voice cloning, voice design, "
            "and environment checks."
        ),
    )
    subparsers = parser.add_subparsers(dest="command")

    _add_clone_parser(subparsers)
    _add_design_parser(subparsers)
    _add_check_env_parser(subparsers)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
