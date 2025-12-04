#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行入口：查看最近添加的文献并生成分析结果。
"""

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from thesis_tools.zotero_analysis import main


if __name__ == "__main__":  # pragma: no cover - 脚本入口
    main()
