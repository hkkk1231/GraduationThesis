const https = require('https');

const apiKey = 'CIApUKos6l9E0GOaCBrILRrt';
const userId = '18982351';

console.log('测试Zotero API连接...');

// 测试获取用户文献库
const options = {
  hostname: 'api.zotero.org',
  path: `/users/${userId}/items?limit=5`,
  method: 'GET',
  headers: {
    'Zotero-API-Key': apiKey
  }
};

const req = https.request(options, (res) => {
  console.log(`状态码: ${res.statusCode}`);
  console.log(`响应头: ${JSON.stringify(res.headers)}`);
  
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    try {
      const items = JSON.parse(data);
      console.log(`找到 ${items.length} 个文献项`);
      if (items.length > 0) {
        console.log('第一个文献项:', JSON.stringify(items[0], null, 2));
      }
      console.log('✅ Zotero API连接成功！');
    } catch (e) {
      console.log('响应数据:', data);
      console.log('❌ 解析响应失败');
    }
  });
});

req.on('error', (e) => {
  console.error('❌ 请求错误:', e);
});

req.end();