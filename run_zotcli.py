#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行zotero-cli的包装脚本
"""

from zotero_cli.cli import cli
import sys

if __name__ == "__main__":
    # 将命令行参数传递给zotero-cli
    cli(sys.argv[1:])