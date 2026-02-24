import json
import subprocess
import sys
from pathlib import Path
from jsonschema import Draft7Validator, RefResolver

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "spec" / "domain_profiles"
BRIDGES = ROOT / "bridges" / "domain_profiles"

def load_schema(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def build_store():
    schema_files = sorted(SPEC.rglob('*.schema.json'))
    store = {}
    for p in schema_files:
        s = load_schema(p)
        sid = s.get('$id')
        if isinstance(sid, str) and sid:
            store[sid] = s
        store[str(p.as_uri())] = s
    return store

def validator_for(profile: str, store: dict):
    schema_path = SPEC / profile / f"{profile}.schema.json"
    schema = load_schema(schema_path)
    resolver = RefResolver(base_uri=str(schema_path.as_uri()), referrer=schema, store=store)
    return Draft7Validator(schema, resolver=resolver)

def run_converter(py: Path, sample: Path):
    out = subprocess.check_output([sys.executable, str(py), str(sample)], cwd=str(py.parent), text=True)
    return json.loads(out)

def main():
    failures = []
    store = build_store()
    for profile_dir in sorted(BRIDGES.iterdir()):
        if not profile_dir.is_dir():
            continue
        profile = profile_dir.name
        # Skip shared helper folders or unknown profiles
        schema_path = SPEC / profile / f"{profile}.schema.json"
        if profile == "common" or not schema_path.exists():
            continue
        v = validator_for(profile, store)
        for bridge_dir in sorted(profile_dir.iterdir()):
            py = bridge_dir / "convert.py"
            samples = bridge_dir / "samples"
            if not py.exists() or not samples.exists():
                continue
            sample_inputs = sorted([p for p in samples.iterdir() if p.name.startswith("input")])
            for s in sample_inputs:
                try:
                    data = run_converter(py, s)
                    errs = sorted(v.iter_errors(data), key=lambda e: e.path)
                    if errs:
                        failures.append((profile, py, s, errs))
                except Exception as ex:
                    failures.append((profile, py, s, [ex]))
    if failures:
        lines=[]
        for profile, py, s, errs in failures:
            lines.append(f"Profile: {profile}")
            lines.append(f"Bridge: {py}")
            lines.append(f"Sample: {s}")
            for e in errs[:5]:
                if hasattr(e, 'message'):
                    lines.append(f"  - {list(e.path)}: {e.message}")
                else:
                    lines.append(f"  - {repr(e)}")
        raise SystemExit("\n".join(lines))
    print("OK: bridges produced valid profile payloads.")

if __name__ == "__main__":
    main()