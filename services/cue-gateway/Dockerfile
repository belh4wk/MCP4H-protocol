FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN mkdir -p /app/spec/cues
COPY ../../spec/cues/cue.schema.json /app/spec/cues/cue.schema.json
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8080"]
