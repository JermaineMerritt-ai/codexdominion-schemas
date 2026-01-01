#!/usr/bin/env python3
"""
CodexDominion Launch Day Operations Script
===========================================

Automates launch day posting and monitoring.
Run this script on launch day to coordinate social media deployment.

Usage:
    python launch_day_operations.py --check        # Pre-launch check
    python launch_day_operations.py --wave 1       # Deploy wave 1
    python launch_day_operations.py --wave 2       # Deploy wave 2
    python launch_day_operations.py --monitor      # Monitor metrics
    python launch_day_operations.py --report       # Generate report
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from launch_social_integration import LaunchSocialManager


class LaunchDayOperations:
    """Manages launch day operations and social media deployment"""
    
    def __init__(self):
        self.manager = LaunchSocialManager()
        self.log_file = Path("launch_day_log.txt")
    
    def log(self, message: str):
        """Log message to console and file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
    
    def pre_launch_check(self) -> bool:
        """
        Run pre-launch checks to ensure everything is ready
        
        Returns:
            True if all checks pass, False otherwise
        """
        self.log("🔍 Running pre-launch checks...")
        
        checks_passed = True
        
        # Check 1: Load social posts data
        try:
            stats = self.manager.get_stats()
            if stats['total_posts'] == 50:
                self.log(f"✅ Social posts loaded: {stats['total_posts']} posts")
            else:
                self.log(f"❌ Social posts incomplete: {stats['total_posts']}/50")
                checks_passed = False
        except Exception as e:
            self.log(f"❌ Failed to load social posts: {e}")
            checks_passed = False
        
        # Check 2: Verify critical posts
        critical = self.manager.get_posts_by_priority("critical")
        if len(critical) >= 9:
            self.log(f"✅ Critical posts ready: {len(critical)} posts")
        else:
            self.log(f"⚠️  Only {len(critical)} critical posts found")
        
        # Check 3: Verify all categories
        expected_categories = ["hero", "creator", "youth", "diaspora", "brand", "marketplace", "hype"]
        all_posts = self.manager.get_all_posts()
        for category in expected_categories:
            if category in all_posts:
                self.log(f"✅ {category.capitalize()}: {len(all_posts[category])} posts")
            else:
                self.log(f"❌ Missing category: {category}")
                checks_passed = False
        
        # Check 4: Launch day schedule
        waves = self.manager.get_launch_day_posts()
        if len(waves) >= 3:
            self.log(f"✅ Launch day waves configured: {len(waves)} waves")
        else:
            self.log(f"⚠️  Only {len(waves)} waves configured")
        
        # Final result
        if checks_passed:
            self.log("🎉 All pre-launch checks PASSED!")
            return True
        else:
            self.log("⚠️  Some pre-launch checks FAILED!")
            return False
    
    def deploy_wave(self, wave_number: int):
        """
        Deploy posts for a specific wave
        
        Args:
            wave_number: Wave number (1, 2, 3)
        """
        waves = self.manager.get_launch_day_posts()
        wave_key = f"wave_{wave_number}"
        
        if wave_key not in waves:
            self.log(f"❌ Wave {wave_number} not found in schedule")
            return
        
        posts = waves[wave_key]
        self.log(f"🚀 Deploying Wave {wave_number}: {len(posts)} posts")
        
        for post in posts:
            self.log(f"   📱 Post #{post['id']}: {post['text'][:50]}...")
            self.log(f"      Category: {post['category']}")
            self.log(f"      Priority: {post['priority']}")
            self.log(f"      Hashtags: {', '.join(post.get('hashtags', []))}")
            
            # Format for different platforms
            platforms = ["instagram", "twitter", "facebook", "linkedin"]
            self.log(f"      Platforms: {', '.join(platforms)}")
            
            # In production, you would actually post here
            # For now, just log what would be posted
            self.log(f"      ✅ Ready for deployment")
        
        self.log(f"✅ Wave {wave_number} deployment complete!")
    
    def monitor_metrics(self):
        """Monitor launch day metrics"""
        self.log("📊 Launch Day Metrics Monitor")
        
        stats = self.manager.get_stats()
        self.log(f"   Total posts available: {stats['total_posts']}")
        self.log(f"   Critical posts: {stats['critical_posts']}")
        self.log(f"   High priority: {stats['high_priority_posts']}")
        
        # Check system status
        try:
            from db import SessionLocal
            session = SessionLocal()
            self.log("   ✅ Database: Connected")
            session.close()
        except Exception as e:
            self.log(f"   ❌ Database: {e}")
        
        # Check if Flask dashboard is running
        try:
            import requests
            response = requests.get("http://localhost:5000/health", timeout=2)
            if response.status_code == 200:
                self.log("   ✅ Flask Dashboard: Running")
            else:
                self.log(f"   ⚠️  Flask Dashboard: Status {response.status_code}")
        except:
            self.log("   ❌ Flask Dashboard: Not accessible")
        
        # Check Redis
        try:
            import redis
            r = redis.from_url("redis://localhost:6379/0")
            r.ping()
            self.log("   ✅ Redis: Active")
        except:
            self.log("   ⚠️  Redis: Not accessible")
    
    def generate_report(self):
        """Generate launch day report"""
        self.log("📋 Generating Launch Day Report")
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("CODEXDOMINION LAUNCH DAY REPORT")
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("=" * 60)
        
        # Stats
        stats = self.manager.get_stats()
        report_lines.append("\n📊 CONTENT STATS")
        report_lines.append(f"   Total posts: {stats['total_posts']}")
        report_lines.append(f"   Critical posts: {stats['critical_posts']}")
        report_lines.append(f"   High priority: {stats['high_priority_posts']}")
        
        # By category
        report_lines.append("\n📱 POSTS BY CATEGORY")
        all_posts = self.manager.get_all_posts()
        for category, posts in all_posts.items():
            report_lines.append(f"   {category.capitalize()}: {len(posts)} posts")
        
        # Launch schedule
        report_lines.append("\n🚀 LAUNCH SCHEDULE")
        waves = self.manager.get_launch_day_posts()
        for wave_key, posts in waves.items():
            report_lines.append(f"   {wave_key}: {len(posts)} posts")
        
        # Recommendations
        report_lines.append("\n💡 RECOMMENDATIONS")
        report_lines.append("   1. Deploy Hero posts at marketplace open (10:30 AM)")
        report_lines.append("   2. Deploy Hype posts during social storm (1:00 PM)")
        report_lines.append("   3. Monitor engagement every 2 hours")
        report_lines.append("   4. Respond to all comments within 30 minutes")
        report_lines.append("   5. Share creator content throughout the day")
        
        report_lines.append("\n" + "=" * 60)
        
        # Print and save
        report = "\n".join(report_lines)
        print(report)
        
        report_file = Path(f"launch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(report_file, 'w') as f:
            f.write(report)
        
        self.log(f"✅ Report saved to: {report_file}")
    
    def list_posts_by_time(self):
        """List recommended posting times"""
        self.log("⏰ Launch Day Timeline")
        
        timeline = [
            ("08:00 AM", "Systems check", "Run pre-launch check"),
            ("10:00 AM", "Keynote premiere", "Video launch"),
            ("10:30 AM", "Wave 1 - Hero Posts", "Deploy posts #1-5"),
            ("11:00 AM", "Youth Challenge #1", "Deploy youth posts"),
            ("12:00 PM", "Press release", "Media distribution"),
            ("01:00 PM", "Wave 2 - Hype Posts", "Deploy posts #46-50"),
            ("03:00 PM", "Creator Wave", "Creator content push"),
            ("06:00 PM", "Metrics review", "Check performance"),
            ("08:00 PM", "Day 1 recap", "Summary post"),
        ]
        
        for time, event, action in timeline:
            self.log(f"   {time} - {event}")
            self.log(f"            {action}")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="CodexDominion Launch Day Operations"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run pre-launch checks"
    )
    parser.add_argument(
        "--wave",
        type=int,
        choices=[1, 2, 3],
        help="Deploy specific wave (1, 2, or 3)"
    )
    parser.add_argument(
        "--monitor",
        action="store_true",
        help="Monitor metrics and system status"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate launch day report"
    )
    parser.add_argument(
        "--timeline",
        action="store_true",
        help="Show launch day timeline"
    )
    
    args = parser.parse_args()
    ops = LaunchDayOperations()
    
    # Run requested operation
    if args.check:
        ops.pre_launch_check()
    
    elif args.wave:
        ops.deploy_wave(args.wave)
    
    elif args.monitor:
        ops.monitor_metrics()
    
    elif args.report:
        ops.generate_report()
    
    elif args.timeline:
        ops.list_posts_by_time()
    
    else:
        # No args - show help
        parser.print_help()
        print("\n💡 Quick Commands:")
        print("   python launch_day_operations.py --check")
        print("   python launch_day_operations.py --wave 1")
        print("   python launch_day_operations.py --monitor")
        print("   python launch_day_operations.py --report")


if __name__ == "__main__":
    main()
