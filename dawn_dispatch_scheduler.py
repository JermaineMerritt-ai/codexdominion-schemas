"""
🌅 DAWN DISPATCH SCHEDULER 👑
Automated scheduling system for daily Dawn Dispatches

The Merritt Method™ - Scheduled Digital Sovereignty
"""

import schedule
import time
import datetime
import sys
from pathlib import Path

# Add current directory to path
sys.path.append('.')

try:
    from codex_dawn_dispatch import CodexDawnDispatch, dawn_dispatch
    print("✅ Dawn Dispatch scheduler initialized!")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

class DawnDispatchScheduler:
    """
    🌅 Automated Dawn Dispatch Scheduler 👑
    
    Handles automatic scheduling and execution of dawn dispatches
    with configurable timing and error handling
    """
    
    def __init__(self):
        self.dawn_system = CodexDawnDispatch()
        self.config = self.dawn_system.config
        self.running = False
        
    def execute_dawn_dispatch(self):
        """Execute a scheduled dawn dispatch"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n🌅 Executing scheduled Dawn Dispatch at {timestamp}")
            
            result = self.dawn_system.dawn_dispatch()
            
            if result.get("success"):
                print("✅ Scheduled Dawn Dispatch completed successfully!")
                
                # Log success
                self._log_execution("SUCCESS", result.get("timestamp"))
                
            else:
                error_msg = result.get("error", "Unknown error")
                print(f"❌ Scheduled Dawn Dispatch failed: {error_msg}")
                
                # Log failure
                self._log_execution("FAILURE", result.get("timestamp"), error_msg)
                
        except Exception as e:
            error_msg = f"Scheduler execution error: {str(e)}"
            print(f"❌ {error_msg}")
            self._log_execution("ERROR", datetime.datetime.now().isoformat(), error_msg)
    
    def _log_execution(self, status: str, timestamp: str, error: str = None):
        """Log scheduler execution results"""
        try:
            log_file = Path("dawn_dispatch_scheduler.log")
            
            log_entry = {
                "timestamp": timestamp,
                "status": status,
                "scheduled_time": datetime.datetime.now().isoformat(),
                "error": error if error else None
            }
            
            # Append to log file
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"{datetime.datetime.now().isoformat()} - {status} - {error if error else 'OK'}\n")
                
        except Exception as e:
            print(f"⚠️ Failed to log execution: {str(e)}")
    
    def setup_schedule(self):
        """Setup the daily schedule based on configuration"""
        try:
            # Get schedule time from config
            schedule_time = self.config.get("dispatch_settings", {}).get("daily_schedule", "06:00")
            
            # Schedule daily execution
            schedule.every().day.at(schedule_time).do(self.execute_dawn_dispatch)
            
            print(f"⏰ Dawn Dispatch scheduled for {schedule_time} daily (UTC)")
            print("🔄 Scheduler is now running...")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup schedule: {str(e)}")
            return False
    
    def run_scheduler(self):
        """Run the scheduler loop"""
        if not self.setup_schedule():
            return
        
        self.running = True
        
        try:
            print("\n🌅 Dawn Dispatch Scheduler Active 👑")
            print("Press Ctrl+C to stop the scheduler...")
            print("-" * 50)
            
            while self.running:
                schedule.run_pending()
                
                # Show next scheduled run
                next_run = schedule.next_run()
                if next_run:
                    time_until = next_run - datetime.datetime.now()
                    hours, remainder = divmod(time_until.total_seconds(), 3600)
                    minutes, _ = divmod(remainder, 60)
                    
                    print(f"\r⏰ Next dispatch in: {int(hours):02d}h {int(minutes):02d}m", end="", flush=True)
                
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            print("\n\n🛑 Scheduler stopped by user")
            self.running = False
        except Exception as e:
            print(f"\n❌ Scheduler error: {str(e)}")
            self.running = False
        finally:
            print("🔥 Dawn Dispatch Scheduler terminated. 👑")
    
    def run_once_now(self):
        """Execute dawn dispatch immediately (for testing)"""
        print("🌅 Executing Dawn Dispatch immediately...")
        self.execute_dawn_dispatch()
    
    def show_schedule_info(self):
        """Display current schedule information"""
        try:
            config = self.config.get("dispatch_settings", {})
            
            print("\n📋 DAWN DISPATCH SCHEDULE INFO")
            print("=" * 40)
            print(f"⏰ Daily Time: {config.get('daily_schedule', 'Not set')}")
            print(f"🌐 Timezone: {config.get('timezone', 'UTC')}")
            print(f"📚 Archive: {'Enabled' if config.get('archive_enabled', True) else 'Disabled'}")
            print(f"📢 Auto Proclaim: {'Enabled' if config.get('auto_proclaim', False) else 'Disabled'}")
            
            # Show next scheduled runs
            jobs = schedule.get_jobs()
            if jobs:
                print(f"\n📅 Scheduled Jobs: {len(jobs)}")
                for i, job in enumerate(jobs, 1):
                    next_run = job.next_run
                    if next_run:
                        print(f"   {i}. Next run: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print("\n⚠️ No scheduled jobs found")
            
        except Exception as e:
            print(f"❌ Error showing schedule info: {str(e)}")

def main():
    """Main scheduler entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Dawn Dispatch Scheduler")
    parser.add_argument("--now", action="store_true", help="Execute dawn dispatch immediately")
    parser.add_argument("--info", action="store_true", help="Show schedule information")
    parser.add_argument("--schedule", action="store_true", help="Start the scheduler")
    
    args = parser.parse_args()
    
    scheduler = DawnDispatchScheduler()
    
    if args.now:
        scheduler.run_once_now()
    elif args.info:
        scheduler.show_schedule_info()
    elif args.schedule:
        scheduler.run_scheduler()
    else:
        # Interactive menu
        print("🌅 DAWN DISPATCH SCHEDULER 👑")
        print("=" * 40)
        print("1. Run Dawn Dispatch Now")
        print("2. Start Scheduled Runner")
        print("3. Show Schedule Info")
        print("4. Exit")
        
        try:
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == "1":
                scheduler.run_once_now()
            elif choice == "2":
                scheduler.run_scheduler()
            elif choice == "3":
                scheduler.show_schedule_info()
            elif choice == "4":
                print("👑 Goodbye!")
            else:
                print("❌ Invalid choice")
                
        except KeyboardInterrupt:
            print("\n👑 Goodbye!")

if __name__ == "__main__":
    main()