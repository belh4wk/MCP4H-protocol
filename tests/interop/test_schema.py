import glob
import json
from pathlib import Path

import jsonschema

schema = json.load(open('spec/cues/cue.schema.json', encoding='utf-8'))
for f in glob.glob('examples/messages/cues/*.json'):
    data = json.load(open(f, encoding='utf-8'))
    jsonschema.validate(data, schema)
    print(f'Schema OK: {Path(f).name}')
print('Schema OK')
