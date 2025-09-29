import glob, json, os, pytest

try:
    import jsonschema
except Exception:  # pragma: no cover
    jsonschema = None

SCHEMA_PATH = os.path.join('spec', 'schema', 'mcp4h-v0.1.1.json')
VECTORS_DIR = os.path.join('tests', 'vectors', 'json')

@pytest.mark.skipif(jsonschema is None, reason="jsonschema not installed")
def test_vectors_validate_against_schema():
    assert os.path.exists(SCHEMA_PATH), "Schema file missing: %s" % SCHEMA_PATH
    schema = json.load(open(SCHEMA_PATH, 'r'))
    files = sorted(glob.glob(os.path.join(VECTORS_DIR, '*.json')))
    assert files, "No JSON vectors found in %s" % VECTORS_DIR
    for path in files:
        obj = json.load(open(path, 'r'))
        jsonschema.validate(obj, schema)
