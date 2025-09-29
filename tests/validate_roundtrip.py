#!/usr/bin/env python3
import json, os, sys, glob

try:
    import jsonschema
except ImportError:
    jsonschema = None

SCHEMA_PATH = os.path.join("spec", "schema", "mcp4h-v0.1.1.json")

def load_schema():
    with open(SCHEMA_PATH, "r") as f:
        return json.load(f)

def main():
    schema = None
    if jsonschema:
        schema = load_schema()
    else:
        print("jsonschema not installed; skipping schema validation.", file=sys.stderr)

    ok = True
    for path in glob.glob(os.path.join("tests", "vectors", "json", "*.json")):
        with open(path, "r") as f:
            obj = json.load(f)
        if schema and jsonschema:
            try:
                jsonschema.validate(obj, schema)
            except Exception as e:
                ok = False
                print(f"FAIL {path}: {e}")
        else:
            print(f"Loaded {path}")
    print("OK" if ok else "FAIL")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
