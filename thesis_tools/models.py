#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
领域模型定义模块。

本模块在重构第二阶段中落地 `Literature` / `Note` / `AnalysisResult`
等核心领域对象，用于在脚本之间传递统一的数据结构，并提供
与现有 JSON 文件之间的转换辅助函数。

约定：
- 模型内部字段全部使用 snake_case 命名；
- 与 Zotero/现有 JSON 的驼峰字段通过工厂方法进行映射；
- 写回 `zotero_items.json` 时尽量保持向后兼容当前字段结构。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

JsonDict = dict[str, Any]


@dataclass
class Literature:
    """文献条目的统一领域模型。

    该模型抽象了 Zotero 条目以及下游分析/笔记生成所需的核心字段，
    并提供从 API 原始结构和本地 JSON 结构之间的相互转换。
    """

    id: str
    title: str
    creators: list[JsonDict] = field(default_factory=list)
    date: str | None = None
    abstract: str | None = None
    publication_title: str | None = None
    item_type: str | None = None
    tags: list[JsonDict] = field(default_factory=list)
    notes: list[Any] = field(default_factory=list)
    date_added: str | None = None
    date_modified: str | None = None
    url: str | None = None
    doi: str | None = None
    pages: str | None = None
    volume: str | None = None
    issue: str | None = None
    publisher: str | None = None
    language: str | None = None

    @classmethod
    def from_zotero_api_item(cls, item: Mapping[str, Any]) -> "Literature":
        """从 Zotero API 返回的原始 item 结构构建实例。

        典型结构：{"data": {...}, "notes": [...], ...}
        """
        data = item.get("data", {}) or {}

        key = data.get("key") or item.get("key") or ""

        return cls(
            id=str(key),
            title=data.get("title", "") or "",
            creators=list(data.get("creators", []) or []),
            date=data.get("date") or None,
            abstract=data.get("abstractNote") or None,
            publication_title=data.get("publicationTitle") or None,
            item_type=data.get("itemType") or None,
            tags=list(data.get("tags", []) or []),
            notes=list(item.get("notes", []) or data.get("notes", []) or []),
            date_added=data.get("dateAdded") or None,
            date_modified=data.get("dateModified") or None,
            url=data.get("url") or None,
            doi=data.get("doi") or None,
            pages=data.get("pages") or None,
            volume=data.get("volume") or None,
            issue=data.get("issue") or None,
            publisher=data.get("publisher") or None,
            language=data.get("language") or None,
        )

    @classmethod
    def from_zotero_item_dict(cls, data: Mapping[str, Any]) -> "Literature":
        """从本地 `zotero_items.json` 中的一条记录构建实例。

        为兼容现有数据，既支持驼峰字段（例如 abstractNote），也支持
        未来可能引入的 snake_case 字段（例如 abstract）。
        """
        return cls(
            id=str(data.get("key", "")),
            title=data.get("title", "") or "",
            creators=list(data.get("creators", []) or []),
            date=data.get("date") or None,
            abstract=(
                data.get("abstract")
                or data.get("abstractNote")
                or None
            ),
            publication_title=(
                data.get("publication_title")
                or data.get("publicationTitle")
                or data.get("publication")
                or None
            ),
            item_type=data.get("item_type") or data.get("itemType") or None,
            tags=list(data.get("tags", []) or []),
            notes=list(data.get("notes", []) or []),
            date_added=data.get("date_added") or data.get("dateAdded") or None,
            date_modified=(
                data.get("date_modified") or data.get("dateModified") or None
            ),
            url=data.get("url") or None,
            doi=data.get("doi") or None,
            pages=data.get("pages") or None,
            volume=data.get("volume") or None,
            issue=data.get("issue") or None,
            publisher=data.get("publisher") or None,
            language=data.get("language") or None,
        )

    def to_zotero_item_dict(self) -> JsonDict:
        """导出为写入 `zotero_items.json` 的标准结构。

        为了保持与现有脚本的兼容性，这里沿用 Zotero 的驼峰字段名称：
        - abstractNote / publicationTitle / itemType / dateAdded / dateModified
        """
        return {
            "key": self.id,
            "title": self.title,
            "creators": self.creators,
            "date": self.date or "",
            "abstractNote": self.abstract or "",
            "publicationTitle": self.publication_title or "",
            "itemType": self.item_type or "",
            "tags": self.tags,
            "notes": self.notes,
            "dateAdded": self.date_added or "",
            "dateModified": self.date_modified or "",
            "url": self.url or "",
            "doi": self.doi or "",
            "pages": self.pages or "",
            "volume": self.volume or "",
            "issue": self.issue or "",
            "publisher": self.publisher or "",
            "language": self.language or "",
        }


@dataclass
class Note:
    """Obsidian / 研究笔记的领域模型。

    目前主要用于为后续 Phase 3 的 CLI 和深度阅读流水线预留结构。
    """

    note_id: str
    literature_id: str | None = None
    note_path: str | None = None
    summary: str | None = None
    key_points: list[str] = field(default_factory=list)
    quotes: list[str] = field(default_factory=list)
    status: str | None = None  # 如: "todo" / "in_progress" / "done"

    def to_dict(self) -> JsonDict:
        """导出为可序列化的 dict 结构。"""
        return {
            "note_id": self.note_id,
            "literature_id": self.literature_id,
            "note_path": self.note_path,
            "summary": self.summary,
            "key_points": list(self.key_points),
            "quotes": list(self.quotes),
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Note":
        """从 dict 恢复 Note 实例。"""
        return cls(
            note_id=str(data.get("note_id", "")),
            literature_id=data.get("literature_id"),
            note_path=data.get("note_path"),
            summary=data.get("summary"),
            key_points=list(data.get("key_points", []) or []),
            quotes=list(data.get("quotes", []) or []),
            status=data.get("status"),
        )


@dataclass
class AnalysisResult:
    """单篇文献的分析结果模型。

    预期用于承载深度阅读或结构化评审的要点，便于后续输出到
    Obsidian、Word 草稿或 MCP 调用。
    """

    literature_id: str
    problem_statement: str | None = None
    methodology: str | None = None
    contribution: str | None = None
    limitations: str | None = None
    future_work: str | None = None

    def to_dict(self) -> JsonDict:
        """导出为 JSON 友好的 dict。"""
        return {
            "literature_id": self.literature_id,
            "problem_statement": self.problem_statement,
            "methodology": self.methodology,
            "contribution": self.contribution,
            "limitations": self.limitations,
            "future_work": self.future_work,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "AnalysisResult":
        """从 dict 恢复 AnalysisResult 实例。"""
        return cls(
            literature_id=str(data.get("literature_id", "")),
            problem_statement=data.get("problem_statement"),
            methodology=data.get("methodology"),
            contribution=data.get("contribution"),
            limitations=data.get("limitations"),
            future_work=data.get("future_work"),
        )

