#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian 笔记生成相关辅助函数。

当前主要封装了原 ``create_obsidian_notes.py`` 的逻辑，用于从
Zotero 导出的 JSON 数据批量创建最新文献的 Obsidian 笔记。
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime
from typing import Any


def sanitize_filename(title: str) -> str:
    """清理文件名，移除不合法字符并限制长度。"""
    safe = re.sub(r'[<>:"/\\|?*]', "", title)
    safe = safe.replace("\n", " ").replace("\r", " ")
    if len(safe) > 100:
        safe = safe[:100] + "..."
    return safe.strip()


def generate_bibtex_citation(item: dict[str, Any]) -> str:
    """生成近似 GB/T 7714-2015 形式的引用字符串。"""
    title = item.get("title", "")
    authors = item.get("creators", [])
    year = item.get("date", "")
    publication = item.get("publicationTitle", "")

    author_list: list[str] = []
    for creator in authors:
        if creator.get("name"):
            author_list.append(creator["name"])

    author_str = ", ".join(author_list) if author_list else "未知作者"

    year_match = re.search(r"\b(19|20)\d{2}\b", year)
    year_str = year_match.group() if year_match else year

    if publication:
        citation = f"[1] {author_str}. {title}[J]. {publication}, {year_str}"
    else:
        citation = f"[1] {author_str}. {title}[J]. 未明确期刊, {year_str}"

    return citation


def create_obsidian_note(item: dict[str, Any], template_path: str) -> str | None:
    """根据模板和文献信息生成单篇 Obsidian 笔记内容。"""
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    except Exception as exc:  # pragma: no cover - I/O
        print(f"读取模板失败: {exc}")
        return None

    creators = item.get("creators", [])
    author_list: list[str] = []
    for creator in creators:
        if creator.get("name"):
            author_list.append(creator["name"])
        elif creator.get("lastName") and creator.get("firstName"):
            author_list.append(f"{creator['lastName']} {creator['firstName']}")

    authors_str = ", ".join(author_list) if author_list else "未知"

    tags = item.get("tags", [])
    tag_list = [tag.get("tag", "") for tag in tags if tag.get("tag")]
    tags_str = ", ".join(tag_list) if tag_list else "无"
    first_tag = tag_list[0] if tag_list else "未分类"

    date_value = item.get("date", "")
    year_match = re.search(r"\b(19|20)\d{2}\b", date_value)
    year_str = year_match.group() if year_match else date_value

    citation = generate_bibtex_citation(item)

    note_content = template.replace("{{title}}", item.get("title", "未知标题"))
    note_content = note_content.replace("{{authors}}", authors_str)
    note_content = note_content.replace(
        "{{publication}}", item.get("publicationTitle", "未知")
    )
    note_content = note_content.replace("{{year}}", year_str)
    note_content = note_content.replace("{{doi}}", item.get("doi", "无"))
    note_content = note_content.replace("{{citekey}}", item.get("key", ""))
    note_content = note_content.replace("{{itemType}}", item.get("itemType", "未知"))
    note_content = note_content.replace("{{tags}}", tags_str)
    note_content = note_content.replace("{{collections}}", "未分类")
    note_content = note_content.replace(
        "{{dateAdded}}", item.get("dateAdded", "未知")
    )
    note_content = note_content.replace(
        "{{abstract}}", item.get("abstractNote", "无摘要")
    )
    note_content = note_content.replace("{{bibtex}}", citation)
    note_content = note_content.replace("{{firstTag}}", first_tag)
    note_content = note_content.replace(
        "{{date}}", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    return note_content


def generate_latest_notes(
    items_file: str,
    template_path: str,
    output_dir: str,
    max_items: int = 5,
) -> None:
    """从给定 JSON 文件中选择最新若干文献并生成 Obsidian 笔记。"""
    os.makedirs(output_dir, exist_ok=True)

    try:
        with open(items_file, "r", encoding="utf-8") as f:
            items = json.load(f)
    except Exception as exc:  # pragma: no cover - I/O
        print(f"读取文献数据失败: {exc}")
        return

    valid_items: list[dict[str, Any]] = []
    for item in items:
        if (
            item.get("itemType") != "attachment"
            and item.get("title")
            and item.get("title") != '"测试文献"'
            and not item.get("title", "").endswith("(1)")
        ):
            valid_items.append(item)

    valid_items.sort(key=lambda x: x.get("dateAdded", ""), reverse=True)
    recent_items = valid_items[:max_items]

    print(f"将为最新的 {len(recent_items)} 篇文献创建 Obsidian 笔记")

    created_files: list[str] = []

    for index, item in enumerate(recent_items, 1):
        print(f"\n{index}. 创建笔记: {item.get('title', '')}")

        note_content = create_obsidian_note(item, template_path)
        if not note_content:
            print("   创建失败: 无法生成笔记内容")
            continue

        title = item.get("title", "")
        year_value = item.get("date", "")
        year_match = re.search(r"\b(19|20)\d{2}\b", year_value)
        year_str = year_match.group() if year_match else ""

        creators = item.get("creators", [])
        main_author = "未知"
        if creators and creators[0].get("name"):
            main_author = creators[0]["name"]

        filename = f"{index:02d}-{year_str}-{main_author}-{title}.md"
        filename = sanitize_filename(filename)
        file_path = os.path.join(output_dir, filename)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(note_content)
            print(f"   创建成功: {filename}")
            created_files.append(file_path)
        except Exception as exc:  # pragma: no cover - I/O
            print(f"   创建失败: {exc}")

    index_content = (
        "# 最新文献笔记索引\n"
        f"**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"**文献数量**: {len(created_files)}\n\n"
        "## 文献列表\n\n"
    )

    for index, file_path in enumerate(created_files, 1):
        filename = os.path.basename(file_path)
        title_part = filename.replace(".md", "").split("-", 3)[-1]
        index_content += f"{index}. [[{filename}|{title_part}]]\n"

    index_file = os.path.join(output_dir, "最新文献笔记索引.md")
    try:
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(index_content)
        print(f"\n索引文件已创建: {index_file}")
    except Exception as exc:  # pragma: no cover - I/O
        print(f"创建索引文件失败: {exc}")

    print("\n=== 任务完成 ===")
    print(f"成功创建 {len(created_files)} 个文献笔记")
    print(f"笔记保存于: {output_dir}")
    print(f"索引文件: {index_file}")


def main() -> None:
    """命令行入口：基于默认路径生成最新文献笔记。"""
    print("=== 创建 Obsidian 文献笔记 ===")

    items_file = r"E:\仓库\毕业论文\zotero_items.json"
    template_path = (
        r"E:\仓库\毕业论文\obsidian\04-工具模板\文献笔记模板\文献笔记模板.md"
    )
    output_dir = (
        r"E:\仓库\毕业论文\obsidian\02-文献管理\文献笔记\核心文献"
    )

    generate_latest_notes(items_file, template_path, output_dir, max_items=5)


if __name__ == "__main__":  # pragma: no cover - 脚本入口
    main()

