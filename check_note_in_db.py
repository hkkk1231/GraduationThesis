#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查笔记是否在数据库中
"""

import sqlite3
from pathlib import Path

def check_note_in_database():
    """检查笔记是否在数据库中"""
    db_path = "C:\\Users\\28480\\Zotero\\zotero.sqlite"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查找笔记
        note_key = "XIWO6PLQ"
        cursor.execute("""
            SELECT i.itemID, i.key, i.dateAdded, n.note
            FROM items i
            LEFT JOIN itemNotes n ON i.itemID = n.itemID
            WHERE i.key = ?
        """, (note_key,))
        
        result = cursor.fetchone()
        
        if result:
            item_id, key, date_added, note_content = result
            print("✓ 找到笔记！")
            print(f"笔记Key: {key}")
            print(f"添加时间: {date_added}")
            print(f"笔记内容长度: {len(note_content) if note_content else 0} 字符")
            
            if note_content:
                print("\n笔记内容预览:")
                preview = note_content[:200] + "..." if len(note_content) > 200 else note_content
                print(preview)
            
            # 查找父文献
            cursor.execute("""
                SELECT parentItemID FROM itemNotes WHERE itemID = ?
            """, (item_id,))
            
            parent_result = cursor.fetchone()
            if parent_result:
                parent_id = parent_result[0]
                cursor.execute("""
                    SELECT key, title FROM items WHERE itemID = ?
                """, (parent_id,))
                
                parent_info = cursor.fetchone()
                if parent_info:
                    parent_key, parent_title = parent_info
                    print(f"\n父文献Key: {parent_key}")
                    print(f"父文献标题: {parent_title}")
            
            return True
        else:
            print("✗ 未找到笔记")
            return False
            
    except Exception as e:
        print(f"检查数据库时出错: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def check_all_notes_for_parent():
    """检查父文献下的所有笔记"""
    db_path = "C:\\Users\\28480\\Zotero\\zotero.sqlite"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查找父文献
        parent_key = "LA2VSHG9"
        cursor.execute("SELECT itemID FROM items WHERE key = ?", (parent_key,))
        parent_result = cursor.fetchone()
        
        if not parent_result:
            print(f"✗ 未找到父文献: {parent_key}")
            return False
        
        parent_id = parent_result[0]
        
        # 查找所有相关的笔记
        cursor.execute("""
            SELECT i.itemID, i.key, i.dateAdded, n.note
            FROM items i
            LEFT JOIN itemNotes n ON i.itemID = n.itemID
            WHERE i.itemID IN (
                SELECT itemID FROM itemNotes WHERE parentItemID = ?
            )
        """, (parent_id,))
        
        notes = cursor.fetchall()
        
        print(f"\n父文献 {parent_key} 下的笔记数量: {len(notes)}")
        
        for note in notes:
            item_id, key, date_added, note_content = note
            print(f"\n笔记Key: {key}")
            print(f"添加时间: {date_added}")
            if note_content:
                preview = note_content[:100] + "..." if len(note_content) > 100 else note_content
                print(f"内容预览: {preview}")
        
        return len(notes) > 0
        
    except Exception as e:
        print(f"检查笔记时出错: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=== 检查笔记是否在Zotero数据库中 ===")
    
    # 检查特定笔记
    check_note_in_database()
    
    print("\n" + "="*50)
    
    # 检查父文献下的所有笔记
    check_all_notes_for_parent()