const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

// MCP服务器管理
class MCPServerManager {
  constructor() {
    this.servers = new Map();
    this.config = require('./mcp_config.json');
  }

  async startServer(name, config) {
    if (this.servers.has(name)) {
      console.log(`服务器 ${name} 已在运行`);
      return;
    }

    const server = spawn(config.command, config.args, {
      env: { ...process.env, ...config.env },
      stdio: ['pipe', 'pipe', 'pipe']
    });

    server.on('error', (error) => {
      console.error(`服务器 ${name} 启动失败:`, error);
    });

    server.on('close', (code) => {
      console.log(`服务器 ${name} 退出，代码: ${code}`);
      this.servers.delete(name);
    });

    server.stdout.on('data', (data) => {
      console.log(`[${name}] ${data.toString()}`);
    });

    server.stderr.on('data', (data) => {
      console.error(`[${name}] ${data.toString()}`);
    });

    this.servers.set(name, server);
    console.log(`服务器 ${name} 启动成功`);
  }

  async stopServer(name) {
    const server = this.servers.get(name);
    if (server) {
      server.kill();
      this.servers.delete(name);
      console.log(`服务器 ${name} 已停止`);
    }
  }

  async startAll() {
    for (const [name, config] of Object.entries(this.config.mcpServers)) {
      await this.startServer(name, config);
    }
  }

  async stopAll() {
    for (const name of this.servers.keys()) {
      await this.stopServer(name);
    }
  }

  getStatus() {
    return Array.from(this.servers.keys());
  }
}

const manager = new MCPServerManager();

// API路由
app.get('/api/servers', (req, res) => {
  res.json({
    running: manager.getStatus(),
    configured: Object.keys(manager.config.mcpServers)
  });
});

app.post('/api/servers/:name/start', async (req, res) => {
  const name = req.params.name;
  const config = manager.config.mcpServers[name];
  
  if (!config) {
    return res.status(404).json({ error: '服务器配置未找到' });
  }

  try {
    await manager.startServer(name, config);
    res.json({ message: `服务器 ${name} 启动成功` });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/servers/:name/stop', async (req, res) => {
  try {
    await manager.stopServer(req.params.name);
    res.json({ message: `服务器 ${req.params.name} 已停止` });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/servers/start-all', async (req, res) => {
  try {
    await manager.startAll();
    res.json({ message: '所有服务器启动成功' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/servers/stop-all', async (req, res) => {
  try {
    await manager.stopAll();
    res.json({ message: '所有服务器已停止' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// 启动HTTP服务器
app.listen(PORT, () => {
  console.log(`MCP服务器管理器运行在 http://localhost:${PORT}`);
  
  // 自动启动所有MCP服务器
  setTimeout(() => {
    manager.startAll().catch(console.error);
  }, 1000);
});

// 优雅关闭
process.on('SIGINT', async () => {
  console.log('正在关闭所有服务器...');
  await manager.stopAll();
  process.exit(0);
});