#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化查找正确的父文献
"""

import sqlite3
from pathlib import Path

def find_parent_simplified():
    """简化版查找父文献"""
    db_path = r"C:\Users\28480\Zotero\zotero.sqlite"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查找57T8RALW和LA2VSHG9的详细信息
        print("=== 对比两个可能的父文献 ===")
        
        for key in ["57T8RALW", "LA2VSHG9"]:
            cursor.execute("SELECT itemID, itemTypeID, dateAdded FROM items WHERE key = ?", (key,))
            result = cursor.fetchone()
            
            if result:
                item_id, item_type_id, date_added = result
                print(f"\nKey: {key}")
                print(f"  ItemID: {item_id}")
                print(f"  ItemTypeID: {item_type_id}")
                print(f"  DateAdded: {date_added}")
                
                # 查找所有子条目
                cursor.execute("""
                    SELECT i.key, i.itemTypeID 
                    FROM items i 
                    WHERE i.itemID IN (
                        SELECT itemID FROM itemNotes WHERE parentItemID = ?
                        UNION
                        SELECT itemID FROM itemAttachments WHERE parentItemID = ?
                    )
                """, (item_id, item_id))
                
                children = cursor.fetchall()
                print(f"  子条目数量: {len(children)}")
                for child_key, child_type in children:
                    print(f"    - {child_key} (Type: {child_type})")
        
        # 查找所有包含PDF附件的文献
        print("\n=== 包含附件的文献 ===")
        cursor.execute("""
            SELECT DISTINCT parent.itemID, parent.key, parent.dateAdded
            FROM items parent
            JOIN items child ON parent.itemID = child.parentItemID
            WHERE child.itemTypeID IN (
                SELECT itemTypeID FROM itemTypes WHERE typeName = 'attachment'
            )
            ORDER BY parent.dateAdded DESC
            LIMIT 10
        """)
        
        parents_with_attachments = cursor.fetchall()
        
        for item_id, key, date_added in parents_with_attachments:
            print(f"ItemID: {item_id}, Key: {key}, DateAdded: {date_added}")
            
            # 查找附件
            cursor.execute("""
                SELECT key FROM items 
                WHERE parentItemID = ? AND itemTypeID IN (
                    SELECT itemTypeID FROM itemTypes WHERE typeName = 'attachment'
                )
            """, (item_id,))
            
            attachments = cursor.fetchall()
            for att_key, in attachments:
                print(f"  附件: {att_key}")
        
        return True
        
    except Exception as e:
        print(f"查找时出错: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=== 简化查找正确的父文献 ===")
    find_parent_simplified()
