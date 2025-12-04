#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zotero 文献分析助手。

当前封装了原 `get_recent_literature.py` 与外文文献分析脚本的核心逻辑，
用于：
- 获取最近添加的文献并输出基础统计；
- 检查可能包含外文内容的条目；
- 生成外文文献分析报告 JSON。

第二阶段重构中，本模块统一使用 `Literature` 领域模型作为数据载体，
并通过 `thesis_tools.schemas` 中的约定输出 JSON 结构。
"""

from __future__ import annotations

from datetime import datetime
import json
import re
from typing import Any

from .models import Literature
from .paths import (
    ZOTERO_ITEMS_FILE,
    FOREIGN_LITERATURE_ANALYSIS_FILE,
    RECENT_LITERATURE_ANALYSIS_FILE,
)


# 默认使用 report/ 目录中的 JSON 作为输入输出位置
DEFAULT_ITEMS_FILE = str(ZOTERO_ITEMS_FILE)
DEFAULT_FOREIGN_ANALYSIS_FILE = str(FOREIGN_LITERATURE_ANALYSIS_FILE)
DEFAULT_RECENT_ANALYSIS_FILE = str(RECENT_LITERATURE_ANALYSIS_FILE)


def _load_literature_items(items_file: str) -> list[Literature]:
    """从给定 JSON 文件中加载 `Literature` 列表。"""
    try:
        with open(items_file, "r", encoding="utf-8") as f:
            raw_items = json.load(f)
    except Exception as exc:  # pragma: no cover - I/O
        print(f"读取文件失败: {exc}")
        return []

    literature_items: list[Literature] = []
    for raw in raw_items:
        if not isinstance(raw, dict):
            continue
        try:
            literature_items.append(Literature.from_zotero_item_dict(raw))
        except Exception:
            # 单条解析失败时跳过，避免中断整体分析。
            continue

    return literature_items


def get_recent_literature_details(
    items_file: str = DEFAULT_ITEMS_FILE,
    limit: int = 10,
) -> list[Literature]:
    """获取最近添加的文献详细信息。"""
    items = _load_literature_items(items_file)
    if not items:
        return []

    valid_items = [
        item
        for item in items
        if item.item_type != "attachment" and item.title
    ]

    # 优先按添加时间排序，其次按年份和 key 兜底，避免空值导致排序混乱。
    def _sort_key(lit: Literature) -> tuple[str, str, str]:
        return (
            lit.date_added or "",
            lit.date or "",
            lit.id,
        )

    valid_items.sort(key=_sort_key, reverse=True)

    print("=== 最近添加的文献详细信息 ===")
    print(f"有效文献总数: {len(valid_items)}")

    recent_items = valid_items[:limit]

    for index, item in enumerate(recent_items, 1):
        print(f"\n{'=' * 80}")
        print(f"{index}. {item.title or '未知标题'}")
        print(f"   Key: {item.id}")
        print(f"   添加时间: {item.date_added or '未知'}")
        print(f"   修改时间: {item.date_modified or '未知'}")

        creators = item.creators
        if creators:
            author_list: list[str] = []
            for creator in creators:
                if creator.get("name"):
                    author_list.append(creator["name"])
                elif creator.get("firstName") and creator.get("lastName"):
                    author_list.append(
                        f"{creator['lastName']} {creator['firstName']}"
                    )
                elif creator.get("lastName"):
                    author_list.append(creator["lastName"])
            print(f"   作者: {', '.join(author_list)}")
        else:
            print("   作者: 未知")

        print(f"   年份: {item.date or '未知'}")
        print(f"   期刊: {item.publication_title or '未知'}")
        print(f"   类型: {item.item_type or '未知'}")

        abstract = item.abstract or ""
        if abstract:
            if len(abstract) > 500:
                abstract = abstract[:500] + "..."
            print(f"   摘要: {abstract}")
        else:
            print("   摘要: 无")

        tags = item.tags
        if tags:
            tag_list = [
                tag.get("tag", "")
                for tag in tags
                if isinstance(tag, dict) and tag.get("tag")
            ]
            if tag_list:
                print(f"   标签: {', '.join(tag_list)}")

        if item.url:
            print(f"   URL: {item.url}")
        if item.doi:
            print(f"   DOI: {item.doi}")

        print(f"   笔记数量: {len(item.notes)}")

    return recent_items


def analyze_literature_characteristics(items: list[Literature]) -> None:
    """分析文献特征（年份、期刊、类型、是否有笔记等）。"""
    print("\n=== 文献特征分析 ===")

    years: list[int] = []
    for item in items:
        date_value = item.date or ""
        year_match = re.search(r"\b(19|20)\d{2}\b", date_value)
        if year_match:
            years.append(int(year_match.group()))

    if years:
        year_count: dict[int, int] = {}
        for year in years:
            year_count[year] = year_count.get(year, 0) + 1
        print(f"年份分布: {dict(sorted(year_count.items()))}")

    journals: dict[str, int] = {}
    for item in items:
        journal = item.publication_title or ""
        if journal:
            journals[journal] = journals.get(journal, 0) + 1

    if journals:
        top_journals = dict(
            sorted(journals.items(), key=lambda x: x[1], reverse=True)[:5]
        )
        print(f"期刊分布（前若干个）: {top_journals}")

    types: dict[str, int] = {}
    for item in items:
        item_type = item.item_type or ""
        if item_type:
            types[item_type] = types.get(item_type, 0) + 1
    print(f"文献类型分布: {types}")

    with_notes = sum(1 for item in items if item.notes)
    without_notes = len(items) - with_notes
    print(f"有笔记的文献: {with_notes} 篇")
    print(f"无笔记的文献: {without_notes} 篇")


def check_for_foreign_content(
    items: list[Literature],
) -> list[dict[str, str]]:
    """检查是否包含外文内容（标题/摘要/期刊）。"""
    print("\n=== 外文内容检查 ===")

    potential_foreign: list[dict[str, str]] = []

    for item in items:
        title = item.title or ""
        abstract = item.abstract or ""
        publication = item.publication_title or ""

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
        print(f"发现 {len(potential_foreign)} 个可能的外文内容：")
        for entry in potential_foreign:
            print(f"  - {entry['title'][:50]}... ({entry['reason']})")
    else:
        print("未发现明显的外文内容")

    return potential_foreign


def is_foreign_literature(item: Literature) -> bool:
    """根据标题、摘要、期刊和作者信息判断是否为外文文献。"""
    title = (item.title or "").lower()
    abstract = (item.abstract or "").lower()
    publication = (item.publication_title or "").lower()
    creators = item.creators

    has_foreign_authors = False
    for creator in creators:
        name = creator.get("name", "")
        if " " in name and not re.search(r"[\u4e00-\u9fff]", name):
            has_foreign_authors = True
            break

    has_english_title = bool(re.search(r"[a-zA-Z]", title)) and not re.search(
        r"[\u4e00-\u9fff]", title
    )
    has_foreign_publication = bool(
        re.search(r"[a-zA-Z]", publication)
    ) and not re.search(r"[\u4e00-\u9fff]", publication)
    has_foreign_abstract = bool(
        re.search(r"[a-zA-Z]", abstract)
    ) and not re.search(r"[\u4e00-\u9fff]", abstract)

    return (
        has_foreign_authors
        or has_english_title
        or has_foreign_publication
        or has_foreign_abstract
    )


def extract_foreign_literature_info(item: Literature) -> dict[str, Any]:
    """提取外文文献信息，结构化为下游可直接使用的字典。"""
    creators = item.creators

    author_list: list[str] = []
    for creator in creators:
        if creator.get("name"):
            author_list.append(creator["name"])
        elif creator.get("firstName") and creator.get("lastName"):
            author_list.append(f"{creator['lastName']}, {creator['firstName']}")

    date_value = item.date or ""
    year_match = re.search(r"\b(19|20)\d{2}\b", date_value)
    year = year_match.group() if year_match else date_value

    tags = [
        tag.get("tag", "")
        for tag in item.tags
        if isinstance(tag, dict) and tag.get("tag")
    ]

    return {
        "key": item.id,
        "title": item.title or "",
        "authors": author_list,
        "year": year,
        "abstract": item.abstract or "",
        "publication": item.publication_title or "",
        "item_type": item.item_type or "",
        "tags": tags,
        "date_added": item.date_added or "",
        "url": item.url or "",
        "doi": item.doi or "",
        "pages": item.pages or "",
        "volume": item.volume or "",
        "issue": item.issue or "",
        "publisher": item.publisher or "",
        "language": item.language or "",
    }


def analyze_foreign_literature(
    items_file: str = DEFAULT_ITEMS_FILE,
    output_file: str = DEFAULT_FOREIGN_ANALYSIS_FILE,
    recent_limit: int = 5,
) -> dict[str, Any] | None:
    """从 Zotero JSON 中筛选外文文献，生成分析报告并写入 JSON。"""
    print("=== 外文文献分析工具 ===")

    items = _load_literature_items(items_file)
    if not items:
        return None

    print(f"总文献数: {len(items)}")

    foreign_literature: list[dict[str, Any]] = []
    for item in items:
        if item.item_type == "attachment":
            continue
        if is_foreign_literature(item):
            foreign_literature.append(extract_foreign_literature_info(item))

    print(f"发现外文文献: {len(foreign_literature)} 篇")

    if not foreign_literature:
        print("未发现外文文献，展示部分文献供人工检查...")
        for index, item in enumerate(items[:10], 1):
            if item.item_type == "attachment":
                continue
            print(f"\n{index}. {item.title or ''}")
            print(f"   类型: {item.item_type or ''}")
            print(f"   期刊: {item.publication_title or ''}")
        return None

    foreign_literature.sort(key=lambda x: x.get("date_added", ""), reverse=True)
    recent_foreign = foreign_literature[:recent_limit]

    print(f"\n=== 最近新增的 {recent_limit} 篇外文文献 ===")
    for index, info in enumerate(recent_foreign, 1):
        print(f"\n{'=' * 60}")
        print(f"{index}. {info['title']}")
        print(f"   Key: {info['key']}")
        authors = ", ".join(info["authors"]) if info["authors"] else "未知"
        print(f"   作者: {authors}")
        print(f"   年份: {info['year'] or '未知'}")
        print(f"   期刊: {info['publication'] or '未知'}")
        print(f"   类型: {info['item_type']}")
        if info.get("volume"):
            print(f"   卷: {info['volume']}")
        if info.get("issue"):
            print(f"   期: {info['issue']}")
        if info.get("pages"):
            print(f"   页码: {info['pages']}")
        if info.get("publisher"):
            print(f"   出版社: {info['publisher']}")

        abstract = info.get("abstract", "")
        if abstract:
            preview = abstract[:300] + "..." if len(abstract) > 300 else abstract
            print(f"   摘要: {preview}")
        else:
            print("   摘要: 无")

        if info.get("tags"):
            print(f"   标签: {', '.join(info['tags'])}")
        if info.get("doi"):
            print(f"   DOI: {info['doi']}")
        if info.get("url"):
            print(f"   URL: {info['url']}")
        print(f"   添加时间: {info['date_added']}")

    report = {
        "total_foreign_literature": len(foreign_literature),
        "recent_5_foreign": recent_foreign,
        "all_foreign_literature": foreign_literature,
        "analysis_time": datetime.now().isoformat(),
    }

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n外文文献分析结果已保存到: {output_file}")
    except Exception as exc:  # pragma: no cover - I/O
        print(f"保存文件时出错: {exc}")

    return report


def main() -> None:
    """命令行入口：获取最近文献并完成基础分析。"""
    print("=== Zotero 最近文献详细分析 ===")

    recent_items = get_recent_literature_details()
    if not recent_items:
        return

    analyze_literature_characteristics(recent_items)
    foreign_items = check_for_foreign_content(recent_items)

    analysis_result = {
        "recent_literature": [
            item.to_zotero_item_dict() for item in recent_items
        ],
        "foreign_content_found": bool(foreign_items),
        "potential_foreign_items": foreign_items,
        "analysis_time": datetime.now().isoformat(),
        "total_recent_items": len(recent_items),
    }

    output_file = DEFAULT_RECENT_ANALYSIS_FILE
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        print(f"\n分析结果已保存到: {output_file}")
    except Exception as exc:  # pragma: no cover - I/O
        print(f"保存文件时出错: {exc}")


if __name__ == "__main__":  # pragma: no cover - 脚本入口
    main()
