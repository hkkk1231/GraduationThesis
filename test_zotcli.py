#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试zotero-cli模块
"""

try:
    import zotero_cli
    print("✓ zotero-cli模块导入成功")
    print(f"模块位置: {zotero_cli.__file__}")
    
    # 尝试导入主要组件
    from pyzotero import zotero
    print("✓ Pyzotero导入成功")
    
except ImportError as e:
    print(f"✗ 导入失败: {e}")

# 检查是否有可执行的CLI入口点
import pkg_resources
try:
    entry_points = pkg_resources.get_entry_map('zotero-cli')
    if 'console_scripts' in entry_points:
        print("✓ 找到控制台脚本入口点:")
        for name, entry in entry_points['console_scripts'].items():
            print(f"  - {name}: {entry}")
    else:
        print("✗ 未找到控制台脚本入口点")
except Exception as e:
    print(f"检查入口点时出错: {e}")