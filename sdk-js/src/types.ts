
export type LanguageTag = string; // BCP-47

export interface MCPText {
  lang: LanguageTag;
  content: string;
  translation?: Array<{ target: LanguageTag; content: string; confidence?: number }>;
  tone?: { label: string; confidence?: number };
}

export interface MCPAudio {
  stream_id?: string;
  codec?: string; // e.g., opus48
  prosody?: { pitch?: 'low'|'med'|'high'; pace?: 'slow'|'med'|'fast'; energy?: 'low'|'med'|'high' };
  tone?: { label: string; confidence?: number };
}

export interface MCPVisual {
  emoji?: string[];
  stickers?: string[];
  gif?: string;
  overlays?: Array<{ type: 'gloss'|'note'|'sketch'; text?: string; lang?: LanguageTag }>;
}

export interface MCPHaptic {
  pattern: string; // registry code, e.g., HB_SLOW
  intensity?: number; // 0..1
  duration_ms?: number;
}

export interface MCPModalities {
  text?: MCPText;
  audio?: MCPAudio;
  visual?: MCPVisual;
  haptic?: MCPHaptic;
}

export interface MCPMessage {
  mcp_version: string;
  session_id: string;
  message_id: string;
  timestamp: string; // ISO 8601
  sender_id: string;
  priority?: 'balanced'|'accessibility_text_first'|'low_bandwidth_visual_haptic'|'tone_sensitive_audio_first';
  context?: string;
  modalities: MCPModalities;
  signals?: { conflict?: boolean; sensitive?: boolean };
  integrity?: { sig?: string; alg?: string };
}
