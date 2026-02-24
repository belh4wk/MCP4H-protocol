import sys, json
import os
# Ensure shared bridge helpers are importable (bridges/common)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
import xml.etree.ElementTree as ET
from common.mcp4h_build import base_payload, add_event

def main(path: str):
    xml = open(path, "r", encoding="utf-8").read()
    root = ET.fromstring(xml)
    msg_id = None
    for el in root.iter():
        if el.tag.lower().endswith("msgid"):
            msg_id = (el.text or "").strip()
            break
    p = base_payload("finance")
    add_event(p, eid="obs:msg", kind="observation", etype="finance.message.received",
              data={"modality":"document","artifact":{"uri":"file://"+path,"hash":"sha256:" + __import__('hashlib').sha256(xml.encode('utf-8')).hexdigest(),"content_type":"application/xml"}})
    add_event(p, eid="der:msgid", kind="derivation", etype="finance.transaction.recorded",
              refs=["obs:msg"], method="system", data={"name":"message_id","value":msg_id or "unknown","unit":"string"})
    add_event(p, eid="clm:risk", kind="claim", etype="finance.risk.signal",
              refs=["der:msgid"], method="heuristic", confidence=0.2,
              data={"statement":"No risk rules evaluated in reference bridge"})
    add_event(p, eid="cue:hold", kind="cue", etype="finance.cue.release",
              refs=["clm:risk"], data={"channel":"system","intent":"release","urgency":"normal","payload":{"decision":"release"}})
    print(json.dumps(p, indent=2))
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python convert.py <input.xml>")
    main(sys.argv[1])
