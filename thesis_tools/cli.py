#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一毕业论文项目的命令行入口（thesis CLI）。

目标：
- 提供统一的命令行界面：`python -m thesis_tools.cli <subcommand>`
- 将现有脚本能力（Zotero 拉取、分析、Obsidian 导出、同步检查）收敛到一个入口
- 为后续测试体系与 MCP 集成提供稳定的调用面
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Sequence

from . import obsidian_export, schemas, sync_checks, zotero_analysis, zotero_ingest


ROOT_DIR = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT_DIR / "config"


def _load_config() -> dict[str, Any]:
    """加载 `config/zotero_obsidian_config.json`，不存在或解析失败时返回空字典。"""
    config_path = CONFIG_DIR / "zotero_obsidian_config.json"
    if not config_path.exists():
        return {}

    try:
        with open(config_path, "r", encoding="utf-8") as config_file:
            return json.load(config_file)
    except Exception:
        # 配置解析失败时不抛出异常，避免阻塞其他子命令
        return {}


def _get_obsidian_vault_path(config: dict[str, Any]) -> Path | None:
    """根据环境变量或配置文件推断 Obsidian vault 路径。"""
    vault_path_str = os.environ.get("THESIS_OBSIDIAN_VAULT") or config.get(
        "obsidian_vault_path"
    )
    if not vault_path_str:
        return None
    return Path(vault_path_str)


def _load_json_if_exists(path: Path) -> Any | None:
    """若 JSON 文件存在则加载，否则返回 None。"""
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# 子命令实现
# ---------------------------------------------------------------------------


def handle_setup(args: argparse.Namespace) -> int:
    """`thesis setup`：检查基础配置与环境变量。"""
    print("=== 环境与配置自检 ===")

    config_data = _load_config()

    required_paths = [
        ("config/zotero-config.md", ROOT_DIR / "config" / "zotero-config.md"),
        ("config/obsidian-config.md", ROOT_DIR / "config" / "obsidian-config.md"),
        (
            "config/zotero_obsidian_config.json",
            ROOT_DIR / "config" / "zotero_obsidian_config.json",
        ),
        ("ilfow/mcp_config.json", ROOT_DIR / "ilfow" / "mcp_config.json"),
    ]

    all_ok = True
    for label, path in required_paths:
        if path.exists():
            print(f"[OK] {label}")
        else:
            print(f"[MISSING] {label}")
            all_ok = False

    api_key_set = bool(os.environ.get("ZOTERO_API_KEY"))
    library_id_set = bool(os.environ.get("ZOTERO_LIBRARY_ID"))
    print(f"ZOTERO_API_KEY: {'已设置' if api_key_set else '未设置'}")
    print(f"ZOTERO_LIBRARY_ID: {'已设置' if library_id_set else '未设置'}")

    vault_path = _get_obsidian_vault_path(config_data)
    if vault_path is not None:
        print(f"Obsidian vault 路径: {vault_path}")
    else:
        print(
            "Obsidian vault 路径: 未配置（请检查 config/zotero_obsidian_config.json 中的 obsidian_vault_path）"
        )

    report_dir = ROOT_DIR / "report"
    print(f"report 目录: {report_dir} {'(已存在)' if report_dir.exists() else '(将按需创建)'}")

    return 0 if all_ok else 1


def handle_ingest(args: argparse.Namespace) -> int:
    """`thesis ingest`：从 Zotero 拉取文献并写入 JSON。"""
    api_key = args.api_key or os.environ.get("ZOTERO_API_KEY") or zotero_ingest.API_KEY
    library_id = (
        args.library_id
        or os.environ.get("ZOTERO_LIBRARY_ID")
        or zotero_ingest.LIBRARY_ID
    )
    base_url = (
        args.base_url
        or os.environ.get("ZOTERO_BASE_URL")
        or zotero_ingest.BASE_URL
    )
    limit = args.limit

    print("=== Zotero 文献信息拉取（thesis ingest） ===")
    print(f"- Library ID: {library_id}")
    print(f"- Base URL: {base_url}")
    print(f"- Limit: {limit}")

    items = zotero_ingest.fetch_from_zotero(
        api_key=api_key,
        library_id=library_id,
        base_url=base_url,
        limit=limit,
    )
    if not items:
        print("未从 Zotero 获取到任何条目，请检查 API 配置或网络连接。")
        return 1

    processed_items = zotero_ingest.process_items(items)
    items_without_notes = zotero_ingest.split_items_by_notes(processed_items)
    zotero_ingest.print_summary(processed_items)
    zotero_ingest.save_items_to_files(processed_items, items_without_notes)

    return 0


def handle_analyze(args: argparse.Namespace) -> int:
    """`thesis analyze`：分析最近文献或外文文献。"""
    if args.foreign_only:
        print("=== 外文文献分析（thesis analyze --foreign-only） ===")
        zotero_analysis.analyze_foreign_literature()
    else:
        print("=== 最近文献分析（thesis analyze） ===")
        zotero_analysis.main()
    return 0


def handle_export_notes(args: argparse.Namespace) -> int:
    """`thesis export-notes`：基于最新文献生成 Obsidian 笔记。"""
    config_data = _load_config()
    vault_path = _get_obsidian_vault_path(config_data)
    if vault_path is None:
        print(
            "Obsidian vault 路径未配置，无法生成笔记。"
            "请在 config/zotero_obsidian_config.json 中设置 obsidian_vault_path，"
            "或通过环境变量 THESIS_OBSIDIAN_VAULT 覆盖。"
        )
        return 1

    items_file = args.items_file or str(ROOT_DIR / "zotero_items.json")
    template_folder_name = config_data.get("template_folder", "模板")
    notes_folder_name = config_data.get("literature_notes_folder", "文献笔记")

    template_path = vault_path / template_folder_name / args.template_name
    output_dir = vault_path / notes_folder_name

    print("=== 生成 Obsidian 文献笔记（thesis export-notes） ===")
    print(f"- items 文件: {items_file}")
    print(f"- 模板文件: {template_path}")
    print(f"- 输出目录: {output_dir}")

    obsidian_export.generate_latest_notes(
        items_file=items_file,
        template_path=str(template_path),
        output_dir=str(output_dir),
        max_items=args.max_items,
    )
    return 0


def handle_sync_check(args: argparse.Namespace) -> int:
    """`thesis sync-check`：检查 Zotero API 以及 Obsidian 目录结构。"""
    config_data = _load_config()
    overall_ok = True

    if args.skip_api:
        print(">>> 跳过 Zotero API 检查")
    else:
        api_key = args.api_key or os.environ.get("ZOTERO_API_KEY")
        library_id = args.library_id or os.environ.get("ZOTERO_LIBRARY_ID")
        base_url = (
            args.base_url
            or os.environ.get("ZOTERO_BASE_URL")
            or "https://api.zotero.org"
        )

        if not api_key or not library_id:
            print(
                "Zotero API 相关环境变量未设置，无法执行 API 检查。"
                "请设置 ZOTERO_API_KEY 和 ZOTERO_LIBRARY_ID。"
            )
            overall_ok = False
        else:
            api_results = sync_checks.run_zotero_api_checks(
                api_key=api_key,
                library_id=library_id,
                base_url=base_url,
            )
            api_all_ok = sync_checks.summarize_results(api_results)
            overall_ok = overall_ok and api_all_ok

    if args.skip_obsidian:
        print(">>> 跳过 Obsidian 结构检查")
    else:
        vault_path = _get_obsidian_vault_path(config_data)
        if vault_path is None:
            print(
                "Obsidian vault 路径未配置，无法执行结构检查。"
                "请在配置文件或环境变量中提供 obsidian_vault_path。"
            )
            overall_ok = False
        else:
            print(f"使用 Obsidian vault 路径: {vault_path}")
            results, _details = sync_checks.run_obsidian_zotero_sync_checks(vault_path)
            print("\n=== Obsidian / Zotero 同步检查结果 ===")
            for name, ok_flag in results.items():
                status_text = "OK" if ok_flag else "FAILED"
                print(f"[{status_text}] {name}")
            overall_ok = overall_ok and all(results.values())

    return 0 if overall_ok else 1


def handle_report(args: argparse.Namespace) -> int:
    """`thesis report`：汇总现有 JSON 报告并做基础结构校验。"""
    print("=== 汇总当前分析与同步报告（thesis report） ===")

    recent_path = ROOT_DIR / "recent_literature_analysis.json"
    foreign_path = ROOT_DIR / "foreign_literature_analysis.json"
    sync_report_path = ROOT_DIR / "report" / "obsidian_zotero_sync_report.json"

    recent_data = _load_json_if_exists(recent_path)
    if recent_data is None:
        print(f"[MISSING] {recent_path}")
    else:
        is_valid = schemas.validate_recent_literature_analysis(recent_data)
        status_text = "结构正常" if is_valid else "结构可能异常"
        total_recent = recent_data.get("total_recent_items")
        print(f"[OK] 发现 recent_literature_analysis.json（{status_text}）")
        if total_recent is not None:
            print(f"  最近文献条数: {total_recent}")

    foreign_data = _load_json_if_exists(foreign_path)
    if foreign_data is None:
        print(f"[MISSING] {foreign_path}")
    else:
        is_valid = schemas.validate_foreign_literature_analysis(foreign_data)
        status_text = "结构正常" if is_valid else "结构可能异常"
        total_foreign = foreign_data.get("total_foreign_literature")
        print(f"[OK] 发现 foreign_literature_analysis.json（{status_text}）")
        if total_foreign is not None:
            print(f"  外文文献总数: {total_foreign}")

    sync_data = _load_json_if_exists(sync_report_path)
    if sync_data is None:
        print(f"[MISSING] {sync_report_path}")
    else:
        print("[OK] 发现 obsidian_zotero_sync_report.json")
        result_flags = (
            sync_data.get("测试结果")
            or sync_data.get("results")
            or sync_data.get("æµ‹è¯•ç»“æžœ")
            or {}
        )
        if isinstance(result_flags, dict):
            failed_items = [
                name for name, ok_flag in result_flags.items() if not ok_flag
            ]
            if not failed_items:
                print("  同步检查全部通过。")
            else:
                print(f"  未通过的检查: {', '.join(failed_items)}")

    return 0


# ---------------------------------------------------------------------------
# 参数解析与入口
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    """构建 thesis CLI 的顶层解析器。"""
    parser = argparse.ArgumentParser(
        prog="thesis",
        description="毕业论文 Zotero-Obsidian 工具链统一 CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # setup
    setup_parser = subparsers.add_parser(
        "setup",
        help="检查配置文件与基础环境",
    )
    setup_parser.set_defaults(handler=handle_setup)

    # ingest
    ingest_parser = subparsers.add_parser(
        "ingest",
        help="从 Zotero 拉取文献并写入 JSON",
    )
    ingest_parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="最大拉取文献条数（默认 100）",
    )
    ingest_parser.add_argument(
        "--api-key",
        dest="api_key",
        help="Zotero API 密钥（默认读取环境变量 ZOTERO_API_KEY）",
    )
    ingest_parser.add_argument(
        "--library-id",
        dest="library_id",
        help="Zotero Library ID（默认读取环境变量 ZOTERO_LIBRARY_ID）",
    )
    ingest_parser.add_argument(
        "--base-url",
        dest="base_url",
        default=None,
        help="Zotero API 基础地址（默认 https://api.zotero.org）",
    )
    ingest_parser.set_defaults(handler=handle_ingest)

    # analyze
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="分析最近文献或外文文献",
    )
    analyze_parser.add_argument(
        "--foreign-only",
        action="store_true",
        help="仅生成外文文献分析报告",
    )
    analyze_parser.set_defaults(handler=handle_analyze)

    # export-notes
    export_parser = subparsers.add_parser(
        "export-notes",
        help="基于最新文献生成 Obsidian 文献笔记",
    )
    export_parser.add_argument(
        "--items-file",
        dest="items_file",
        help="Zotero items JSON 路径（默认项目根目录 zotero_items.json）",
    )
    export_parser.add_argument(
        "--max-items",
        dest="max_items",
        type=int,
        default=5,
        help="生成笔记的最大文献数量（默认 5）",
    )
    export_parser.add_argument(
        "--template-name",
        dest="template_name",
        default="文献笔记模板.md",
        help="Obsidian 模板文件名（默认 文献笔记模板.md）",
    )
    export_parser.set_defaults(handler=handle_export_notes)

    # sync-check
    sync_parser = subparsers.add_parser(
        "sync-check",
        help="检查 Zotero API 与 Obsidian 目录结构",
    )
    sync_parser.add_argument(
        "--skip-api",
        action="store_true",
        help="跳过 Zotero API 检查",
    )
    sync_parser.add_argument(
        "--skip-obsidian",
        action="store_true",
        help="跳过 Obsidian 结构检查",
    )
    sync_parser.add_argument(
        "--api-key",
        dest="api_key",
        help="Zotero API 密钥（默认读取环境变量 ZOTERO_API_KEY）",
    )
    sync_parser.add_argument(
        "--library-id",
        dest="library_id",
        help="Zotero Library ID（默认读取环境变量 ZOTERO_LIBRARY_ID）",
    )
    sync_parser.add_argument(
        "--base-url",
        dest="base_url",
        default=None,
        help="Zotero API 基础地址（默认 https://api.zotero.org）",
    )
    sync_parser.set_defaults(handler=handle_sync_check)

    # report
    report_parser = subparsers.add_parser(
        "report",
        help="汇总现有 JSON 报告并做基础校验",
    )
    report_parser.set_defaults(handler=handle_report)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """命令行入口：解析参数并分发到各子命令。"""
    parser = build_parser()
    parsed_args = parser.parse_args(list(argv) if argv is not None else None)
    handler = getattr(parsed_args, "handler", None)
    if handler is None:
        parser.print_help()
        return 1
    return handler(parsed_args)


if __name__ == "__main__":  # pragma: no cover - 脚本入口
    raise SystemExit(main())

