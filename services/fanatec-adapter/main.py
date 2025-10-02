import os, json
import paho-mqtt.client as mqtt
MQTT_HOST=os.getenv("MQTT_HOST","localhost"); MQTT_PORT=int(os.getenv("MQTT_PORT","1883"))
BACKEND=os.getenv("BACKEND","mock")
def render_mock(c): print("[FANATEC:MOCK]", c.get("signal"), c.get("state"), c.get("urgency"))
def render_openrgb(c): print("[FANATEC:OPENRGB] urgency=", c.get("urgency"))
def render_fanatec_sdk(c): print("[FANATEC:SDK] mapped to LED/haptic pattern")
RENDER={"mock":render_mock,"openrgb":render_openrgb,"fanatec_sdk":render_fanatec_sdk}.get(BACKEND,render_mock)
def on_msg(cl,u,m): 
    try: c=json.loads(m.payload.decode("utf-8"))
    except Exception: return
    RENDER(c)
m=mqtt.Client(); m.on_message=on_msg; m.connect(MQTT_HOST, MQTT_PORT, 60); m.subscribe("mcp4h/#"); print("[FANATEC] backend=",BACKEND); m.loop_forever()
