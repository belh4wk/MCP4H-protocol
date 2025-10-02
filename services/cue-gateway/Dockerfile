FROM python:3.11-slim

WORKDIR /app

# Copy app code
COPY services/cue-gateway/ /app/

# Install requirements if present
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Copy spec files from repo root (compose context is project root)
RUN mkdir -p /app/spec/cues
COPY spec/cues/cue.schema.json /app/spec/cues/cue.schema.json
COPY spec/cues/lexicon.v0.1.json /app/spec/cues/lexicon.v0.1.json

EXPOSE 8080
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8080"]
