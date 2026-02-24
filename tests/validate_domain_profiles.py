import json
from pathlib import Path
from jsonschema import Draft7Validator, RefResolver

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "spec" / "domain_profiles"

def load_schema(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def make_resolver(base: Path):
    def handler(uri):
        # allow relative refs in domain_profiles
        if uri.startswith("https://belh4wk.github.io/MCP4H/"):
            rel = uri.split("spec/domain_profiles/")[-1]
            local = SPEC / rel
            return load_schema(local)
        return None
    return RefResolver(base_uri=str(base.as_uri()), referrer=None, handlers={"https": handler})

def validate_examples():
    schema_files = sorted(SPEC.rglob("*.schema.json"))
    failures = []
    for schema_path in schema_files:
        schema = load_schema(schema_path)
        resolver = RefResolver(base_uri=str(schema_path.as_uri()), referrer=schema)
        v = Draft7Validator(schema, resolver=resolver)
        ex_dir = schema_path.parent / "examples"
        if not ex_dir.exists():
            continue
        for ex in sorted(ex_dir.glob("*.json")):
            data = json.loads(ex.read_text(encoding="utf-8"))
            errs = sorted(v.iter_errors(data), key=lambda e: e.path)
            if errs:
                failures.append((schema_path, ex, errs))
    if failures:
        lines = []
        for schema_path, ex, errs in failures:
            lines.append(f"Schema: {schema_path}")
            lines.append(f"Example: {ex}")
            for e in errs[:10]:
                lines.append(f"  - {list(e.path)}: {e.message}")
        raise SystemExit("\n".join(lines))
    print(f"OK: validated domain profile examples for {len(schema_files)} schemas.")

if __name__ == "__main__":
    validate_examples()
