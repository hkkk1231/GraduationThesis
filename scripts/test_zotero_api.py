#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行入口：测试 Zotero API 连接。

直接复用 `thesis_tools.sync_checks` 中的检查逻辑，
避免再经过根目录兼容薄包装脚本。
"""

from __future__ import annotations

import os
from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from thesis_tools.sync_checks import run_zotero_api_checks, summarize_results  # type: ignore[import]


def main() -> None:
    api_key = os.environ.get("ZOTERO_API_KEY")
    library_id = os.environ.get("ZOTERO_LIBRARY_ID")
    base_url = os.environ.get("ZOTERO_BASE_URL") or "https://api.zotero.org"

    if not api_key or not library_id:
        print("ZOTERO_API_KEY / ZOTERO_LIBRARY_ID 未设置，无法测试 API 连接。")
        return

    print("=== 测试 Zotero API 连接 ===")
    results = run_zotero_api_checks(
        api_key=api_key,
        library_id=library_id,
        base_url=base_url,
    )
    summarize_results(results)


if __name__ == "__main__":  # pragma: no cover
    main()

