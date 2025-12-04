#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行入口：批量生成文献笔记。

Phase 1：通过 ``thesis_tools.obsidian_export.batch_create_notes`` 复用统一
的笔记生成逻辑，原根目录脚本仅作为兼容入口存在。
"""

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from thesis_tools.obsidian_export import batch_create_notes


def main() -> None:
    batch_create_notes()


if __name__ == "__main__":  # pragma: no cover
    main()
