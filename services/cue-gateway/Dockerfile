FROM python:3.11-slim

WORKDIR /app

COPY services/cue-gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY services/cue-gateway/ .

# Copy spec files from repo root (context is project root per compose)
RUN mkdir -p /app/spec/cues
COPY spec/cues/cue.schema.json /app/spec/cues/cue.schema.json
COPY spec/cues/lexicon.v0.1.json /app/spec/cues/lexicon.v0.1.json

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8080"]
