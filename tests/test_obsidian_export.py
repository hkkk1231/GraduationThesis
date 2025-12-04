#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""thesis_tools.obsidian_export 模块的基础单元测试。"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List

from thesis_tools import obsidian_export


class ObsidianExportTests(unittest.TestCase):
    """针对文件名清洗与笔记生成的核心路径做小样本测试。"""

    def test_sanitize_filename_removes_illegal_chars(self) -> None:
        raw = '01:2024?"Invalid*Name<test>|.md'
        sanitized = obsidian_export.sanitize_filename(raw)
        self.assertNotIn(":", sanitized)
        self.assertNotIn("?", sanitized)
        self.assertNotIn("*", sanitized)
        self.assertNotIn("<", sanitized)
        self.assertNotIn("|", sanitized)
        self.assertTrue(sanitized.endswith(".md"))

    def test_create_obsidian_note_fills_template_placeholders(self) -> None:
        item: Dict[str, Any] = {
            "title": "Test 文献",
            "creators": [
                {"name": "张三"},
                {"lastName": "Doe", "firstName": "John"},
            ],
            "date": "2024",
            "publicationTitle": "测试期刊",
            "doi": "10.1234/example",
            "itemType": "journalArticle",
            "tags": [{"tag": "AI"}, {"tag": "Thesis"}],
            "dateAdded": "2024-01-01T00:00:00Z",
            "abstractNote": "This is a test abstract.",
            "key": "ABC123",
        }

        template_content = (
            "{{title}}\n"
            "{{authors}}\n"
            "{{publication}}\n"
            "{{year}}\n"
            "{{doi}}\n"
            "{{citekey}}\n"
            "{{itemType}}\n"
            "{{tags}}\n"
            "{{collections}}\n"
            "{{dateAdded}}\n"
            "{{abstract}}\n"
            "{{bibtex}}\n"
            "{{firstTag}}\n"
            "{{date}}\n"
        )

        with tempfile.TemporaryDirectory() as tmpdir_str:
            tmpdir = Path(tmpdir_str)
            template_path = tmpdir / "template.md"
            template_path.write_text(template_content, encoding="utf-8")

            note = obsidian_export.create_obsidian_note(
                item, str(template_path)
            )

            self.assertIsNotNone(note)
            assert note is not None  # for type checkers
            self.assertIn("Test 文献", note)
            self.assertIn("张三", note)
            self.assertIn("2024", note)
            # BibTeX 风格引用应被插入
            self.assertIn("[1]", note)
            self.assertIn("journalArticle", note)

    def test_generate_latest_notes_creates_note_and_index_files(self) -> None:
        # 使用一条有效的 items 记录，确保被 generate_latest_notes 挑选到
        items: List[Dict[str, Any]] = [
            {
                "key": "ABC123",
                "title": "Test Article",
                "creators": [{"name": "John Doe"}],
                "date": "2024",
                "abstractNote": "Sample abstract",
                "publicationTitle": "Sample Journal",
                "itemType": "journalArticle",
                "tags": [{"tag": "AI"}],
                "notes": [],
                "dateAdded": "2024-01-01T00:00:00Z",
                "dateModified": "2024-01-02T00:00:00Z",
                "doi": "10.1234/example",
            }
        ]

        with tempfile.TemporaryDirectory() as tmpdir_str:
            tmpdir = Path(tmpdir_str)
            items_path = tmpdir / "zotero_items.json"
            template_path = tmpdir / "template.md"
            output_dir = tmpdir / "notes"

            items_path.write_text(
                json.dumps(items, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            template_path.write_text("{{title}}", encoding="utf-8")

            obsidian_export.generate_latest_notes(
                items_file=str(items_path),
                template_path=str(template_path),
                output_dir=str(output_dir),
                max_items=1,
            )

            self.assertTrue(output_dir.exists())
            md_files = [f for f in os.listdir(output_dir) if f.endswith(".md")]
            # 至少应包含 1 个笔记文件和 1 个索引文件
            self.assertGreaterEqual(len(md_files), 2)
            self.assertIn("最新文献笔记索引.md", md_files)


if __name__ == "__main__":  # pragma: no cover - 直接运行测试模块
    unittest.main()

