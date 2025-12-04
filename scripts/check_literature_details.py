#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行入口：检查文献详细信息与可能的外文内容。
"""

from check_literature_details import analyze_all_literature, suggest_next_steps


def main() -> None:
    result = analyze_all_literature()
    if result is not None:
        suggest_next_steps(result)


if __name__ == "__main__":  # pragma: no cover
    main()

