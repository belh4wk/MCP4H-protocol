#!/usr/bin/env python3
import argparse, json, socket, time, os
from datetime import datetime
from uuid import uuid4

GREEN="#1FDB51"; AMBER="#FFCC00"; RED="#FF3B30"

def ema(prev, x, alpha=0.3):
    return alpha*x + (1-alpha)*prev if prev is not None else x

def classify_slip(x, last_state):
    lo, hi = 0.05, 0.12
    if last_state == "critical" and x < hi*0.8: last_state = "warning"
    if last_state == "warning" and x < lo*0.8: last_state = "ok"
    if x > hi: return "critical"
    if x > lo: return "warning"
    return last_state if last_state else "ok"

def color_for(sev): return {"ok":GREEN,"warning":AMBER,"critical":RED}[sev]
def blink_for(sev): return sev == "critical"

def build_envelope(vals, sev, colors, blink):
    return {
      "version":"mcp4h/0.1",
      "id": str(uuid4()),
      "timestamp": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
      "origin": {"platform":"simhub","relation":"telemetry"},
      "actor": {"role":"system","handle":"local_sim"},
      "text": "",
      "metadata": {"heat":1,"valence":"neutral","tone":"telemetry","constraints_detected":["traction","grip"]},
      "extensions": {"traction_leds": {
          "unit":"slip_ratio","values":vals,"severity":sev,"colors":colors,"blink":blink
      }}
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["demo","udp"], default="demo")
    ap.add_argument("--udp-host", default="127.0.0.1")
    ap.add_argument("--udp-port", type=int, default=9999)
    ap.add_argument("--hz", type=float, default=10.0)
    ap.add_argument("--out", default="out/SimHubVars.json")
    args = ap.parse_args()

    os.makedirs("out", exist_ok=True)
    sock = None
    if args.mode == "udp":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    slip = {"LF":0.02,"RF":0.03,"LR":0.04,"RR":0.05}
    slip_ema = {"LF":None,"RF":None,"LR":None,"RR":None}
    last = {"LF":"","RF":"","LR":"","RR":""}
    t=0.0; dt=1.0/args.hz

    try:
        while True:
            slip["LF"] = 0.03 + 0.01
            slip["RF"] = 0.03 + 0.01
            slip["LR"] = 0.04 + (0.12 if int(t)%4==0 else 0.02)
            slip["RR"] = 0.05 + (0.16 if int(t)%5==0 else 0.03)

            for w in slip:
                slip_ema[w] = ema(slip_ema[w], slip[w], 0.3)

            sev = {w: classify_slip(slip_ema[w], last[w]) for w in slip}
            for w in sev: last[w] = sev[w]
            colors = {w: color_for(sev[w]) for w in sev}
            blink  = {w: blink_for(sev[w]) for w in sev}

            env = build_envelope({w: round(slip_ema[w],3) for w in slip}, sev, colors, blink)

            vars_obj = {
                "MCP4H_Traction_LF_Color": colors["LF"],
                "MCP4H_Traction_RF_Color": colors["RF"],
                "MCP4H_Traction_LR_Color": colors["LR"],
                "MCP4H_Traction_RR_Color": colors["RR"],
                "MCP4H_Traction_LF_Blink": blink["LF"],
                "MCP4H_Traction_RF_Blink": blink["RF"],
                "MCP4H_Traction_LR_Blink": blink["LR"],
                "MCP4H_Traction_RR_Blink": blink["RR"]
            }
            with open(args.out,"w",encoding="utf-8") as f: json.dump(vars_obj,f,indent=2)

            if sock:
                msg = json.dumps(env).encode("utf-8")
                sock.sendto(msg, (args.udp_host, args.udp_port))

            time.sleep(dt); t += dt
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
