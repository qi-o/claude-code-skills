#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrapling 统一 Fetcher 工厂
供所有下载脚本 import 使用
"""

try:
    from scrapling.fetchers import Fetcher, DynamicFetcher, StealthyFetcher
    SCRAPLING_AVAILABLE = True
except ImportError:
    SCRAPLING_AVAILABLE = False


def fetch_page(url, mode="static", **kwargs):
    """
    统一页面获取接口
    mode: "static" | "browser" | "stealth"
    返回 Scrapling Page 对象，或在不可用时返回 None（调用方 fallback 到 requests/curl）
    """
    if not SCRAPLING_AVAILABLE:
        return None
    try:
        if mode == "browser":
            return DynamicFetcher().fetch(url, **kwargs)
        elif mode == "stealth":
            return StealthyFetcher().fetch(url, **kwargs)
        else:
            return Fetcher().get(url, **kwargs)
    except Exception:
        return None
