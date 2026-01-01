// Plain Node.js HTTP server test - bypassing NestJS entirely
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ status: 'ok', message: 'Plain Node.js server works!' }));
});

server.listen(4000, '0.0.0.0', () => {
  console.log('✅ Plain Node.js server listening on port 4000');
  console.log('Test: http://localhost:4000');
});

server.on('error', (err) => {
  console.error('❌ Server error:', err);
  process.exit(1);
});
