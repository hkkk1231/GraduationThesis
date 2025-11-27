当前目录下一共有三个文件夹，分别是 obsidian，zotero，iflow，config。
我的目标是：利用 AI 工具辅助阅读、编写毕业论文。
目录架构：毕业论文的参考文献放在 zotero 中。AI 做的笔记放入 obsidian 中。iflow 的相关配置以及 MCP 放到 iflow 目录中。config 放一些项目的配置文件。roport 放置智能体的汇报文件。

具体方案

1. MCP 服务器
   安装基础的 Zotero MCP 和 PDF Reader MCP
   安装 cookjohn/zotero-mcp (GitHub 星标项目) - 提供更强大的 PDF 注释提取功能
   集成 54yyyu/zotero-mcp - 支持直接 PDF 处理和图像注释
   配置 Streamable HTTP 协议替代 stdio，提升稳定性
2. 新增关键 MCP 服务器
   Morphik MCP - 专门用于深度文档理解，特别适合复杂论文分析
   文档处理 MCP 服务器 - 基于 ABBBY 技术，提供 OCR 和结构化数据提取
   学术搜索 MCP - 集成 arXiv、Web of Science、PubMed 等多个学术平台
3. 笔记管理系统优化方案:
   Obsidian + Zotero 集成 - 建立双向链接的知识图谱
   Zotfile 插件 - 自动提取 PDF 注释并转换为笔记
   Better BibTeX
