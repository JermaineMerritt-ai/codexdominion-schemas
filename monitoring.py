"""
📊 Monitoring & Logging Module
================================
System metrics, error tracking, and logging configuration
"""

import os
import logging
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime
from functools import wraps
import time
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from flask import request, g
from prometheus_client import Counter, Histogram, Gauge
from db import SessionLocal
from models import Workflow

# Environment configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "detailed")
SENTRY_DSN = os.getenv("SENTRY_DSN")
SENTRY_ENABLED = os.getenv("SENTRY_ENABLED", "false").lower() == "true"

# =============================================================================
# Sentry Error Tracking
# =============================================================================

def init_sentry():
    """Initialize Sentry error tracking"""
    if SENTRY_ENABLED and SENTRY_DSN:
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            environment=ENVIRONMENT,
            integrations=[
                FlaskIntegration(),
                RedisIntegration(),
                SqlalchemyIntegration(),
            ],
            traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.1")),
            profiles_sample_rate=float(os.getenv("SENTRY_PROFILES_SAMPLE_RATE", "0.1")),
            before_send=filter_sensitive_data,
        )
        print(f"✅ Sentry initialized for {ENVIRONMENT}")
    else:
        print("ℹ️  Sentry disabled")


def filter_sensitive_data(event, hint):
    """Filter sensitive data from Sentry events"""
    # Remove passwords, tokens, API keys
    if 'request' in event:
        if 'data' in event['request']:
            data = event['request']['data']
            if isinstance(data, dict):
                for key in ['password', 'token', 'api_key', 'secret']:
                    if key in data:
                        data[key] = '[FILTERED]'
        
        if 'headers' in event['request']:
            headers = event['request']['headers']
            for key in ['Authorization', 'X-Api-Key']:
                if key in headers:
                    headers[key] = '[FILTERED]'
    
    return event


# =============================================================================
# Prometheus Metrics
# =============================================================================

# Request metrics
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

# Workflow metrics
workflow_created = Counter(
    'workflow_created_total',
    'Total workflows created',
    ['workflow_type']
)

workflow_completed = Counter(
    'workflow_completed_total',
    'Total workflows completed',
    ['workflow_type']
)

workflow_failed = Counter(
    'workflow_failed_total',
    'Total workflows failed',
    ['workflow_type']
)

workflow_duration = Histogram(
    'workflow_duration_seconds',
    'Workflow execution duration in seconds',
    ['workflow_type']
)

# Queue metrics
queue_length = Gauge(
    'rq_queue_length',
    'Number of jobs in RQ queue',
    ['queue_name']
)

# Database metrics
db_connections = Gauge(
    'db_connections_active',
    'Number of active database connections'
)

db_query_duration = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['query_type']
)


def track_request_metrics(f):
    """Decorator to track request metrics"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        
        try:
            response = f(*args, **kwargs)
            status = response.status_code if hasattr(response, 'status_code') else 200
            
            # Record metrics
            request_count.labels(
                method=request.method,
                endpoint=request.endpoint,
                status=status
            ).inc()
            
            request_duration.labels(
                method=request.method,
                endpoint=request.endpoint
            ).observe(time.time() - start_time)
            
            return response
        except Exception as e:
            request_count.labels(
                method=request.method,
                endpoint=request.endpoint,
                status=500
            ).inc()
            raise
    
    return decorated_function


def update_queue_metrics():
    """Update RQ queue length metrics"""
    try:
        from rq import Queue
        from redis import Redis
        
        redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
        workflows_queue = Queue("workflows", connection=redis_conn)
        
        queue_length.labels(queue_name="workflows").set(len(workflows_queue))
    except Exception as e:
        print(f"⚠️  Failed to update queue metrics: {e}")


def update_workflow_metrics():
    """Update workflow completion metrics from database"""
    try:
        session = SessionLocal()
        
        # Count workflows by status
        pending = session.query(Workflow).filter(Workflow.status == "pending").count()
        running = session.query(Workflow).filter(Workflow.status == "running").count()
        completed = session.query(Workflow).filter(Workflow.status == "completed").count()
        failed = session.query(Workflow).filter(Workflow.status == "failed").count()
        
        # Update gauges (create if needed)
        from prometheus_client import Gauge
        
        workflow_status = Gauge('workflow_status_count', 'Workflow count by status', ['status'])
        workflow_status.labels(status='pending').set(pending)
        workflow_status.labels(status='running').set(running)
        workflow_status.labels(status='completed').set(completed)
        workflow_status.labels(status='failed').set(failed)
        
        session.close()
    except Exception as e:
        print(f"⚠️  Failed to update workflow metrics: {e}")


# =============================================================================
# Logging Configuration
# =============================================================================

def setup_logging(app):
    """Configure application logging"""
    # Set log level
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    app.logger.setLevel(log_level)
    
    # Remove default handlers
    app.logger.handlers.clear()
    
    # JSON formatter for production
    if LOG_FORMAT == "json":
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
    
    # Console handler (stdout)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)
    
    # File handler (rotating)
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    file_handler = RotatingFileHandler(
        'logs/codex.log',
        maxBytes=10_000_000,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    
    # Error file handler
    error_handler = RotatingFileHandler(
        'logs/errors.log',
        maxBytes=10_000_000,
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    app.logger.addHandler(error_handler)
    
    print(f"✅ Logging configured: level={LOG_LEVEL}, format={LOG_FORMAT}")


class JsonFormatter(logging.Formatter):
    """JSON log formatter for structured logging"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        
        return json.dumps(log_data)


# =============================================================================
# Health Check Endpoint
# =============================================================================

def get_system_health():
    """Get system health status"""
    health = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": ENVIRONMENT,
        "checks": {}
    }
    
    # Database check
    try:
        from db import SessionLocal
        session = SessionLocal()
        session.execute("SELECT 1")
        session.close()
        health["checks"]["database"] = "healthy"
    except Exception as e:
        health["checks"]["database"] = f"unhealthy: {str(e)}"
        health["status"] = "degraded"
    
    # Redis check
    try:
        from redis import Redis
        redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
        redis_conn.ping()
        health["checks"]["redis"] = "healthy"
    except Exception as e:
        health["checks"]["redis"] = f"unhealthy: {str(e)}"
        health["status"] = "degraded"
    
    # RQ queue check
    try:
        from rq import Queue
        from redis import Redis
        redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
        queue = Queue("workflows", connection=redis_conn)
        health["checks"]["rq_queue"] = {
            "status": "healthy",
            "length": len(queue)
        }
    except Exception as e:
        health["checks"]["rq_queue"] = f"unhealthy: {str(e)}"
    
    return health


# Add to flask_dashboard.py:
"""
from monitoring import init_sentry, setup_logging, get_system_health, track_request_metrics
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Initialize monitoring
init_sentry()
setup_logging(app)

# Prometheus metrics endpoint
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

@app.route('/health')
def health_check():
    return jsonify(get_system_health())

# Track metrics on all routes
@app.before_request
def before_request_metrics():
    g.start_time = time.time()

@app.after_request
@track_request_metrics
def after_request_metrics(response):
    return response
"""
