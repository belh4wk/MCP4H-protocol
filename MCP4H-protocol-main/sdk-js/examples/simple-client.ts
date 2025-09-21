
import { MCPClient, MCPMessage } from '../src/index.js'

const client = new MCPClient({
  url: process.env.MCP_WS_URL || 'ws://localhost:8080',
  onOpen: () => {
    console.log('Connected. Sending demo message...')

    const msg: MCPMessage = {
      mcp_version: '1.0',
      session_id: 'sess_demo1',
      message_id: 'msg_' + Math.random().toString(36).slice(2),
      timestamp: new Date().toISOString(),
      sender_id: 'user_demo',
      priority: 'balanced',
      modalities: {
        text: { lang: 'en', content: 'Hello!', translation: [{ target: 'fr', content: 'Salut!', confidence: 0.95 }] },
        visual: { emoji: ['👋'] },
        haptic: { pattern: 'PULSE_S', intensity: 0.8, duration_ms: 120 }
      },
      signals: { conflict: false, sensitive: false }
    }

    client.send(msg)
  },
  onMessage: (m) => console.log('Received:', m),
  onError: (e) => console.error('WS error:', e),
  onClose: () => console.log('Closed')
})

client.connect()
