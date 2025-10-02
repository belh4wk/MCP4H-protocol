from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json, os, time
import paho.mqtt.client as mqtt
from jsonschema import validate, ValidationError

MQTT_HOST = os.getenv("MQTT_HOST","mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT","1883"))
TOPIC = os.getenv("MQTT_TOPIC","mcp4h/cues")

# Load schema and lexicon
with open("spec/cues/cue.schema.json","r") as f:
    CUE_SCHEMA = json.load(f)
with open("spec/cues/lexicon.v0.1.json","r") as f:
    LEX = json.load(f)

app = FastAPI(title="MCP4H Cue Gateway")

class CueModel(BaseModel):
    id: str
    ts: str
    channel: str
    intent: str
    urgency: str | None = "low"
    payload: dict | None = None

# MQTT client
m = mqtt.Client()
m.connect(MQTT_HOST, MQTT_PORT, 60)
m.loop_start()

@app.get("/health")
def health():
    return {"ok": True, "time": time.time()}

@app.post("/cue")
def post_cue(cue: CueModel):
    data = cue.model_dump()
    # validate
    try:
        validate(instance=data, schema=CUE_SCHEMA)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"schema: {e.message}")
    # enrich with lexicon defaults (optional)
    data.setdefault("payload",{})
    m.publish(TOPIC, json.dumps(data))
    return {"accepted": True, "topic": TOPIC}
