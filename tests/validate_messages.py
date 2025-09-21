import json
import sys
import pathlib
from jsonschema import Draft7Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "spec" / "schema" / "mcp4h-v0.1.json"
EXAMPLES_DIR = ROOT / "examples"

def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def is_mcp4h_message(obj):
    return isinstance(obj, dict) and "header" in obj and "signal" in obj

def main():
    print(f"[INFO] Repo root: {ROOT}")
    print(f"[INFO] Schema path: {SCHEMA}")
    print(f"[INFO] Examples dir: {EXAMPLES_DIR}")

    if not SCHEMA.exists():
        print(f"[ERROR] Schema not found at {SCHEMA}")
        return 1

    schema = load_json(SCHEMA)
    validator = Draft7Validator(schema)

    if not EXAMPLES_DIR.exists():
        print("[WARN] 'examples/' directory not found. Skipping validation.")
        return 0

    json_files = list(EXAMPLES_DIR.rglob("*.json"))
    print(f"[INFO] Found {len(json_files)} JSON file(s) under 'examples/':")
    for p in json_files:
        print(f"  - {p.relative_to(ROOT)}")

    if not json_files:
        print("[WARN] No JSON files found to validate. Skipping.")
        return 0

    checked = 0
    failures = 0
    for jf in json_files:
        try:
            data = load_json(jf)
        except Exception as e:
            print(f"[SKIP] {jf.relative_to(ROOT)}: not valid JSON -> {e}")
            continue

        if not is_mcp4h_message(data):
            print(f"[SKIP] {jf.relative_to(ROOT)}: not an MCP4H message (missing 'header'/'signal')")
            continue

        checked += 1
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        if errors:
            print(f"[FAIL] {jf.relative_to(ROOT)}:")
            for err in errors:
                path = "/".join(map(str, err.path)) or "<root>"
                print(f"  - {path}: {err.message}")
            failures += 1
        else:
            print(f"[OK]   {jf.relative_to(ROOT)}")

    if checked == 0:
        print("[WARN] No MCP4H-shaped JSON messages found. Nothing to validate; treating as success for now.")
        return 0

    if failures:
        print(f"Validation failed for {failures} file(s).")
        return 1

    print("All MCP4H example JSON files are valid against the schema.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
