#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zotero 文献拉取与预处理模块。

等价于原先的 `get_zotero_items.py` 核心逻辑，但以模块形式提供，
方便被脚本入口和后续 CLI 复用。
"""

from __future__ import annotations

import json
import os
from typing import Any

import requests

from .models import Literature


API_KEY = "CIApUKos6l9E0GOaCBrILRrt"
LIBRARY_ID = "18982351"
BASE_URL = "https://api.zotero.org"

# 以当前包所在目录的上一级作为项目根目录，避免写死绝对路径。
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def fetch_from_zotero(
    api_key: str = API_KEY,
    library_id: str = LIBRARY_ID,
    base_url: str = BASE_URL,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """从 Zotero API 拉取原始条目列表。"""
    print("正在获取 Zotero 文献信息...")

    headers = {"Zotero-API-Key": api_key}
    url = f"{base_url}/users/{library_id}/items"
    params = {"format": "json", "limit": limit}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:  # pragma: no cover - I/O
        print(f"请求错误: {exc}")
        return []

    items = response.json()
    print(f"成功获取 {len(items)} 个文献条目")
    return items


def process_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """提取关键字段，生成统一结构的文献列表。"""
    processed_items: list[dict[str, Any]] = []

    for item in items:
        literature = Literature.from_zotero_api_item(item)
        processed_items.append(literature.to_zotero_item_dict())

    return processed_items


def split_items_by_notes(
    processed_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """筛选出没有任何笔记的文献条目。"""
    return [
        item
        for item in processed_items
        if not item.get("notes") and item.get("itemType") != "note"
    ]


def save_items_to_files(
    processed_items: list[dict[str, Any]],
    items_without_notes: list[dict[str, Any]],
    output_dir: str | None = None,
) -> None:
    """将处理后的文献信息写入 JSON 文件。"""
    base_dir = output_dir or ROOT_DIR
    os.makedirs(base_dir, exist_ok=True)

    all_items_path = os.path.join(base_dir, "zotero_items.json")
    without_notes_path = os.path.join(
        base_dir, "zotero_items_without_notes.json"
    )

    try:
        with open(all_items_path, "w", encoding="utf-8") as f:
            json.dump(processed_items, f, ensure_ascii=False, indent=2)

        with open(without_notes_path, "w", encoding="utf-8") as f:
            json.dump(items_without_notes, f, ensure_ascii=False, indent=2)
    except Exception as exc:  # pragma: no cover - I/O
        print(f"保存文件时出错: {exc}")
        return

    print("\n数据已保存到:")
    print(f"- {all_items_path}")
    print(f"- {without_notes_path}")


def print_summary(processed_items: list[dict[str, Any]]) -> None:
    """在控制台输出简要统计信息和无笔记文献列表。"""
    items_without_notes = split_items_by_notes(processed_items)

    print("\n=== 文献统计 ===")
    print(f"总文献数: {len(processed_items)}")
    with_notes = [item for item in processed_items if item.get("notes")]
    print(f"有笔记的文献数: {len(with_notes)}")
    print(f"无笔记的文献数: {len(items_without_notes)}")

    print("\n=== 无笔记文献列表 ===")
    for index, item in enumerate(items_without_notes, 1):
        title = item.get("title", "")
        print(f"\n{index}. {title}")

        authors: list[str] = []
        for creator in item.get("creators", []):
            if creator.get("lastName") and creator.get("firstName"):
                authors.append(f"{creator['lastName']} {creator['firstName']}")
            elif creator.get("name"):
                authors.append(creator["name"])

        print(f"   作者: {', '.join(authors) if authors else '未知'}")
        print(f"   年份: {item.get('date') or '未知'}")
        print(f"   期刊: {item.get('publicationTitle') or '未知'}")

        abstract = item.get("abstractNote") or ""
        if abstract:
            preview = abstract[:100] + "..." if len(abstract) > 100 else abstract
            print(f"   摘要: {preview}")
        else:
            print("   摘要: 无")

        print(f"   Key: {item.get('key', '')}")


def main() -> None:
    """命令行入口：拉取 Zotero 文献并输出统计与 JSON。"""
    print("=== Zotero 文献信息获取工具 ===")

    items = fetch_from_zotero()
    if not items:
        print("未获取到文献信息，请检查 API 配置")
        return

    processed_items = process_items(items)
    items_without_notes = split_items_by_notes(processed_items)
    print_summary(processed_items)
    save_items_to_files(processed_items, items_without_notes)


if __name__ == "__main__":  # pragma: no cover - 脚本入口
    main()

