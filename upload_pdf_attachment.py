#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传PDF附件到已有的Zotero文献条目
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

def find_existing_item():
    """查找已有的文献条目"""
    
    url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{LIBRARY_ID}/items"
    headers = {
        "Zotero-API-Version": "3",
        "Authorization": f"Bearer {API_KEY}"
    }
    params = {
        "q": "人工智能赋能初中英语项目式学习策略探究",
        "limit": 10
    }
    
    try:
        print("正在查找已有文献条目...")
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            items = response.json()
            
            for item in items:
                data = item.get('data', {})
                title = data.get('title', '')
                item_type = data.get('itemType', '')
                
                if "人工智能赋能初中英语项目式学习策略探究" in title and item_type == 'journalArticle':
                    print(f"✓ 找到文献条目: {title}")
                    print(f"   Key: {data.get('key')}")
                    print(f"   Version: {data.get('version')}")
                    return data.get('key'), data.get('version')
            
            print("✗ 未找到匹配的文献条目")
            return None, None
        else:
            print(f"✗ 查询失败: {response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"✗ 查询出错: {str(e)}")
        return None, None

def upload_pdf_attachment(item_key):
    """上传PDF附件到指定条目"""
    
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
        
        print(f"PDF文件大小: {len(pdf_content)} 字节")
        
        # 创建附件条目数据
        attachment_data = {
            "itemType": "attachment",
            "title": os.path.basename(PDF_PATH),
            "linkMode": "imported_file",
            "contentType": "application/pdf",
            "filename": os.path.basename(PDF_PATH),
            "parentItem": item_key,
            "tags": [
                {"tag": "项目式学习"},
                {"tag": "人工智能"},
                {"tag": "初中英语"}
            ]
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
        print(f"✓ 附件元数据创建成功，Key: {attachment_key}")
        
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
            print(f"✓ PDF文件上传成功！")
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
        "q": "人工智能赋能初中英语项目式学习策略探究",
        "limit": 5
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            items = response.json()
            print(f"✓ 找到 {len(items)} 个相关项目:")
            
            for item in items:
                data = item.get('data', {})
                title = data.get('title', '')
                item_type = data.get('itemType', '')
                
                if item_type == 'attachment' and title.endswith('.pdf'):
                    print(f"📄 PDF附件: {title}")
                    print(f"   父项目: {data.get('parentItem')}")
                    return True
                elif "人工智能赋能初中英语项目式学习策略探究" in title:
                    print(f"📚 文献条目: {title}")
                    
                    # 查找附件
                    attachments_url = f"https://api.zotero.org/{LIBRARY_TYPE}s/{LIBRARY_ID}/items/{item['key']}/children"
                    attachments_response = requests.get(attachments_url, headers=headers)
                    if attachments_response.status_code == 200:
                        attachments = attachments_response.json()
                        for attachment in attachments:
                            att_data = attachment.get('data', {})
                            if att_data.get('itemType') == 'attachment':
                                print(f"   附件: {att_data.get('title')}")
        else:
            print(f"✗ 验证失败: {response.status_code}")
            
    except Exception as e:
        print(f"✗ 验证出错: {str(e)}")
    
    return False

def main():
    """主函数"""
    print("=== Zotero PDF附件上传工具 ===\n")
    
    # 查找已有文献条目
    item_key, item_version = find_existing_item()
    
    if item_key:
        # 上传PDF附件
        if upload_pdf_attachment(item_key):
            print("\n✓ PDF附件上传成功！")
            # 验证结果
            if verify_upload():
                print("\n🎉 完整导入成功！文献条目和PDF附件都已在云端")
                print("您可以在Zotero中同步查看该文献及其PDF附件")
            else:
                print("\n⚠️ 附件上传可能有问题，请手动检查")
        else:
            print("\n✗ PDF附件上传失败")
    else:
        print("\n✗ 未找到文献条目，无法上传附件")

if __name__ == "__main__":
    main()