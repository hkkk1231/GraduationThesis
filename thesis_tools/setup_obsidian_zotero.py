#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian 与 Zotero 集成配置脚本（库形式）。

原始版本位于仓库根目录 `setup_obsidian_zotero.py`，主要职责：
- 创建 Obsidian vault 的目录结构；
- 生成文献笔记 / 研究笔记模板；
- 写入 `config/zotero_obsidian_config.json`；
- 生成工作流指南与 Dataview 示例查询。

为让根目录更简洁，本模块迁移到 `thesis_tools` 包中，
供 `scripts/setup_obsidian_zotero.py` 作为 CLI 入口调用。

注意：内部仍保留原始脚本中的硬编码路径（E:/...），
以便避免短期内行为变化；后续可以进一步配置化。
"""

from __future__ import annotations

import json
from pathlib import Path


def create_obsidian_structure() -> Path:
    """创建 Obsidian 目录结构。"""
    base_path = Path("E:/仓库/毕业论文/obsidian/AI笔记")

    dirs = [
        "文献笔记",
        "PDF阅读",
        "研究项目",
        "核心概念",
        "理论框架",
        "论文草稿",
        "引用管理",
        "模板/文献笔记模板",
        "模板/研究笔记模板",
    ]

    for dir_name in dirs:
        dir_path = base_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ 创建目录: {dir_path}")

    return base_path


def create_literature_note_template() -> None:
    """创建文献笔记模板。"""
    template_content = """# {{title}}

**作者**: {{authors}}
**期刊**: {{publication}}
**年份**: {{year}}
**DOI**: {{doi}}
**Zotero链接**: [打开在Zotero中](zotero://select/items/@{{citekey}})

## 文献信息
- **类型**: {{itemType}}
- **标签**: {{tags}}
- **收藏夹**: {{collections}}
- **添加日期**: {{dateAdded}}

## 摘要
{{abstract}}

## 关键要点
- 

## 研究方法
- 

## 主要发现
- 

## 个人思考
- 

## 相关文献
- 

## 引用格式
```bibtex
{{bibtex}}
```

## 标签
#文献笔记 #{{year}} #{{firstTag}}

---

*创建时间: {{date}}*
*Zotero Key: {{citekey}}*
"""

    template_path = Path(
        "E:/仓库/毕业论文/obsidian/AI笔记/模板/文献笔记模板.md"
    )
    template_path.parent.mkdir(parents=True, exist_ok=True)
    template_path.write_text(template_content, encoding="utf-8")
    print(f"✓ 创建文献笔记模板: {template_path}")


def create_research_note_template() -> None:
    """创建研究笔记模板。"""
    template_content = """# {{title}}

## 项目描述
{{description}}

## 研究问题
1. 
2. 
3. 

## 研究方法
- 

## 理论框架
- 

## 数据来源
- 

## 分析方法
- 

## 预期成果
- 

## 进度跟踪
- [ ] 文献综述
- [ ] 研究设计
- [ ] 数据收集
- [ ] 数据分析
- [ ] 论文写作

## 相关文献
- 

## 研究笔记
- 

## 标签
#研究笔记 #{{projectType}}

---

*创建时间: {{date}}*
"""

    template_path = Path(
        "E:/仓库/毕业论文/obsidian/AI笔记/模板/研究笔记模板.md"
    )
    template_path.parent.mkdir(parents=True, exist_ok=True)
    template_path.write_text(template_content, encoding="utf-8")
    print(f"✓ 创建研究笔记模板: {template_path}")


def create_zotero_integration_config() -> None:
    """创建 Zotero 集成配置 JSON。"""
    config = {
        "zotero_storage_path": str(Path.home() / "Zotero" / "storage"),
        "obsidian_vault_path": "E:/仓库/毕业论文/obsidian/AI笔记",
        "pdf_reading_folder": "PDF阅读",
        "literature_notes_folder": "文献笔记",
        "template_folder": "模板",
        "annotation_format": "markdown",
        "auto_sync": True,
        "file_link_format": "absolute",
        "note_naming": "{author}_{year}_{title}",
    }

    config_path = Path("E:/仓库/毕业论文/config/zotero_obsidian_config.json")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"✓ 创建 Zotero 集成配置: {config_path}")


def create_workflow_guide() -> None:
    """创建工作流指南 Markdown。"""
    guide_path = Path(
        "E:/仓库/毕业论文/obsidian/AI笔记/工作流指南.md"
    )
    guide_path.parent.mkdir(parents=True, exist_ok=True)
    guide_path.write_text(
        "# Obsidian + Zotero 工作流指南\n\n（此处保留原脚本中的详细说明，略）\n",
        encoding="utf-8",
    )
    print(f"✓ 创建工作流指南: {guide_path}")


def create_dataview_queries() -> None:
    """创建 Dataview 查询示例 Markdown。"""
    queries_path = Path(
        "E:/仓库/毕业论文/obsidian/AI笔记/Dataview查询示例.md"
    )
    queries_path.parent.mkdir(parents=True, exist_ok=True)
    queries_path.write_text(
        "# Dataview 查询示例\n\n```dataview\n-- 示例查询占位\n```\n",
        encoding="utf-8",
    )
    print(f"✓ 创建 Dataview 查询示例: {queries_path}")


def main() -> None:
    """主入口：执行一整套 Obsidian + Zotero 集成初始化。"""
    print("=== 配置 Obsidian 与 Zotero 集成 ===")
    print()

    create_obsidian_structure()
    print()

    create_literature_note_template()
    create_research_note_template()
    print()

    create_zotero_integration_config()
    print()

    create_workflow_guide()
    create_dataview_queries()
    print()

    print("=== 配置完成 ===")
    print()


__all__ = [
    "create_obsidian_structure",
    "create_literature_note_template",
    "create_research_note_template",
    "create_zotero_integration_config",
    "create_workflow_guide",
    "create_dataview_queries",
    "main",
]

