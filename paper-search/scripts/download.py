#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学术论文下载工具
支持 arXiv, bioRxiv, medRxiv, IACR
"""
import argparse
import os
import sys

try:
    import requests
except ImportError:
    print("请先安装依赖: pip install requests")
    sys.exit(1)


def download_arxiv(paper_id: str, output_dir: str) -> str:
    """下载 arXiv 论文 PDF"""
    # 清理 paper_id
    paper_id = paper_id.replace('arXiv:', '').replace('arxiv:', '')
    if '/' in paper_id and not paper_id.startswith('http'):
        # 旧格式如 hep-th/9901001
        pass

    pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"arxiv_{paper_id.replace('/', '_')}.pdf")

    print(f"下载中: {pdf_url}")
    response = requests.get(pdf_url, timeout=60)

    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"已保存: {output_file}")
        return output_file
    else:
        print(f"下载失败: HTTP {response.status_code}")
        return ""


def download_biorxiv(doi: str, output_dir: str) -> str:
    """下载 bioRxiv 论文 PDF"""
    # DOI 格式: 10.1101/2023.01.01.123456
    if not doi.startswith('10.1101/'):
        doi = f"10.1101/{doi}"

    pdf_url = f"https://www.biorxiv.org/content/{doi}.full.pdf"

    os.makedirs(output_dir, exist_ok=True)
    safe_name = doi.replace('/', '_').replace('.', '_')
    output_file = os.path.join(output_dir, f"biorxiv_{safe_name}.pdf")

    print(f"下载中: {pdf_url}")
    response = requests.get(pdf_url, timeout=60, allow_redirects=True)

    if response.status_code == 200 and 'application/pdf' in response.headers.get('content-type', ''):
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"已保存: {output_file}")
        return output_file
    else:
        print(f"下载失败: HTTP {response.status_code}")
        return ""


def download_medrxiv(doi: str, output_dir: str) -> str:
    """下载 medRxiv 论文 PDF"""
    if not doi.startswith('10.1101/'):
        doi = f"10.1101/{doi}"

    pdf_url = f"https://www.medrxiv.org/content/{doi}.full.pdf"

    os.makedirs(output_dir, exist_ok=True)
    safe_name = doi.replace('/', '_').replace('.', '_')
    output_file = os.path.join(output_dir, f"medrxiv_{safe_name}.pdf")

    print(f"下载中: {pdf_url}")
    response = requests.get(pdf_url, timeout=60, allow_redirects=True)

    if response.status_code == 200 and 'application/pdf' in response.headers.get('content-type', ''):
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"已保存: {output_file}")
        return output_file
    else:
        print(f"下载失败: HTTP {response.status_code}")
        return ""


def download_iacr(paper_id: str, output_dir: str) -> str:
    """下载 IACR ePrint 论文 PDF"""
    # paper_id 格式: 2023/123 或 2023/1234
    if '/' not in paper_id:
        print("IACR paper_id 格式应为: YYYY/NNNN (如 2023/123)")
        return ""

    pdf_url = f"https://eprint.iacr.org/{paper_id}.pdf"

    os.makedirs(output_dir, exist_ok=True)
    safe_name = paper_id.replace('/', '_')
    output_file = os.path.join(output_dir, f"iacr_{safe_name}.pdf")

    print(f"下载中: {pdf_url}")
    response = requests.get(pdf_url, timeout=60)

    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"已保存: {output_file}")
        return output_file
    else:
        print(f"下载失败: HTTP {response.status_code}")
        return ""


def download_semantic(paper_id: str, output_dir: str) -> str:
    """下载 Semantic Scholar 论文 PDF（如果有开放获取版本）"""
    api_url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
    params = {'fields': 'openAccessPdf,title'}

    response = requests.get(api_url, params=params, timeout=30)
    if response.status_code != 200:
        print(f"获取论文信息失败: HTTP {response.status_code}")
        return ""

    data = response.json()
    pdf_info = data.get('openAccessPdf')

    if not pdf_info or not pdf_info.get('url'):
        print("该论文没有开放获取的 PDF")
        return ""

    pdf_url = pdf_info['url']
    title = data.get('title', paper_id)[:50]  # 截断标题

    os.makedirs(output_dir, exist_ok=True)
    safe_name = "".join(c if c.isalnum() or c in ' -_' else '_' for c in title)
    output_file = os.path.join(output_dir, f"semantic_{safe_name}.pdf")

    print(f"下载中: {pdf_url}")
    response = requests.get(pdf_url, timeout=60, allow_redirects=True)

    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"已保存: {output_file}")
        return output_file
    else:
        print(f"下载失败: HTTP {response.status_code}")
        return ""


DOWNLOADERS = {
    'arxiv': download_arxiv,
    'biorxiv': download_biorxiv,
    'medrxiv': download_medrxiv,
    'iacr': download_iacr,
    'semantic': download_semantic,
}


def main():
    parser = argparse.ArgumentParser(description='学术论文下载工具')
    parser.add_argument('source', choices=list(DOWNLOADERS.keys()),
                        help='数据源: arxiv, biorxiv, medrxiv, iacr, semantic')
    parser.add_argument('paper_id', help='论文 ID (arXiv ID, DOI, IACR ID 等)')
    parser.add_argument('--output', '-o', default='./downloads', help='输出目录 (默认: ./downloads)')

    args = parser.parse_args()

    downloader = DOWNLOADERS[args.source]
    result = downloader(args.paper_id, args.output)

    if result:
        print(f"\n下载成功: {result}")
    else:
        print("\n下载失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
