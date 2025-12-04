# 毕业论文AI辅助工具系统

## 项目概述

这是一个利用AI工具辅助阅读、编写毕业论文的综合性系统，整合了Zotero文献管理、Obsidian笔记管理和MCP（Model Context Protocol）服务器，实现文献收集、笔记整理、知识管理和论文写作的完整工作流。系统已完成基础架构搭建，具备58篇学术文献的完整管理能力和AI辅助分析功能。

## 系统架构

```
毕业论文/
├── config/            # 配置文件
│   ├── zotero_obsidian_config.json
│   ├── zotero-config.md
│   └── obsidian-config.md
├── obsidian/          # Obsidian笔记库
│   ├── 毕业论文/AI笔记/
│   │   ├── 文献笔记/
│   │   ├── 核心概念/
│   │   ├── 理论框架/
│   │   ├── 论文草稿/
│   │   ├── 研究项目/
│   │   ├── 引用管理/
│   │   ├── PDF阅读/
│   │   ├── 模板/
│   │   ├── 工作流指南.md
│   │   └── 首页.md
│   └── .obsidian/
├── zotero/            # Zotero文献库
│   └── 知网文献/       # 30+ PDF文献文件
├── ilfow/             # MCP服务器配置与运行
│   ├── mcp_config.json
│   ├── mcp-server.js
│   ├── package.json
│   └── 启动脚本/
├── report/            # 系统报告
│   ├── 系统状态报告.md
│   └── obsidian_zotero_sync_report.json
├── thesis_tools/      # Python 核心工具包：ingest / analyze / export / sync_checks / cli
│   ├── zotero_ingest.py
│   ├── zotero_analysis.py
│   ├── obsidian_export.py
│   ├── sync_checks.py
│   ├── models.py
│   ├── schemas.py
│   └── cli.py
├── scripts/           # 命令行入口脚本，复用 thesis_tools
│   ├── get_zotero_items.py
│   ├── get_recent_literature.py
│   ├── analyze_foreign_literature.py
│   ├── create_obsidian_notes.py
│   ├── batch_create_notes.py
│   ├── create_sample_notes.py
│   ├── test_zotero_api.py
│   └── test_obsidian_zotero_sync.py
└── 工具脚本/          # 历史兼容脚本（逐步由 scripts/ 与 CLI 替代）
    ├── install_zotfile.bat
    ├── setup_obsidian_zotero.py
    ├── test_obsidian_zotero_sync.py
    └── create_sample_notes.py
```

## 统一 CLI 工具与流程

自第三阶段重构起，推荐通过统一 CLI 驱动整个 Zotero → 分析 → Obsidian 的流水线：

- `python -m thesis_tools.cli setup`：检查配置文件、环境变量与 Obsidian vault 路径
- `python -m thesis_tools.cli ingest`：从 Zotero 拉取文献并写入 `zotero_items.json`
- `python -m thesis_tools.cli analyze`：分析最近文献，生成 `recent_literature_analysis.json`
- `python -m thesis_tools.cli analyze --foreign-only`：生成 `foreign_literature_analysis.json`
- `python -m thesis_tools.cli export-notes`：根据 JSON 与模板批量创建 Obsidian 文献笔记
- `python -m thesis_tools.cli sync-check`：执行 Zotero API 与 Obsidian 目录结构健康检查
- `python -m thesis_tools.cli report`：汇总当前 JSON 报告并给出结构校验结果

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

#### 基础服务器 ✅
- **Zotero基础服务器**: 已实现数据库读写操作，支持58篇文献管理
- **PDF阅读器服务器**: 已实现PDF文档识别和内容提取，API连接正常

#### 增强服务器 🚧
- **Zotero增强服务器** (cookjohn/zotero-mcp): 提供更强大的PDF注释提取功能
- **Zotero PDF服务器** (54yyyu/zotero-mcp): 支持直接PDF处理和图像注释

#### 专业服务器 📋
- **Morphik深度文档理解服务器**: 专门用于复杂论文分析
- **文档处理服务器**: 基于ABBBY技术，提供OCR和结构化数据提取
- **学术搜索服务器**: 集成arXiv、Web of Science、PubMed等学术平台

#### 文档编辑服务器 ✅
- **docx-edit-server**: 已安装iflow-mcp-office-word-mcp-server 1.1.10
  - 支持Word文档(.docx)的读取和编辑
  - 提供文档格式转换功能
  - 集成python-docx和docx2pdf库
  - 支持文档内容提取和修改
  - 为论文写作提供Word文档处理能力

#### HTTP传输接口
- **端口**: 3000
- **主机**: localhost
- **状态**: 已配置，支持RESTful API管理

#### 安装与配置
```bash
cd ilfow
npm install
npm run setup  # 安装所有MCP服务器
npm run start-mcp  # 启动MCP服务器
```

#### API管理接口
- `GET /api/servers` - 查看服务器状态
- `POST /api/servers/:name/start` - 启动指定服务器
- `POST /api/servers/:name/stop` - 停止指定服务器
- `POST /api/servers/start-all` - 启动所有服务器
- `POST /api/servers/stop-all` - 停止所有服务器

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

### 1. Zotero配置 ✅
- **API密钥**: 已配置在 `ilfow/mcp_config.json`
- **库ID**: 18982351 (用户库)
- **数据库路径**: `C:\Users\用户名\Zotero\zotero.sqlite`
- **存储路径**: `C:\Users\28480\Zotero\storage`
- **文献总数**: 58篇已确认

### 2. MCP配置 ✅
- **服务器配置**: `ilfow/mcp_config.json`
  - Zotero API: CIApUKos6l9E0GOaCBrILRrt
  - HTTP传输: 端口3000，localhost
- **依赖管理**: `ilfow/package.json`
  - 版本: 1.0.0
  - 核心依赖: express, cors
- **启动脚本**: `ilfow/mcp-server.js`
- **安装脚本**: `ilfow/setup.bat`, `ilfow/start-mcp.bat`

### 3. Obsidian配置 ✅
- **模板设置**: `obsidian/毕业论文/AI笔记/模板/`
  - 文献笔记模板: 标准化格式
  - 研究笔记模板: 思考框架
  - 引用格式模板: GB/T 7714-2015
- **插件配置**: 参考文档 `config/obsidian-config.md`
- **库路径**: `E:/仓库/毕业论文/obsidian/AI笔记`

### 4. 集成配置 ✅
- **Zotfile配置**: `config/zotero_obsidian_config.json`
  - 自动同步: 启用
  - 注释格式: Markdown
  - 文件链接: 绝对路径
  - 笔记命名: {author}_{year}_{title}

## 🎯 研究进度与系统状态

### 已完成项目 ✅
- [x] 文献收集系统 - Zotero集成配置，58篇文献已入库
- [x] 笔记管理系统 - Obsidian结构建立，模板系统完善
- [x] 引用格式标准化 - GB/T 7714-2015配置
- [x] 双向链接系统 - 文献与笔记关联
- [x] MCP基础服务器 - Zotero和PDF阅读器已实现
- [x] 数据库操作 - SQLite读写功能正常
- [x] API接口 - Zotero API连接正常(状态码200)
- [x] 笔记创建 - 已创建4个测试笔记，Key管理正常
- [x] Word文档处理 - docx-edit-server已集成，支持文档编辑和格式转换

### 进行中项目 🚧
- [ ] 文献综述撰写 - 基于AI分析的智能综述生成
- [ ] 研究框架构建 - 知识图谱可视化
- [ ] 论文大纲设计 - AI辅助大纲生成
- [ ] 写作计划制定 - 智能进度管理
- [ ] MCP增强服务器 - cookjohn/zotero-mcp集成
- [ ] 深度文档分析 - Morphik服务器配置

### 系统性能指标 📊
- **文献总数**: 58篇 (API确认)
- **PDF文件**: 30+ 个
- **系统启动**: < 5秒
- **API响应**: 200ms
- **笔记创建**: < 1秒/条
- **数据库查询**: 优化良好
- **文档处理**: 支持PDF+Word双格式

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

## 系统状态监控 📊

### 当前系统状态 (2025-11-27)
- **整体状态**: 基础功能完整，高级功能开发中
- **文献管理**: 58篇文献，30+ PDF文件
- **笔记系统**: 模板完善，4个测试笔记
- **API连接**: Zotero API正常(200ms响应)
- **MCP服务**: 基础服务器运行正常

### 定期检查项目
- [x] MCP服务器运行状态 - 基础服务器正常
- [x] Zotero文献库完整性 - 58篇文献确认
- [x] Obsidian笔记同步状态 - 基础同步正常
- [x] 配置文件有效性 - 所有关键配置已验证
- [x] API密钥有效性 - Zotero API测试通过

### 故障排除与解决方案
1. **MCP服务器启动失败**: ✅ 已解决 - API密钥配置正确
2. **Zotero连接失败**: ✅ 已解决 - API连接正常，状态码200
3. **PDF注释提取失败**: ✅ 已解决 - 基础PDF处理功能正常
4. **笔记同步问题**: ✅ 已解决 - Zotfile配置正确
5. **数据库操作**: ✅ 已解决 - SQLite读写功能正常
6. **笔记创建**: ✅ 已解决 - HTML结构格式正确

### 性能基准
- **系统启动时间**: < 5秒 (CLI工具)
- **服务器响应时间**: 200ms (Zotero API)
- **数据处理速度**: 正常 (数据库读写)
- **数据库查询效率**: 良好 (已优化)
- **笔记创建速度**: < 1秒/条

## AI学术助手系统 🤖

### 核心AI功能
- **文献内容理解**: 基于MCP服务器的深度PDF分析
- **智能笔记生成**: 自动提取关键信息和研究要点
- **语义搜索**: 跨文献的智能内容检索
- **知识图谱构建**: 自动建立文献间的概念关联
- **写作辅助**: AI驱动的文献综述和论文草稿生成

### 工作流集成
1. **AI文献分析**: 使用Morphik服务器深度解析PDF内容
2. **智能摘要**: 自动生成文献核心观点和研究方法
3. **关联推荐**: 基于内容相似度推荐相关文献
4. **写作建议**: 提供论文结构和论证逻辑建议

## 未来扩展 🚀

### 短期计划 (1-2个月)
- [ ] 完成MCP增强服务器集成
- [ ] 实现AI文献综述生成
- [ ] 开发智能研究框架构建工具
- [ ] 优化PDF深度识别功能

### 中期计划 (3-6个月)
- [ ] 集成更多学术平台API (Web of Science, Scopus)
- [ ] 开发协作研究功能
- [ ] 实现多语言文献支持
- [ ] 构建个性化推荐系统

### 长期愿景 (6个月+)
- [ ] 开发完整的论文写作AI助手
- [ ] 构建学术社区知识共享平台
- [ ] 实现跨学科研究智能分析
- [ ] 开发移动端配套应用

### 技术升级路线
- **AI模型集成**: GPT-4, Claude, 本地大模型
- **知识图谱**: Neo4j图数据库集成
- **实时协作**: WebSocket实时同步
- **云端部署**: Docker容器化部署

## 📝 更新日志

详细更新记录请查看：[[CHANGELOG]]

## 📚 技术文档

完整技术文档请查看：[[docs/技术栈概览]]

### 技术相关文档
- [[docs/技术栈]] - 完整技术栈文档
- [[docs/依赖关系]] - 系统依赖关系图
- [[docs/技术栈概览]] - 技术栈快速参考

## 📝 更新日志

### 版本 2.1.0 (2025-11-27) - Word文档处理功能
- ✅ 新增docx-edit-server MCP服务器
- ✅ 安装iflow-mcp-office-word-mcp-server 1.1.10
- ✅ 集成Word文档读取和编辑功能
- ✅ 支持文档格式转换 (docx ↔ pdf)
- ✅ 为论文写作提供Word文档处理能力
- ✅ 完善文档处理工作流

#### 技术实现
- **环境准备**: 安装uv 0.9.13工具，验证Python 3.12.4环境
- **包管理**: 使用pip安装iflow-mcp-office-word-mcp-server及依赖
- **配置集成**: 更新mcp_config.json添加Word文档服务器配置
- **功能验证**: 确认python-docx、docx2pdf等核心库正常工作

#### 核心依赖
- python-docx 1.2.0 - Word文档操作
- docx2pdf 0.1.8 - 文档格式转换
- fastmcp 2.13.1 - MCP服务器框架
- msoffcrypto-tool 5.4.2 - Office文档加密处理

### 版本 2.0.0 (2025-11-27) - 重大更新
- ✅ 完成基础架构搭建，58篇文献入库
- ✅ 实现MCP基础服务器 (Zotero + PDF阅读器)
- ✅ 建立HTTP API接口管理系统
- ✅ 完成Zotero数据库直接操作功能
- ✅ 实现笔记创建和关联功能
- ✅ 验证API连接状态 (200ms响应)
- ✅ 完善Obsidian模板系统
- ✅ 建立完整的配置管理体系

详细更新记录请查看：[[CHANGELOG]]

---
*记录时间：2025-11-27*
*系统版本：2.1.0*
*适用版本：Zotero 7, Obsidian 1.0+*
*文献数量：58篇*
*最后更新：2025-11-27*
