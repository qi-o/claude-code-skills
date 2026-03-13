#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨平台编码处理工具
解决 Windows GBK 环境下的 Unicode 输出问题
"""

import sys
import io
import os


def setup_utf8_output():
    """
    配置 stdout/stderr 使用 UTF-8 编码

    适用于 Python 3.6+，在 Windows GBK 环境下确保 Unicode 字符正常输出
    """
    # 检查当前编码
    current_encoding = getattr(sys.stdout, 'encoding', None) or 'ascii'

    if current_encoding.lower() not in ('utf-8', 'utf8'):
        try:
            # Python 3.7+ 支持 reconfigure()
            if hasattr(sys.stdout, 'reconfigure'):
                sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
                sys.stderr.reconfigure(encoding='utf-8', errors='backslashreplace')
            else:
                # Python 3.6 fallback: 包装现有流
                sys.stdout = io.TextIOWrapper(
                    sys.stdout.buffer,
                    encoding='utf-8',
                    errors='backslashreplace',
                    line_buffering=True
                )
                sys.stderr = io.TextIOWrapper(
                    sys.stderr.buffer,
                    encoding='utf-8',
                    errors='backslashreplace',
                    line_buffering=True
                )
        except (AttributeError, io.UnsupportedOperation):
            # 某些环境下可能失败（如 IDLE），静默处理
            pass


def supports_emoji():
    """
    检测终端是否支持 emoji

    Returns:
        bool: True 如果支持 emoji，False 否则
    """
    # 检查编码
    encoding = getattr(sys.stdout, 'encoding', None) or 'ascii'
    if encoding.lower() not in ('utf-8', 'utf8'):
        return False

    # 检查是否是 TTY
    if not sys.stdout.isatty():
        return False

    # Windows 特殊检查
    if sys.platform == 'win32':
        # Windows Terminal, VS Code 终端支持
        if os.environ.get('WT_SESSION') or os.environ.get('TERM_PROGRAM') == 'vscode':
            return True
        # Git Bash 通常支持
        if os.environ.get('TERM'):
            return True
        # 传统 cmd.exe 可能不支持
        return False

    return True


class SafeOutput:
    """
    安全的输出类，自动处理 emoji 降级
    """

    def __init__(self):
        self.use_emoji = supports_emoji()

        # 定义符号集
        if self.use_emoji:
            self.symbols = {
                'rocket': '🚀',
                'check': '✓',
                'cross': '✗',
                'warning': '⚠',
                'info': 'ℹ',
                'folder': '📁',
                'file': '📄',
                'package': '📦',
            }
        else:
            self.symbols = {
                'rocket': '[*]',
                'check': '[OK]',
                'cross': '[X]',
                'warning': '[!]',
                'info': '[i]',
                'folder': '[DIR]',
                'file': '[FILE]',
                'package': '[PKG]',
            }

    def get_symbol(self, name):
        """获取符号"""
        return self.symbols.get(name, '')

    def print(self, message, symbol=None):
        """打印消息，可选符号前缀"""
        if symbol:
            icon = self.get_symbol(symbol)
            print(f'{icon} {message}')
        else:
            print(message)
