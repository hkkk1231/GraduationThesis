#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行入口：测试 Zotero API 连接。

当前直接复用根目录 ``test_zotero_api.py`` 中的实现，
后续可将检查逻辑抽取到 ``thesis_tools.sync_checks``。
"""

from test_zotero_api import test_api_connection


def main() -> None:
    test_api_connection()


if __name__ == "__main__":  # pragma: no cover
    main()

