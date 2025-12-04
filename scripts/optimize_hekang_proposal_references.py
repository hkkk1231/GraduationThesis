#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行入口：为“何康”课题版本的开题报告优化参考文献。

该脚本保留在 scripts/ 目录中，作为特定场景下的 CLI 封装，
内部复用 `thesis_tools.optimize_proposal_references` 中的模型与工具。
"""

from __future__ import annotations

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from thesis_tools.optimize_proposal_references import (  # type: ignore[import]
    ReferenceItem,
    format_reference_text,
    load_chinese_items_from_json,
    load_foreign_items_from_sqlite,
    select_clean_references,
    rewrite_references_in_proposal,
)


def main() -> None:
    """特化版本入口：当前直接委托通用实现。"""
    print("=== 开题报告参考文献自动优化工具（何康版本） ===")
    refs = select_clean_references(target_total=30, min_foreign=4)
    print(f"[INFO] 实际选用参考文献数量: {len(refs)}")
    rewrite_references_in_proposal(refs)


if __name__ == "__main__":  # pragma: no cover
    main()

