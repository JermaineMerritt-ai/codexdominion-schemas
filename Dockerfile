FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir flask flask-cors openai waitress redis

# Copy application
COPY dashboard_complete_fixed.py app.py
COPY codex_ledger.json .
COPY proclamations.json .
COPY cycles.json .

# Expose port
EXPOSE 80

# Run application
CMD ["python", "app.py"]
