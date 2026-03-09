#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hostboard.com 论坛小说下载器
依赖: pip install DrissionPage beautifulsoup4

使用方法:
1. 修改 URLS 列表为目标帖子URL
2. 修改 OUTPUT_DIR 为输出目录
3. 运行: python -X utf8 hostboard.py

特点:
- 使用 DrissionPage 绕过 Cloudflare Turnstile 验证
- 通过内容长度过滤评论，只保留小说正文
- 支持多页帖子自动翻页
- 文件以帖子标题命名
"""
import sys
import time
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from DrissionPage import ChromiumPage, ChromiumOptions
from bs4 import BeautifulSoup

# Scrapling 开关 - StealthyFetcher 能否绕过 Cloudflare Turnstile 需实测验证
SCRAPLING_ENABLED = False  # 设为 True 启用 StealthyFetcher（实验性）

try:
    from scrapling_fetcher import fetch_page as _scrapling_fetch
    _SCRAPLING_AVAILABLE = True
except ImportError:
    _SCRAPLING_AVAILABLE = False

# ============ 配置区域 - 修改这里 ============
URLS = [
    "https://www.hostboard.com/forums/f1751/THREAD_ID-title.html",
]
OUTPUT_DIR = Path(r"C:\Users\ZDS\Downloads")
MIN_STORY_LENGTH = 1000  # 短于此长度的帖子视为评论
# ============================================


def wait_for_cloudflare(page, timeout=60):
    """Wait for Cloudflare challenge to resolve."""
    for i in range(timeout // 2):
        time.sleep(2)
        title = str(page.title)
        html_len = len(page.html)
        if html_len > 30000 and '请稍候' not in title and 'just a moment' not in title.lower():
            return True
    return False


def extract_story(html):
    """Extract story content from forum HTML, filtering out comments."""
    soup = BeautifulSoup(html, 'html.parser')

    title_el = soup.find('title')
    title = title_el.get_text(strip=True) if title_el else "Unknown"
    title = re.sub(r'^Thread:\s*', '', title)

    post_msgs = soup.find_all(id=re.compile(r'post_message_'))

    story_parts = []
    for msg in post_msgs:
        text = msg.get_text('\n', strip=True)
        if len(text) >= MIN_STORY_LENGTH:
            story_parts.append(text)

    return title, story_parts


def check_pagination(html):
    """Check if thread has multiple pages and return page URLs."""
    soup = BeautifulSoup(html, 'html.parser')
    pages = []
    for a in soup.select('.pagenav a[href*="page="]'):
        href = a.get('href', '')
        if href and href not in pages and 'printthread' not in href:
            pages.append(href)
    return pages


def sanitize_filename(name):
    """Remove invalid filename characters."""
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()


def fetch_with_scrapling(url):
    """使用 StealthyFetcher 获取页面（实验性，需验证能否绕过 Turnstile）"""
    if not (SCRAPLING_ENABLED and _SCRAPLING_AVAILABLE):
        return None
    page = _scrapling_fetch(url, mode="stealth")
    if page is None:
        return None
    return str(page.html)


def main():
    co = ChromiumOptions()
    co.set_argument('--no-sandbox')
    page = ChromiumPage(co)

    for idx, url in enumerate(URLS, 1):
        print(f"\n{'='*60}")
        print(f"[{idx}/{len(URLS)}] Fetching: {url[:80]}...")

        page.get(url)
        if not wait_for_cloudflare(page):
            print(f"  FAILED: Cloudflare challenge did not resolve")
            continue

        html = page.html
        title, story_parts = extract_story(html)
        print(f"  Title: {title}")
        print(f"  Story parts found: {len(story_parts)}")

        if not story_parts:
            print("  WARNING: No story content found!")
            continue

        extra_pages = check_pagination(html)
        if extra_pages:
            print(f"  Found {len(extra_pages)} additional pages")
            for page_url in extra_pages:
                if not page_url.startswith('http'):
                    page_url = 'https://www.hostboard.com/forums/' + page_url
                page.get(page_url)
                if wait_for_cloudflare(page):
                    _, extra_parts = extract_story(page.html)
                    story_parts.extend(extra_parts)
                    print(f"    +{len(extra_parts)} parts from extra page")

        content = f"{title}\n{'='*50}\n\n"
        for i, part in enumerate(story_parts):
            if i > 0:
                content += f"\n\n{'─'*40}\n\n"
            content += part

        filename = sanitize_filename(title) + ".txt"
        filepath = OUTPUT_DIR / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        total_chars = sum(len(p) for p in story_parts)
        print(f"  Saved: {filepath.name} ({total_chars:,} chars)")

    page.quit()
    print(f"\n{'='*60}")
    print("All done!")


if __name__ == "__main__":
    main()
