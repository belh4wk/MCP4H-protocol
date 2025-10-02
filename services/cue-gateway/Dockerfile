FROM python:3.11-slim
WORKDIR /app
COPY services/cue-gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/cue-gateway/ .
# Startup banner + run
CMD ["/bin/sh", "-lc", "echo '[mcp4h] 🚀 cue-gateway ready on :8080'; python main.py"]
