#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zotero CLI配置脚本
设置API密钥和库ID
"""

import os
import json
from pathlib import Path

# 配置信息
ZOTERO_CONFIG = {
    "api_key": "CIApUKos6l9E0GOaCBrILRrt",
    "library_id": "18982351",
    "library_type": "user",
    "local_storage": str(Path.home() / ".zotero")
}

def create_config_directory():
    """创建配置目录"""
    config_dir = Path(ZOTERO_CONFIG["local_storage"])
    config_dir.mkdir(exist_ok=True)
    return config_dir

def save_credentials():
    """保存API凭据"""
    config_dir = create_config_directory()
    creds_file = config_dir / "creds.txt"
    
    # 保存凭据文件
    with open(creds_file, 'w', encoding='utf-8') as f:
        f.write(f"api_key={ZOTERO_CONFIG['api_key']}\n")
        f.write(f"library_id={ZOTERO_CONFIG['library_id']}\n")
        f.write(f"library_type={ZOTERO_CONFIG['library_type']}\n")
    
    # 设置文件权限（仅用户可读写）
    os.chmod(creds_file, 0o600)
    print(f"✓ 凭据已保存到: {creds_file}")
    
def save_config():
    """保存配置文件"""
    config_dir = create_config_directory()
    config_file = config_dir / "config.json"
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(ZOTERO_CONFIG, f, indent=2, ensure_ascii=False)
    
    print(f"✓ 配置已保存到: {config_file}")

def setup_environment():
    """设置环境变量"""
    os.environ['ZOTERO_API_KEY'] = ZOTERO_CONFIG['api_key']
    os.environ['ZOTERO_LIBRARY_ID'] = ZOTERO_CONFIG['library_id']
    os.environ['ZOTERO_LIBRARY_TYPE'] = ZOTERO_CONFIG['library_type']
    print("✓ 环境变量已设置")

if __name__ == "__main__":
    print("=== Zotero CLI配置工具 ===")
    print(f"API密钥: {ZOTERO_CONFIG['api_key'][:10]}...")
    print(f"库ID: {ZOTERO_CONFIG['library_id']}")
    print(f"库类型: {ZOTERO_CONFIG['library_type']}")
    print()
    
    save_credentials()
    save_config()
    setup_environment()
    
    print("\n配置完成！现在可以使用zotero-cli了。")