import json, sys
import os
# Ensure shared bridge helpers are importable (bridges/common)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from common.mcp4h_build import base_payload, add_event, sha256_text

def main(path: str):
    src = json.load(open(path, "r", encoding="utf-8"))
    p = base_payload("codex")
    ts = None
    add_event(p, eid="obs:img", kind="observation", etype="codex.page.image.observed", ts=ts,
              data={"modality":"visual","artifact":{"uri":src["image_uri"],"hash":sha256_text(src["image_uri"]), "content_type":"image/jpeg"}})
    add_event(p, eid="der:regions", kind="derivation", etype="codex.region.detected",
              refs=["obs:img"], method="system", data={"name":"region_count","value":1,"unit":"count"})
    add_event(p, eid="clm:reading", kind="claim", etype="codex.translation.hypothesis",
              refs=["der:regions"], method="model", confidence=0.4,
              alternates=[{"id":"alt:1","statement":"Could be a calendar table","refs":["der:regions"],"confidence":0.2,"method":"model"}],
              data={"statement":"Likely header line followed by body text"})
    add_event(p, eid="cue:review", kind="cue", etype="codex.cue.review_requested",
              refs=["clm:reading"], data={"channel":"text","intent":"review","urgency":"normal","payload":{"text":"Review hypotheses for page 1"}})
    p["extensions"]["codex"].update({"document_id":src["document_id"],"page":src["page"]})
    print(json.dumps(p, indent=2))
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python convert.py <input.json>")
    main(sys.argv[1])
