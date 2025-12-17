"""Celery configuration for background tasks."""
from celery import Celery
from celery.schedules import crontab
import os

# Initialize Celery
celery_app = Celery(
    'codex',
    broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    result_expires=3600,  # Results expire after 1 hour
)

# Scheduled tasks
celery_app.conf.beat_schedule = {
    # Update stock prices after market close (4:30 PM ET = 9:30 PM UTC)
    'update-stock-prices-daily': {
        'task': 'tasks.update_stock_prices',
        'schedule': crontab(hour=21, minute=30),
    },

    # Generate market alerts before market open (9:00 AM ET = 2:00 PM UTC)
    'generate-market-alerts-daily': {
        'task': 'tasks.generate_market_alerts',
        'schedule': crontab(hour=14, minute=0),
    },

    # Send weekly newsletter (Monday 7:00 AM ET = 12:00 PM UTC)
    'send-weekly-newsletter': {
        'task': 'tasks.send_newsletter',
        'schedule': crontab(day_of_week=1, hour=12, minute=0),
    },

    # Calculate portfolio performance daily (midnight)
    'calculate-portfolio-performance': {
        'task': 'tasks.calculate_all_portfolio_performance',
        'schedule': crontab(hour=0, minute=0),
    },

    # Cleanup old data (weekly, Sunday midnight)
    'cleanup-old-data': {
        'task': 'tasks.cleanup_old_data',
        'schedule': crontab(day_of_week=0, hour=0, minute=0),
    },
}

if __name__ == '__main__':
    celery_app.start()
