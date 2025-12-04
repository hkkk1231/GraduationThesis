#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""thesis_tools.zotero_ingest 模块的基础单元测试。"""

from __future__ import annotations

import unittest
from typing import Any, Dict, List

from thesis_tools import zotero_ingest
from thesis_tools import schemas


def _make_sample_api_item(
    key: str,
    title: str,
    has_notes: bool = False,
) -> Dict[str, Any]:
    """构造一个模拟的 Zotero API item 结构。"""
    data: Dict[str, Any] = {
        "key": key,
        "title": title,
        "creators": [{"name": "John Doe"}],
        "date": "2024",
        "abstractNote": "Sample abstract",
        "publicationTitle": "Sample Journal",
        "itemType": "journalArticle",
        "tags": [{"tag": "AI"}],
        "dateAdded": "2024-01-01T00:00:00Z",
        "dateModified": "2024-01-02T00:00:00Z",
    }
    api_item: Dict[str, Any] = {"data": data}
    if has_notes:
        api_item["notes"] = ["note-1"]
    return api_item


class ZoteroIngestTests(unittest.TestCase):
    """针对 process_items / split_items_by_notes 的基础行为测试。"""

    def test_process_items_produces_schema_compatible_output(self) -> None:
        api_items: List[Dict[str, Any]] = [
            _make_sample_api_item("ABC123", "First Article"),
            _make_sample_api_item("XYZ789", "Second Article", has_notes=True),
        ]

        processed = zotero_ingest.process_items(api_items)

        # 数量保持一致
        self.assertEqual(len(processed), len(api_items))
        # 关键字段被正确映射
        first = processed[0]
        self.assertEqual(first["key"], "ABC123")
        self.assertEqual(first["title"], "First Article")
        self.assertEqual(first["publicationTitle"], "Sample Journal")

        # 结构与约定的 schema 基本一致
        self.assertTrue(schemas.validate_zotero_items_structure(processed))

    def test_split_items_by_notes_filters_items_without_notes(self) -> None:
        processed: List[Dict[str, Any]] = [
            {
                "key": "1",
                "title": "With Notes",
                "notes": ["some-note"],
                "itemType": "journalArticle",
            },
            {
                "key": "2",
                "title": "Without Notes",
                "notes": [],
                "itemType": "journalArticle",
            },
            {
                "key": "3",
                "title": "A Note Item",
                "notes": [],
                "itemType": "note",
            },
        ]

        without_notes = zotero_ingest.split_items_by_notes(processed)
        keys = {item["key"] for item in without_notes}

        # 只保留“没有任何笔记且本身不是 note 类型”的条目
        self.assertEqual(keys, {"2"})


if __name__ == "__main__":  # pragma: no cover - 直接运行测试模块
    unittest.main()

