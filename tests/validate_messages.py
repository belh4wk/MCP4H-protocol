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

def is_mcp4h_like(data):
    return isinstance(data, dict) and isinstance(data.get("metadata"), dict) and isinstance(data.get("version"), str) and data["version"].startswith("mcp4h/")

def validate_dir(dir_path, schema_path, label):
    print(f"[INFO] Validating {label} with {schema_path}")
    Draft202012Validator.check_schema(load(schema_path))
    ok = fail = skip = 0
    for ex in sorted(glob.glob(str(dir_path / "*.json"))):
        try:
            data = load(ex)
        except Exception as e:
            print(f"  [SKIP] {Path(ex).name}: unreadable JSON ({e})"); skip += 1; continue
        if not is_mcp4h_like(data):
            print(f"  [SKIP] {Path(ex).name}: not an MCP4H envelope"); skip += 1; continue
        try:
            validate(instance=data, schema=load(schema_path))
            print(f"  [OK]  {Path(ex).name}")
            ok += 1
        except Exception as e:
            print(f"  [FAIL]{Path(ex).name}: {e}"); fail += 1
    print(f"[INFO] {label}: {ok} ok, {fail} failed, {skip} skipped")
    return ok, fail, skip

def main():
    total_ok = total_fail = total_skip = 0
    for folder, schema in [(REPO / 'examples', SCHEMA_V01), (REPO / 'examples_v0.1.1', SCHEMA_V011)]:
        if folder.exists():
            ok, fail, skip = validate_dir(folder, schema, folder.name)
            total_ok += ok; total_fail += fail; total_skip += skip
    print(f"[INFO] Summary: {total_ok} ok, {total_fail} failed, {total_skip} skipped")
    raise SystemExit(0 if total_fail == 0 else 1)

if __name__ == "__main__":
    main()
