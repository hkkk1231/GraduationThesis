#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通过Zotero的JavaScript API添加笔记
"""

import requests
import time
from datetime import datetime

def add_note_via_javascript():
    """通过JavaScript API添加笔记"""
    
    # 创建JavaScript脚本
    script = f"""
    // 获取目标文献条目
    var items = Zotero.Items.get('LA2VSHG9');
    if (!items || items.length === 0) {{
        throw new Error('未找到目标文献条目');
    }}
    
    var item = items[0];
    
    // 创建笔记内容
    var noteContent = `<h1>基于教学评一体化的小学英语阅读教学中AI技术的运用</h1>
<h2>文献信息</h2>
<ul>
<li><strong>标题</strong>: 基于教学评一体化的小学英语阅读教学中AI技术的运用</li>
<li><strong>作者</strong>: 吴雪云</li>
<li><strong>创建时间</strong>: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
</ul>
<h2>研究要点</h2>
<h3>核心概念</h3>
<ul>
<li><strong>教学评一体化</strong>: 将教学、学习、评价三个环节有机结合</li>
<li><strong>AI技术在英语阅读教学中的应用</strong>: 智能化辅助教学工具的使用</li>
</ul>
<h3>主要观点</h3>
<ol>
<li>AI技术可以实现个性化阅读推荐</li>
<li>智能评估系统能够实时反馈学习效果</li>
<li>数据驱动的教学决策支持</li>
</ol>
<h3>实践应用</h3>
<ul>
<li>智能阅读平台的使用</li>
<li>语音识别技术在口语练习中的应用</li>
<li>学习分析系统的构建</li>
</ul>
<h3>研究意义</h3>
<ul>
<li>提高小学英语阅读教学效率</li>
<li>促进学生个性化学习发展</li>
<li>推动教育信息化进程</li>
</ul>
<h2>思考与启发</h2>
<ul>
<li>如何平衡技术工具与传统教学方法</li>
<li>AI技术在教育中的伦理考量</li>
<li>教师专业能力的新要求</li>
</ul>
<h2>相关研究</h2>
<ul>
<li>人工智能支持下的小学数学"教学评"一体化课堂实践</li>
<li>AI技术在小学英语课堂教学中的应用</li>
<li>生成式人工智能在学科教学中的应用研究</li>
</ul>`;
    
    // 创建笔记条目
    var note = new Zotero.Item('note');
    note.parentKey = item.key;
    note.setNote(noteContent);
    
    // 保存笔记
    await note.saveTx();
    
    // 返回结果
    return {{
        success: true,
        noteKey: note.key,
        parentKey: item.key,
        message: '笔记创建成功'
    }};
    """
    
    try:
        # 等待Zotero启动
        time.sleep(2)
        
        # 发送脚本到debug-bridge
        url = "http://127.0.0.1:23119/debug-bridge/execute"
        headers = {"Content-Type": "application/javascript"}
        
        print("正在通过JavaScript API添加笔记...")
        response = requests.post(url, data=script.encode('utf-8'), headers=headers, timeout=30)
        
        if response.status_code == 201:
            result = response.json()
            print("✓ JavaScript执行成功")
            print(f"结果: {result}")
            return True
        else:
            print(f"✗ JavaScript执行失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"执行JavaScript时出错: {e}")
        print("请确保Zotero正在运行并且debug-bridge已启用")
        return False

def check_zotero_connection():
    """检查Zotero连接"""
    try:
        url = "http://127.0.0.1:23119/debug-bridge/ping"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            print("✓ Zotero debug-bridge连接正常")
            return True
        else:
            print("✗ Zotero debug-bridge连接失败")
            return False
    except Exception as e:
        print(f"无法连接到Zotero debug-bridge: {e}")
        print("请确保Zotero正在运行并且已启用debug-bridge")
        return False

if __name__ == "__main__":
    print("=== 通过JavaScript API添加笔记到Zotero ===")
    
    # 检查连接
    if check_zotero_connection():
        # 添加笔记
        success = add_note_via_javascript()
        
        if success:
            print("\n✓ 笔记已成功添加到Zotero数据库！")
            print("请在Zotero中查看'基于教学评一体化的小学英语阅读教学中AI技术的运用'条目下的笔记")
        else:
            print("\n✗ 笔记添加失败")
    else:
        print("\n请先启动Zotero并启用debug-bridge功能")
        print("启用方法: 编辑 → 首选项 → 高级 → 配置编辑器")
        print("设置: extensions.zotero.debugBridge.enabled = true")
