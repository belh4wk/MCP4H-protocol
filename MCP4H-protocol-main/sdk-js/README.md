
# MCP JavaScript SDK

Reference SDK for the Multimodal Communication Protocol (MCP).

## Quick Start
```bash
cd sdk-js
npm install
npm run build
# Run the example (needs a WebSocket endpoint that echoes messages)
export MCP_WS_URL=ws://localhost:8080
node --loader ts-node/esm examples/simple-client.ts
```

## What It Does
- Defines TypeScript types for MCP messages
- Provides JSON encoder/decoder stubs
- Minimal WebSocket client for real-time messaging

## Roadmap
- QUIC/HTTP3 transport
- CBOR/Protobuf encoding
- Capability negotiation + profiles
- Tone/translation adapters
- Haptics helper utilities
