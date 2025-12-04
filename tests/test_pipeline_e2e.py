#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 Zotero ingest 到分析结果的端到端小样本测试。"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List

from thesis_tools import zotero_ingest, zotero_analysis, schemas


def _make_foreign_like_item(key: str) -> Dict[str, Any]:
    """构造一条容易被识别为“外文文献”的条目。"""
    return {
        "data": {
            "key": key,
            "title": "Deep Learning for Thesis Work",
            "creators": [{"name": "John Doe"}],
            "date": "2023",
            "abstractNote": "An English abstract about deep learning.",
            "publicationTitle": "International Journal of AI",
            "itemType": "journalArticle",
            "tags": [{"tag": "AI"}],
            "dateAdded": "2023-12-01T00:00:00Z",
            "dateModified": "2023-12-02T00:00:00Z",
            "doi": "10.1234/foreign",
        }
    }


def _make_chinese_item(key: str) -> Dict[str, Any]:
    """构造一条“本地中文文献”条目，用于对比。"""
    return {
        "data": {
            "key": key,
            "title": "基于深度学习的毕业论文写作支持",
            "creators": [{"name": "张三"}],
            "date": "2024",
            "abstractNote": "中文摘要内容。",
            "publicationTitle": "教育技术研究",
            "itemType": "journalArticle",
            "tags": [{"tag": "教育技术"}],
            "dateAdded": "2024-01-01T00:00:00Z",
            "dateModified": "2024-01-02T00:00:00Z",
            "doi": "10.1234/chinese",
        }
    }


class PipelineE2ETests(unittest.TestCase):
    """验证从 ingest → JSON 文件 → 分析报告的基本流水线是否可用。"""

    def test_ingest_and_analyze_foreign_literature_pipeline(self) -> None:
        api_items: List[Dict[str, Any]] = [
            _make_foreign_like_item("FOREIGN1"),
            _make_chinese_item("LOCAL1"),
        ]

        processed = zotero_ingest.process_items(api_items)
        items_without_notes = zotero_ingest.split_items_by_notes(processed)

        # 基本结构应满足 schema 约定
        self.assertTrue(schemas.validate_zotero_items_structure(processed))
        self.assertGreaterEqual(len(items_without_notes), 1)

        with tempfile.TemporaryDirectory() as tmpdir_str:
            tmpdir = Path(tmpdir_str)
            items_path = tmpdir / "zotero_items.json"
            foreign_report_path = tmpdir / "foreign_literature_analysis.json"

            items_path.write_text(
                json.dumps(processed, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            report = zotero_analysis.analyze_foreign_literature(
                items_file=str(items_path),
                output_file=str(foreign_report_path),
                recent_limit=5,
            )

            # 至少应当识别出一条外文文献
            self.assertIsNotNone(report)
            assert report is not None
            self.assertGreaterEqual(report.get("total_foreign_literature", 0), 1)

            # 输出文件存在且结构满足 schema 约定
            self.assertTrue(foreign_report_path.exists())
            loaded = json.loads(foreign_report_path.read_text(encoding="utf-8"))
            self.assertTrue(
                schemas.validate_foreign_literature_analysis(loaded),
                "foreign_literature_analysis.json 结构不符合预期",
            )

            titles = {
                entry.get("title")
                for entry in loaded.get("recent_5_foreign", [])
            }
            self.assertIn("Deep Learning for Thesis Work", titles)


if __name__ == "__main__":  # pragma: no cover - 直接运行测试模块
    unittest.main()

