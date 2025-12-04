#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行入口：测试 Obsidian 与 Zotero 的同步与目录结构。

原先实现位于根目录 `test_obsidian_zotero_sync.py`，现内联到本脚本，
直接调用 `thesis_tools.sync_checks.run_obsidian_zotero_sync_checks`，
并生成 `report/obsidian_zotero_sync_report.json`。
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from thesis_tools.sync_checks import run_obsidian_zotero_sync_checks  # type: ignore[import]
from thesis_tools.cli import _load_config, _get_obsidian_vault_path  # type: ignore[attr-defined]


def generate_sync_report() -> Dict[str, Any]:
    """生成同步测试报告并写入 report/ 目录。"""
    print("\n=== 生成同步报告 ===")

    config = _load_config()
    vault_path = _get_obsidian_vault_path(config)
    if vault_path is None:
        raise RuntimeError(
            "未能从 config/zotero_obsidian_config.json 或环境变量 "
            "推断出 Obsidian vault 路径。"
        )

    results, details = run_obsidian_zotero_sync_checks(vault_path)

    report: Dict[str, Any] = {
        "测试时间": datetime.now().isoformat(),
        "测试结果": results,
        "测试详情": details,
    }

    report_path = Path("report") / "obsidian_zotero_sync_report.json"
    report_path.parent.mkdir(exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"[OK] 同步报告已保存到 {report_path}")

    print("\n=== 测试结果汇总 ===")
    for name, ok in results.items():
        status = "通过" if ok else "失败"
        print(f"{name}: {status}")

    return report


def main() -> None:
    """执行一整套 Obsidian-Zotero 集成测试。"""
    print("Obsidian 与 Zotero 双向同步功能测试")
    print("=" * 50)

    report = generate_sync_report()
    all_passed = all(report["测试结果"].values())

    print("\n" + "=" * 50)
    if all_passed:
        print("所有测试通过，Obsidian 与 Zotero 集成配置看起来正常。")
    else:
        print("部分测试未通过，请检查上方输出与报告文件。")


if __name__ == "__main__":  # pragma: no cover
    main()

