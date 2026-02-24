import json, sys
from common.mcp4h_build import base_payload, add_event

def main(path: str):
    src = json.load(open(path, "r", encoding="utf-8"))
    p = base_payload("industrial")
    add_event(p, eid="obs:sensor", kind="observation", etype="industrial.sensor.observed",
              data={"modality":"telemetry","value":src["value"],"unit":src.get("unit","")})
    add_event(p, eid="der:state", kind="derivation", etype="industrial.state.derived",
              refs=["obs:sensor"], method="system",
              data={"name":"temp_c","value":src["value"],"unit":"C"})
    add_event(p, eid="clm:fault", kind="claim", etype="industrial.fault.hypothesis",
              refs=["der:state"], method="heuristic", confidence=0.05,
              data={"statement":"No fault suspected at current temperature"})
    add_event(p, eid="cue:maint", kind="cue", etype="industrial.maintenance.cue",
              refs=["clm:fault"], data={"channel":"system","intent":"noop","urgency":"low","payload":{"action":"none"}})
    p["extensions"]["industrial"]["opcua"]={"nodeId":src.get("nodeId")}
    print(json.dumps(p, indent=2))
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python convert.py <input.json>")
    main(sys.argv[1])
