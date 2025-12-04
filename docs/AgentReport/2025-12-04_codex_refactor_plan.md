# 毕业论文项目重构规划存档 Thesis Project Refactor Plan

日期 Date: 2025-12-04  
来源 Source: Codex CLI Agent（GPT-5.1）

---

## 一、项目目的与总体定位 Project Goal

- 构建一套围绕“毕业论文写作”的 AI 辅助工作流，打通：
  - Zotero 文献管理（收集、元数据、PDF、引用）  
  - Obsidian 笔记与知识库管理（文献笔记、概念、框架、草稿）  
  - MCP（Model Context Protocol）服务层（Zotero、PDF、外部 AI 服务）的自动化能力
- 形成完整流水线：**Zotero 文献 → 结构化数据/分析 → Obsidian 笔记 → 论文写作与报告输出**。

---

## 二、当前已实现功能 Current Implemented Features

### 1. 配置与架构

- `config/`：集中管理 Zotero / Obsidian / 连接信息
  - `zotero-config.md`、`obsidian-config.md`：安装路径、字段约定、连接方式说明
  - `zotero_obsidian_config.json`：API Key、库 ID、Obsidian vault 路径等关键参数
- 架构文档
  - `IFLOW.md`：整体工作流与目录结构说明  
  - `docs/技术栈.md`、`docs/依赖关系.md`：技术栈、依赖关系、项目结构概览

### 2. Zotero 侧能力

- 文献拉取与导出
  - `get_zotero_items.py` / `get_zotero_items.js`：从 Zotero 提取条目，生成 `zotero_items.json` 等本地 JSON
  - `test_zotero_api.py`：验证 Zotero API 凭据与连通性
- 文献分析
  - `get_recent_literature.py`：获取最近文献并输出分析，写入 `recent_literature_analysis.json`
  - `check_literature_details.py`：检查文献条目的字段完整性等细节
  - `analyze_foreign_literature.py`：针对外文文献进行重点分析（结构拆解、关键信息提取等）

### 3. Obsidian 侧能力

- 连接与初始化
  - `setup_obsidian_zotero.py`：配置 Obsidian 与 Zotero 的基础集成（路径、模板、同步方式）
- 笔记生成
  - `create_obsidian_notes.py`：根据 Zotero JSON 与模板生成 Obsidian 文献笔记
  - `batch_create_notes.py`、`create_sample_notes.py`：批量生成笔记/示例笔记，便于调试与展示
- 同步检查
  - `test_obsidian_zotero_sync.py`：检查 vault 目录、模板存在性，执行一次同步测试，并写入 `report/obsidian_zotero_sync_report.json`

### 4. MCP / ilfow 服务层

- `ilfow/` 目录：
  - `mcp-server.js`、`mcp_config.json`、`package.json`：MCP 控制器，集成 Zotero、PDF Reader 与第三方 MCP 服务器
  - `setup.bat`、`start-mcp.bat`：安装依赖、启动 MCP 服务
  - `test-zotero-connection.js`：测试 MCP 层与 Zotero 的连接
  - `create_word_report.py`、`create_word_report_direct.py`：根据分析结果生成 Word 报告/文档草稿

### 5. 报告与监控

- `report/`：
  - `obsidian_zotero_sync_report.json`：记录一次 Obsidian-Zotero 同步的检查结果
  - 其他报告文件（例如 `zotero_literature_report.md`、系统状态报告等），用于描述当前系统状态与文献处理进度

---

## 三、主要问题与不足 Main Issues and Gaps

1. **脚本散乱，缺乏统一模块化结构**
   - 根目录存在大量独立 Python 脚本（`get_zotero_items.py`、`create_obsidian_notes.py`、`get_recent_literature.py`、`analyze_foreign_literature.py` 等），功能交叉但缺少统一分层。
   - 按“动作命名的脚本”主导，而非“按领域模块组织的包结构”（如 `zotero/ingest.py`、`obsidian/export.py`）。

2. **领域模型缺失，数据结构分散**
   - `zotero_items.json`、`recent_literature_analysis.json` 等 JSON 无统一 schema 文档，字段含义分散在脚本内部和注释中。
   - 没有统一的 `Literature` / `Note` / `AnalysisResult` 等领域对象定义，字段演化难以集中管理。

3. **测试体系薄弱，自动化不足**
   - 虽有 `test_zotero_api.py`、`test_obsidian_zotero_sync.py`，但属于“脚本式 smoke test”，没有标准的 `tests/` 目录和用例结构。
   - 缺少统一的自动化测试入口（如 `pytest` / `unittest`），无法快速做回归验证。

4. **Python / MCP / Node 三层边界不清晰**
   - Python 脚本同时承担业务逻辑、IO 读写、命令行解析，层次耦合度高。
   - 没有清晰的 MCP 客户端封装（例如 `mcp_client.py`），Python 与 MCP 的交互在多个脚本中散乱存在。

5. **文档与实际代码结构存在偏差风险**
   - `IFLOW.md` 和 `docs/*.md` 描述了理想化的结构和数据流，但顶层仍然偏“工具脚本堆”。
   - 如果不及时同步，未来可能出现“文档与代码结构不完全一致”的问题。

6. **命名与目录约定略有不统一**
   - 例如 `ilfow/` 目录与 `IFLOW.md` 名称存在细微差异，可能是历史命名遗留。
   - `backup/`、`zotero_items_without_notes.json` 等资源的角色与生命周期在文档中尚未完全标准化说明。

---

## 四、重构总体思路 Overall Refactor Strategy

重构目标：在不破坏现有工作流的前提下，将“脚本堆”演进为 **结构清晰、模块划分明确、可持续扩展** 的论文助手平台。

分为三个阶段：

1. **第一阶段：目录与模块重组（逻辑基本不变）**  
2. **第二阶段：抽象领域模型与统一数据流**  
3. **第三阶段：统一 CLI / 服务化接口 + 测试体系搭建**

---

## 五、第一阶段：目录与模块重组 Phase 1 – Structure & Modules

核心原则：**不大改业务逻辑，只重排结构，抽出可复用模块**。

### 1. 建立 Python 包 `thesis_tools/`

建议新结构示例：

- `thesis_tools/`
  - `__init__.py`
  - `zotero_ingest.py`：封装原 `get_zotero_items.py` 核心逻辑
  - `zotero_analysis.py`：封装 `get_recent_literature.py`、`analyze_foreign_literature.py` 的分析逻辑
  - `obsidian_export.py`：封装 `create_obsidian_notes.py`、`batch_create_notes.py`、`create_sample_notes.py` 的笔记生成逻辑
  - `sync_checks.py`：抽取 `test_zotero_api.py`、`test_obsidian_zotero_sync.py` 中可复用的检查逻辑
  - `models.py` / `schemas.py`：为第二阶段准备的领域模型与数据结构定义

### 2. 建立 `scripts/` 目录作为脚本入口层

- 将当前根目录的脚本改为“薄入口”，迁移到 `scripts/`：
  - `scripts/get_zotero_items.py`
  - `scripts/create_obsidian_notes.py`
  - `scripts/get_recent_literature.py`
  - `scripts/analyze_foreign_literature.py`
  - `scripts/check_literature_details.py`
  - `scripts/setup_obsidian_zotero.py`
  - `scripts/test_zotero_api.py`
  - `scripts/test_obsidian_zotero_sync.py`
- 脚本自身只负责：
  - 解析命令行参数（`argparse`）
  - 调用 `thesis_tools` 中的函数
  - 处理退出码与基础日志输出

### 3. 平滑迁移策略

- 初期可以在根目录保留原脚本文件，但内部改为简单地 `import scripts/...` 或 `thesis_tools`，保证现有调用方式不被打断。
- 等新的目录结构稳定后，再统一更新文档与 README，逐步引导使用 `scripts/` 或 CLI。

---

### 4. 第一阶段进度小结 Phase 1 Progress

- 已完成 `thesis_tools/` 包搭建：`zotero_ingest.py`、`zotero_analysis.py`、`obsidian_export.py`、`sync_checks.py`、`models.py`、`schemas.py` 均已落地，其中 `models.py` / `schemas.py` 暂为占位。
- 已创建 `scripts/` 入口脚本：`scripts/get_zotero_items.py`、`scripts/get_recent_literature.py`、`scripts/create_obsidian_notes.py` 等负责命令行入口与日志输出，内部复用 `thesis_tools` 中的功能函数。
- 根目录原有脚本（如 `get_zotero_items.py`、`get_recent_literature.py`、`create_obsidian_notes.py`、`test_zotero_api.py`、`test_obsidian_zotero_sync.py`）已改造成薄入口，主要职责是转发到 `scripts/` 或 `thesis_tools`，保持原有调用方式不变。
- `test_zotero_api.py` 和 `test_obsidian_zotero_sync.py` 的核心检查逻辑已抽取入 `thesis_tools.sync_checks`，两处测试与后续 CLI 将共用同一套健康检查实现，属于“重排结构、不改业务语义”的调整，符合第一阶段的改造边界。

---

## 六、第二阶段：领域模型与数据流抽象 Phase 2 – Domain Models & Data Flow

目标：让“文献、笔记、分析结果”都有统一、明确的数据结构与 schema，减少隐式耦合。

### 1. 定义领域模型 `thesis_tools/models.py`

示例模型：

- `Literature`：
  - 字段：`id`, `title`, `authors`, `year`, `venue`, `tags`, `language`, `pdf_path`, `abstract`, `notes` 等
- `Note`：
  - 字段：`note_id`, `literature_id`, `note_path`, `summary`, `key_points`, `quotes`, `status`（未读/粗读/深度阅读）等
- `AnalysisResult`：
  - 字段：`literature_id`, `problem_statement`, `methodology`, `contribution`, `limitations`, `future_work` 等

可以使用 `dataclasses` 或 `pydantic` 来实现，保证类型明确。

### 2. 统一 JSON Schema 与字段命名

- 在 `thesis_tools/schemas.py` 或 `docs/data_schema.md` 中定义：
  - `zotero_items.json` 的字段结构
  - `recent_literature_analysis.json` 的字段结构
- 约定：
  - 全部使用 snake_case 命名
  - 明确必选/可选字段
  - 时间、日期、数值等格式规范

### 3. 统一数据流水线

- 标准流程：
  1. **Zotero → Raw JSON**：`zotero_ingest.fetch_from_zotero()` → `zotero_items.json`
  2. **Raw JSON → 分析结果**：`zotero_analysis.analyze_items()` → `recent_literature_analysis.json`（或多种分析结果 JSON）
  3. **分析结果 → Obsidian 笔记**：`obsidian_export.generate_notes()` → 写入 `obsidian/` 相应目录
- 其他辅助脚本（如单篇检查、外文分析）统一复用上述模型和 JSON，而不是各自定义一套结构。

---

## 七、第三阶段：统一 CLI、服务化与测试体系 Phase 3 – Unified CLI, Services & Tests

目标：提供统一命令行入口和系统测试能力，使得整套流程“一条命令跑通”并可自动回归。

### 1. 统一 CLI 入口

- 在根目录提供一个统一命令（例如）：
  - `python -m thesis_tools.cli ...` 或配置 `thesis` 作为 `console_scripts`
- CLI 支持子命令：
  - `thesis setup`：检查配置、路径与 MCP 状态
  - `thesis ingest`：从 Zotero 拉取文献并更新 `zotero_items.json`
  - `thesis analyze`：对最近或指定文献集进行分析
  - `thesis export-notes`：生成/更新 Obsidian 笔记
  - `thesis report`：汇总生成监控报告（包括 `report/*.json`、`zotero_literature_report.md` 等）

### 2. 测试体系搭建

- 新建 `tests/` 目录：
  - `tests/test_zotero_ingest.py`
  - `tests/test_obsidian_export.py`
  - `tests/test_pipeline_e2e.py`（端到端小样本测试）
- 迁移现有脚本中的检查逻辑：
  - 基于第一阶段已完成的 `thesis_tools.sync_checks`，在 `tests/` 下复用同一套检查函数，并为 CLI 提供统一入口（不再在脚本中复制检查代码）。
- 使用 `pytest` 或 `unittest`：
  - 确保文献解析、笔记生成、关键 CLI 子命令能稳定运行。

### 3. MCP / ilfow 的边界与封装

- 在 `thesis_tools/mcp_client.py` 中封装与 `ilfow` MCP 服务的交互：
  - 例如 `analyze_pdf(literature_id)`、`summarize_notes(note_id)` 等方法
- 所有 Python 侧需要 AI/MCP 能力的地方，通过 `mcp_client` 访问，避免直接在各脚本中拼接请求。
- MCP 服务本身的 Node 逻辑和配置仍集中在 `ilfow/`，保持分层清晰。

### 4. 文档与 README 更新

- 更新 `IFLOW.md` 与 `docs/技术栈.md`：
  - 使用新的目录结构和模块名称重画架构图
  - 辅以新命令示例（`thesis ingest` / `thesis analyze` / `thesis export-notes`）
- 在根目录更新 `README.md`：
  - 用最少步骤说明如何从零安装并跑通完整流程
  - 简单 FAQ，覆盖常见连接错误与路径问题

---

## 八、与远程仓库的一致性说明 Alignment with Remote

- 当前 `git status -sb` 显示：`main...origin/main`  
- `git diff --stat origin/main...HEAD` 为空，说明：
  - 本地 `main` 与 `origin/main` 内容一致  
  - 没有未推送的本地修改  
- 因此，本次重构计划基于 **当前远程仓库最新结构** 制定，可以直接按上述阶段在新分支或主干上推进。
