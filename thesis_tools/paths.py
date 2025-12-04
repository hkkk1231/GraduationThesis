#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一管理毕业论文项目中的关键路径。

核心目标：
- 为 CLI 与各功能模块提供一致的 ROOT_DIR / REPORT_DIR 等路径常量；
- 约定 Zotero 相关 JSON 默认位于 `report/` 目录，而不是仓库根目录；
- 为后续逐步去除硬编码绝对路径打基础。
"""

from __future__ import annotations

from pathlib import Path


# 项目根目录：thesis_tools 包的上一级
ROOT_DIR: Path = Path(__file__).resolve().parents[1]

# 配置、数据与集成相关目录
CONFIG_DIR: Path = ROOT_DIR / "config"
REPORT_DIR: Path = ROOT_DIR / "report"
OBSIDIAN_DIR: Path = ROOT_DIR / "obsidian"
ZOTERO_DIR: Path = ROOT_DIR / "zotero"

# Zotero JSON 与分析结果的默认文件位置（统一迁移到 report/）
ZOTERO_ITEMS_FILE: Path = REPORT_DIR / "zotero_items.json"
ZOTERO_ITEMS_WITHOUT_NOTES_FILE: Path = REPORT_DIR / "zotero_items_without_notes.json"
RECENT_LITERATURE_ANALYSIS_FILE: Path = REPORT_DIR / "recent_literature_analysis.json"
FOREIGN_LITERATURE_ANALYSIS_FILE: Path = REPORT_DIR / "foreign_literature_analysis.json"


__all__ = [
    "ROOT_DIR",
    "CONFIG_DIR",
    "REPORT_DIR",
    "OBSIDIAN_DIR",
    "ZOTERO_DIR",
    "ZOTERO_ITEMS_FILE",
    "ZOTERO_ITEMS_WITHOUT_NOTES_FILE",
    "RECENT_LITERATURE_ANALYSIS_FILE",
    "FOREIGN_LITERATURE_ANALYSIS_FILE",
]

