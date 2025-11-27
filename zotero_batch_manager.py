#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zotero批量管理工具
提供批量导入、分类管理等功能
"""

import os
import json
import argparse
from pathlib import Path
from zotero_unified_cli import ZoteroUnifiedCLI

class ZoteroBatchManager(ZoteroUnifiedCLI):
    def __init__(self):
        super().__init__()
        
    def batch_import_pdfs(self, pdf_dir, collection_name=None):
        """批量导入PDF文件"""
        pdf_dir = Path(pdf_dir)
        if not pdf_dir.exists():
            print(f"✗ 目录不存在: {pdf_dir}")
            return False
            
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            print(f"✗ 目录中没有PDF文件: {pdf_dir}")
            return False
            
        print(f"找到 {len(pdf_files)} 个PDF文件")
        
        for pdf_file in pdf_files:
            print(f"\n处理: {pdf_file.name}")
            if self.import_pdf(str(pdf_file)):
                print(f"✓ 导入成功: {pdf_file.name}")
            else:
                print(f"✗ 导入失败: {pdf_file.name}")
        
        return True
    
    def create_collection_structure(self, structure):
        """创建分类结构
        
        Args:
            structure: 字典格式的分类结构，例如:
            {
                "教育学": {
                    "英语教学": {},
                    "数学教学": {}
                },
                "计算机科学": {
                    "人工智能": {},
                    "机器学习": {}
                }
            }
        """
        zot = self.get_zotero()
        
        def create_recursive(parent_key, collection_name, children):
            """递归创建分类"""
            try:
                # 创建当前分类
                collection_data = {
                    'name': collection_name,
                    'parentCollection': parent_key
                }
                
                resp = zot.create_collections([collection_data])
                if resp.get('successful'):
                    collection_key = resp['successful'][0]['key']
                    print(f"✓ 创建分类: {collection_name} (Key: {collection_key})")
                    
                    # 递归创建子分类
                    for child_name, child_children in children.items():
                        create_recursive(collection_key, child_name, child_children)
                else:
                    print(f"✗ 创建分类失败: {collection_name}")
            except Exception as e:
                print(f"创建分类出错: {e}")
        
        print("开始创建分类结构...")
        for name, children in structure.items():
            create_recursive(False, name, children)
        
        print("分类结构创建完成！")
    
    def auto_classify_by_keywords(self, keywords_mapping):
        """根据关键词自动分类
        
        Args:
            keywords_mapping: 关键词到分类的映射，例如:
            {
                "英语教学": ["英语", "English", "语言", "Language"],
                "人工智能": ["AI", "人工智能", "机器学习", "深度学习"]
            }
        """
        zot = self.get_zotero()
        
        # 获取所有分类
        collections = zot.collections()
        collection_map = {c['data']['name']: c['key'] for c in collections}
        
        # 获取所有文献
        items = zot.items(limit=100)  # 限制数量避免过多
        
        classified_count = 0
        for item in items:
            item_data = item.get('data', {})
            title = item_data.get('title', '').lower()
            item_key = item_data.get('key')
            
            # 检查关键词
            for collection_name, keywords in keywords_mapping.items():
                if collection_name not in collection_map:
                    continue
                    
                for keyword in keywords:
                    if keyword.lower() in title:
                        # 添加到分类
                        try:
                            zot.add_to_collection(collection_map[collection_name], item_key)
                            print(f"✓ 已分类: {title} -> {collection_name}")
                            classified_count += 1
                            break
                        except Exception as e:
                            print(f"✗ 分类失败: {title} -> {collection_name}: {e}")
        
        print(f"\n自动分类完成，共分类 {classified_count} 篇文献")
    
    def export_library_summary(self, output_file):
        """导出文献库摘要"""
        zot = self.get_zotero()
        
        try:
            # 获取统计信息
            items = zot.items(limit=1000)
            collections = zot.collections()
            
            # 按类型统计
            type_stats = {}
            for item in items:
                item_type = item.get('data', {}).get('itemType', 'unknown')
                type_stats[item_type] = type_stats.get(item_type, 0) + 1
            
            # 按分类统计
            collection_stats = {}
            for collection in collections:
                collection_stats[collection['data']['name']] = collection['data'].get('numItems', 0)
            
            # 生成摘要
            summary = {
                "total_items": len(items),
                "total_collections": len(collections),
                "items_by_type": type_stats,
                "items_by_collection": collection_stats,
                "recent_items": [
                    {
                        "title": item.get('data', {}).get('title', ''),
                        "type": item.get('data', {}).get('itemType', ''),
                        "date": item.get('data', {}).get('date', '')
                    }
                    for item in items[:10]
                ]
            }
            
            # 保存到文件
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            print(f"✓ 文献库摘要已导出到: {output_file}")
            print(f"总计文献: {summary['total_items']}")
            print(f"总计分类: {summary['total_collections']}")
            
        except Exception as e:
            print(f"导出摘要失败: {e}")

def main():
    parser = argparse.ArgumentParser(description="Zotero批量管理工具")
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 批量导入
    import_parser = subparsers.add_parser('batch-import', help='批量导入PDF')
    import_parser.add_argument('pdf_dir', help='PDF目录路径')
    import_parser.add_argument('--collection', help='目标分类')
    
    # 创建分类结构
    struct_parser = subparsers.add_parser('create-structure', help='创建分类结构')
    struct_parser.add_argument('config_file', help='分类结构配置文件(JSON)')
    
    # 自动分类
    auto_parser = subparsers.add_parser('auto-classify', help='根据关键词自动分类')
    auto_parser.add_argument('keywords_file', help='关键词映射文件(JSON)')
    
    # 导出摘要
    export_parser = subparsers.add_parser('export-summary', help='导出文献库摘要')
    export_parser.add_argument('output_file', help='输出文件路径')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = ZoteroBatchManager()
    
    if args.command == 'batch-import':
        manager.batch_import_pdfs(args.pdf_dir, args.collection)
    elif args.command == 'create-structure':
        with open(args.config_file, 'r', encoding='utf-8') as f:
            structure = json.load(f)
        manager.create_collection_structure(structure)
    elif args.command == 'auto-classify':
        with open(args.keywords_file, 'r', encoding='utf-8') as f:
            keywords_mapping = json.load(f)
        manager.auto_classify_by_keywords(keywords_mapping)
    elif args.command == 'export-summary':
        manager.export_library_summary(args.output_file)

if __name__ == "__main__":
    main()