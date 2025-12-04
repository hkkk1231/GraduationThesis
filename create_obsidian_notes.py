#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
from datetime import datetime

def sanitize_filename(title):
    """清理文件名，移除不合法字符"""
    # 移除或替换不合法字符
    title = re.sub(r'[<>:"/\\|?*]', '', title)
    title = title.replace('\n', ' ').replace('\r', ' ')
    # 限制长度
    if len(title) > 100:
        title = title[:100] + "..."
    return title.strip()

def generate_bibtex_citation(item):
    """生成GB/T 7714-2015格式的引用"""
    title = item.get('title', '')
    authors = item.get('creators', [])
    year = item.get('date', '')
    publication = item.get('publicationTitle', '')
    
    # 处理作者
    author_list = []
    for creator in authors:
        if creator.get('name'):
            author_list.append(creator['name'])
    
    author_str = ', '.join(author_list) if author_list else '未知作者'
    
    # 提取年份
    year_match = re.search(r'\b(19|20)\d{2}\b', year)
    year_str = year_match.group() if year_match else year
    
    # 生成引用
    if publication:
        citation = f"[1] {author_str}. {title}[J]. {publication}, {year_str}"
    else:
        citation = f"[1] {author_str}. {title}[J]. 未明确期刊, {year_str}"
    
    return citation

def create_obsidian_note(item, template_path):
    """创建Obsidian笔记"""
    
    # 读取模板
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except Exception as e:
        print(f"读取模板失败: {e}")
        return None
    
    # 处理作者信息
    creators = item.get('creators', [])
    author_list = []
    for creator in creators:
        if creator.get('name'):
            author_list.append(creator['name'])
        elif creator.get('lastName') and creator.get('firstName'):
            author_list.append(f"{creator['lastName']} {creator['firstName']}")
    
    authors_str = ', '.join(author_list) if author_list else '未知'
    
    # 处理标签
    tags = item.get('tags', [])
    tag_list = [tag.get('tag', '') for tag in tags if tag.get('tag')]
    tags_str = ', '.join(tag_list) if tag_list else '无'
    first_tag = tag_list[0] if tag_list else '未分类'
    
    # 提取年份
    date = item.get('date', '')
    year_match = re.search(r'\b(19|20)\d{2}\b', date)
    year_str = year_match.group() if year_match else date
    
    # 生成引用
    citation = generate_bibtex_citation(item)
    
    # 替换模板变量
    note_content = template.replace('{{title}}', item.get('title', '未知标题'))
    note_content = note_content.replace('{{authors}}', authors_str)
    note_content = note_content.replace('{{publication}}', item.get('publicationTitle', '未知'))
    note_content = note_content.replace('{{year}}', year_str)
    note_content = note_content.replace('{{doi}}', item.get('doi', '无'))
    note_content = note_content.replace('{{citekey}}', item.get('key', ''))
    note_content = note_content.replace('{{itemType}}', item.get('itemType', '未知'))
    note_content = note_content.replace('{{tags}}', tags_str)
    note_content = note_content.replace('{{collections}}', '未分类')  # API不返回收藏夹信息
    note_content = note_content.replace('{{dateAdded}}', item.get('dateAdded', '未知'))
    note_content = note_content.replace('{{abstract}}', item.get('abstractNote', '无摘要'))
    note_content = note_content.replace('{{bibtex}}', citation)
    note_content = note_content.replace('{{firstTag}}', first_tag)
    note_content = note_content.replace('{{date}}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    return note_content

def main():
    """主函数"""
    print("=== 创建Obsidian文献笔记 ===")
    
    # 配置路径
    items_file = r"E:\仓库\毕业论文\zotero_items.json"
    template_path = r"E:\仓库\毕业论文\obsidian\04-工具模板\文献笔记模板\文献笔记模板.md"
    output_dir = r"E:\仓库\毕业论文\obsidian\02-文献管理\文献笔记\核心文献"
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取文献数据
    try:
        with open(items_file, 'r', encoding='utf-8') as f:
            items = json.load(f)
    except Exception as e:
        print(f"读取文献数据失败: {e}")
        return
    
    # 过滤有效的文献（排除附件和测试文献）
    valid_items = []
    for item in items:
        if (item.get('itemType') != 'attachment' and 
            item.get('title') and 
            item.get('title') != '"测试文献"' and
            not item.get('title').endswith('(1)')):  # 排除重复的附件
            valid_items.append(item)
    
    # 按添加时间排序，获取最新的5篇
    valid_items.sort(key=lambda x: x.get('dateAdded', ''), reverse=True)
    recent_items = valid_items[:5]
    
    print(f"将为最新的 {len(recent_items)} 篇文献创建Obsidian笔记")
    
    created_files = []
    
    for i, item in enumerate(recent_items, 1):
        print(f"\n{i}. 创建笔记: {item.get('title', '')}")
        
        # 生成笔记内容
        note_content = create_obsidian_note(item, template_path)
        if not note_content:
            print(f"   创建失败: 无法生成笔记内容")
            continue
        
        # 生成文件名
        title = item.get('title', '')
        year = item.get('date', '')
        year_match = re.search(r'\b(19|20)\d{2}\b', year)
        year_str = year_match.group() if year_match else ''
        
        # 提取主要作者
        creators = item.get('creators', [])
        main_author = '未知'
        if creators and creators[0].get('name'):
            main_author = creators[0]['name']
        
        # 构建文件名: 序号-年份-作者-标题
        filename = f"{i:02d}-{year_str}-{main_author}-{title}.md"
        filename = sanitize_filename(filename)
        file_path = os.path.join(output_dir, filename)
        
        # 写入文件
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(note_content)
            print(f"   创建成功: {filename}")
            created_files.append(file_path)
        except Exception as e:
            print(f"   创建失败: {e}")
    
    # 创建索引文件
    index_content = f"""# 最新文献笔记索引

**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**文献数量**: {len(created_files)}

## 文献列表

"""
    
    for i, file_path in enumerate(created_files, 1):
        filename = os.path.basename(file_path)
        title = filename.replace('.md', '').split('-', 3)[-1]  # 提取标题部分
        index_content += f"{i}. [[{filename}|{title}]]\n"
    
    index_file = os.path.join(output_dir, "最新文献笔记索引.md")
    try:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        print(f"\n索引文件已创建: 最新文献笔记索引.md")
    except Exception as e:
        print(f"创建索引文件失败: {e}")
    
    print(f"\n=== 任务完成 ===")
    print(f"成功创建 {len(created_files)} 个文献笔记")
    print(f"笔记保存在: {output_dir}")
    print(f"索引文件: {index_file}")

if __name__ == "__main__":
    main()