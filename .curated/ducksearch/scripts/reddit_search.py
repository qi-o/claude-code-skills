#!/usr/bin/env python3
"""
Reddit search via Reddit JSON API (no API key required).
Usage:
  python reddit_search.py "关键词" [--subreddit NAME] [--max N] [--output text|json]
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request


def search_reddit(query: str, subreddit: str = "", max_results: int = 10) -> list:
    """Search Reddit using the public JSON API."""
    if subreddit:
        url = (
            f"https://www.reddit.com/r/{subreddit}/search.json"
            f"?q={urllib.parse.quote(query)}&restrict_sr=true&sort=relevance&limit={max_results}"
        )
    else:
        url = (
            f"https://www.reddit.com/search.json"
            f"?q={urllib.parse.quote(query)}&sort=relevance&limit={max_results}"
        )

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "rss-reader/1.0 (academic research tool)"},
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"Error: Reddit API returned {e.code}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    results = []
    for post in data.get("data", {}).get("children", []):
        d = post.get("data", {})
        results.append({
            "title": d.get("title", ""),
            "subreddit": f"r/{d.get('subreddit', '')}",
            "url": "https://reddit.com" + d.get("permalink", ""),
            "score": d.get("score", 0),
            "num_comments": d.get("num_comments", 0),
            "snippet": (d.get("selftext", "") or "")[:200],
        })

    return results


def print_text(results: list):
    if not results:
        print("No Reddit results found.")
        return
    for i, r in enumerate(results, 1):
        print(f"[{i}] {r['title']}")
        print(f"    {r['subreddit']}  |  {r['score']} pts  |  {r['num_comments']} comments")
        if r["snippet"]:
            print(f"    {r['snippet'].strip()[:120]}...")
        print(f"    {r['url']}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Search Reddit via Reddit JSON API")
    parser.add_argument("query", help="Search keywords")
    parser.add_argument("--subreddit", default="", help="Limit to a specific subreddit")
    parser.add_argument("--max", type=int, default=10, dest="max_results", help="Max results (default: 10)")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    # Fix Windows GBK terminal encoding
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    results = search_reddit(args.query, args.subreddit, args.max_results)

    if args.output == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_text(results)


if __name__ == "__main__":
    main()
