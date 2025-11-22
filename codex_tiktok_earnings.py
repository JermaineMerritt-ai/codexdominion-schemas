"""
🔥 CODEX TIKTOK EARNINGS SYSTEM 👑
Advanced TikTok Creator Program Analytics and Revenue Tracking

The Merritt Method™ - Digital Creator Sovereignty
"""

import os
import datetime
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging
import requests
from urllib.parse import urlencode

class CodexTikTokEarnings:
    """
    🔥 Sacred TikTok Earnings Management System 👑
    
    Comprehensive TikTok Creator Program integration for the Codex Dominion:
    - Creator Fund analytics and earnings
    - Live Gift and virtual gift tracking
    - Creator Program payouts monitoring
    - Audience engagement metrics
    - Revenue stream analysis
    - Archive management system
    """
    
    def __init__(self, config_file: str = "tiktok_config.json"):
        """Initialize the TikTok Earnings System"""
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.token = self.config.get("tiktok", {}).get("token") or os.getenv("TIKTOK_TOKEN")
        self.user_id = self.config.get("tiktok", {}).get("user_id", "")
        self.archive_file = Path("ledger_tiktok.jsonl")
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # API endpoints (using placeholder/third-party services)
        self.api_base = self.config.get("tiktok", {}).get("api_base", "https://api.tiktok-analytics.example")
        self.backup_apis = self.config.get("tiktok", {}).get("backup_apis", [
            "https://tiktok-creator-api.example.com",
            "https://social-analytics.example.net/tiktok"
        ])
    
    def _load_config(self) -> Dict[str, Any]:
        """Load TikTok configuration from JSON file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Create default config
                default_config = {
                    "tiktok": {
                        "token": "YOUR_TIKTOK_TOKEN_HERE",
                        "user_id": "YOUR_USER_ID_HERE",
                        "api_base": "https://api.tiktok-analytics.example",
                        "backup_apis": [
                            "https://tiktok-creator-api.example.com",
                            "https://social-analytics.example.net/tiktok"
                        ]
                    },
                    "earnings_settings": {
                        "track_creator_fund": True,
                        "track_live_gifts": True,
                        "track_brand_partnerships": True,
                        "currency": "USD",
                        "auto_archive": True,
                        "payout_threshold": 10.0
                    },
                    "analytics_settings": {
                        "track_engagement": True,
                        "track_growth": True,
                        "competitor_analysis": False,
                        "export_format": "json",
                        "alert_thresholds": {
                            "earnings_milestone": 100.0,
                            "follower_milestone": 1000,
                            "view_spike": 100000,
                            "engagement_drop": 0.05
                        }
                    },
                    "content_settings": {
                        "auto_tag_earnings": True,
                        "track_viral_content": True,
                        "monetization_insights": True,
                        "performance_categories": ["dance", "comedy", "educational", "lifestyle"]
                    }
                }
                
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2)
                
                return default_config
                
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            return {}
    
    def tiktok_metrics(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Enhanced TikTok metrics collection with earnings focus
        
        Args:
            user_id: Optional user ID, uses configured default if not provided
            
        Returns:
            Dictionary with comprehensive TikTok metrics and earnings data
        """
        target_user = user_id or self.user_id
        
        if not target_user or target_user == "YOUR_USER_ID_HERE":
            return self._generate_demo_metrics()
        
        try:
            # Try primary API first
            metrics = self._fetch_from_primary_api(target_user)
            
            if metrics.get("error") and self.backup_apis:
                # Try backup APIs
                for backup_api in self.backup_apis:
                    try:
                        backup_metrics = self._fetch_from_backup_api(backup_api, target_user)
                        if not backup_metrics.get("error"):
                            metrics = backup_metrics
                            break
                    except Exception as e:
                        self.logger.warning(f"Backup API failed: {str(e)}")
            
            # Enhance with calculated metrics
            enhanced_metrics = self._enhance_metrics(metrics)
            
            self.logger.info(f"Retrieved TikTok metrics for user: {target_user}")
            return enhanced_metrics
            
        except Exception as e:
            self.logger.error(f"Error retrieving TikTok metrics: {str(e)}")
            return {"error": str(e), "followers": 0, "views": 0, "payouts": 0}
    
    def _fetch_from_primary_api(self, user_id: str) -> Dict[str, Any]:
        """Fetch metrics from primary TikTok API"""
        try:
            if not self.token or self.token == "YOUR_TIKTOK_TOKEN_HERE":
                return self._generate_demo_metrics()
            
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "User-Agent": "CodexDominion-TikTokEarnings/1.0"
            }
            
            # Primary metrics endpoint
            url = f"{self.api_base}/metrics?uid={user_id}"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "followers": data.get("followers", 0),
                    "views": data.get("views", 0),
                    "payouts": data.get("creator_payouts", 0),
                    "likes": data.get("likes", 0),
                    "shares": data.get("shares", 0),
                    "comments": data.get("comments", 0),
                    "live_gifts": data.get("live_gifts", 0),
                    "creator_fund": data.get("creator_fund_earnings", 0),
                    "brand_partnerships": data.get("brand_partnerships", 0),
                    "video_count": data.get("video_count", 0),
                    "source": "primary_api"
                }
            else:
                return {"error": f"API returned status {response.status_code}"}
                
        except requests.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def _fetch_from_backup_api(self, api_url: str, user_id: str) -> Dict[str, Any]:
        """Fetch metrics from backup API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            url = f"{api_url}/user/{user_id}/metrics"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # Normalize backup API response
                return {
                    "followers": data.get("follower_count", 0),
                    "views": data.get("total_views", 0),
                    "payouts": data.get("total_earnings", 0),
                    "likes": data.get("total_likes", 0),
                    "shares": data.get("total_shares", 0),
                    "comments": data.get("total_comments", 0),
                    "live_gifts": data.get("gift_earnings", 0),
                    "creator_fund": data.get("fund_earnings", 0),
                    "brand_partnerships": data.get("partnership_earnings", 0),
                    "video_count": data.get("videos", 0),
                    "source": "backup_api"
                }
            else:
                return {"error": f"Backup API returned status {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Backup API error: {str(e)}"}
    
    def _generate_demo_metrics(self) -> Dict[str, Any]:
        """Generate demo metrics when API is not available"""
        import random
        
        # Generate realistic demo data
        base_followers = 12500
        base_views = 850000
        base_earnings = 245.75
        
        # Add some realistic variation
        followers = base_followers + random.randint(-500, 1000)
        views = base_views + random.randint(-50000, 100000)
        earnings = round(base_earnings + random.uniform(-50, 100), 2)
        
        return {
            "followers": followers,
            "views": views,
            "payouts": earnings,
            "likes": int(views * 0.08),  # ~8% engagement rate
            "shares": int(views * 0.02),  # ~2% share rate
            "comments": int(views * 0.015),  # ~1.5% comment rate
            "live_gifts": round(earnings * 0.3, 2),  # 30% from gifts
            "creator_fund": round(earnings * 0.4, 2),  # 40% from creator fund
            "brand_partnerships": round(earnings * 0.3, 2),  # 30% from partnerships
            "video_count": 156,
            "source": "demo_data",
            "demo": True
        }
    
    def _enhance_metrics(self, base_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance base metrics with calculated values"""
        try:
            followers = base_metrics.get("followers", 0)
            views = base_metrics.get("views", 0)
            likes = base_metrics.get("likes", 0)
            video_count = base_metrics.get("video_count", 1)
            payouts = base_metrics.get("payouts", 0)
            
            # Calculate engagement metrics
            engagement_rate = (likes / views * 100) if views > 0 else 0
            avg_views_per_video = views // video_count if video_count > 0 else 0
            views_per_follower = views / followers if followers > 0 else 0
            
            # Calculate earnings metrics
            earnings_per_view = (payouts / views * 1000) if views > 0 else 0  # Per 1K views
            earnings_per_follower = payouts / followers if followers > 0 else 0
            
            # Calculate creator score (0-100)
            creator_score = self._calculate_creator_score(base_metrics)
            
            # Get historical comparison if available
            growth_metrics = self._calculate_growth_metrics()
            
            enhanced = {
                **base_metrics,
                "engagement_rate": round(engagement_rate, 2),
                "avg_views_per_video": avg_views_per_video,
                "views_per_follower": round(views_per_follower, 1),
                "earnings_per_1k_views": round(earnings_per_view, 4),
                "earnings_per_follower": round(earnings_per_follower, 4),
                "creator_score": creator_score,
                "last_updated": datetime.datetime.utcnow().isoformat(),
                **growth_metrics
            }
            
            return enhanced
            
        except Exception as e:
            self.logger.error(f"Error enhancing metrics: {str(e)}")
            return base_metrics
    
    def _calculate_creator_score(self, metrics: Dict[str, Any]) -> int:
        """Calculate overall creator performance score (0-100)"""
        try:
            followers = metrics.get("followers", 0)
            engagement_rate = (metrics.get("likes", 0) / metrics.get("views", 1)) * 100
            payouts = metrics.get("payouts", 0)
            
            # Scoring algorithm for TikTok creators
            follower_score = min(followers / 50000 * 30, 30)  # Max 30 points for 50K+ followers
            engagement_score = min(engagement_rate * 3, 40)    # Max 40 points for ~13% engagement
            earnings_score = min(payouts / 500 * 30, 30)       # Max 30 points for $500+ earnings
            
            total_score = follower_score + engagement_score + earnings_score
            return min(int(total_score), 100)
            
        except Exception:
            return 0
    
    def _calculate_growth_metrics(self) -> Dict[str, Any]:
        """Calculate growth trends from historical data"""
        try:
            history = self.get_archive_history(30)  # Last 30 entries
            
            if len(history) < 2:
                return {
                    "follower_growth": 0,
                    "earnings_growth": 0,
                    "view_growth": 0,
                    "trend_direction": "stable"
                }
            
            # Get previous metrics (7 days ago if available)
            recent = history[-1] if history else {}
            previous = history[-7] if len(history) >= 7 else history[0]
            
            current_followers = recent.get("followers", 0)
            previous_followers = previous.get("followers", 0)
            
            current_earnings = recent.get("payouts", 0)
            previous_earnings = previous.get("payouts", 0)
            
            current_views = recent.get("views", 0)
            previous_views = previous.get("views", 0)
            
            follower_growth = current_followers - previous_followers
            earnings_growth = round(current_earnings - previous_earnings, 2)
            view_growth = current_views - previous_views
            
            # Determine trend direction
            if follower_growth > 0 and earnings_growth > 0:
                trend_direction = "growing"
            elif follower_growth < 0 or earnings_growth < 0:
                trend_direction = "declining"
            else:
                trend_direction = "stable"
            
            return {
                "follower_growth": follower_growth,
                "earnings_growth": earnings_growth,
                "view_growth": view_growth,
                "trend_direction": trend_direction,
                "growth_rate": round((follower_growth / previous_followers * 100), 2) if previous_followers > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating growth metrics: {str(e)}")
            return {
                "follower_growth": 0,
                "earnings_growth": 0,
                "view_growth": 0,
                "trend_direction": "unknown"
            }
    
    def archive_tiktok(self, report: Dict[str, Any]) -> bool:
        """
        Enhanced TikTok archive system with earnings tracking
        
        Args:
            report: TikTok metrics report to archive
            
        Returns:
            bool: True if archived successfully
        """
        try:
            # Prepare archive entry
            archive_entry = {
                "ts": datetime.datetime.utcnow().isoformat(),
                "type": "tiktok_earnings",
                **report
            }
            
            # Append to JSONL file
            with open(self.archive_file, "a", encoding='utf-8') as f:
                f.write(json.dumps(archive_entry, ensure_ascii=False) + "\n")
            
            self.logger.info("TikTok earnings metrics archived successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error archiving TikTok report: {str(e)}")
            return False
    
    def get_archive_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get TikTok archive history"""
        try:
            if not self.archive_file.exists():
                return []
            
            history = []
            with open(self.archive_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        history.append(entry)
                    except json.JSONDecodeError:
                        continue
            
            # Return most recent entries
            return history[-limit:] if limit else history
            
        except Exception as e:
            self.logger.error(f"Error reading archive history: {str(e)}")
            return []
    
    def get_earnings_summary(self) -> Dict[str, Any]:
        """Get comprehensive TikTok earnings summary"""
        try:
            # Get current metrics
            current_metrics = self.tiktok_metrics()
            
            if current_metrics.get("error"):
                return current_metrics
            
            # Get historical data for earnings analysis
            history = self.get_archive_history(90)  # Last 90 entries
            
            # Calculate earnings trends and projections
            earnings_analysis = self._analyze_earnings_trends(history, current_metrics)
            
            # Revenue stream breakdown
            revenue_streams = self._analyze_revenue_streams(current_metrics)
            
            # Performance insights
            performance_insights = self._generate_performance_insights(current_metrics, history)
            
            # Combine all data
            summary = {
                **current_metrics,
                **earnings_analysis,
                **revenue_streams,
                **performance_insights,
                "summary_generated": datetime.datetime.utcnow().isoformat(),
                "data_points": len(history)
            }
            
            # Archive current summary if auto-archive is enabled
            if self.config.get("earnings_settings", {}).get("auto_archive", True):
                self.archive_tiktok(summary)
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generating earnings summary: {str(e)}")
            return {"error": str(e)}
    
    def _analyze_earnings_trends(self, history: List[Dict[str, Any]], current: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze earnings trends and projections"""
        try:
            if len(history) < 2:
                return {"monthly_projection": 0, "weekly_average": 0, "best_month": 0}
            
            # Calculate recent earnings velocity
            recent_earnings = [entry.get("payouts", 0) for entry in history[-30:]]  # Last 30 days
            daily_average = sum(recent_earnings) / len(recent_earnings) if recent_earnings else 0
            weekly_average = daily_average * 7
            monthly_projection = daily_average * 30
            
            # Find best performing period
            monthly_earnings = []
            for i in range(0, len(history), 30):  # Group by ~30 day periods
                month_data = history[i:i+30]
                month_total = sum(entry.get("payouts", 0) for entry in month_data)
                monthly_earnings.append(month_total)
            
            best_month = max(monthly_earnings) if monthly_earnings else 0
            
            return {
                "daily_average_earnings": round(daily_average, 2),
                "weekly_average": round(weekly_average, 2),
                "monthly_projection": round(monthly_projection, 2),
                "best_month": round(best_month, 2),
                "earnings_velocity": "increasing" if len(recent_earnings) > 1 and recent_earnings[-1] > recent_earnings[-7] else "stable"
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing earnings trends: {str(e)}")
            return {"monthly_projection": 0, "weekly_average": 0, "best_month": 0}
    
    def _analyze_revenue_streams(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze revenue stream breakdown"""
        try:
            total_earnings = metrics.get("payouts", 0)
            creator_fund = metrics.get("creator_fund", 0)
            live_gifts = metrics.get("live_gifts", 0)
            brand_partnerships = metrics.get("brand_partnerships", 0)
            
            if total_earnings == 0:
                return {"revenue_breakdown": "No earnings data available"}
            
            # Calculate percentages
            creator_fund_pct = (creator_fund / total_earnings * 100) if total_earnings > 0 else 0
            live_gifts_pct = (live_gifts / total_earnings * 100) if total_earnings > 0 else 0
            partnerships_pct = (brand_partnerships / total_earnings * 100) if total_earnings > 0 else 0
            
            # Identify primary revenue source
            sources = {
                "Creator Fund": creator_fund_pct,
                "Live Gifts": live_gifts_pct,
                "Brand Partnerships": partnerships_pct
            }
            
            primary_source = max(sources, key=sources.get) if sources else "Unknown"
            
            return {
                "revenue_streams": {
                    "creator_fund": {"amount": creator_fund, "percentage": round(creator_fund_pct, 1)},
                    "live_gifts": {"amount": live_gifts, "percentage": round(live_gifts_pct, 1)},
                    "brand_partnerships": {"amount": brand_partnerships, "percentage": round(partnerships_pct, 1)}
                },
                "primary_revenue_source": primary_source,
                "revenue_diversification": len([s for s in sources.values() if s > 10])  # Sources over 10%
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing revenue streams: {str(e)}")
            return {"revenue_breakdown": "Analysis error"}
    
    def _generate_performance_insights(self, current: Dict[str, Any], history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate actionable performance insights"""
        try:
            insights = []
            recommendations = []
            
            # Engagement analysis
            engagement_rate = current.get("engagement_rate", 0)
            if engagement_rate > 8:
                insights.append("🔥 Excellent engagement rate - content resonates well with audience")
            elif engagement_rate > 5:
                insights.append("📈 Good engagement - consider optimizing posting times")
            else:
                insights.append("⚠️ Low engagement - review content strategy")
                recommendations.append("Focus on trending hashtags and participate in challenges")
            
            # Earnings analysis
            earnings_per_1k = current.get("earnings_per_1k_views", 0)
            if earnings_per_1k > 0.5:
                insights.append("💰 Strong monetization - above average earnings per view")
            elif earnings_per_1k > 0.1:
                insights.append("💵 Moderate monetization - room for improvement")
            else:
                insights.append("📊 Focus on monetization optimization needed")
                recommendations.append("Apply for Creator Fund and explore brand partnerships")
            
            # Growth analysis
            follower_growth = current.get("follower_growth", 0)
            if follower_growth > 100:
                insights.append("🚀 Rapid growth phase - capitalize on momentum")
            elif follower_growth > 0:
                insights.append("📊 Steady growth - maintain consistency")
            else:
                insights.append("🎯 Growth stagnation - refresh content strategy")
                recommendations.append("Experiment with new content formats and collaborate with other creators")
            
            # Creator score analysis
            creator_score = current.get("creator_score", 0)
            if creator_score > 80:
                insights.append("👑 Top-tier creator performance")
            elif creator_score > 60:
                insights.append("⭐ Strong creator performance")
            else:
                insights.append("📈 Improvement opportunities available")
            
            return {
                "performance_insights": insights,
                "recommendations": recommendations,
                "optimization_priority": "engagement" if engagement_rate < 5 else "monetization" if earnings_per_1k < 0.1 else "growth"
            }
            
        except Exception as e:
            self.logger.error(f"Error generating insights: {str(e)}")
            return {"performance_insights": ["Analysis temporarily unavailable"]}
    
    def test_connection(self) -> bool:
        """Test TikTok API connection"""
        try:
            if not self.token or self.token == "YOUR_TIKTOK_TOKEN_HERE":
                return False
            
            # Simple API test with timeout
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.api_base}/test", headers=headers, timeout=5)
            
            return response.status_code == 200
            
        except Exception as e:
            self.logger.error(f"TikTok connection test failed: {str(e)}")
            return False

# Enhanced backward compatibility functions
def tiktok_metrics(user_id: str) -> Dict[str, Any]:
    """
    🔥 Enhanced TikTok Metrics Function 👑
    Your original function enhanced with comprehensive earnings analytics
    """
    try:
        tiktok_system = CodexTikTokEarnings()
        return tiktok_system.tiktok_metrics(user_id)
    except Exception as e:
        return {"error": str(e), "followers": 0, "views": 0, "payouts": 0}

def archive_tiktok(report: Dict[str, Any]) -> bool:
    """
    🔥 Enhanced TikTok Archive Function 👑
    Your original function enhanced with structured earnings archiving
    """
    try:
        tiktok_system = CodexTikTokEarnings()
        return tiktok_system.archive_tiktok(report)
    except Exception as e:
        return False

# Quick analytics function
def get_tiktok_earnings(user_id: Optional[str] = None) -> Dict[str, Any]:
    """Get comprehensive TikTok earnings analytics"""
    try:
        tiktok_system = CodexTikTokEarnings()
        if user_id:
            tiktok_system.user_id = user_id
        
        return tiktok_system.get_earnings_summary()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Test the system
    tiktok_system = CodexTikTokEarnings()
    
    print("🔥 TikTok Earnings System Test 👑")
    
    # Test metrics
    metrics = tiktok_system.get_earnings_summary()
    print(f"Earnings summary: {metrics}")
    
    if tiktok_system.test_connection():
        print("✅ TikTok API connection successful!")
    else:
        print("⚠️ TikTok API connection failed - using demo data")