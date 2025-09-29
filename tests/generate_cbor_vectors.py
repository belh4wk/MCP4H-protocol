#!/usr/bin/env python3
"""Generate CBOR encodings for test vectors if `cbor2` is available."""
import json, os, binascii, sys
try:
    import cbor2
except ImportError:
    print("cbor2 not installed; skip CBOR generation.", file=sys.stderr)
    sys.exit(0)

BASE = os.path.dirname(__file__)
json_dir = os.path.join(BASE, "vectors", "json")
cbor_dir = os.path.join(BASE, "vectors", "cbor")
os.makedirs(cbor_dir, exist_ok=True)

for name in ["golden1", "golden2"]:
    with open(os.path.join(json_dir, f"{name}.json"), "r") as f:
        obj = json.load(f)
    data = cbor2.dumps(obj)
    with open(os.path.join(cbor_dir, f"{name}.cbor.hex"), "w") as f:
        f.write(binascii.hexlify(data).decode("ascii"))
print("CBOR vectors written to tests/vectors/cbor/*.cbor.hex")
