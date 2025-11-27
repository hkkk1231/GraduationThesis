// 脚本：将PDF文件导入到Zotero
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const pdfPath = 'E:\\仓库\\毕业论文\\zotero\\知网文献\\人工智能赋能初中英语项目式学习策略探究_周颖.pdf';
const zoteroPath = 'D:\\工具\\zotero\\zotero.exe';

// 检查文件是否存在
if (fs.existsSync(pdfPath)) {
    console.log('PDF文件存在，准备导入到Zotero...');
    
    // 使用Zotero命令行导入
    exec(`"${zoteroPath}" -ZoteroAttach "${pdfPath}"`, (error, stdout, stderr) => {
        if (error) {
            console.error('导入失败:', error);
            return;
        }
        console.log('导入成功！');
    });
} else {
    console.log('PDF文件不存在');
}