FROM python:3.11-slim
WORKDIR /app
COPY services/cue-gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY spec/cues/cue.schema.json /app/spec/cues/cue.schema.json
COPY spec/cues/lexicon.v0.1.json /app/spec/cues/lexicon.v0.1.json
COPY services/cue-gateway/ .
EXPOSE 8080
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8080"]
