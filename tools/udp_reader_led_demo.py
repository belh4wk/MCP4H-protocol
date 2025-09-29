#!/usr/bin/env python3
import socket, json
HOST='0.0.0.0'; PORT=42424
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); sock.bind((HOST,PORT))
print(f'Listening on {HOST}:{PORT} ...')
def led_for(state): return {'ok':'OFF','warn':'ON (dim)','crit':'BLINK'}.get(state,'OFF')
while True:
    data,_=sock.recvfrom(65535)
    try:
        msg=json.loads(data.decode('utf-8'))
        tyres=msg.get('payload',{}).get('traction',{}).get('tyres',{})
        leds={k: led_for(v.get('state','ok')) for k,v in tyres.items()}
        print('LEDs:', leds)
    except Exception as e:
        print('Bad packet:', e)
