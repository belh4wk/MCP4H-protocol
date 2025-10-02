import os, json, socket, time
import paho.mqtt.client as mqtt

UDP_HOST = os.getenv("SIMHUB_UDP_HOST","0.0.0.0")
UDP_PORT = int(os.getenv("SIMHUB_UDP_PORT","9999"))
MQTT_HOST = os.getenv("MQTT_HOST","localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT","1883"))

thresholds = {"brake_deep":0.85,"slip_alert":0.25}
try:
    with open("mapping.json","r",encoding="utf-8") as f:
        thresholds.update(json.load(f))
except Exception: pass

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_HOST, UDP_PORT)); sock.settimeout(0.5)

m = mqtt.Client(); m.connect(MQTT_HOST, MQTT_PORT, 60); m.loop_start()
def publish(cue):
    topic = f"mcp4h/{cue['subject'].replace('.','/')}/{cue['signal']}"
    m.publish(topic, json.dumps(cue), qos=1, retain=False)

print(f"[SIMHUB] Listening UDP on {UDP_HOST}:{UDP_PORT}")
while True:
    try: data, addr = sock.recvfrom(8192)
    except socket.timeout: continue
    except Exception as e: print("[SIMHUB] UDP error:", e); continue
    try: frame = json.loads(data.decode("utf-8","ignore"))
    except Exception: continue

    speed = float(frame.get("speed", 0.0))
    brake = float(frame.get("brake", 0.0))
    rrSlip = float(frame.get("rrSlip", 0.0))
    ts = int(time.time())

    if brake >= thresholds["brake_deep"] and speed > 5.0:
        publish({"subject":"brake.front","signal":"BRAKE","state":"RISK","trend":"unstable","urgency":"caution",
                 "action_hint":"LIFT","channels":{"text":["FRONT","BRAKE","↯","RISK","LIFT"]},"ts": ts,"version":"cues.v0.1"})
    if rrSlip >= thresholds["slip_alert"]:
        publish({"subject":"tyre.RR","signal":"GRIP","state":"ALERT","trend":"down","urgency":"act",
                 "action_hint":"HOLD","channels":{"text":["RR","GRIP","↓","ALERT","HOLD"]},"ts": ts,"version":"cues.v0.1"})
