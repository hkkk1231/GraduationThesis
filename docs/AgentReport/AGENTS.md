# Repository Guidelines

## 项目结构与模块组织 Project Structure & Module Organization
- Root Python automation scripts (`get_zotero_items.py`, `create_obsidian_notes.py`, `analyze_foreign_literature.py`) move Zotero data into the Obsidian vault.
- Long-lived configuration lives in `config/`, architecture and process docs in `docs/` (this folder contains agent-facing reports), MCP controller in `ilfow/`, generated notes in `obsidian/`, and monitoring outputs in `report/`.
- Keep `obsidian/` and `report/` tidy and version controlled; treat `config/` and `docs/` as the source of truth for workflows.

## 构建与开发命令 Build, Test, and Development Commands
- Use Python 3.12 and Node LTS on Windows; create a venv with `python -m venv .venv && .\.venv\Scripts\activate`.
- Install core dependencies with `python -m pip install requests` in the repository root.
- Data flow loop:
  - `python get_zotero_items.py` – pull Zotero items into JSON under `report/`.
  - `python create_obsidian_notes.py` – generate Obsidian-ready notes into `obsidian/`.
- MCP services: `cd ilfow && npm install && npm run start-mcp`; run `npm run setup` only when provisioning a new machine.

## 编码风格与命名规范 Coding Style & Naming Conventions
- Python: 4-space indentation, snake_case for helpers and variables; keep modules small and task-focused.
- JavaScript/TypeScript (in `ilfow/`): camelCase for functions, PascalCase for classes (e.g., `MCPServerManager`).
- Markdown/JSON: UTF-8 encoded, concise bilingual headings (Chinese + key English terms), deterministic snake_case keys in JSON.

## 测试规范 Testing Guidelines
- Run `python test_zotero_api.py` after changing Zotero credentials or `config/zotero-config.md`.
- Run `python test_obsidian_zotero_sync.py` when modifying note templates or vault paths; confirm it updates `report/obsidian_zotero_sync_report.json` and clean up any temporary notes.

## 提交与合并请求规范 Commit & Pull Request Guidelines
- Start commit messages with a short Chinese verb phrase plus scope, e.g., `完善文献深度阅读流程`.
- In commit bodies or PR descriptions, list touched modules, key scripts run, and resulting artifacts (e.g., `report/*.json`, `docs/*`, `obsidian/*`).
- Link PRs to issues or tasks and attach screenshots or vault snippets whenever user-facing Obsidian content changes.

## 安全与配置提示 Security & Configuration Tips
- Keep real secrets out of version control: use environment variables for `ZOTERO_API_KEY` and other tokens; JSON in `config/` and `ilfow/mcp_config.json` should contain placeholders only.
- Scrub sensitive data from generated JSON before committing and verify `.gitignore` continues to exclude local-only Obsidian vaults or exports.

