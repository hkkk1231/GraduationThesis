#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接操作Zotero SQLite数据库添加笔记
"""

import sqlite3
import os
import json
from pathlib import Path
from datetime import datetime

def find_zotero_database():
    """查找Zotero数据库文件"""
    possible_paths = [
        Path.home() / "Zotero" / "zotero.sqlite",
        Path.home() / "AppData" / "Roaming" / "Zotero" / "Zotero" / "Profiles" / "zotero.sqlite",
        Path("C:") / "Users" / os.getenv("USERNAME") / "Zotero" / "zotero.sqlite"
    ]
    
    for path in possible_paths:
        if path.exists():
            return str(path)
    
    return None

def add_note_to_sqlite():
    """直接向SQLite数据库添加笔记"""
    db_path = find_zotero_database()
    
    if not db_path:
        print("✗ 未找到Zotero数据库文件")
        return False
    
    print(f"找到数据库: {db_path}")
    
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查找目标文献条目
        parent_key = "LA2VSHG9"
        cursor.execute("SELECT itemID FROM items WHERE key = ?", (parent_key,))
        parent_result = cursor.fetchone()
        
        if not parent_result:
            print(f"✗ 未找到父文献条目: {parent_key}")
            return False
        
        parent_id = parent_result[0]
        print(f"找到父文献条目ID: {parent_id}")
        
        # 生成新的笔记key
        import random
        import string
        note_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        # 创建笔记内容
        note_content = f"""<h1>基于教学评一体化的小学英语阅读教学中AI技术的运用</h1>
<h2>文献信息</h2>
<ul>
<li><strong>标题</strong>: 基于教学评一体化的小学英语阅读教学中AI技术的运用</li>
<li><strong>作者</strong>: 吴雪云</li>
<li><strong>创建时间</strong>: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
</ul>
<h2>研究要点</h2>
<h3>核心概念</h3>
<ul>
<li><strong>教学评一体化</strong>: 将教学、学习、评价三个环节有机结合</li>
<li><strong>AI技术在英语阅读教学中的应用</strong>: 智能化辅助教学工具的使用</li>
</ul>
<h3>主要观点</h3>
<ol>
<li>AI技术可以实现个性化阅读推荐</li>
<li>智能评估系统能够实时反馈学习效果</li>
<li>数据驱动的教学决策支持</li>
</ol>
<h3>实践应用</h3>
<ul>
<li>智能阅读平台的使用</li>
<li>语音识别技术在口语练习中的应用</li>
<li>学习分析系统的构建</li>
</ul>
<h3>研究意义</h3>
<ul>
<li>提高小学英语阅读教学效率</li>
<li>促进学生个性化学习发展</li>
<li>推动教育信息化进程</li>
</ul>
<h2>思考与启发</h2>
<ul>
<li>如何平衡技术工具与传统教学方法</li>
<li>AI技术在教育中的伦理考量</li>
<li>教师专业能力的新要求</li>
</ul>
<h2>相关研究</h2>
<ul>
<li>人工智能支持下的小学数学"教学评"一体化课堂实践</li>
<li>AI技术在小学英语课堂教学中的应用</li>
<li>生成式人工智能在学科教学中的应用研究</li>
</ul>"""
        
        # 插入笔记条目
        cursor.execute("""
            INSERT INTO items (itemID, libraryID, key, itemTypeID, dateAdded, dateModified, clientDateModified)
            VALUES (?, 1, ?, 1, datetime('now'), datetime('now'), datetime('now'))
        """, (None, note_key))
        
        # 获取新插入的itemID
        note_id = cursor.lastrowid
        print(f"创建笔记条目ID: {note_id}, Key: {note_key}")
        
        # 设置父子关系
        cursor.execute("""
            INSERT INTO itemNotes (itemID, parentItemID, note)
            VALUES (?, ?, ?)
        """, (note_id, parent_id, note_content))
        
        # 提交事务
        conn.commit()
        conn.close()
        
        print(f"✓ 笔记已成功添加到数据库")
        print(f"  笔记Key: {note_key}")
        print(f"  父文献Key: {parent_key}")
        print(f"  请重启Zotero以查看更改")
        
        return True
        
    except Exception as e:
        print(f"操作数据库时出错: {e}")
        return False

if __name__ == "__main__":
    print("=== 直接操作Zotero SQLite数据库添加笔记 ===")
    print("警告: 直接操作数据库有风险，请确保已备份Zotero数据库")
    print()
    
    add_note_to_sqlite()