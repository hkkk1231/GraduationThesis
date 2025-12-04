#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行入口：基于 Zotero JSON 生成最新文献的 Obsidian 笔记。
"""

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from thesis_tools.obsidian_export import main


if __name__ == "__main__":  # pragma: no cover - 脚本入口
    main()
