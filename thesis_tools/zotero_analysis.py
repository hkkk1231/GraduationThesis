#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zotero 分析助手。

目前封装原 ``get_recent_literature.py`` 的核心逻辑，用于获取最近
添加的文献、做基础特征分析并输出 JSON 结果。
"""

from __future__ import annotations

from datetime import datetime
import json
import re
from typing import Any


def get_recent_literature_details(
    items_file: str = r"E:\仓库\毕业论文\zotero_items.json",
    limit: int = 10,
) -> list[dict[str, Any]]:
    """获取最近添加的文献详细信息。"""
    try:
        with open(items_file, "r", encoding="utf-8") as f:
            items = json.load(f)
    except Exception as exc:  # pragma: no cover - I/O
        print(f"读取文件失败: {exc}")
        return []

    valid_items = [
        item
        for item in items
        if item.get("itemType") != "attachment" and item.get("title")
    ]

    valid_items.sort(key=lambda x: x.get("dateAdded", ""), reverse=True)

    print("=== 最近添加的文献详细信息 ===")
    print(f"有效文献总数: {len(valid_items)}")

    recent_items = valid_items[:limit]

    for index, item in enumerate(recent_items, 1):
        print(f"\n{'=' * 80}")
        print(f"{index}. {item.get('title', '未知标题')}")
        print(f"   Key: {item.get('key', '')}")
        print(f"   添加时间: {item.get('dateAdded', '未知')}")
        print(f"   修改时间: {item.get('dateModified', '未知')}")

        creators = item.get("creators", [])
        if creators:
            author_list: list[str] = []
            for creator in creators:
                if creator.get("name"):
                    author_list.append(creator["name"])
                elif creator.get("firstName") and creator.get("lastName"):
                    author_list.append(f"{creator['lastName']} {creator['firstName']}")
                elif creator.get("lastName"):
                    author_list.append(creator["lastName"])
            print(f"   作者: {', '.join(author_list)}")
        else:
            print("   作者: 未知")

        print(f"   年份: {item.get('date', '未知')}")
        print(f"   期刊: {item.get('publicationTitle', '未知')}")
        print(f"   类型: {item.get('itemType', '未知')}")

        abstract = item.get("abstractNote", "")
        if abstract:
            if len(abstract) > 500:
                abstract = abstract[:500] + "..."
            print(f"   摘要: {abstract}")
        else:
            print("   摘要: 无")

        tags = item.get("tags", [])
        if tags:
            tag_list = [tag.get("tag", "") for tag in tags if tag.get("tag")]
            print(f"   标签: {', '.join(tag_list)}")

        if item.get("url"):
            print(f"   URL: {item['url']}")
        if item.get("doi"):
            print(f"   DOI: {item['doi']}")

        notes = item.get("notes", [])
        print(f"   笔记数量: {len(notes)}")

    return recent_items


def analyze_literature_characteristics(items: list[dict[str, Any]]) -> None:
    """分析文献特点（年份、期刊、类型、是否有笔记等）。"""
    print("\n=== 文献特征分析 ===")

    years: list[int] = []
    for item in items:
        date = item.get("date", "")
        year_match = re.search(r"\b(19|20)\d{2}\b", date)
        if year_match:
            years.append(int(year_match.group()))

    if years:
        year_count: dict[int, int] = {}
        for year in years:
            year_count[year] = year_count.get(year, 0) + 1
        print(f"年份分布: {dict(sorted(year_count.items()))}")

    journals: dict[str, int] = {}
    for item in items:
        journal = item.get("publicationTitle", "")
        if journal:
            journals[journal] = journals.get(journal, 0) + 1

    if journals:
        top_journals = dict(
            sorted(journals.items(), key=lambda x: x[1], reverse=True)[:5]
        )
        print(f"期刊分布 (前若干): {top_journals}")

    types: dict[str, int] = {}
    for item in items:
        item_type = item.get("itemType", "")
        if item_type:
            types[item_type] = types.get(item_type, 0) + 1
    print(f"文献类型分布: {types}")

    with_notes = sum(1 for item in items if item.get("notes"))
    without_notes = len(items) - with_notes
    print(f"有笔记的文献: {with_notes} 篇")
    print(f"无笔记的文献: {without_notes} 篇")


def check_for_foreign_content(
    items: list[dict[str, Any]],
) -> list[dict[str, str]]:
    """检查是否含有外文内容。"""
    print("\n=== 外文内容检查 ===")

    potential_foreign: list[dict[str, str]] = []

    for item in items:
        title = item.get("title", "")
        abstract = item.get("abstractNote", "")
        publication = item.get("publicationTitle", "")

        if re.search(r"^[a-zA-Z\s:,\-\.?]+$", title) and len(title) > 10:
            potential_foreign.append(
                {
                    "title": title,
                    "reason": "英文标题",
                    "publication": publication,
                }
            )

        if abstract and re.search(r"^[a-zA-Z\s:,\-\.?]+$", abstract[:100]):
            potential_foreign.append(
                {
                    "title": title,
                    "reason": "英文摘要",
                    "publication": publication,
                }
            )

        if publication and re.search(r"^[a-zA-Z\s:,\-\.?]+$", publication):
            potential_foreign.append(
                {
                    "title": title,
                    "reason": "英文期刊名称",
                    "publication": publication,
                }
            )

    if potential_foreign:
        print(f"发现 {len(potential_foreign)} 个可能的外文内容:")
        for item in potential_foreign:
            print(f"  - {item['title'][:50]}... ({item['reason']})")
    else:
        print("未发现明显的外文内容")

    return potential_foreign


def main() -> None:
    """命令行入口：获取最近文献并完成基础分析。"""
    print("=== Zotero 最近文献详细分析 ===")

    recent_items = get_recent_literature_details()
    if not recent_items:
        return

    analyze_literature_characteristics(recent_items)
    foreign_items = check_for_foreign_content(recent_items)

    analysis_result = {
        "recent_literature": recent_items,
        "foreign_content_found": bool(foreign_items),
        "potential_foreign_items": foreign_items,
        "analysis_time": datetime.now().isoformat(),
        "total_recent_items": len(recent_items),
    }

    output_file = r"E:\仓库\毕业论文\recent_literature_analysis.json"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        print(f"\n分析结果已保存到: {output_file}")
    except Exception as exc:  # pragma: no cover - I/O
        print(f"保存文件时出错: {exc}")


if __name__ == "__main__":  # pragma: no cover - 脚本入口
    main()

