#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证修复结果
"""

import sqlite3
from pathlib import Path

def verify_fixed_notes():
    """验证修复后的笔记"""
    db_path = r"C:\Users\28480\Zotero\zotero.sqlite"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查找修复后的笔记
        fixed_key = "WC7G53SC"  # 修复的笔记
        new_key = "2JXJFNXQ"    # 新创建的笔记
        
        print("=== 验证修复结果 ===")
        
        # 检查修复的笔记
        cursor.execute("""
            SELECT i.itemID, i.key, i.dateAdded, n.note
            FROM items i
            LEFT JOIN itemNotes n ON i.itemID = n.itemID
            WHERE i.key = ?
        """, (fixed_key,))
        
        fixed_note = cursor.fetchone()
        
        if fixed_note:
            print(f"\n✓ 修复的笔记 {fixed_key}:")
            print(f"  包含data-schema-version: {'data-schema-version' in fixed_note[3]}")
            print(f"  内容预览: {fixed_note[3][:100]}...")
        
        # 检查新创建的笔记
        cursor.execute("""
            SELECT i.itemID, i.key, i.dateAdded, n.note
            FROM items i
            LEFT JOIN itemNotes n ON i.itemID = n.itemID
            WHERE i.key = ?
        """, (new_key,))
        
        new_note = cursor.fetchone()
        
        if new_note:
            print(f"\n✓ 新创建的笔记 {new_key}:")
            print(f"  包含data-schema-version: {'data-schema-version' in new_note[3]}")
            print(f"  内容预览: {new_note[3][:100]}...")
        
        # 检查父文献下的所有笔记
        parent_key = "LA2VSHG9"
        cursor.execute("SELECT itemID FROM items WHERE key = ?", (parent_key,))
        parent_id = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT i.key, i.dateAdded, n.note
            FROM items i
            LEFT JOIN itemNotes n ON i.itemID = n.itemID
            WHERE i.itemID IN (
                SELECT itemID FROM itemNotes WHERE parentItemID = ?
            )
            ORDER BY i.dateAdded DESC
        """, (parent_id,))
        
        all_notes = cursor.fetchall()
        
        print(f"\n父文献 {parent_key} 下的所有笔记:")
        for note_key, date_added, note_content in all_notes:
            has_schema = 'data-schema-version' in note_content if note_content else False
            status = "✓" if has_schema else "✗"
            print(f"  {status} {note_key} - {date_added} - 包含schema: {has_schema}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"验证时出错: {e}")
        return False

if __name__ == "__main__":
    print("=== 验证笔记修复结果 ===")
    verify_fixed_notes()
    print("\n验证完成！请重启Zotero检查笔记是否正常显示。")