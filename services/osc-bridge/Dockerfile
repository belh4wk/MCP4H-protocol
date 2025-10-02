FROM python:3.11-slim
WORKDIR /app
RUN pip install paho-mqtt python-osc
COPY . .
CMD ["python","main.py"]
