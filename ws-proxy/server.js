/**
 * ClawMUD WebSocket-to-Telnet Proxy
 * 
 * Bridges browser WebSocket connections to the MUD's telnet port.
 * Each WebSocket client gets their own TCP connection to the MUD.
 */

const WebSocket = require('ws');
const net = require('net');

// Configuration
const WS_PORT = process.env.PORT || 8080;
const MUD_HOST = process.env.MUD_HOST || 'localhost';
const MUD_PORT = process.env.MUD_PORT || 4000;

// Create WebSocket server
const wss = new WebSocket.Server({ 
  port: WS_PORT,
  // Handle CORS for browser clients
  verifyClient: (info, callback) => {
    // Allow all origins (you might want to restrict this in production)
    callback(true);
  }
});

console.log(`🌐 ClawMUD WebSocket Proxy`);
console.log(`   WebSocket: ws://0.0.0.0:${WS_PORT}`);
console.log(`   MUD Target: ${MUD_HOST}:${MUD_PORT}`);
console.log(`   Waiting for connections...`);

// Track connections for stats
let connectionCount = 0;
let activeConnections = 0;

wss.on('connection', (ws, req) => {
  connectionCount++;
  activeConnections++;
  
  const clientId = connectionCount;
  const clientIP = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
  
  console.log(`[${clientId}] New connection from ${clientIP} (${activeConnections} active)`);
  
  // Create TCP connection to MUD
  const mudSocket = net.createConnection({
    host: MUD_HOST,
    port: MUD_PORT
  });

  let mudConnected = false;

  // MUD socket events
  mudSocket.on('connect', () => {
    mudConnected = true;
    console.log(`[${clientId}] Connected to MUD`);
  });

  mudSocket.on('data', (data) => {
    // Send MUD output to browser
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'output',
        data: data.toString('binary')  // Preserve ANSI codes
      }));
    }
  });

  mudSocket.on('error', (err) => {
    console.error(`[${clientId}] MUD socket error:`, err.message);
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'error',
        message: 'Connection to MUD failed'
      }));
      ws.close();
    }
  });

  mudSocket.on('close', () => {
    console.log(`[${clientId}] MUD connection closed`);
    mudConnected = false;
    if (ws.readyState === WebSocket.OPEN) {
      ws.close();
    }
  });

  // WebSocket events
  ws.on('message', (message) => {
    try {
      const msg = JSON.parse(message);
      
      switch (msg.type) {
        case 'input':
          // Send user input to MUD
          if (mudConnected) {
            mudSocket.write(msg.data);
          }
          break;
          
        case 'resize':
          // Could implement NAWS (Negotiate About Window Size) here
          // For now, just log it
          console.log(`[${clientId}] Terminal resize: ${msg.cols}x${msg.rows}`);
          break;
          
        default:
          console.log(`[${clientId}] Unknown message type: ${msg.type}`);
      }
    } catch (e) {
      console.error(`[${clientId}] Invalid message:`, e.message);
    }
  });

  ws.on('close', () => {
    activeConnections--;
    console.log(`[${clientId}] WebSocket closed (${activeConnections} active)`);
    mudSocket.destroy();
  });

  ws.on('error', (err) => {
    console.error(`[${clientId}] WebSocket error:`, err.message);
    mudSocket.destroy();
  });
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('Received SIGTERM, shutting down...');
  wss.close(() => {
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('Received SIGINT, shutting down...');
  wss.close(() => {
    process.exit(0);
  });
});
