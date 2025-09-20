
import json, sys, pathlib
def main():
    failed = False
    for p in pathlib.Path('examples').glob('**/*.json'):
        try:
            json.loads(p.read_text(encoding='utf-8'))
            print(f"[OK] {p}")
        except Exception as e:
            failed = True
            print(f"[FAIL] {p}: {e}")
    sys.exit(1 if failed else 0)
if __name__ == "__main__":
    main()
