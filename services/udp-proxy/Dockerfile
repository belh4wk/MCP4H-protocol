FROM python:3.11-slim
WORKDIR /app
COPY services/udp-proxy/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/udp-proxy/ .
EXPOSE 20777/udp
CMD ["python","main.py"]
