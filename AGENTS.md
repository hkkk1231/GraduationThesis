# Repository Guidelines

## Project Structure & Module Organization
Core Python automation logic lives in the `thesis_tools/` package and is exposed via a unified CLI (`python -m thesis_tools.cli`). Convenience entry scripts live under `scripts/` (e.g. `scripts/get_zotero_items.py`, `scripts/create_obsidian_notes.py`) when you prefer direct calls. Long-lived configuration is in `config/` (JSON + Markdown) and architecture references in `docs/` plus `IFLOW.md`. The MCP controller resides in `ilfow/` beside `mcp_config.json`, while generated knowledge assets belong in `obsidian/` and monitoring outputs in `report/`; keep those directories tidy and version controlled.

## Build, Test, and Development Commands
Target Python 3.12, Node LTS, and Windows paths. Typical loop:
```
python -m venv .venv && .\.venv\Scripts\activate
python -m pip install requests
python -m thesis_tools.cli ingest         # pull Zotero data into JSON
python -m thesis_tools.cli export-notes   # emit Obsidian-ready notes
cd ilfow && npm install && npm run start-mcp
python scripts/test_zotero_api.py
python scripts/test_obsidian_zotero_sync.py
```
`npm run setup` installs the optional MCP servers listed in `ilfow/package.json`; invoke it only when provisioning a new machine.

## Coding Style & Naming Conventions
Use 4-space indentation and snake_case names for Python helpers, aligning with existing modules. JavaScript utilities should stick to camelCase plus class-based organization (`MCPServerManager`). Markdown and JSON artifacts must remain UTF-8; keep Markdown bilingual headers (Chinese primary, English keywords where necessary) and prefer deterministic snake_case keys in structured files.

## Testing Guidelines
`test_zotero_api.py` is the smoke test for credentials and Zotero connectivity; run it whenever API keys or `config/zotero-config.md` change. `test_obsidian_zotero_sync.py` checks vault directories, validates template presence, emits a disposable note, and updates `report/obsidian_zotero_sync_report.json`—verify paths before running and delete the generated note if you skip the cleanup branch. After each ingestion, eyeball the refreshed JSON in `report/` and confirm the new Obsidian links resolve.

## Commit & Pull Request Guidelines
Match the log history by starting commit messages with a short Chinese verb phrase plus scope (e.g., `完善文献深度阅读流程`). Describe touched modules, list critical scripts or commands that were run, and mention resulting artifacts (`report/*.json`, `docs/*`). Pull requests should enumerate affected directories, link to the issue or task, include smoke-test evidence (scripts/MCP boots), and attach UI screenshots whenever `obsidian/` content changes.

## Security & Configuration Tips
Secrets in `config/zotero_obsidian_config.json` and `ilfow/mcp_config.json` are placeholders only; export real `ZOTERO_API_KEY`, ABBYY, or Morphik tokens through your shell before starting the services. Scrub sensitive data from generated JSON before committing, and keep local-only vault exports ignored through `.gitignore` entries.
