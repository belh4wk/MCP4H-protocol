import json

# --- THE BRIDGE (Normalization Layer) ---
def universal_bridge(source, raw_input):
    """
    Translates any incoming raw data into an MCP4H-compatible packet.
    """
    is_emergency = raw_input.get('status') == 'CRITICAL'
    
    return {
        "bridge_id": f"bridge-{source}",
        "intensity_map": 1.0 if is_emergency else 0.3,
        "payload": {
            "summary": raw_input.get('msg', 'New Signal'),
            "metadata": {"category": "emergency" if is_emergency else "info"}
        }
    }

# --- THE ARBITER (Intelligence Layer) ---
def arbiter_evaluate(candidate_packet):
    """
    The AI-governed gatekeeper: Deciding if/how the human should feel the data.
    """
    intensity = candidate_packet['intensity_map']
    
    # Logic: Only allow 'Haptic' feedback if intensity is high
    if intensity >= 0.8:
        return {
            "action": "DELIVER_SENSORY",
            "channels": ["haptic", "audio", "visual"],
            "intensity": intensity
        }
    
    return {"action": "LOG_ONLY", "channels": ["visual"]}

# --- THE PROTOCOL EXECUTION (The Run) ---
if __name__ == "__main__":
    print("--- MCP4H v0.1.5 Protocol Test ---")
    
    # Simulate a raw Jira 'CRITICAL' alert
    raw_data = {"status": "CRITICAL", "msg": "Production Server Down!"}
    print(f"1. Raw Input: {raw_data}")

    # Step 1: Bridge it
    bridge_packet = universal_bridge("Jira", raw_data)
    print(f"2. Bridge Result: {json.dumps(bridge_packet, indent=2)}")

    # Step 2: Arbitrate it
    final_sensory_output = arbiter_evaluate(bridge_packet)
    print(f"3. Final MCP4H Output: {json.dumps(final_sensory_output, indent=2)}")
    
    print("\n[Result: Sensory hardware would now trigger a High-Intensity Haptic pulse.]")