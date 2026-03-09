#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 论文页面抓取器
处理不提供 API 的出版商页面（Nature/Science/Elsevier 等）
依赖: pip install scrapling requests
"""
import re
import sys
from typing import Optional

try:
    from scrapling.fetchers import Fetcher, DynamicFetcher
    _SCRAPLING = True
except ImportError:
    _SCRAPLING = False

try:
    import requests
    _REQUESTS = True
except ImportError:
    _REQUESTS = False


def _fetch_html(url: str, js_render: bool = False) -> Optional[str]:
    """获取页面 HTML，优先 Scrapling，fallback requests"""
    if _SCRAPLING:
        try:
            if js_render:
                page = DynamicFetcher().fetch(url)
            else:
                page = Fetcher(auto_match=False).get(url)
            return str(page.html_content)
        except Exception:
            pass
    if _REQUESTS:
        try:
            resp = requests.get(url, timeout=30, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; academic-bot/1.0)'
            })
            return resp.text
        except Exception:
            pass
    return None


def fetch_paper_metadata(url: str) -> dict:
    """
    从论文页面提取元数据
    自动选择 fetcher（静态/JS渲染）
    返回: {title, authors, abstract, doi, pdf_url}
    """
    html = _fetch_html(url, js_render=False)
    if not html:
        html = _fetch_html(url, js_render=True)
    if not html:
        return {}

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    result = {}

    # 标题
    for sel in ['h1.c-article-title', 'h1.article-title', 'h1[class*="title"]', 'h1']:
        elem = soup.select_one(sel)
        if elem:
            result['title'] = elem.get_text(strip=True)
            break

    # DOI
    doi_meta = soup.find('meta', attrs={'name': 'citation_doi'}) or \
               soup.find('meta', attrs={'property': 'citation_doi'})
    if doi_meta:
        result['doi'] = doi_meta.get('content', '')

    # PDF URL
    pdf_meta = soup.find('meta', attrs={'name': 'citation_pdf_url'})
    if pdf_meta:
        result['pdf_url'] = pdf_meta.get('content', '')

    # 摘要
    for sel in ['div.c-article-section__content', 'div#abstract', 'section[class*="abstract"]',
                'div[class*="abstract"]']:
        elem = soup.select_one(sel)
        if elem:
            result['abstract'] = elem.get_text(' ', strip=True)[:1000]
            break

    return result


def extract_from_doi_page(doi: str) -> dict:
    """
    通过 DOI 访问出版商页面提取元数据
    支持 Nature/Science/Elsevier 等
    """
    url = f"https://doi.org/{doi}"
    return fetch_paper_metadata(url)


def try_unpaywall(doi: str, email: str = "research@example.com") -> str:
    """
    通过 Unpaywall API 获取开放获取 PDF URL
    返回 PDF URL 或空字符串
    """
    api_url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
    html = _fetch_html(api_url)
    if not html:
        return ""
    try:
        import json
        data = json.loads(html)
        best_oa = data.get('best_oa_location') or {}
        return best_oa.get('url_for_pdf', '') or best_oa.get('url', '')
    except Exception:
        return ""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python html_scraper.py <URL或DOI>")
        sys.exit(1)

    arg = sys.argv[1]
    if arg.startswith('10.'):
        result = extract_from_doi_page(arg)
        pdf = try_unpaywall(arg)
        if pdf:
            result['unpaywall_pdf'] = pdf
    else:
        result = fetch_paper_metadata(arg)

    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))
