#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在正确的父文献下创建笔记
"""

import sqlite3
import random
import string
from datetime import datetime
from pathlib import Path

def create_note_on_correct_parent():
    """在正确的父文献下创建笔记"""
    db_path = r"C:\Users\28480\Zotero\zotero.sqlite"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 使用正确的父文献Key
        parent_key = "57T8RALW"
        cursor.execute("SELECT itemID FROM items WHERE key = ?", (parent_key,))
        parent_result = cursor.fetchone()
        
        if not parent_result:
            print(f"未找到父文献: {parent_key}")
            return False
        
        parent_id = parent_result[0]
        print(f"在父文献 {parent_key} (ID: {parent_id}) 下创建笔记")
        
        # 生成新的笔记key
        note_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        # 创建正确的笔记内容
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
        
        # 创建正确的HTML结构
        formatted_note = f"""<div class="zotero-note znv1"><div data-schema-version="9">{note_content}</div></div>"""
        
        # 插入笔记条目
        cursor.execute("""
            INSERT INTO items (libraryID, key, itemTypeID, dateAdded, dateModified, clientDateModified)
            VALUES (1, ?, 28, datetime('now'), datetime('now'), datetime('now'))
        """, (note_key,))
        
        # 获取新插入的itemID
        note_id = cursor.lastrowid
        print(f"创建新笔记，ID: {note_id}, Key: {note_key}")
        
        # 设置父子关系和内容
        cursor.execute("""
            INSERT INTO itemNotes (itemID, parentItemID, note)
            VALUES (?, ?, ?)
        """, (note_id, parent_id, formatted_note))
        
        conn.commit()
        conn.close()
        
        print(f"✓ 新笔记已创建在正确的父文献下")
        print(f"  笔记Key: {note_key}")
        print(f"  父文献Key: {parent_key}")
        print("  请重启Zotero查看修复后的笔记")
        
        return True
        
    except Exception as e:
        print(f"创建新笔记时出错: {e}")
        return False

if __name__ == "__main__":
    print("=== 在正确的父文献下创建笔记 ===")
    create_note_on_correct_parent()