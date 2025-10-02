FROM python:3.11-slim
WORKDIR /app
COPY services/voice-coach/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/voice-coach/ .
CMD ["python","main.py"]
