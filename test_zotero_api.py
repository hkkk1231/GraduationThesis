#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

# Zotero API配置
API_KEY = 'CIApUKos6l9E0GOaCBrILRrt'
LIBRARY_ID = '18982351'
BASE_URL = 'https://api.zotero.org'

def test_api_connection():
    """测试API连接"""
    print("=== 测试Zotero API连接 ===")
    
    headers = {
        'Zotero-API-Key': API_KEY
    }
    
    # 1. 测试API密钥
    print("\n1. 测试API密钥...")
    try:
        response = requests.get(f"{BASE_URL}/keys/current", headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            user_info = response.json()
            print(f"用户信息: {user_info}")
            print(f"用户ID: {user_info.get('user', {}).get('id', '未知')}")
        else:
            print(f"错误响应: {response.text}")
    except Exception as e:
        print(f"API密钥测试失败: {e}")
    
    # 2. 测试库信息
    print(f"\n2. 测试库信息 (ID: {LIBRARY_ID})...")
    try:
        response = requests.get(f"{BASE_URL}/users/{LIBRARY_ID}/collections", headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            collections = response.json()
            print(f"集合数量: {len(collections)}")
        else:
            print(f"错误响应: {response.text}")
    except Exception as e:
        print(f"库信息测试失败: {e}")
    
    # 3. 测试文献获取（简化版）
    print(f"\n3. 测试文献获取...")
    try:
        response = requests.get(f"{BASE_URL}/users/{LIBRARY_ID}/items?format=json&limit=5", headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            items = response.json()
            print(f"获取到 {len(items)} 个文献")
            if items:
                first_item = items[0]
                data = first_item.get('data', {})
                print(f"第一个文献标题: {data.get('title', '未知')}")
        else:
            print(f"错误响应: {response.text}")
    except Exception as e:
        print(f"文献获取测试失败: {e}")

if __name__ == "__main__":
    test_api_connection()