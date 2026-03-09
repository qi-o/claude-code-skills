#!/usr/bin/env python3
"""
rss_fetch.py - Academic RSS feed fetcher with keyword filtering.
Usage: python rss_fetch.py --source biorxiv --keywords "single cell,RNA-seq" --days 7
"""

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta

try:
    import feedparser
except ImportError:
    print("Error: feedparser not installed. Run: pip install feedparser")
    sys.exit(1)

# Preset academic RSS feeds
FEEDS = {
    "biorxiv": "https://connect.biorxiv.org/biorxiv_xml.php?subject=bioinformatics",
    "biorxiv-all": "https://connect.biorxiv.org/biorxiv_xml.php?subject=all",
    "medrxiv": "https://connect.medrxiv.org/medrxiv_xml.php?subject=all",
    # Note: PubMed RSS requires login; use paper-search skill for PubMed queries
    "nature": "https://www.nature.com/nature.rss",
    "cell": "https://www.cell.com/cell/current.rss",
    "science": "https://www.science.org/rss/news_current.xml",
    "nejm": (
        "https://www.nejm.org/action/showFeed"
        "?jc=nejm&type=etoc&feed=rss"
    ),
    "pnas": "https://www.pnas.org/rss/current.xml",
    "elife": "https://elifesciences.org/rss/recent.xml",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fetch and filter academic RSS feeds."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--feed", help="Custom RSS feed URL")
    group.add_argument(
        "--source",
        choices=list(FEEDS.keys()),
        help="Preset source name",
    )
    parser.add_argument(
        "--keywords",
        default="",
        help="Comma-separated keywords to filter (title + abstract)",
    )
    parser.add_argument(
        "--max", type=int, default=20, dest="max_items",
        help="Maximum number of results (default: 20)",
    )
    parser.add_argument(
        "--days", type=int, default=7,
        help="Only return articles from the last N days (default: 7)",
    )
    parser.add_argument(
        "--output", choices=["text", "json"], default="text",
        help="Output format (default: text)",
    )
    return parser.parse_args()


def entry_date(entry):
    """Return a timezone-aware datetime for a feed entry, or None."""
    for attr in ("published_parsed", "updated_parsed"):
        t = getattr(entry, attr, None)
        if t:
            try:
                return datetime(*t[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return None


def matches_keywords(entry, keywords):
    """Return True if any keyword appears in title or summary."""
    if not keywords:
        return True
    title = getattr(entry, "title", "") or ""
    summary = getattr(entry, "summary", "") or ""
    text = (title + " " + summary).lower()
    return any(kw.lower() in text for kw in keywords)


def fetch_feed(url, keywords, max_items, days):
    """Fetch and filter a feed. Returns list of dicts."""
    try:
        feed = feedparser.parse(url, request_headers={"User-Agent": "rss-reader/1.0"})
    except Exception as exc:
        print(f"Error fetching feed: {exc}", file=sys.stderr)
        sys.exit(1)

    if feed.bozo and not feed.entries:
        print(
            f"Warning: feed parse issue: {feed.bozo_exception}", file=sys.stderr
        )

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    results = []

    for entry in feed.entries:
        pub = entry_date(entry)
        if pub and pub < cutoff:
            continue
        if not matches_keywords(entry, keywords):
            continue

        authors = ""
        if hasattr(entry, "authors"):
            authors = ", ".join(
                a.get("name", "") for a in entry.authors if a.get("name")
            )
        elif hasattr(entry, "author"):
            authors = entry.author

        results.append(
            {
                "title": getattr(entry, "title", "No title"),
                "authors": authors,
                "date": pub.strftime("%Y-%m-%d") if pub else "Unknown",
                "summary": (getattr(entry, "summary", "") or "")[:200],
                "link": getattr(entry, "link", ""),
            }
        )
        if len(results) >= max_items:
            break

    return results


def print_text(results):
    if not results:
        print("No articles found matching your criteria.")
        return
    for i, r in enumerate(results, 1):
        print(f"\n{'='*60}")
        print(f"[{i}] {r['title']}")
        print(f"Authors : {r['authors'] or 'N/A'}")
        print(f"Date    : {r['date']}")
        print(f"Abstract: {r['summary']}...")
        print(f"Link    : {r['link']}")
    print(f"\n{'='*60}")
    print(f"Total: {len(results)} article(s)")


def main():
    args = parse_args()
    url = args.feed if args.feed else FEEDS[args.source]
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]

    results = fetch_feed(url, keywords, args.max_items, args.days)

    if args.output == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_text(results)


if __name__ == "__main__":
    main()
