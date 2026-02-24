import hashlib, json, datetime
from datetime import timezone

def iso_now():
    return datetime.datetime.now(timezone.utc).isoformat().replace("+00:00","Z")

def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()

def base_payload(profile: str):
    return {"profile": f"{profile}/dev", "events": [], "extensions": {profile: {"_x": {"producer":"reference_bridge"}}}}

def add_event(payload, *, eid, kind, etype, ts=None, refs=None, method=None, confidence=None, uncertainty=None, alternates=None, data=None):
    ev = {"id": eid, "kind": kind, "type": etype, "data": data or {}}
    if ts is None:
        ts = iso_now()
    ev["ts"] = ts
    if refs:
        ev["refs"] = refs
    if method:
        ev["method"] = method
    if confidence is not None:
        ev["confidence"] = float(confidence)
    if uncertainty is not None:
        ev["uncertainty"] = uncertainty
    if alternates is not None:
        ev["alternates"] = alternates
    payload["events"].append(ev)
    return ev
