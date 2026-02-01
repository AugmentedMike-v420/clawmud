const http = require('http');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const PORT = 4400;
const LOGS_DIR = process.env.LOGS_DIR || '/agent/logs';

const html = `<!DOCTYPE html>
<html>
<head>
  <title>ClawMud Test Agent Logs</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { 
      background: #0d1117; 
      color: #c9d1d9; 
      font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
      font-size: 13px;
    }
    .header {
      background: #161b22;
      border-bottom: 1px solid #30363d;
      padding: 12px 20px;
      display: flex;
      align-items: center;
      gap: 16px;
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .header h1 { font-size: 16px; font-weight: 600; }
    .header select {
      background: #21262d;
      border: 1px solid #30363d;
      color: #c9d1d9;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 13px;
    }
    .status {
      margin-left: auto;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #3fb950;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.5; }
    }
    .controls { display: flex; gap: 8px; }
    .btn {
      background: #21262d;
      border: 1px solid #30363d;
      color: #c9d1d9;
      padding: 6px 12px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 12px;
    }
    .btn:hover { background: #30363d; }
    #logs {
      padding: 16px 20px;
      overflow-y: auto;
      height: calc(100vh - 60px);
    }
    .log-line {
      padding: 2px 0;
      border-bottom: 1px solid #21262d;
      display: flex;
      gap: 12px;
    }
    .log-line:hover { background: #161b22; }
    .timestamp { color: #8b949e; min-width: 90px; }
    .role { min-width: 80px; font-weight: 600; }
    .role.user { color: #58a6ff; }
    .role.assistant { color: #3fb950; }
    .role.system { color: #f0883e; }
    .role.tool { color: #a371f7; }
    .content { flex: 1; white-space: pre-wrap; word-break: break-word; }
    .raw { color: #8b949e; font-size: 11px; }
  </style>
</head>
<body>
  <div class="header">
    <h1>🐾 ClawMud Test Agent</h1>
    <select id="file-select"><option value="">Select log file...</option></select>
    <div class="controls">
      <button class="btn" onclick="toggleRaw()">Toggle Raw</button>
      <button class="btn" onclick="clearLogs()">Clear</button>
      <button class="btn" onclick="scrollBottom()">↓ Bottom</button>
    </div>
    <div class="status"><div class="dot"></div><span id="status">Connecting...</span></div>
  </div>
  <div id="logs"></div>
  <script>
    let evtSource = null;
    let showRaw = false;
    let autoScroll = true;
    
    const logsEl = document.getElementById('logs');
    const statusEl = document.getElementById('status');
    const fileSelect = document.getElementById('file-select');
    
    logsEl.addEventListener('scroll', () => {
      const atBottom = logsEl.scrollHeight - logsEl.scrollTop <= logsEl.clientHeight + 50;
      autoScroll = atBottom;
    });
    
    function scrollBottom() {
      logsEl.scrollTop = logsEl.scrollHeight;
      autoScroll = true;
    }
    
    function clearLogs() { logsEl.innerHTML = ''; }
    function toggleRaw() { 
      showRaw = !showRaw; 
      document.querySelectorAll('.raw').forEach(el => el.style.display = showRaw ? 'block' : 'none');
    }
    
    function formatLine(data) {
      try {
        const j = JSON.parse(data);
        const ts = j.ts ? new Date(j.ts).toLocaleTimeString() : '';
        const role = j.role || j.type || 'log';
        let content = j.content || j.message || j.text || JSON.stringify(j);
        if (typeof content === 'object') content = JSON.stringify(content, null, 2);
        
        return \`<div class="log-line">
          <span class="timestamp">\${ts}</span>
          <span class="role \${role}">\${role}</span>
          <span class="content">\${escapeHtml(content)}</span>
        </div>
        <div class="raw" style="display:\${showRaw ? 'block' : 'none'}">\${escapeHtml(data)}</div>\`;
      } catch {
        return \`<div class="log-line"><span class="content">\${escapeHtml(data)}</span></div>\`;
      }
    }
    
    function escapeHtml(s) {
      return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    }
    
    function connect(file) {
      if (evtSource) evtSource.close();
      if (!file) return;
      
      statusEl.textContent = 'Connecting...';
      evtSource = new EventSource('/stream?file=' + encodeURIComponent(file));
      
      evtSource.onopen = () => { statusEl.textContent = 'Streaming'; };
      evtSource.onmessage = (e) => {
        logsEl.innerHTML += formatLine(e.data);
        if (autoScroll) scrollBottom();
      };
      evtSource.onerror = () => { statusEl.textContent = 'Reconnecting...'; };
    }
    
    async function loadFiles() {
      const res = await fetch('/files');
      const files = await res.json();
      fileSelect.innerHTML = '<option value="">Select log file...</option>' + 
        files.map(f => \`<option value="\${f}">\${f}</option>\`).join('');
      if (files.length === 1) {
        fileSelect.value = files[0];
        connect(files[0]);
      }
    }
    
    fileSelect.onchange = () => connect(fileSelect.value);
    loadFiles();
    setInterval(loadFiles, 5000);
  </script>
</body>
</html>`;

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  
  if (url.pathname === '/') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(html);
    return;
  }
  
  if (url.pathname === '/files') {
    try {
      const files = fs.readdirSync(LOGS_DIR)
        .filter(f => f.endsWith('.jsonl'))
        .sort((a, b) => {
          const statA = fs.statSync(path.join(LOGS_DIR, a));
          const statB = fs.statSync(path.join(LOGS_DIR, b));
          return statB.mtime - statA.mtime;
        });
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(files));
    } catch {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end('[]');
    }
    return;
  }
  
  if (url.pathname === '/stream') {
    const file = url.searchParams.get('file');
    if (!file || file.includes('..')) {
      res.writeHead(400);
      res.end('Bad request');
      return;
    }
    
    const filePath = path.join(LOGS_DIR, file);
    if (!fs.existsSync(filePath)) {
      res.writeHead(404);
      res.end('Not found');
      return;
    }
    
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*'
    });
    
    // Send existing content
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      content.split('\n').filter(Boolean).forEach(line => {
        res.write(`data: ${line}\n\n`);
      });
    } catch {}
    
    // Tail new content
    const tail = spawn('tail', ['-f', '-n', '0', filePath]);
    tail.stdout.on('data', (data) => {
      data.toString().split('\n').filter(Boolean).forEach(line => {
        res.write(`data: ${line}\n\n`);
      });
    });
    
    req.on('close', () => tail.kill());
    return;
  }
  
  res.writeHead(404);
  res.end('Not found');
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`🔍 Log viewer running at http://0.0.0.0:${PORT}`);
});
