#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON Schema 与数据结构约定。

本模块为 `zotero_items.json`、`recent_literature_analysis.json` 等
核心中间文件提供轻量级的 schema 描述与基础校验工具，用于在
脚本内部保持字段命名和类型的一致性。

说明：
- 现有 JSON 中部分字段（如 `abstractNote`、`publicationTitle`）沿用
  Zotero 的驼峰命名以兼容既有脚本；
- 项目自定义字段（如分析结果中的元信息）统一采用 snake_case；
- 这里的 schema 不是完整 JSON Schema 实现，仅覆盖常用字段与
  必填项，便于后续扩展为严格校验。
"""

from __future__ import annotations

from typing import Any, Mapping

JsonDict = dict[str, Any]

# ---------------------------------------------------------------------------
# 基础字段 Schema
# ---------------------------------------------------------------------------

ZOTERO_ITEM_SCHEMA: JsonDict = {
    "type": "object",
    "title": "ZoteroItem",
    "properties": {
        "key": {"type": "string"},
        "title": {"type": "string"},
        "creators": {"type": "array"},
        "date": {"type": "string"},
        "abstractNote": {"type": "string"},
        "publicationTitle": {"type": "string"},
        "itemType": {"type": "string"},
        "tags": {"type": "array"},
        "notes": {"type": "array"},
        "dateAdded": {"type": "string"},
        "dateModified": {"type": "string"},
        "url": {"type": "string"},
        "doi": {"type": "string"},
        "pages": {"type": "string"},
        "volume": {"type": "string"},
        "issue": {"type": "string"},
        "publisher": {"type": "string"},
        "language": {"type": "string"},
    },
    "required": ["key", "title"],
    "additionalProperties": True,
}

ZOTERO_ITEMS_FILE_SCHEMA: JsonDict = {
    "type": "array",
    "title": "ZoteroItemsFile",
    "items": ZOTERO_ITEM_SCHEMA,
}

# recent_literature_analysis.json 顶层结构
RECENT_LITERATURE_ANALYSIS_SCHEMA: JsonDict = {
    "type": "object",
    "title": "RecentLiteratureAnalysis",
    "properties": {
        "recent_literature": {
            "type": "array",
            "items": ZOTERO_ITEM_SCHEMA,
        },
        "foreign_content_found": {"type": "boolean"},
        "potential_foreign_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "reason": {"type": "string"},
                    "publication": {"type": "string"},
                },
                "required": ["title", "reason"],
                "additionalProperties": True,
            },
        },
        "analysis_time": {"type": "string"},
        "total_recent_items": {"type": "integer"},
    },
    "required": ["recent_literature", "analysis_time", "total_recent_items"],
    "additionalProperties": True,
}

# foreign_literature_analysis.json 顶层结构
FOREIGN_LITERATURE_ANALYSIS_SCHEMA: JsonDict = {
    "type": "object",
    "title": "ForeignLiteratureAnalysis",
    "properties": {
        "total_foreign_literature": {"type": "integer"},
        "recent_5_foreign": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "title": {"type": "string"},
                    "authors": {"type": "array"},
                    "year": {"type": "string"},
                    "abstract": {"type": "string"},
                    "publication": {"type": "string"},
                    "item_type": {"type": "string"},
                    "tags": {"type": "array"},
                    "date_added": {"type": "string"},
                    "url": {"type": "string"},
                    "doi": {"type": "string"},
                    "pages": {"type": "string"},
                    "volume": {"type": "string"},
                    "issue": {"type": "string"},
                    "publisher": {"type": "string"},
                    "language": {"type": "string"},
                },
                "required": ["key", "title"],
                "additionalProperties": True,
            },
        },
        "all_foreign_literature": {
            "type": "array",
            "items": {"$ref": "#/properties/recent_5_foreign/items"},
        },
        "analysis_time": {"type": "string"},
    },
    "required": ["total_foreign_literature", "analysis_time"],
    "additionalProperties": True,
}


# ---------------------------------------------------------------------------
# 轻量级校验辅助函数（不依赖外部 jsonschema 库）
# ---------------------------------------------------------------------------

def _validate_required_fields(data: Any, schema: Mapping[str, Any]) -> bool:
    """只检查最外层 type 与 required 字段是否符合预期。"""
    schema_type = schema.get("type")

    if schema_type == "object":
        if not isinstance(data, dict):
            return False
        required = schema.get("required", [])
        missing = [name for name in required if name not in data]
        return not missing

    if schema_type == "array":
        if not isinstance(data, list):
            return False
        item_schema = schema.get("items")
        if isinstance(item_schema, Mapping):
            return all(_validate_required_fields(item, item_schema) for item in data)
        return True

    # 其他类型暂不做深度校验
    return True


def validate_zotero_items_structure(data: Any) -> bool:
    """检查 `zotero_items.json` 的基础结构是否满足预期。"""
    return _validate_required_fields(data, ZOTERO_ITEMS_FILE_SCHEMA)


def validate_recent_literature_analysis(data: Any) -> bool:
    """检查 `recent_literature_analysis.json` 顶层结构。"""
    return _validate_required_fields(data, RECENT_LITERATURE_ANALYSIS_SCHEMA)


def validate_foreign_literature_analysis(data: Any) -> bool:
    """检查 `foreign_literature_analysis.json` 顶层结构。"""
    return _validate_required_fields(data, FOREIGN_LITERATURE_ANALYSIS_SCHEMA)

