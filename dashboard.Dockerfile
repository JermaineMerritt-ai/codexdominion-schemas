FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY codex_master_dashboard.py ./app.py
COPY codex_multi_cycle_orchestrator.py ./codex_multi_cycle_orchestrator.py
COPY codex_ledger.json ./codex_ledger.json
COPY accounts.json ./accounts.json
COPY proclamations.json ./proclamations.json
COPY cycles.json ./cycles.json

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
