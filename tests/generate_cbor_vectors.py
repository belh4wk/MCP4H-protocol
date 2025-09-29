#!/usr/bin/env python3
import json, os, binascii, sys
try:
    import cbor2
except ImportError:
    print('cbor2 not installed; skipping CBOR.', file=sys.stderr); sys.exit(0)
for name in ['golden1','golden2']:
    obj=json.load(open(f'tests/vectors/json/{name}.json'))
    data=cbor2.dumps(obj)
    open(f'tests/vectors/cbor/{name}.cbor.hex','w').write(binascii.hexlify(data).decode())
print('CBOR written to tests/vectors/cbor/*.cbor.hex')
