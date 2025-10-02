import os, json, asyncio, time, pathlib
from fastapi import FastAPI, WebSocket, HTTPException
from pydantic import BaseModel
import paho.mqtt.client as mqtt
from jsonschema import validate, ValidationError

MQTT_HOST = os.getenv("MQTT_HOST","localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT","1883"))
SCHEMA = json.loads(open("/app/spec/cues/cue.schema.json").read())

app = FastAPI(title="MCP4H Cue Gateway")
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_start()

class Cue(BaseModel):
    subject: str; signal: str; state: str; trend: str; urgency: str
    action_hint: str | None = None; confidence: float | None = None
    channels: dict; scope: list[str] | None = None; ts: int; version: str

@app.post("/cue")
def post_cue(cue: Cue):
    data = cue.dict()
    try: validate(instance=data, schema=SCHEMA)
    except ValidationError as e: raise HTTPException(400, f"Schema validation error: {e.message}")
    data["received_ts"] = int(time.time())
    topic = f"mcp4h/{data['subject'].replace('.','/')}/{data['signal']}"
    mqtt_client.publish(topic, json.dumps(data), qos=1, retain=False)
    return {"ok": True, "topic": topic}

subs = set()
def on_mqtt(client, userdata, msg):
    payload = msg.payload.decode("utf-8", errors="ignore")
    for ws in list(subs):
        try: asyncio.create_task(ws.send_text(payload))
        except Exception: pass

mqtt_client.on_message = on_mqtt
mqtt_client.subscribe("mcp4h/#")

@app.websocket("/cues")
async def ws_cues(ws: WebSocket):
    await ws.accept(); subs.add(ws)
    try:
        while True: await asyncio.sleep(1)
    finally:
        subs.discard(ws)
