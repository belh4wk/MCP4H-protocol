import json
from pathlib import Path

from jsonschema import Draft7Validator, RefResolver

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "spec" / "domain_profiles"

def load_schema(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_store(schema_files):
    """Build a resolver store so $id-based resolution never hits the network.

    jsonschema resolves relative $ref against the active base URI, which often
    becomes the schema's $id (https://...) rather than the local file:// URI.
    If we don't preload a store mapping those $id URIs to local schema objects,
    the validator will attempt an HTTP fetch and fail in CI.
    """

    store = {}
    for p in schema_files:
        s = load_schema(p)
        sid = s.get("$id")
        if isinstance(sid, str) and sid:
            store[sid] = s
        store[str(p.as_uri())] = s
    return store

def validate_examples():
    schema_files = sorted(SPEC.rglob("*.schema.json"))
    store = build_store(schema_files)
    failures = []
    for schema_path in schema_files:
        schema = load_schema(schema_path)
        resolver = RefResolver(
            base_uri=str(schema_path.as_uri()),
            referrer=schema,
            store=store,
        )
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
