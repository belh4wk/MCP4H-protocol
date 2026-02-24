import json, sys
import os
# Ensure shared bridge helpers are importable (bridges/common)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from common.mcp4h_build import base_payload, add_event

def main(path: str):
    src = json.load(open(path, "r", encoding="utf-8"))
    p = base_payload("health")
    val = src.get("valueQuantity", {}).get("value")
    unit = src.get("valueQuantity", {}).get("unit")
    add_event(p, eid="obs:fhir", kind="observation", etype="health.observation.recorded",
              data={"modality":"document","value":src, "note":"FHIR Observation"})
    add_event(p, eid="der:vital", kind="derivation", etype="health.vital.observed",
              refs=["obs:fhir"], method="system", data={"name":"heart_rate","value":val,"unit":unit})
    add_event(p, eid="clm:risk", kind="claim", etype="health.risk.hypothesis",
              refs=["der:vital"], method="heuristic", confidence=0.1,
              data={"statement":"No elevated risk detected from this single observation"})
    add_event(p, eid="cue:monitor", kind="cue", etype="health.cue.monitor",
              refs=["clm:risk"], data={"channel":"text","intent":"monitor","urgency":"low","payload":{"text":"Continue monitoring"}})
    p["extensions"]["health"]["fhir"] = {"resourceType":src.get("resourceType"), "id":src.get("id")}
    print(json.dumps(p, indent=2))
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python convert.py <input.json>")
    main(sys.argv[1])
