import json,glob,jsonschema
schema=json.load(open('spec/cues/cue.schema.json'))
for f in glob.glob('examples_cues/*.json'):
 d=json.load(open(f)); jsonschema.validate(d,schema)
print('Schema OK')
