#!/usr/bin/env python3
"""
MiniMax Multi-Modal Toolkit Media Tools CLI.

FFmpeg-based utilities for audio/video format conversion, concatenation,
extraction, trimming, and media inspection.

Usage:
    python media_tools.py convert-video input.webm -o output.mp4
    python media_tools.py convert-audio input.wav -o output.mp3
    python media_tools.py concat-video seg1.mp4 seg2.mp4 -o merged.mp4
    python media_tools.py concat-audio part1.mp3 part2.mp3 -o combined.mp3
    python media_tools.py extract-audio input.mp4 -o audio.mp3
    python media_tools.py trim-video input.mp4 --start 5 --end 15 -o clip.mp4
    python media_tools.py add-audio --video video.mp4 --audio bgm.mp3 -o output.mp4
    python media_tools.py probe input.mp4
"""

import argparse
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from _common import ensure_dir, run_ffmpeg

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_CRF = 18
DEFAULT_PRESET = "medium"
DEFAULT_VIDEO_BITRATE = "192k"
DEFAULT_AUDIO_BITRATE = "192k"
DEFAULT_CONCAT_VIDEO_CROSSFADE = 0.5
DEFAULT_CONCAT_AUDIO_CROSSFADE = 0.0
BYTES_PER_MB = 1048576

VIDEO_CODEC_MAP = {
    "mp4": "libx264", "mov": "libx264", "mkv": "libx264",
    "avi": "libx264", "ts": "libx264", "flv": "libx264",
    "webm": "libvpx-vp9",
}

AUDIO_CODEC_CONTAINER_MAP = {
    "mp4": "aac", "mov": "aac", "mkv": "aac",
    "ts": "aac", "flv": "aac", "webm": "libopus", "avi": "mp3",
}

AUDIO_CODEC_FORMAT_MAP = {
    "mp3": "libmp3lame", "wav": "pcm_s16le", "flac": "flac",
    "ogg": "libvorbis", "aac": "aac", "m4a": "aac",
    "opus": "libopus", "wma": "wmav2",
}


# ---------------------------------------------------------------------------
# Probe / info helpers
# ---------------------------------------------------------------------------

def _run_ffprobe(args):
    """Run ffprobe and return its JSON-decoded stdout."""
    cmd = ["ffprobe"] + args
    try:
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=120,
        )
    except FileNotFoundError:
        print("Error: ffprobe not found. Install it first.", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("Error: ffprobe timed out", file=sys.stderr)
        sys.exit(1)
    if result.returncode != 0:
        print(f"Error: ffprobe exited with code {result.returncode}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.decode("utf-8", errors="replace")


def probe_media(filepath):
    """Return parsed JSON from ffprobe for *filepath*."""
    raw = _run_ffprobe(["-v", "error", "-show_format", "-show_streams",
                        "-of", "json", str(filepath)])
    return json.loads(raw)


def get_duration(filepath):
    """Return the duration of *filepath* in seconds (float)."""
    info = probe_media(filepath)
    return float(info.get("format", {}).get("duration", 0))


def get_video_fps(filepath):
    """Return the approximate integer FPS of the first video stream."""
    raw = _run_ffprobe([
        "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0",
        str(filepath),
    ]).strip()
    if not raw or "/" not in raw:
        return 25
    try:
        num, den = raw.split("/")
        return max(1, (int(num) + int(den) // 2) // int(den))
    except (ValueError, ZeroDivisionError):
        return 25


def has_audio_stream(filepath):
    """Return True if *filepath* has at least one audio stream."""
    raw = _run_ffprobe([
        "-v", "error", "-select_streams", "a",
        "-show_entries", "stream=codec_type", "-of", "csv=p=0",
        str(filepath),
    ]).strip()
    return "audio" in raw


# ---------------------------------------------------------------------------
# Codec helpers
# ---------------------------------------------------------------------------

def _get_ext(path):
    """Return the lowercased file extension without the dot."""
    return Path(path).suffix.lstrip(".").lower()


def video_codec_for(ext):
    """Return the video codec name for a container extension."""
    return VIDEO_CODEC_MAP.get(ext, "libx264")


def audio_codec_for_container(ext):
    """Return the audio codec for a video container extension."""
    return AUDIO_CODEC_CONTAINER_MAP.get(ext, "aac")


def audio_codec_for_format(ext):
    """Return the audio codec for an audio-only format extension."""
    return AUDIO_CODEC_FORMAT_MAP.get(ext, "libmp3lame")


# ---------------------------------------------------------------------------
# Subcommand: convert-video
# ---------------------------------------------------------------------------

def cmd_convert_video(args):
    """Convert a video file to a different format or quality."""
    parser = argparse.ArgumentParser(prog="media_tools.py convert-video")
    parser.add_argument("input", help="Input video file")
    parser.add_argument("-o", "--output", required=True, help="Output file")
    parser.add_argument("--crf", type=int, default=DEFAULT_CRF,
                        help="Quality (default: 18)")
    parser.add_argument("--preset", default=DEFAULT_PRESET,
                        help="Encoding preset (default: medium)")
    parser.add_argument("--resolution", default="",
                        help="Target resolution (e.g. 1920x1080)")
    parser.add_argument("--fps", type=int, default=0,
                        help="Frame rate (default: auto)")
    opts = parser.parse_args(args)

    input_path = Path(opts.input)
    if not input_path.is_file():
        print(f"Error: Input file not found: {opts.input}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(opts.output)
    ext = _get_ext(output_path)
    v_codec = video_codec_for(ext)
    a_codec = audio_codec_for_container(ext)

    ensure_dir(output_path.parent)

    ffmpeg_args = ["-y", "-i", str(input_path)]

    if opts.resolution:
        w, h = opts.resolution.split("x", 1)
        ffmpeg_args.extend(["-vf", f"scale={w}:{h}"])

    ffmpeg_args.extend(["-c:v", v_codec])
    if v_codec in ("libx264", "libx265"):
        ffmpeg_args.extend([
            "-crf", str(opts.crf), "-preset", opts.preset, "-pix_fmt", "yuv420p",
        ])
    elif v_codec == "libvpx-vp9":
        ffmpeg_args.extend(["-crf", str(opts.crf), "-b:v", "0"])

    if opts.fps > 0:
        ffmpeg_args.extend(["-r", str(opts.fps)])

    if has_audio_stream(input_path):
        ffmpeg_args.extend(["-c:a", a_codec, "-b:a", DEFAULT_VIDEO_BITRATE])
    else:
        ffmpeg_args.append("-an")

    ffmpeg_args.append(str(output_path))

    print(f"Converting: {input_path} -> {output_path} ({v_codec}/{a_codec})")
    run_ffmpeg(ffmpeg_args)
    print(f"  Done: {output_path}")


# ---------------------------------------------------------------------------
# Subcommand: convert-audio
# ---------------------------------------------------------------------------

def cmd_convert_audio(args):
    """Convert an audio file to a different format."""
    parser = argparse.ArgumentParser(prog="media_tools.py convert-audio")
    parser.add_argument("input", help="Input audio file")
    parser.add_argument("-o", "--output", required=True, help="Output file")
    parser.add_argument("--bitrate", default=DEFAULT_AUDIO_BITRATE,
                        help="Bitrate (e.g. 320k)")
    parser.add_argument("--sample-rate", type=int, default=0,
                        help="Sample rate (e.g. 48000)")
    parser.add_argument("--channels", type=int, default=0,
                        help="Channels (1 or 2)")
    opts = parser.parse_args(args)

    input_path = Path(opts.input)
    if not input_path.is_file():
        print(f"Error: Input file not found: {opts.input}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(opts.output)
    ext = _get_ext(output_path)
    codec = audio_codec_for_format(ext)

    ensure_dir(output_path.parent)

    ffmpeg_args = [
        "-y", "-i", str(input_path),
        "-c:a", codec, "-b:a", opts.bitrate,
    ]
    if opts.sample_rate > 0:
        ffmpeg_args.extend(["-ar", str(opts.sample_rate)])
    if opts.channels > 0:
        ffmpeg_args.extend(["-ac", str(opts.channels)])
    ffmpeg_args.append(str(output_path))

    print(f"Converting audio: {input_path} -> {output_path} ({codec})")
    run_ffmpeg(ffmpeg_args)
    print(f"  Done: {output_path}")


# ---------------------------------------------------------------------------
# Subcommand: concat-video
# ---------------------------------------------------------------------------

def _build_xfade_filter(inputs, crossfade, offsets, has_audio):
    """Build the xfade/acrossfade filter_complex string for N inputs."""
    n = len(inputs)
    vf_parts = []
    af_parts = []

    if n == 2:
        vf_parts.append(
            f"[0:v][1:v]xfade=transition=fade:duration={crossfade}"
            f":offset={offsets[0]}[vout]"
        )
        if has_audio:
            af_parts.append(
                f"[0:a][1:a]acrossfade=d={crossfade}:c1=tri:c2=tri[aout]"
            )
    else:
        vf_parts.append(
            f"[0:v][1:v]xfade=transition=fade:duration={crossfade}"
            f":offset={offsets[0]}[xv1]"
        )
        if has_audio:
            af_parts.append(
                f"[0:a][1:a]acrossfade=d={crossfade}:c1=tri:c2=tri[xa1]"
            )
        for i in range(2, n):
            prev_v = f"[xv{i - 1}]"
            prev_a = f"[xa{i - 1}]"
            out_v = "[vout]" if i == n - 1 else f"[xv{i}]"
            out_a = "[aout]" if i == n - 1 else f"[xa{i}]"
            vf_parts.append(
                f"{prev_v}[{i}:v]xfade=transition=fade:duration={crossfade}"
                f":offset={offsets[i - 1]}{out_v}"
            )
            if has_audio:
                af_parts.append(
                    f"{prev_a}[{i}:a]acrossfade=d={crossfade}"
                    f":c1=tri:c2=tri{out_a}"
                )

    parts = vf_parts
    if af_parts:
        parts.append(";" + ";".join(af_parts))
    return ";".join(parts)


def _concat_video_fallback(inputs, output_path, fps, has_audio):
    """Concatenate videos using the concat demuxer (no crossfade)."""
    concat_file = tempfile.NamedTemporaryFile(
        suffix=".txt", mode="w", delete=False,
    )
    try:
        for vp in inputs:
            resolved = Path(vp).resolve()
            concat_file.write(f"file '{resolved}'\n")
        concat_file.close()

        ffmpeg_args = [
            "-y", "-f", "concat", "-safe", "0",
            "-i", concat_file.name,
            "-c:v", "libx264", "-preset", DEFAULT_PRESET,
            "-crf", str(DEFAULT_CRF), "-pix_fmt", "yuv420p",
            "-r", str(fps),
        ]
        if has_audio:
            ffmpeg_args.extend(["-c:a", "aac", "-b:a", DEFAULT_VIDEO_BITRATE])
        ffmpeg_args.append(str(output_path))

        run_ffmpeg(ffmpeg_args)
    finally:
        Path(concat_file.name).unlink(missing_ok=True)


def cmd_concat_video(args):
    """Concatenate multiple video files with optional crossfade."""
    parser = argparse.ArgumentParser(prog="media_tools.py concat-video")
    parser.add_argument("inputs", nargs="+", help="Input video files")
    parser.add_argument("-o", "--output", required=True, help="Output file")
    parser.add_argument("--crossfade", type=float,
                        default=DEFAULT_CONCAT_VIDEO_CROSSFADE,
                        help="Crossfade duration in seconds (default: 0.5)")
    opts = parser.parse_args(args)

    if len(opts.inputs) < 2:
        print("Error: At least 2 input files required", file=sys.stderr)
        sys.exit(1)

    for vp in opts.inputs:
        if not Path(vp).is_file():
            print(f"Error: Input file not found: {vp}", file=sys.stderr)
            sys.exit(1)

    output_path = Path(opts.output)
    ensure_dir(output_path.parent)

    fps = get_video_fps(opts.inputs[0])
    has_audio = all(has_audio_stream(vp) for vp in opts.inputs)
    n = len(opts.inputs)

    if opts.crossfade > 0:
        durations = [get_duration(vp) for vp in opts.inputs]
        offsets = []
        cumulative = 0.0
        for i in range(n - 1):
            offset = cumulative + durations[i] - opts.crossfade
            offsets.append(offset)
            cumulative = offset

        filter_complex = _build_xfade_filter(
            opts.inputs, opts.crossfade, offsets, has_audio,
        )

        ffmpeg_args = ["-y"]
        for vp in opts.inputs:
            ffmpeg_args.extend(["-i", str(Path(vp).resolve())])
        ffmpeg_args.extend(["-filter_complex", filter_complex, "-map", "[vout]"])
        if has_audio:
            ffmpeg_args.append("-map")
            ffmpeg_args.append("[aout]")
        ffmpeg_args.extend([
            "-c:v", "libx264", "-preset", DEFAULT_PRESET,
            "-crf", str(DEFAULT_CRF), "-pix_fmt", "yuv420p",
            "-r", str(fps),
        ])
        if has_audio:
            ffmpeg_args.extend(["-c:a", "aac", "-b:a", DEFAULT_VIDEO_BITRATE])
        ffmpeg_args.append(str(output_path))

        print(f"Concatenating {n} videos with {opts.crossfade}s crossfade...")
        try:
            run_ffmpeg(ffmpeg_args)
            print(f"  Done: {output_path}")
            return
        except SystemExit:
            print("  Crossfade failed, falling back to re-encode...")
    else:
        print(f"Concatenating {n} videos (hard cut)...")

    _concat_video_fallback(opts.inputs, output_path, fps, has_audio)
    print(f"  Done: {output_path}")


# ---------------------------------------------------------------------------
# Subcommand: concat-audio
# ---------------------------------------------------------------------------

def _concat_audio_fallback(inputs, output_path, codec):
    """Concatenate audio files using the concat demuxer."""
    concat_file = tempfile.NamedTemporaryFile(
        suffix=".txt", mode="w", delete=False,
    )
    try:
        for ap in inputs:
            resolved = Path(ap).resolve()
            concat_file.write(f"file '{resolved}'\n")
        concat_file.close()

        ffmpeg_args = [
            "-y", "-f", "concat", "-safe", "0",
            "-i", concat_file.name,
            "-c:a", codec, "-b:a", DEFAULT_AUDIO_BITRATE,
            str(output_path),
        ]
        run_ffmpeg(ffmpeg_args)
    finally:
        Path(concat_file.name).unlink(missing_ok=True)


def cmd_concat_audio(args):
    """Concatenate multiple audio files with optional crossfade."""
    parser = argparse.ArgumentParser(prog="media_tools.py concat-audio")
    parser.add_argument("inputs", nargs="+", help="Input audio files")
    parser.add_argument("-o", "--output", required=True, help="Output file")
    parser.add_argument("--crossfade", type=float,
                        default=DEFAULT_CONCAT_AUDIO_CROSSFADE,
                        help="Crossfade duration in seconds (default: 0)")
    opts = parser.parse_args(args)

    if len(opts.inputs) < 1:
        print("Error: At least 1 input file required", file=sys.stderr)
        sys.exit(1)

    for ap in opts.inputs:
        if not Path(ap).is_file():
            print(f"Error: Input file not found: {ap}", file=sys.stderr)
            sys.exit(1)

    output_path = Path(opts.output)
    ensure_dir(output_path.parent)

    if len(opts.inputs) == 1:
        shutil.copy2(opts.inputs[0], output_path)
        print(f"  Done: {output_path}")
        return

    ext = _get_ext(output_path)
    codec = audio_codec_for_format(ext)
    n = len(opts.inputs)

    if opts.crossfade > 0:
        af_parts = []
        if n == 2:
            af_parts.append(
                f"[0:a][1:a]acrossfade=d={opts.crossfade}:c1=tri:c2=tri[aout]"
            )
        else:
            af_parts.append(
                f"[0:a][1:a]acrossfade=d={opts.crossfade}:c1=tri:c2=tri[xa1]"
            )
            for i in range(2, n):
                prev = f"[xa{i - 1}]"
                out = "[aout]" if i == n - 1 else f"[xa{i}]"
                af_parts.append(
                    f"{prev}[{i}:a]acrossfade=d={opts.crossfade}"
                    f":c1=tri:c2=tri{out}"
                )

        filter_complex = ";".join(af_parts)

        ffmpeg_args = ["-y"]
        for ap in opts.inputs:
            ffmpeg_args.extend(["-i", str(Path(ap).resolve())])
        ffmpeg_args.extend([
            "-filter_complex", filter_complex,
            "-map", "[aout]",
            "-c:a", codec, "-b:a", DEFAULT_AUDIO_BITRATE,
            str(output_path),
        ])

        print(f"Concatenating {n} audio files with {opts.crossfade}s crossfade...")
        try:
            run_ffmpeg(ffmpeg_args)
            print(f"  Done: {output_path}")
            return
        except SystemExit:
            print("  Crossfade failed, falling back...")

    _concat_audio_fallback(opts.inputs, output_path, codec)
    print(f"  Done: {output_path}")


# ---------------------------------------------------------------------------
# Subcommand: extract-audio
# ---------------------------------------------------------------------------

def cmd_extract_audio(args):
    """Extract the audio stream from a video file."""
    parser = argparse.ArgumentParser(prog="media_tools.py extract-audio")
    parser.add_argument("input", help="Input video file")
    parser.add_argument("-o", "--output", required=True, help="Output file")
    parser.add_argument("--bitrate", default=DEFAULT_AUDIO_BITRATE,
                        help="Bitrate (e.g. 320k)")
    opts = parser.parse_args(args)

    input_path = Path(opts.input)
    if not input_path.is_file():
        print(f"Error: Input not found: {opts.input}", file=sys.stderr)
        sys.exit(1)
    if not has_audio_stream(input_path):
        print(f"Error: No audio stream in {opts.input}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(opts.output)
    ext = _get_ext(output_path)
    codec = audio_codec_for_format(ext)

    ensure_dir(output_path.parent)

    ffmpeg_args = [
        "-y", "-i", str(input_path),
        "-vn", "-c:a", codec, "-b:a", opts.bitrate,
        str(output_path),
    ]

    print(f"Extracting audio: {input_path} -> {output_path}")
    run_ffmpeg(ffmpeg_args)
    print(f"  Done: {output_path}")


# ---------------------------------------------------------------------------
# Subcommand: trim-video
# ---------------------------------------------------------------------------

def cmd_trim_video(args):
    """Trim a video to a time range."""
    parser = argparse.ArgumentParser(prog="media_tools.py trim-video")
    parser.add_argument("input", help="Input video file")
    parser.add_argument("-o", "--output", required=True, help="Output file")
    parser.add_argument("--start", type=float, default=0,
                        help="Start time in seconds")
    parser.add_argument("--end", type=float, default=0,
                        help="End time in seconds")
    parser.add_argument("--duration", type=float, default=0,
                        help="Duration in seconds (alternative to --end)")
    opts = parser.parse_args(args)

    input_path = Path(opts.input)
    if not input_path.is_file():
        print(f"Error: Input not found: {opts.input}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(opts.output)
    ensure_dir(output_path.parent)

    ffmpeg_args = ["-y"]
    if opts.start > 0:
        ffmpeg_args.extend(["-ss", str(opts.start)])
    ffmpeg_args.extend(["-i", str(input_path)])

    if opts.duration > 0:
        ffmpeg_args.extend(["-t", str(opts.duration)])
    elif opts.end > 0:
        duration = opts.end - opts.start
        ffmpeg_args.extend(["-t", str(duration)])

    ffmpeg_args.extend([
        "-c:v", "libx264", "-preset", DEFAULT_PRESET,
        "-crf", str(DEFAULT_CRF), "-pix_fmt", "yuv420p",
    ])
    if has_audio_stream(input_path):
        ffmpeg_args.extend(["-c:a", "aac", "-b:a", DEFAULT_VIDEO_BITRATE])
    ffmpeg_args.append(str(output_path))

    start_str = f"{opts.start}s"
    if opts.end > 0:
        end_str = f"{opts.end}s"
    elif opts.duration > 0:
        end_str = f"+{opts.duration}s"
    else:
        end_str = "end"
    print(f"Trimming: {input_path} [{start_str} - {end_str}] -> {output_path}")
    run_ffmpeg(ffmpeg_args)
    print(f"  Done: {output_path}")


# ---------------------------------------------------------------------------
# Subcommand: add-audio
# ---------------------------------------------------------------------------

def cmd_add_audio(args):
    """Add or overlay an audio track onto a video."""
    parser = argparse.ArgumentParser(prog="media_tools.py add-audio")
    parser.add_argument("--video", required=True, help="Video file")
    parser.add_argument("--audio", required=True, help="Audio file")
    parser.add_argument("-o", "--output", required=True, help="Output file")
    parser.add_argument("--volume", type=float, default=1.0,
                        help="Audio volume (0.0-1.0)")
    parser.add_argument("--replace", action="store_true",
                        help="Replace original audio instead of mixing")
    parser.add_argument("--fade-in", type=float, default=0,
                        help="Fade in duration in seconds")
    parser.add_argument("--fade-out", type=float, default=0,
                        help="Fade out duration in seconds")
    opts = parser.parse_args(args)

    video_path = Path(opts.video)
    audio_path = Path(opts.audio)
    if not video_path.is_file():
        print(f"Error: Video not found: {opts.video}", file=sys.stderr)
        sys.exit(1)
    if not audio_path.is_file():
        print(f"Error: Audio not found: {opts.audio}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(opts.output)
    ensure_dir(output_path.parent)

    duration = get_duration(video_path)
    video_has_audio = has_audio_stream(video_path)

    # Build audio filter chain
    af = f"[1:a]volume={opts.volume}"
    if opts.fade_in > 0:
        af += f",afade=t=in:d={opts.fade_in}"
    if opts.fade_out > 0:
        fo_start = max(0.0, duration - opts.fade_out)
        af += f",afade=t=out:st={fo_start}:d={opts.fade_out}"

    if video_has_audio and not opts.replace:
        af += ("[newaudio];"
               "[0:a][newaudio]amix=inputs=2:duration=first"
               ":dropout_transition=2[aout]")
        mode = "mixing with"
    else:
        af += "[aout]"
        mode = "replacing"

    print(f"Adding audio ({mode} original): {output_path}")
    ffmpeg_args = [
        "-y", "-i", str(video_path), "-i", str(audio_path),
        "-filter_complex", af,
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac",
        "-b:a", DEFAULT_VIDEO_BITRATE,
        "-shortest",
        str(output_path),
    ]
    run_ffmpeg(ffmpeg_args)
    print(f"  Done: {output_path}")


# ---------------------------------------------------------------------------
# Subcommand: probe
# ---------------------------------------------------------------------------

def cmd_probe(args):
    """Display detailed information about a media file."""
    parser = argparse.ArgumentParser(prog="media_tools.py probe")
    parser.add_argument("input", help="Media file to inspect")
    opts = parser.parse_args(args)

    input_path = Path(opts.input)
    if not input_path.is_file():
        print(f"Error: File not found: {opts.input}", file=sys.stderr)
        sys.exit(1)

    info = probe_media(input_path)
    fmt = info.get("format", {})
    streams = info.get("streams", [])

    fmt_name = fmt.get("format_long_name", "unknown")
    dur = float(fmt.get("duration", 0))
    size = int(fmt.get("size", 0))
    bitrate = float(fmt.get("bit_rate", 0))

    print(f"File:     {input_path}")
    print(f"Format:   {fmt_name}")
    print(f"Duration: {dur:.2f}s")
    print(f"Size:     {size / BYTES_PER_MB:.2f} MB")
    print(f"Bitrate:  {bitrate / 1000:.0f} kbps")

    for stream in streams:
        codec_type = stream.get("codec_type", "")
        if codec_type == "video":
            codec_name = stream.get("codec_name", "?")
            width = stream.get("width", "?")
            height = stream.get("height", "?")
            r_frame_rate = stream.get("r_frame_rate", "?")
            print(f"Video:    {codec_name} {width}x{height} @ {r_frame_rate} fps")
        elif codec_type == "audio":
            codec_name = stream.get("codec_name", "?")
            sample_rate = stream.get("sample_rate", "?")
            channels = stream.get("channels", "?")
            print(f"Audio:    {codec_name} {sample_rate}Hz {channels}ch")


# ---------------------------------------------------------------------------
# Main dispatcher
# ---------------------------------------------------------------------------

COMMANDS = {
    "convert-video": cmd_convert_video,
    "convert-audio": cmd_convert_audio,
    "concat-video": cmd_concat_video,
    "concat-audio": cmd_concat_audio,
    "extract-audio": cmd_extract_audio,
    "trim-video": cmd_trim_video,
    "add-audio": cmd_add_audio,
    "probe": cmd_probe,
}

USAGE_TEXT = """\
MiniMax Multi-Modal Toolkit Media Tools

Usage:
  media_tools.py <command> [options]

Commands:
  convert-video  Convert video format
  convert-audio  Convert audio format
  concat-video   Concatenate videos with crossfade
  concat-audio   Concatenate audio files
  extract-audio  Extract audio from video
  trim-video     Trim video by time range
  add-audio      Add/overlay audio on video
  probe          Show media file info

Examples:
  media_tools.py convert-video input.webm -o output.mp4
  media_tools.py convert-audio input.wav -o output.mp3
  media_tools.py concat-video seg1.mp4 seg2.mp4 -o merged.mp4
  media_tools.py extract-audio video.mp4 -o audio.mp3
  media_tools.py trim-video input.mp4 --start 5 --end 15 -o clip.mp4
  media_tools.py add-audio --video video.mp4 --audio bgm.mp3 -o output.mp4
  media_tools.py probe input.mp4
"""


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print(USAGE_TEXT)
        sys.exit(0)

    command = argv[0]
    if command in ("-h", "--help", "help"):
        print(USAGE_TEXT)
        sys.exit(0)

    handler = COMMANDS.get(command)
    if handler is None:
        print(f"Unknown command: {command}", file=sys.stderr)
        print(USAGE_TEXT, file=sys.stderr)
        sys.exit(1)

    handler(argv[1:])


if __name__ == "__main__":
    main()
