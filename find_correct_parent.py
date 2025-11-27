#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查找正确的父文献
"""

import sqlite3
from pathlib import Path

def find_correct_parent():
    """查找正确的父文献"""
    db_path = r"C:\Users\28480\Zotero\zotero.sqlite"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查找包含"教学评一体化"的文献
        cursor.execute("""
            SELECT itemID, key, dateAdded, itemTypeID
            FROM items
            WHERE key IN (
                SELECT parentItemID FROM itemNotes 
                WHERE note LIKE '%教学评一体化%'
            )
        """)
        
        teaching_notes = cursor.fetchall()
        
        print("=== 包含'教学评一体化'笔记的父文献 ===")
        for note in teaching_notes:
            item_id, key, date_added, item_type_id = note
            print(f"ItemID: {item_id}, Key: {key}, DateAdded: {date_added}, Type: {item_type_id}")
        
        # 查找所有文献标题
        print("\n=== 所有文献标题 ===")
        cursor.execute("""
            SELECT i.itemID, i.key, i.itemTypeID
            FROM items i
            WHERE i.itemTypeID IN (SELECT itemTypeID FROM itemTypes WHERE typeName IN ('journalArticle', 'book', 'thesis'))
            ORDER BY i.dateAdded DESC
            LIMIT 20
        """)
        
        all_items = cursor.fetchall()
        
        for item in all_items:
            item_id, key, item_type_id = item
            
            # 查找附件
            cursor.execute("""
                SELECT key, filename FROM items 
                WHERE parentItemID = ? AND itemTypeID IN (
                    SELECT itemTypeID FROM itemTypes WHERE typeName = 'attachment'
                )
            """, (item_id,))
            
            attachments = cursor.fetchall()
            
            if attachments:
                for att_key, filename in attachments:
                    if filename and "教学评一体化" in filename:
                        print(f"✓ ItemID: {item_id}, Key: {key}, 附件: {filename}")
        
        # 查找57T8RALW和LA2VSHG9的详细信息
        print("\n=== 对比两个可能的父文献 ===")
        
        for key in ["57T8RALW", "LA2VSHG9"]:
            cursor.execute("SELECT itemID, itemTypeID, dateAdded FROM items WHERE key = ?", (key,))
            result = cursor.fetchone()
            
            if result:
                item_id, item_type_id, date_added = result
                print(f"\nKey: {key}")
                print(f"  ItemID: {item_id}")
                print(f"  ItemTypeID: {item_type_id}")
                print(f"  DateAdded: {date_added}")
                
                # 查找附件
                cursor.execute("""
                    SELECT key, filename FROM items 
                    WHERE parentItemID = ? AND itemTypeID IN (
                        SELECT itemTypeID FROM itemTypes WHERE typeName = 'attachment'
                    )
                """, (item_id,))
                
                attachments = cursor.fetchall()
                print(f"  附件数量: {len(attachments)}")
                for att_key, filename in attachments:
                    print(f"    - {att_key}: {filename}")
                
                # 查找笔记
                cursor.execute("""
                    SELECT key FROM items 
                    WHERE itemID IN (
                        SELECT itemID FROM itemNotes WHERE parentItemID = ?
                    )
                """, (item_id,))
                
                notes = cursor.fetchall()
                print(f"  笔记数量: {len(notes)}")
                for note_key, in notes:
                    print(f"    - {note_key}")
        
        return True
        
    except Exception as e:
        print(f"查找时出错: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=== 查找正确的父文献 ===")
    find_correct_parent()