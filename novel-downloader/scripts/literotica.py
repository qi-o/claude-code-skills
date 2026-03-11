#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Literotica 小说下载器
使用curl绕过HTTP/2限制，支持分页章节
"""
import subprocess
import re
from bs4 import BeautifulSoup
import time
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_URL = "https://www.literotica.com"
# 修改这两个变量
SERIES_URL = "https://www.literotica.com/series/se/YOUR-SERIES-SLUG"
OUTPUT_FILE = "output.txt"

def fetch_url(url):
    """使用curl获取页面"""
    result = subprocess.run([
        'curl', '-s', '-L',
        '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        '-H', 'Accept: text/html,application/xhtml+xml',
        '-H', 'Accept-Language: en-US,en;q=0.9',
        url
    ], capture_output=True, text=True, timeout=60)
    return result.stdout

def get_chapter_list():
    """获取章节列表"""
    html = fetch_url(SERIES_URL)

    # 从URL提取slug
    slug_match = re.search(r'/series/se/([^/]+)', SERIES_URL)
    if not slug_match:
        print("无法从URL提取slug")
        return None, None, []

    slug = slug_match.group(1)

    # 从页面提取章节链接
    chapters = []
    pattern = rf'/s/{slug}-ch-(\d+)'
    matches = re.findall(pattern, html)

    seen = set()
    for num in matches:
        if num not in seen:
            seen.add(num)
            chapters.append({
                'url': f"{BASE_URL}/s/{slug}-ch-{num}",
                'title': f"Chapter {int(num)}"
            })

    chapters.sort(key=lambda x: int(re.search(r'ch-(\d+)', x['url']).group(1)))

    # 提取标题和作者
    soup = BeautifulSoup(html, 'html.parser')
    title = slug.replace('-', ' ').title()
    author = "Unknown"
    author_link = soup.select_one('a[href*="/authors/"]')
    if author_link:
        author = author_link.get_text(strip=True)

    return title, author, chapters

def get_chapter_content(url):
    """获取单章内容（处理分页）"""
    all_text = []
    current_page = 1

    while True:
        page_url = url if current_page == 1 else f"{url}?page={current_page}"

        html = fetch_url(page_url)
        soup = BeautifulSoup(html, 'html.parser')

        # 查找正文内容 - 使用class包含_article__content的div
        content_div = soup.select_one('div[class*="_article__content"]')

        if content_div:
            paragraphs = content_div.find_all('p')
            if paragraphs:
                text = '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            else:
                text = content_div.get_text('\n', strip=True)

            if text and len(text) > 50:
                all_text.append(text)

        # 检查是否有下一页
        next_page_link = soup.select_one(f'a[href*="?page={current_page + 1}"]')
        if next_page_link:
            current_page += 1
            time.sleep(0.5)
        else:
            break

    return '\n\n'.join(all_text)

def main():
    print("获取章节列表...")
    title, author, chapters = get_chapter_list()

    print(f"小说: {title}")
    print(f"作者: {author}")
    print(f"章节数: {len(chapters)}")

    if not chapters:
        print("未找到章节")
        return

    content = [f"《{title}》", f"Author: {author}", "=" * 50, ""]

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
