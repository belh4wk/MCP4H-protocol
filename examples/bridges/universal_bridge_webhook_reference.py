import json
# A Bridge for the rest of us: Translating Webhooks to Sensation
def process_webhook_to_mcp4h(provider, data):
    """
    Example: Bridge a GitHub 'Build Failed' alert.
    """
    is_critical = data.get('status') == 'failure'
    
    return {
        "bridge_id": f"{provider}-bridge-v1",
        "haptic": {
            "intensity": 1.0 if is_critical else 0.2,
            "pattern": "double_thump" if is_critical else "soft_pulse"
        },
        "audio": {
            "tone": "major_chord" if is_critical else "none"
        },
        "text": f"SYSTEM ALERT: {data.get('repo_name')} {data.get('status')}"
    }

# usage: bridge_to_mcp4h("GitHub", {"status": "failure", "repo_name": "MCP4H-Core"})