
/**
 * MCP JavaScript SDK - v0.1.0
 * Provides message encoding/decoding and WebSocket client stubs.
 */

const WebSocket = require('ws');

class MCPClient {
  constructor(url) {
    this.url = url;
    this.ws = null;
  }

  connect() {
    this.ws = new WebSocket(this.url);
    this.ws.on('open', () => console.log('[MCP] Connected'));
    this.ws.on('message', (msg) => this.handleMessage(msg));
    this.ws.on('close', () => console.log('[MCP] Disconnected'));
  }

  sendMessage(message) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      console.error('[MCP] Cannot send, WebSocket not open');
      return;
    }
    const payload = JSON.stringify(message);
    this.ws.send(payload);
  }

  handleMessage(raw) {
    try {
      const msg = JSON.parse(raw);
      console.log('[MCP] Received:', msg);
    } catch (err) {
      console.error('[MCP] Failed to parse message', err);
    }
  }
}

function buildMessage({ sessionId, senderId, text, emoji, haptic }) {
  return {
    mcp_version: "1.0",
    session_id: sessionId,
    message_id: "msg_" + Math.random().toString(36).substr(2, 6),
    timestamp: new Date().toISOString(),
    sender_id: senderId,
    priority: "balanced",
    modalities: {
      text: { lang: "en", content: text },
      visual: { emoji: emoji ? [emoji] : [] },
      haptic: haptic ? { pattern: haptic, intensity: 0.5, duration_ms: 200 } : null
    },
    signals: { conflict: false, sensitive: false }
  };
}

module.exports = { MCPClient, buildMessage };
