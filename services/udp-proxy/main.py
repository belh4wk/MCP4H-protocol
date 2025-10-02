import os, socket, json
import paho.mqtt.client as mqtt

UDP_PORT = int(os.getenv("UDP_PORT","20777"))  # F1 default
MQTT_HOST = os.getenv("MQTT_HOST","mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT","1883"))
TOPIC = os.getenv("MQTT_TOPIC","mcp4h/udp")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", UDP_PORT))

m = mqtt.Client()
m.connect(MQTT_HOST, MQTT_PORT, 60)
m.loop_start()

print(f"[udp-proxy] listening on UDP {UDP_PORT}")
while True:
    data, addr = sock.recvfrom(4096)
    payload = {"src": addr[0], "len": len(data)}
    m.publish(TOPIC, json.dumps(payload))
