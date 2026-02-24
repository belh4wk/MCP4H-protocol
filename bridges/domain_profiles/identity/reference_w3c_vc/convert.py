import json, sys
from common.mcp4h_build import base_payload, add_event

def main(path: str):
    src = json.load(open(path, "r", encoding="utf-8"))
    p = base_payload("identity")
    add_event(p, eid="obs:vc", kind="observation", etype="identity.credential.issued",
              data={"modality":"document","value":src})
    add_event(p, eid="der:sub", kind="derivation", etype="identity.claim.asserted",
              refs=["obs:vc"], method="system", data={"name":"subject_id","value":src.get("credentialSubject",{}).get("id"),"unit":"did"})
    add_event(p, eid="clm:verify", kind="claim", etype="identity.verification.performed",
              refs=["der:sub"], method="heuristic", confidence=0.5,
              data={"statement":"Credential structure looks valid; cryptographic verification not performed"})
    add_event(p, eid="cue:allow", kind="cue", etype="identity.cue.allow",
              refs=["clm:verify"], data={"channel":"system","intent":"allow","urgency":"normal","payload":{"decision":"allow"}})
    print(json.dumps(p, indent=2))
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python convert.py <input.json>")
    main(sys.argv[1])
