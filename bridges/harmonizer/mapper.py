from __future__ import annotations
import uuid
from typing import Dict, Tuple, Any

DEFAULT_VERSION = "0.1.1"
DEFAULT_PROFILE = "harmonizer"
DEFAULT_SOURCE = {"agent": "bridges/harmonizer", "version": "0.0.1"}

def _now_iso() -> str:
    import datetime as _dt
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def mcp4h_to_prompt(packet: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    version = packet.get("mcp4h_version", DEFAULT_VERSION)
    profile = packet.get("profile", DEFAULT_PROFILE)
    pkt_id = packet.get("id", str(uuid.uuid4()))
    ts = packet.get("timestamp", _now_iso())
    context = packet.get("context", {})
    signal = packet.get("signal", {})
    role = signal.get("role", "user")
    stype = signal.get("type", "text")
    content = signal.get("content", "")

    header = f"[MCP4H {version} | profile={profile} | role={role} | type={stype} | id={pkt_id}]"
    ctx_lines = []
    if isinstance(context, dict) and context:
        for k, v in context.items():
            ctx_lines.append(f"{k}: {v}")
    ctx_block = "\\n".join(ctx_lines)

    if ctx_block:
        prompt = f"{header}\\n<context>\\n{ctx_block}\\n</context>\\n\\n{content}"
    else:
        prompt = f"{header}\\n\\n{content}"

    meta = {
        "mcp4h_version": version,
        "profile": profile,
        "id": pkt_id,
        "timestamp": ts,
        "context": context,
        "source": packet.get("source"),
        "constraints_detected": packet.get("constraints_detected", []),
        "original_role": role,
        "original_type": stype,
    }
    return prompt, meta

def prompt_to_mcp4h_response(gpt_text: str, meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "mcp4h_version": meta.get("mcp4h_version", DEFAULT_VERSION),
        "profile": meta.get("profile", DEFAULT_PROFILE),
        "id": str(uuid.uuid4()),
        "correlation_id": meta.get("id"),
        "timestamp": _now_iso(),
        "source": DEFAULT_SOURCE,
        "context": meta.get("context", {}),
        "signal": {
            "role": "assistant",
            "type": "text",
            "content": gpt_text
        },
        "constraints_detected": meta.get("constraints_detected", []),
        "meta": {
            "original_role": meta.get("original_role"),
            "original_type": meta.get("original_type")
        }
    }
