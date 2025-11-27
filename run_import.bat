@echo off
echo 正在通过debug-bridge导入PDF到Zotero...
echo.
echo 请先确保：
echo 1. Zotero已经启动
echo 2. 已安装Better BibTeX插件 (zotero-better-bibtex-7.0.35.xpi)
echo 3. 在Zotero中: 工具 - 插件 - 齿轮图标 - Install Add-on From File... - 选择xpi文件
echo.
echo 安装完成后，按任意键继续导入...
pause > nul

echo 正在发送导入命令到Zotero...
powershell -Command "curl -s -H 'Content-Type: application/javascript' -X POST --data-binary @'E:\仓库\毕业论文\import_pdf_zotero.js' http://127.0.0.1:23119/debug-bridge/execute"

echo.
echo 导入完成！请检查Zotero中的文献库。
pause