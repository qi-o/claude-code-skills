#!/usr/bin/env python3
"""
从YouTube视频下载字幕（Windows 兼容）。
优先下载人工字幕，无人工字幕则下载自动生成字幕。
语言优先级：中文 > 英文 > 其他。

用法:
    python download_subtitles.py <YouTube_URL> [输出目录]

依赖: yt-dlp (pip install yt-dlp)
"""

import sys
import subprocess
import os
from pathlib import Path
from datetime import datetime


def run_ytdlp(args: list[str]) -> subprocess.CompletedProcess:
    """运行 yt-dlp 命令"""
    cmd = ["yt-dlp"] + args
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def list_subs(url: str) -> str:
    """列出可用字幕"""
    result = run_ytdlp(["--list-subs", "--no-download", url])
    return result.stdout or result.stderr


def try_download(url: str, output_dir: str, lang: str, auto: bool = False) -> Path | None:
    """尝试下载指定语言的字幕，返回下载的文件路径或 None"""
    output_template = str(Path(output_dir) / "%(title)s")

    before = set(Path(output_dir).glob("*.srt")) | set(Path(output_dir).glob("*.vtt"))

    args = [
        "--sub-langs", lang,
        "--sub-format", "srt",
        "--skip-download",
        "-o", output_template,
        url,
    ]
    if auto:
        args.insert(0, "--write-auto-subs")
    else:
        args.insert(0, "--write-subs")

    result = run_ytdlp(args)

    after = set(Path(output_dir).glob("*.srt")) | set(Path(output_dir).glob("*.vtt"))
    new_files = after - before

    if new_files:
        return sorted(new_files, key=lambda f: f.stat().st_mtime, reverse=True)[0]
    return None


def main():
    if len(sys.argv) < 2:
        print("用法: python download_subtitles.py <YouTube_URL> [输出目录]")
        sys.exit(1)

    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) >= 3 else "."
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 检查 yt-dlp 是否可用
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ yt-dlp 未安装。请运行: pip install yt-dlp")
        sys.exit(1)

    print(">>> 检查可用字幕...")
    subs_info = list_subs(url)
    if subs_info:
        # 只显示最后20行（可用字幕列表）
        lines = subs_info.strip().split("\n")
        for line in lines[-20:]:
            print(f"  {line}")

    # 下载策略：人工中文 → 人工英文 → 自动中文 → 自动英文
    strategies = [
        ("zh-Hans,zh-Hant,zh,zh-CN,zh-TW", False, "人工中文"),
        ("en,en-US,en-GB", False, "人工英文"),
        ("zh-Hans,zh,zh-CN", True, "自动中文"),
        ("en,en-US,en-GB", True, "自动英文"),
    ]

    for lang, auto, label in strategies:
        print(f"\n>>> 尝试下载{label}字幕...")
        result = try_download(url, output_dir, lang, auto)
        if result:
            print(f"✅ 下载成功: {result}")
            sys.exit(0)

    print("\n❌ 未找到任何可用字幕")
    sys.exit(1)


if __name__ == "__main__":
    main()
