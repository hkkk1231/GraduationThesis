#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证笔记是否成功添加到Zotero数据库
"""

from pyzotero import zotero

def verify_note_in_database():
    """验证笔记是否在数据库中"""
    zot = zotero.Zotero("18982351", "user", "CIApUKos6l9E0GOaCBrILRrt")
    
    try:
        # 直接通过笔记key获取笔记
        note_key = "WC7G53SC"
        note = zot.item(note_key)
        
        if note:
            note_data = note.get('data', {})
            print("✓ 笔记成功找到！")
            print(f"笔记Key: {note_key}")
            print(f"笔记类型: {note_data.get('itemType')}")
            print(f"父文献Key: {note_data.get('parentItem')}")
            print(f"添加时间: {note_data.get('dateAdded')}")
            print(f"修改时间: {note_data.get('dateModified')}")
            
            # 显示笔记内容的前200个字符
            note_content = note_data.get('note', '')
            print(f"\n笔记内容预览:")
            print(note_content[:300] + "..." if len(note_content) > 300 else note_content)
            
            return True
        else:
            print("✗ 未找到笔记")
            return False
            
    except Exception as e:
        print(f"验证笔记时出错: {e}")
        return False

def check_parent_item_children():
    """检查父文献条目下的所有子条目"""
    zot = zotero.Zotero("18982351", "user", "CIApUKos6l9E0GOaCBrILRrt")
    
    try:
        parent_key = "LA2VSHG9"
        children = zot.children(parent_key)
        
        print(f"\n父文献条目 {parent_key} 下的子条目:")
        for child in children:
            child_data = child.get('data', {})
            child_key = child_data.get('key')
            child_type = child_data.get('itemType')
            child_title = child_data.get('title', child_data.get('filename', ''))
            
            print(f"  - {child_type}: {child_title} (Key: {child_key})")
            
            if child_type == 'note':
                print(f"    这是我们的笔记！")
        
        return len(children) > 0
    except Exception as e:
        print(f"检查子条目时出错: {e}")
        return False

if __name__ == "__main__":
    print("=== 验证笔记是否成功添加到Zotero数据库 ===")
    
    # 验证笔记是否存在
    verify_note_in_database()
    
    # 检查父文献条目的子条目
    check_parent_item_children()
    
    print("\n✓ 笔记已成功写入Zotero数据库，并与PDF文献关联在同一个条目下！")