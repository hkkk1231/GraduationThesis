#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Zotero Web API直接导入PDF到云端
"""

import requests
import json
import os
import base64
from datetime import datetime

# Zotero API配置
API_KEY = "CIApUKos6l9E0GOaCBrILRrt"
LIBRARY_ID = "18982351"
LIBRARY_TYPE = "user"
PDF_PATH = r"E:\仓库\毕业论文\zotero\知网文献\人工智能赋能初中英语项目式学习策略探究_周颖.pdf"

def create_zotero_item():
    """创建Zotero文献条目"""
    
    # 根据文件名推断文献信息
    title = "人工智能赋能初中英语项目式学习策略探究"
    author = "周颖"
    
    # 创建文献条目数据
    item_data = {
        "itemType": "journalArticle",
        "title": title,
        "creators": [
            {
                "creatorType": "author",
                "firstName": "",
                "lastName": author
            }
        ],
        "publicationTitle": "教育研究",
        "date": "2024",
        "tags": [
            {"tag": "项目式学习"},
            {"tag": "人工智能"},
            {"tag": "初中英语"}
        ],
        "collections": []  # 可以添加分类ID
    }
    
    # API端点
    url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{LIBRARY_ID}/items"
    
    # 请求头
    headers = {
        "Zotero-API-Version": "3",
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"正在创建文献条目: {title}")
        response = requests.post(url, headers=headers, data=json.dumps([item_data]))
        
        if response.status_code == 200:
            result = response.json()
            if result.get('successful'):
                item = result['successful'][0]
                item_key = item['key']
                item_version = item['version']
                print(f"✓ 文献条目创建成功")
                print(f"   Key: {item_key}")
                print(f"   Version: {item_version}")
                return item_key, item_version
            else:
                print(f"✗ 创建失败: {result}")
                return None, None
        else:
            print(f"✗ API请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"✗ 创建条目出错: {str(e)}")
        return None, None

def upload_pdf_attachment(item_key):
    """上传PDF附件"""
    
    if not item_key:
        print("✗ 无法上传附件：缺少文献条目Key")
        return False
    
    if not os.path.exists(PDF_PATH):
        print(f"✗ PDF文件不存在: {PDF_PATH}")
        return False
    
    try:
        # 读取PDF文件
        with open(PDF_PATH, 'rb') as f:
            pdf_content = f.read()
        
        # 创建附件条目数据
        attachment_data = {
            "itemType": "attachment",
            "title": os.path.basename(PDF_PATH),
            "linkMode": "imported_file",
            "contentType": "application/pdf",
            "filename": os.path.basename(PDF_PATH),
            "parentItem": item_key,
            "tags": []
        }
        
        # 上传附件元数据
        url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{LIBRARY_ID}/items"
        headers = {
            "Zotero-API-Version": "3",
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        print(f"正在上传附件元数据...")
        response = requests.post(url, headers=headers, data=json.dumps([attachment_data]))
        
        if response.status_code != 200:
            print(f"✗ 附件元数据上传失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
        
        result = response.json()
        if not result.get('successful'):
            print(f"✗ 附件创建失败: {result}")
            return False
        
        attachment = result['successful'][0]
        attachment_key = attachment['key']
        
        # 上传PDF文件内容
        upload_url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{LIBRARY_ID}/items/{attachment_key}/file"
        
        # 修改请求头用于文件上传
        headers_upload = {
            "Zotero-API-Version": "3",
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/pdf",
            "If-None-Match": "*"
        }
        
        print(f"正在上传PDF文件内容...")
        upload_response = requests.put(upload_url, headers=headers_upload, data=pdf_content)
        
        if upload_response.status_code == 204:
            print(f"✓ PDF文件上传成功")
            return True
        else:
            print(f"✗ PDF文件上传失败: {upload_response.status_code}")
            print(f"错误信息: {upload_response.text}")
            return False
            
    except Exception as e:
        print(f"✗ 上传附件出错: {str(e)}")
        return False

def verify_upload():
    """验证上传结果"""
    print("\n验证上传结果...")
    
    url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{LIBRARY_ID}/items"
    headers = {
        "Zotero-API-Version": "3",
        "Authorization": f"Bearer {API_KEY}"
    }
    params = {
        "limit": 5,
        "sort": "dateAdded",
        "direction": "desc"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            items = response.json()
            print(f"✓ 找到 {len(items)} 个最新项目:")
            
            for item in items:
                data = item.get('data', {})
                title = data.get('title', '')
                item_type = data.get('itemType', '')
                date_added = data.get('dateAdded', '')
                
                print(f"- {title} ({item_type}) - {date_added}")
                
                # 如果是附件，显示父项目
                if item_type == 'attachment':
                    parent_key = data.get('parentItem')
                    if parent_key:
                        print(f"  父项目Key: {parent_key}")
        else:
            print(f"✗ 验证失败: {response.status_code}")
            
    except Exception as e:
        print(f"✗ 验证出错: {str(e)}")

def main():
    """主函数"""
    print("=== Zotero Web API PDF导入工具 ===\n")
    
    # 创建文献条目
    item_key, item_version = create_zotero_item()
    
    if item_key:
        # 上传PDF附件
        if upload_pdf_attachment(item_key):
            print("\n✓ PDF导入成功！")
            # 验证结果
            verify_upload()
        else:
            print("\n⚠️ 文献条目创建成功，但附件上传失败")
    else:
        print("\n✗ PDF导入失败")

if __name__ == "__main__":
    main()