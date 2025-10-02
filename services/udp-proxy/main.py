import os, socket, json

GAME_PORT = int(os.getenv("GAME_UDP_PORT","20777"))
FWD_HOST = os.getenv("FORWARD_UDP_HOST","127.0.0.1")
FWD_PORT = int(os.getenv("FORWARD_UDP_PORT","9999"))

sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_in.bind(("0.0.0.0", GAME_PORT)); sock_in.settimeout(0.5)
sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"[UDP-PROXY] Listening 0.0.0.0:{GAME_PORT} -> {FWD_HOST}:{FWD_PORT}")

while True:
    try: data, addr = sock_in.recvfrom(8192)
    except socket.timeout: continue
    except Exception as e: print("[UDP-PROXY] error", e); continue
    try:
        s = data.decode("utf-8","ignore")
        if '=' in s:  # Assetto Corsa style
            kv = {}
            for part in s.split(';'):
                if '=' in part:
                    k,v = part.split('=',1); k=k.strip(); v=v.strip()
                    if not k: continue
                    try: kv[k]=float(v)
                    except: kv[k]=v
            frame={"speed":float(kv.get("speedKmh",kv.get("speed",0.0))),
                   "brake":float(kv.get("brakeInput",kv.get("brake",0.0))),
                   "rrSlip":float(kv.get("slipRR",kv.get("rrSlip",0.0)))}
        else:  # passthrough JSON
            frame = json.loads(s)
    except Exception:
        continue
    sock_out.sendto(json.dumps(frame).encode("utf-8"), (FWD_HOST, FWD_PORT))
