const https = require('https');

const apiKey = 'CIApUKos6l9E0GOaCBrILRrt';
const libraryId = '18982351';

function getZoteroItems() {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'api.zotero.org',
            path: `/users/${libraryId}/items?format=json&limit=100&include=data,bib`,
            method: 'GET',
            headers: {
                'Zotero-API-Key': apiKey
            }
        };

        const req = https.request(options, (res) => {
            console.log(`状态码: ${res.statusCode}`);
            
            let data = '';
            res.on('data', (chunk) => {
                data += chunk;
            });
            
            res.on('end', () => {
                try {
                    const items = JSON.parse(data);
                    console.log(`获取到 ${items.length} 个文献条目`);
                    resolve(items);
                } catch (e) {
                    console.error('解析错误:', e);
                    console.log('响应数据:', data);
                    reject(e);
                }
            });
        });

        req.on('error', (e) => {
            console.error('请求错误:', e);
            reject(e);
        });

        req.end();
    });
}

async function main() {
    console.log('开始获取Zotero文献信息...');
    try {
        const items = await getZoteroItems();
        console.log(`成功获取 ${items.length} 个文献条目`);
        
        // 处理文献信息
        const processedItems = items.map(item => {
            const data = item.data || {};
            return {
                key: data.key,
                title: data.title,
                creators: data.creators || [],
                date: data.date,
                abstractNote: data.abstractNote,
                publicationTitle: data.publicationTitle,
                itemType: data.itemType,
                tags: data.tags || [],
                notes: item.notes || []
            };
        });

        // 过滤出没有笔记的文献
        const itemsWithoutNotes = processedItems.filter(item => 
            item.notes.length === 0 && item.itemType !== 'note'
        );

        console.log('\n=== 文献统计 ===');
        console.log(`总文献数: ${processedItems.length}`);
        console.log(`有笔记的文献数: ${processedItems.filter(item => item.notes.length > 0).length}`);
        console.log(`没有笔记的文献数: ${itemsWithoutNotes.length}`);

        console.log('\n=== 没有笔记的文献列表 ===');
        itemsWithoutNotes.forEach((item, index) => {
            console.log(`\n${index + 1}. ${item.title}`);
            console.log(`   作者: ${item.creators.map(c => `${c.lastName} ${c.firstName}`).join(', ')}`);
            console.log(`   年份: ${item.date || '未知'}`);
            console.log(`   期刊: ${item.publicationTitle || '未知'}`);
            console.log(`   摘要: ${item.abstractNote ? item.abstractNote.substring(0, 100) + '...' : '无'}`);
            console.log(`   Key: ${item.key}`);
        });

        // 保存到文件
        const fs = require('fs');
        const outputPath = 'E:\\仓库\\毕业论文\\zotero_items.json';
        const outputPath2 = 'E:\\仓库\\毕业论文\\zotero_items_without_notes.json';
        
        fs.writeFileSync(outputPath, JSON.stringify(processedItems, null, 2));
        fs.writeFileSync(outputPath2, JSON.stringify(itemsWithoutNotes, null, 2));
        
        console.log(`\n数据已保存到 ${outputPath} 和 ${outputPath2}`);

    } catch (error) {
        console.error('错误:', error);
        console.error('错误堆栈:', error.stack);
    }
}

main();