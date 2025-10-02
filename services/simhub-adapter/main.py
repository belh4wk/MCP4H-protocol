import json, os, time
import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv("MQTT_HOST","mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT","1883"))
SUB = os.getenv("MQTT_SUB","mcp4h/cues")

def on_message(client, userdata, msg):
    try:
        cue = json.loads(msg.payload.decode("utf-8"))
    except Exception:
        return
    # Placeholder: push to SimHub via local endpoints/UDP as needed
    print("[simhub] cue:", cue.get("intent"), cue.get("payload",{}))

m = mqtt.Client()
m.on_message = on_message
m.connect(MQTT_HOST, MQTT_PORT, 60)
m.subscribe(SUB)
m.loop_forever()
