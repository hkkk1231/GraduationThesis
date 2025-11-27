#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查找正确的文献Key
"""

import sqlite3
from pathlib import Path

def find_keys_by_title():
    """根据标题查找文献Key"""
    db_path = "C:\\Users\\28480\\Zotero\\zotero.sqlite"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查找包含特定标题的文献
        cursor.execute("""
            SELECT itemID, key, itemTypeID 
            FROM items 
            WHERE key LIKE '%LA2%' OR key LIKE '%SHG%'
            ORDER BY itemID DESC
            LIMIT 10
        """)
        
        results = cursor.fetchall()
        
        print("查找包含LA2或SHG的Key:")
        for item_id, key, item_type_id in results:
            print(f"  ID: {item_id}, Key: {key}, Type: {item_type_id}")
        
        # 查找所有笔记的父文献
        print("\n查找有笔记的文献:")
        cursor.execute("""
            SELECT DISTINCT i.itemID, i.key, i.itemTypeID
            FROM items i
            JOIN itemNotes n ON i.itemID = n.parentItemID
            ORDER BY i.itemID DESC
            LIMIT 10
        """)
        
        parent_results = cursor.fetchall()
        for item_id, key, item_type_id in parent_results:
            print(f"  ID: {item_id}, Key: {key}, Type: {item_type_id}")
            
            # 查找该文献的笔记数量
            cursor.execute("""
                SELECT COUNT(*) FROM itemNotes WHERE parentItemID = ?
            """, (item_id,))
            note_count = cursor.fetchone()[0]
            print(f"    笔记数量: {note_count}")
        
        # 查找特定标题的文献
        cursor.execute("""
            SELECT itemID, key 
            FROM items 
            WHERE key IN (
                SELECT parentItemID FROM itemNotes 
                WHERE note LIKE '%教学评一体化%'
            )
        """)
        
        title_results = cursor.fetchall()
        print("\n包含'教学评一体化'笔记的文献:")
        for item_id, key in title_results:
            print(f"  ID: {item_id}, Key: {key}")
        
        return True
        
    except Exception as e:
        print(f"查找Key时出错: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=== 查找正确的文献Key ===")
    find_keys_by_title()