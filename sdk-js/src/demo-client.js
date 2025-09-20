
/**
 * Demo client using MCP SDK
 * Run: `npm install && npm start`
 */

const { MCPClient, buildMessage } = require('./index');

// Example: local echo server (replace with real MCP relay later)
const client = new MCPClient('ws://localhost:8080');

client.connect();

setTimeout(() => {
  const msg = buildMessage({
    sessionId: 'sess_demo1',
    senderId: 'user_demo',
    text: 'Hello from MCP SDK!',
    emoji: '👋',
    haptic: 'PULSE_S'
  });
  client.sendMessage(msg);
}, 2000);
