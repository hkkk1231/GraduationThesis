#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接向Zotero数据库添加笔记并关联到PDF文献条目
"""

from pyzotero import zotero
from datetime import datetime

def add_note_to_parent_item(parent_key, note_content):
    """为父文献条目添加笔记"""
    zot = zotero.Zotero(
        "18982351",
        "user", 
        "CIApUKos6l9E0GOaCBrILRrt"
    )
    
    # 创建笔记条目
    note_data = {
        'itemType': 'note',
        'note': note_content,
        'parentItem': parent_key
    }
    
    try:
        resp = zot.create_items([note_data])
        print(f"API响应: {resp}")
        
        if resp.get('successful'):
            note_key = resp['successful'][0]['key']
            print(f"✓ 笔记成功添加到数据库，Key: {note_key}")
            return note_key
        elif resp.get('failed'):
            print(f"✗ 笔记添加失败: {resp['failed']}")
            return None
        else:
            print(f"✗ 未知响应: {resp}")
            return None
    except Exception as e:
        print(f"添加笔记时出错: {e}")
        return None

def get_parent_item_key(attachment_key):
    """获取附件的父文献条目key"""
    zot = zotero.Zotero("18982351", "user", "CIApUKos6l9E0GOaCBrILRrt")
    
    try:
        attachment = zot.item(attachment_key)
        parent_key = attachment.get('data', {}).get('parentItem')
        return parent_key
    except Exception as e:
        print(f"获取父文献key时出错: {e}")
        return None

def create_note_content():
    """创建笔记内容"""
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
    
    return note_content

def verify_note_added(parent_key):
    """验证笔记是否成功添加"""
    zot = zotero.Zotero("18982351", "user", "CIApUKos6l9E0GOaCBrILRrt")
    
    try:
        # 获取该文献条目的所有子条目
        children = zot.children(parent_key)
        notes = [child for child in children if child.get('data', {}).get('itemType') == 'note']
        
        print(f"文献条目 {parent_key} 下的笔记数量: {len(notes)}")
        for note in notes:
            note_data = note.get('data', {})
            note_key = note_data.get('key')
            note_content = note_data.get('note', '')[:100] + "..." if len(note_data.get('note', '')) > 100 else note_data.get('note', '')
            print(f"  - 笔记Key: {note_key}")
            print(f"    内容预览: {note_content}")
        
        return len(notes) > 0
    except Exception as e:
        print(f"验证笔记时出错: {e}")
        return False

if __name__ == "__main__":
    print("=== 向Zotero数据库添加笔记 ===")
    
    # PDF附件的key
    attachment_key = "V2G5HDET"
    
    # 获取父文献条目key
    print(f"获取附件 {attachment_key} 的父文献条目...")
    parent_key = get_parent_item_key(attachment_key)
    
    if parent_key:
        print(f"找到父文献条目Key: {parent_key}")
        
        # 创建笔记内容
        print("创建笔记内容...")
        note_content = create_note_content()
        
        # 添加笔记到数据库
        print("向数据库添加笔记...")
        note_key = add_note_to_parent_item(parent_key, note_content)
        
        if note_key:
            print("验证笔记是否成功添加...")
            verify_note_added(parent_key)
        else:
            print("笔记添加失败")
    else:
        print("无法获取父文献条目Key")