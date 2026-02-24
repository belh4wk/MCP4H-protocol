import json, sys
from common.mcp4h_build import base_payload, add_event

def main(path: str):
    src = json.load(open(path, "r", encoding="utf-8"))
    p = base_payload("incident")
    ts = src.get("ts")
    add_event(p, eid="obs:alert", kind="observation", etype="incident.alert.received", ts=ts,
              data={"modality":"event","value":src})
    add_event(p, eid="der:sev", kind="derivation", etype="incident.signal.enriched", ts=ts,
              refs=["obs:alert"], method="system",
              data={"name":"severity_norm","value":src.get("severity","unknown"), "unit":"enum"})
    add_event(p, eid="clm:rca", kind="claim", etype="incident.hypothesis.raised", ts=ts,
              refs=["der:sev"], method="heuristic", confidence=0.55,
              alternates=[{"id":"alt:cache","statement":"Cache eviction storm","refs":["der:sev"],"confidence":0.25,"method":"heuristic"}],
              data={"statement":"Likely recent deploy correlated with latency spike"})
    add_event(p, eid="cue:page", kind="cue", etype="incident.followup.task", ts=ts,
              refs=["clm:rca"], data={"channel":"system","intent":"page","urgency":"high","payload":{"target":"oncall","task":"investigate"}})
    print(json.dumps(p, indent=2))
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python convert.py <input.json>")
    main(sys.argv[1])
