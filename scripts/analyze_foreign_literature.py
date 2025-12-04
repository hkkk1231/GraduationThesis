#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行入口：分析 Zotero 库中的外文文献。

Phase 1：通过 ``thesis_tools.zotero_analysis`` 复用统一的分析逻辑，
避免与根目录脚本重复实现。
"""

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from thesis_tools.zotero_analysis import analyze_foreign_literature


def main() -> None:
    analyze_foreign_literature()


if __name__ == "__main__":  # pragma: no cover
    main()
