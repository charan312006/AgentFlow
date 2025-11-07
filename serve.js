#!/usr/bin/env node
/**
 * Simple HTTP server for AgentFlow Gemini Adapter demo viewer
 * Serves the sandbox directory at http://127.0.0.1:5050
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 5050;
const HOST = '127.0.0.1';
const SANDBOX_DIR = path.join(__dirname, 'sandbox');

const MIME_TYPES = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.yaml': 'text/yaml',
  '.yml': 'text/yaml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
  let filePath = req.url === '/' ? '/viewer-standalone.html' : req.url;
  
  // Remove query string
  filePath = filePath.split('?')[0];
  
  // Sanitize path
  filePath = path.normalize(filePath).replace(/^(\.\.[\/\\])+/, '');
  filePath = path.join(SANDBOX_DIR, filePath);
  
  const extname = String(path.extname(filePath)).toLowerCase();
  const contentType = MIME_TYPES[extname] || 'application/octet-stream';
  
  fs.readFile(filePath, (error, content) => {
    if (error) {
      if (error.code === 'ENOENT') {
        res.writeHead(404, { 'Content-Type': 'text/html' });
        res.end('<h1>404 - File Not Found</h1>', 'utf-8');
      } else {
        res.writeHead(500);
        res.end(`Server Error: ${error.code}`, 'utf-8');
      }
    } else {
      res.writeHead(200, {
        'Content-Type': contentType,
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'no-cache'
      });
      res.end(content, 'utf-8');
    }
  });
});

server.listen(PORT, HOST, () => {
  console.log('╔═══════════════════════════════════════════════════════════╗');
  console.log('║  🚀 AgentFlow Gemini Adapter - Live Server               ║');
  console.log('╚═══════════════════════════════════════════════════════════╝');
  console.log('');
  console.log(`  📂 Serving: ${SANDBOX_DIR}`);
  console.log(`  🌐 URL:     http://${HOST}:${PORT}`);
  console.log('');
  console.log(`  ✨ Server is running! Open http://${HOST}:${PORT} in your browser`);
  console.log('  ⛔ Press Ctrl+C to stop the server');
  console.log('');
  console.log('─'.repeat(61));
});

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`\n❌ Port ${PORT} is already in use. Try a different port or stop the other server.\n`);
  } else {
    console.error(`\n❌ Server error: ${err.message}\n`);
  }
  process.exit(1);
});
