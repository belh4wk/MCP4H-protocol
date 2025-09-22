#!/usr/bin/env python3
import json, glob
from pathlib import Path
from jsonschema import validate, Draft202012Validator

REPO = Path(__file__).resolve().parents[1]
SCHEMA_V01  = REPO / "spec" / "schema" / "mcp4h-v0.1.json"
SCHEMA_V011 = REPO / "schemas" / "mcp4h-0.1.1.schema.json"

def load(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def check_schema(p):
    Draft202012Validator.check_schema(load(p))

def validate_dir(dir_path, schema_path, label):
    check_schema(schema_path)
    examples = sorted(glob.glob(str(dir_path / "*.json")))
    if not examples:
        print(f"[WARN] No examples in {dir_path}")
        return 0, 0
    ok = fail = 0
    schema = load(schema_path)
    for ex in examples:
        try:
            data = load(ex)
            validate(instance=data, schema=schema)
            print(f"[OK]   {Path(ex).name}")
            ok += 1
        except Exception as e:
            print(f"[FAIL] {Path(ex).name}: {e}")
            fail += 1
    return ok, fail

def main():
    print(f"[INFO] Repo root: {REPO}")
    ok1, fail1 = validate_dir(REPO / "examples", SCHEMA_V01, "examples (v0.1)")
    ok2 = fail2 = 0
    if (REPO / "examples_v0.1.1").exists():
        ok2, fail2 = validate_dir(REPO / "examples_v0.1.1", SCHEMA_V011, "examples_v0.1.1 (extensions)")
    print(f"[INFO] Summary: {ok1+ok2} ok, {fail1+fail2} failed")
    raise SystemExit(0 if (fail1+fail2)==0 else 1)

if __name__ == "__main__":
    main()
