# Optional local TTS (run outside Docker): pip install pyttsx3
import json, pyttsx3, sys
engine = pyttsx3.init()
for line in sys.stdin:
    line=line.strip()
    if not line: continue
    engine.say(line); engine.runAndWait()
