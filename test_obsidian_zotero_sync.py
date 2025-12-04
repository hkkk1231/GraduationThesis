#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Obsidian 与 Zotero 双向同步功能。

核心检查逻辑已抽取到 ``thesis_tools.sync_checks`` 中，
本脚本负责组合这些检查并生成 JSON 报告。
"""

import json
from datetime import datetime
from pathlib import Path

from thesis_tools.sync_checks import run_obsidian_zotero_sync_checks


def generate_sync_report() -> dict:
    """生成同步测试报告并写入 report/ 目录。"""
    print("\n=== 生成同步报告 ===")

    base_obsidian_path = Path("E:/仓库/毕业论文/obsidian/AI笔记")

    results, details = run_obsidian_zotero_sync_checks(base_obsidian_path)

    report = {
        "测试时间": datetime.now().isoformat(),
        "测试结果": results,
        "测试详情": details,
    }

    report_path = Path("E:/仓库/毕业论文/report/obsidian_zotero_sync_report.json")
    report_path.parent.mkdir(exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"✓ 同步报告已保存: {report_path}")

    print("\n=== 测试结果汇总 ===")
    for name, ok in results.items():
        status = "✓ 通过" if ok else "✗ 失败"
        print(f"{name}: {status}")

    return report


def main() -> None:
    """主函数：执行同步测试。"""
    print("Obsidian 与 Zotero 双向同步功能测试")
    print("=" * 50)

    report = generate_sync_report()

    all_passed = all(report["测试结果"].values())

    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有测试通过！Obsidian 与 Zotero 集成配置成功")
        print("\n下一步：")
        print("1. 在 Zotero 中选择文献")
        print("2. 右键 → Manage Attachments → Send to Tablet")
        print("3. 检查 Obsidian 中是否自动生成笔记")
        print("4. 测试双向链接功能")
    else:
        print("⚠️ 部分测试失败，请检查配置")
        print("\n故障排除建议：")
        print("1. 确认 Zotero 正在运行，且本机数据库路径正确")
        print("2. 检查 Obsidian vault 路径与目录结构是否与脚本配置一致")
        print("3. 确认模板文件已创建（文献笔记模板、研究笔记模板）")
        print("4. 检查 PDF 阅读文件夹路径和权限")


if __name__ == "__main__":  # pragma: no cover - 脚本入口
    main()

