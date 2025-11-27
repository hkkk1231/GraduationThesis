#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Zotero MCP工具将PDF导入到云端
"""

import subprocess
import json
import sys
import os
from pathlib import Path

# 配置
PDF_PATH = r"E:\仓库\毕业论文\zotero\知网文献\人工智能赋能初中英语项目式学习策略探究_周颖.pdf"
MCP_CONFIG = r"E:\仓库\毕业论文\ifow\mcp_config.json"

def run_mcp_command(command):
    """运行MCP命令"""
    try:
        # 切换到MCP配置目录
        mcp_dir = os.path.dirname(MCP_CONFIG)
        
        # 构建MCP命令
        cmd = ["npx", "-y", "@modelcontextprotocol/server-zotero"]
        
        # 设置环境变量
        env = os.environ.copy()
        with open(MCP_CONFIG, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        zotero_config = config.get('mcpServers', {}).get('zotero', {})
        env.update(zotero_config.get('env', {}))
        
        print(f"执行MCP命令: {' '.join(command)}")
        print(f"工作目录: {mcp_dir}")
        
        # 运行命令
        result = subprocess.run(
            cmd + command,
            cwd=mcp_dir,
            env=env,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return result.returncode == 0, result.stdout, result.stderr
        
    except Exception as e:
        return False, "", str(e)

def import_pdf_to_zotero_cloud():
    """使用MCP工具导入PDF到云端"""
    print("=== 使用MCP工具导入PDF到Zotero云端 ===\n")
    
    # 检查PDF文件是否存在
    if not os.path.exists(PDF_PATH):
        print(f"✗ PDF文件不存在: {PDF_PATH}")
        return False
    
    print(f"✓ PDF文件存在: {os.path.basename(PDF_PATH)}")
    
    # MCP导入命令
    # 注意：具体的MCP命令格式需要根据实际的MCP服务器API来确定
    import_commands = [
        ["import", PDF_PATH],
        ["add-item", "--file", PDF_PATH],
        ["upload", PDF_PATH]
    ]
    
    for cmd in import_commands:
        print(f"\n尝试命令: {' '.join(cmd)}")
        success, stdout, stderr = run_mcp_command(cmd)
        
        if success:
            print(f"✓ 命令执行成功")
            if stdout:
                print(f"输出: {stdout}")
            return True
        else:
            print(f"✗ 命令执行失败")
            if stderr:
                print(f"错误: {stderr}")
    
    return False

def check_mcp_status():
    """检查MCP服务器状态"""
    print("检查MCP服务器状态...")
    
    # 尝试获取MCP服务器信息
    status_commands = [
        ["status"],
        ["info"],
        ["--help"]
    ]
    
    for cmd in status_commands:
        success, stdout, stderr = run_mcp_command(cmd)
        if success and stdout:
            print(f"✓ MCP服务器响应正常")
            print(f"信息: {stdout[:200]}...")  # 只显示前200个字符
            return True
    
    print("✗ 无法连接到MCP服务器")
    return False

def main():
    """主函数"""
    print("Zotero MCP云端导入工具\n")
    
    # 检查MCP状态
    if not check_mcp_status():
        print("\n请检查MCP服务器配置和连接")
        return
    
    # 导入PDF
    if import_pdf_to_zotero_cloud():
        print("\n✓ PDF导入成功！")
        print("请检查Zotero云端库和本地同步状态")
    else:
        print("\n✗ PDF导入失败")
        print("可能需要手动检查MCP工具的API文档")

if __name__ == "__main__":
    main()