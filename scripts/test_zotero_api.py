#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
命令行入口：测试 Zotero API 连接。

当前通过根目录 ``test_zotero_api.py`` 复用 `thesis_tools.sync_checks` 中的检查逻辑，
本脚本在第一阶段仅作为薄入口，保持命令行调用习惯不变。
'''

from test_zotero_api import test_api_connection


def main() -> None:
    test_api_connection()


if __name__ == '__main__':  # pragma: no cover
    main()

