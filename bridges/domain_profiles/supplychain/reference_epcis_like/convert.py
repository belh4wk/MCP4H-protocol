import json, sys
import os
# Ensure shared bridge helpers are importable (bridges/common)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from common.mcp4h_build import base_payload, add_event

def main(path: str):
    src = json.load(open(path, "r", encoding="utf-8"))
    p = base_payload("supplychain")
    ts = src.get("eventTime")
    add_event(p, eid="obs:epcis", kind="observation", etype="supplychain.event.observed", ts=ts,
              data={"modality":"event","value":src})
    add_event(p, eid="der:cond", kind="derivation", etype="supplychain.condition.derived", ts=ts,
              refs=["obs:epcis"], method="system", data={"name":"bizStep","value":src.get("bizStep"),"unit":"enum"})
    add_event(p, eid="clm:ok", kind="claim", etype="supplychain.compliance.claim", ts=ts,
              refs=["der:cond"], method="heuristic", confidence=0.6,
              data={"statement":"No compliance issues inferred from event alone"})
    add_event(p, eid="cue:release", kind="cue", etype="supplychain.cue.release", ts=ts,
              refs=["clm:ok"], data={"channel":"system","intent":"release","urgency":"normal","payload":{"action":"release"}})
    print(json.dumps(p, indent=2))
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python convert.py <input.json>")
    main(sys.argv[1])
