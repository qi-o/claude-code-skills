#!/usr/bin/env python3
"""
MiniMax Multi-Modal Toolkit -- Environment Check

Verifies that all required dependencies and configuration are in place.

Usage:
    python check_environment.py
    python check_environment.py --test-api
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

# Allow running as a standalone script or as a module
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import load_env, get_api_host, get_api_key


# ---------------------------------------------------------------------------
# Check functions
# ---------------------------------------------------------------------------

def check_requests():
    """Verify that the ``requests`` library is importable."""
    try:
        import requests  # noqa: F401
        print("[OK] requests installed")
        return True
    except ImportError:
        print("[FAIL] requests not installed (pip install requests)")
        return False


def check_ffmpeg():
    """Verify that ffmpeg is on PATH."""
    if shutil.which("ffmpeg"):
        print("[OK] FFmpeg installed")
        return True
    print("[FAIL] FFmpeg not installed")
    return False


def check_ffprobe():
    """Verify that ffprobe is on PATH."""
    if shutil.which("ffprobe"):
        print("[OK] ffprobe installed")
        return True
    print("[FAIL] ffprobe not installed")
    return False


def check_api_host():
    """Validate MINIMAX_API_HOST value (must be a known MiniMax endpoint)."""
    load_env()
    api_host = get_api_host()
    if not api_host:
        print("[FAIL] MINIMAX_API_HOST not set")
        print("  China Mainland: export MINIMAX_API_HOST='https://api.minimaxi.com'")
        print("  Global:         export MINIMAX_API_HOST='https://api.minimax.io'")
        return False

    known_hosts = (
        "https://api.minimaxi.com",
        "https://api.minimax.io",
    )
    if api_host not in known_hosts:
        print(f"[WARN] MINIMAX_API_HOST has non-standard value: {api_host}")
        print("  Expected: https://api.minimaxi.com (China) or https://api.minimax.io (Global)")
        return True

    print(f"[OK] MINIMAX_API_HOST set ({api_host})")
    return True


def check_api_key():
    """Validate MINIMAX_API_KEY format (must start with sk-api- or sk-cp-)."""
    load_env()
    api_key = os.environ.get("MINIMAX_API_KEY", "")

    if not api_key:
        print("[FAIL] MINIMAX_API_KEY not set")
        print("  export MINIMAX_API_KEY='your-key'")
        return False

    if not (api_key.startswith("sk-api-") or api_key.startswith("sk-cp-")):
        print("[FAIL] Invalid API key format")
        print("  Expected: sk-api-xxx... or sk-cp-xxx...")
        print(f"  Got: {api_key[:20]}...")
        return False

    print(f"[OK] MINIMAX_API_KEY set ({len(api_key)} chars)")
    return True


def check_api_connectivity():
    """Test that the API host is reachable with the configured key."""
    load_env()
    api_host = get_api_host()
    api_key = os.environ.get("MINIMAX_API_KEY", "")

    if not api_key:
        print("[FAIL] API connectivity skipped (MINIMAX_API_KEY not set)")
        return False

    if not api_host:
        print("[FAIL] API connectivity skipped (MINIMAX_API_HOST not set)")
        return False

    try:
        import requests
        resp = requests.get(
            api_host,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )
        if resp.status_code < 500:
            print(f"[OK] API host reachable (HTTP {resp.status_code})")
            return True
    except Exception:
        pass

    print(f"[FAIL] API host unreachable ({api_host})")
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="MiniMax Multi-Modal Toolkit -- Environment Check"
    )
    parser.add_argument(
        "--test-api",
        action="store_true",
        help="Test API connectivity",
    )
    args = parser.parse_args()

    passed = 0
    failed = 0
    total = 0

    checks = [
        check_requests,
        check_ffmpeg,
        check_ffprobe,
        check_api_host,
        check_api_key,
    ]

    if args.test_api:
        checks.append(check_api_connectivity)

    print("MiniMax Multi-Modal Toolkit -- Environment Check")
    print("========================================")

    for check_fn in checks:
        total += 1
        try:
            if check_fn():
                passed += 1
            else:
                failed += 1
        except Exception:
            failed += 1

    print("")
    print("========================================")
    if failed == 0:
        print(f"All {total} checks passed!")
        sys.exit(0)
    else:
        print(f"{failed} check(s) failed out of {total}")
        sys.exit(1)


if __name__ == "__main__":
    main()
