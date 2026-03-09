#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Syosetu R18 (novel18.syosetu.com) 小说下载器
依赖: pip install requests beautifulsoup4

使用方法:
1. 修改 NOVEL_URL 为目标小说的目录页URL
2. 修改 OUTPUT_FILE 为输出文件名
3. 运行: python -X utf8 syosetu_r18.py
"""
import requests
from bs4 import BeautifulSoup
import time
import sys

try:
    from scrapling_fetcher import fetch_page as _scrapling_fetch
    _SCRAPLING = True
except ImportError:
    _SCRAPLING = False

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ============ 配置区域 - 修改这里 ============
BASE_URL = "https://novel18.syosetu.com"
NOVEL_URL = "https://novel18.syosetu.com/n9104ba/"  # 修改为目标小说URL
OUTPUT_FILE = "syosetu_novel.txt"  # 修改为输出文件名
# ============================================

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'ja,en;q=0.9',
}

def get_chapter_list():
    html = None
    if _SCRAPLING:
        page = _scrapling_fetch(NOVEL_URL, mode="static", cookies={"over18": "yes"})
        if page is not None:
            html = str(page.html_content)
    if html is None:
        session = requests.Session()
        session.headers.update(HEADERS)
        session.cookies.set('over18', 'yes', domain='.syosetu.com')
        resp = session.get(NOVEL_URL)
        resp.encoding = 'utf-8'
        html = resp.text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.select_one('.novel_title, .p-novel__title')
    author = soup.select_one('.novel_writername a, .p-novel__author a')

    chapters = []
    for link in soup.select('.index_box a, .p-eplist__sublist a'):
        href = link.get('href', '')
        if href:
            full_url = BASE_URL + href if href.startswith('/') else href
            chapters.append({'url': full_url, 'title': link.get_text(strip=True)})

    return (
        title.get_text(strip=True) if title else "Unknown",
        author.get_text(strip=True) if author else "Unknown",
        chapters
    )

def get_chapter_content(url):
    html = None
    if _SCRAPLING:
        page = _scrapling_fetch(url, mode="static", cookies={"over18": "yes"})
        if page is not None:
            html = str(page.html_content)
    if html is None:
        session = requests.Session()
        session.headers.update(HEADERS)
        session.cookies.set('over18', 'yes', domain='.syosetu.com')
        resp = session.get(url)
        resp.encoding = 'utf-8'
        html = resp.text
    soup = BeautifulSoup(html, 'html.parser')

    parts = []
    # novel18使用 .p-novel__body，普通syosetu使用 #novel_honbun
    for selector in ['#novel_p', '.p-novel__body', '#novel_honbun', '#novel_a']:
        elem = soup.select_one(selector)
        if elem:
            parts.append(elem.get_text('\n', strip=True))

    return '\n\n'.join(parts)

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
        print(f"[{i}/{len(chapters)}] {ch['title'][:30]}")
        text = get_chapter_content(ch['url'])
        content.extend([f"\n{'=' * 30}", f"第{i}章 {ch['title']}", "=" * 30, text, ""])
        time.sleep(1)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

    print(f"\n完成: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
