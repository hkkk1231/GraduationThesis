# 毕业论文AI辅助工具系统

## 项目概述

这是一个利用AI工具辅助阅读、编写毕业论文的综合性系统，整合了Zotero文献管理、Obsidian笔记管理和MCP（Model Context Protocol）服务器，实现文献收集、笔记整理、知识管理和论文写作的完整工作流。

## 系统架构

```
毕业论文/
├── config/            # 配置文件
│   └── zotero_obsidian_config.json
├── obsidian/          # Obsidian笔记库
│   ├── 毕业论文/AI笔记/
│   │   ├── 文献笔记/
│   │   ├── 核心概念/
│   │   ├── 引用管理/
│   │   ├── 模板/
│   │   └── 工作流指南.md
│   └── .obsidian/
├── zotero/            # Zotero文献库
│   └── 知网文献/
├── report/            # 系统报告
│   ├── 系统状态报告.md
│   └── obsidian_zotero_sync_report.json
└── 工具脚本/
    ├── install_zotfile.bat
    ├── setup_obsidian_zotero.py
    ├── test_obsidian_zotero_sync.py
    └── create_sample_notes.py
```

## 核心组件

### 1. Zotero文献管理系统

#### 核心功能
- **文献收集**: 通过多种渠道收集学术文献
- **PDF管理**: 自动管理和组织PDF附件
- **引用生成**: 支持GB/T 7714-2015标准引用格式
- **笔记同步**: 与Obsidian双向同步

#### 引用格式配置
- **标准**: GB/T 7714-2015《信息与文献 参考文献著录规则》
- **插件**: 按需安装茉莉花插件增强中文支持
- **格式示例**: `[1] 李荣琼. 基于人工智能技术的语文课堂教学设计与分析[J]. 未明确期刊, 2025(10): 146-147.`

#### 使用方法
1. **收集文献**: 从数据库、网页直接导入到Zotero
2. **管理PDF**: 自动下载和整理PDF附件
3. **生成引用**: 使用快捷键直接生成标准格式引用
4. **同步笔记**: 通过Zotfile自动提取注释到Obsidian

### 2. MCP服务器架构

#### 基础服务器
- **Zotero基础服务器**: 实现数据库读写操作
- **PDF阅读器服务器**: 提供PDF文档识别和内容提取

#### 增强服务器
- **Zotero增强服务器** (cookjohn/zotero-mcp): 提供更强大的PDF注释提取功能
- **Zotero PDF服务器** (54yyyu/zotero-mcp): 支持直接PDF处理和图像注释

#### 专业服务器
- **Morphik深度文档理解服务器**: 专门用于复杂论文分析
- **文档处理服务器**: 基于ABBBY技术，提供OCR和结构化数据提取
- **学术搜索服务器**: 集成arXiv、Web of Science、PubMed等学术平台

#### 安装与配置
```bash
cd ifow
npm install
npm run setup  # 安装所有MCP服务器
npm run start-mcp  # 启动MCP服务器
```

### 3. Obsidian笔记管理

#### 功能特点
- 与Zotero双向链接的知识图谱
- 自动提取PDF注释并转换为笔记
- 支持模板化笔记结构
- 建立文献间的关联网络

#### 笔记模板
- **文献笔记模板**: 标准化的文献阅读笔记格式
- **研究笔记模板**: 研究思路和理论框架记录

## Zotero CLI操作经验

### 问题背景
尝试通过CLI向Zotero数据库添加笔记，但创建的笔记无法在GUI界面中显示，而手动创建的笔记可以正常显示。

### 关键发现

#### 1. HTML结构要求
**正确的笔记HTML结构**：
```html
<div class="zotero-note znv1"><div data-schema-version="9">笔记内容</div></div>
```

**错误的结构**（缺少schema属性）：
```html
<div class="zotero-note znv1">笔记内容</div>
```

#### 2. 数据库操作前提
- **必须完全关闭Zotero**才能操作SQLite数据库
- ItemTypeID 28 对应笔记类型
- 数据库路径：`C:\Users\用户名\Zotero\zotero.sqlite`

#### 3. 父文献Key的重要性
- 不同的文献条目有不同的Key
- 确保为正确的父文献创建笔记，否则会添加到错误的文献下
- 需要通过数据库查询确认正确的父文献Key

### 调试流程

#### 系统化排查步骤
1. **确认父文献Key**: 查询数据库确保操作的是正确的文献条目
2. **对比数据结构**: 分析手动创建和代码创建的笔记差异
3. **检查HTML格式**: 验证必需的属性和结构
4. **验证数据库存储**: 确认数据正确写入数据库
5. **重启验证**: 重启Zotero检查显示效果

#### 常用查询语句
```sql
-- 查找父文献下的所有笔记
SELECT i.key, i.dateAdded, n.note
FROM items i
LEFT JOIN itemNotes n ON i.itemID = n.itemID
WHERE i.itemID IN (
    SELECT itemID FROM itemNotes WHERE parentItemID = ?
)
ORDER BY i.dateAdded DESC

-- 检查笔记HTML结构
SELECT note FROM itemNotes WHERE itemID = ?
```

### 解决方案

#### 创建笔记的正确代码结构
```python
# 生成正确的HTML结构
formatted_note = f"""<div class="zotero-note znv1"><div data-schema-version="9">{note_content}</div></div>"""

# 插入笔记条目
cursor.execute("""
    INSERT INTO items (libraryID, key, itemTypeID, dateAdded, dateModified, clientDateModified)
    VALUES (1, ?, 28, datetime('now'), datetime('now'), datetime('now'))
""", (note_key,))

# 设置父子关系和内容
cursor.execute("""
    INSERT INTO itemNotes (itemID, parentItemID, note)
    VALUES (?, ?, ?)
""", (note_id, parent_id, formatted_note))
```

## 工作流程

### 1. 文献收集与管理
1. 使用Zotero收集和管理文献
2. 配置GB/T 7714-2015引用格式
3. 自动分类和标签管理

### 2. 文献阅读与注释
1. 在Zotero中阅读PDF并添加注释
2. 使用统一的高亮和注释规范
3. Zotfile自动提取注释到Obsidian

### 3. 知识整合与写作
1. 在Obsidian中建立知识图谱
2. 直接从Zotero复制标准引用格式
3. 基于整理的笔记进行论文写作

## 配置文件说明

### 1. Zotero配置
- **API密钥**: 存储在 `~/.zotero/creds.txt`
- **库配置**: 保存为 `~/.zotero/config.json`
- **分类结构**: 定义在 `collection_structure.json`
- **关键词映射**: 配置在 `keywords_mapping.json`

### 2. MCP配置
- **服务器配置**: `ifow/mcp_config.json`
- **依赖管理**: `ifow/package.json`
- **启动脚本**: `ifow/mcp-server.js`

### 3. Obsidian配置
- **模板设置**: `obsidian/AI笔记/模板/`
- **插件配置**: 参考文档 `config/obsidian-config.md`

## 🎯 研究进度

### 已完成项目
- [x] 文献收集系统 - Zotero集成配置
- [x] 笔记管理系统 - Obsidian结构建立
- [x] 引用格式标准化 - GB/T 7714-2015配置
- [x] 双向链接系统 - 文献与笔记关联

### 进行中项目
- [ ] 文献综述撰写
- [ ] 研究框架构建
- [ ] 论文大纲设计
- [ ] 写作计划制定

## 📝 项目维护原则

### 及时更新文档要求
- **代码变更**: 任何代码修改必须同步更新相关文档
- **功能调整**: 新增或删除功能需更新IFLOW.md和工作流指南
- **配置变更**: 配置文件修改需更新对应的配置文档
- **结构变更**: 目录结构调整需更新系统架构图

### 文档更新流程
1. **修改前**: 先确认需要更新的文档范围
2. **修改中**: 同步进行文档更新
3. **修改后**: 验证文档与实际功能的一致性
4. **提交前**: 确保所有相关文档都已更新

### 文档质量标准
- **准确性**: 文档内容必须与实际功能完全一致
- **完整性**: 涵盖所有重要功能和使用方法
- **时效性**: 及时反映最新的系统状态
- **易用性**: 提供清晰的使用指导和示例

### 避免的坑
- 不要假设某个Key就是正确的父文献
- 不要忽略HTML结构的细微差异
- 不要在Zotero运行时操作数据库
- 不要跳过验证步骤直接提交
- 不要忽视MCP服务器的API密钥配置
- 不要混淆不同工具的配置文件路径

## 工具脚本

### 系统集成
- `install_zotfile.bat` - Zotfile插件安装脚本
- `setup_obsidian_zotero.py` - Obsidian与Zotero集成配置
- `obsidian_plugins_guide.md` - Obsidian插件安装指南

### 测试工具
- `test_obsidian_zotero_sync.py` - 双向同步功能测试
- `create_sample_notes.py` - 示例笔记创建工具

### 配置文件
- `config/zotero_obsidian_config.json` - 集成配置
- `obsidian/AI笔记/引用管理/` - 引用规范和模板

## 应用场景

### 学术研究
- 批量导入文献时自动创建笔记
- 通过CLI管理Zotero文献库
- 自动化文献整理和分类
- 与其他工具集成时的数据同步

### 论文写作
- 文献综述的自动化生成
- 研究思路的可视化整理
- 引用管理的标准化流程
- 知识图谱的构建与维护

### 教学应用
- 课程文献的快速整理
- 学生研究项目的指导工具
- 学术写作的教学辅助
- 知识管理的最佳实践示范

## 系统状态监控

### 定期检查项目
- MCP服务器运行状态
- Zotero文献库完整性
- Obsidian笔记同步状态
- 配置文件有效性
- API密钥有效性

### 故障排除
1. **MCP服务器启动失败**: 检查API密钥配置和网络连接
2. **Zotero连接失败**: 确认Zotero正在运行且API设置正确
3. **PDF注释提取失败**: 检查PDF文件权限和格式
4. **笔记同步问题**: 验证Zotfile插件配置和目标文件夹权限

## 未来扩展

### 计划功能
- 增加更多学术平台的MCP集成
- 实现智能文献推荐系统
- 开发论文写作辅助AI
- 构建协作研究平台

### 技术升级
- 迁移到更稳定的HTTP协议MCP通信
- 集成更多AI模型和分析工具
- 优化数据库操作性能
- 增强用户界面和交互体验

## 📝 更新日志

详细更新记录请查看：[[CHANGELOG]]

### 最新更新 (2025-11-27)
- ✅ 系统架构简化，移除复杂CLI工具
- ✅ 优化引用流程，直接从Zotero获取标准格式
- ✅ 完善文档结构，增加使用指南
- ✅ 建立双向链接，增强知识管理

---
*记录时间：2025-11-27*
*系统版本：2.0.0*
*适用版本：Zotero 7, Obsidian 1.0+*
*最后更新：2025-11-27*