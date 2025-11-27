#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建毕业论文分类并移动文献
"""

import requests
import json
import time

# Zotero API配置
API_KEY = "CIApUKos6l9E0GOaCBrILRrt"
LIBRARY_ID = "18982351"
LIBRARY_TYPE = "user"

def create_collection(name):
    """创建新的分类"""
    
    url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{LIBRARY_ID}/collections"
    headers = {
        "Zotero-API-Version": "3",
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    collection_data = {
        "name": name,
        "parentCollection": False  # 顶级分类
    }
    
    try:
        print(f"正在创建分类: {name}")
        response = requests.post(url, headers=headers, data=json.dumps([collection_data]))
        
        if response.status_code == 200:
            result = response.json()
            if result.get('successful'):
                collection = result['successful'][0]
                collection_key = collection['key']
                collection_version = collection['version']
                print(f"✓ 分类创建成功")
                print(f"   名称: {name}")
                print(f"   Key: {collection_key}")
                print(f"   Version: {collection_version}")
                return collection_key, collection_version
            else:
                print(f"✗ 创建失败: {result}")
                return None, None
        else:
            print(f"✗ API请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"✗ 创建分类出错: {str(e)}")
        return None, None

def find_item_by_title(title):
    """根据标题查找文献条目"""
    
    url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{LIBRARY_ID}/items"
    headers = {
        "Zotero-API-Version": "3",
        "Authorization": f"Bearer {API_KEY}"
    }
    params = {
        "q": title,
        "limit": 10
    }
    
    try:
        print(f"正在查找文献: {title}")
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            items = response.json()
            
            for item in items:
                data = item.get('data', {})
                item_title = data.get('title', '')
                item_type = data.get('itemType', '')
                
                if title in item_title and item_type == 'journalArticle':
                    print(f"✓ 找到文献条目: {item_title}")
                    print(f"   Key: {data.get('key')}")
                    print(f"   Version: {data.get('version')}")
                    return data.get('key'), data.get('version'), item
            
            print("✗ 未找到匹配的文献条目")
            return None, None, None
        else:
            print(f"✗ 查询失败: {response.status_code}")
            return None, None, None
            
    except Exception as e:
        print(f"✗ 查询出错: {str(e)}")
        return None, None, None

def move_item_to_collection(item_key, item_version, collection_key, collection_version):
    """将文献条目移动到指定分类"""
    
    if not item_key or not collection_key:
        print("✗ 无法移动：缺少条目Key或分类Key")
        return False
    
    url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{LIBRARY_ID}/items/{item_key}"
    headers = {
        "Zotero-API-Version": "3",
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "If-Match": str(item_version)
    }
    
    # 更新条目，添加到分类
    update_data = {
        "collections": [collection_key]
    }
    
    try:
        print(f"正在将文献移动到分类...")
        response = requests.patch(url, headers=headers, data=json.dumps(update_data))
        
        if response.status_code == 200:
            print(f"✓ 文献移动成功")
            return True
        else:
            print(f"✗ 移动失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ 移动出错: {str(e)}")
        return False

def verify_changes():
    """验证更改结果"""
    print("\n验证更改结果...")
    
    # 检查分类
    collections_url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{LIBRARY_ID}/collections"
    headers = {
        "Zotero-API-Version": "3",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    try:
        response = requests.get(collections_url, headers=headers)
        if response.status_code == 200:
            collections = response.json()
            print("✓ 当前分类:")
            for collection in collections:
                data = collection.get('data', {})
                name = data.get('name', '')
                if name:
                    print(f"   - {name}")
        
        # 检查分类中的文献
        items_url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{LIBRARY_ID}/items"
        params = {
            "q": "人工智能赋能初中英语项目式学习策略探究",
            "limit": 5
        }
        
        response = requests.get(items_url, headers=headers, params=params)
        if response.status_code == 200:
            items = response.json()
            print("\n✓ 文献状态:")
            for item in items:
                data = item.get('data', {})
                title = data.get('title', '')
                collections = data.get('collections', [])
                
                if "人工智能赋能初中英语项目式学习策略探究" in title:
                    print(f"   标题: {title}")
                    print(f"   所属分类: {len(collections)} 个")
                    if collections:
                        print(f"   分类Keys: {collections}")
        
        print("\n✓ 验证完成！请检查本地Zotero是否同步显示新的分类结构")
        
    except Exception as e:
        print(f"✗ 验证出错: {str(e)}")

def main():
    """主函数"""
    print("=== 创建毕业论文分类并移动文献 ===\n")
    
    # 1. 创建"毕业论文"分类
    collection_key, collection_version = create_collection("毕业论文")
    
    if collection_key:
        # 2. 查找文献条目
        item_key, item_version, item_data = find_item_by_title("人工智能赋能初中英语项目式学习策略探究")
        
        if item_key:
            # 3. 移动文献到分类
            if move_item_to_collection(item_key, item_version, collection_key, collection_version):
                print("\n✓ 操作成功完成！")
                # 4. 验证结果
                verify_changes()
            else:
                print("\n✗ 文献移动失败")
        else:
            print("\n✗ 未找到文献条目")
    else:
        print("\n✗ 分类创建失败")

if __name__ == "__main__":
    main()