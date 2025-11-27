// 通过Zotero debug-bridge导入PDF文件的脚本
const pdfPath = 'E:\\仓库\\毕业论文\\zotero\\知网文献\\人工智能赋能初中英语项目式学习策略探究_周颖.pdf';

// 创建新条目并导入PDF
async function importPDF() {
    try {
        // 导入PDF文件
        const item = await Zotero.Attachments.importFromFile({
            file: pdfPath,
            libraryID: Zotero.Libraries.userLibraryID
        });
        
        // 获取PDF元数据
        await item.recognizePDF();
        
        // 添加分类
        const collection = await getOrCreateCollection('教育学', '英语教学');
        item.addToCollection(collection.id);
        
        // 添加标签
        item.addTag('项目式学习');
        item.addTag('人工智能');
        item.addTag('初中英语');
        
        await item.saveTx();
        
        return 'PDF导入成功！';
    } catch (error) {
        return '导入失败: ' + error.message;
    }
}

// 获取或创建分类
async function getOrCreateCollection(parentName, childName) {
    let parentCollection = Zotero.Collections.getByLibrary(Zotero.Libraries.userLibraryID).find(c => c.name === parentName);
    
    if (!parentCollection) {
        parentCollection = new Zotero.Collection();
        parentCollection.name = parentName;
        parentCollection.libraryID = Zotero.Libraries.userLibraryID;
        await parentCollection.saveTx();
    }
    
    let childCollection = Zotero.Collections.getByLibrary(Zotero.Libraries.userLibraryID).find(c => c.name === childName && c.parentID === parentCollection.id);
    
    if (!childCollection) {
        childCollection = new Zotero.Collection();
        childCollection.name = childName;
        childCollection.parentID = parentCollection.id;
        childCollection.libraryID = Zotero.Libraries.userLibraryID;
        await childCollection.saveTx();
    }
    
    return childCollection;
}

importPDF().then(result => {
    return result;
}).catch(error => {
    return '错误: ' + error.message;
});