#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行入口：从 Zotero 拉取文献并输出分析 JSON。

Phase 1：直接复用 ``thesis_tools.zotero_ingest`` 中的 ``main`` 函数，
后续可根据需要增加参数解析。
"""

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from thesis_tools.zotero_ingest import main


if __name__ == "__main__":  # pragma: no cover - 脚本入口
    main()
