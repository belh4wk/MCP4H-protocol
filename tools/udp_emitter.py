#!/usr/bin/env python3
import socket, time, os
HOST='127.0.0.1'; PORT=42424; INTERVAL=0.01
path=os.path.join(os.path.dirname(__file__),'..','examples_v0.1.1','tyre_slip','packets.ndjson')
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
for line in open(path,'r'):
    sock.sendto(line.strip().encode('utf-8'), (HOST,PORT)); time.sleep(INTERVAL)
print(f'Sent NDJSON packets to {HOST}:{PORT}')