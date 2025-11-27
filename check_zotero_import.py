#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查Zotero中是否成功导入PDF文件
"""

import requests
import json
from datetime import datetime

# Zotero API配置（从之前的mcp_config.json获取）
API_KEY = "CIApUKos6l9E0GOaCBrILRrt"
LIBRARY_ID = "18982351"
LIBRARY_TYPE = "user"

def check_zotero_items():
    """查询Zotero库中的项目"""
    try:
        # API端点
        url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{LIBRARY_ID}/items"
        
        # 请求头
        headers = {
            "Zotero-API-Version": "3",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        # 查询参数 - 获取最近添加的项目
        params = {
            "limit": 10,
            "sort": "dateAdded",
            "direction": "desc"
        }
        
        print("正在查询Zotero库中的项目...")
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            items = response.json()
            print(f"✓ 成功获取 {len(items)} 个最新项目\n")
            
            # 查找PDF文件
            pdf_found = False
            for item in items:
                data = item.get('data', {})
                item_type = data.get('itemType', '')
                title = data.get('title', '')
                date_added = data.get('dateAdded', '')
                
                # 检查是否是附件
                if item_type == 'attachment':
                    filename = data.get('filename', '')
                    content_type = data.get('contentType', '')
                    
                    if filename.endswith('.pdf') or 'pdf' in content_type.lower():
                        pdf_found = True
                        print(f"📄 找到PDF文件:")
                        print(f"   标题: {title}")
                        print(f"   文件名: {filename}")
                        print(f"   添加时间: {date_added}")
                        
                        # 获取父项目信息
                        parent_key = data.get('parentItem')
                        if parent_key:
                            parent_url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{LIBRARY_ID}/items/{parent_key}"
                            parent_response = requests.get(parent_url, headers=headers)
                            if parent_response.status_code == 200:
                                parent_data = parent_response.json().get('data', {})
                                parent_title = parent_data.get('title', '')
                                print(f"   父项目标题: {parent_title}")
                        print()
                
                # 检查是否是包含PDF附件的项目
                elif '人工智能' in title or '英语' in title:
                    print(f"📚 找到相关文献:")
                    print(f"   标题: {title}")
                    print(f"   类型: {item_type}")
                    print(f"   添加时间: {date_added}")
                    
                    # 查找附件
                    attachments_url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{LIBRARY_ID}/items/{item['key']}/children"
                    attachments_response = requests.get(attachments_url, headers=headers)
                    if attachments_response.status_code == 200:
                        attachments = attachments_response.json()
                        for attachment in attachments:
                            att_data = attachment.get('data', {})
                            if att_data.get('itemType') == 'attachment':
                                att_filename = att_data.get('filename', '')
                                if att_filename.endswith('.pdf'):
                                    print(f"   附件: {att_filename}")
                                    pdf_found = True
                    print()
            
            if not pdf_found:
                print("⚠️  未找到PDF文件")
                print("\n最近添加的项目:")
                for item in items[:5]:
                    data = item.get('data', {})
                    print(f"- {data.get('title', '无标题')} ({data.get('itemType', '未知类型')})")
        else:
            print(f"✗ API请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"✗ 查询出错: {str(e)}")

def check_zotero_connection():
    """检查Zotero连接状态"""
    try:
        url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{LIBRARY_ID}/items/top"
        headers = {
            "Zotero-API-Version": "3",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        response = requests.get(url, headers=headers, params={"limit": 1})
        
        if response.status_code == 200:
            print("✓ Zotero API连接正常")
            return True
        else:
            print(f"✗ Zotero API连接失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 连接检查出错: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Zotero导入状态检查 ===\n")
    
    if check_zotero_connection():
        check_zotero_items()
    
    print("\n=== 检查完成 ===")