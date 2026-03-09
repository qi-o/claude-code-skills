#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purple Novel (purple-novel.com) 小说下载器 - WordPress站点
依赖: pip install requests beautifulsoup4

使用方法:
1. 修改 NOVEL_URL 为目标小说的第一页URL
2. 修改 NOVEL_SLUG 为URL中的小说标识 (如 ikaseai)
3. 修改 OUTPUT_FILE 为输出文件名
4. 运行: python -X utf8 purple_novel.py
"""
import requests
from bs4 import BeautifulSoup
import time
import sys
import re

try:
    from scrapling_fetcher import fetch_page as _scrapling_fetch
    _SCRAPLING = True
except ImportError:
    _SCRAPLING = False

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ============ 配置区域 - 修改这里 ============
BASE_URL = "https://purple-novel.com"
NOVEL_SLUG = "ikaseai"  # URL中的小说标识
NOVEL_URL = f"{BASE_URL}/{NOVEL_SLUG}/"
OUTPUT_FILE = "purple_novel.txt"  # 修改为输出文件名
# ============================================

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

def get_chapter_list():
    """Purple Novel是分页形式，每页就是一章"""
    html = None
    if _SCRAPLING:
        page = _scrapling_fetch(NOVEL_URL, mode="static")
        if page is not None:
            html = str(page.html_content)
    if html is None:
        resp = requests.get(NOVEL_URL, headers=HEADERS)
        resp.encoding = 'utf-8'
        html = resp.text
    soup = BeautifulSoup(html, 'html.parser')

    title_elem = soup.select_one('h1.entry-title, h1')
    title = title_elem.get_text(strip=True) if title_elem else "Unknown"

    # 尝试从页面提取作者
    author = "Unknown"

    chapters = [{'url': NOVEL_URL, 'title': '第1話'}]

    # 查找分页确定总页数
    page_links = soup.select(f'a[href*="/{NOVEL_SLUG}/"]')
    max_page = 1
    for link in page_links:
        href = link.get('href', '')
        match = re.search(rf'/{NOVEL_SLUG}/(\d+)/', href)
        if match:
            page_num = int(match.group(1))
            if page_num > max_page:
                max_page = page_num

    for i in range(2, max_page + 1):
        chapters.append({
            'url': f"{BASE_URL}/{NOVEL_SLUG}/{i}/",
            'title': f'第{i}話'
        })

    return title, author, chapters

def get_chapter_content(url):
    html = None
    if _SCRAPLING:
        page = _scrapling_fetch(url, mode="static")
        if page is not None:
            html = str(page.html_content)
    if html is None:
        resp = requests.get(url, headers=HEADERS)
        resp.encoding = 'utf-8'
        html = resp.text
    soup = BeautifulSoup(html, 'html.parser')

    content_elem = soup.select_one('article')
    if content_elem:
        for unwanted in content_elem.select('script, style, .sharedaddy, .jp-relatedposts, nav, .post-navigation'):
            unwanted.decompose()
        return content_elem.get_text('\n', strip=True)
    return ""

def main():
    print("获取章节列表...")
    title, author, chapters = get_chapter_list()

    print(f"小说: {title}")
    print(f"作者: {author}")
    print(f"章节数: {len(chapters)}")

    if not chapters:
        print("未找到章节")
        return

    content = [f"《{title}》", f"作者: {author}", "=" * 50, ""]

    for i, ch in enumerate(chapters, 1):
        print(f"[{i}/{len(chapters)}] {ch['title']}")
        text = get_chapter_content(ch['url'])
        content.extend([f"\n{'=' * 30}", f"{ch['title']}", "=" * 30, text, ""])
        time.sleep(1)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

    print(f"\n完成: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
