#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import os
from datetime import datetime

def is_foreign_literature(item):
    """判断是否为外文文献"""
    title = item.get('title', '').lower()
    abstract = item.get('abstractNote', '').lower()
    publication = item.get('publicationTitle', '').lower()
    creators = item.get('creators', [])
    
    # 检查作者姓名是否为外文（包含空格的非中文字符）
    has_foreign_authors = False
    for creator in creators:
        name = creator.get('name', '')
        if ' ' in name and not re.search(r'[\u4e00-\u9fff]', name):
            has_foreign_authors = True
            break
    
    # 检查标题是否包含英文字符且不包含中文字符
    has_english_title = bool(re.search(r'[a-zA-Z]', title)) and not re.search(r'[\u4e00-\u9fff]', title)
    
    # 检查期刊名称是否为外文
    has_foreign_publication = bool(re.search(r'[a-zA-Z]', publication)) and not re.search(r'[\u4e00-\u9fff]', publication)
    
    # 检查摘要是否为外文
    has_foreign_abstract = bool(re.search(r'[a-zA-Z]', abstract)) and not re.search(r'[\u4e00-\u9fff]', abstract)
    
    # 判断标准：满足以下任一条件即认为是外文文献
    return (has_foreign_authors or 
            has_english_title or 
            has_foreign_publication or 
            has_foreign_abstract)

def extract_detailed_info(item):
    """提取文献详细信息"""
    creators = item.get('creators', [])
    
    # 格式化作者信息
    author_list = []
    for creator in creators:
        if creator.get('name'):
            author_list.append(creator['name'])
        elif creator.get('firstName') and creator.get('lastName'):
            author_list.append(f"{creator['lastName']}, {creator['firstName']}")
    
    # 提取年份
    date = item.get('date', '')
    year_match = re.search(r'\b(19|20)\d{2}\b', date)
    year = year_match.group() if year_match else date
    
    # 获取标签
    tags = [tag.get('tag', '') for tag in item.get('tags', []) if tag.get('tag')]
    
    return {
        'key': item.get('key', ''),
        'title': item.get('title', ''),
        'authors': author_list,
        'year': year,
        'abstract': item.get('abstractNote', ''),
        'publication': item.get('publicationTitle', ''),
        'item_type': item.get('itemType', ''),
        'tags': tags,
        'date_added': item.get('dateAdded', ''),
        'url': item.get('url', ''),
        'doi': item.get('doi', ''),
        'pages': item.get('pages', ''),
        'volume': item.get('volume', ''),
        'issue': item.get('issue', ''),
        'publisher': item.get('publisher', ''),
        'language': item.get('language', '')
    }

def main():
    """主函数"""
    print("=== 外文文献分析工具 ===")
    
    # 读取Zotero数据
    items_file = r"E:\仓库\毕业论文\zotero_items.json"
    
    try:
        with open(items_file, 'r', encoding='utf-8') as f:
            items = json.load(f)
    except Exception as e:
        print(f"读取文件失败: {e}")
        return
    
    print(f"总文献数: {len(items)}")
    
    # 筛选外文文献
    foreign_literature = []
    for item in items:
        if is_foreign_literature(item) and item.get('itemType') != 'attachment':
            foreign_literature.append(extract_detailed_info(item))
    
    print(f"发现外文文献: {len(foreign_literature)} 篇")
    
    if not foreign_literature:
        print("未发现外文文献，显示所有文献供检查...")
        for i, item in enumerate(items[:10], 1):
            if item.get('itemType') != 'attachment':
                print(f"\n{i}. {item.get('title', '')}")
                print(f"   类型: {item.get('itemType', '')}")
                print(f"   期刊: {item.get('publicationTitle', '')}")
        return
    
    # 按添加时间排序，获取最新的5篇
    foreign_literature.sort(key=lambda x: x['date_added'], reverse=True)
    recent_foreign = foreign_literature[:5]
    
    print(f"\n=== 最近新增的5篇外文文献 ===")
    
    for i, item in enumerate(recent_foreign, 1):
        print(f"\n{'='*60}")
        print(f"{i}. {item['title']}")
        print(f"   Key: {item['key']}")
        print(f"   作者: {', '.join(item['authors']) if item['authors'] else '未知'}")
        print(f"   年份: {item['year'] if item['year'] else '未知'}")
        print(f"   期刊: {item['publication'] if item['publication'] else '未知'}")
        print(f"   类型: {item['item_type']}")
        
        if item['volume']:
            print(f"   卷: {item['volume']}")
        if item['issue']:
            print(f"   期: {item['issue']}")
        if item['pages']:
            print(f"   页码: {item['pages']}")
        if item['publisher']:
            print(f"   出版社: {item['publisher']}")
        
        # 摘要处理
        if item['abstract']:
            abstract = item['abstract']
            if len(abstract) > 300:
                abstract = abstract[:300] + "..."
            print(f"   摘要: {abstract}")
        else:
            print(f"   摘要: 无")
        
        if item['tags']:
            print(f"   标签: {', '.join(item['tags'])}")
        
        if item['doi']:
            print(f"   DOI: {item['doi']}")
        
        if item['url']:
            print(f"   URL: {item['url']}")
        
        print(f"   添加时间: {item['date_added']}")
    
    # 保存外文文献数据
    output_file = r"E:\仓库\毕业论文\foreign_literature_analysis.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'total_foreign_literature': len(foreign_literature),
                'recent_5_foreign': recent_foreign,
                'all_foreign_literature': foreign_literature,
                'analysis_time': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n外文文献分析结果已保存到: {output_file}")
        
    except Exception as e:
        print(f"保存文件时出错: {e}")

if __name__ == "__main__":
    main()