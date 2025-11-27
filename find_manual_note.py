#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查找手动创建的"1111"笔记
"""

import sqlite3
from pathlib import Path

def find_manual_note():
    """查找手动创建的笔记"""
    db_path = "C:\\Users\\28480\\Zotero\\zotero.sqlite"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 搜索包含"1111"的笔记
        cursor.execute("""
            SELECT i.itemID, i.key, i.dateAdded, i.itemTypeID, n.note
            FROM items i
            LEFT JOIN itemNotes n ON i.itemID = n.itemID
            WHERE n.note LIKE '%1111%'
        """)
        
        results = cursor.fetchall()
        
        print(f"找到 {len(results)} 个包含'1111'的笔记:")
        
        for item_id, key, date_added, item_type_id, note_content in results:
            print(f"\n=== 手动创建的笔记 ===")
            print(f"Key: {key}")
            print(f"ItemID: {item_id}")
            print(f"DateAdded: {date_added}")
            print(f"ItemTypeID: {item_type_id}")
            print(f"Note Content: {note_content}")
            
            # 查找父文献
            cursor.execute("""
                SELECT parentItemID FROM itemNotes WHERE itemID = ?
            """, (item_id,))
            parent_result = cursor.fetchone()
            
            if parent_result:
                parent_id = parent_result[0]
                cursor.execute("""
                    SELECT key FROM items WHERE itemID = ?
                """, (parent_id,))
                parent_key = cursor.fetchone()
                
                if parent_key:
                    print(f"Parent Key: {parent_key[0]}")
        
        # 如果没找到，搜索所有笔记
        if not results:
            print("\n未找到包含'1111'的笔记，搜索所有笔记:")
            
            cursor.execute("""
                SELECT i.itemID, i.key, i.dateAdded, i.itemTypeID, 
                       LENGTH(n.note) as note_length,
                       SUBSTR(n.note, 1, 50) as note_preview
                FROM items i
                LEFT JOIN itemNotes n ON i.itemID = n.itemID
                WHERE n.note IS NOT NULL
                ORDER BY i.dateAdded DESC
            """)
            
            all_notes = cursor.fetchall()
            
            print(f"总共找到 {len(all_notes)} 个笔记:")
            for item_id, key, date_added, item_type_id, note_length, note_preview in all_notes:
                print(f"  Key: {key}, TypeID: {item_type_id}, Length: {note_length}, Preview: {note_preview}")
        
        return results
        
    except Exception as e:
        print(f"查找时出错: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=== 查找手动创建的'1111'笔记 ===")
    find_manual_note()