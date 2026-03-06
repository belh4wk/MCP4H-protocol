
// Simple MCP Echo Server (TypeScript/Node)
// Run with: ts-node echo-server.ts (after npm install ws ts-node typescript)

import WebSocket, { WebSocketServer } from 'ws'

const wss = new WebSocketServer({ port: 8080 })

wss.on('connection', (ws) => {
  console.log('Client connected')

  ws.on('message', (data) => {
    console.log('Received:', data.toString())

    // Echo back the same payload
    ws.send(data.toString())
  })

  ws.on('close', () => console.log('Client disconnected'))
})

console.log('MCP Echo Server running on ws://localhost:8080')
