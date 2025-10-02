FROM python:3.11-slim
WORKDIR /app
COPY services/osc-bridge/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/osc-bridge/ .
CMD ["python","main.py"]
