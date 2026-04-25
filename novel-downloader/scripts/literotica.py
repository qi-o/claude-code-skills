#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Literotica 小说下载器
支持: 作者作品页、系列页、单篇故事
自动按系列合并输出
"""
import subprocess
import re
import os
import time
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_URL = "https://www.literotica.com"

# 修改这里 ======
# 支持三种URL格式:
#   作者页: https://www.literotica.com/authors/USERNAME/works/stories
#   系列页: https://www.literotica.com/series/se/SLUG
#   单篇:   https://www.literotica.com/s/STORY-SLUG
URL = "https://www.literotica.com/authors/Fuzzypen/works/stories"
OUTPUT_DIR = ""  # 留空则自动在当前目录创建
# ===============

def fetch_url(url, retries=3):
    for attempt in range(retries):
        try:
            result = subprocess.run([
                'curl', '-s', '-L', '-k', '--http1.1',
                '--connect-timeout', '15', '--max-time', '60',
                '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                '-H', 'Accept: text/html,application/xhtml+xml',
                '-H', 'Accept-Language: en-US,en;q=0.9',
                url
            ], capture_output=True, timeout=90)
            html = result.stdout.decode('utf-8', errors='replace')
            if html and len(html) > 100:
                return html
        except (subprocess.TimeoutExpired, Exception) as e:
            print(f"    retry {attempt+1}/{retries}: {e}")
            time.sleep(3 * (attempt + 1))
    return ""

def get_stories_from_author(url):
    html = fetch_url(url)
    if not html:
        return "Unknown", []
    titles = re.findall(
        r'<a[^>]*href="(https://www\.literotica\.com/s/[^"]+)"[^>]*>([^<]+)</a>',
        html
    )
    seen = set()
    stories = []
    for surl, title in titles:
        if surl not in seen:
            seen.add(surl)
            stories.append((surl, title.strip()))
    soup = BeautifulSoup(html, 'html.parser')
    author = "Unknown"
    author_el = soup.select_one('a[href*="/authors/"]')
    if author_el:
        author = author_el.get_text(strip=True)
    return author, stories

def get_chapters_from_series(url):
    html = fetch_url(url)
    if not html:
        return "Unknown", "Unknown", []
    slug_match = re.search(r'/series/se/([^/]+)', url)
    slug = slug_match.group(1) if slug_match else ""
    chapters = []
    if slug:
        matches = re.findall(rf'/s/{slug}-ch-(\d+)', html)
        seen = set()
        for num in matches:
            if num not in seen:
                seen.add(num)
                chapters.append({
                    'url': f"{BASE_URL}/s/{slug}-ch-{num}",
                    'title': f"Chapter {int(num)}"
                })
        chapters.sort(key=lambda x: int(re.search(r'ch-(\d+)', x['url']).group(1)))
    soup = BeautifulSoup(html, 'html.parser')
    title = slug.replace('-', ' ').title() if slug else "Unknown"
    author = "Unknown"
    author_el = soup.select_one('a[href*="/authors/"]')
    if author_el:
        author = author_el.get_text(strip=True)
    return title, author, chapters

def get_story_content(url):
    all_text = []
    current_page = 1
    title = None

    while True:
        page_url = url if current_page == 1 else f"{url}?page={current_page}"
        html = fetch_url(page_url)
        if not html:
            break
        soup = BeautifulSoup(html, 'html.parser')

        if title is None:
            h1 = soup.select_one('h1')
            if h1:
                title = h1.get_text(strip=True)

        content_div = soup.select_one('div[class*="_article__content"]')
        if content_div:
            paragraphs = content_div.find_all('p')
            text = '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)) if paragraphs else content_div.get_text('\n', strip=True)
            if text and len(text) > 50:
                all_text.append(text)

        next_page_link = soup.select_one(f'a[href*="?page={current_page + 1}"]')
        if next_page_link:
            current_page += 1
            time.sleep(0.5)
        else:
            break

    return title or "Unknown", '\n\n'.join(all_text)

def slug_to_filename(slug):
    name = os.path.basename(slug)
    return re.sub(r'[\\/*?:"<>|]', '', name)[:80]

def detect_url_type(url):
    if '/authors/' in url:
        return 'author'
    elif '/series/' in url:
        return 'series'
    elif '/s/' in url:
        return 'single'
    return 'unknown'

def group_stories(stories):
    series_map = {}
    standalone = []
    for url, title in stories:
        slug = url.split('/s/')[-1]
        series_match = re.match(r'^(.+?)-(?:ch|pt)-(\d+)$', slug)
        if series_match:
            series_name = series_match.group(1)
            ch_num = int(series_match.group(2))
            if series_name not in series_map:
                series_map[series_name] = []
            series_map[series_name].append((ch_num, url, title))
        else:
            standalone.append((url, title))
    for k in series_map:
        series_map[k].sort(key=lambda x: x[0])
    return standalone, series_map

def download_and_save(url, filepath, label=""):
    if os.path.exists(filepath):
        print(f"  SKIP (exists): {label}")
        return True
    print(f"  {label}")
    story_title, content = get_story_content(url)
    if content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"{story_title}\n{'=' * 50}\n\n{content}")
        print(f"    OK ({len(content)} chars)")
        return True
    else:
        print(f"    FAILED - empty content")
        return False

def main():
    global OUTPUT_DIR
    url_type = detect_url_type(URL)

    if url_type == 'author':
        print(f"Fetching author page...")
        author, stories = get_stories_from_author(URL)
        if not stories:
            print("No stories found.")
            return
        if not OUTPUT_DIR:
            OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), slug_to_filename(author.lower().replace(' ', '-')))
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        print(f"Author: {author}")
        print(f"Stories: {len(stories)}\n")

        standalone, series_map = group_stories(stories)

        for i, (surl, title) in enumerate(standalone, 1):
            slug = surl.split('/s/')[-1]
            filepath = os.path.join(OUTPUT_DIR, slug_to_filename(slug) + '.txt')
            download_and_save(surl, filepath, f"[standalone {i}/{len(standalone)}] {title}")
            time.sleep(1)

        series_parts = {}
        for series_name, chapters in series_map.items():
            sdir = os.path.join(OUTPUT_DIR, slug_to_filename(series_name))
            os.makedirs(sdir, exist_ok=True)
            print(f"\nSeries: {series_name} ({len(chapters)} chapters)")
            for i, (ch_num, curl, ctitle) in enumerate(chapters, 1):
                filename = f"ch{ch_num:02d}_{slug_to_filename(curl.split('/s/')[-1])}.txt"
                filepath = os.path.join(sdir, filename)
                download_and_save(curl, filepath, f"  [{i}/{len(chapters)}] {ctitle}")
                time.sleep(1)
            series_parts[series_name] = sdir

        # Merge series into single files
        for series_name, sdir in series_parts.items():
            merged = os.path.join(OUTPUT_DIR, slug_to_filename(series_name) + '.txt')
            files = sorted([os.path.join(sdir, f) for f in os.listdir(sdir) if f.endswith('.txt')])
            with open(merged, 'w', encoding='utf-8') as out:
                for fp in files:
                    with open(fp, 'r', encoding='utf-8') as inp:
                        out.write(inp.read())
                        out.write('\n\n')
            # Remove chapter directory
            import shutil
            shutil.rmtree(sdir)
            print(f"\nMerged: {slug_to_filename(series_name)}.txt ({len(files)} chapters)")

    elif url_type == 'series':
        print("Fetching series...")
        title, author, chapters = get_chapters_from_series(URL)
        if not chapters:
            print("No chapters found.")
            return
        if not OUTPUT_DIR:
            OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
        filename = slug_to_filename(title.lower().replace(' ', '-')) + '.txt'
        filepath = os.path.join(OUTPUT_DIR, filename)

        content_parts = [f"{title}\nAuthor: {author}\n{'=' * 50}\n"]
        for i, ch in enumerate(chapters, 1):
            print(f"[{i}/{len(chapters)}] {ch['title']}")
            _, text = get_story_content(ch['url'])
            if text:
                content_parts.extend([f"\n{'=' * 30}\n{ch['title']}\n{'=' * 30}\n\n{text}"])
            time.sleep(1)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_parts))
        print(f"\nDone: {filepath}")

    elif url_type == 'single':
        print("Fetching story...")
        if not OUTPUT_DIR:
            OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
        slug = URL.split('/s/')[-1]
        filepath = os.path.join(OUTPUT_DIR, slug_to_filename(slug) + '.txt')
        story_title, content = get_story_content(URL)
        if content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"{story_title}\n{'=' * 50}\n\n{content}")
            print(f"Done: {filepath}")
        else:
            print("Failed to download.")
    else:
        print(f"Unsupported URL: {URL}")

if __name__ == "__main__":
    main()
