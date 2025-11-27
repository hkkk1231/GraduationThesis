@echo off
chcp 65001 >nul
echo === Zotfile Plugin Installation Script ===
echo.

echo 1. Checking Zotero installation...
if exist "C:\Program Files\Zotero\zotero.exe" (
    echo Zotero found at C:\Program Files\Zotero\
) else if exist "C:\Program Files (x86)\Zotero\zotero.exe" (
    echo Zotero found at C:\Program Files (x86)\Zotero\
) else (
    echo Zotero not found. Please install Zotero first: https://www.zotero.org/download/
    pause
    exit /b 1
)

echo.
echo 2. Downloading Zotfile plugin...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/jlegewie/zotfile/releases/latest/download/zotfile-5.1.3.xpi' -OutFile 'zotfile.xpi'"

if exist "zotfile.xpi" (
    echo Zotfile plugin downloaded successfully
) else (
    echo Failed to download Zotfile plugin
    pause
    exit /b 1
)

echo.
echo 3. Installing Zotfile plugin...
echo Please follow these steps in Zotero:
echo 1. Open Zotero
echo 2. Go to Tools - Add-ons
echo 3. Click gear icon - Install Add-on From File
echo 4. Select zotfile.xpi from current directory
echo 5. Restart Zotero
echo.

echo 4. Configuring Zotfile...
echo After installation, please configure these settings:
echo 1. Go to Tools - Zotfile Preferences
echo 2. General Settings:
echo    - Source Folder for Attaching New Files: Set to your Downloads folder
echo    - Location of Files: Set to %USERPROFILE%\Zotero\storage
echo 3. Tablet Settings:
echo    - Send to Tablet: Enable
echo    - Folder for Tablet: Set to E:\仓库\毕业论文\obsidian\AI笔记\PDF阅读
echo 4. Renaming Rules:
echo    - Enable auto-rename
echo    - Format: {%a_}{%y_}{%t}
echo.

echo 5. Creating Obsidian PDF reading directory...
if not exist "E:\仓库\毕业论文\obsidian\AI笔记\PDF阅读" mkdir "E:\仓库\毕业论文\obsidian\AI笔记\PDF阅读"
echo PDF reading directory created

echo.
echo === Installation Complete ===
echo Please complete the configuration in Zotero as described above
pause