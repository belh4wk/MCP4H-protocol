import os, json
import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv("MQTT_HOST","localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT","1883"))

def say(cue):
    sig = cue.get("signal","").upper()
    state = cue.get("state","")
    urg = cue.get("urgency","")
    ah = (cue.get("action_hint") or "").upper()
    out = []
    if sig == "BRAKE":
        if urg == "act": out.append("Brake")
        if urg == "caution": out.append("Hold")
        if ah in ("LIFT","HOLD","BOX"): out.append(ah.capitalize())
    elif sig == "GRIP":
        if state == "ALERT": out.append("Hold")
        if ah in ("HOLD","LIFT"): out.append(ah.capitalize())
    if out: print("[VOICE-COACH]", " ".join(out))

def on_message(client, userdata, msg):
    try: cue = json.loads(msg.payload.decode("utf-8"))
    except Exception: return
    say(cue)

m = mqtt.Client(); m.on_message = on_message
m.connect(MQTT_HOST, MQTT_PORT, 60)
m.subscribe("mcp4h/#"); m.loop_forever()
