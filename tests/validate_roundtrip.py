#!/usr/bin/env python3
import json, os, sys, glob
try:
    import jsonschema
except ImportError:
    jsonschema=None

SCHEMA='spec/schema/mcp4h-v0.1.1.json'
def main():
    ok=True
    if jsonschema:
        schema=json.load(open(SCHEMA))
    else:
        print('jsonschema not installed; skipping validation.', file=sys.stderr)
        schema=None
    for path in glob.glob('tests/vectors/json/*.json'):
        obj=json.load(open(path))
        if schema and jsonschema:
            try:
                jsonschema.validate(obj, schema)
            except Exception as e:
                ok=False
                print(f'FAIL {path}: {e}')
    print('OK' if ok else 'FAIL')
    sys.exit(0 if ok else 1)
if __name__=='__main__':
    main()
