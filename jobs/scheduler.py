# jobs/scheduler.py
"""
Dawn Dispatch Job Scheduler
Handles automated execution of daily metrics aggregation
"""

import schedule
import time
import datetime
import logging
import subprocess
import sys
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | SCHEDULER | %(levelname)s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('jobs/scheduler.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

def run_dawn_dispatch():
    """Execute dawn dispatch job"""
    try:
        logger.info("⏰ Scheduled Dawn Dispatch Starting")
        
        # Run dawn dispatch script
        result = subprocess.run([
            sys.executable, 
            'jobs/dawn_dispatch.py'
        ], 
        cwd=Path(__file__).parent.parent,
        capture_output=True, 
        text=True,
        timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            logger.info("✅ Dawn Dispatch completed successfully")
            logger.info(f"Output: {result.stdout}")
        else:
            logger.error(f"❌ Dawn Dispatch failed with code {result.returncode}")
            logger.error(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        logger.error("⏱️ Dawn Dispatch timed out after 5 minutes")
    except Exception as e:
        logger.error(f"💥 Error running Dawn Dispatch: {e}")

def run_api_health_check():
    """Check API health status"""
    try:
        import requests
        
        api_url = "http://127.0.0.1:8000/health"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ API Health OK - Status: {data.get('status')}")
        else:
            logger.warning(f"⚠️ API Health Warning - Status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        logger.warning("⚠️ API Health Check - API not running")
    except Exception as e:
        logger.error(f"❌ API Health Check failed: {e}")

def cleanup_logs():
    """Clean up old log files"""
    try:
        jobs_dir = Path("jobs")
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=7)
        
        cleaned = 0
        for log_file in jobs_dir.glob("*.log"):
            if log_file.stat().st_mtime < cutoff_date.timestamp():
                # Archive instead of delete
                archive_name = f"{log_file.stem}_{datetime.date.today().isoformat()}.log.old"
                log_file.rename(jobs_dir / archive_name)
                cleaned += 1
        
        if cleaned > 0:
            logger.info(f"📚 Archived {cleaned} old log files")
            
    except Exception as e:
        logger.error(f"Error during log cleanup: {e}")

def setup_schedule():
    """Setup job scheduling"""
    logger.info("📅 Setting up job schedule")
    
    # Daily dawn dispatch at 6:00 AM
    schedule.every().day.at("06:00").do(run_dawn_dispatch)
    
    # API health checks every hour during business hours
    schedule.every().hour.do(run_api_health_check)
    
    # Weekly log cleanup on Sundays at 2:00 AM
    schedule.every().sunday.at("02:00").do(cleanup_logs)
    
    logger.info("✅ Schedule configured:")
    logger.info("   📊 Dawn Dispatch: Daily at 6:00 AM")
    logger.info("   🏥 Health Checks: Every hour")
    logger.info("   🧹 Log Cleanup: Sundays at 2:00 AM")

def run_scheduler():
    """Main scheduler loop"""
    logger.info("🚀 Dawn Dispatch Scheduler Starting")
    
    setup_schedule()
    
    # Show next scheduled jobs
    logger.info("📋 Next scheduled jobs:")
    for job in schedule.get_jobs():
        logger.info(f"   {job}")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        logger.info("🛑 Scheduler stopped by user")
    except Exception as e:
        logger.error(f"💥 Scheduler error: {e}")

def run_manual_dispatch():
    """Run dawn dispatch manually for testing"""
    logger.info("🔧 Running manual Dawn Dispatch")
    run_dawn_dispatch()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "manual":
        run_manual_dispatch()
    else:
        run_scheduler()