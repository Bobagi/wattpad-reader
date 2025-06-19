FROM python:3.11-slim

WORKDIR /app

COPY main.py .

RUN pip install --no-cache-dir requests beautifulsoup4

CMD ["python", "main.py"]
