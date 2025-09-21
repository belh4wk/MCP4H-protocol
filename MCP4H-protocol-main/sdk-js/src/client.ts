
import WebSocket from 'isomorphic-ws'
import { encodeMessage, decodeMessage } from './encoder.js'
import { MCPMessage } from './types.js'

export interface MCPClientOptions {
  url: string
  token?: string
  onMessage?: (msg: MCPMessage) => void
  onOpen?: () => void
  onClose?: (code?: number, reason?: string) => void
  onError?: (err: any) => void
}

export class MCPClient {
  private ws?: WebSocket
  private opts: MCPClientOptions

  constructor(opts: MCPClientOptions) {
    this.opts = opts
  }

  connect() {
    this.ws = new WebSocket(this.opts.url, {
      headers: this.opts.token ? { Authorization: `Bearer ${this.opts.token}` } : undefined
    } as any)

    this.ws.onopen = () => this.opts.onOpen?.()
    this.ws.onclose = (ev) => this.opts.onClose?.(ev.code as any, (ev as any).reason)
    this.ws.onerror = (err) => this.opts.onError?.(err)
    this.ws.onmessage = (ev) => {
      try {
        const msg = decodeMessage(ev.data.toString())
        this.opts.onMessage?.(msg)
      } catch (e) {
        this.opts.onError?.(e)
      }
    }
  }

  send(msg: MCPMessage) {
    if (!this.ws || this.ws.readyState !== this.ws.OPEN) throw new Error('WebSocket not open')
    this.ws.send(encodeMessage(msg))
  }

  close() {
    this.ws?.close()
  }
}
