import json, os
import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv("MQTT_HOST","mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT","1883"))
SUB = os.getenv("MQTT_SUB","mcp4h/cues")
PUB = os.getenv("MQTT_PUB","mcp4h/osc")

def on_message(client, userdata, msg):
    try:
        cue = json.loads(msg.payload.decode("utf-8"))
    except Exception:
        return
    # Placeholder: translate to OSC; we publish a marker instead
    out = {"osc": "/mcp4h/cue", "args": cue.get("intent","unknown")}
    client.publish(PUB, json.dumps(out))

m = mqtt.Client()
m.on_message = on_message
m.connect(MQTT_HOST, MQTT_PORT, 60)
m.subscribe(SUB)
m.loop_forever()
