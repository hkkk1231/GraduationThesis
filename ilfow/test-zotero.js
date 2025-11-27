const https = require('https');

const apiKey = 'CIApUKos6l9E0GOaCBrILRrt';

const options = {
  hostname: 'api.zotero.org',
  path: '/keys/current',
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
      const user = JSON.parse(data);
      console.log('用户信息:', user);
      if (user.id) {
        console.log(`用户ID: ${user.id}`);
        console.log('请将以下配置添加到mcp_config.json中:');
        console.log(`"ZOTERO_LIBRARY_ID": "${user.id}",`);
      }
    } catch (e) {
      console.log('响应数据:', data);
    }
  });
});

req.on('error', (e) => {
  console.error('请求错误:', e);
});

req.end();