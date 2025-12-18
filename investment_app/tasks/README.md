# Scheduled Tasks

Automated background jobs for the investment platform.

## Job Schedule

### Daily (6:00 AM ET)
- **6:00** - `update_daily_prices()` - Fetch latest stock prices
- **6:05** - `generate_daily_picks()` - Generate AI stock picks
- **6:10** - `send_daily_newsletter()` - Email picks to subscribers

### Weekly (Sunday 6:00 PM ET)
- **18:00** - `send_weekly_portfolio_summaries()` - Portfolio health checks

### Monthly (1st at 9:00 AM ET)
- **09:00** - `send_monthly_deep_dive()` - Macro analysis & strategy

## Setup

### 1. Install APScheduler
```bash
pip install apscheduler
```

### 2. Initialize in Flask App
```python
# In app.py create_app()
from tasks import init_scheduler, shutdown_scheduler

def create_app():
    app = Flask(__name__)
    # ... other setup ...

    # Initialize scheduler
    with app.app_context():
        init_scheduler(app)

    # Cleanup on shutdown
    import atexit
    atexit.register(shutdown_scheduler)

    return app
```

### 3. Configuration
Add to `config.py`:
```python
TRACKED_TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
                   'NVDA', 'META', 'JPM', 'JNJ', 'V']
```

## Manual Job Execution

For testing or admin purposes:
```python
from tasks import run_job_now

# Trigger any job manually
run_job_now('update_daily_prices')
run_job_now('generate_daily_picks')
run_job_now('send_daily_newsletter')
```

## Admin Dashboard Route

Add to your admin routes:
```python
from tasks import get_scheduled_jobs

@admin_bp.route('/jobs')
def view_jobs():
    jobs = get_scheduled_jobs()
    return render_template('admin/jobs.html', jobs=jobs)
```

## Job Details

### `update_daily_prices(tickers)`
Fetches OHLC + volume data for all tracked stocks and stores in `DailyPrices` table.

### `generate_daily_picks()`
Uses AI to analyze curated stock universe and select 3 top picks with reasoning. Saves to `DailyPicks` table.

### `send_daily_newsletter()`
Retrieves latest picks and emails to all subscribers with `daily_picks` segment.

### `send_weekly_portfolio_summaries()`
Generates AI-powered portfolio health analysis for each user and emails them.

### `send_monthly_deep_dive()`
Sends comprehensive macro analysis, sector trends, and strategic allocations to subscribers.

## Production Considerations

- **Timezone**: All jobs use `US/Eastern` timezone
- **Error Handling**: Jobs log errors but don't crash the app
- **Idempotency**: Jobs check for existing data to avoid duplicates
- **Rate Limits**: Respect API rate limits when fetching stock data
- **Email Limits**: Consider batching emails to avoid provider limits

## Monitoring

Check logs for job execution:
```bash
grep "Background scheduler" app.log
grep "job" app.log
```

## Troubleshooting

**Jobs not running?**
- Check `scheduler.running` status
- Verify timezone configuration
- Check app context is available
- Review error logs

**Duplicate data?**
- Jobs check for existing records
- Use unique constraints in DB models
- Add date-based filtering in job logic
