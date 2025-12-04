#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行入口：测试 Obsidian 与 Zotero 的同步与目录结构。
"""

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from test_obsidian_zotero_sync import generate_sync_report


def main() -> None:
    generate_sync_report()


if __name__ == "__main__":  # pragma: no cover
    main()
