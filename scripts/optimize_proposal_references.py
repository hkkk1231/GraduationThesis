#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行入口：基于 Zotero 数据自动优化开题报告参考文献。

内部复用 `thesis_tools.optimize_proposal_references.main`，
便于从仓库根目录运行：

    python scripts/optimize_proposal_references.py
"""

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from thesis_tools.optimize_proposal_references import main  # type: ignore[import]


if __name__ == "__main__":  # pragma: no cover
    main()

