@echo off
echo 毕业论文AI工具安装脚本
echo ========================

echo.
echo 正在检查Node.js环境...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Node.js，请先安装Node.js
    pause
    exit /b 1
)
echo Node.js环境检查通过

echo.
echo 正在进入ifow目录...
cd /d "%~dp0"

echo.
echo 正在安装npm依赖...
npm install

echo.
echo 正在安装MCP服务器...
npm run setup

echo.
echo 正在创建启动脚本...
echo @echo off > start-mcp.bat
echo cd /d "%%~dp0" >> start-mcp.bat
echo echo 正在启动MCP服务器... >> start-mcp.bat
echo npm run start-mcp >> start-mcp.bat

echo.
echo 安装完成！
echo.
echo 下一步：
echo 1. 编辑 mcp_config.json 填入API密钥
echo 2. 运行 start-mcp.bat 启动服务器
echo 3. 配置Obsidian和Zotero
echo.
pause