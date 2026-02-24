import json, sys
import os
# Ensure shared bridge helpers are importable (bridges/common)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from common.mcp4h_build import base_payload, add_event

def main(path: str):
    src = json.load(open(path, "r", encoding="utf-8"))
    p = base_payload("observability")
    add_event(p, eid="obs:log", kind="observation", etype="observability.log.observed",
              data={"modality":"text","value":src.get("body"),"note":src.get("severityText","")})
    add_event(p, eid="der:svc", kind="derivation", etype="observability.span.derived",
              refs=["obs:log"], method="system", data={"name":"service","value":src.get("attributes",{}).get("service.name","unknown"),"unit":"string"})
    add_event(p, eid="clm:an", kind="claim", etype="observability.anomaly.detected",
              refs=["der:svc"], method="heuristic", confidence=0.7,
              data={"statement":"Elevated timeout rate suspected"})
    add_event(p, eid="cue:page", kind="cue", etype="observability.cue.page",
              refs=["clm:an"], data={"channel":"system","intent":"page","urgency":"high","payload":{"target":"oncall"}})
    p["extensions"]["observability"]["otel"] = {"severityText":src.get("severityText"),"attributes":src.get("attributes",{})}
    print(json.dumps(p, indent=2))
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python convert.py <input.json>")
    main(sys.argv[1])
