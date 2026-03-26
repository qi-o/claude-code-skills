#!/usr/bin/env python3
"""
MiniMax Video Toolkit -- Unified CLI for video generation, long videos,
template videos, and background music overlay.

Merges generate_video.sh, generate_long_video.sh, generate_template_video.sh,
and add_bgm.sh into a single Python script with argparse subcommands.

Usage:
    python minimax_video.py video --mode t2v --prompt "A cat" -o out.mp4
    python minimax_video.py long-video --scenes "Scene 1" "Scene 2" -o out.mp4
    python minimax_video.py template --template-id T001 --media img.jpg -o out.mp4
    python minimax_video.py add-bgm --video in.mp4 --audio bgm.mp3 -o out.mp4
"""

import argparse
import base64
import json
import mimetypes
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from _common import (
    api_request,
    download_file,
    ensure_dir,
    get_api_host,
    get_api_key,
    load_env,
    run_ffmpeg,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

POLL_INTERVAL = 10
MAX_WAIT_TIME = 600
REQUEST_TIMEOUT = 60
MAX_CONSECUTIVE_FAILURES = 5
DEFAULT_MODEL_T2V_I2V = "MiniMax-Hailuo-2.3"
DEFAULT_MODEL_SEF = "MiniMax-Hailuo-02"
DEFAULT_MODEL_REF = "S2V-01"
DEFAULT_DURATION = 10
DEFAULT_RESOLUTION = "768P"
DEFAULT_BGM_VOLUME = 0.3
DEFAULT_CROSSFADE = 0.5

# MiniMax-Hailuo-2.3 constraints: 10s -> 768P only; 6s -> 768P or 1080P
INVALID_COMBOS = {
    (DEFAULT_MODEL_T2V_I2V, 10, "1080P"),
}

VALID_DURATIONS = (6, 10)
VALID_RESOLUTIONS = ("512P", "720P", "768P", "1080P")

# ---------------------------------------------------------------------------
# Helpers: resolve images / media to data URLs
# ---------------------------------------------------------------------------


def resolve_image(input_path):
    """Return a data-URL string for *input_path*, or pass through URLs unchanged."""
    if not input_path:
        return None
    if input_path.startswith(("http://", "https://", "data:")):
        return input_path
    path = Path(input_path)
    if not path.is_file():
        print(f"Error: Image not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    mime = mimetypes.guess_type(str(path))[0] or "image/jpeg"
    with open(path, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def resolve_media(input_value):
    """Resolve a media file path or URL to a data URL or pass through."""
    if input_value.startswith(("http://", "https://", "data:")):
        return input_value
    path = Path(input_value)
    if not path.is_file():
        print(f"Error: Media file not found: {input_value}", file=sys.stderr)
        sys.exit(1)
    mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    with open(path, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


# ---------------------------------------------------------------------------
# Helpers: validation
# ---------------------------------------------------------------------------


def validate_duration_resolution(model, duration, resolution):
    """Reject known invalid duration/resolution combinations for the given model."""
    if (model, duration, resolution) in INVALID_COMBOS:
        print(
            f"Error: {model} does not support {duration}s at {resolution}. "
            f"Use 6s for {resolution} or 10s with 768P.",
            file=sys.stderr,
        )
        sys.exit(1)
    if duration not in VALID_DURATIONS:
        print(
            f"Error: Invalid duration {duration}s. Allowed: {VALID_DURATIONS}",
            file=sys.stderr,
        )
        sys.exit(1)
    if resolution not in VALID_RESOLUTIONS:
        print(
            f"Error: Invalid resolution {resolution}. Allowed: {VALID_RESOLUTIONS}",
            file=sys.stderr,
        )
        sys.exit(1)


def default_model_for_mode(mode):
    """Return the default model name for a given generation mode."""
    models = {
        "t2v": DEFAULT_MODEL_T2V_I2V,
        "i2v": DEFAULT_MODEL_T2V_I2V,
        "sef": DEFAULT_MODEL_SEF,
        "ref": DEFAULT_MODEL_REF,
    }
    return models.get(mode)


# ---------------------------------------------------------------------------
# Core API: create task, poll, download
# ---------------------------------------------------------------------------


def create_video_task(api_host, api_key, payload):
    """POST to /v1/video_generation and return the task_id."""
    url = f"{api_host}/v1/video_generation"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    print("Creating video generation task...", file=sys.stderr)
    data = api_request("POST", url, headers=headers, json_body=payload, timeout=REQUEST_TIMEOUT)
    task_id = data.get("task_id", "")
    if not task_id:
        print("Error: No task_id in response", file=sys.stderr)
        sys.exit(1)
    print(f"Task created: {task_id}", file=sys.stderr)
    return task_id


def poll_video_task(api_host, api_key, task_id, query_path="query/video_generation"):
    """Poll a video generation task until it succeeds or fails.

    Uses ``requests`` directly (not ``api_request``) so transient HTTP errors
    can be handled gracefully without exiting.

    Returns the ``file_id`` (for video generation) or ``video_url`` (for template tasks).
    """
    url = f"{api_host}/v1/{query_path}"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"task_id": task_id}
    start_time = time.time()
    consecutive_failures = 0

    while True:
        elapsed = int(time.time() - start_time)
        if elapsed > MAX_WAIT_TIME:
            print(f"Error: Task {task_id} timed out after {MAX_WAIT_TIME}s", file=sys.stderr)
            sys.exit(1)

        try:
            resp = requests.get(
                url, params=params, headers=headers, timeout=REQUEST_TIMEOUT
            )
            consecutive_failures = 0
        except requests.RequestException:
            consecutive_failures += 1
            print(
                f"  Poll error ({consecutive_failures}/{MAX_CONSECUTIVE_FAILURES})",
                file=sys.stderr,
            )
            if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                print("Error: Too many consecutive poll failures", file=sys.stderr)
                sys.exit(1)
            time.sleep(POLL_INTERVAL)
            continue

        if resp.status_code >= 400:
            consecutive_failures += 1
            print(f"  HTTP {resp.status_code} on poll", file=sys.stderr)
            if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                sys.exit(1)
            time.sleep(POLL_INTERVAL)
            continue

        try:
            data = resp.json()
        except (json.JSONDecodeError, ValueError):
            consecutive_failures += 1
            time.sleep(POLL_INTERVAL)
            continue

        status = data.get("status", "Unknown")
        print(f"  [{elapsed}s] Status: {status}", file=sys.stderr)

        if status == "Success":
            file_id = data.get("file_id", "")
            video_url = data.get("video_url", "")
            if file_id:
                return file_id
            if video_url:
                return video_url
            print("Error: Task succeeded but no file_id or video_url", file=sys.stderr)
            sys.exit(1)

        if status in ("Fail", "Failed", "Error"):
            err_msg = data.get("base_resp", {}).get("status_msg", "Unknown error")
            print(f"Error: Task failed: {err_msg}", file=sys.stderr)
            sys.exit(1)

        time.sleep(POLL_INTERVAL)


def download_video_by_file_id(api_host, api_key, file_id, output_path):
    """Retrieve the download URL from /v1/files/retrieve and download the video."""
    url = f"{api_host}/v1/files/retrieve"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"file_id": file_id}

    print(f"Retrieving file {file_id}...", file=sys.stderr)
    resp = requests.get(url, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()

    dl_url = data.get("file", {}).get("download_url", "")
    if not dl_url:
        print("Error: No download_url in file response", file=sys.stderr)
        sys.exit(1)

    print("Downloading video...", file=sys.stderr)
    download_file(dl_url, output_path)


# ---------------------------------------------------------------------------
# FFmpeg helpers
# ---------------------------------------------------------------------------


def get_video_duration(video_path):
    """Return video duration in seconds as a float."""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "json", str(video_path),
            ],
            capture_output=True, text=True, timeout=30,
        )
        info = json.loads(result.stdout)
        return float(info["format"]["duration"])
    except Exception:
        return 0.0


def get_video_fps(video_path):
    """Return the video's frame rate as an integer (default 25)."""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=r_frame_rate",
                "-of", "csv=p=0", str(video_path),
            ],
            capture_output=True, text=True, timeout=30,
        )
        fps_str = result.stdout.strip()
        num, _, den = fps_str.partition("/")
        num, den = int(num), int(den)
        return (num + den // 2) // den
    except Exception:
        return 25


def video_has_audio(video_path):
    """Return True if the video has an audio stream."""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-select_streams", "a",
                "-show_entries", "stream=codec_type",
                "-of", "csv=p=0", str(video_path),
            ],
            capture_output=True, text=True, timeout=30,
        )
        return "audio" in result.stdout
    except Exception:
        return False


def extract_last_frame(video_path, output_image):
    """Extract the last frame from a video as a JPEG image."""
    result = subprocess.run(
        [
            "ffmpeg", "-y",
            "-sseof", "-0.04",
            "-i", str(video_path),
            "-frames:v", "1",
            "-q:v", "2",
            str(output_image),
        ],
        capture_output=True, timeout=30,
    )
    if result.returncode != 0 or not Path(output_image).is_file():
        print("Warning: Could not extract last frame", file=sys.stderr)
        return False
    print(f"  Extracted last frame: {output_image}", file=sys.stderr)
    return True


# ---------------------------------------------------------------------------
# Long video: concatenate with crossfade
# ---------------------------------------------------------------------------


def concatenate_videos(output_path, crossfade, video_paths):
    """Concatenate multiple video segments with optional crossfade.

    Falls back to simple concat demuxer if crossfade fails.
    """
    n = len(video_paths)
    if n == 1:
        shutil.copy2(video_paths[0], output_path)
        return

    fps = get_video_fps(video_paths[0])
    all_have_audio = all(video_has_audio(vp) for vp in video_paths)

    if crossfade > 0:
        success = _concatenate_with_xfade(
            output_path, crossfade, video_paths, fps, all_have_audio, n
        )
        if success:
            return
        print("  Crossfade failed, falling back to re-encode concat...", file=sys.stderr)

    # Fallback: concat demuxer with re-encode
    _concatenate_with_demuxer(output_path, video_paths, fps, all_have_audio)


def _concatenate_with_xfade(output_path, crossfade, video_paths, fps, all_have_audio, n):
    """Try xfade-based concatenation. Returns True on success."""
    durations = [get_video_duration(vp) for vp in video_paths]

    inputs = []
    for vp in video_paths:
        inputs.extend(["-i", str(vp)])

    # Calculate offsets for xfade transitions
    offsets = []
    cumulative = 0.0
    for i in range(n - 1):
        offset = cumulative + durations[i] - crossfade
        offsets.append(offset)
        cumulative = offset

    # Build video filter parts
    vf_parts = []
    af_parts = []

    if n == 2:
        vf_parts.append(
            f"[0:v][1:v]xfade=transition=fade:duration={crossfade}:offset={offsets[0]}[vout]"
        )
        if all_have_audio:
            af_parts.append(
                f"[0:a][1:a]acrossfade=d={crossfade}:c1=tri:c2=tri[aout]"
            )
    else:
        vf_parts.append(
            f"[0:v][1:v]xfade=transition=fade:duration={crossfade}:offset={offsets[0]}[xv1]"
        )
        if all_have_audio:
            af_parts.append(
                f"[0:a][1:a]acrossfade=d={crossfade}:c1=tri:c2=tri[xa1]"
            )
        for i in range(2, n):
            is_last = i == n - 1
            v_out = "[vout]" if is_last else f"[xv{i}]"
            a_out = "[aout]" if is_last else f"[xa{i}]"
            vf_parts.append(
                f"[xv{i-1}][{i}:v]xfade=transition=fade:duration={crossfade}:offset={offsets[i-1]}{v_out}"
            )
            if all_have_audio:
                af_parts.append(
                    f"[xa{i-1}][{i}:a]acrossfade=d={crossfade}:c1=tri:c2=tri{a_out}"
                )

    filter_parts = vf_parts[:]
    if af_parts:
        filter_parts.extend(af_parts)
    filter_complex = ";".join(filter_parts)

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_complex,
        "-map", "[vout]",
    ]
    if all_have_audio:
        cmd.extend(["-map", "[aout]"])
    cmd.extend([
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", str(fps),
    ])
    if all_have_audio:
        cmd.extend(["-c:a", "aac", "-b:a", "192k"])
    cmd.append(str(output_path))

    result = subprocess.run(cmd, capture_output=True, timeout=300)
    if result.returncode == 0:
        print(f"Concatenated {n} segments -> {output_path}", file=sys.stderr)
        return True
    return False


def _concatenate_with_demuxer(output_path, video_paths, fps, all_have_audio):
    """Fallback concatenation using the concat demuxer with re-encode."""
    concat_file = tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, prefix="concat_"
    )
    try:
        for vp in video_paths:
            abs_path = Path(vp).resolve()
            concat_file.write(f"file '{abs_path}'\n")
        concat_file.close()

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", concat_file.name,
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-r", str(fps),
        ]
        if all_have_audio:
            cmd.extend(["-c:a", "aac", "-b:a", "192k"])
        cmd.append(str(output_path))

        result = subprocess.run(cmd, capture_output=True, timeout=300)
        if result.returncode != 0:
            print(f"Error: ffmpeg concat failed", file=sys.stderr)
            sys.exit(1)
    finally:
        os.unlink(concat_file.name)

    print(f"Concatenated {len(video_paths)} segments -> {output_path}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Music generation
# ---------------------------------------------------------------------------


def generate_music(api_host, api_key, prompt, output_path, instrumental=False):
    """Generate background music via the MiniMax music API and download it."""
    url = f"{api_host}/v1/music_generation"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    effective_prompt = prompt or "background music, cinematic, ambient"
    if instrumental:
        full_prompt = f"{effective_prompt}. pure music, no lyrics"
        lyrics = "[intro] [outro]"
    else:
        full_prompt = effective_prompt
        lyrics = "[Intro]\nla da da\nla la la"

    payload = {
        "model": "music-2.5",
        "prompt": full_prompt,
        "lyrics": lyrics,
        "output_format": "url",
    }

    kind = "instrumental " if instrumental else ""
    print(f"Generating {kind}music...", file=sys.stderr)
    print(f"  Prompt: {prompt}", file=sys.stderr)

    data = api_request("POST", url, headers=headers, json_body=payload, timeout=300)

    audio_url = (
        data.get("data", {}).get("audio_url")
        or data.get("data", {}).get("audio")
        or data.get("data", {}).get("audio_file", {}).get("download_url")
        or ""
    )
    if not audio_url:
        print("Error: No audio URL in music response", file=sys.stderr)
        sys.exit(1)

    # Download with retry
    for attempt in range(1, 4):
        try:
            download_file(audio_url, output_path, timeout=120)
            return output_path
        except SystemExit:
            if attempt < 3:
                wait = 2 ** attempt
                print(f"  Download attempt {attempt} failed. Retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
            else:
                print("Error: Music download failed after 3 attempts", file=sys.stderr)
                sys.exit(1)


# ---------------------------------------------------------------------------
# Audio/video merge
# ---------------------------------------------------------------------------


def merge_video_audio(video_path, audio_path, output_path,
                      bgm_volume=DEFAULT_BGM_VOLUME, fade_in=0, fade_out=0):
    """Merge a video file with an audio file using ffmpeg."""
    duration = get_video_duration(video_path)
    print(f"Video duration: {duration:.1f}s", file=sys.stderr)

    bgm_filter = f"[1:a]volume={bgm_volume}"
    if fade_in > 0:
        bgm_filter += f",afade=t=in:d={fade_in}"
    if fade_out > 0:
        fo_start = max(duration - fade_out, 0)
        bgm_filter += f",afade=t=out:st={fo_start}:d={fade_out}"
    bgm_filter += "[bgm]"

    ensure_dir(Path(output_path).parent)

    has_audio = video_has_audio(video_path)

    if has_audio:
        # Mix with original audio
        filter_complex = f"{bgm_filter};[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]"
        print(f"Merging video + audio (mixing with original, bgm_volume={bgm_volume})...", file=sys.stderr)
        run_ffmpeg([
            "-y",
            "-i", str(video_path), "-i", str(audio_path),
            "-filter_complex", filter_complex,
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac", "-shortest",
            str(output_path),
        ])
    else:
        filter_complex = bgm_filter
        print(f"Merging video + audio (no original audio, bgm_volume={bgm_volume})...", file=sys.stderr)
        run_ffmpeg([
            "-y",
            "-i", str(video_path), "-i", str(audio_path),
            "-filter_complex", filter_complex,
            "-map", "0:v", "-map", "[bgm]",
            "-c:v", "copy", "-c:a", "aac", "-shortest",
            str(output_path),
        ])


# ---------------------------------------------------------------------------
# Subcommand: video (single video generation)
# ---------------------------------------------------------------------------


def build_video_payload(args):
    """Build the JSON payload for a single video generation request."""
    mode = args.mode
    model = args.model or default_model_for_mode(mode)
    duration = int(args.duration)
    resolution = args.resolution

    validate_duration_resolution(model, duration, resolution)

    payload = {"model": model}

    if args.prompt:
        payload["prompt"] = args.prompt
    payload["duration"] = duration
    payload["resolution"] = resolution

    if mode == "i2v":
        if not args.first_frame:
            print("Error: --first-frame is required for i2v mode", file=sys.stderr)
            sys.exit(1)
        ff_url = resolve_image(args.first_frame)
        payload["first_frame_image"] = ff_url

    elif mode == "sef":
        if not args.first_frame:
            print("Error: --first-frame is required for sef mode", file=sys.stderr)
            sys.exit(1)
        ff_url = resolve_image(args.first_frame)
        payload["first_frame_image"] = ff_url
        if args.last_frame:
            lf_url = resolve_image(args.last_frame)
            payload["last_frame_image"] = lf_url

    elif mode == "ref":
        if not args.subject_image:
            print("Error: --subject-image is required for ref mode", file=sys.stderr)
            sys.exit(1)
        si_url = resolve_image(args.subject_image)
        payload["subject_reference"] = [{"type": "character", "image": [si_url]}]
        if args.first_frame:
            ff_url = resolve_image(args.first_frame)
            payload["first_frame_image"] = ff_url

    return payload, model


def cmd_video(args):
    """Generate a single video."""
    load_env()
    api_key = get_api_key()
    api_host = get_api_host()

    payload, model = build_video_payload(args)

    print(f"Mode: {args.mode}", file=sys.stderr)
    print(f"Model: {model}", file=sys.stderr)

    task_id = create_video_task(api_host, api_key, payload)
    file_id = poll_video_task(api_host, api_key, task_id)
    download_video_by_file_id(api_host, api_key, file_id, args.output)
    print("Done!")


# ---------------------------------------------------------------------------
# Subcommand: long-video (multi-scene)
# ---------------------------------------------------------------------------


def cmd_long_video(args):
    """Generate a multi-scene long video by chaining segments."""
    load_env()
    api_key = get_api_key()
    api_host = get_api_host()

    scenes = args.scenes
    if not scenes:
        print("Error: --scenes requires at least one scene prompt", file=sys.stderr)
        sys.exit(1)
    if not args.output:
        print("Error: --output is required", file=sys.stderr)
        sys.exit(1)

    segment_duration = int(args.segment_duration)
    resolution = args.resolution
    crossfade = float(args.crossfade)
    first_frame = args.first_frame or ""

    validate_duration_resolution(DEFAULT_MODEL_T2V_I2V, segment_duration, resolution)

    output_dir = Path(args.output).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    tmpdir = output_dir / "tmp"
    tmpdir.mkdir(parents=True, exist_ok=True)
    print(f"Temp directory: {tmpdir}")

    segment_paths = []
    current_first_frame = first_frame

    print(f"=== Generating {len(scenes)} video segments ===")
    print()

    for i, scene in enumerate(scenes):
        print(f"--- Segment {i+1}/{len(scenes)} ---")
        print(f"  Prompt: {scene}")

        seg_output = str(tmpdir / f"segment_{i:03d}.mp4")

        # Determine mode
        if current_first_frame:
            seg_mode = "i2v"
        else:
            seg_mode = "t2v"

        seg_model = args.model or default_model_for_mode(seg_mode)

        # Build payload
        payload = {
            "model": seg_model,
            "prompt": scene,
            "duration": segment_duration,
            "resolution": resolution,
        }

        if seg_mode == "i2v":
            ff_url = resolve_image(current_first_frame)
            payload["first_frame_image"] = ff_url
            payload["prompt_optimizer"] = False

        # Generate segment
        try:
            task_id = create_video_task(api_host, api_key, payload)
            file_id = poll_video_task(api_host, api_key, task_id)
            download_video_by_file_id(api_host, api_key, file_id, seg_output)
            segment_paths.append(seg_output)

            # Extract last frame for next segment
            last_frame_path = str(tmpdir / f"last_frame_{i:03d}.jpg")
            if extract_last_frame(seg_output, last_frame_path):
                current_first_frame = last_frame_path
            else:
                current_first_frame = ""
        except SystemExit:
            print(f"  Error generating segment {i+1}", file=sys.stderr)
            if not segment_paths:
                sys.exit(1)
            break

    if not segment_paths:
        print("Error: No segments were generated.", file=sys.stderr)
        sys.exit(1)

    # Concatenate
    final_video = args.output
    if args.music_prompt:
        final_video = str(tmpdir / "concatenated.mp4")

    if len(segment_paths) == 1:
        shutil.copy2(segment_paths[0], final_video)
    else:
        concatenate_videos(final_video, crossfade, segment_paths)

    # Add BGM if requested
    if args.music_prompt:
        print()
        print("--- Generating background music ---")
        music_path = str(tmpdir / "bgm.mp3")
        try:
            generate_music(api_host, api_key, args.music_prompt, music_path, instrumental=True)
            try:
                merge_video_audio(final_video, music_path, args.output)
            except SystemExit:
                print("Warning: Failed to add BGM, using video without music", file=sys.stderr)
                if final_video != args.output:
                    shutil.copy2(final_video, args.output)
        except SystemExit:
            print("Warning: Failed to generate BGM", file=sys.stderr)
            if final_video != args.output:
                shutil.copy2(final_video, args.output)

    print()
    print(f"=== Done! Output: {args.output} ===")
    print(f"  Intermediate files in: {tmpdir}")
    print(f"  Delete with: rm -rf {tmpdir}")


# ---------------------------------------------------------------------------
# Subcommand: template
# ---------------------------------------------------------------------------


def cmd_template(args):
    """Generate a video from a template."""
    load_env()
    api_key = get_api_key()
    api_host = get_api_host()

    if not args.template_id:
        print("Error: --template-id is required", file=sys.stderr)
        sys.exit(1)
    if not args.output:
        print("Error: --output is required", file=sys.stderr)
        sys.exit(1)

    template_url = f"{api_host}/v1/video_template_generation"
    query_url = f"{api_host}/v1/query/video_template_generation"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {"template_id": args.template_id}

    # Add media inputs
    if args.media:
        media_inputs = []
        for idx, media_val in enumerate(args.media):
            resolved = resolve_media(media_val)
            media_inputs.append({"value": resolved})
            print(f"  Media [{idx}]: {media_val}")
        payload["media_inputs"] = media_inputs

    # Add text inputs
    if args.text:
        text_inputs = []
        for idx, text_val in enumerate(args.text):
            text_inputs.append({"value": text_val})
            print(f"  Text [{idx}]: {text_val}")
        payload["text_inputs"] = text_inputs

    # Create task
    print(f"Creating template video task (template: {args.template_id})...")
    data = api_request("POST", template_url, headers=headers, json_body=payload, timeout=REQUEST_TIMEOUT)
    task_id = data.get("task_id", "")
    if not task_id:
        print("Error: No task_id in response", file=sys.stderr)
        sys.exit(1)
    print(f"Task created: {task_id}")

    # Poll task -- template API returns video_url directly
    video_url = poll_video_task(api_host, api_key, task_id, query_path="query/video_template_generation")
    # poll_video_task returns video_url for template tasks

    # Download directly from video_url
    print("Downloading video...")
    ensure_dir(Path(args.output).parent)
    download_file(video_url, args.output)
    print("Done!")


# ---------------------------------------------------------------------------
# Subcommand: add-bgm
# ---------------------------------------------------------------------------


def cmd_add_bgm(args):
    """Add background music to a video."""
    load_env()

    if not args.video or not Path(args.video).is_file():
        print(f"Error: Video file not found: {args.video or '<none>'}", file=sys.stderr)
        sys.exit(1)
    if not args.audio and not args.generate_bgm:
        print("Error: Provide --audio or --generate-bgm", file=sys.stderr)
        sys.exit(1)
    if not args.output:
        print("Error: --output is required", file=sys.stderr)
        sys.exit(1)

    audio_path = args.audio

    if args.generate_bgm:
        api_key = get_api_key()
        api_host = get_api_host()
        # Derive BGM path from output path
        audio_path = str(Path(args.output).with_suffix("")) + "_bgm.mp3"
        generate_music(api_host, api_key, args.music_prompt or "", audio_path, instrumental=args.instrumental)

    if not audio_path or not Path(audio_path).is_file():
        print(f"Error: Audio file not found: {audio_path}", file=sys.stderr)
        sys.exit(1)

    merge_video_audio(
        args.video,
        audio_path,
        args.output,
        bgm_volume=args.bgm_volume,
    )

    print(f"Output saved: {args.output}")
    print("Done!")


# ---------------------------------------------------------------------------
# CLI setup
# ---------------------------------------------------------------------------


def build_parser():
    """Build the argparse parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="minimax_video.py",
        description="MiniMax Video Toolkit: generate, concatenate, template, and add BGM to videos.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # -- video --
    p_video = subparsers.add_parser("video", help="Generate a single video")
    p_video.add_argument("--mode", choices=["t2v", "i2v", "sef", "ref"], default="t2v",
                         help="Generation mode (default: t2v)")
    p_video.add_argument("--prompt", type=str, default="",
                         help="Video description")
    p_video.add_argument("--first-frame", type=str, default="",
                         help="First frame image (for i2v, sef)")
    p_video.add_argument("--last-frame", type=str, default="",
                         help="Last frame image (for sef)")
    p_video.add_argument("--subject-image", type=str, default="",
                         help="Subject reference image (for ref)")
    p_video.add_argument("--duration", type=int, default=DEFAULT_DURATION,
                         help="Duration: 6 or 10 (default: 10)")
    p_video.add_argument("--resolution", type=str, default=DEFAULT_RESOLUTION,
                         help="Resolution: 720P, 768P, 1080P, 512P (default: 768P)")
    p_video.add_argument("--model", type=str, default="",
                         help="Model name")
    p_video.add_argument("--seed", type=int, default=None,
                         help="Random seed")
    p_video.add_argument("-o", "--output", type=str, required=True,
                         help="Output path")
    p_video.set_defaults(func=cmd_video)

    # -- long-video --
    p_long = subparsers.add_parser("long-video", help="Generate a multi-scene long video")
    p_long.add_argument("--scenes", nargs="+", required=True,
                        help="Scene prompts (at least 1)")
    p_long.add_argument("--model", type=str, default="",
                        help="Model name (default: auto)")
    p_long.add_argument("--segment-duration", type=int, default=DEFAULT_DURATION,
                        help="Duration per segment (default: 10)")
    p_long.add_argument("--resolution", type=str, default=DEFAULT_RESOLUTION,
                        help="Resolution per segment (default: 768P)")
    p_long.add_argument("--first-frame", type=str, default="",
                        help="First frame for scene 1 (local file or URL)")
    p_long.add_argument("--crossfade", type=float, default=DEFAULT_CROSSFADE,
                        help="Crossfade duration between segments (default: 0.5)")
    p_long.add_argument("--music-prompt", type=str, default="",
                        help="BGM prompt for auto-generated music")
    p_long.add_argument("--bgm-volume", type=float, default=DEFAULT_BGM_VOLUME,
                        help="BGM volume (default: 0.3)")
    p_long.add_argument("-o", "--output", type=str, required=True,
                        help="Output path")
    p_long.set_defaults(func=cmd_long_video)

    # -- template --
    p_tmpl = subparsers.add_parser("template", help="Generate a template-based video")
    p_tmpl.add_argument("--template-id", type=str, required=True,
                        help="Template ID")
    p_tmpl.add_argument("--media", nargs="+", default=[],
                        help="Photo/image files or URLs")
    p_tmpl.add_argument("--text", nargs="+", default=[],
                        help="Text inputs for template slots")
    p_tmpl.add_argument("-o", "--output", type=str, required=True,
                        help="Output path")
    p_tmpl.set_defaults(func=cmd_template)

    # -- add-bgm --
    p_bgm = subparsers.add_parser("add-bgm", help="Add background music to a video")
    p_bgm.add_argument("--video", type=str, required=True,
                       help="Input video file")
    p_bgm.add_argument("--audio", type=str, default="",
                       help="Audio file to overlay")
    p_bgm.add_argument("--generate-bgm", action="store_true",
                       help="Auto-generate BGM via music API")
    p_bgm.add_argument("--instrumental", action="store_true",
                       help="Generate instrumental BGM")
    p_bgm.add_argument("--music-prompt", type=str, default="",
                       help="Music style prompt")
    p_bgm.add_argument("--bgm-volume", type=float, default=DEFAULT_BGM_VOLUME,
                       help="BGM volume (0.0-1.0, default: 0.3)")
    p_bgm.add_argument("-o", "--output", type=str, required=True,
                       help="Output path")
    p_bgm.set_defaults(func=cmd_add_bgm)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
