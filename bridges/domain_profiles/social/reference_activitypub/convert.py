import json, sys
import os
# Ensure shared bridge helpers are importable (bridges/common)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from common.mcp4h_build import base_payload, add_event

def main(path: str):
    src = json.load(open(path, "r", encoding="utf-8"))
    p = base_payload("social")
    add_event(p, eid="obs:post", kind="observation", etype="social.post.created",
              data={"modality":"text","value":src.get("object",{}).get("content","")})
    add_event(p, eid="der:ctx", kind="derivation", etype="social.context.added",
              refs=["obs:post"], method="system", data={"name":"actor","value":src.get("actor"),"unit":"uri"})
    add_event(p, eid="clm:misinfo", kind="claim", etype="social.claim.contested",
              refs=["der:ctx"], method="heuristic", confidence=0.05,
              data={"statement":"No contestation signals present"})
    add_event(p, eid="cue:req", kind="cue", etype="social.cue.request_sources",
              refs=["clm:misinfo"], data={"channel":"text","intent":"ask","urgency":"low","payload":{"text":"If making a claim, please provide a source."}})
    p["extensions"]["social"]["activitypub"]= {"type":src.get("type"),"actor":src.get("actor")}
    print(json.dumps(p, indent=2))
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python convert.py <input.json>")
    main(sys.argv[1])
