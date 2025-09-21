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
    schema = load_json(SCHEMA)
    validator = Draft7Validator(schema)

    json_files = list(EXAMPLES_DIR.rglob("*.json"))
    if not json_files:
        print("No example JSON files found to validate in 'examples/'.")
        return 0

    checked = 0
    failures = 0
    for jf in json_files:
        try:
            data = load_json(jf)
        except Exception as e:
            print(f"[SKIP] {jf}: not valid JSON -> {e}")
            continue

        if not is_mcp4h_message(data):
            print(f"[SKIP] {jf}: not an MCP4H message (no 'header'+'signal' keys)")
            continue

        checked += 1
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        if errors:
            print(f"[FAIL] {jf}:")
            for err in errors:
                path = "/".join(map(str, err.path)) or "<root>"
                print(f"  - {path}: {err.message}")
            failures += 1
        else:
            print(f"[OK]   {jf}")

    if checked == 0:
        print("Found JSON files, but none looked like MCP4H messages. Add an example to 'examples/' to enable validation.")
        return 1 if json_files else 0

    if failures:
        print(f"Validation failed for {failures} file(s).")
        return 1

    print("All MCP4H example JSON files are valid against the schema.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
