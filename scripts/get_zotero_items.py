#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行入口：从 Zotero 拉取文献并输出分析 JSON。

Phase 1：直接复用 ``thesis_tools.zotero_ingest`` 中的 ``main`` 函数，
后续可根据需要增加参数解析。
"""

from thesis_tools.zotero_ingest import main


if __name__ == "__main__":  # pragma: no cover - 脚本入口
    main()

