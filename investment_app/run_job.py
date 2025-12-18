#!/usr/bin/env python
"""
Cron Job Runner
Execute scheduled tasks from command line or cron

Usage:
    python run_job.py <job_name>

Examples:
    python run_job.py update_daily_prices
    python run_job.py generate_daily_picks
    python run_job.py send_daily_newsletter
    python run_job.py send_weekly_portfolio_summaries
    python run_job.py send_monthly_deep_dive
"""
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from tasks.jobs import (
    update_daily_prices,
    generate_daily_picks,
    send_daily_newsletter,
    send_weekly_portfolio_summaries,
    send_monthly_deep_dive
)

# Default ticker list for price updates
DEFAULT_TICKERS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
    'NVDA', 'META', 'JPM', 'JNJ', 'V'
]

# Job registry
JOBS = {
    'update_daily_prices': lambda: update_daily_prices(DEFAULT_TICKERS),
    'generate_daily_picks': generate_daily_picks,
    'send_daily_newsletter': send_daily_newsletter,
    'send_weekly_portfolio_summaries': send_weekly_portfolio_summaries,
    'send_monthly_deep_dive': send_monthly_deep_dive
}


def log(message, level='INFO'):
    """Simple logging function"""
    timestamp = datetime.utcnow().isoformat()
    print(f"[{timestamp}] {level}: {message}", flush=True)


def run_job(job_name):
    """Execute a scheduled job by name"""
    if job_name not in JOBS:
        log(f"Unknown job: {job_name}", 'ERROR')
        log(f"Available jobs: {', '.join(JOBS.keys())}", 'ERROR')
        return False

    log(f"Starting job: {job_name}")

    # Create Flask app and context
    app = create_app()

    try:
        with app.app_context():
            # Execute the job
            result = JOBS[job_name]()

            log(f"Job completed: {job_name}", 'SUCCESS')
            if result:
                log(f"Result: {result}")

            return True

    except Exception as e:
        log(f"Job failed: {job_name}", 'ERROR')
        log(f"Error: {str(e)}", 'ERROR')

        # Print full traceback for debugging
        import traceback
        traceback.print_exc()

        return False


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        log("Usage: python run_job.py <job_name>", 'ERROR')
        log(f"Available jobs: {', '.join(JOBS.keys())}", 'INFO')
        sys.exit(1)

    job_name = sys.argv[1]

    success = run_job(job_name)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
