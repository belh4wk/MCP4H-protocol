FROM python:3.11-slim
WORKDIR /app
COPY services/cue-router/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY services/cue-router/main.py /app/main.py
COPY bridges/cue-router /app/bridges/cue-router
EXPOSE 8090
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8090"]
