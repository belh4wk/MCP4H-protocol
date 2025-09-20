
import { MCPMessage } from './types.js'

export function encodeMessage(msg: MCPMessage): string {
  // Future: support CBOR/Protobuf via feature negotiation.
  return JSON.stringify(msg)
}

export function decodeMessage(raw: string): MCPMessage {
  return JSON.parse(raw) as MCPMessage
}
