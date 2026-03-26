#!/usr/bin/env python3
"""Convert MP4 to GIF using ffmpeg two-pass with palettegen"""

import argparse
import os
import subprocess
import sys

def convert_mp4_to_gif(input_path, output_path, fps=15, width=360):
    """Convert MP4 to GIF using ffmpeg two-pass method"""

    # Check ffmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: ffmpeg not found on PATH. Install ffmpeg first.", file=sys.stderr)
        sys.exit(2)

    if not os.path.exists(input_path):
        print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Two-pass GIF creation with palettegen
    palette_file = output_path.replace(".gif", "_palette.png")

    # Pass 1: generate palette
    cmd1 = [
        "ffmpeg", "-y", "-i", input_path,
        "-vf", f"fps={fps},scale={width}:-1:flags=lanczos,palettegen=max_colors=128",
        palette_file
    ]
    print(f"Generating palette for {os.path.basename(input_path)}...")
    result1 = subprocess.run(cmd1, capture_output=True, text=True)
    if result1.returncode != 0:
        print(f"ERROR: ffmpeg pass 1 failed: {result1.stderr}", file=sys.stderr)
        sys.exit(1)

    # Pass 2: create GIF using palette
    cmd2 = [
        "ffmpeg", "-y", "-i", input_path,
        "-i", palette_file,
        "-lavfi", f"fps={fps},scale={width}:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=3",
        output_path
    ]
    print(f"Converting to GIF: {os.path.basename(output_path)}...")
    result2 = subprocess.run(cmd2, capture_output=True, text=True)
    if result2.returncode != 0:
        print(f"ERROR: ffmpeg pass 2 failed: {result2.stderr}", file=sys.stderr)
        sys.exit(1)

    size = os.path.getsize(output_path)
    print(f"Created {output_path} ({size / 1024:.1f} KB)")

    # Clean up palette
    if os.path.exists(palette_file):
        os.remove(palette_file)

    return output_path

def main():
    parser = argparse.ArgumentParser(description="Convert MP4 to GIF with ffmpeg two-pass")
    parser.add_argument("inputs", nargs="+", help="Input MP4 files")
    parser.add_argument("--fps", type=int, default=15, help="Frames per second (default: 15)")
    parser.add_argument("--width", type=int, default=360, help="Output width in pixels (default: 360)")
    args = parser.parse_args()

    for input_path in args.inputs:
        # Derive output path
        basename = os.path.basename(input_path)
        name_without_ext = os.path.splitext(basename)[0]
        output_path = input_path.replace(".mp4", ".gif")

        convert_mp4_to_gif(input_path, output_path, args.fps, args.width)

if __name__ == "__main__":
    main()
