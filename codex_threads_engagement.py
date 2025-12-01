"""
🔥 CODEX THREADS ENGAGEMENT SYSTEM 👑
Advanced Meta Threads Analytics and Community Management

The Merritt Method™ - Social Network Sovereignty
"""

import datetime
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import requests


class CodexThreadsEngagement:
    """
    🔥 Sacred Threads Engagement Management System 👑

    Comprehensive Meta Threads integration for the Codex Dominion:
    - Thread engagement analytics (likes, reposts, replies)
    - Community growth tracking
    - Content performance analysis
    - Audience engagement insights
    - Social listening capabilities
    - Archive management system
    """

    def __init__(self, config_file: str = "threads_config.json"):
        """Initialize the Threads Engagement System"""
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.meta_token = self.config.get("threads", {}).get("meta_token") or os.getenv(
            "META_TOKEN"
        )
        self.profile_id = self.config.get("threads", {}).get("profile_id") or os.getenv(
            "THREADS_PROFILE_ID"
        )
        self.archive_file = Path("ledger_threads.jsonl")

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Meta Graph API endpoints
        self.graph_base = "https://graph.facebook.com/v19.0"
        self.threads_api_version = "v19.0"

    def _load_config(self) -> Dict[str, Any]:
        """Load Threads configuration from JSON file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                # Create default config
                default_config = {
                    "threads": {
                        "meta_token": "YOUR_META_TOKEN_HERE",
                        "profile_id": "YOUR_THREADS_PROFILE_ID_HERE",
                        "app_id": "YOUR_META_APP_ID",
                        "app_secret": "YOUR_META_APP_SECRET",
                    },
                    "engagement_settings": {
                        "track_likes": True,
                        "track_reposts": True,
                        "track_replies": True,
                        "track_mentions": True,
                        "track_hashtags": True,
                        "auto_archive": True,
                        "sentiment_analysis": False,
                    },
                    "analytics_settings": {
                        "track_growth": True,
                        "track_reach": True,
                        "track_impressions": True,
                        "competitor_analysis": False,
                        "export_format": "json",
                        "alert_thresholds": {
                            "engagement_spike": 500,
                            "follower_milestone": 1000,
                            "viral_threshold": 10000,
                            "engagement_drop": 0.1,
                        },
                    },
                    "content_settings": {
                        "auto_tag_engagement": True,
                        "track_viral_threads": True,
                        "content_categories": ["tech", "business", "lifestyle", "news"],
                        "optimal_posting_times": ["09:00", "12:00", "15:00", "18:00"],
                    },
                }

                with open(self.config_file, "w", encoding="utf-8") as f:
                    json.dump(default_config, f, indent=2)

                return default_config

        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            return {}

    def threads_metrics(self, profile_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Enhanced Threads metrics collection

        Args:
            profile_id: Optional profile ID, uses configured default if not provided

        Returns:
            Dictionary with comprehensive Threads engagement metrics
        """
        target_profile = profile_id or self.profile_id

        if not target_profile or target_profile == "YOUR_THREADS_PROFILE_ID_HERE":
            return self._generate_demo_metrics()

        try:
            # Get profile insights and metrics
            metrics = self._fetch_threads_insights(target_profile)

            # Enhance with calculated metrics
            enhanced_metrics = self._enhance_metrics(metrics)

            self.logger.info(f"Retrieved Threads metrics for profile: {target_profile}")
            return enhanced_metrics

        except Exception as e:
            self.logger.error(f"Error retrieving Threads metrics: {str(e)}")
            return {"error": str(e), "likes": 0, "reposts": 0, "replies": 0}

    def _fetch_threads_insights(self, profile_id: str) -> Dict[str, Any]:
        """Fetch insights from Meta Graph API for Threads"""
        try:
            if not self.meta_token or self.meta_token == "YOUR_META_TOKEN_HERE":
                return self._generate_demo_metrics()

            headers = {
                "Authorization": f"Bearer {self.meta_token}",
                "Content-Type": "application/json",
            }

            # Fetch profile insights
            insights_url = f"{self.graph_base}/{profile_id}/insights"
            params = {
                "metric": "likes,comments,shares,reach,impressions",
                "period": "day",
                "since": (
                    datetime.datetime.now() - datetime.timedelta(days=7)
                ).isoformat(),
                "until": datetime.datetime.now().isoformat(),
            }

            response = requests.get(
                insights_url, headers=headers, params=params, timeout=10
            )

            if response.status_code == 200:
                data = response.json()

                # Extract metrics from Meta Graph API response
                return {
                    "likes": self._extract_metric_value(data, "likes"),
                    "reposts": self._extract_metric_value(
                        data, "shares"
                    ),  # Shares = Reposts
                    "replies": self._extract_metric_value(data, "comments"),
                    "reach": self._extract_metric_value(data, "reach"),
                    "impressions": self._extract_metric_value(data, "impressions"),
                    "profile_id": profile_id,
                    "source": "meta_graph_api",
                }
            else:
                # Handle API errors gracefully
                self.logger.warning(
                    f"Meta Graph API returned status {response.status_code}"
                )
                return self._generate_demo_metrics()

        except requests.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            return self._generate_demo_metrics()
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return self._generate_demo_metrics()

    def _extract_metric_value(self, data: Dict[str, Any], metric_name: str) -> int:
        """Extract metric value from Meta Graph API response"""
        try:
            # Meta Graph API returns data in a specific format
            for item in data.get("data", []):
                if item.get("name") == metric_name:
                    values = item.get("values", [])
                    if values:
                        return sum(v.get("value", 0) for v in values)
            return 0
        except Exception:
            return 0

    def _generate_demo_metrics(self) -> Dict[str, Any]:
        """Generate demo metrics when API is not available"""
        import random

        # Generate realistic demo data for Threads
        base_likes = 2400
        base_reposts = 180
        base_replies = 320
        base_reach = 15000
        base_impressions = 25000

        # Add some realistic variation
        likes = base_likes + random.randint(-200, 500)
        reposts = base_reposts + random.randint(-20, 80)
        replies = base_replies + random.randint(-30, 100)
        reach = base_reach + random.randint(-2000, 5000)
        impressions = base_impressions + random.randint(-3000, 8000)

        return {
            "likes": likes,
            "reposts": reposts,
            "replies": replies,
            "reach": reach,
            "impressions": impressions,
            "followers": 8500 + random.randint(-500, 1000),
            "following": 1200 + random.randint(-50, 200),
            "threads_count": 450 + random.randint(-20, 50),
            "source": "demo_data",
            "demo": True,
        }

    def _enhance_metrics(self, base_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance base metrics with calculated values"""
        try:
            likes = base_metrics.get("likes", 0)
            reposts = base_metrics.get("reposts", 0)
            replies = base_metrics.get("replies", 0)
            reach = base_metrics.get("reach", 0)
            impressions = base_metrics.get("impressions", 0)
            followers = base_metrics.get("followers", 0)
            threads_count = base_metrics.get("threads_count", 1)

            # Calculate engagement metrics
            total_engagement = likes + reposts + replies
            engagement_rate = (
                (total_engagement / impressions * 100) if impressions > 0 else 0
            )
            reach_rate = (reach / impressions * 100) if impressions > 0 else 0
            avg_engagement_per_thread = (
                total_engagement / threads_count if threads_count > 0 else 0
            )

            # Calculate community metrics
            reply_to_like_ratio = (replies / likes) if likes > 0 else 0
            repost_to_like_ratio = (reposts / likes) if likes > 0 else 0

            # Calculate performance score (0-100)
            performance_score = self._calculate_performance_score(base_metrics)

            # Get growth metrics
            growth_metrics = self._calculate_growth_metrics()

            enhanced = {
                **base_metrics,
                "total_engagement": total_engagement,
                "engagement_rate": round(engagement_rate, 2),
                "reach_rate": round(reach_rate, 2),
                "avg_engagement_per_thread": round(avg_engagement_per_thread, 1),
                "reply_to_like_ratio": round(reply_to_like_ratio, 3),
                "repost_to_like_ratio": round(repost_to_like_ratio, 3),
                "performance_score": performance_score,
                "last_updated": datetime.datetime.utcnow().isoformat(),
                **growth_metrics,
            }

            return enhanced

        except Exception as e:
            self.logger.error(f"Error enhancing metrics: {str(e)}")
            return base_metrics

    def _calculate_performance_score(self, metrics: Dict[str, Any]) -> int:
        """Calculate overall Threads performance score (0-100)"""
        try:
            likes = metrics.get("likes", 0)
            reposts = metrics.get("reposts", 0)
            replies = metrics.get("replies", 0)
            reach = metrics.get("reach", 0)
            impressions = metrics.get("impressions", 0)

            # Scoring algorithm for Threads engagement
            engagement_score = min(
                (likes + reposts + replies) / 1000 * 40, 40
            )  # Max 40 points
            reach_score = min(reach / 10000 * 30, 30)  # Max 30 points
            interaction_quality = min(
                (replies + reposts) / likes * 100 if likes > 0 else 0, 30
            )  # Max 30 points

            total_score = engagement_score + reach_score + interaction_quality
            return min(int(total_score), 100)

        except Exception:
            return 0

    def _calculate_growth_metrics(self) -> Dict[str, Any]:
        """Calculate growth trends from historical data"""
        try:
            history = self.get_archive_history(30)  # Last 30 entries

            if len(history) < 2:
                return {
                    "likes_growth": 0,
                    "engagement_growth": 0,
                    "reach_growth": 0,
                    "trend_direction": "stable",
                }

            # Get previous metrics (7 days ago if available)
            recent = history[-1] if history else {}
            previous = history[-7] if len(history) >= 7 else history[0]

            current_likes = recent.get("likes", 0)
            previous_likes = previous.get("likes", 0)

            current_engagement = recent.get("total_engagement", 0)
            previous_engagement = previous.get("total_engagement", 0)

            current_reach = recent.get("reach", 0)
            previous_reach = previous.get("reach", 0)

            likes_growth = current_likes - previous_likes
            engagement_growth = current_engagement - previous_engagement
            reach_growth = current_reach - previous_reach

            # Determine trend direction
            if likes_growth > 0 and engagement_growth > 0:
                trend_direction = "growing"
            elif likes_growth < 0 or engagement_growth < 0:
                trend_direction = "declining"
            else:
                trend_direction = "stable"

            return {
                "likes_growth": likes_growth,
                "engagement_growth": engagement_growth,
                "reach_growth": reach_growth,
                "trend_direction": trend_direction,
                "growth_rate": (
                    round((likes_growth / previous_likes * 100), 2)
                    if previous_likes > 0
                    else 0
                ),
            }

        except Exception as e:
            self.logger.error(f"Error calculating growth metrics: {str(e)}")
            return {
                "likes_growth": 0,
                "engagement_growth": 0,
                "reach_growth": 0,
                "trend_direction": "unknown",
            }

    def archive_threads(self, report: Dict[str, Any]) -> bool:
        """
        Enhanced Threads archive system

        Args:
            report: Threads metrics report to archive

        Returns:
            bool: True if archived successfully
        """
        try:
            # Prepare archive entry
            archive_entry = {
                "ts": datetime.datetime.utcnow().isoformat(),
                "type": "threads_engagement",
                **report,
            }

            # Append to JSONL file
            with open(self.archive_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(archive_entry, ensure_ascii=False) + "\n")

            self.logger.info("Threads engagement metrics archived successfully")
            return True

        except Exception as e:
            self.logger.error(f"Error archiving Threads report: {str(e)}")
            return False

    def get_archive_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get Threads archive history"""
        try:
            if not self.archive_file.exists():
                return []

            history = []
            with open(self.archive_file, "r", encoding="utf-8") as f:
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

    def get_engagement_summary(self) -> Dict[str, Any]:
        """Get comprehensive Threads engagement summary"""
        try:
            # Get current metrics
            current_metrics = self.threads_metrics()

            if current_metrics.get("error"):
                return current_metrics

            # Get historical data for analysis
            history = self.get_archive_history(90)  # Last 90 entries

            # Calculate engagement trends and insights
            engagement_analysis = self._analyze_engagement_trends(
                history, current_metrics
            )

            # Community insights
            community_insights = self._analyze_community_engagement(current_metrics)

            # Content performance insights
            content_insights = self._generate_content_insights(current_metrics, history)

            # Combine all data
            summary = {
                **current_metrics,
                **engagement_analysis,
                **community_insights,
                **content_insights,
                "summary_generated": datetime.datetime.utcnow().isoformat(),
                "data_points": len(history),
            }

            # Archive current summary if auto-archive is enabled
            if self.config.get("engagement_settings", {}).get("auto_archive", True):
                self.archive_threads(summary)

            return summary

        except Exception as e:
            self.logger.error(f"Error generating engagement summary: {str(e)}")
            return {"error": str(e)}

    def _analyze_engagement_trends(
        self, history: List[Dict[str, Any]], current: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze engagement trends and patterns"""
        try:
            if len(history) < 2:
                return {
                    "engagement_velocity": "stable",
                    "peak_engagement_time": "unknown",
                }

            # Calculate engagement velocity
            recent_engagements = [
                entry.get("total_engagement", 0) for entry in history[-14:]
            ]  # Last 14 days
            if len(recent_engagements) > 7:
                recent_avg = sum(recent_engagements[-7:]) / 7
                previous_avg = sum(recent_engagements[-14:-7]) / 7

                if recent_avg > previous_avg * 1.1:
                    velocity = "accelerating"
                elif recent_avg < previous_avg * 0.9:
                    velocity = "decelerating"
                else:
                    velocity = "stable"
            else:
                velocity = "insufficient_data"

            # Find peak engagement patterns
            hourly_engagement = {}
            for entry in history[-30:]:  # Last 30 entries
                timestamp = entry.get("ts", "")
                if timestamp:
                    try:
                        hour = datetime.datetime.fromisoformat(
                            timestamp.replace("Z", "+00:00")
                        ).hour
                        engagement = entry.get("total_engagement", 0)
                        if hour not in hourly_engagement:
                            hourly_engagement[hour] = []
                        hourly_engagement[hour].append(engagement)
                    except Exception:
                        continue

            # Calculate average engagement by hour
            avg_by_hour = {}
            for hour, engagements in hourly_engagement.items():
                avg_by_hour[hour] = sum(engagements) / len(engagements)

            peak_hour = (
                max(avg_by_hour, key=avg_by_hour.get) if avg_by_hour else "unknown"
            )

            return {
                "engagement_velocity": velocity,
                "peak_engagement_hour": (
                    f"{peak_hour}:00" if peak_hour != "unknown" else "unknown"
                ),
                "avg_daily_engagement": (
                    sum(recent_engagements) / len(recent_engagements)
                    if recent_engagements
                    else 0
                ),
            }

        except Exception as e:
            self.logger.error(f"Error analyzing engagement trends: {str(e)}")
            return {"engagement_velocity": "unknown", "peak_engagement_time": "unknown"}

    def _analyze_community_engagement(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze community engagement patterns"""
        try:
            likes = metrics.get("likes", 0)
            reposts = metrics.get("reposts", 0)
            replies = metrics.get("replies", 0)
            total_engagement = likes + reposts + replies

            if total_engagement == 0:
                return {"community_type": "low_engagement"}

            # Calculate engagement distribution
            like_percentage = (likes / total_engagement) * 100
            repost_percentage = (reposts / total_engagement) * 100
            reply_percentage = (replies / total_engagement) * 100

            # Determine community characteristics
            if reply_percentage > 30:
                community_type = "conversational"
            elif repost_percentage > 20:
                community_type = "sharing_focused"
            elif like_percentage > 70:
                community_type = "passive_consumers"
            else:
                community_type = "balanced"

            # Calculate engagement quality score
            quality_score = (replies * 3 + reposts * 2 + likes * 1) / total_engagement

            return {
                "community_type": community_type,
                "engagement_distribution": {
                    "likes": round(like_percentage, 1),
                    "reposts": round(repost_percentage, 1),
                    "replies": round(reply_percentage, 1),
                },
                "engagement_quality_score": round(quality_score, 2),
            }

        except Exception as e:
            self.logger.error(f"Error analyzing community engagement: {str(e)}")
            return {"community_type": "unknown"}

    def _generate_content_insights(
        self, current: Dict[str, Any], history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate actionable content insights"""
        try:
            insights = []
            recommendations = []

            # Engagement analysis
            engagement_rate = current.get("engagement_rate", 0)
            if engagement_rate > 5:
                insights.append(
                    "🔥 Excellent engagement rate - content resonates strongly"
                )
            elif engagement_rate > 2:
                insights.append(
                    "📈 Good engagement - consider posting frequency optimization"
                )
            else:
                insights.append("⚠️ Low engagement - review content strategy")
                recommendations.append(
                    "Experiment with trending topics and interactive content"
                )

            # Community interaction analysis
            reply_ratio = current.get("reply_to_like_ratio", 0)
            if reply_ratio > 0.3:
                insights.append(
                    "💬 Strong conversational engagement - community is highly interactive"
                )
            elif reply_ratio > 0.1:
                insights.append("🗣️ Moderate conversation - encourage more discussion")
            else:
                insights.append(
                    "📢 Broadcast style - consider adding conversation starters"
                )
                recommendations.append("Ask questions and create discussion prompts")

            # Reach analysis
            reach_rate = current.get("reach_rate", 0)
            if reach_rate > 80:
                insights.append(
                    "🎯 Excellent reach efficiency - content is highly discoverable"
                )
            elif reach_rate > 50:
                insights.append("👀 Good reach - content finding its audience")
            else:
                insights.append("📊 Reach optimization needed")
                recommendations.append(
                    "Use relevant hashtags and post at optimal times"
                )

            # Performance score analysis
            performance_score = current.get("performance_score", 0)
            if performance_score > 80:
                insights.append("👑 Top-tier performance across all metrics")
            elif performance_score > 60:
                insights.append("⭐ Strong overall performance")
            else:
                insights.append("📈 Growth opportunities available")

            return {
                "content_insights": insights,
                "recommendations": recommendations,
                "optimization_priority": self._determine_optimization_priority(current),
            }

        except Exception as e:
            self.logger.error(f"Error generating content insights: {str(e)}")
            return {"content_insights": ["Analysis temporarily unavailable"]}

    def _determine_optimization_priority(self, metrics: Dict[str, Any]) -> str:
        """Determine the top optimization priority"""
        engagement_rate = metrics.get("engagement_rate", 0)
        reach_rate = metrics.get("reach_rate", 0)
        reply_ratio = metrics.get("reply_to_like_ratio", 0)

        if engagement_rate < 2:
            return "engagement"
        elif reach_rate < 50:
            return "reach"
        elif reply_ratio < 0.1:
            return "conversation"
        else:
            return "growth"

    def test_connection(self) -> bool:
        """Test Meta Graph API connection"""
        try:
            if not self.meta_token or self.meta_token == "YOUR_META_TOKEN_HERE":
                return False

            # Simple API test
            headers = {"Authorization": f"Bearer {self.meta_token}"}
            response = requests.get(f"{self.graph_base}/me", headers=headers, timeout=5)

            return response.status_code == 200

        except Exception as e:
            self.logger.error(f"Threads connection test failed: {str(e)}")
            return False


# Enhanced backward compatibility functions
def threads_metrics(profile_id: Optional[str] = None) -> Dict[str, Any]:
    """
    🔥 Enhanced Threads Metrics Function 👑
    Your original function enhanced with comprehensive engagement analytics
    """
    try:
        threads_system = CodexThreadsEngagement()
        return threads_system.threads_metrics(profile_id)
    except Exception as e:
        return {"error": str(e), "likes": 0, "reposts": 0, "replies": 0}


def archive_threads(report: Dict[str, Any]) -> bool:
    """
    🔥 Enhanced Threads Archive Function 👑
    Your original function enhanced with structured engagement archiving
    """
    try:
        threads_system = CodexThreadsEngagement()
        return threads_system.archive_threads(report)
    except Exception as e:
        return False


# Quick analytics function
def get_threads_engagement(profile_id: Optional[str] = None) -> Dict[str, Any]:
    """Get comprehensive Threads engagement analytics"""
    try:
        threads_system = CodexThreadsEngagement()
        if profile_id:
            threads_system.profile_id = profile_id

        return threads_system.get_engagement_summary()
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # Test the system
    threads_system = CodexThreadsEngagement()

    print("🔥 Threads Engagement System Test 👑")

    # Test metrics
    metrics = threads_system.get_engagement_summary()
    print(f"Engagement summary: {metrics}")

    if threads_system.test_connection():
        print("✅ Meta Graph API connection successful!")
    else:
        print("⚠️ Meta Graph API connection failed - using demo data")
