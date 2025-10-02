FROM python:3.11-slim
WORKDIR /app
COPY services/voice-coach/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/voice-coach/ .
# Startup banner + run
CMD ["/bin/sh", "-lc", "echo '[mcp4h] 🚀 voice-coach ready'; python main.py"]
