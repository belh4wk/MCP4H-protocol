FROM python:3.11-slim
WORKDIR /app
COPY services/simhub-adapter/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/simhub-adapter/ .
# Startup banner + run
CMD ["/bin/sh", "-lc", "echo '[mcp4h] 🚀 simhub-adapter ready'; python main.py"]
