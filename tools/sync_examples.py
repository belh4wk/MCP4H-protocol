#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil

REPO = Path(__file__).resolve().parents[1]
MAP_PATH = REPO / 'examples' / '_sync_map.json'


def load_map() -> dict:
    return json.loads(MAP_PATH.read_text(encoding='utf-8'))


def sync(check_only: bool) -> int:
    spec = load_map()
    mismatches = []
    for entry in spec.get('mirrors', []):
        src = REPO / entry['source']
        if not src.exists():
            mismatches.append(f'missing source: {src.relative_to(REPO)}')
            continue
        src_bytes = src.read_bytes()
        for target_rel in entry.get('targets', []):
            target = REPO / target_rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists() or target.read_bytes() != src_bytes:
                if check_only:
                    mismatches.append(f'out of sync: {target.relative_to(REPO)} <- {src.relative_to(REPO)}')
                else:
                    shutil.copyfile(src, target)
                    print(f'[SYNC] {target.relative_to(REPO)} <- {src.relative_to(REPO)}')
    if check_only:
        if mismatches:
            for item in mismatches:
                print(f'[FAIL] {item}')
            return 1
        print('[OK] example mirrors are in sync')
        return 0
    print('[OK] example mirrors synchronized')
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description='Sync or verify legacy example mirrors from canonical examples/messages sources.')
    parser.add_argument('--check', action='store_true', help='Fail if any mirrored example is missing or out of sync.')
    args = parser.parse_args()
    return sync(check_only=args.check)


if __name__ == '__main__':
    raise SystemExit(main())
