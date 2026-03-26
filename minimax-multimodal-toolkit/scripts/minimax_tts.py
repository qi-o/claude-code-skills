#!/usr/bin/env python3
"""MiniMax TTS CLI -- Text-to-speech, voice listing, merging, and conversion.

Subcommands extracted from generate_voice.sh (bash).  Voice cloning, voice
design, segment validation, and multi-segment generation are handled by
``minimax_voice.py`` instead.

Usage:
    python minimax_tts.py tts "Hello world" -o hello.mp3
    python minimax_tts.py list-voices
    python minimax_tts.py merge a.mp3 b.mp3 -o combined.mp3
    python minimax_tts.py convert input.wav -o output.mp3
"""

import argparse
import json
import sys
import tempfile
from pathlib import Path

import requests

# Allow running as ``python scripts/minimax_tts.py`` from the project root
# *or* from the scripts directory itself.
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from _common import (
    ensure_dir,
    get_api_host,
    get_api_key,
    run_ffmpeg,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_VOICE_ID = "female-shaonv"
DEFAULT_MODEL = "speech-2.8-hd"
DEFAULT_SAMPLE_RATE = 32000
DEFAULT_BITRATE = 128000
DEFAULT_CROSSFADE_MS = 300
LOUDNORM_FILTER = "loudnorm=I=-16:TP=-1.5:LRA=11"

VALID_EMOTIONS = {
    "happy", "sad", "angry", "fearful",
    "disgusted", "surprised", "calm", "fluent", "whisper",
}

CODEC_MAP = {
    "mp3": "libmp3lame",
    "wav": "pcm_s16le",
    "flac": "flac",
    "ogg": "libvorbis",
    "aac": "aac",
    "m4a": "aac",
}


# ---------------------------------------------------------------------------
# TTS
# ---------------------------------------------------------------------------

def cmd_tts(args):
    """Synthesise speech from *text* and save to *output*."""
    text = args.text
    voice_id = args.voice_id
    output = args.output
    model = args.model
    speed = args.speed
    emotion = args.emotion or ""
    audio_format = args.format or Path(output).suffix.lstrip(".") or "mp3"
    sample_rate = args.sample_rate or DEFAULT_SAMPLE_RATE

    if not text:
        print("Error: text is required.", file=sys.stderr)
        sys.exit(1)
    if not output:
        print("Error: -o/--output is required.", file=sys.stderr)
        sys.exit(1)

    # Validate emotion when provided
    if emotion and emotion not in VALID_EMOTIONS:
        print(
            f"Warning: emotion '{emotion}' may not be supported. "
            f"Valid options: {', '.join(sorted(VALID_EMOTIONS))}",
            file=sys.stderr,
        )

    voice_setting = {
        "voice_id": voice_id,
        "speed": speed,
        "vol": 1.0,
        "pitch": 0,
    }
    if emotion:
        voice_setting["emotion"] = emotion

    payload = {
        "model": model,
        "text": text,
        "voice_setting": voice_setting,
        "audio_setting": {
            "sample_rate": sample_rate,
            "bitrate": DEFAULT_BITRATE,
            "format": audio_format,
            "channel": 1,
        },
        "stream": False,
        "subtitle_enable": False,
        "output_format": "hex",
    }

    api_key = get_api_key()
    api_host = get_api_host()
    url = f"{api_host}/v1/t2a_v2"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    preview = text[:50] + ("..." if len(text) > 50 else "")
    print(f"Synthesizing: {preview}")

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=120)
    except requests.RequestException as exc:
        print(f"Error: TTS request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    if resp.status_code >= 400:
        print(f"Error: API returned HTTP {resp.status_code}", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        sys.exit(1)

    try:
        data = resp.json()
    except (json.JSONDecodeError, ValueError):
        print("Error: TTS response is not valid JSON.", file=sys.stderr)
        sys.exit(1)

    base_resp = data.get("base_resp", {})
    if base_resp.get("status_code", 0) != 0:
        code = base_resp.get("status_code")
        msg = base_resp.get("status_msg", "Unknown error")
        print(f"Error: API Error [{code}]: {msg}", file=sys.stderr)
        sys.exit(1)

    audio_hex = data.get("data", {}).get("audio") or data.get("extra_info", {}).get("audio") or ""
    if not audio_hex:
        print("Error: No audio data returned from API.", file=sys.stderr)
        sys.exit(1)

    try:
        audio_bytes = bytes.fromhex(audio_hex)
    except ValueError:
        print("Error: Audio data is not valid hex.", file=sys.stderr)
        sys.exit(1)

    output_path = Path(output).resolve()
    ensure_dir(output_path.parent)
    output_path.write_bytes(audio_bytes)

    size = output_path.stat().st_size
    print(f"Done: {output_path} ({size} bytes)")


# ---------------------------------------------------------------------------
# List voices
# ---------------------------------------------------------------------------

def _fetch_voice_list(voice_type, api_key, api_host):
    """Fetch a single voice category from the API.

    Returns the parsed JSON dict, or None on failure.
    """
    url = f"{api_host}/v1/voice/list"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(
            url, headers=headers,
            json={"voice_type": voice_type}, timeout=30,
        )
        if resp.status_code >= 400:
            return None
        data = resp.json()
        base_resp = data.get("base_resp", {})
        if base_resp.get("status_code", 0) != 0:
            return None
        return data
    except (requests.RequestException, json.JSONDecodeError):
        return None


def cmd_list_voices(_args):
    """Print system, cloned, and designed voices."""
    api_key = get_api_key()
    api_host = get_api_host()

    # --- System voices ---
    print("=== System Voices ===")
    sys_data = _fetch_voice_list("system", api_key, api_host)
    if sys_data:
        voice_list = sys_data.get("voice_list", [])
        count = len(voice_list)
        if count > 0:
            for voice in voice_list[:10]:
                vid = voice.get("voice_id", "unknown")
                name = voice.get("name", "N/A")
                print(f"  {vid}: {name}")
            if count > 10:
                print(f"  ... and {count - 10} more")
        else:
            print("  (None found)")
    else:
        print("  (Could not fetch system voices)")

    # --- Custom voices ---
    print("")
    print("=== Custom Voices ===")

    has_custom = False

    clone_data = _fetch_voice_list("voice_cloning", api_key, api_host)
    if clone_data:
        clone_list = clone_data.get("voice_list", [])
        if clone_list:
            has_custom = True
            print(f"Cloned ({len(clone_list)}):")
            for voice in clone_list:
                print(f"  {voice.get('voice_id', 'unknown')}")

    design_data = _fetch_voice_list("voice_generation", api_key, api_host)
    if design_data:
        design_list = design_data.get("voice_list", [])
        if design_list:
            has_custom = True
            print(f"Designed ({len(design_list)}):")
            for voice in design_list:
                print(f"  {voice.get('voice_id', 'unknown')}")

    if not has_custom:
        print("  (None found)")


# ---------------------------------------------------------------------------
# Merge audio files
# ---------------------------------------------------------------------------

def _merge_audio_files(output_path, input_files, crossfade_ms, normalize):
    """Merge *input_files* into *output_path* using ffmpeg.

    Tries crossfade first when *crossfade_ms* > 0 and there are >= 2 files.
    Falls back to the concat demuxer on failure.  Applies loudnorm when
    *normalize* is True.
    """
    n = len(input_files)
    output_path = Path(output_path).resolve()
    ensure_dir(output_path.parent)

    if crossfade_ms > 0 and n >= 2:
        success = _merge_with_crossfade(output_path, input_files, crossfade_ms, normalize)
        if success:
            return
        print("  Crossfade merge failed, falling back to concat demuxer...",
              file=sys.stderr)

    _merge_with_concat(output_path, input_files, normalize)


def _merge_with_crossfade(output_path, input_files, crossfade_ms, normalize):
    """Attempt crossfade merge.  Returns True on success."""
    n = len(input_files)
    crossfade_sec = crossfade_ms / 1000.0

    # Build ffmpeg arguments
    ffmpeg_args = ["-y"]
    for f in input_files:
        ffmpeg_args += ["-i", str(f)]

    # Build filter_complex string
    # Each input gets resampled and formatted to mono float
    parts = []
    for i in range(n):
        parts.append(
            f"[{i}:a]aresample=32000,aformat=sample_fmts=fltp:channel_layouts=mono[s{i}]"
        )

    # Chain acrossfade filters
    if n == 2:
        parts.append(f"[s0][s1]acrossfade=d={crossfade_sec}[merged]")
    else:
        parts.append(f"[s0][s1]acrossfade=d={crossfade_sec}[m1]")
        for i in range(2, n):
            prev = f"[m{i - 1}]"
            if i == n - 1:
                parts.append(f"{prev}[s{i}]acrossfade=d={crossfade_sec}[merged]")
            else:
                parts.append(f"{prev}[s{i}]acrossfade=d={crossfade_sec}[m{i}]")

    # Final output filter
    final_filter = "[merged]aformat=sample_fmts=fltp"
    if normalize:
        final_filter += f",{LOUDNORM_FILTER}"
    final_filter += "[final]"
    parts.append(final_filter)

    filter_complex = ";".join(parts)

    ffmpeg_args += [
        "-filter_complex", filter_complex,
        "-map", "[final]",
        "-ar", "32000", "-ac", "1", "-acodec", "libmp3lame",
        str(output_path),
    ]

    try:
        run_ffmpeg(ffmpeg_args)
        return True
    except SystemExit:
        return False


def _merge_with_concat(output_path, input_files, normalize):
    """Merge using ffmpeg concat demuxer (no crossfade)."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False,
    ) as fh:
        for f in input_files:
            resolved = Path(f).resolve()
            fh.write(f"file '{resolved}'\n")
        concat_list_path = fh.name

    try:
        if normalize:
            tmp_concat = tempfile.NamedTemporaryFile(
                suffix=".mp3", delete=False,
            )
            tmp_concat_path = tmp_concat.name
            tmp_concat.close()

            run_ffmpeg([
                "-y", "-f", "concat", "-safe", "0",
                "-i", concat_list_path,
                "-c", "copy", tmp_concat_path,
            ])
            run_ffmpeg([
                "-y", "-i", tmp_concat_path,
                "-af", LOUDNORM_FILTER,
                "-acodec", "libmp3lame", str(output_path),
            ])
            Path(tmp_concat_path).unlink(missing_ok=True)
        else:
            run_ffmpeg([
                "-y", "-f", "concat", "-safe", "0",
                "-i", concat_list_path,
                "-c", "copy", str(output_path),
            ])
    finally:
        Path(concat_list_path).unlink(missing_ok=True)


def cmd_merge(args):
    """Merge multiple audio files into one."""
    input_files = args.inputs
    output = args.output
    crossfade_ms = args.crossfade
    normalize = not args.no_normalize

    if len(input_files) < 2:
        print("Error: At least 2 input files are required.", file=sys.stderr)
        sys.exit(1)
    if not output:
        print("Error: -o/--output is required.", file=sys.stderr)
        sys.exit(1)

    for f in input_files:
        if not Path(f).is_file():
            print(f"Error: File not found: {f}", file=sys.stderr)
            sys.exit(1)

    print(f"Merging {len(input_files)} files...")
    _merge_audio_files(output, input_files, crossfade_ms, normalize)
    print(f"Merged audio saved to: {output}")


# ---------------------------------------------------------------------------
# Convert audio format
# ---------------------------------------------------------------------------

def cmd_convert(args):
    """Convert an audio file to a different format."""
    input_file = args.input
    output = args.output
    fmt = args.format
    sample_rate = args.sample_rate
    bitrate = args.bitrate
    channels = args.channels

    if not input_file or not Path(input_file).is_file():
        print(f"Error: Input file not found: {input_file or '<none>'}", file=sys.stderr)
        sys.exit(1)
    if not output:
        print("Error: -o/--output is required.", file=sys.stderr)
        sys.exit(1)

    # If format not explicitly given, infer from output extension
    if not fmt:
        fmt = Path(output).suffix.lstrip(".") or "mp3"

    codec = CODEC_MAP.get(fmt, "copy")

    ffmpeg_args = ["-y", "-i", input_file, "-acodec", codec]
    if sample_rate:
        ffmpeg_args += ["-ar", str(sample_rate)]
    if channels:
        ffmpeg_args += ["-ac", str(channels)]
    if bitrate:
        ffmpeg_args += ["-b:a", str(bitrate)]
    ffmpeg_args.append(output)

    ensure_dir(Path(output).parent)

    print(f"Converting {input_file} to {fmt}...")
    run_ffmpeg(ffmpeg_args)
    print(f"Converted audio saved to: {output}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _add_tts_parser(subparsers):
    parser = subparsers.add_parser(
        "tts", help="Basic text-to-speech",
    )
    parser.add_argument("text", nargs="?", default="", help="Text to synthesise")
    parser.add_argument(
        "-v", "--voice-id", default=DEFAULT_VOICE_ID,
        help=f"Voice ID (default: {DEFAULT_VOICE_ID})",
    )
    parser.add_argument(
        "-o", "--output", required=True,
        help="Output file path (e.g. output.mp3)",
    )
    parser.add_argument(
        "--speed", type=float, default=1.0,
        help="Speech speed 0.5-2.0 (default: 1.0)",
    )
    parser.add_argument(
        "--emotion", default="",
        help="Emotion tag (only for speech-2.6 models)",
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL,
        help=f"Model name (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--format", default="",
        help="Audio format: mp3, wav, flac, ogg (default: from output extension)",
    )
    parser.add_argument(
        "--sample-rate", type=int, default=None,
        help=f"Sample rate (default: {DEFAULT_SAMPLE_RATE})",
    )
    parser.set_defaults(func=cmd_tts)


def _add_list_voices_parser(subparsers):
    parser = subparsers.add_parser(
        "list-voices", help="List available voices",
    )
    parser.set_defaults(func=cmd_list_voices)


def _add_merge_parser(subparsers):
    parser = subparsers.add_parser(
        "merge", help="Merge multiple audio files",
    )
    parser.add_argument(
        "inputs", nargs="+", metavar="FILE",
        help="Input audio files (at least 2)",
    )
    parser.add_argument(
        "-o", "--output", required=True,
        help="Output file path",
    )
    parser.add_argument(
        "--crossfade", type=int, default=DEFAULT_CROSSFADE_MS,
        help=f"Crossfade duration in ms, 0 to disable (default: {DEFAULT_CROSSFADE_MS})",
    )
    parser.add_argument(
        "--no-normalize", action="store_true",
        help="Skip loudnorm normalization",
    )
    parser.set_defaults(func=cmd_merge)


def _add_convert_parser(subparsers):
    parser = subparsers.add_parser(
        "convert", help="Convert audio format",
    )
    parser.add_argument(
        "input", help="Input audio file",
    )
    parser.add_argument(
        "-o", "--output", required=True,
        help="Output file path",
    )
    parser.add_argument(
        "--format", default="",
        help="Target format: mp3, wav, flac, ogg, aac, m4a (default: from output extension)",
    )
    parser.add_argument(
        "--sample-rate", type=int, default=None,
        help="Target sample rate",
    )
    parser.add_argument(
        "--bitrate", default=None,
        help="Target bitrate (e.g. 128k, 320k)",
    )
    parser.add_argument(
        "--channels", type=int, default=None,
        help="Target channel count (1=mono, 2=stereo)",
    )
    parser.set_defaults(func=cmd_convert)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="minimax_tts.py",
        description="MiniMax TTS CLI -- text-to-speech, voice listing, merging, and conversion.",
    )
    subparsers = parser.add_subparsers(dest="command")

    _add_tts_parser(subparsers)
    _add_list_voices_parser(subparsers)
    _add_merge_parser(subparsers)
    _add_convert_parser(subparsers)

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
