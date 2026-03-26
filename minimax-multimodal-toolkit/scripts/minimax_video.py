#!/usr/bin/env python3
"""MiniMax Video generation (T2V and I2V)"""

import argparse
import base64
import os
import sys
import time
import requests
from pathlib import Path

API_BASE = os.environ.get("MINIMAX_API_HOST", "https://api.minimax.io")
CREATE_ENDPOINT = f"{API_BASE}/v1/video_generation"
QUERY_ENDPOINT = f"{API_BASE}/query/video_generation"
FILE_ENDPOINT = f"{API_BASE}/files/retrieve"

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

def create_video(prompt: str, mode: str = "t2v", image_path: str = "",
                 duration: int = 10, resolution: str = "768P",
                 camera: str = ""):

    api_key = get_api_key()
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": "MiniMax-Hailuo-2.3",
        "prompt": prompt,
        "duration": duration,
        "resolution": resolution,
        "prompt_optimizer": True
    }

    if camera:
        payload["camera_commands"] = camera

    if mode == "i2v" and image_path:
        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        payload["image"] = img_b64
        payload["model"] = "MiniMax-Hailuo-2.3"  # i2v uses same model with image input

    resp = requests.post(CREATE_ENDPOINT, headers=headers, json=payload)
    data = resp.json()

    base_resp = data.get("base_resp", {})
    if base_resp.get("status_code", 0) != 0:
        raise SystemExit(f"API Error [{base_resp.get('status_code')}]: {base_resp.get('status_msg')}")

    task_id = data.get("task_id", "")
    print(f"Task created: {task_id}")
    return task_id

def poll_video(task_id: str, max_wait: int = 600, interval: int = 10):
    api_key = get_api_key()
    headers = {"Authorization": f"Bearer {api_key}"}

    for _ in range(max_wait // interval):
        resp = requests.get(QUERY_ENDPOINT, params={"task_id": task_id}, headers=headers)
        data = resp.json()
        status = data.get("status", "")

        if status == "Success":
            file_id = data.get("file_id", "")
            return file_id
        elif status == "Fail":
            raise SystemExit(f"Video generation failed: {data}")
        else:
            print(f"Status: {status}, waiting...")
            time.sleep(interval)

    raise SystemExit("Video polling timeout")

def download_video(file_id: str, output: str):
    api_key = get_api_key()
    headers = {"Authorization": f"Bearer {api_key}"}

    resp = requests.get(FILE_ENDPOINT, params={"file_id": file_id}, headers=headers)
    data = resp.json()

    video_url = data.get("file_url", {})
    if isinstance(video_url, dict):
        video_url = video_url.get("url", "")

    if not video_url:
        raise SystemExit(f"No URL in response: {data}")

    video_resp = requests.get(video_url)
    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    with open(output, "wb") as f:
        f.write(video_resp.content)
    print(f"Saved video to {output} ({len(video_resp.content)} bytes)")

def generate(prompt: str, output: str, mode: str = "t2v", image_path: str = "",
             duration: int = 10, resolution: str = "768P", camera: str = ""):

    task_id = create_video(prompt, mode, image_path, duration, resolution, camera)
    file_id = poll_video(task_id)
    download_video(file_id, output)

def main():
    p = argparse.ArgumentParser(description="MiniMax Video generation")
    p.add_argument("--mode", default="t2v", help="t2v (text-to-video) or i2v (image-to-video)")
    p.add_argument("--prompt", required=True, help="Video scene description")
    p.add_argument("-o", "--output", required=True, help="Output MP4 file path")
    p.add_argument("--image", default="", help="Input image for i2v mode")
    p.add_argument("--duration", type=int, default=10, help="Duration: 6 or 10 seconds")
    p.add_argument("--resolution", default="768P", help="Resolution: 720P, 768P, 1080P")
    p.add_argument("--camera", default="", help="Camera commands e.g. [Truck left]")
    args = p.parse_args()

    if args.duration not in (6, 10):
        p.error("--duration must be 6 or 10 seconds")
    if args.resolution not in ("720P", "768P", "1080P"):
        p.error("--resolution must be 720P, 768P, or 1080P")

    generate(args.prompt, args.output, args.mode, args.image, args.duration, args.resolution, args.camera)

if __name__ == "__main__":
    main()