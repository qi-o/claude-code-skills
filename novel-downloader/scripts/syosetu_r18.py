#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Syosetu R18 (novel18.syosetu.com) 小说下载器
依赖: 无需 pip，调用系统 curl 绕过代理

使用方法:
1. 修改 NOVEL_URL 为目标小说的目录页URL
2. 修改 OUTPUT_FILE 为输出文件名
3. 运行: python -X utf8 syosetu_r18.py
"""
import subprocess
import re
import time
import sys
import os

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ============ 配置区域 - 修改这里 ============
BASE_URL = "https://novel18.syosetu.com"
NOVEL_URL = "https://novel18.syosetu.com/n9104ba/"  # 修改为目标小说URL
OUTPUT_FILE = "syosetu_novel.txt"  # 修改为输出文件名
# ============================================

def curl_get(url):
    """使用 curl 绕过系统代理直连访问"""
    result = subprocess.run(
        ['curl.exe', '-x', '', '-k', '--tlsv1.2', '-s', '-L',
         '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
         '-b', 'over18=yes', url],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    return result.stdout

def get_chapter_list():
    html = curl_get(NOVEL_URL)
    title_m = re.search(r'<title>([^<]+)</title>', html)
    title = title_m.group(1) if title_m else "Unknown"

    author_m = re.search(r'class="novel_writername"[^>]*>[^<]*<a[^>]*>([^<]+)</a>', html)
    author = author_m.group(1) if author_m else "Unknown"

    # 提取章节链接
    import urllib.parse
    novel_id = re.search(r'novel18\.syosetu\.com/(n[a-z0-9]+)', NOVEL_URL).group(1)
    links = re.findall(rf'href="(/{novel_id}/\d+/)"', html)
    chapters = []
    for href in links:
        full_url = BASE_URL + href if href.startswith('/') else href
        # 尝试从 HTML 中提取标题
        title_m = re.search(rf'href="{re.escape(href)}"[^>]*>\s*([^<]+)', html)
        ch_title = title_m.group(1).strip() if title_m else f"第{len(chapters)+1}章"
        chapters.append({'url': full_url, 'title': ch_title})

    return title, author, chapters

def get_chapter_content(url):
    html = curl_get(url)
    # 尝试多个选择器
    for sel_pat in [r'id="novel_honbun"[^>]*>(.*?)</div>', r'class="p-novel__body"[^>]*>(.*?)</div>',
                    r'id="novel_p"[^>]*>(.*?)</div>', r'id="novel_a"[^>]*>(.*?)</div>']:
        m = re.search(sel_pat, html, re.DOTALL)
        if m:
            text = re.sub(r'<[^>]+>', '', m.group(1))
            text = re.sub(r'\n+', '\n', text).strip()
            return text
    return re.sub(r'<[^>]+>', '', html)[:500]

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
