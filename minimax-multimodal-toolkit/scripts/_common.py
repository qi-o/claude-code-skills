"""
MiniMax Multi-Modal Toolkit -- Shared utilities for all Python scripts.

Provides env loading, API helpers, file downloads, and ffmpeg wrappers.
All downstream scripts should import from this module rather than duplicating
these helpers.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_API_HOST = "https://api.minimax.io"
DEFAULT_OUTPUT_DIR = "minimax-output"
REQUEST_TIMEOUT = 120
DOWNLOAD_TIMEOUT = 300
FFMPEG_TIMEOUT = 300

ENV_FILE_PATHS = [
    Path.home() / ".claude" / "env.d" / "minimax.env",
    Path(".env"),
]


# ---------------------------------------------------------------------------
# Environment loading
# ---------------------------------------------------------------------------

def load_env():
    """Load KEY=VALUE pairs from env files into os.environ.

    Searches ``~/.claude/env.d/minimax.env`` first, then ``.env`` in CWD.
    Lines starting with ``#`` are skipped.  Surrounding quotes are stripped.
    Values are only set when the key is not already present in the
    environment (system / caller values take precedence).
    """
    for env_file in ENV_FILE_PATHS:
        env_file = Path(env_file).resolve()
        if not env_file.is_file():
            continue
        with open(env_file, "r", encoding="utf-8") as fh:
            for raw_line in fh:
                line = raw_line.split("#", 1)[0].strip()
                if not line or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                key = key.strip()
                val = val.strip()
                # Remove surrounding quotes (single or double)
                if len(val) >= 2:
                    if (val[0] == '"' and val[-1] == '"') or (
                        val[0] == "'" and val[-1] == "'"
                    ):
                        val = val[1:-1]
                if key not in os.environ:
                    os.environ[key] = val


def get_api_key():
    """Return the MINIMAX_API_KEY from the environment.

    Calls ``load_env()`` first so that env files are always consulted.
    Raises ``SystemExit`` if the key is missing.
    """
    load_env()
    api_key = os.environ.get("MINIMAX_API_KEY", "")
    if not api_key:
        print("Error: MINIMAX_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    return api_key


def get_api_host():
    """Return the MINIMAX_API_HOST from the environment, defaulting to ``DEFAULT_API_HOST``."""
    load_env()
    return os.environ.get("MINIMAX_API_HOST", DEFAULT_API_HOST)


def get_output_dir():
    """Return the MINIMAX_OUTPUT_DIR from the environment, defaulting to ``DEFAULT_OUTPUT_DIR``."""
    load_env()
    return os.environ.get("MINIMAX_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def api_request(method, url, headers=None, json_body=None, timeout=REQUEST_TIMEOUT):
    """Make an HTTP request and check for MiniMax ``base_resp`` errors.

    Parameters
    ----------
    method : str
        HTTP method (``GET``, ``POST``, ...).
    url : str
        Full URL (including path).
    headers : dict | None
        Extra request headers.  ``Authorization`` is **not** added
        automatically -- the caller must supply it.
    json_body : dict | list | None
        JSON-serialisable body for POST/PUT requests.
    timeout : int
        Seconds before the request times out.

    Returns
    -------
    dict
        Parsed JSON response body.

    Raises
    ------
    SystemExit
        On HTTP errors or MiniMax ``base_resp`` error codes.
    """
    merged_headers = {"Accept-Encoding": "gzip, deflate"}
    if headers:
        merged_headers.update(headers)

    try:
        resp = requests.request(
            method,
            url,
            headers=merged_headers,
            json=json_body,
            timeout=timeout,
        )
    except requests.RequestException as exc:
        print(f"Error: request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    if resp.status_code >= 400:
        print(f"Error: API returned HTTP {resp.status_code}", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        sys.exit(1)

    try:
        data = resp.json()
    except (json.JSONDecodeError, ValueError):
        print("Error: response is not valid JSON", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        sys.exit(1)

    base_resp = data.get("base_resp", {})
    if base_resp.get("status_code", 0) != 0:
        code = base_resp.get("status_code")
        msg = base_resp.get("status_msg", "Unknown error")
        raise SystemExit(f"API Error [{code}]: {msg}")

    return data


def download_file(url, output_path, timeout=DOWNLOAD_TIMEOUT):
    """Download *url* to *output_path* with a progress indicator.

    Parameters
    ----------
    url : str
        Remote URL to download.
    output_path : str | Path
        Local file path to write.
    timeout : int
        Seconds before the download times out.

    Raises
    ------
    SystemExit
        On network failure or non-2xx HTTP status.
    """
    output_path = Path(output_path)
    ensure_dir(output_path.parent)

    try:
        resp = requests.get(url, stream=True, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"Error: download failed: {exc}", file=sys.stderr)
        sys.exit(1)

    total = int(resp.headers.get("content-length", 0))
    downloaded = 0
    with open(output_path, "wb") as fh:
        for chunk in resp.iter_content(chunk_size=8192):
            fh.write(chunk)
            downloaded += len(chunk)
            if total > 0:
                pct = downloaded / total * 100
                print(f"\r  Downloading: {pct:5.1f}%", end="", flush=True)

    if total > 0:
        print()  # newline after progress bar

    size = output_path.stat().st_size
    print(f"  Saved: {output_path} ({size} bytes)")


# ---------------------------------------------------------------------------
# FFmpeg helpers
# ---------------------------------------------------------------------------

def run_ffmpeg(args, timeout=FFMPEG_TIMEOUT):
    """Run ffmpeg with the given argument list, raising on non-zero exit.

    Parameters
    ----------
    args : list[str]
        Arguments passed directly to the ffmpeg binary (e.g.
        ``["-y", "-i", "input.mp4", "output.mp4"]``).
    timeout : int
        Maximum seconds to wait.

    Returns
    -------
    subprocess.CompletedProcess

    Raises
    ------
    SystemExit
        If ffmpeg is not found or exits with a non-zero code.
    """
    cmd = ["ffmpeg"] + args
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
    except FileNotFoundError:
        print("Error: ffmpeg not found. Install it first.", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(f"Error: ffmpeg timed out after {timeout}s", file=sys.stderr)
        sys.exit(1)

    if result.returncode != 0:
        print(f"Error: ffmpeg exited with code {result.returncode}", file=sys.stderr)
        if result.stderr:
            print(result.stderr.decode("utf-8", errors="replace"), file=sys.stderr)
        sys.exit(1)

    return result


# ---------------------------------------------------------------------------
# Filesystem helpers
# ---------------------------------------------------------------------------

def ensure_dir(path):
    """Create *path* (and parents) if it does not already exist.

    Parameters
    ----------
    path : str | Path
        Directory path to create.
    """
    Path(path).mkdir(parents=True, exist_ok=True)
