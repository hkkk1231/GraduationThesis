#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行入口：初始化 Obsidian + Zotero 集成环境。

核心实现位于 `thesis_tools.setup_obsidian_zotero` 模块。
"""

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from thesis_tools.setup_obsidian_zotero import main  # type: ignore[import]


if __name__ == "__main__":  # pragma: no cover
    main()

