#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取特定文献的key
"""

from pyzotero import zotero

def get_item_key_by_title(title):
    """根据标题获取文献key"""
    zot = zotero.Zotero(
        "18982351",
        "user",
        "CIApUKos6l9E0GOaCBrILRrt"
    )
    
    items = zot.items(q=title, limit=10)
    for item in items:
        item_data = item.get('data', {})
        item_title = item_data.get('title', '')
        item_key = item_data.get('key')
        item_type = item_data.get('itemType')
        
        if title in item_title:
            print(f"标题: {item_title}")
            print(f"Key: {item_key}")
            print(f"类型: {item_type}")
            return item_key
    
    print("未找到匹配的文献")
    return None

if __name__ == "__main__":
    target_title = "基于教学评一体化的小学英语阅读教学中AI技术的运用"
    get_item_key_by_title(target_title)