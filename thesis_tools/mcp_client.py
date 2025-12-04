#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP 客户端封装模块 mcp_client
============================

本模块用于在 Python 侧以统一方式与 `ilfow/` 中的 MCP 管理服务交互，
目前聚焦于以下两类能力：

- HTTP 级别的 MCP 服务器生命周期管理（启动 / 停止 / 查询状态）
- 为后续 AI 分析能力预留的统一调用接口（如 analyze_pdf / summarize_notes）

说明：
- 真实的 MCP 工具调用（如对 PDF 进行深度分析）依赖于上层 LLM/MCP 客户端，
  当前仓库中仅提供 MCP 服务器管理端点（见 `ilfow/mcp-server.js`）。
- 因此，本模块中的高层分析函数暂以占位实现形式给出，便于后续扩展。
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


ROOT_DIR = Path(__file__).resolve().parents[1]
ILFOW_DIR = ROOT_DIR / "ilfow"
MCP_CONFIG_PATH = ILFOW_DIR / "mcp_config.json"


@dataclass
class MCPHttpConfig:
    """MCP HTTP 传输配置（来自 ilfow/mcp_config.json::httpTransport）。"""

    host: str = "localhost"
    port: int = 3000
    enabled: bool = True

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"


def _load_http_config() -> MCPHttpConfig:
    """从 ilfow/mcp_config.json 中加载 HTTP 传输配置，不存在时使用默认值。"""
    if not MCP_CONFIG_PATH.exists():
        return MCPHttpConfig()

    try:
        with MCP_CONFIG_PATH.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception:
        return MCPHttpConfig()

    transport = raw.get("httpTransport") or {}
    host = str(transport.get("host") or "localhost")
    port_value = transport.get("port", 3000)
    try:
        port = int(port_value)
    except (TypeError, ValueError):
        port = 3000

    enabled = bool(transport.get("enabled", True))
    return MCPHttpConfig(host=host, port=port, enabled=enabled)


def _request(
    method: str,
    path: str,
    *,
    timeout: float = 10.0,
    json_body: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """向 MCP 管理服务发送 HTTP 请求并返回 JSON 响应。

    若 MCP 管理服务不可达或返回非 JSON，将抛出 RuntimeError，调用方可决定如何处理。
    """
    config = _load_http_config()
    if not config.enabled:
        raise RuntimeError("MCP HTTP 传输在 mcp_config.json 中被禁用（enabled = false）")

    url = f"{config.base_url}{path}"

    try:
        response = requests.request(
            method,
            url,
            json=json_body,
            timeout=timeout,
        )
    except Exception as exc:  # pragma: no cover - 网络 I/O
        raise RuntimeError(f"无法连接 MCP 管理服务 {url}: {exc}") from exc

    if response.status_code >= 400:
        raise RuntimeError(
            f"MCP 管理服务返回错误 {response.status_code}: {response.text}"
        )

    try:
        return response.json()
    except Exception:
        # 响应不是 JSON 时，返回简单包装后的结果
        return {"status_code": response.status_code, "text": response.text}


# ---------------------------------------------------------------------------
# MCP 服务器生命周期管理
# ---------------------------------------------------------------------------


def list_servers() -> Dict[str, List[str]]:
    """列出 MCP 管理服务中“已配置”和“当前运行”的服务器名称。"""
    data = _request("GET", "/api/servers")
    running = data.get("running") or []
    configured = data.get("configured") or []
    return {
        "running": list(running),
        "configured": list(configured),
    }


def start_server(name: str) -> Dict[str, Any]:
    """启动单个 MCP 服务器（如 'zotero'、'pdf-reader'）。"""
    return _request("POST", f"/api/servers/{name}/start")


def stop_server(name: str) -> Dict[str, Any]:
    """停止单个 MCP 服务器。"""
    return _request("POST", f"/api/servers/{name}/stop")


def start_all_servers() -> Dict[str, Any]:
    """启动 mcp_config.json 中配置的所有 MCP 服务器。"""
    return _request("POST", "/api/servers/start-all")


def stop_all_servers() -> Dict[str, Any]:
    """停止当前运行的所有 MCP 服务器。"""
    return _request("POST", "/api/servers/stop-all")


# ---------------------------------------------------------------------------
# 为后续 AI 能力预留的占位接口
# ---------------------------------------------------------------------------


def analyze_pdf(literature_key: str) -> Dict[str, Any]:
    """占位接口：对指定文献的 PDF 进行分析。

    当前仓库中尚未提供面向 Python 的直接 MCP 调用通道，
    实际的 PDF 深度分析通常通过支持 MCP 的对话式客户端完成。

    该函数的存在主要用于：
    - 让上层代码在接口层与 MCP 解耦
    - 为后续接入具体 MCP 工具（如 zotero-pdf、pdf-reader）预留统一入口
    """
    raise NotImplementedError(
        "analyze_pdf 目前仅为占位接口：\n"
        "- MCP 服务器由 ilfow/mcp-server.js 管理\n"
        "- 具体 PDF 分析需通过 MCP 客户端（如支持 MCP 的对话式 AI）调用\n"
        "- 如需在 Python 中直接调用，请在 mcp_client.py 中实现具体协议适配"
    )


def summarize_notes(note_id: str) -> Dict[str, Any]:
    """占位接口：对指定 Obsidian/Zotero 笔记进行自动摘要。

    实际实现依赖于具体 MCP 工具与协议，当前仅提供统一接口约定。
    """
    raise NotImplementedError(
        "summarize_notes 目前仅为占位接口，尚未在仓库中接入具体 MCP 工具。"
    )


