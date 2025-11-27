#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为Zotero文献添加笔记
"""

from pyzotero import zotero
from datetime import datetime

def add_note_to_item(item_key, note_content):
    """为文献添加笔记"""
    zot = zotero.Zotero(
        "18982351",
        "user",
        "CIApUKos6l9E0GOaCBrILRrt"
    )
    
    # 创建笔记条目
    note_template = zot.item_template('note')
    note_template['note'] = note_content
    note_template['parentItem'] = item_key
    
    try:
        resp = zot.create_items([note_template])
        if resp.get('successful'):
            note_key = resp['successful'][0]['key']
            print(f"✓ 笔记创建成功，Key: {note_key}")
            return note_key
        else:
            print(f"✗ 笔记创建失败: {resp}")
            return None
    except Exception as e:
        print(f"创建笔记出错: {e}")
        return None

def create_note_content():
    """创建笔记内容"""
    note_content = f"""
# 基于教学评一体化的小学英语阅读教学中AI技术的运用

## 文献信息
- **标题**: 基于教学评一体化的小学英语阅读教学中AI技术的运用
- **作者**: 吴雪云
- **创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 研究要点

### 核心概念
- **教学评一体化**: 将教学、学习、评价三个环节有机结合
- **AI技术在英语阅读教学中的应用**: 智能化辅助教学工具的使用

### 主要观点
1. AI技术可以实现个性化阅读推荐
2. 智能评估系统能够实时反馈学习效果
3. 数据驱动的教学决策支持

### 实践应用
- 智能阅读平台的使用
- 语音识别技术在口语练习中的应用
- 学习分析系统的构建

### 研究意义
- 提高小学英语阅读教学效率
- 促进学生个性化学习发展
- 推动教育信息化进程

## 思考与启发
- 如何平衡技术工具与传统教学方法
- AI技术在教育中的伦理考量
- 教师专业能力的新要求

## 相关研究
- 人工智能支持下的小学数学"教学评"一体化课堂实践
- AI技术在小学英语课堂教学中的应用
- 生成式人工智能在学科教学中的应用研究
"""
    
    return note_content

if __name__ == "__main__":
    # 目标文献的附件key
    attachment_key = "V2G5HDET"
    
    # 获取父文献key（附件的父文献才是真正的文献条目）
    zot = zotero.Zotero("18982351", "user", "CIApUKos6l9E0GOaCBrILRrt")
    attachment = zot.item(attachment_key)
    parent_key = attachment.get('data', {}).get('parentItem')
    
    if parent_key:
        print(f"父文献Key: {parent_key}")
        
        # 创建笔记内容
        note_content = create_note_content()
        
        # 添加笔记
        add_note_to_item(parent_key, note_content)
    else:
        print("无法获取父文献Key")