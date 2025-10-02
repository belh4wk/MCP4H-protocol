#!/usr/bin/env python3
import argparse, json, time, requests, sys
ap = argparse.ArgumentParser(description="MCP4H CLI")
ap.add_argument("file", help="cue JSON file (or examples_cues/*.json)")
ap.add_argument("--url", default="http://localhost:8080/cue")
args = ap.parse_args()
cue = json.load(open(args.file))
r = requests.post(args.url, json=cue, headers={"Content-Type":"application/mcp4h+json"})
print(r.status_code, r.text)
