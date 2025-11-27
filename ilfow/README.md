# 毕业论文AI工具配置

## 项目结构

```
毕业论文/
├── ifow/              # MCP服务器配置和脚本
├── config/            # 各种工具的配置文件
├── obsidian/          # Obsidian笔记库
├── zotero/            # Zotero文献库
└── report/            # 智能体汇报文件
```

## 快速开始

### 1. 安装依赖
```bash
cd ifow
npm install
npm run setup
```

### 2. 配置API密钥
编辑 `ifow/mcp_config.json`，填入相应的API密钥：
- ZOTERO_API_KEY: Zotero API密钥
- ZOTERO_LIBRARY_ID: Zotero图书馆ID
- MORPHIK_API_KEY: Morphik API密钥
- ABBYY_API_KEY: ABBYY API密钥
- ARXIV_API_KEY: arXiv API密钥

### 3. 启动MCP服务器
```bash
cd ifow
npm run start-mcp
```

### 4. 配置Obsidian
参考 `config/obsidian-config.md` 进行配置

### 5. 配置Zotero
参考 `config/zotero-config.md` 进行配置

## MCP服务器说明

### 基础服务器
- **zotero**: 基础Zotero集成
- **pdf-reader**: PDF阅读和注释提取

### 增强服务器
- **zotero-enhanced**: cookjohn/zotero-mcp，提供更强大的PDF注释提取
- **zotero-pdf**: 54yyyu/zotero-mcp，支持直接PDF处理和图像注释

### 专业服务器
- **morphik**: 深度文档理解，适合复杂论文分析
- **document-processor**: 基于ABBBY技术的OCR和结构化数据提取
- **academic-search**: 集成多个学术平台的搜索功能

## 工作流程

1. **文献收集**: 使用Zotero收集和管理文献
2. **PDF阅读**: 在Zotero中阅读PDF并添加注释
3. **自动提取**: Zotfile自动提取注释到Obsidian
4. **AI分析**: 使用MCP服务器进行深度分析
5. **知识整合**: 在Obsidian中建立知识图谱
6. **论文写作**: 基于整理的笔记进行论文写作

## API接口

启动后可通过以下接口管理MCP服务器：

- `GET /api/servers` - 查看服务器状态
- `POST /api/servers/:name/start` - 启动指定服务器
- `POST /api/servers/:name/stop` - 停止指定服务器
- `POST /api/servers/start-all` - 启动所有服务器
- `POST /api/servers/stop-all` - 停止所有服务器

## 故障排除

### 常见问题
1. **MCP服务器启动失败**: 检查API密钥配置
2. **Zotero连接失败**: 确认Zotero正在运行且API设置正确
3. **PDF注释提取失败**: 检查PDF文件权限和格式

### 日志查看
服务器日志会在控制台输出，包含详细的错误信息。

## 联系支持

如遇到问题，请检查：
1. 所有依赖是否正确安装
2. API密钥是否有效
3. 网络连接是否正常
4. 防火墙设置是否阻止了连接