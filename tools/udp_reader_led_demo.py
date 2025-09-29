#!/usr/bin/env python3
"""Listen for MCP4H NDJSON over UDP and print LED states per tyre."""
import socket, json

HOST = "0.0.0.0"
PORT = 42424

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
print(f"Listening on {HOST}:{PORT} ...")

def led_for(state):
    return {"ok": "OFF", "warn": "ON (dim)", "crit": "BLINK"}[state]

while True:
    data, addr = sock.recvfrom(65535)
    try:
        msg = json.loads(data.decode("utf-8"))
        tyres = msg.get("payload", {}).get("traction", {}).get("tyres", {})
        states = {k: v.get("state", "ok") for k, v in tyres.items()}
        leds = {k: led_for(s) for k, s in states.items()}
        print(f"LEDs: {leds}")
    except Exception as e:
        print(f"Bad packet from {addr}: {e}")
