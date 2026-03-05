import json
import os
from bridges.universal_webhook_bridge import universal_bridge_webhook_reference
from arbiters.reference_arbiter import arbiter_logic_reference

# --- HELPER ---
def load_example_envelope(filename):
    data_path = os.path.join("messages", "templates", filename)
    with open(data_path, "r") as file:
        return json.load(file)
        
# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("--- MCP4H v0.1.5 Protocol Test ---")
    
    # 1. Test JSON Loading
    example_data = load_example_envelope("mcp4h_minimal_example.json")
    print(f"Loaded JSON Envelope: {example_data}")
    
    # 2. Simulate raw input
    raw_data = {"status": "CRITICAL", "msg": "Production Server Down!"}
    print(f"1. Raw Input: {raw_data}")

    # 3. Use the IMPORTED functions
    bridge_packet = universal_bridge_webhook_reference("Jira", raw_data)
    print(f"2. Bridge Result: {json.dumps(bridge_packet, indent=2)}")

    # 4. Use the IMPORTED Arbiter
    final_sensory_output = arbiter_logic_reference(bridge_packet)
    print(f"3. Final MCP4H Output: {json.dumps(final_sensory_output, indent=2)}")
    
    print("\n[Result: Sensory hardware would now trigger a High-Intensity Haptic pulse.]")