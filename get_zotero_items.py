#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
兼容入口：保留原有 ``python get_zotero_items.py`` 调用方式。

内部委托给 ``scripts/get_zotero_items.py``，后者再调用
``thesis_tools.zotero_ingest`` 中的逻辑。
"""

from scripts.get_zotero_items import main


if __name__ == "__main__":  # pragma: no cover
    main()

