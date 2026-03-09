#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学术论文搜索工具
支持 arXiv, PubMed, bioRxiv, medRxiv, Google Scholar, Semantic Scholar, CrossRef, IACR
"""
import argparse
import json
import sys

# Windows GBK 编码修复：强制 stdout/stderr 使用 UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ('utf-8', 'utf8'):
    sys.stderr.reconfigure(encoding='utf-8')

from datetime import datetime
from typing import List, Dict, Optional

try:
    import requests
    import feedparser
except ImportError:
    print("请先安装依赖: pip install requests feedparser")
    sys.exit(1)

try:
    from scrapling.fetchers import DynamicFetcher as _PWFetcher
    _SCHOLAR_SCRAPLING = True
except ImportError:
    _SCHOLAR_SCRAPLING = False


class Paper:
    """论文数据类"""
    def __init__(self, paper_id: str, title: str, authors: List[str], abstract: str,
                 url: str, pdf_url: str = "", published_date: datetime = None,
                 source: str = "", categories: List[str] = None, doi: str = ""):
        self.paper_id = paper_id
        self.title = title
        self.authors = authors
        self.abstract = abstract
        self.url = url
        self.pdf_url = pdf_url
        self.published_date = published_date
        self.source = source
        self.categories = categories or []
        self.doi = doi

    def to_dict(self) -> Dict:
        return {
            "paper_id": self.paper_id,
            "title": self.title,
            "authors": self.authors,
            "abstract": self.abstract[:500] + "..." if len(self.abstract) > 500 else self.abstract,
            "url": self.url,
            "pdf_url": self.pdf_url,
            "published_date": self.published_date.strftime("%Y-%m-%d") if self.published_date else "",
            "source": self.source,
            "categories": self.categories,
            "doi": self.doi
        }


class ArxivSearcher:
    """arXiv 搜索器"""
    BASE_URL = "http://export.arxiv.org/api/query"

    def search(self, query: str, max_results: int = 10) -> List[Paper]:
        params = {
            'search_query': f'all:{query}',
            'max_results': max_results,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        response = requests.get(self.BASE_URL, params=params, timeout=30)
        feed = feedparser.parse(response.content)
        papers = []
        for entry in feed.entries:
            try:
                authors = [author.name for author in entry.authors]
                published = datetime.strptime(entry.published, '%Y-%m-%dT%H:%M:%SZ')
                pdf_url = next((link.href for link in entry.links if link.type == 'application/pdf'), '')
                papers.append(Paper(
                    paper_id=entry.id.split('/')[-1],
                    title=entry.title.replace('\n', ' '),
                    authors=authors,
                    abstract=entry.summary.replace('\n', ' '),
                    url=entry.id,
                    pdf_url=pdf_url,
                    published_date=published,
                    source='arxiv',
                    categories=[tag.term for tag in entry.tags],
                    doi=entry.get('arxiv_doi', '')
                ))
            except Exception as e:
                print(f"解析 arXiv 条目出错: {e}", file=sys.stderr)
        return papers


class PubMedSearcher:
    """PubMed 搜索器"""
    SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    def search(self, query: str, max_results: int = 10) -> List[Paper]:
        # 搜索获取 ID 列表
        search_params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'retmode': 'json',
            'sort': 'date'
        }
        search_resp = requests.get(self.SEARCH_URL, params=search_params, timeout=30)
        search_data = search_resp.json()

        id_list = search_data.get('esearchresult', {}).get('idlist', [])
        if not id_list:
            return []

        # 获取详细信息
        fetch_params = {
            'db': 'pubmed',
            'id': ','.join(id_list),
            'retmode': 'xml'
        }
        fetch_resp = requests.get(self.FETCH_URL, params=fetch_params, timeout=30)

        # 简单解析 XML
        papers = []
        from xml.etree import ElementTree as ET
        try:
            root = ET.fromstring(fetch_resp.content)
            for article in root.findall('.//PubmedArticle'):
                try:
                    pmid = article.find('.//PMID').text
                    title_elem = article.find('.//ArticleTitle')
                    title = title_elem.text if title_elem is not None else "No title"

                    authors = []
                    for author in article.findall('.//Author'):
                        lastname = author.find('LastName')
                        forename = author.find('ForeName')
                        if lastname is not None:
                            name = lastname.text
                            if forename is not None:
                                name = f"{forename.text} {name}"
                            authors.append(name)

                    abstract_elem = article.find('.//AbstractText')
                    abstract = abstract_elem.text if abstract_elem is not None else ""

                    # 获取发布日期
                    pub_date = None
                    date_elem = article.find('.//PubDate')
                    if date_elem is not None:
                        year = date_elem.find('Year')
                        month = date_elem.find('Month')
                        if year is not None:
                            try:
                                month_num = int(month.text) if month is not None and month.text.isdigit() else 1
                                pub_date = datetime(int(year.text), month_num, 1)
                            except:
                                pass

                    papers.append(Paper(
                        paper_id=pmid,
                        title=title,
                        authors=authors,
                        abstract=abstract or "",
                        url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                        source='pubmed',
                        published_date=pub_date
                    ))
                except Exception as e:
                    print(f"解析 PubMed 条目出错: {e}", file=sys.stderr)
        except ET.ParseError as e:
            print(f"解析 PubMed XML 出错: {e}", file=sys.stderr)

        return papers


class BioRxivSearcher:
    """bioRxiv 搜索器"""
    BASE_URL = "https://api.biorxiv.org/details/biorxiv"

    def search(self, query: str, max_results: int = 10) -> List[Paper]:
        # bioRxiv API 按日期范围搜索
        from datetime import timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)

        url = f"{self.BASE_URL}/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}/0/100"
        response = requests.get(url, timeout=30)
        data = response.json()

        papers = []
        query_lower = query.lower()
        for item in data.get('collection', []):
            # 简单关键词匹配
            if query_lower in item.get('title', '').lower() or query_lower in item.get('abstract', '').lower():
                try:
                    pub_date = datetime.strptime(item['date'], '%Y-%m-%d')
                    papers.append(Paper(
                        paper_id=item.get('doi', ''),
                        title=item.get('title', ''),
                        authors=item.get('authors', '').split('; '),
                        abstract=item.get('abstract', ''),
                        url=f"https://www.biorxiv.org/content/{item.get('doi', '')}",
                        pdf_url=f"https://www.biorxiv.org/content/{item.get('doi', '')}.full.pdf",
                        published_date=pub_date,
                        source='biorxiv',
                        doi=item.get('doi', '')
                    ))
                    if len(papers) >= max_results:
                        break
                except Exception as e:
                    print(f"解析 bioRxiv 条目出错: {e}", file=sys.stderr)

        return papers


class SemanticScholarSearcher:
    """Semantic Scholar 搜索器"""
    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

    def search(self, query: str, max_results: int = 10) -> List[Paper]:
        import os
        headers = {}
        api_key = os.environ.get('SEMANTIC_SCHOLAR_API_KEY')
        if api_key:
            headers['x-api-key'] = api_key

        params = {
            'query': query,
            'limit': max_results,
            'fields': 'paperId,title,authors,abstract,url,openAccessPdf,publicationDate,externalIds'
        }

        response = requests.get(self.BASE_URL, params=params, headers=headers, timeout=30)
        data = response.json()

        papers = []
        for item in data.get('data', []):
            try:
                authors = [a.get('name', '') for a in item.get('authors', [])]
                pub_date = None
                if item.get('publicationDate'):
                    try:
                        pub_date = datetime.strptime(item['publicationDate'], '%Y-%m-%d')
                    except:
                        pass

                pdf_url = ""
                if item.get('openAccessPdf'):
                    pdf_url = item['openAccessPdf'].get('url', '')

                external_ids = item.get('externalIds', {})
                doi = external_ids.get('DOI', '')

                papers.append(Paper(
                    paper_id=item.get('paperId', ''),
                    title=item.get('title', ''),
                    authors=authors,
                    abstract=item.get('abstract', '') or '',
                    url=item.get('url', ''),
                    pdf_url=pdf_url,
                    published_date=pub_date,
                    source='semantic_scholar',
                    doi=doi
                ))
            except Exception as e:
                print(f"解析 Semantic Scholar 条目出错: {e}", file=sys.stderr)

        return papers


class CrossRefSearcher:
    """CrossRef 搜索器"""
    BASE_URL = "https://api.crossref.org/works"

    def search(self, query: str, max_results: int = 10) -> List[Paper]:
        params = {
            'query': query,
            'rows': max_results,
            'sort': 'relevance'
        }

        response = requests.get(self.BASE_URL, params=params, timeout=30)
        data = response.json()

        papers = []
        for item in data.get('message', {}).get('items', []):
            try:
                authors = []
                for author in item.get('author', []):
                    name = f"{author.get('given', '')} {author.get('family', '')}".strip()
                    if name:
                        authors.append(name)

                pub_date = None
                date_parts = item.get('published', {}).get('date-parts', [[]])
                if date_parts and date_parts[0]:
                    parts = date_parts[0]
                    try:
                        year = parts[0] if len(parts) > 0 else 2000
                        month = parts[1] if len(parts) > 1 else 1
                        day = parts[2] if len(parts) > 2 else 1
                        pub_date = datetime(year, month, day)
                    except:
                        pass

                title = item.get('title', [''])[0] if item.get('title') else ''
                abstract = item.get('abstract', '')

                papers.append(Paper(
                    paper_id=item.get('DOI', ''),
                    title=title,
                    authors=authors,
                    abstract=abstract,
                    url=item.get('URL', ''),
                    published_date=pub_date,
                    source='crossref',
                    doi=item.get('DOI', '')
                ))
            except Exception as e:
                print(f"解析 CrossRef 条目出错: {e}", file=sys.stderr)

        return papers

    def get_by_doi(self, doi: str) -> Optional[Paper]:
        """通过 DOI 获取论文信息"""
        url = f"{self.BASE_URL}/{doi}"
        response = requests.get(url, timeout=30)
        if response.status_code != 200:
            return None

        item = response.json().get('message', {})
        try:
            authors = []
            for author in item.get('author', []):
                name = f"{author.get('given', '')} {author.get('family', '')}".strip()
                if name:
                    authors.append(name)

            title = item.get('title', [''])[0] if item.get('title') else ''

            return Paper(
                paper_id=doi,
                title=title,
                authors=authors,
                abstract=item.get('abstract', ''),
                url=item.get('URL', ''),
                source='crossref',
                doi=doi
            )
        except:
            return None


class GoogleScholarScraper:
    """Google Scholar 搜索器（使用 Scrapling DynamicFetcher）"""

    def search(self, query: str, max_results: int = 10) -> List[Paper]:
        if not _SCHOLAR_SCRAPLING:
            print("Google Scholar 搜索需要 scrapling: pip install scrapling[all] && scrapling install",
                  file=sys.stderr)
            return []
        try:
            import urllib.parse
            encoded = urllib.parse.quote(query)
            url = f"https://scholar.google.com/scholar?q={encoded}&num={min(max_results, 20)}"
            page = _PWFetcher().fetch(url)
            html = str(page.html)
        except Exception as e:
            print(f"Google Scholar 抓取失败: {e}", file=sys.stderr)
            return []

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        papers = []

        for result in soup.select('.gs_r.gs_or.gs_scl')[:max_results]:
            try:
                title_elem = result.select_one('.gs_rt a')
                if not title_elem:
                    continue
                title = title_elem.get_text(strip=True)
                url_link = title_elem.get('href', '')

                authors_elem = result.select_one('.gs_a')
                authors_text = authors_elem.get_text(strip=True) if authors_elem else ''
                authors = [a.strip() for a in authors_text.split('-')[0].split(',')]

                abstract_elem = result.select_one('.gs_rs')
                abstract = abstract_elem.get_text(strip=True) if abstract_elem else ''

                pdf_elem = result.select_one('.gs_or_ggsm a')
                pdf_url = pdf_elem.get('href', '') if pdf_elem else ''

                papers.append(Paper(
                    paper_id=url_link,
                    title=title,
                    authors=authors,
                    abstract=abstract,
                    url=url_link,
                    pdf_url=pdf_url,
                    source='google_scholar'
                ))
            except Exception as e:
                print(f"解析 Google Scholar 条目出错: {e}", file=sys.stderr)

        return papers


# 搜索器映射
SEARCHERS = {
    'arxiv': ArxivSearcher(),
    'pubmed': PubMedSearcher(),
    'biorxiv': BioRxivSearcher(),
    'semantic': SemanticScholarSearcher(),
    'crossref': CrossRefSearcher(),
    'scholar': GoogleScholarScraper(),
}


def main():
    parser = argparse.ArgumentParser(description='学术论文搜索工具')
    parser.add_argument('source', choices=list(SEARCHERS.keys()) + ['doi'],
                        help='数据源: arxiv, pubmed, biorxiv, semantic, crossref, doi')
    parser.add_argument('query', help='搜索关键词或 DOI')
    parser.add_argument('--max', type=int, default=10, help='最大结果数 (默认: 10)')
    parser.add_argument('--format', choices=['json', 'text'], default='json', help='输出格式')

    args = parser.parse_args()

    if args.source == 'doi':
        # 通过 DOI 查询
        paper = CrossRefSearcher().get_by_doi(args.query)
        if paper:
            papers = [paper]
        else:
            papers = []
    else:
        searcher = SEARCHERS[args.source]
        papers = searcher.search(args.query, args.max)

    if args.format == 'json':
        result = [p.to_dict() for p in papers]
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for i, p in enumerate(papers, 1):
            print(f"\n[{i}] {p.title}")
            print(f"    作者: {', '.join(p.authors[:3])}{'...' if len(p.authors) > 3 else ''}")
            print(f"    来源: {p.source} | 日期: {p.published_date.strftime('%Y-%m-%d') if p.published_date else 'N/A'}")
            print(f"    链接: {p.url}")
            if p.doi:
                print(f"    DOI: {p.doi}")


if __name__ == "__main__":
    main()
