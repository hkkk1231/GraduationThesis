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


DEFAULT_ITEMS_FILE = r"E:\仓库\毕业论文\zotero_items.json"
DEFAULT_FOREIGN_ANALYSIS_FILE = (
    r"E:\仓库\毕业论文\foreign_literature_analysis.json"
)


def get_recent_literature_details(
    items_file: str = DEFAULT_ITEMS_FILE,
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


def is_foreign_literature(item: dict[str, Any]) -> bool:
    """根据标题、摘要、期刊和作者信息判断是否为外文文献。"""
    title = item.get("title", "").lower()
    abstract = item.get("abstractNote", "").lower()
    publication = item.get("publicationTitle", "").lower()
    creators = item.get("creators", [])

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


def extract_foreign_literature_info(item: dict[str, Any]) -> dict[str, Any]:
    """提取外文文献信息，结构化为下游可直接使用的字典。"""
    creators = item.get("creators", [])

    author_list: list[str] = []
    for creator in creators:
        if creator.get("name"):
            author_list.append(creator["name"])
        elif creator.get("firstName") and creator.get("lastName"):
            author_list.append(f"{creator['lastName']}, {creator['firstName']}")

    date_value = item.get("date", "")
    year_match = re.search(r"\b(19|20)\d{2}\b", date_value)
    year = year_match.group() if year_match else date_value

    tags = [
        tag.get("tag", "")
        for tag in item.get("tags", [])
        if isinstance(tag, dict) and tag.get("tag")
    ]

    return {
        "key": item.get("key", ""),
        "title": item.get("title", ""),
        "authors": author_list,
        "year": year,
        "abstract": item.get("abstractNote", ""),
        "publication": item.get("publicationTitle", ""),
        "item_type": item.get("itemType", ""),
        "tags": tags,
        "date_added": item.get("dateAdded", ""),
        "url": item.get("url", ""),
        "doi": item.get("doi", ""),
        "pages": item.get("pages", ""),
        "volume": item.get("volume", ""),
        "issue": item.get("issue", ""),
        "publisher": item.get("publisher", ""),
        "language": item.get("language", ""),
    }


def analyze_foreign_literature(
    items_file: str = DEFAULT_ITEMS_FILE,
    output_file: str = DEFAULT_FOREIGN_ANALYSIS_FILE,
    recent_limit: int = 5,
) -> dict[str, Any] | None:
    """从 Zotero JSON 中筛选外文文献，生成分析报告并写入 JSON。"""
    print("=== 外文文献分析工具 ===")

    try:
        with open(items_file, "r", encoding="utf-8") as f:
            items = json.load(f)
    except Exception as exc:  # pragma: no cover - I/O
        print(f"读取文件失败: {exc}")
        return None

    print(f"总文献数: {len(items)}")

    foreign_literature: list[dict[str, Any]] = []
    for item in items:
        if item.get("itemType") == "attachment":
            continue
        if is_foreign_literature(item):
            foreign_literature.append(extract_foreign_literature_info(item))

    print(f"发现外文文献: {len(foreign_literature)} 篇")

    if not foreign_literature:
        print("未发现外文文献，展示部分文献供人工检查...")
        for index, item in enumerate(items[:10], 1):
            if item.get("itemType") == "attachment":
                continue
            print(f"\n{index}. {item.get('title', '')}")
            print(f"   类型: {item.get('itemType', '')}")
            print(f"   期刊: {item.get('publicationTitle', '')}")
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
