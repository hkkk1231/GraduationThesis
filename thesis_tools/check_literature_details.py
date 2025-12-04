#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查文献详情与潜在外文内容的辅助脚本逻辑。

原始版本位于仓库根目录 `check_literature_details.py`，主要用于：
- 基于 `zotero_items.json` 做中英文文献分布与最近文献统计；
- 给出下一步人工整理/阅读建议。

出于目录职责清晰的考虑，核心实现被移动到 `thesis_tools` 包内，
供 Codex CLI 与 `scripts/check_literature_details.py` 复用。

当前实现已改为通过 `thesis_tools.paths.ZOTERO_ITEMS_FILE`
（即 `report/zotero_items.json`）加载数据，避免根目录堆积 JSON。
如需进一步配置化，可以改由 `config/` 与 CLI 参数驱动。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from .paths import ZOTERO_ITEMS_FILE


ITEMS_FILE = ZOTERO_ITEMS_FILE


def load_items() -> List[Dict[str, Any]]:
    """从默认路径加载 Zotero 条目列表。"""
    try:
        with open(ITEMS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"未找到 Zotero 数据文件: {ITEMS_FILE}")
        return []
    except Exception as exc:
        print(f"读取 {ITEMS_FILE} 时出错: {exc}")
        return []


def analyze_all_literature() -> Dict[str, Any] | None:
    """占位函数：复用原根目录脚本中的分析逻辑。

    具体实现仍保留在原脚本中，在完全迁移前，这里仅作为
    Codex CLI 调用的统一入口占位符，避免接口变更。
    """
    print(
        "analyze_all_literature() 的完整实现仍在迁移过程中，"
        "当前仅保留占位入口以保证导入稳定。"
    )
    items = load_items()
    if not items:
        return None

    return {
        "total_items": len(items),
        "chinese_literature": 0,
        "potential_foreign": 0,
        "recent_items": items[:10],
    }


def suggest_next_steps(analysis_result: Dict[str, Any] | None) -> None:
    """占位函数：根据分析结果给出后续建议。"""
    if analysis_result is None:
        print("没有可用的分析结果，无法给出具体建议。")
        return

    total = analysis_result.get("total_items", 0)
    print("\n=== 建议和下一步操作（占位实现） ===")
    print(f"当前总文献条目数：{total}")
    print("建议：使用 `thesis ingest` + `thesis analyze` 获取更详细的结构化分析。")


__all__ = ["ITEMS_FILE", "load_items", "analyze_all_literature", "suggest_next_steps"]
