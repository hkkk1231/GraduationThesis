#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import os
from datetime import datetime

def analyze_all_literature():
    """分析所有文献，查找可能的外文内容"""
    
    # 读取Zotero数据
    items_file = r"E:\仓库\毕业论文\zotero_items.json"
    
    try:
        with open(items_file, 'r', encoding='utf-8') as f:
            items = json.load(f)
    except Exception as e:
        print(f"读取文件失败: {e}")
        return
    
    print("=== 详细文献分析 ===")
    print(f"总文献数: {len(items)}")
    
    # 分析每篇文献
    potential_foreign = []
    chinese_literature = []
    
    for i, item in enumerate(items, 1):
        if item.get('itemType') == 'attachment':
            continue
            
        title = item.get('title', '')
        creators = item.get('creators', [])
        publication = item.get('publicationTitle', '')
        abstract = item.get('abstractNote', '')
        
        # 检查各种外文特征
        has_english_chars = bool(re.search(r'[a-zA-Z]', title))
        has_chinese_chars = bool(re.search(r'[\u4e00-\u9fff]', title))
        has_foreign_authors = False
        has_english_publication = bool(re.search(r'[a-zA-Z]', publication)) and not re.search(r'[\u4e00-\u9fff]', publication)
        
        # 检查作者
        foreign_author_names = []
        for creator in creators:
            name = creator.get('name', '')
            if ' ' in name and not re.search(r'[\u4e00-\u9fff]', name):
                has_foreign_authors = True
                foreign_author_names.append(name)
        
        # 分类
        if has_foreign_authors or has_english_publication:
            potential_foreign.append({
                'index': i,
                'title': title,
                'creators': creators,
                'publication': publication,
                'foreign_authors': foreign_author_names,
                'has_english_publication': has_english_publication
            })
        elif has_chinese_chars:
            chinese_literature.append({
                'index': i,
                'title': title,
                'publication': publication
            })
    
    print(f"\n=== 中文文献 ({len(chinese_literature)} 篇) ===")
    for item in chinese_literature[:10]:
        print(f"{item['index']}. {item['title'][:50]}...")
        if item['publication']:
            print(f"   期刊: {item['publication']}")
    
    print(f"\n=== 可能包含外文元素的文献 ({len(potential_foreign)} 篇) ===")
    if potential_foreign:
        for item in potential_foreign:
            print(f"\n{item['index']}. {item['title']}")
            print(f"   期刊: {item['publication']}")
            if item['foreign_authors']:
                print(f"   外文作者: {', '.join(item['foreign_authors'])}")
            if item['has_english_publication']:
                print(f"   英文期刊名称")
    else:
        print("未发现明显的外文文献特征")
    
    # 检查最近添加的文献
    print(f"\n=== 按添加时间排序的最近文献 ===")
    
    # 按dateAdded排序
    valid_items = [item for item in items if item.get('itemType') != 'attachment' and item.get('dateAdded')]
    valid_items.sort(key=lambda x: x.get('dateAdded', ''), reverse=True)
    
    for i, item in enumerate(valid_items[:10], 1):
        title = item.get('title', '')
        date_added = item.get('dateAdded', '')
        publication = item.get('publicationTitle', '')
        
        print(f"\n{i}. {title}")
        print(f"   添加时间: {date_added}")
        if publication:
            print(f"   期刊: {publication}")
        
        # 检查创作者
        creators = item.get('creators', [])
        if creators:
            creator_names = []
            for creator in creators:
                if creator.get('name'):
                    creator_names.append(creator['name'])
                elif creator.get('firstName') and creator.get('lastName'):
                    creator_names.append(f"{creator['lastName']} {creator['firstName']}")
            print(f"   作者: {', '.join(creator_names)}")
    
    return {
        'total_items': len(items),
        'chinese_literature': len(chinese_literature),
        'potential_foreign': len(potential_foreign),
        'recent_items': valid_items[:10]
    }

def suggest_next_steps(analysis_result):
    """建议下一步操作"""
    print(f"\n=== 建议和下一步操作 ===")
    
    if analysis_result['potential_foreign'] == 0:
        print("1. 当前Zotero库中暂无外文文献")
        print("2. 建议通过以下方式添加外文文献：")
        print("   - 从Google Scholar、Web of Science等学术数据库导入")
        print("   - 使用Zotero Connector直接从网页抓取")
        print("   - 通过DOI或ISBN手动添加")
        print("3. 可以先为现有的中文文献创建标准化笔记作为模板")
    else:
        print(f"发现 {analysis_result['potential_foreign']} 篇可能包含外文元素的文献")
        print("建议进一步分析这些文献的具体内容")

if __name__ == "__main__":
    result = analyze_all_literature()
    suggest_next_steps(result)