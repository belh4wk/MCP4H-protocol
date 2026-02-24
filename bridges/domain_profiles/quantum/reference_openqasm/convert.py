import sys, json
from common.mcp4h_build import base_payload, add_event, sha256_text

def main(path: str):
    qasm = open(path, "r", encoding="utf-8").read()
    p = base_payload("quantum")
    h = sha256_text(qasm)
    add_event(p, eid="obs:qasm", kind="observation", etype="quantum.job.submitted",
              data={"modality":"code","artifact":{"uri":"file://"+path,"hash":h,"content_type":"text/plain"}})
    add_event(p, eid="der:depth", kind="derivation", etype="quantum.circuit.compiled",
              refs=["obs:qasm"], method="system",
              data={"name":"estimated_depth","value":3,"unit":"gates"})
    add_event(p, eid="clm:noise", kind="claim", etype="quantum.anomaly.detected",
              refs=["der:depth"], method="heuristic", confidence=0.35,
              data={"statement":"Depth may exceed coherence on some devices"})
    add_event(p, eid="cue:rec", kind="cue", etype="quantum.cue.recommendation",
              refs=["clm:noise"], data={"channel":"text","intent":"recommend","urgency":"normal","payload":{"text":"Try transpiling with optimization level 3"}})
    print(json.dumps(p, indent=2))
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python convert.py <input.qasm>")
    main(sys.argv[1])
