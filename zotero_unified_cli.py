#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一的Zotero CLI工具
整合多种Zotero操作方式
"""

import os
import sys
import json
import argparse
from pathlib import Path
import requests
from pyzotero import zotero

# 配置
CONFIG_FILE = Path.home() / ".zotero" / "config.json"
CREDS_FILE = Path.home() / ".zotero" / "creds.txt"

class ZoteroUnifiedCLI:
    def __init__(self):
        self.config = self.load_config()
        self.zot = None
        
    def load_config(self):
        """加载配置文件"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "api_key": "CIApUKos6l9E0GOaCBrILRrt",
                "library_id": "18982351",
                "library_type": "user"
            }
    
    def get_zotero(self):
        """获取Zotero API连接"""
        if not self.zot:
            self.zot = zotero.Zotero(
                self.config['library_id'],
                self.config['library_type'],
                self.config['api_key']
            )
        return self.zot
    
    def search_items(self, query, limit=10):
        """搜索文献"""
        zot = self.get_zotero()
        try:
            items = zot.items(q=query, limit=limit)
            print(f"找到 {len(items)} 个结果:")
            for item in items:
                title = item.get('data', {}).get('title', '无标题')
                item_type = item.get('data', {}).get('itemType', '未知类型')
                date = item.get('data', {}).get('date', '无日期')
                print(f"- {title} ({item_type}) - {date}")
            return items
        except Exception as e:
            print(f"搜索失败: {e}")
            return []
    
    def create_item(self, title, item_type="book"):
        """创建新文献条目"""
        zot = self.get_zotero()
        template = zot.item_template(item_type)
        template['title'] = title
        
        try:
            resp = zot.create_items([template])
            if resp.get('successful'):
                item_key = resp['successful'][0]['key']
                print(f"✓ 成功创建文献: {title} (Key: {item_key})")
                return item_key
            else:
                print(f"✗ 创建失败: {resp}")
                return None
        except Exception as e:
            print(f"创建失败: {e}")
            return None
    
    def list_collections(self):
        """列出所有分类"""
        zot = self.get_zotero()
        try:
            collections = zot.collections()
            print("分类列表:")
            for collection in collections:
                name = collection['data']['name']
                parent = collection['data'].get('parentCollection', False)
                indent = "  " if parent else ""
                print(f"{indent}- {name}")
            return collections
        except Exception as e:
            print(f"获取分类失败: {e}")
            return []
    
    def add_to_collection(self, item_key, collection_name):
        """将文献添加到分类"""
        zot = self.get_zotero()
        try:
            # 查找分类
            collections = zot.collections()
            target_collection = None
            for collection in collections:
                if collection['data']['name'] == collection_name:
                    target_collection = collection
                    break
            
            if not target_collection:
                print(f"✗ 未找到分类: {collection_name}")
                return False
            
            # 添加到分类
            zot.add_to_collection(target_collection['key'], item_key)
            print(f"✓ 已将文献添加到分类: {collection_name}")
            return True
        except Exception as e:
            print(f"添加到分类失败: {e}")
            return False
    
    def import_pdf(self, pdf_path):
        """导入PDF文件"""
        if not Path(pdf_path).exists():
            print(f"✗ 文件不存在: {pdf_path}")
            return False
        
        # 使用现有的导入脚本
        try:
            import subprocess
            result = subprocess.run([
                sys.executable, 
                "E:\\仓库\\毕业论文\\zotero_auto_import.py"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ PDF导入成功: {pdf_path}")
                return True
            else:
                print(f"✗ PDF导入失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"导入PDF出错: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="统一的Zotero CLI工具")
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 搜索命令
    search_parser = subparsers.add_parser('search', help='搜索文献')
    search_parser.add_argument('query', help='搜索关键词')
    search_parser.add_argument('--limit', type=int, default=10, help='结果数量限制')
    
    # 创建命令
    create_parser = subparsers.add_parser('create', help='创建文献')
    create_parser.add_argument('title', help='文献标题')
    create_parser.add_argument('--type', default='book', help='文献类型')
    
    # 分类命令
    collections_parser = subparsers.add_parser('collections', help='列出分类')
    
    # 添加到分类命令
    addto_parser = subparsers.add_parser('addto', help='添加到分类')
    addto_parser.add_argument('item_key', help='文献Key')
    addto_parser.add_argument('collection', help='分类名称')
    
    # 导入PDF命令
    import_parser = subparsers.add_parser('import', help='导入PDF')
    import_parser.add_argument('pdf_path', help='PDF文件路径')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = ZoteroUnifiedCLI()
    
    if args.command == 'search':
        cli.search_items(args.query, args.limit)
    elif args.command == 'create':
        cli.create_item(args.title, args.type)
    elif args.command == 'collections':
        cli.list_collections()
    elif args.command == 'addto':
        cli.add_to_collection(args.item_key, args.collection)
    elif args.command == 'import':
        cli.import_pdf(args.pdf_path)

if __name__ == "__main__":
    main()