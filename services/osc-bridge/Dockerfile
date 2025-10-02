FROM python:3.11-slim
WORKDIR /app
COPY services/osc-bridge/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/osc-bridge/ .
# Startup banner + run
CMD ["/bin/sh", "-lc", "echo '[mcp4h] 🚀 osc-bridge ready'; python main.py"]
