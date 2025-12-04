# Repository Guidelines

## 项目结构与模块组织 Project Structure & Module Organization
- 核心 Python 自动化逻辑集中在 `thesis_tools/` 包中，并通过统一 CLI 入口 `python -m thesis_tools.cli` 暴露。
- `scripts/` 目录保留给未来的一次性脚本，目前默认空；推荐直接使用 CLI 而不是单独脚本。
- 长期配置位于 `config/`，架构与流程文档在 `docs/`（本目录下为 agent-facing 报告），MCP 控制器在 `ilfow/`，生成的笔记在 `obsidian/`，监控与中间 JSON 输出在 `report/`。
- 保持 `obsidian/` 与 `report/` 结构整洁并纳入版本控制；将 `config/` 与 `docs/` 视为工作流的权威说明。

## 构建与开发命令 Build, Test, and Development Commands
- 使用 Python 3.12 与 Node LTS（Windows 环境）；推荐：
  - `python -m venv .venv && .\.venv\Scripts\activate`
  - `python -m pip install requests`
- 数据流主通路（推荐）：
  - `python -m thesis_tools.cli ingest` – 从 Zotero 拉取条目并生成/更新 `report/zotero_items.json` 等 JSON。
  - `python -m thesis_tools.cli analyze` – 分析最近文献，生成 `report/recent_literature_analysis.json` 等报告。
  - `python -m thesis_tools.cli export-notes` – 将文献转为 Obsidian 笔记。
- MCP 服务：
  - `cd ilfow && npm install && npm run start-mcp`
  - 仅在新机器上运行 `npm run setup` 以安装可选 MCP servers。

## 编码风格与命名规范 Coding Style & Naming Conventions
- Python：4 空格缩进，函数/变量使用 snake_case；模块粒度保持任务单一，公共逻辑优先收敛到 `thesis_tools.*`。
- JavaScript/TypeScript（`ilfow/`）：函数 camelCase，类 PascalCase（如 `MCPServerManager`）。
- Markdown / JSON：UTF-8 编码；标题保持中英双语（中文为主、英文关键词补充），JSON key 建议使用稳定的 snake_case。

## 测试规范 Testing Guidelines
- 更推荐使用统一 CLI 与 `tests/`：
  - `python -m unittest discover -s tests`：执行端到端与单元测试（如 `test_pipeline_e2e.py`、`test_obsidian_export.py`）。
  - `python -m thesis_tools.cli sync-check`：基于 `thesis_tools.sync_checks` 的 Zotero API 冒烟测试与 Obsidian 结构检查；更改凭据或 `config/zotero-config.md` 后运行。
  - `python -m thesis_tools.cli report`：汇总 `report/` 下 JSON 报告并做结构校验。
- 每次 ingestion 后，建议检查：
  - `report/zotero_items.json` / `report/recent_literature_analysis.json` 结构是否符合 `thesis_tools.schemas` 约定；
  - 新生成的 Obsidian 链接是否可点击回到 Zotero 条目。

## 提交与合并请求规范 Commit & Pull Request Guidelines
- Commit message 采用“简短中文动词 + 范围”，如：`完善文献深度阅读流程`。
- 在提交说明 / PR 描述中：
  - 列出修改过的模块与目录（如 `thesis_tools/*`、`scripts/*`、`docs/*`）；
  - 标明运行过的关键命令（CLI 子命令、脚本、测试）；
  - 说明新产生或更新的工件（如 `report/*.json`、`obsidian/*`、`docs/AgentReport/*`）。
- PR 应：
  - 明确关联的任务或 Issue；
  - 在涉及 Obsidian 内容变更时附上截图或笔记片段；
  - 给出基本的“可以安全回滚”的说明（例如仅移动文件/重构结构，无数据层变更）。

## 安全与配置建议 Security & Configuration Tips
- 真实密钥一律不入库。`config/zotero_obsidian_config.json` 与 `ilfow/mcp_config.json` 中应只包含占位符：
  - 运行前通过环境变量注入：`ZOTERO_API_KEY`、`ZOTERO_LIBRARY_ID`、ABBYY/Morphik 等 token。
- 提交前检查：
  - 生成的 JSON 报告中不含个人身份敏感信息；
  - `.gitignore` 持续忽略本地-only vault 导出、`.venv/`、`ilfow/node_modules/` 等。
- MCP / 外部服务访问时，优先通过 `thesis_tools.mcp_client` 或 `ilfow/mcp-server.js` 封装的接口，避免在零散脚本中硬编码 URL 与密钥。
