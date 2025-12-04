# 毕业论文项目重构第二阶段设计与进展（Phase 2） Codex Agent Report

日期 Date: 2025-12-04  
代理 Agent: Codex CLI（GPT-5.1）  

---

## 一、本报告与整体重构计划的关系 Relation to Refactor Plan

- 对应文档：`docs/AgentReport/2025-12-04_codex_refactor_plan.md`
- 聚焦部分：**第六节：第二阶段 – 领域模型与数据流抽象 Phase 2 – Domain Models & Data Flow**
- 本报告目标：
  - 将第二阶段中“领域模型 + JSON 数据流”的设计进一步细化为可以落地复用的结构；
  - 归档本次已完成的全部 Phase 2 代码与数据流调整，作为后续 Phase 3（CLI + 测试体系）的基础。

---

## 二、领域模型设计落地情况 Domain Models

本阶段的核心是让“文献、笔记、分析结果”在代码层面有统一的结构化表达，避免脚本之间隐式约定字段。

### 1. `Literature`：统一文献实体模型

- 文件位置：`thesis_tools/models.py`
- 类型定义：使用 `dataclasses.dataclass` 实现：
  - 核心字段（全部 snake_case）：
    - `id`：对应 Zotero 的 `key`
    - `title`
    - `creators`: `list[dict]`
    - `date`: 原始日期字符串（可能包含“2025-…”等）
    - `abstract`
    - `publication_title`
    - `item_type`
    - `tags`: `list[dict]`
    - `notes`: `list[Any]`
    - `date_added` / `date_modified`
    - `url`, `doi`, `pages`, `volume`, `issue`, `publisher`, `language`
- 工厂方法与映射策略：
  - `Literature.from_zotero_api_item(item)`：
    - 输入：Zotero Web API 返回的原始结构（外层包含 `data` 键）。
    - 映射：
      - `data["key"]` → `id`
      - `data["abstractNote"]` → `abstract`
      - `data["publicationTitle"]` → `publication_title`
      - 其他字段直接平移，缺失时返回 `None` 或空列表。
  - `Literature.from_zotero_item_dict(data)`：
    - 输入：本地 `zotero_items.json` 中的单条记录。
    - 兼容字段：
      - 支持 `abstract` / `abstractNote`
      - 支持 `publication_title` / `publicationTitle` / `publication`
      - 支持 `item_type` / `itemType`
      - 时间字段支持 `date_added` / `dateAdded`、`date_modified` / `dateModified`
  - `Literature.to_zotero_item_dict()`：
    - 输出：用于写回 `zotero_items.json` 的字典，**保持与现有脚本兼容的驼峰命名**：
      - `abstractNote` / `publicationTitle` / `itemType` / `dateAdded` / `dateModified` 等。
- 设计结果：
  - 第 2 阶段之后，“Zotero 条目 → 下游分析/导出”的唯一结构化入口是 `Literature`；
  - 各脚本若需要访问文献字段，应优先通过 `Literature` 实例，而非直接操作裸 `dict`。

### 2. `Note` 与 `AnalysisResult`：为深度阅读与报告预留结构

- 文件位置：`thesis_tools/models.py`
- `Note` 模型：
  - 字段：`note_id`, `literature_id`, `note_path`, `summary`, `key_points: list[str]`, `quotes: list[str]`, `status`
  - 方法：
    - `to_dict()`：导出为 JSON 友好结构；
    - `from_dict()`：从持久化结构恢复。
- `AnalysisResult` 模型：
  - 字段：`literature_id`, `problem_statement`, `methodology`, `contribution`, `limitations`, `future_work`
  - 方法：
    - `to_dict()` / `from_dict()` 与 `Note` 类似。
- 当前状态：
  - Phase 2 中先完成了“占位 + 结构设计”，未强行接入所有脚本；
  - 这些模型将主要在 Phase 3 的深度阅读流水线、Word 报告生成、MCP 调用中被正式使用。

---

## 三、JSON Schema 与数据文件约定 JSON Schemas & Files

第二阶段的另一目标是明确关键 JSON 文件的结构与命名约定，使得后续 CLI 和测试可以“按约定读取/断言”。

### 1. `thesis_tools/schemas.py` 中的 Schema 定义

- `ZOTERO_ITEM_SCHEMA` / `ZOTERO_ITEMS_FILE_SCHEMA`：
  - 描述 `zotero_items.json`：
    - 顶层类型：`array`
    - 单条条目：
      - 关键字段：`key`, `title`（必填）
      - 其他字段：`creators`, `date`, `abstractNote`, `publicationTitle`, `itemType`,
        `tags`, `notes`, `dateAdded`, `dateModified`, `url`, `doi`, `pages`, `volume`, `issue`, `publisher`, `language`
- `RECENT_LITERATURE_ANALYSIS_SCHEMA`：
  - 对应 `recent_literature_analysis.json` 顶层结构：
    - `recent_literature`: `array`，元素结构复用 `ZOTERO_ITEM_SCHEMA`
    - `foreign_content_found`: `boolean`
    - `potential_foreign_items`: `array`，元素包含 `title` / `reason` / `publication`
    - `analysis_time`: `string`
    - `total_recent_items`: `integer`
- `FOREIGN_LITERATURE_ANALYSIS_SCHEMA`：
  - 对应 `foreign_literature_analysis.json` 顶层结构：
    - `total_foreign_literature`: `integer`
    - `recent_5_foreign`: `array`，每项为外文文献概要（`key`, `title`, `authors`, `year`, …）
    - `all_foreign_literature`: `array`，结构与 `recent_5_foreign` 相同
    - `analysis_time`: `string`

### 2. 轻量级校验工具

- 为避免引入额外依赖（如 `jsonschema`），本阶段实现了简单的必填字段校验函数：
  - `validate_zotero_items_structure(data)`
  - `validate_recent_literature_analysis(data)`
  - `validate_foreign_literature_analysis(data)`
- 这些函数：
  - 检查最外层 `type` 是否匹配（`object` / `array`）；
  - 检查 `required` 字段是否存在；
  - 不做类型的深度断言（避免与实际数据轻微偏差时频繁报错）。
- 预期用途：
  - Phase 3 的 CLI 子命令可在读写关键 JSON 时调用，以早发现结构性错误；
  - 测试代码可在 fixture / 输出断言中使用这些函数作为“快速 sanity check”。

---

## 四、数据流与管道统一 Data Flow & Pipeline

在 Phase 2 中，数据流从“脚本堆”收敛为明确的三段式流水线，各阶段的 Python 实现如下。

### 1. 阶段一：Zotero 拉取与预处理（Ingest）

- 文件：`thesis_tools/zotero_ingest.py`
- 关键函数：
  - `fetch_from_zotero(api_key, library_id, base_url, limit)`：
    - 从 Zotero Web API 拉取原始条目列表；
    - 仍保留 `API_KEY` / `LIBRARY_ID` / `BASE_URL` 常量，后续可改为从环境变量读取。
  - `process_items(items)`：
    - 将 API 返回的列表映射为 `Literature` 实例，再统一导出为 `dict`：
      - 这是“原始 Zotero 数据 → 项目内部标准结构”的唯一入口。
  - `split_items_by_notes(processed_items)`：
    - 切分出“无任何笔记且类型不为 note 的文献列表”，用于 `zotero_items_without_notes.json`。
  - `save_items_to_files(processed_items, items_without_notes, output_dir=None)`：
    - 默认使用 `ROOT_DIR`（即项目根目录）作为输出路径；
    - 输出：
      - `zotero_items.json`
      - `zotero_items_without_notes.json`
  - `print_summary(processed_items)`：
    - 控制台摘要统计（总数、有/无笔记数量、无笔记文献明细预览）。
- 脚本入口：
  - `scripts/get_zotero_items.py` → 调用 `thesis_tools.zotero_ingest.main()`；
  - 根目录 `get_zotero_items.py` 仍作为兼容入口存在。

### 2. 阶段二：最近文献分析（Recent Analysis）

- 文件：`thesis_tools/zotero_analysis.py`
- 数据加载：
  - `_load_literature_items(items_file)`：
    - 从 `items_file`（默认 `zotero_items.json`）加载原始列表；
    - 将每条记录转换为 `Literature` 实例，跳过非 dict 或解析失败的项。
- 分析函数：
  - `get_recent_literature_details(items_file=DEFAULT_ITEMS_FILE, limit=10)`：
    - 过滤掉 `item_type == "attachment"` 或无标题条目；
    - 按 `(date_added, date, id)` 逆序排序，取前 `limit` 条；
    - 控制台输出详细信息（作者、期刊、摘要、URL/DOI、笔记数）。
  - `analyze_literature_characteristics(items: list[Literature])`：
    - 年份分布（通过正则从 `date` 中提取 4 位年份）；
    - 期刊分布（Top N）；
    - 类型分布；
    - 有/无笔记数量。
  - `check_for_foreign_content(items: list[Literature])`：
    - 针对标题/摘要/期刊，检测“全英文字符串”的潜在外文内容；
    - 返回包含 `title` / `reason` / `publication` 的列表。
- 输出：
  - `main()`：
    - 调用上述三个函数；
    - 将结果写入 `recent_literature_analysis.json`，使用 `Literature.to_zotero_item_dict()` 保持字段结构与 `zotero_items.json` 一致。
- 脚本入口：
  - `scripts/get_recent_literature.py` → 调用 `thesis_tools.zotero_analysis.main()`。

### 3. 阶段三：外文文献分析（Foreign Literature Analysis）

- 文件：`thesis_tools/zotero_analysis.py`
- 判定与抽取：
  - `is_foreign_literature(item: Literature)`：
    - 依据：
      - 作者姓名中是否存在无中文字符的“名+空格+姓”模式；
      - 标题/期刊/摘要中是否存在英文字符且无中文字符。
  - `extract_foreign_literature_info(item: Literature)`：
    - 返回统一结构：
      - `key`, `title`, `authors`, `year`, `abstract`, `publication`, `item_type`,
        `tags`, `date_added`, `url`, `doi`, `pages`, `volume`, `issue`, `publisher`, `language`
- 报告生成：
  - `analyze_foreign_literature(items_file, output_file, recent_limit)`：
    - 从指定 `items_file` 加载 `Literature` 列表；
    - 跳过 `attachment` 类型，筛选出外文文献；
    - 按 `date_added` 逆序排序，生成：
      - `total_foreign_literature`
      - `recent_5_foreign`
      - `all_foreign_literature`
      - `analysis_time`
    - 写入 `foreign_literature_analysis.json`；
    - 在控制台输出最近若干篇外文文献的摘要信息。
- 脚本入口：
  - `scripts/analyze_foreign_literature.py` → 调用 `thesis_tools.zotero_analysis.analyze_foreign_literature()`。

---

## 五、本次 Phase 2 已完成工作小结 Summary of Completed Phase 2 Work

1. **领域模型落地**
   - `thesis_tools/models.py` 中的 `Literature`/`Note`/`AnalysisResult` 已实现；
   - 所有与 Zotero 数据读写相关的核心逻辑，现统一通过 `Literature` 进行字段映射与导出。
2. **JSON 结构与 Schema 约定**
   - `thesis_tools/schemas.py` 中定义了 `zotero_items.json`、`recent_literature_analysis.json` 与 `foreign_literature_analysis.json` 的顶层结构；
   - 提供了轻量级校验函数，后续可直接在 CLI 和测试中复用。
3. **数据流管道重排**
   - `thesis_tools/zotero_ingest.py` 与 `thesis_tools/zotero_analysis.py` 完成了对原有脚本的“模块化收口”：
     - ingest → `zotero_items*.json`
     - analyze_recent → `recent_literature_analysis.json`
     - analyze_foreign → `foreign_literature_analysis.json`
   - 路径处理改为基于 `ROOT_DIR` 推导，减少硬编码绝对路径的依赖。
4. **脚本与模块的一致性验证**
   - 已运行并通过的脚本（基于当前环境）：
     - `python scripts/get_zotero_items.py`
     - `python scripts/get_recent_literature.py`
     - `python scripts/analyze_foreign_literature.py`
   - 对应 JSON 输出的结构与本次定义的 Schema 保持一致。

---

## 六、对后续工作的建议与对接 Phase 3 Handover Suggestions

基于当前 Phase 2 的落地情况，后续可优先推进以下事项，作为 Phase 3 的起点：

1. **将 `Literature` 引入 Obsidian 导出层**
   - 在 `thesis_tools/obsidian_export.py` 中逐步替换对裸 `dict` 的操作：
     - 输入参数从 `dict` 列表升级为 `List[Literature]`；
     - 统一通过模型字段访问作者、年份、期刊等信息。
2. **在 CLI 中复用 Schema 校验**
   - 未来的 `thesis_tools/cli.py` 子命令（如 `thesis analyze` / `thesis report`）在读写 JSON 时：
     - 使用 `validate_zotero_items_structure` / `validate_recent_literature_analysis` / `validate_foreign_literature_analysis` 做快速检查；
     - 在发现结构异常时给出明确的错误提示与修复建议。
3. **测试用例与固定样本**
   - 在 `tests/` 中引入小样本 JSON fixture：
     - 利用当前的模型与 Schema 进行端到端验证；
     - 为 Phase 3 的 CLI 和 MCP 集成提供稳定的回归基础。

> 本报告连同 `thesis_tools/` 中的改动，构成了“第二阶段：领域模型与数据流抽象”的完整落地与归档，可视为进入统一 CLI 与测试体系（Phase 3）的结构化基线。  

