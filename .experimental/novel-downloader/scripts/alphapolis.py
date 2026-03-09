#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alphapolis 小说下载器 (使用Playwright绕过WAF)
依赖: pip install scrapling[all] beautifulsoup4 && scrapling install

使用方法:
1. 修改 NOVEL_URL 为目标小说的目录页URL
2. 修改 OUTPUT_FILE 为输出文件名
3. 运行: python -X utf8 alphapolis.py
"""
from playwright.sync_api import sync_playwright
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
BASE_URL = "https://www.alphapolis.co.jp"
NOVEL_URL = "https://www.alphapolis.co.jp/novel/528033569/74508709"  # 修改为目标小说URL
OUTPUT_FILE = "alphapolis_novel.txt"  # 修改为输出文件名
# ============================================

def get_chapter_list(page):
    """获取章节列表"""
    print("访问小说目录页...")
    page.goto(NOVEL_URL, wait_until='domcontentloaded', timeout=60000)
    time.sleep(3)

    html = page.content()
    soup = BeautifulSoup(html, 'html.parser')

    title_elem = soup.select_one('h2.title, h1.title, .title')
    author_elem = soup.select_one('.author a, .author')

    title = title_elem.get_text(strip=True) if title_elem else "Unknown"
    author = author_elem.get_text(strip=True) if author_elem else "Unknown"

    chapters = []
    seen = set()
    for link in soup.select('a[href*="/episode/"]'):
        href = link.get('href', '')
        if '/episode/' in href and href not in seen:
            seen.add(href)
            ch_title = link.get_text(strip=True)
            if ch_title:
                full_url = href if href.startswith('http') else BASE_URL + href
                chapters.append({'url': full_url, 'title': ch_title})

    return title, author, chapters

def get_chapter_content(page, url):
    """获取单章内容"""
    page.goto(url, wait_until='domcontentloaded', timeout=60000)
    time.sleep(2)

    try:
        page.wait_for_selector('#novelBody', timeout=10000)
        time.sleep(1)
    except:
        pass

    html = page.content()
    soup = BeautifulSoup(html, 'html.parser')

    body = soup.select_one('#novelBody')
    if body:
        for br in body.find_all('br'):
            br.replace_with('\n')
        return body.get_text().strip()
    return ""

def main():
    if _SCRAPLING:
        _main_scrapling()
    else:
        _main_playwright()


def _main_scrapling():
    """使用 Scrapling DynamicFetcher"""
    print("使用 Scrapling 获取章节列表...")
    page_obj = _scrapling_fetch(NOVEL_URL, mode="browser")
    if page_obj is None:
        print("Scrapling 不可用，切换到 Playwright...")
        _main_playwright()
        return

    html = str(page_obj.html)
    soup = BeautifulSoup(html, 'html.parser')

    title_elem = soup.select_one('h2.title, h1.title, .title')
    author_elem = soup.select_one('.author a, .author')
    title = title_elem.get_text(strip=True) if title_elem else "Unknown"
    author = author_elem.get_text(strip=True) if author_elem else "Unknown"

    chapters = []
    seen = set()
    for link in soup.select('a[href*="/episode/"]'):
        href = link.get('href', '')
        if '/episode/' in href and href not in seen:
            seen.add(href)
            ch_title = link.get_text(strip=True)
            if ch_title:
                full_url = href if href.startswith('http') else BASE_URL + href
                chapters.append({'url': full_url, 'title': ch_title})

    print(f"小说: {title}")
    print(f"作者: {author}")
    print(f"章节数: {len(chapters)}")

    if not chapters:
        print("未找到章节")
        return

    content = [f"《{title}》", f"作者: {author}", "=" * 50, ""]

    for i, ch in enumerate(chapters, 1):
        print(f"[{i}/{len(chapters)}] {ch['title'][:30]}")
        ch_page = _scrapling_fetch(ch['url'], mode="browser")
        if ch_page is None:
            text = ""
        else:
            ch_soup = BeautifulSoup(str(ch_page.html_content), 'html.parser')
            body = ch_soup.select_one('#novelBody')
            if body:
                for br in body.find_all('br'):
                    br.replace_with('\n')
                text = body.get_text().strip()
            else:
                text = ""
        content.extend([f"\n{'=' * 30}", f"第{i}章 {ch['title']}", "=" * 30, text, ""])

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

    print(f"\n完成: {OUTPUT_FILE}")


def _main_playwright():
    """原始 Playwright 实现（fallback）"""
    with sync_playwright() as p:
        print("启动浏览器...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()

        title, author, chapters = get_chapter_list(page)

        print(f"小说: {title}")
        print(f"作者: {author}")
        print(f"章节数: {len(chapters)}")

        if not chapters:
            print("未找到章节")
            browser.close()
            return

        content = [f"《{title}》", f"作者: {author}", "=" * 50, ""]

        for i, ch in enumerate(chapters, 1):
            print(f"[{i}/{len(chapters)}] {ch['title'][:30]}")
            text = get_chapter_content(page, ch['url'])
            content.extend([f"\n{'=' * 30}", f"第{i}章 {ch['title']}", "=" * 30, text, ""])

        browser.close()

        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))

        print(f"\n完成: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
