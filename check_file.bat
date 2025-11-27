@echo off
echo 检查插件文件...
if exist "E:\仓库\毕业论文\zotero-better-bibtex-7.0.35.xpi" (
    echo 文件存在！
    dir "E:\仓库\毕业论文\zotero-better-bibtex-7.0.35.xpi"
) else (
    echo 文件不存在
)
pause