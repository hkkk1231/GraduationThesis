#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对比手动创建和代码创建的笔记数据结构差异
"""

import sqlite3
import json
from pathlib import Path

def analyze_note_structure():
    """分析笔记数据结构"""
    db_path = "C:\\Users\\28480\\Zotero\\zotero.sqlite"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查找父文献
        cursor.execute("SELECT itemID FROM items WHERE key = 'LA2VSHG9'")
        parent_result = cursor.fetchone()
        
        if not parent_result:
            print("未找到父文献 LA2VSHG9")
            return
        
        parent_id = parent_result[0]
        print(f"父文献ID: {parent_id}")
        
        # 查找该父文献下的所有笔记
        cursor.execute("""
            SELECT i.itemID, i.key, i.dateAdded, i.dateModified, 
                   i.libraryID, i.itemTypeID, n.note
            FROM items i
            LEFT JOIN itemNotes n ON i.itemID = n.itemID
            WHERE i.itemID IN (
                SELECT itemID FROM itemNotes WHERE parentItemID = ?
            )
            ORDER BY i.dateAdded DESC
        """, (parent_id,))
        
        notes = cursor.fetchall()
        
        print(f"\n找到 {len(notes)} 个笔记:")
        
        for i, note in enumerate(notes):
            item_id, key, date_added, date_modified, library_id, item_type_id, note_content = note
            
            print(f"\n=== 笔记 {i+1} ===")
            print(f"Key: {key}")
            print(f"ItemID: {item_id}")
            print(f"DateAdded: {date_added}")
            print(f"DateModified: {date_modified}")
            print(f"LibraryID: {library_id}")
            print(f"ItemTypeID: {item_type_id}")
            
            if note_content:
                print(f"Note Length: {len(note_content)}")
                print(f"Note Preview: {note_content[:100]}...")
                
                # 检查是否包含"1111"（手动创建的）
                if "1111" in note_content:
                    print("*** 这是手动创建的笔记 ***")
                    manual_note = {
                        'item_id': item_id,
                        'key': key,
                        'date_added': date_added,
                        'date_modified': date_modified,
                        'library_id': library_id,
                        'item_type_id': item_type_id,
                        'note_content': note_content
                    }
                
                # 检查是否包含"教学评一体化"（代码创建的）
                elif "教学评一体化" in note_content and len(note_content) > 500:
                    print("*** 这是代码创建的笔记 ***")
                    code_note = {
                        'item_id': item_id,
                        'key': key,
                        'date_added': date_added,
                        'date_modified': date_modified,
                        'library_id': library_id,
                        'item_type_id': item_type_id,
                        'note_content': note_content
                    }
        
        # 详细对比数据结构
        if 'manual_note' in locals() and 'code_note' in locals():
            print("\n" + "="*60)
            print("详细对比分析:")
            print("="*60)
            
            print("\n1. 基本字段对比:")
            print(f"手动笔记 - LibraryID: {manual_note['library_id']}, ItemTypeID: {manual_note['item_type_id']}")
            print(f"代码笔记 - LibraryID: {code_note['library_id']}, ItemTypeID: {code_note['item_type_id']}")
            
            print("\n2. 日期格式对比:")
            print(f"手动笔记 - DateAdded: {manual_note['date_added']}")
            print(f"代码笔记 - DateAdded: {code_note['date_added']}")
            
            print("\n3. HTML格式对比:")
            manual_html = manual_note['note_content'][:200]
            code_html = code_note['note_content'][:200]
            print(f"手动笔记HTML: {manual_html}")
            print(f"代码笔记HTML: {code_html}")
            
            # 检查itemDataValues表
            print("\n4. itemDataValues表对比:")
            cursor.execute("""
                SELECT fieldID, value FROM itemDataValues 
                WHERE itemID = ?
            """, (manual_note['item_id'],))
            manual_values = cursor.fetchall()
            
            cursor.execute("""
                SELECT fieldID, value FROM itemDataValues 
                WHERE itemID = ?
            """, (code_note['item_id'],))
            code_values = cursor.fetchall()
            
            print(f"手动笔记 itemDataValues: {manual_values}")
            print(f"代码笔记 itemDataValues: {code_values}")
            
            # 检查itemData表
            print("\n5. itemData表对比:")
            cursor.execute("""
                SELECT fieldID, itemID FROM itemData 
                WHERE itemID = ?
            """, (manual_note['item_id'],))
            manual_data = cursor.fetchall()
            
            cursor.execute("""
                SELECT fieldID, itemID FROM itemData 
                WHERE itemID = ?
            """, (code_note['item_id'],))
            code_data = cursor.fetchall()
            
            print(f"手动笔记 itemData: {manual_data}")
            print(f"代码笔记 itemData: {code_data}")
            
            return manual_note, code_note
        
        return None, None
        
    except Exception as e:
        print(f"分析时出错: {e}")
        return None, None
    finally:
        if 'conn' in locals():
            conn.close()

def check_item_types():
    """检查itemTypes表"""
    db_path = "C:\\Users\\28480\\Zotero\\zotero.sqlite"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT itemTypeID, typeName FROM itemTypes WHERE typeName LIKE '%note%'")
        note_types = cursor.fetchall()
        
        print("\n笔记相关的itemTypes:")
        for type_id, type_name in note_types:
            print(f"  ID: {type_id}, Name: {type_name}")
        
        return note_types
        
    except Exception as e:
        print(f"检查itemTypes时出错: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=== 对比手动创建和代码创建的笔记数据结构 ===")
    
    # 检查itemTypes
    check_item_types()
    
    # 分析笔记结构
    manual_note, code_note = analyze_note_structure()
    
    if manual_note and code_note:
        print("\n分析完成，准备创建修复脚本...")
    else:
        print("\n未找到足够的笔记数据进行对比")