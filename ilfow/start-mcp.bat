@echo off
title MCP服务器管理器

echo 毕业论文AI工具 - MCP服务器
echo ========================
echo.

cd /d "%~dp0"

echo 正在启动MCP服务器管理器...
echo 服务器将在 http://localhost:3000 运行
echo 按 Ctrl+C 停止所有服务器
echo.

node mcp-server.js

echo.
echo MCP服务器已停止
pause