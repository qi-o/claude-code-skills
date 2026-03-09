#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrapling 增强版网页抓取工具
与 ducksearch fetch 接口对齐，支持 JS 渲染和反爬保护

用法:
  python scrapling_fetch.py <URL> [--mode static|browser|stealth|auto] [--json] [-o output.txt]

auto 模式逻辑:
  1. 先用 Fetcher 尝试
  2. 内容 < 500 字符或含 JS 挑战标志 → 升级 DynamicFetcher
  3. 返回 403/429 → 升级 StealthyFetcher
"""
import argparse
import json
import sys

try:
    from scrapling.fetchers import Fetcher, DynamicFetcher, StealthyFetcher
    SCRAPLING_AVAILABLE = True
except ImportError:
    SCRAPLING_AVAILABLE = False
    print("错误: 需要安装 scrapling: pip install scrapling", file=sys.stderr)
    print("JS 渲染还需要: scrapling install (或 playwright install chromium)", file=sys.stderr)

# JS 挑战特征标志
_JS_CHALLENGE_MARKERS = [
    'just a moment', 'checking your browser', 'please wait',
    'enable javascript', 'cf-browser-verification', 'ray id',
    '__cf_chl', 'turnstile',
]


def _has_js_challenge(text: str) -> bool:
    lower = text.lower()
    return any(marker in lower for marker in _JS_CHALLENGE_MARKERS)


def fetch_static(url: str):
    return Fetcher(auto_match=False).get(url)


def fetch_browser(url: str):
    return DynamicFetcher().fetch(url)


def fetch_stealth(url: str):
    return StealthyFetcher().fetch(url)


def fetch_auto(url: str):
    """
    自动升级策略:
    1. 静态 Fetcher
    2. 内容不足或含 JS 挑战 → DynamicFetcher
    3. 403/429 → StealthyFetcher
    """
    try:
        page = fetch_static(url)
        status = getattr(page, 'status', 200)
        text = str(page.html_content) if hasattr(page, 'html_content') else ''

        if status in (403, 429):
            print(f"[auto] 静态获取返回 {status}，升级到 StealthyFetcher...", file=sys.stderr)
            return fetch_stealth(url)

        if len(text) < 500 or _has_js_challenge(text):
            print("[auto] 内容不足或检测到 JS 挑战，升级到 DynamicFetcher...", file=sys.stderr)
            return fetch_browser(url)

        return page
    except Exception as e:
        print(f"[auto] 静态获取失败 ({e})，升级到 DynamicFetcher...", file=sys.stderr)
        return fetch_browser(url)


def extract_text(page) -> str:
    """从 Scrapling Page 提取纯文本"""
    html = str(page.html_content) if hasattr(page, 'html_content') else ''
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        return soup.get_text('\n', strip=True)
    except ImportError:
        import re
        return re.sub(r'<[^>]+>', ' ', html).strip()


def extract_links(page) -> list:
    """提取页面所有链接"""
    html = str(page.html_content) if hasattr(page, 'html_content') else ''
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('http'):
                links.append({'text': a.get_text(strip=True), 'url': href})
        return links
    except ImportError:
        return []


def get_title(page) -> str:
    html = str(page.html_content) if hasattr(page, 'html_content') else ''
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title')
        return title.get_text(strip=True) if title else ''
    except ImportError:
        import re
        m = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        return m.group(1).strip() if m else ''


def main():
    parser = argparse.ArgumentParser(description='Scrapling 增强版网页抓取工具')
    parser.add_argument('url', help='目标 URL')
    parser.add_argument('--mode', choices=['static', 'browser', 'stealth', 'auto'],
                        default='auto', help='抓取模式 (默认: auto)')
    parser.add_argument('--json', action='store_true', dest='output_json',
                        help='输出 JSON 格式 {url, title, text, links[], status}')
    parser.add_argument('-o', '--output', help='输出文件路径（默认: stdout）')

    args = parser.parse_args()

    if not SCRAPLING_AVAILABLE:
        sys.exit(1)

    try:
        if args.mode == 'static':
            page = fetch_static(args.url)
        elif args.mode == 'browser':
            page = fetch_browser(args.url)
        elif args.mode == 'stealth':
            page = fetch_stealth(args.url)
        else:
            page = fetch_auto(args.url)
    except Exception as e:
        print(f"抓取失败: {e}", file=sys.stderr)
        sys.exit(1)

    status = getattr(page, 'status', 200)
    title = get_title(page)
    text = extract_text(page)

    if args.output_json:
        links = extract_links(page)
        result = {
            'url': args.url,
            'title': title,
            'text': text,
            'links': links[:50],  # 限制链接数量
            'status': status,
        }
        output = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        output = text

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"已保存到: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()

