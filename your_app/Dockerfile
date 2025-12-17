# Multi-stage build for smaller image size
FROM python:3.12-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install packages system-wide instead of user
COPY --from=builder /usr/local /usr/local

# Copy application code
COPY . .

# Create non-root user (but run as root for now to avoid permission issues)
# RUN useradd -m -u 1000 codex && chown -R codex:codex /app
# USER codex

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5001/health')"

# Run with Gunicorn
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
