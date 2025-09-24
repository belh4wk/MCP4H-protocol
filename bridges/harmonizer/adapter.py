#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from mapper import mcp4h_to_prompt, prompt_to_mcp4h_response

def simulate_gpt_completion(prompt: str) -> str:
    # Deterministic echo for demo purposes
    first = ""
    for line in prompt.splitlines():
        if line.strip():
            first = line.strip()[:120]
            break
    return f"[Harmonizer demo] Ack. First line: {first}"

def main():
    ap = argparse.ArgumentParser(description="Harmonizer reference bridge (MCP4H ↔ GPT)")
    ap.add_argument("--in", dest="infile", required=True, help="Path to MCP4H input packet (JSON)")
    ap.add_argument("--out", dest="outfile", required=False, help="Path for MCP4H response packet (JSON)")
    args = ap.parse_args()

    data = json.loads(Path(args.infile).read_text(encoding="utf-8"))

    prompt, meta = mcp4h_to_prompt(data)
    print("=== Prompt to GPT ===")
    print(prompt)
    print("=====================")

    gpt_text = simulate_gpt_completion(prompt)
    response_packet = prompt_to_mcp4h_response(gpt_text, meta)

    if args.outfile:
        Path(args.outfile).write_text(json.dumps(response_packet, indent=2), encoding="utf-8")
        print(f"\nWrote MCP4H response packet to {args.outfile}")
    else:
        print("\n=== MCP4H Response Packet ===")
        print(json.dumps(response_packet, indent=2))

if __name__ == "__main__":
    main()
