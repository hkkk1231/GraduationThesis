#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度分析所有笔记的完整数据结构
"""

import sqlite3
from pathlib import Path

def deep_analysis():
    """深度分析笔记数据结构"""
    db_path = r"C:\Users\28480\Zotero\zotero.sqlite"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查找包含"abcde"的新笔记
        cursor.execute("""
            SELECT i.itemID, i.key, i.dateAdded, i.itemTypeID, n.note
            FROM items i
            LEFT JOIN itemNotes n ON i.itemID = n.itemID
            WHERE n.note LIKE '%abcde%'
        """)
        
        abcde_notes = cursor.fetchall()
        
        print("=== 新创建的'abcde'笔记 ===")
        for note in abcde_notes:
            item_id, key, date_added, item_type_id, note_content = note
            print(f"Key: {key}")
            print(f"ItemID: {item_id}")
            print(f"ItemTypeID: {item_type_id}")
            print(f"DateAdded: {date_added}")
            print(f"Note Content: {note_content}")
            
            # 查找父文献
            cursor.execute("""
                SELECT parentItemID FROM itemNotes WHERE itemID = ?
            """, (item_id,))
            parent_id = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT key FROM items WHERE itemID = ?
            """, (parent_id,))
            parent_key = cursor.fetchone()[0]
            
            print(f"Parent Key: {parent_key}")
        
        # 查找"1111"笔记作为参考
        cursor.execute("""
            SELECT i.itemID, i.key, i.dateAdded, i.itemTypeID, n.note
            FROM items i
            LEFT JOIN itemNotes n ON i.itemID = n.itemID
            WHERE n.note LIKE '%1111%'
        """)
        
        manual_notes = cursor.fetchall()
        
        print("\n=== 手动创建的'1111'笔记（参考） ===")
        for note in manual_notes:
            item_id, key, date_added, item_type_id, note_content = note
            print(f"Key: {key}")
            print(f"ItemID: {item_id}")
            print(f"ItemTypeID: {item_type_id}")
            print(f"DateAdded: {date_added}")
            print(f"Note Content: {note_content}")
        
        # 检查所有相关表
        if abcde_notes and manual_notes:
            abcde_id = abcde_notes[0][0]
            manual_id = manual_notes[0][0]
            
            print("\n=== 完整数据结构对比 ===")
            
            # 检查items表的所有字段
            cursor.execute("PRAGMA table_info(items)")
            items_columns = cursor.fetchall()
            print("\nitems表字段:")
            for col in items_columns:
                print(f"  {col[1]} ({col[2]})")
            
            # 对比items表数据
            cursor.execute(f"SELECT * FROM items WHERE itemID = {abcde_id}")
            abcde_items = cursor.fetchone()
            
            cursor.execute(f"SELECT * FROM items WHERE itemID = {manual_id}")
            manual_items = cursor.fetchone()
            
            print(f"\nitems表对比:")
            for i, col in enumerate(items_columns):
                if i < len(abcde_items) and i < len(manual_items):
                    col_name = col[1]
                    abcde_val = abcde_items[i]
                    manual_val = manual_items[i]
                    match = "✓" if abcde_val == manual_val else "✗"
                    print(f"  {match} {col_name}: {abcde_val} vs {manual_val}")
            
            # 检查其他相关表
            tables_to_check = ['itemNotes', 'itemData', 'itemDataValues', 'itemTags']
            
            for table in tables_to_check:
                try:
                    cursor.execute(f"SELECT * FROM {table} WHERE itemID = {abcde_id}")
                    abcde_data = cursor.fetchall()
                    
                    cursor.execute(f"SELECT * FROM {table} WHERE itemID = {manual_id}")
                    manual_data = cursor.fetchall()
                    
                    print(f"\n{table}表:")
                    print(f"  abcde笔记: {abcde_data}")
                    print(f"  手动笔记: {manual_data}")
                except Exception as e:
                    print(f"\n{table}表: 查询失败 - {e}")
        
        return abcde_notes, manual_notes
        
    except Exception as e:
        print(f"深度分析时出错: {e}")
        return None, None
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=== 深度分析笔记数据结构 ===")
    deep_analysis()