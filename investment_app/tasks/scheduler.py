# tasks/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from .jobs import (
    update_daily_prices,
    generate_daily_picks,
    send_daily_newsletter,
    send_weekly_portfolio_summaries,
    send_monthly_deep_dive
)

logger = logging.getLogger(__name__)

# Initialize scheduler
scheduler = BackgroundScheduler()

def init_scheduler(app):
    """
    Initialize and configure all scheduled jobs.
    Call this from your Flask app factory (app.py).
    """

    # Get tracked tickers from config or default list
    TRACKED_TICKERS = app.config.get('TRACKED_TICKERS', [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
        'NVDA', 'META', 'JPM', 'JNJ', 'V'
    ])

    # Daily jobs at 6 AM Eastern
    scheduler.add_job(
        func=lambda: update_daily_prices(TRACKED_TICKERS),
        trigger=CronTrigger(hour=6, minute=0, timezone='US/Eastern'),
        id='update_daily_prices',
        name='Update Daily Stock Prices',
        replace_existing=True
    )

    scheduler.add_job(
        func=generate_daily_picks,
        trigger=CronTrigger(hour=6, minute=5, timezone='US/Eastern'),
        id='generate_daily_picks',
        name='Generate Daily AI Stock Picks',
        replace_existing=True
    )

    scheduler.add_job(
        func=send_daily_newsletter,
        trigger=CronTrigger(hour=6, minute=10, timezone='US/Eastern'),
        id='send_daily_newsletter',
        name='Send Daily Newsletter',
        replace_existing=True
    )

    # Weekly job - Sunday at 6 PM
    scheduler.add_job(
        func=send_weekly_portfolio_summaries,
        trigger=CronTrigger(day_of_week='sun', hour=18, minute=0, timezone='US/Eastern'),
        id='weekly_portfolio_summaries',
        name='Send Weekly Portfolio Summaries',
        replace_existing=True
    )

    # Monthly job - 1st of month at 9 AM
    scheduler.add_job(
        func=send_monthly_deep_dive,
        trigger=CronTrigger(day=1, hour=9, minute=0, timezone='US/Eastern'),
        id='monthly_deep_dive',
        name='Send Monthly Deep Dive',
        replace_existing=True
    )

    # Start scheduler
    if not scheduler.running:
        scheduler.start()
        logger.info("Background scheduler started successfully")
        logger.info(f"Scheduled jobs: {len(scheduler.get_jobs())}")

    return scheduler


def shutdown_scheduler():
    """
    Gracefully shutdown the scheduler.
    """
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Background scheduler stopped")


def get_scheduled_jobs():
    """
    Get list of all scheduled jobs with their next run times.
    Useful for admin dashboard or debugging.
    """
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            'id': job.id,
            'name': job.name,
            'next_run': job.next_run_time.isoformat() if job.next_run_time else None,
            'trigger': str(job.trigger)
        })
    return jobs


def run_job_now(job_id):
    """
    Manually trigger a job immediately (for testing/admin).
    """
    try:
        job = scheduler.get_job(job_id)
        if job:
            job.func()
            logger.info(f"Manually executed job: {job_id}")
            return True
        else:
            logger.error(f"Job not found: {job_id}")
            return False
    except Exception as e:
        logger.error(f"Error running job {job_id}: {e}")
        return False
