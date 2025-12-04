# 毕业论文 AI 工具链 README

本仓库是围绕“毕业论文写作”构建的一套 AI 辅助工具链，整合了：

- Zotero 文献管理（采集、元数据、PDF、引用）
- Obsidian 笔记与知识库管理（文献笔记、概念、框架、草稿）
- MCP（Model Context Protocol）服务层（Zotero、PDF、外部 AI 服务）

通过统一的 Python 包 `thesis_tools` 与命令行入口，可以用一条命令跑通
“Zotero → 结构化分析 → Obsidian 笔记 → 报告/写作”的基础流程。

## 一、环境准备 Environment

- 操作系统：Windows 10 / 11
- Python：3.12+
- Node.js：LTS（用于 MCP 服务）
- 已安装并配置好的 Zotero 7 与 Obsidian

推荐使用虚拟环境：

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -U pip requests
```

## 二、统一 CLI 使用方式

在仓库根目录下，通过 `thesis_tools.cli` 统一调用各个子命令：

```bash
cd E:\仓库\毕业论文
python -m thesis_tools.cli setup
```

常用子命令：

- `setup`：检查配置文件与环境变量  
  `python -m thesis_tools.cli setup`

- `ingest`：从 Zotero 拉取文献并更新 `report/zotero_items.json`  
  `python -m thesis_tools.cli ingest --limit 100`

- `analyze`：分析最近文献，生成 `report/recent_literature_analysis.json`  
  `python -m thesis_tools.cli analyze`

- `analyze --foreign-only`：分析外文文献，生成 `report/foreign_literature_analysis.json`  
  `python -m thesis_tools.cli analyze --foreign-only`

- `export-notes`：基于最新文献在 Obsidian 中生成文献笔记  
  `python -m thesis_tools.cli export-notes`

- `sync-check`：检查 Zotero API 与 Obsidian 目录结构  
  `python -m thesis_tools.cli sync-check`

- `report`：汇总当前 JSON 报告并做结构校验  
  `python -m thesis_tools.cli report`

> 提示：Obsidian vault 路径、模板目录等参数来自
> `config/zotero_obsidian_config.json` 或环境变量 `THESIS_OBSIDIAN_VAULT`；
> 首次使用前请先根据 `config/` 文档完成配置。

## 三、脚本与模块结构

- `thesis_tools/`：Python 核心工具包  
  - `zotero_ingest.py`：从 Zotero API 拉取并规范化文献记录  
  - `zotero_analysis.py`：最近文献分析、外文文献分析  
  - `obsidian_export.py`：基于模板生成 Obsidian 文献笔记  
  - `sync_checks.py`：Zotero / Obsidian 健康检查与同步测试  
  - `models.py`：`Literature` / `Note` / `AnalysisResult` 等领域模型  
  - `schemas.py`：`zotero_items.json` 等中间 JSON 的结构约定与轻量校验  
  - `reference_tools.py` / `optimize_proposal_references.py`：开题报告参考文献相关工具  
  - `mcp_client.py`：与 `ilfow` MCP 管理服务交互的封装（服务启动、停止等）  
  - `cli.py`：统一命令行入口（`python -m thesis_tools.cli`）

- `scripts/`：命令行脚本入口（内部复用 `thesis_tools`）  
  - `get_zotero_items.py` / `get_recent_literature.py` / `analyze_foreign_literature.py`  
  - `create_obsidian_notes.py` / `batch_create_notes.py` / `create_sample_notes.py`  
  - `setup_obsidian_zotero.py`：初始化 Obsidian + Zotero 集成环境  
  - `test_zotero_api.py` / `test_obsidian_zotero_sync.py`：冒烟与集成测试入口  
  - `optimize_proposal_references.py` / `optimize_hekang_proposal_references.py`：开题报告参考文献优化工具

- `ilfow/`：MCP 服务（Node）与配置  
  - `mcp_config.json`：列出可用 MCP 服务与 HTTP 传输配置  
  - `mcp-server.js`：启动 / 管理 MCP 服务的 Node 服务

- `docs/`：架构与技术文档（参见 `IFLOW.md`、`docs/技术栈.md` 等）

- `config/`：Zotero / Obsidian / 集成配置（JSON + Markdown）

- `report/`：监控与分析输出（例如 `zotero_items.json`、`zotero_items_without_notes.json`、`recent_literature_analysis.json`、`obsidian_zotero_sync_report.json`、Zotero 处理报告 Markdown）

- `obsidian/`：Obsidian vault（AI 笔记等）

- `zotero/`：Zotero 本地数据库与附件镜像（`Base/zotero.sqlite`、`Base/storage/` 等）

## 四、测试与验证 Tests

当前提供了一组以 `unittest` 为基础的测试，用于快速验证核心流水线：

- `tests/test_zotero_ingest.py`：验证 ingest 输出结构与 schema 一致  
- `tests/test_obsidian_export.py`：验证 Obsidian 笔记生成逻辑  
- `tests/test_pipeline_e2e.py`：从模拟 API 数据到外文文献分析报告的端到端小样本测试

在虚拟环境中可运行：

```bash
python -m unittest discover -s tests
```

此外还有脚本级冒烟测试：

- `python scripts/test_zotero_api.py`：测试 Zotero API 连接  
- `python scripts/test_obsidian_zotero_sync.py`：测试 Obsidian 目录结构与同步健康度（会更新 `report/obsidian_zotero_sync_report.json`）

## 五、MCP 与 AI 能力

- MCP 服务由 `ilfow/mcp-server.js` 管理，配置见 `ilfow/mcp_config.json`。  
- Python 侧通过 `thesis_tools.mcp_client` 管理 MCP 服务的启动/停止与状态查询。  
- 针对 PDF 深度分析、长文档理解等高阶能力，推荐通过支持 MCP 的客户端
  （如带 MCP 扩展的编辑器或终端）调用对应服务，而非在零散脚本中直接拼接 HTTP 调用。

## 六、常见问题 FAQ（摘要）

- **Zotero API 连接失败**：  
  - 检查 `ZOTERO_API_KEY` / `ZOTERO_LIBRARY_ID` 环境变量；  
  - 可先运行 `python scripts/test_zotero_api.py` 做独立验证。

- **Obsidian 笔记未生成**：  
  - 确认 `config/zotero_obsidian_config.json` 中的 `obsidian_vault_path`、模板文件、目标目录是否存在；  
  - 使用 `python -m thesis_tools.cli export-notes` 并检查终端输出。

- **同步检查失败**：  
  - 查看 `report/obsidian_zotero_sync_report.json` 中的具体失败项；  
  - 对照 `IFLOW.md` 与 `docs/技术栈.md` 中的路径说明逐项排查。

如需对目录结构或 CLI 做进一步扩展，建议先更新 `IFLOW.md` 与 `AGENTS.md`，
保持“结构清晰、入口统一”的整体设计。 
