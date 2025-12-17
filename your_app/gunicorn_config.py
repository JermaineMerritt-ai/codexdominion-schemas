"""Gunicorn configuration for production deployment."""
import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '5001')}"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000  # Restart workers after 1000 requests (prevent memory leaks)
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Restart workers gracefully
graceful_timeout = 30
preload_app = True

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = os.getenv('LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "codex-portfolio"

# Server hooks
def on_starting(server):
    """Called just before the master process is initialized."""
    print("🔥 Starting Gunicorn server...")

def on_reload(server):
    """Called when a worker is reloaded."""
    print("♻️  Reloading worker...")

def worker_int(worker):
    """Called when a worker receives SIGINT or SIGQUIT."""
    print(f"💤 Worker {worker.pid} shutting down...")

def worker_abort(worker):
    """Called when a worker receives SIGABRT."""
    print(f"⚠️  Worker {worker.pid} aborted!")
