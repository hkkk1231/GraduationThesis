#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
兼容入口：保留原 ``python analyze_foreign_literature.py`` 的使用方式。

核心分析逻辑已收敛到 ``thesis_tools.zotero_analysis.analyze_foreign_literature``，
本脚本仅作为薄包装，方便从仓库根目录直接调用。
"""

from thesis_tools.zotero_analysis import analyze_foreign_literature


def main() -> None:
    """命令行入口：执行外文文献分析。"""
    analyze_foreign_literature()


if __name__ == "__main__":  # pragma: no cover - 脚本入口
    main()
