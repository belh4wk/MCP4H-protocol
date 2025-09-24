from mapper import mcp4h_to_prompt, prompt_to_mcp4h_response

def test_roundtrip_minimal():
    pkt = {
        "mcp4h_version": "0.1.1",
        "profile": "harmonizer",
        "id": "t-1",
        "timestamp": "2025-09-24T00:00:00Z",
        "signal": {"role": "user", "type": "text", "content": "hello"},
        "context": {"foo": "bar"}
    }
    prompt, meta = mcp4h_to_prompt(pkt)
    assert "MCP4H 0.1.1" in prompt
    resp = prompt_to_mcp4h_response("ok", meta)
    assert resp["signal"]["content"] == "ok"
    assert resp["correlation_id"] == "t-1"
