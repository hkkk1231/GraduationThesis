#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Zotero API 连接。

核心检查逻辑已抽取到 ``thesis_tools.sync_checks`` 中，
本脚本作为兼容入口，保持原有命令行用法。
"""

from thesis_tools.sync_checks import run_zotero_api_checks, summarize_results

# Zotero API 配置（保持原有常量以兼容既有调用方式）
API_KEY = "CIApUKos6l9E0GOaCBrILRrt"
LIBRARY_ID = "18982351"
BASE_URL = "https://api.zotero.org"


def test_api_connection() -> None:
    """测试 Zotero API 连接。"""
    results = run_zotero_api_checks(
        api_key=API_KEY,
        library_id=LIBRARY_ID,
        base_url=BASE_URL,
    )
    summarize_results(results)


if __name__ == "__main__":  # pragma: no cover - 脚本入口
    test_api_connection()

