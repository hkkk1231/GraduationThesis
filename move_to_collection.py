#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将文献移动到毕业论文分类
"""

import requests
import json

# Zotero API配置
API_KEY = "CIApUKos6l9E0GOaCBrILRrt"
LIBRARY_ID = "18982351"
LIBRARY_TYPE = "user"

def get_collection_key(collection_name):
    """获取分类的Key"""
    
    url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{LIBRARY_ID}/collections"
    headers = {
        "Zotero-API-Version": "3",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            collections = response.json()
            
            for collection in collections:
                data = collection.get('data', {})
                name = data.get('name', '')
                key = data.get('key', '')
                
                if name == collection_name:
                    print(f"✓ 找到分类: {name} (Key: {key})")
                    return key, data.get('version', 0)
            
            print(f"✗ 未找到分类: {collection_name}")
            return None, None
        else:
            print(f"✗ 获取分类失败: {response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"✗ 查询分类出错: {str(e)}")
        return None, None

def find_item_key(title):
    """查找文献条目的Key"""
    
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
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            items = response.json()
            
            for item in items:
                data = item.get('data', {})
                item_title = data.get('title', '')
                item_type = data.get('itemType', '')
                
                if title in item_title and item_type == 'journalArticle':
                    print(f"✓ 找到文献: {item_title}")
                    print(f"   Key: {data.get('key')}")
                    print(f"   Version: {data.get('version')}")
                    return data.get('key'), data.get('version', 0), data
            
            print(f"✗ 未找到文献: {title}")
            return None, None, None
        else:
            print(f"✗ 查找文献失败: {response.status_code}")
            return None, None, None
            
    except Exception as e:
        print(f"✗ 查找文献出错: {str(e)}")
        return None, None, None

def move_item_to_collection(item_key, item_version, item_data, collection_key):
    """移动文献到分类"""
    
    url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{LIBRARY_ID}/items/{item_key}"
    headers = {
        "Zotero-API-Version": "3",
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "If-Match": str(item_version)
    }
    
    # 更新文献，添加到分类
    updated_data = item_data.copy()
    updated_data['collections'] = [collection_key]
    
    try:
        print(f"正在移动文献到分类...")
        
        response = requests.patch(url, headers=headers, data=json.dumps(updated_data))
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✓ 文献移动成功！")
            return True
        else:
            print(f"✗ 移动失败: {response.status_code}")
            if response.text:
                print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ 移动出错: {str(e)}")
        return False

def verify_move():
    """验证移动结果"""
    
    print("\n验证移动结果...")
    
    # 查找毕业论文分类中的文献
    collection_key, _ = get_collection_key("毕业论文")
    
    if collection_key:
        url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{LIBRARY_ID}/collections/{collection_key}/items"
        headers = {
            "Zotero-API-Version": "3",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                items = response.json()
                print(f"✓ '毕业论文'分类中有 {len(items)} 个文献:")
                
                for item in items:
                    data = item.get('data', {})
                    title = data.get('title', '')
                    item_type = data.get('itemType', '')
                    
                    print(f"   - {title} ({item_type})")
                
                return len(items) > 0
            else:
                print(f"✗ 验证失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ 验证出错: {str(e)}")
            return False
    
    return False

def main():
    """主函数"""
    print("=== 移动文献到毕业论文分类 ===\n")
    
    # 1. 获取毕业论文分类的Key
    collection_key, collection_version = get_collection_key("毕业论文")
    
    if not collection_key:
        print("无法找到毕业论文分类")
        return
    
    # 2. 查找文献条目
    item_key, item_version, item_data = find_item_key("人工智能赋能初中英语项目式学习策略探究")
    
    if not item_key:
        print("无法找到文献条目")
        return
    
    # 3. 移动文献到分类
    if move_item_to_collection(item_key, item_version, item_data, collection_key):
        print("\n✓ 操作完成！")
        
        # 4. 验证结果
        if verify_move():
            print("\n🎉 文献已成功移动到'毕业论文'分类！")
            print("请检查本地Zotero是否同步显示")
        else:
            print("\n⚠️ 移动可能未成功，请手动检查")
    else:
        print("\n✗ 文献移动失败")

if __name__ == "__main__":
    main()