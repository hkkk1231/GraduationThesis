#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Obsidian与Zotero双向同步功能
"""

import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime

def test_zotero_connection():
    """测试Zotero数据库连接"""
    print("=== 测试Zotero数据库连接 ===")
    
    # 查找Zotero数据库路径
    zotero_path = Path.home() / "Zotero" / "zotero.sqlite"
    if not zotero_path.exists():
        print("✗ 未找到Zotero数据库")
        return False
    
    try:
        conn = sqlite3.connect(str(zotero_path))
        cursor = conn.cursor()
        
        # 测试查询
        cursor.execute("SELECT COUNT(*) FROM items")
        count = cursor.fetchone()[0]
        print(f"✓ Zotero数据库连接成功，共有 {count} 个条目")
        
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Zotero数据库连接失败: {e}")
        return False

def test_obsidian_structure():
    """测试Obsidian目录结构"""
    print("\n=== 测试Obsidian目录结构 ===")
    
    base_path = Path("E:/仓库/毕业论文/obsidian/AI笔记")
    required_dirs = [
        "文献笔记",
        "PDF阅读", 
        "研究项目",
        "核心概念",
        "理论框架",
        "模板",
        "引用管理"
    ]
    
    all_exist = True
    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists():
            print(f"✓ {dir_name} 目录存在")
        else:
            print(f"✗ {dir_name} 目录不存在")
            all_exist = False
    
    return all_exist

def test_templates():
    """测试模板文件"""
    print("\n=== 测试模板文件 ===")
    
    templates = [
        "E:/仓库/毕业论文/obsidian/AI笔记/模板/文献笔记模板.md",
        "E:/仓库/毕业论文/obsidian/AI笔记/模板/研究笔记模板.md"
    ]
    
    all_exist = True
    for template_path in templates:
        path = Path(template_path)
        if path.exists():
            print(f"✓ {path.name} 模板存在")
        else:
            print(f"✗ {path.name} 模板不存在")
            all_exist = False
    
    return all_exist

def create_test_note():
    """创建测试笔记"""
    print("\n=== 创建测试笔记 ===")
    
    # 获取一个Zotero文献作为测试
    zotero_path = Path.home() / "Zotero" / "zotero.sqlite"
    
    try:
        conn = sqlite3.connect(str(zotero_path))
        cursor = conn.cursor()
        
        # 获取第一个文献
        cursor.execute("""
            SELECT i.key, i.dateAdded, d.title, d.abstractNote 
            FROM items i 
            JOIN itemData d ON i.itemID = d.itemID 
            WHERE i.itemTypeID = 28 
            LIMIT 1
        """)
        
        result = cursor.fetchone()
        if result:
            key, date_added, title, abstract = result
            
            # 创建测试笔记
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
            
            note_path = Path("E:/仓库/毕业论文/obsidian/AI笔记/文献笔记") / f"测试_{key}.md"
            with open(note_path, 'w', encoding='utf-8') as f:
                f.write(note_content)
            
            print(f"✓ 测试笔记已创建: {note_path}")
            conn.close()
            return True
        else:
            print("✗ 未找到可用于测试的文献")
            conn.close()
            return False
            
    except Exception as e:
        print(f"✗ 创建测试笔记失败: {e}")
        return False

def test_pdf_reading_folder():
    """测试PDF阅读文件夹"""
    print("\n=== 测试PDF阅读文件夹 ===")
    
    pdf_folder = Path("E:/仓库/毕业论文/obsidian/AI笔记/PDF阅读")
    
    if pdf_folder.exists():
        print(f"✓ PDF阅读文件夹存在: {pdf_folder}")
        
        # 检查文件夹内容
        files = list(pdf_folder.glob("*"))
        print(f"  当前包含 {len(files)} 个文件")
        
        return True
    else:
        print(f"✗ PDF阅读文件夹不存在: {pdf_folder}")
        return False

def generate_sync_report():
    """生成同步报告"""
    print("\n=== 生成同步报告 ===")
    
    report = {
        "测试时间": datetime.now().isoformat(),
        "测试结果": {
            "zotero_connection": test_zotero_connection(),
            "obsidian_structure": test_obsidian_structure(),
            "templates": test_templates(),
            "pdf_folder": test_pdf_reading_folder(),
            "test_note": create_test_note()
        }
    }
    
    # 保存报告
    report_path = Path("E:/仓库/毕业论文/report/obsidian_zotero_sync_report.json")
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"✓ 同步报告已保存: {report_path}")
    
    # 显示测试结果
    print("\n=== 测试结果汇总 ===")
    for test_name, result in report["测试结果"].items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
    
    return report

def main():
    """主函数"""
    print("Obsidian与Zotero双向同步功能测试")
    print("=" * 50)
    
    report = generate_sync_report()
    
    # 判断整体状态
    all_passed = all(report["测试结果"].values())
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有测试通过！Obsidian与Zotero集成配置成功")
        print("\n下一步:")
        print("1. 在Zotero中选择文献")
        print("2. 右键 → Manage Attachments → Send to Tablet")
        print("3. 检查Obsidian中是否自动生成笔记")
        print("4. 测试双向链接功能")
    else:
        print("⚠️ 部分测试失败，请检查配置")
        print("\n故障排除:")
        print("1. 确认Zotero正在运行")
        print("2. 检查Zotfile插件配置")
        print("3. 验证Obsidian插件安装")
        print("4. 确认文件夹路径正确")

if __name__ == "__main__":
    main()