#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zotero PDF自动导入和分类脚本
使用Zotero 7原生命令行功能导入PDF并自动分类
"""

import os
import subprocess
import time
import sys
from pathlib import Path

# 配置
ZOTERO_PATH = r"D:\工具\zotero\zotero.exe"
PDF_DIR = r"E:\仓库\毕业论文\zotero\知网文献"
COLLECTION_NAME = "教育学"
SUBCOLLECTION_NAME = "英语教学"

def import_pdf_to_zotero(pdf_path):
    """使用Zotero 7原生功能导入PDF"""
    try:
        # 启动Zotero并导入PDF
        cmd = [ZOTERO_PATH, pdf_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ 成功导入: {os.path.basename(pdf_path)}")
            return True
        else:
            print(f"✗ 导入失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ 导入出错: {str(e)}")
        return False

def create_collection_script():
    """创建分类脚本（Zotero JavaScript）"""
    script = f"""
    // 创建分类结构
    var libraryID = Zotero.Libraries.userLibraryID;
    
    // 创建主分类
    var parentCollection = Zotero.Collections.getByLibrary(libraryID).find(
        c => c.name === "{COLLECTION_NAME}"
    );
    
    if (!parentCollection) {{
        parentCollection = new Zotero.Collection();
        parentCollection.name = "{COLLECTION_NAME}";
        parentCollection.libraryID = libraryID;
        await parentCollection.saveTx();
        Zotero.debug("创建主分类: {COLLECTION_NAME}");
    }}
    
    // 创建子分类
    var childCollection = Zotero.Collections.getByLibrary(libraryID).find(
        c => c.name === "{SUBCOLLECTION_NAME}" && c.parentID === parentCollection.id
    );
    
    if (!childCollection) {{
        childCollection = new Zotero.Collection();
        childCollection.name = "{SUBCOLLECTION_NAME}";
        childCollection.parentID = parentCollection.id;
        childCollection.libraryID = libraryID;
        await childCollection.saveTx();
        Zotero.debug("创建子分类: {SUBCOLLECTION_NAME}");
    }}
    
    // 获取最新导入的项目
    var items = Zotero.Items.getAll(libraryID).slice(-5);
    
    // 为项目添加标签和分类
    for (let item of items) {{
        if (item.isAttachment() && item.attachmentFilename.endsWith('.pdf')) {{
            var parentItem = await item.getParentItem();
            if (parentItem) {{
                // 添加到分类
                parentItem.addToCollection(childCollection.id);
                
                // 添加标签
                parentItem.addTag('项目式学习');
                parentItem.addTag('人工智能');
                parentItem.addTag('初中英语');
                
                await parentItem.saveTx();
                Zotero.debug("已分类项目: " + parentItem.getDisplayTitle());
            }}
        }}
    }}
    
    "分类完成";
    """
    
    return script

def run_zotero_script(script):
    """通过Zotero debug-bridge运行JavaScript脚本"""
    try:
        import requests
        
        # 等待Zotero启动
        time.sleep(3)
        
        # 发送脚本到debug-bridge
        url = "http://127.0.0.1:23119/debug-bridge/execute"
        headers = {"Content-Type": "application/javascript"}
        
        response = requests.post(url, data=script.encode('utf-8'), headers=headers, timeout=30)
        
        if response.status_code == 201:
            print("✓ 分类脚本执行成功")
            return True
        else:
            print(f"✗ 分类脚本执行失败: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 无法执行分类脚本: {str(e)}")
        print("提示: 请确保已安装Better BibTeX插件")
        return False

def main():
    """主函数"""
    print("=== Zotero PDF自动导入工具 ===")
    print(f"PDF目录: {PDF_DIR}")
    print(f"目标分类: {COLLECTION_NAME} > {SUBCOLLECTION_NAME}")
    print()
    
    # 查找PDF文件
    pdf_files = list(Path(PDF_DIR).glob("*.pdf"))
    
    if not pdf_files:
        print("✗ 未找到PDF文件")
        return
    
    print(f"找到 {len(pdf_files)} 个PDF文件:")
    for pdf in pdf_files:
        print(f"  - {pdf.name}")
    print()
    
    # 导入PDF文件
    success_count = 0
    for pdf_file in pdf_files:
        if import_pdf_to_zotero(str(pdf_file)):
            success_count += 1
        time.sleep(1)  # 避免导入过快
    
    print(f"\n导入完成: {success_count}/{len(pdf_files)} 个文件成功")
    
    # 创建并执行分类脚本
    if success_count > 0:
        print("\n正在执行自动分类...")
        script = create_collection_script()
        run_zotero_script(script)
    
    print("\n操作完成！请检查Zotero中的文献库。")

if __name__ == "__main__":
    main()