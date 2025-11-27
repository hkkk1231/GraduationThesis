#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细对比手动创建和代码创建的笔记
"""

import sqlite3
from pathlib import Path

def detailed_comparison():
    """详细对比笔记结构"""
    db_path = "C:\\Users\\28480\\Zotero\\zotero.sqlite"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 手动创建的笔记
        manual_key = "Z7WTPU52"
        cursor.execute("""
            SELECT i.itemID, i.key, i.dateAdded, i.dateModified, 
                   i.libraryID, i.itemTypeID, n.note
            FROM items i
            LEFT JOIN itemNotes n ON i.itemID = n.itemID
            WHERE i.key = ?
        """, (manual_key,))
        
        manual_note = cursor.fetchone()
        
        if manual_note:
            print("=== 手动创建的笔记 ===")
            print(f"ItemID: {manual_note[0]}")
            print(f"Key: {manual_note[1]}")
            print(f"DateAdded: {manual_note[2]}")
            print(f"DateModified: {manual_note[3]}")
            print(f"LibraryID: {manual_note[4]}")
            print(f"ItemTypeID: {manual_note[5]}")
            print(f"Note Content: {manual_note[6]}")
            
            # 查找父文献
            cursor.execute("""
                SELECT parentItemID FROM itemNotes WHERE itemID = ?
            """, (manual_note[0],))
            parent_id = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT key FROM items WHERE itemID = ?
            """, (parent_id,))
            parent_key = cursor.fetchone()[0]
            
            print(f"Parent ItemID: {parent_id}")
            print(f"Parent Key: {parent_key}")
        
        # 代码创建的笔记（选择一个）
        code_key = "WC7G53SC"  # 这个ItemTypeID是28，与手动笔记相同
        cursor.execute("""
            SELECT i.itemID, i.key, i.dateAdded, i.dateModified, 
                   i.libraryID, i.itemTypeID, n.note
            FROM items i
            LEFT JOIN itemNotes n ON i.itemID = n.itemID
            WHERE i.key = ?
        """, (code_key,))
        
        code_note = cursor.fetchone()
        
        if code_note:
            print("\n=== 代码创建的笔记 ===")
            print(f"ItemID: {code_note[0]}")
            print(f"Key: {code_note[1]}")
            print(f"DateAdded: {code_note[2]}")
            print(f"DateModified: {code_note[3]}")
            print(f"LibraryID: {code_note[4]}")
            print(f"ItemTypeID: {code_note[5]}")
            print(f"Note Content: {code_note[6]}")
            
            # 查找父文献
            cursor.execute("""
                SELECT parentItemID FROM itemNotes WHERE itemID = ?
            """, (code_note[0],))
            parent_id = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT key FROM items WHERE itemID = ?
            """, (parent_id,))
            parent_key = cursor.fetchone()[0]
            
            print(f"Parent ItemID: {parent_id}")
            print(f"Parent Key: {parent_key}")
        
        # 对比分析
        if manual_note and code_note:
            print("\n=== 差异分析 ===")
            
            # 1. ItemTypeID对比
            print(f"ItemTypeID - 手动: {manual_note[5]}, 代码: {code_note[5]}")
            
            # 2. HTML结构对比
            manual_html = manual_note[6]
            code_html = code_note[6]
            
            print(f"\n手动笔记HTML结构:")
            print(manual_html[:200])
            
            print(f"\n代码笔记HTML结构:")
            print(code_html[:200])
            
            # 3. 检查是否有data-schema-version
            if 'data-schema-version' in manual_html:
                print("\n✓ 手动笔记包含data-schema-version")
            else:
                print("\n✗ 手动笔记不包含data-schema-version")
                
            if 'data-schema-version' in code_html:
                print("✓ 代码笔记包含data-schema-version")
            else:
                print("✗ 代码笔记不包含data-schema-version")
            
            # 4. 检查itemDataValues表
            print("\n=== itemDataValues表检查 ===")
            cursor.execute("""
                SELECT fieldID, value FROM itemDataValues 
                WHERE itemID = ?
            """, (manual_note[0],))
            manual_values = cursor.fetchall()
            
            cursor.execute("""
                SELECT fieldID, value FROM itemDataValues 
                WHERE itemID = ?
            """, (code_note[0],))
            code_values = cursor.fetchall()
            
            print(f"手动笔记 itemDataValues: {manual_values}")
            print(f"代码笔记 itemDataValues: {code_values}")
            
            return manual_note, code_note
        
        return None, None
        
    except Exception as e:
        print(f"对比时出错: {e}")
        return None, None
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=== 详细对比手动创建和代码创建的笔记 ===")
    detailed_comparison()