#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行入口：创建示例文献笔记和工作流测试文档。

Phase 1：通过 ``thesis_tools.obsidian_export.create_sample_notes`` 复用统一
的笔记生成逻辑。
"""

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from thesis_tools.obsidian_export import create_sample_notes


def main() -> None:
    create_sample_notes()


if __name__ == "__main__":  # pragma: no cover
    main()
