#!/usr/bin/env python3
"""MiniMax Music Generation CLI (model: music-2.5).

Translates ``scripts/music/generate_music.sh`` to idiomatic Python.
Imports shared helpers from ``_common.py``.

Usage:
    python minimax_music.py --prompt "ambient electronic" --instrumental --output ambient.mp3
    python minimax_music.py --lyrics "[verse]\\nHello world" --output song.mp3
    python minimax_music.py --lyrics "[verse]\\nStars" --genre pop --mood happy --output happy.mp3
"""

import argparse
import sys
import time
from pathlib import Path

from _common import api_request, download_file, ensure_dir, get_api_host, get_api_key

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_MODEL = "music-2.5"
API_PATH = "/v1/music_generation"

POLL_MAX_WAIT = 600
POLL_INTERVAL = 10

INSTRUMENTAL_LYRICS = "[intro] [outro]"
INSTRUMENTAL_SUFFIX = "pure music, no lyrics"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def build_field_prompt(args: argparse.Namespace) -> str:
    """Assemble a descriptive prompt from structured tag fields."""
    parts = []

    tag_fields = [
        ("Genre", args.genre),
        ("Mood", args.mood),
        ("Tempo", args.tempo),
        ("BPM", args.bpm),
        ("Key", args.key),
        ("Instruments", args.instruments),
        ("Vocals", args.vocals),
        ("Use case", args.use_case),
        ("Structure", args.structure),
        ("Avoid", args.avoid),
        ("References", args.references),
    ]

    for label, value in tag_fields:
        if value:
            parts.append(f"{label}: {value}")

    if not parts:
        return ""

    return ". ".join(parts)


def build_payload(args: argparse.Namespace) -> dict:
    """Construct the JSON request body from parsed CLI arguments."""
    field_prompt = build_field_prompt(args)

    # Merge field prompt with the user-provided --prompt
    if args.prompt and field_prompt:
        prompt = f"{args.prompt}. {field_prompt}"
    elif field_prompt:
        prompt = field_prompt
    else:
        prompt = args.prompt or ""

    payload = {
        "model": args.model,
        "prompt": prompt,
        "output_format": "url",
        "stream": False,
    }

    # Instrumental workaround for music-2.5 (no native is_instrumental flag)
    if args.instrumental:
        payload["lyrics"] = INSTRUMENTAL_LYRICS
        if prompt:
            payload["prompt"] = f"{prompt}. {INSTRUMENTAL_SUFFIX}"
        else:
            payload["prompt"] = INSTRUMENTAL_SUFFIX
    else:
        payload["lyrics"] = args.lyrics or ""

    # Optional audio settings
    audio_setting = {}
    if args.sample_rate:
        audio_setting["sample_rate"] = args.sample_rate
    if args.bitrate:
        audio_setting["bitrate"] = args.bitrate
    if args.format:
        audio_setting["format"] = args.format
    if audio_setting:
        payload["audio_setting"] = audio_setting

    # Optional AIGC watermark
    if args.aigc_watermark:
        payload["aigc_watermark"] = args.aigc_watermark

    return payload


def poll_music(api_url: str, headers: dict, task_id: str) -> str:
    """Poll the music generation status until completion or failure.

    Returns the ``file_id`` of the completed audio.

    Raises ``SystemExit`` on failure or timeout.
    """
    poll_url = f"{api_url.replace(API_PATH, '/v1/query/music_generation')}"

    for attempt in range(POLL_MAX_WAIT // POLL_INTERVAL):
        resp = api_request("GET", poll_url, headers=headers)
        status = resp.get("status", "")
        file_id = resp.get("file_id", "")

        if status == "Success":
            return file_id

        if status == "Fail":
            raise SystemExit(f"Music generation failed: {resp}")

        if not status:
            print(f"  Unexpected response (attempt {attempt + 1}), retrying...")
        else:
            print(f"  Status: {status} (attempt {attempt + 1})")

        time.sleep(POLL_INTERVAL)

    raise SystemExit(f"Music generation polling timeout after {POLL_MAX_WAIT}s")


def extract_audio_url(data: dict) -> str:
    """Extract the audio download URL from a sync API response."""
    inner = data.get("data", {})

    for key in ("audio_url", "audio", "audio_file.download_url"):
        candidate = inner
        for part in key.split("."):
            candidate = candidate.get(part, {}) if isinstance(candidate, dict) else {}
        if isinstance(candidate, str) and candidate.startswith("http"):
            return candidate

    return ""


def save_hex_audio(data: dict, output: str) -> None:
    """Decode hex-encoded audio data and write to disk."""
    audio_hex = data.get("data", {}).get("audio", "")
    if not audio_hex:
        print("Error: No audio hex data in response.", file=sys.stderr)
        sys.exit(1)

    try:
        audio_bytes = bytes.fromhex(audio_hex)
    except ValueError as exc:
        print(f"Error: Invalid hex data: {exc}", file=sys.stderr)
        sys.exit(1)

    out_path = Path(output)
    ensure_dir(out_path.parent)
    out_path.write_bytes(audio_bytes)
    print(f"Audio saved to: {out_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="minimax_music",
        description="MiniMax Music Generation CLI (model: music-2.5)",
    )

    # Core arguments
    parser.add_argument("--lyrics", default="", help="Song lyrics text (with [verse]/[chorus] tags)")
    parser.add_argument("--instrumental", action="store_true", default=False,
                        help="Generate instrumental only (no vocals)")
    parser.add_argument("--prompt", default="", help="Style/genre description")
    parser.add_argument("--genre", default="", help="Genre tag (e.g. pop, rock, jazz)")
    parser.add_argument("--mood", default="", help="Mood tag (e.g. happy, melancholic)")
    parser.add_argument("--tempo", default="", help="Tempo tag (e.g. slow, medium, fast)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model name (default: {DEFAULT_MODEL})")

    # Advanced structured fields
    parser.add_argument("--bpm", type=int, default=None, help="Beats per minute")
    parser.add_argument("--key", default="", help="Musical key (e.g. C major, A minor)")
    parser.add_argument("--instruments", default="", help="Instruments to include")
    parser.add_argument("--vocals", default="", help="Vocal style description")
    parser.add_argument("--use-case", dest="use_case", default="", help="Use case (e.g. background)")
    parser.add_argument("--structure", default="", help="Song structure description")
    parser.add_argument("--avoid", default="", help="Elements to avoid")
    parser.add_argument("--references", default="", help="Reference tracks/artists")

    # Audio settings
    parser.add_argument("--sample-rate", dest="sample_rate", type=int, default=None,
                        help="Audio sample rate")
    parser.add_argument("--bitrate", type=int, default=None, help="Audio bitrate")
    parser.add_argument("--format", default="", help="Audio format (mp3, wav, etc.)")

    # Output control
    parser.add_argument("--no-download", dest="no_download", action="store_true", default=False,
                        help="Print URL instead of downloading")
    parser.add_argument("--aigc-watermark", dest="aigc_watermark", action="store_true",
                        default=False, help="Add AIGC watermark")
    parser.add_argument("-o", "--output", required=True, help="Output file path")

    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    api_key = get_api_key()
    api_host = get_api_host()
    api_url = f"{api_host}{API_PATH}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = build_payload(args)

    print(f"Generating music with model: {args.model}")

    data = api_request("POST", api_url, headers=headers, json_body=payload)

    # Handle async response (returns a task_id)
    task_id = data.get("data", {}).get("task_id", "")
    if task_id:
        print(f"Task submitted: {task_id}")
        print("Polling for completion...")
        file_id = poll_music(api_url, headers, task_id)
        print(f"File ID: {file_id}")

        if args.no_download:
            print(f"Audio file ID: {file_id}")
            print("Use without --no-download to save automatically.")
            return

        download_url = f"{api_host}/v1/music_generation?task_id={task_id}&file_id={file_id}"
        ensure_dir(Path(args.output).parent)
        download_file(download_url, args.output)
        print(f"Audio downloaded to: {args.output}")
        return

    # Handle sync response (returns audio URL or hex directly)
    output_format = payload.get("output_format", "url")

    if output_format == "hex":
        save_hex_audio(data, args.output)
        return

    audio_url = extract_audio_url(data)
    if not audio_url:
        print("Error: No audio URL in response.", file=sys.stderr)
        print(f"Response: {data}", file=sys.stderr)
        sys.exit(1)

    print(f"Audio URL: {audio_url}")

    if args.no_download:
        print("Use without --no-download to save automatically.")
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(audio_url)
        print(f"URL written to: {args.output}")
        return

    ensure_dir(Path(args.output).parent)
    download_file(audio_url, args.output)
    print(f"Audio downloaded to: {args.output}")

    # Print extra info if present
    extra = data.get("extra_info") or data.get("data", {}).get("extra_info")
    if extra:
        print(f"Extra info: {extra}")


if __name__ == "__main__":
    main()
