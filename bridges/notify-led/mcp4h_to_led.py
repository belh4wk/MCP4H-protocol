#!/usr/bin/env python3
import json, sys

def map_led(meta):
    if meta.get("urgency") == "high":
        return ("#FFCC00","triple_quick")
    heat = meta.get("heat",0)
    val  = meta.get("valence","neutral")
    flags = meta.get("civility_flags",[])
    if val == "positive" and heat <= 1:
        return ("#34C759","steady")
    if val in ("neutral","mixed") and heat <= 1:
        return ("#FFFFFF","single")
    if heat >= 2 or val == "negative" or (flags and len(flags)>0):
        return ("#FF3B30","double_pulse")
    return ("#FFFFFF","single")

def main():
    if len(sys.argv) < 2:
        print("usage: mcp4h_to_led.py <envelope.json>"); sys.exit(1)
    env = json.load(open(sys.argv[1], encoding="utf-8"))
    color, pattern = map_led(env.get("metadata",{}))
    print("LED:", color, pattern)

if __name__ == "__main__":
    main()
