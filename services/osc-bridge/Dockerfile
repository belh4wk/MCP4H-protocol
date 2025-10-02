FROM python:3.11-slim
WORKDIR /app
# Copy service code
COPY services/osc-bridge/ /app/
# Install deps only if a requirements.txt exists
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi
CMD ["python","main.py"]
