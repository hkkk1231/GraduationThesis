#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
from datetime import datetime

def load_zotero_data():
    """加载Zotero文献数据"""
    try:
        with open(r"E:\仓库\毕业论文\zotero_items_without_notes.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("未找到Zotero数据文件")
        return []

def get_existing_notes():
    """获取已存在的笔记列表"""
    notes_dir = r"E:\仓库\毕业论文\obsidian\毕业论文\AI笔记\文献笔记"
    existing_notes = set()
    
    if os.path.exists(notes_dir):
        for filename in os.listdir(notes_dir):
            if filename.endswith('.md'):
                # 提取文献标题和作者信息
                existing_notes.add(filename[:-3])  # 去掉.md后缀
    
    return existing_notes

def format_creators(creators):
    """格式化作者信息"""
    if not creators:
        return "未知"
    
    authors = []
    for creator in creators:
        if creator.get('name'):
            authors.append(creator['name'])
        elif creator.get('lastName') and creator.get('firstName'):
            authors.append(f"{creator['lastName']} {creator['firstName']}")
        elif creator.get('lastName'):
            authors.append(creator['lastName'])
    
    return ', '.join(authors) if authors else "未知"

def format_tags(tags):
    """格式化标签"""
    if not tags:
        return ""
    
    tag_list = []
    for tag in tags:
        if isinstance(tag, dict):
            tag_list.append(tag.get('tag', ''))
        elif isinstance(tag, str):
            tag_list.append(tag)
    
    return ', '.join([tag for tag in tag_list if tag])

def generate_filename(item):
    """生成文件名"""
    title = item.get('title', '')
    creators = item.get('creators', [])
    date = item.get('date', '')
    
    # 获取第一作者
    first_author = "未知"
    if creators:
        creator = creators[0]
        if creator.get('name'):
            first_author = creator['name']
        elif creator.get('lastName'):
            first_author = creator['lastName']
    
    # 清理标题，移除特殊字符
    clean_title = re.sub(r'[<>:"/\\|?*]', '', title)
    clean_title = clean_title.replace('\n', ' ').strip()
    
    # 限制长度
    if len(clean_title) > 50:
        clean_title = clean_title[:50] + '...'
    
    # 构建文件名
    if date and date.strip():
        filename = f"{first_author}_{date}_{clean_title}"
    else:
        filename = f"{first_author}_{clean_title}"
    
    return filename

def generate_bibtex(item):
    """生成BibTeX引用格式"""
    creators = item.get('creators', [])
    title = item.get('title', '')
    publication = item.get('publicationTitle', '')
    date = item.get('date', '')
    key = item.get('key', '')
    
    # 格式化作者
    author_list = []
    for creator in creators:
        if creator.get('name'):
            author_list.append(creator['name'])
        elif creator.get('lastName'):
            author_list.append(creator['lastName'])
    
    authors = ' and '.join(author_list)
    
    # 生成BibTeX
    bibtex = f"@article{{{key},\n"
    bibtex += f"  title={{{title}}},\n"
    if authors:
        bibtex += f"  author={{{authors}}},\n"
    if publication:
        bibtex += f"  journal={{{publication}}},\n"
    if date:
        bibtex += f"  year={{{date}}}\n"
    bibtex += "}"
    
    return bibtex

def create_note_content(item, template_path):
    """创建笔记内容"""
    # 读取模板
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 准备替换数据
    title = item.get('title', '')
    authors = format_creators(item.get('creators', []))
    publication = item.get('publicationTitle', '未知')
    date = item.get('date', '未知')
    abstract = item.get('abstractNote', '无摘要')
    item_type = item.get('itemType', '未知')
    tags = format_tags(item.get('tags', []))
    key = item.get('key', '')
    
    # 生成BibTeX
    bibtex = generate_bibtex(item)
    
    # 获取第一个标签作为主要标签
    first_tag = "未分类"
    if item.get('tags'):
        first_tag_obj = item['tags'][0]
        if isinstance(first_tag_obj, dict):
            first_tag = first_tag_obj.get('tag', '未分类')
        elif isinstance(first_tag_obj, str):
            first_tag = first_tag_obj
    
    # 替换模板变量
    replacements = {
        '{{title}}': title,
        '{{authors}}': authors,
        '{{publication}}': publication,
        '{{year}}': date,
        '{{doi}}': '',
        '{{citekey}}': key,
        '{{itemType}}': item_type,
        '{{tags}}': tags,
        '{{collections}}': '',
        '{{dateAdded}}': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        '{{abstract}}': abstract,
        '{{bibtex}}': bibtex,
        '{{firstTag}}': first_tag,
        '{{date}}': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    content = template
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    
    return content

def main():
    """主函数"""
    print("=== 批量生成文献笔记工具 ===")
    
    # 加载数据
    items = load_zotero_data()
    if not items:
        return
    
    # 获取已存在的笔记
    existing_notes = get_existing_notes()
    print(f"已存在 {len(existing_notes)} 个笔记")
    
    # 模板路径
    template_path = r"E:\仓库\毕业论文\obsidian\毕业论文\AI笔记\模板\文献笔记模板.md"
    if not os.path.exists(template_path):
        print(f"模板文件不存在: {template_path}")
        return
    
    # 输出目录
    output_dir = r"E:\仓库\毕业论文\obsidian\毕业论文\AI笔记\文献笔记"
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成笔记
    created_count = 0
    skipped_count = 0
    
    for i, item in enumerate(items, 1):
        # 跳过笔记类型的条目
        if item.get('itemType') == 'note':
            continue
        
        # 生成文件名
        filename = generate_filename(item)
        
        # 检查是否已存在
        if filename in existing_notes:
            print(f"{i}. 跳过已存在的笔记: {filename}")
            skipped_count += 1
            continue
        
        # 创建笔记内容
        try:
            content = create_note_content(item, template_path)
            
            # 写入文件
            filepath = os.path.join(output_dir, f"{filename}.md")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"{i}. 创建笔记: {filename}")
            created_count += 1
            
        except Exception as e:
            print(f"{i}. 创建笔记失败: {filename} - {e}")
    
    print(f"\n=== 完成 ===")
    print(f"总共处理: {len(items)} 个文献")
    print(f"创建笔记: {created_count} 个")
    print(f"跳过已存在: {skipped_count} 个")
    print(f"输出目录: {output_dir}")

if __name__ == "__main__":
    main()