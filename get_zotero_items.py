#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import os

# Zotero API配置
API_KEY = 'CIApUKos6l9E0GOaCBrILRrt'
LIBRARY_ID = '18982351'
BASE_URL = 'https://api.zotero.org'

def get_zotero_items():
    """获取Zotero库中的所有文献"""
    print("正在获取Zotero文献信息...")
    
    headers = {
        'Zotero-API-Key': API_KEY
    }
    
    url = f"{BASE_URL}/users/{LIBRARY_ID}/items"
    params = {
        'format': 'json',
        'limit': 100
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        items = response.json()
        print(f"成功获取 {len(items)} 个文献条目")
        
        return items
        
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return []

def process_items(items):
    """处理文献信息"""
    processed_items = []
    
    for item in items:
        data = item.get('data', {})
        
        processed_item = {
            'key': data.get('key', ''),
            'title': data.get('title', ''),
            'creators': data.get('creators', []),
            'date': data.get('date', ''),
            'abstractNote': data.get('abstractNote', ''),
            'publicationTitle': data.get('publicationTitle', ''),
            'itemType': data.get('itemType', ''),
            'tags': data.get('tags', []),
            'notes': item.get('notes', [])
        }
        
        processed_items.append(processed_item)
    
    return processed_items

def main():
    """主函数"""
    print("=== Zotero文献信息获取工具 ===")
    
    # 获取文献
    items = get_zotero_items()
    if not items:
        print("未获取到文献信息，请检查API配置")
        return
    
    # 处理文献信息
    processed_items = process_items(items)
    
    # 过滤出没有笔记的文献
    items_without_notes = [
        item for item in processed_items 
        if len(item['notes']) == 0 and item['itemType'] != 'note'
    ]
    
    # 统计信息
    print(f"\n=== 文献统计 ===")
    print(f"总文献数: {len(processed_items)}")
    print(f"有笔记的文献数: {len([item for item in processed_items if len(item['notes']) > 0])}")
    print(f"没有笔记的文献数: {len(items_without_notes)}")
    
    # 显示没有笔记的文献
    print(f"\n=== 没有笔记的文献列表 ===")
    for i, item in enumerate(items_without_notes, 1):
        print(f"\n{i}. {item['title']}")
        
        # 处理作者信息
        authors = []
        for creator in item['creators']:
            if creator.get('lastName') and creator.get('firstName'):
                authors.append(f"{creator['lastName']} {creator['firstName']}")
        print(f"   作者: {', '.join(authors) if authors else '未知'}")
        
        print(f"   年份: {item['date'] if item['date'] else '未知'}")
        print(f"   期刊: {item['publicationTitle'] if item['publicationTitle'] else '未知'}")
        
        # 摘要截取
        abstract = item['abstractNote']
        if abstract:
            abstract_preview = abstract[:100] + '...' if len(abstract) > 100 else abstract
            print(f"   摘要: {abstract_preview}")
        else:
            print(f"   摘要: 无")
        
        print(f"   Key: {item['key']}")
    
    # 保存到文件
    output_dir = r"E:\仓库\毕业论文"
    all_items_path = os.path.join(output_dir, "zotero_items.json")
    without_notes_path = os.path.join(output_dir, "zotero_items_without_notes.json")
    
    try:
        with open(all_items_path, 'w', encoding='utf-8') as f:
            json.dump(processed_items, f, ensure_ascii=False, indent=2)
        
        with open(without_notes_path, 'w', encoding='utf-8') as f:
            json.dump(items_without_notes, f, ensure_ascii=False, indent=2)
        
        print(f"\n数据已保存到:")
        print(f"- {all_items_path}")
        print(f"- {without_notes_path}")
        
    except Exception as e:
        print(f"保存文件时出错: {e}")

if __name__ == "__main__":
    main()