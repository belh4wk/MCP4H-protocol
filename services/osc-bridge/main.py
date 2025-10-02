import os, json
import paho.mqtt.client as mqtt
from pythonosc import udp_client

MQTT_HOST = os.getenv("MQTT_HOST","localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT","1883"))
OSC_HOST = os.getenv("OSC_HOST","127.0.0.1")
OSC_PORT = int(os.getenv("OSC_PORT","9000"))
client = udp_client.SimpleUDPClient(OSC_HOST, OSC_PORT)

def on_message(mclient, userdata, msg):
    try: cue = json.loads(msg.payload.decode("utf-8"))
    except Exception: return
    subject = cue.get("subject","").replace(".","/")
    signal = str(cue.get("signal","")).lower()
    addr = f"/mcp4h/{subject}/{signal}"
    args = ["state", cue.get("state",""), "trend", cue.get("trend",""), "urgency", cue.get("urgency","")]
    ah = cue.get("action_hint")
    if ah: args += ["action_hint", ah]
    client.send_message(addr, args)
    print("[OSC]", addr, args)

m = mqtt.Client(); m.on_message = on_message
m.connect(MQTT_HOST, MQTT_PORT, 60)
m.subscribe("mcp4h/#"); m.loop_forever()
