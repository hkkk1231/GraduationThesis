#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from datetime import datetime

def get_recent_literature_details():
    """获取最近添加的文献详细信息"""
    
    # 读取Zotero数据
    items_file = r"E:\仓库\毕业论文\zotero_items.json"
    
    try:
        with open(items_file, 'r', encoding='utf-8') as f:
            items = json.load(f)
    except Exception as e:
        print(f"读取文件失败: {e}")
        return
    
    # 过滤出有效的文献条目（排除附件）
    valid_items = []
    for item in items:
        if item.get('itemType') != 'attachment' and item.get('title'):
            valid_items.append(item)
    
    # 按添加时间排序
    valid_items.sort(key=lambda x: x.get('dateAdded', ''), reverse=True)
    
    print("=== 最近添加的文献详细信息 ===")
    print(f"有效文献总数: {len(valid_items)}")
    
    # 显示前10篇最近添加的文献
    recent_items = valid_items[:10]
    
    for i, item in enumerate(recent_items, 1):
        print(f"\n{'='*80}")
        print(f"{i}. {item.get('title', '未知标题')}")
        print(f"   Key: {item.get('key', '')}")
        print(f"   添加时间: {item.get('dateAdded', '未知')}")
        print(f"   修改时间: {item.get('dateModified', '未知')}")
        
        # 作者信息
        creators = item.get('creators', [])
        if creators:
            author_list = []
            for creator in creators:
                if creator.get('name'):
                    author_list.append(creator['name'])
                elif creator.get('firstName') and creator.get('lastName'):
                    author_list.append(f"{creator['lastName']} {creator['firstName']}")
                elif creator.get('lastName'):
                    author_list.append(creator['lastName'])
            print(f"   作者: {', '.join(author_list)}")
        else:
            print(f"   作者: 未知")
        
        # 基本信息
        print(f"   年份: {item.get('date', '未知')}")
        print(f"   期刊: {item.get('publicationTitle', '未知')}")
        print(f"   类型: {item.get('itemType', '未知')}")
        
        # 详细信息
        if item.get('volume'):
            print(f"   卷: {item['volume']}")
        if item.get('issue'):
            print(f"   期: {item['issue']}")
        if item.get('pages'):
            print(f"   页码: {item['pages']}")
        if item.get('publisher'):
            print(f"   出版社: {item['publisher']}")
        if item.get('language'):
            print(f"   语言: {item['language']}")
        
        # 摘要
        abstract = item.get('abstractNote', '')
        if abstract:
            if len(abstract) > 500:
                abstract = abstract[:500] + "..."
            print(f"   摘要: {abstract}")
        else:
            print(f"   摘要: 无")
        
        # 标签
        tags = item.get('tags', [])
        if tags:
            tag_list = [tag.get('tag', '') for tag in tags if tag.get('tag')]
            print(f"   标签: {', '.join(tag_list)}")
        
        # URL和DOI
        if item.get('url'):
            print(f"   URL: {item['url']}")
        if item.get('doi'):
            print(f"   DOI: {item['doi']}")
        
        # 笔记数量
        notes = item.get('notes', [])
        print(f"   笔记数量: {len(notes)}")
    
    return recent_items

def analyze_literature_characteristics(items):
    """分析文献特征"""
    print(f"\n=== 文献特征分析 ===")
    
    # 年份分布
    years = []
    for item in items:
        date = item.get('date', '')
        year_match = re.search(r'\b(19|20)\d{2}\b', date)
        if year_match:
            years.append(int(year_match.group()))
    
    if years:
        year_count = {}
        for year in years:
            year_count[year] = year_count.get(year, 0) + 1
        print(f"年份分布: {dict(sorted(year_count.items()))}")
    
    # 期刊分布
    journals = {}
    for item in items:
        journal = item.get('publicationTitle', '')
        if journal:
            journals[journal] = journals.get(journal, 0) + 1
    
    if journals:
        print(f"期刊分布 (前5): {dict(sorted(journals.items(), key=lambda x: x[1], reverse=True)[:5])}")
    
    # 文献类型分布
    types = {}
    for item in items:
        item_type = item.get('itemType', '')
        if item_type:
            types[item_type] = types.get(item_type, 0) + 1
    print(f"文献类型分布: {types}")
    
    # 有无笔记统计
    with_notes = sum(1 for item in items if item.get('notes'))
    without_notes = len(items) - with_notes
    print(f"有笔记的文献: {with_notes} 篇")
    print(f"无笔记的文献: {without_notes} 篇")

def check_for_foreign_content(items):
    """检查是否有外文内容"""
    print(f"\n=== 外文内容检查 ===")
    
    potential_foreign = []
    
    for item in items:
        title = item.get('title', '')
        abstract = item.get('abstractNote', '')
        publication = item.get('publicationTitle', '')
        
        # 检查英文标题
        if re.search(r'^[a-zA-Z\s:,-.?]+$', title) and len(title) > 10:
            potential_foreign.append({
                'title': title,
                'reason': '英文标题',
                'publication': publication
            })
        
        # 检查英文摘要
        if abstract and re.search(r'^[a-zA-Z\s:,-.?]+$', abstract[:100]):
            potential_foreign.append({
                'title': title,
                'reason': '英文摘要',
                'publication': publication
            })
        
        # 检查英文期刊
        if publication and re.search(r'^[a-zA-Z\s:,-.?]+$', publication):
            potential_foreign.append({
                'title': title,
                'reason': '英文期刊名称',
                'publication': publication
            })
    
    if potential_foreign:
        print(f"发现 {len(potential_foreign)} 个可能的外文内容:")
        for item in potential_foreign:
            print(f"  - {item['title'][:50]}... ({item['reason']})")
    else:
        print("未发现明显的外文内容")
    
    return potential_foreign

def main():
    """主函数"""
    print("=== Zotero最近文献详细分析 ===")
    
    # 获取最近文献
    recent_items = get_recent_literature_details()
    
    # 分析文献特征
    analyze_literature_characteristics(recent_items)
    
    # 检查外文内容
    foreign_items = check_for_foreign_content(recent_items)
    
    # 保存分析结果
    analysis_result = {
        'recent_literature': recent_items,
        'foreign_content_found': len(foreign_items) > 0,
        'potential_foreign_items': foreign_items,
        'analysis_time': datetime.now().isoformat(),
        'total_recent_items': len(recent_items)
    }
    
    output_file = r"E:\仓库\毕业论文\recent_literature_analysis.json"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        print(f"\n分析结果已保存到: {output_file}")
    except Exception as e:
        print(f"保存文件时出错: {e}")

if __name__ == "__main__":
    main()