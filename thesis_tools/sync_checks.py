#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同步检查与健康度检测工具。

本模块抽取自 `test_zotero_api.py` 和 `test_obsidian_zotero_sync.py`，
用于集中管理 Zotero API 与 Obsidian 集成的可复用检查逻辑。
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import json
import sqlite3

import requests


@dataclass
class SyncCheckResult:
    """简单的同步检查结果结构。"""

    name: str
    ok: bool
    checked_at: datetime
    message: str | None = None


def summarize_results(results: List[SyncCheckResult]) -> bool:
    """汇总多个检查结果并返回整体是否通过。"""
    all_ok = all(r.ok for r in results)
    for result in results:
        status = "OK" if result.ok else "FAILED"
        extra = f" - {result.message}" if result.message else ""
        print(f"[{status}] {result.name}{extra}")
    return all_ok


# ---------------------------------------------------------------------------
# Zotero API 检查（抽取自 test_zotero_api.py）
# ---------------------------------------------------------------------------


def check_zotero_api_key(
    api_key: str,
    base_url: str = "https://api.zotero.org",
) -> SyncCheckResult:
    """测试 Zotero API 密钥是否有效。"""
    print("\n1. 测试API密钥...")
    headers = {"Zotero-API-Key": api_key}

    try:
        response = requests.get(f"{base_url}/keys/current", headers=headers, timeout=30)
        status = response.status_code
        print(f"状态码: {status}")

        ok = status == 200
        message = None
        if ok:
            user_info: Dict[str, Any] = response.json()
            print(f"用户信息: {user_info}")
            print(f"用户ID: {user_info.get('user', {}).get('id', '未知')}")
        else:
            message = response.text
            print(f"错误响应: {response.text}")

        return SyncCheckResult(
            name="zotero_api_key",
            ok=ok,
            checked_at=datetime.now(),
            message=message,
        )
    except Exception as exc:  # pragma: no cover - 网络 I/O
        print(f"API密钥测试失败: {exc}")
        return SyncCheckResult(
            name="zotero_api_key",
            ok=False,
            checked_at=datetime.now(),
            message=str(exc),
        )


def check_zotero_library_access(
    api_key: str,
    library_id: str,
    base_url: str = "https://api.zotero.org",
) -> SyncCheckResult:
    """测试库信息是否可访问。"""
    print(f"\n2. 测试库信息(ID: {library_id})...")
    headers = {"Zotero-API-Key": api_key}

    try:
        response = requests.get(
            f"{base_url}/users/{library_id}/collections", headers=headers, timeout=30
        )
        status = response.status_code
        print(f"状态码: {status}")

        ok = status == 200
        message = None
        if ok:
            collections = response.json()
            print(f"集合数量: {len(collections)}")
        else:
            message = response.text
            print(f"错误响应: {response.text}")

        return SyncCheckResult(
            name="zotero_library",
            ok=ok,
            checked_at=datetime.now(),
            message=message,
        )
    except Exception as exc:  # pragma: no cover - 网络 I/O
        print(f"库信息测试失败: {exc}")
        return SyncCheckResult(
            name="zotero_library",
            ok=False,
            checked_at=datetime.now(),
            message=str(exc),
        )


def check_zotero_items_fetch(
    api_key: str,
    library_id: str,
    base_url: str = "https://api.zotero.org",
    limit: int = 5,
) -> SyncCheckResult:
    """测试文献条目获取是否正常。"""
    print("\n3. 测试文献获取...")
    headers = {"Zotero-API-Key": api_key}

    try:
        response = requests.get(
            f"{base_url}/users/{library_id}/items?format=json&limit={limit}",
            headers=headers,
            timeout=30,
        )
        status = response.status_code
        print(f"状态码: {status}")

        ok = status == 200
        message = None
        if ok:
            items = response.json()
            print(f"获取到 {len(items)} 个文献")
            if items:
                first_item = items[0]
                data = first_item.get("data", {})
                print(f"第一个文献标题: {data.get('title', '未知')}")
        else:
            message = response.text
            print(f"错误响应: {response.text}")

        return SyncCheckResult(
            name="zotero_items_fetch",
            ok=ok,
            checked_at=datetime.now(),
            message=message,
        )
    except Exception as exc:  # pragma: no cover - 网络 I/O
        print(f"文献获取测试失败: {exc}")
        return SyncCheckResult(
            name="zotero_items_fetch",
            ok=False,
            checked_at=datetime.now(),
            message=str(exc),
        )


def run_zotero_api_checks(
    api_key: str,
    library_id: str,
    base_url: str = "https://api.zotero.org",
) -> List[SyncCheckResult]:
    """执行三项 Zotero API 检查并返回结果列表。"""
    print("=== 测试Zotero API连接 ===")
    results = [
        check_zotero_api_key(api_key=api_key, base_url=base_url),
        check_zotero_library_access(
            api_key=api_key, library_id=library_id, base_url=base_url
        ),
        check_zotero_items_fetch(
            api_key=api_key, library_id=library_id, base_url=base_url
        ),
    ]
    return results


# ---------------------------------------------------------------------------
# Obsidian + Zotero 集成检查（抽取自 test_obsidian_zotero_sync.py）
# ---------------------------------------------------------------------------


def check_zotero_sqlite() -> SyncCheckResult:
    """测试 Zotero 本地数据库连接。"""
    print("=== 测试Zotero数据库连接 ===")

    zotero_path = Path.home() / "Zotero" / "zotero.sqlite"
    if not zotero_path.exists():
        print("✗ 未找到Zotero数据库")
        return SyncCheckResult(
            name="zotero_sqlite",
            ok=False,
            checked_at=datetime.now(),
            message=f"not found: {zotero_path}",
        )

    try:
        conn = sqlite3.connect(str(zotero_path))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM items")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"✓ Zotero数据库连接成功，共有 {count} 个条目")
        return SyncCheckResult(
            name="zotero_sqlite",
            ok=True,
            checked_at=datetime.now(),
            message=f"items={count}",
        )
    except Exception as exc:  # pragma: no cover - I/O
        print(f"✗ Zotero数据库连接失败: {exc}")
        return SyncCheckResult(
            name="zotero_sqlite",
            ok=False,
            checked_at=datetime.now(),
            message=str(exc),
        )


def check_zotero_sqlite() -> SyncCheckResult:
    """测试 Zotero 本地数据库连接（覆盖旧版本以避免控制台编码问题）。"""
    print("=== 测试Zotero数据库连接 ===")

    zotero_path = Path.home() / "Zotero" / "zotero.sqlite"
    if not zotero_path.exists():
        print("Zotero数据库文件不存在")
        return SyncCheckResult(
            name="zotero_sqlite",
            ok=False,
            checked_at=datetime.now(),
            message=f"not found: {zotero_path}",
        )

    try:
        conn = sqlite3.connect(str(zotero_path))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM items")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"Zotero数据库连接成功，共有 {count} 个条目")
        return SyncCheckResult(
            name="zotero_sqlite",
            ok=True,
            checked_at=datetime.now(),
            message=f"items={count}",
        )
    except Exception as exc:  # pragma: no cover - I/O
        print(f"Zotero数据库连接失败: {exc}")
        return SyncCheckResult(
            name="zotero_sqlite",
            ok=False,
            checked_at=datetime.now(),
            message=str(exc),
        )


def check_obsidian_structure(base_path: Path) -> SyncCheckResult:
    """测试 Obsidian 目录结构。"""
    print("\n=== 测试Obsidian目录结构 ===")

    required_dirs = [
        "文献笔记",
        "PDF阅读",
        "研究项目",
        "核心概念",
        "理论框架",
        "模板",
        "引用管理",
    ]

    all_exist = True
    missing: List[str] = []

    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists():
            print(f"✓ {dir_name} 目录存在")
        else:
            print(f"✗ {dir_name} 目录不存在")
            all_exist = False
            missing.append(str(dir_path))

    return SyncCheckResult(
        name="obsidian_structure",
        ok=all_exist,
        checked_at=datetime.now(),
        message=None if all_exist else f"missing: {', '.join(missing)}",
    )


def check_obsidian_templates(template_paths: List[Path]) -> SyncCheckResult:
    """测试 Obsidian 模板文件是否存在。"""
    print("\n=== 测试模板文件 ===")

    all_exist = True
    missing: List[str] = []

    for template_path in template_paths:
        if template_path.exists():
            print(f"✓ {template_path.name} 模板存在")
        else:
            print(f"✗ {template_path.name} 模板不存在")
            all_exist = False
            missing.append(str(template_path))

    return SyncCheckResult(
        name="obsidian_templates",
        ok=all_exist,
        checked_at=datetime.now(),
        message=None if all_exist else f"missing: {', '.join(missing)}",
    )


def check_pdf_reading_folder(pdf_folder: Path) -> SyncCheckResult:
    """测试 PDF 阅读文件夹。"""
    print("\n=== 测试PDF阅读文件夹 ===")

    if pdf_folder.exists():
        files = list(pdf_folder.glob("*"))
        print(f"✓ PDF阅读文件夹存在: {pdf_folder}")
        print(f"  当前包含 {len(files)} 个文件")
        return SyncCheckResult(
            name="pdf_reading_folder",
            ok=True,
            checked_at=datetime.now(),
            message=f"files={len(files)}",
        )
    print(f"✗ PDF阅读文件夹不存在: {pdf_folder}")
    return SyncCheckResult(
        name="pdf_reading_folder",
        ok=False,
        checked_at=datetime.now(),
        message=f"not found: {pdf_folder}",
    )


def create_obsidian_test_note(notes_dir: Path) -> SyncCheckResult:
    """在 Obsidian 文献笔记目录中创建一个测试笔记。"""
    print("\n=== 创建测试笔记 ===")

    zotero_path = Path.home() / "Zotero" / "zotero.sqlite"

    try:
        conn = sqlite3.connect(str(zotero_path))
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT i.key, i.dateAdded, d.title, d.abstractNote
            FROM items i
            JOIN itemData d ON i.itemID = d.itemID
            WHERE i.itemTypeID = 28
            LIMIT 1
        """
        )
        result = cursor.fetchone()
        conn.close()

        if not result:
            print("✗ 未找到可用于测试的文献")
            return SyncCheckResult(
                name="obsidian_test_note",
                ok=False,
                checked_at=datetime.now(),
                message="no suitable item found in Zotero",
            )

        key, date_added, title, abstract = result
        notes_dir.mkdir(parents=True, exist_ok=True)

        note_content = f"""# {title}

**Zotero Key**: {key}
**添加日期**: {date_added}

## 摘要
{abstract}

## 测试笔记
这是一个测试笔记，用于验证Obsidian与Zotero的集成功能。

## 同步测试
- [ ] Zotero中的注释能否同步到Obsidian
- [ ] Obsidian中的链接能否跳转到Zotero
- [ ] 文献元数据是否正确显示

## 标签
#测试笔记 #同步测试

---
*创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*测试来源: Zotero Integration*
"""

        note_path = notes_dir / f"测试_{key}.md"
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(note_content)

        print(f"✓ 测试笔记已创建: {note_path}")
        return SyncCheckResult(
            name="obsidian_test_note",
            ok=True,
            checked_at=datetime.now(),
            message=str(note_path),
        )
    except Exception as exc:  # pragma: no cover - I/O
        print(f"✗ 创建测试笔记失败: {exc}")
        return SyncCheckResult(
            name="obsidian_test_note",
            ok=False,
            checked_at=datetime.now(),
            message=str(exc),
        )


def check_obsidian_structure(base_obsidian_path: Path) -> SyncCheckResult:
    """测试 Obsidian 目录结构（覆盖旧版本以避免控制台编码问题）。"""
    print("\n=== 测试Obsidian目录结构 ===")

    required_dirs = [
        "文献笔记",
        "PDF阅读",
        "研究项目",
        "核心概念",
        "理论框架",
        "模板",
        "引用管理",
    ]

    all_exist = True
    missing: List[str] = []

    for dir_name in required_dirs:
        dir_path = base_obsidian_path / dir_name
        if dir_path.exists():
            print(f"[OK] {dir_name} 目录存在")
        else:
            print(f"[MISSING] {dir_name} 目录不存在")
            all_exist = False
            missing.append(str(dir_path))

    return SyncCheckResult(
        name="obsidian_structure",
        ok=all_exist,
        checked_at=datetime.now(),
        message=None if all_exist else f"missing: {', '.join(missing)}",
    )


def check_obsidian_templates(template_paths: List[Path]) -> SyncCheckResult:
    """测试 Obsidian 模板文件是否存在（覆盖旧版本）。"""
    print("\n=== 测试模板文件 ===")

    all_exist = True
    missing: List[str] = []

    for template_path in template_paths:
        if template_path.exists():
            print(f"[OK] 模板存在: {template_path.name}")
        else:
            print(f"[MISSING] 模板不存在: {template_path.name}")
            all_exist = False
            missing.append(str(template_path))

    return SyncCheckResult(
        name="obsidian_templates",
        ok=all_exist,
        checked_at=datetime.now(),
        message=None if all_exist else f"missing: {', '.join(missing)}",
    )


def check_pdf_reading_folder(pdf_folder: Path) -> SyncCheckResult:
    """测试 PDF 阅读文件夹（覆盖旧版本）。"""
    print("\n=== 测试PDF阅读文件夹 ===")

    if pdf_folder.exists():
        files = list(pdf_folder.glob("*"))
        print(f"[OK] PDF阅读文件夹存在: {pdf_folder}")
        print(f"  当前包含 {len(files)} 个文件")
        return SyncCheckResult(
            name="pdf_reading_folder",
            ok=True,
            checked_at=datetime.now(),
            message=f"files={len(files)}",
        )
    print(f"[MISSING] PDF阅读文件夹不存在: {pdf_folder}")
    return SyncCheckResult(
        name="pdf_reading_folder",
        ok=False,
        checked_at=datetime.now(),
        message=f"not found: {pdf_folder}",
    )


def create_obsidian_test_note(notes_dir: Path) -> SyncCheckResult:
    """在 Obsidian 文献笔记目录中创建一个测试笔记（覆盖旧版本）。"""
    print("\n=== 创建测试笔记 ===")

    zotero_path = Path.home() / "Zotero" / "zotero.sqlite"

    try:
        conn = sqlite3.connect(str(zotero_path))
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT i.key, i.dateAdded, d.title, d.abstractNote
            FROM items i
            JOIN itemData d ON i.itemID = d.itemID
            WHERE i.itemTypeID = 28
            LIMIT 1
        """
        )
        result = cursor.fetchone()
        conn.close()

        if not result:
            print("未找到可用于测试的文献")
            return SyncCheckResult(
                name="obsidian_test_note",
                ok=False,
                checked_at=datetime.now(),
                message="no suitable item found in Zotero",
            )

        key, date_added, title, abstract = result
        notes_dir.mkdir(parents=True, exist_ok=True)

        note_content = f"""# {title}

**Zotero Key**: {key}
**添加日期**: {date_added}

## 摘要
{abstract}

## 测试笔记
这是一个测试笔记，用于验证Obsidian与Zotero的集成功能。

## 同步测试
- [ ] Zotero中的注释能否同步到Obsidian
- [ ] Obsidian中的链接能否跳转到Zotero
- [ ] 文献元数据是否正确显示

## 标签
#测试笔记 #同步测试

---
*创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*测试来源: Zotero Integration*
"""

        note_path = notes_dir / f"测试_{key}.md"
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(note_content)

        print(f"[OK] 测试笔记已创建: {note_path}")
        return SyncCheckResult(
            name="obsidian_test_note",
            ok=True,
            checked_at=datetime.now(),
            message=str(note_path),
        )
    except Exception as exc:  # pragma: no cover - I/O
        print(f"[FAILED] 创建测试笔记失败: {exc}")
        return SyncCheckResult(
            name="obsidian_test_note",
            ok=False,
            checked_at=datetime.now(),
            message=str(exc),
        )


def run_obsidian_zotero_sync_checks(
    base_obsidian_path: Path,
) -> Tuple[Dict[str, bool], Dict[str, Any]]:
    """执行 Obsidian + Zotero 集成相关检查并返回结果数据。"""
    results: Dict[str, bool] = {}
    details: Dict[str, Any] = {}

    sqlite_result = check_zotero_sqlite()
    results["zotero_connection"] = sqlite_result.ok
    details["zotero_connection"] = sqlite_result.message

    structure_result = check_obsidian_structure(base_obsidian_path)
    results["obsidian_structure"] = structure_result.ok
    details["obsidian_structure"] = structure_result.message

    template_paths = [
        base_obsidian_path / "模板" / "文献笔记模板.md",
        base_obsidian_path / "模板" / "研究笔记模板.md",
    ]
    templates_result = check_obsidian_templates(template_paths)
    results["templates"] = templates_result.ok
    details["templates"] = templates_result.message

    pdf_result = check_pdf_reading_folder(base_obsidian_path / "PDF阅读")
    results["pdf_folder"] = pdf_result.ok
    details["pdf_folder"] = pdf_result.message

    test_note_result = create_obsidian_test_note(base_obsidian_path / "文献笔记")
    results["test_note"] = test_note_result.ok
    details["test_note"] = test_note_result.message

    return results, details
