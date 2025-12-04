#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行入口：检查文献详细信息与潜在外文内容。

核心逻辑位于 `thesis_tools.check_literature_details` 模块。
"""

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from thesis_tools.check_literature_details import (  # type: ignore[import]
    analyze_all_literature,
    suggest_next_steps,
)


def main() -> None:
    result = analyze_all_literature()
    if result is not None:
        suggest_next_steps(result)


if __name__ == "__main__":  # pragma: no cover
    main()

