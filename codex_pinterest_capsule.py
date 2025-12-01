"""
🔥 CODEX PINTEREST CAPSULE 📌
Advanced Pinterest Business API Integration for Creator Economy

The Merritt Method™ - Pinterest Affiliate Revenue & Pin Performance Sovereignty
"""

import datetime
import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CodexPinterestCapsule:
    """
    🔥 Advanced Pinterest Business API Integration

    Features:
    - Pin analytics and performance tracking
    - Affiliate revenue monitoring
    - Impression and click optimization
    - Board management and strategy
    - Campaign performance analysis
    - Revenue attribution tracking
    """

    def __init__(self, config_file: str = "pinterest_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.base_url = "https://api.pinterest.com/v5"
        self.headers = {
            "Authorization": f"Bearer {self.config.get('pinterest_token', '')}",
            "Content-Type": "application/json",
        }

    def load_config(self) -> Dict[str, Any]:
        """Load Pinterest configuration with fallback to environment variables"""
        try:
            config_path = Path(self.config_file)
            if config_path.exists():
                with open(config_path, "r") as f:
                    config = json.load(f)
            else:
                config = {}

            # Environment variable fallbacks
            config.setdefault("pinterest_token", os.getenv("PINTEREST_TOKEN", ""))
            config.setdefault("pinterest_board_id", os.getenv("PINTEREST_BOARD_ID", ""))
            config.setdefault("pinterest_user_id", os.getenv("PINTEREST_USER_ID", ""))

            # Default settings
            config.setdefault("analytics_days", 30)
            config.setdefault("rate_limit_delay", 1.0)
            config.setdefault("batch_size", 25)
            config.setdefault("demo_mode", not config.get("pinterest_token"))

            return config

        except Exception as e:
            logger.error(f"Error loading Pinterest config: {e}")
            return {
                "pinterest_token": os.getenv("PINTEREST_TOKEN", ""),
                "pinterest_board_id": os.getenv("PINTEREST_BOARD_ID", ""),
                "pinterest_user_id": os.getenv("PINTEREST_USER_ID", ""),
                "demo_mode": True,
                "analytics_days": 30,
                "rate_limit_delay": 1.0,
                "batch_size": 25,
            }

    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving Pinterest config: {e}")

    def test_connection(self) -> bool:
        """Test Pinterest API connection"""
        try:
            if not self.config.get("pinterest_token"):
                return False

            response = requests.get(
                f"{self.base_url}/user_account", headers=self.headers, timeout=10
            )

            return response.status_code == 200

        except Exception as e:
            logger.error(f"Pinterest API connection test failed: {e}")
            return False

    def pinterest_metrics(self) -> Dict[str, Any]:
        """Enhanced Pinterest metrics with comprehensive analytics"""
        try:
            if self.config.get("demo_mode", True):
                return self._get_demo_metrics()

            # Get analytics data
            end_date = datetime.datetime.utcnow()
            start_date = end_date - datetime.timedelta(
                days=self.config.get("analytics_days", 30)
            )

            # Account analytics
            analytics_params = {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "metric_types": "IMPRESSION,OUTBOUND_CLICK,PIN_CLICK,SAVE",
                "granularity": "DAY",
            }

            analytics_response = requests.get(
                f"{self.base_url}/user_account/analytics",
                headers=self.headers,
                params=analytics_params,
                timeout=10,
            )

            if analytics_response.status_code != 200:
                logger.warning(
                    f"Pinterest analytics API error: {analytics_response.status_code}"
                )
                return self._get_demo_metrics()

            analytics_data = analytics_response.json()

            # Get boards data
            boards_response = requests.get(
                f"{self.base_url}/boards", headers=self.headers, timeout=10
            )

            boards_data = (
                boards_response.json()
                if boards_response.status_code == 200
                else {"items": []}
            )

            # Process analytics
            metrics = self._process_pinterest_analytics(analytics_data, boards_data)

            return metrics

        except Exception as e:
            logger.error(f"Error fetching Pinterest metrics: {e}")
            return self._get_demo_metrics()

    def _process_pinterest_analytics(
        self, analytics_data: Dict, boards_data: Dict
    ) -> Dict[str, Any]:
        """Process Pinterest analytics data into comprehensive metrics"""

        # Extract daily metrics
        daily_metrics = analytics_data.get("daily_metrics", [])

        # Calculate totals
        total_impressions = sum(
            day.get("data_status", {}).get("IMPRESSION", 0) for day in daily_metrics
        )
        total_clicks = sum(
            day.get("data_status", {}).get("OUTBOUND_CLICK", 0) for day in daily_metrics
        )
        total_pin_clicks = sum(
            day.get("data_status", {}).get("PIN_CLICK", 0) for day in daily_metrics
        )
        total_saves = sum(
            day.get("data_status", {}).get("SAVE", 0) for day in daily_metrics
        )

        # Calculate rates
        click_through_rate = (
            (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        )
        save_rate = (
            (total_saves / total_impressions * 100) if total_impressions > 0 else 0
        )
        engagement_rate = (
            ((total_clicks + total_saves) / total_impressions * 100)
            if total_impressions > 0
            else 0
        )

        # Estimate affiliate revenue (based on industry averages)
        estimated_cpm = 2.50  # Average Pinterest CPM
        estimated_affiliate_rate = 0.05  # 5% conversion rate
        estimated_commission = 15.00  # Average commission per conversion

        affiliate_revenue = (
            total_clicks * estimated_affiliate_rate * estimated_commission
        )

        # Board analysis
        total_boards = len(boards_data.get("items", []))
        active_boards = sum(
            1 for board in boards_data.get("items", []) if board.get("pin_count", 0) > 0
        )

        # Performance scoring
        performance_score = self._calculate_pinterest_performance_score(
            click_through_rate, save_rate, engagement_rate, total_impressions
        )

        # Growth analysis
        if len(daily_metrics) >= 7:
            recent_week = daily_metrics[-7:]
            previous_week = daily_metrics[-14:-7] if len(daily_metrics) >= 14 else []

            recent_impressions = sum(
                day.get("data_status", {}).get("IMPRESSION", 0) for day in recent_week
            )
            previous_impressions = sum(
                day.get("data_status", {}).get("IMPRESSION", 0) for day in previous_week
            )

            growth_rate = (
                (
                    (recent_impressions - previous_impressions)
                    / previous_impressions
                    * 100
                )
                if previous_impressions > 0
                else 0
            )
        else:
            growth_rate = 0

        return {
            # Core metrics
            "impressions": total_impressions,
            "clicks": total_clicks,
            "pin_clicks": total_pin_clicks,
            "saves": total_saves,
            "affiliate_revenue": affiliate_revenue,
            # Performance rates
            "click_through_rate": round(click_through_rate, 2),
            "save_rate": round(save_rate, 2),
            "engagement_rate": round(engagement_rate, 2),
            # Board metrics
            "total_boards": total_boards,
            "active_boards": active_boards,
            "board_utilization_rate": round(
                (active_boards / total_boards * 100) if total_boards > 0 else 0, 1
            ),
            # Growth metrics
            "growth_rate": round(growth_rate, 1),
            "performance_score": performance_score,
            # Revenue analysis
            "revenue_per_click": round(
                affiliate_revenue / total_clicks if total_clicks > 0 else 0, 2
            ),
            "revenue_per_impression": round(
                (
                    affiliate_revenue / total_impressions * 1000
                    if total_impressions > 0
                    else 0
                ),
                2,
            ),  # RPM
            "estimated_monthly_revenue": round(
                affiliate_revenue * 30 / self.config.get("analytics_days", 30), 2
            ),
            # Quality metrics
            "content_quality": self._assess_content_quality(
                click_through_rate, save_rate
            ),
            "audience_engagement": self._assess_audience_engagement(engagement_rate),
            "monetization_efficiency": self._assess_monetization_efficiency(
                affiliate_revenue, total_clicks
            ),
            # Trend analysis
            "performance_trend": self._determine_performance_trend(
                growth_rate, performance_score
            ),
            "revenue_trend": self._determine_revenue_trend(
                affiliate_revenue, total_clicks
            ),
            # Metadata
            "last_updated": datetime.datetime.utcnow().isoformat(),
            "analytics_period_days": self.config.get("analytics_days", 30),
            "demo": False,
        }

    def _calculate_pinterest_performance_score(
        self, ctr: float, save_rate: float, engagement_rate: float, impressions: int
    ) -> float:
        """Calculate comprehensive Pinterest performance score"""

        # Weight factors
        ctr_weight = 0.35
        save_weight = 0.25
        engagement_weight = 0.25
        reach_weight = 0.15

        # Normalize metrics (industry benchmarks)
        ctr_score = min(ctr / 0.2 * 100, 100)  # 0.2% is good CTR
        save_score = min(save_rate / 2.0 * 100, 100)  # 2% is good save rate
        engagement_score = min(
            engagement_rate / 2.5 * 100, 100
        )  # 2.5% is good engagement
        reach_score = min(impressions / 10000 * 100, 100)  # 10k impressions baseline

        total_score = (
            ctr_score * ctr_weight
            + save_score * save_weight
            + engagement_score * engagement_weight
            + reach_score * reach_weight
        )

        return round(total_score, 1)

    def _assess_content_quality(self, ctr: float, save_rate: float) -> str:
        """Assess content quality based on engagement metrics"""
        avg_metric = (ctr + save_rate) / 2

        if avg_metric >= 2.0:
            return "exceptional"
        elif avg_metric >= 1.0:
            return "excellent"
        elif avg_metric >= 0.5:
            return "good"
        elif avg_metric >= 0.2:
            return "fair"
        else:
            return "needs_improvement"

    def _assess_audience_engagement(self, engagement_rate: float) -> str:
        """Assess audience engagement level"""
        if engagement_rate >= 3.0:
            return "very_high"
        elif engagement_rate >= 2.0:
            return "high"
        elif engagement_rate >= 1.0:
            return "moderate"
        elif engagement_rate >= 0.5:
            return "low"
        else:
            return "very_low"

    def _assess_monetization_efficiency(self, revenue: float, clicks: int) -> str:
        """Assess monetization efficiency"""
        if clicks == 0:
            return "no_data"

        revenue_per_click = revenue / clicks

        if revenue_per_click >= 1.0:
            return "excellent"
        elif revenue_per_click >= 0.5:
            return "good"
        elif revenue_per_click >= 0.2:
            return "fair"
        elif revenue_per_click >= 0.1:
            return "low"
        else:
            return "very_low"

    def _determine_performance_trend(
        self, growth_rate: float, performance_score: float
    ) -> str:
        """Determine overall performance trend"""
        if growth_rate > 10 and performance_score > 70:
            return "accelerating"
        elif growth_rate > 5 or performance_score > 60:
            return "growing"
        elif growth_rate > -5 and performance_score > 40:
            return "stable"
        elif growth_rate > -15:
            return "declining"
        else:
            return "critical"

    def _determine_revenue_trend(self, revenue: float, clicks: int) -> str:
        """Determine revenue performance trend"""
        if clicks == 0:
            return "no_data"

        revenue_per_click = revenue / clicks

        if revenue_per_click >= 0.75:
            return "excellent"
        elif revenue_per_click >= 0.50:
            return "strong"
        elif revenue_per_click >= 0.25:
            return "moderate"
        elif revenue_per_click >= 0.10:
            return "weak"
        else:
            return "poor"

    def _get_demo_metrics(self) -> Dict[str, Any]:
        """Generate comprehensive demo data for Pinterest Capsule"""
        import random

        base_impressions = random.randint(25000, 85000)
        base_clicks = random.randint(
            int(base_impressions * 0.008), int(base_impressions * 0.025)
        )
        base_saves = random.randint(
            int(base_impressions * 0.015), int(base_impressions * 0.040)
        )

        click_through_rate = base_clicks / base_impressions * 100
        save_rate = base_saves / base_impressions * 100
        engagement_rate = (base_clicks + base_saves) / base_impressions * 100

        affiliate_revenue = base_clicks * random.uniform(0.3, 0.8)

        return {
            # Core metrics
            "impressions": base_impressions,
            "clicks": base_clicks,
            "pin_clicks": base_clicks + random.randint(100, 500),
            "saves": base_saves,
            "affiliate_revenue": round(affiliate_revenue, 2),
            # Performance rates
            "click_through_rate": round(click_through_rate, 2),
            "save_rate": round(save_rate, 2),
            "engagement_rate": round(engagement_rate, 2),
            # Board metrics
            "total_boards": random.randint(8, 25),
            "active_boards": random.randint(5, 20),
            "board_utilization_rate": round(random.uniform(60, 95), 1),
            # Growth metrics
            "growth_rate": round(random.uniform(-5, 25), 1),
            "performance_score": round(random.uniform(55, 88), 1),
            # Revenue analysis
            "revenue_per_click": round(
                affiliate_revenue / base_clicks if base_clicks > 0 else 0, 2
            ),
            "revenue_per_impression": round(
                (
                    affiliate_revenue / base_impressions * 1000
                    if base_impressions > 0
                    else 0
                ),
                2,
            ),
            "estimated_monthly_revenue": round(affiliate_revenue * 1.2, 2),
            # Quality assessments
            "content_quality": random.choice(["excellent", "good", "fair"]),
            "audience_engagement": random.choice(["high", "moderate", "good"]),
            "monetization_efficiency": random.choice(["good", "fair", "excellent"]),
            # Trends
            "performance_trend": random.choice(["growing", "stable", "accelerating"]),
            "revenue_trend": random.choice(["strong", "moderate", "excellent"]),
            # Metadata
            "last_updated": datetime.datetime.utcnow().isoformat(),
            "analytics_period_days": 30,
            "demo": True,
        }

    def pinterest_pin(
        self,
        title: str,
        link: str,
        image_url: str,
        board_id: Optional[str] = None,
        description: str = "",
    ) -> Dict[str, Any]:
        """Create a new Pinterest pin with comprehensive tracking"""
        try:
            if self.config.get("demo_mode", True):
                return {
                    "success": True,
                    "pin_id": f"demo_pin_{int(time.time())}",
                    "message": "Demo pin created (Pinterest API not configured)",
                    "demo": True,
                }

            board_id = board_id or self.config.get("pinterest_board_id")
            if not board_id:
                return {"success": False, "error": "No board ID provided or configured"}

            payload = {
                "title": title,
                "description": description,
                "link": link,
                "board_id": board_id,
                "media_source": {"source_type": "image_url", "url": image_url},
            }

            response = requests.post(
                f"{self.base_url}/pins", headers=self.headers, json=payload, timeout=15
            )

            if response.status_code == 201:
                pin_data = response.json()
                return {
                    "success": True,
                    "pin_id": pin_data.get("id"),
                    "pin_url": pin_data.get("url"),
                    "message": "Pin created successfully",
                }
            else:
                return {
                    "success": False,
                    "error": f"Pinterest API error: {response.status_code}",
                }

        except Exception as e:
            logger.error(f"Error creating Pinterest pin: {e}")
            return {"success": False, "error": str(e)}

    def pinterest_batch_pin(self, pins_data: List[Dict]) -> Dict[str, Any]:
        """Create multiple pins with batch processing and rate limiting"""
        results = {
            "successful_pins": 0,
            "failed_pins": 0,
            "pin_results": [],
            "total_processed": 0,
        }

        try:
            for pin_data in pins_data:
                # Rate limiting
                time.sleep(self.config.get("rate_limit_delay", 1.0))

                result = self.pinterest_pin(
                    title=pin_data.get("title", ""),
                    link=pin_data.get("link", ""),
                    image_url=pin_data.get("image_url", ""),
                    board_id=pin_data.get("board_id"),
                    description=pin_data.get("description", ""),
                )

                results["pin_results"].append(result)
                results["total_processed"] += 1

                if result.get("success"):
                    results["successful_pins"] += 1
                else:
                    results["failed_pins"] += 1

                # Break if batch limit reached
                if results["total_processed"] >= self.config.get("batch_size", 25):
                    break

            return results

        except Exception as e:
            logger.error(f"Error in batch pin creation: {e}")
            results["error"] = str(e)
            return results

    def get_archive_history(self, limit: int = 50) -> List[Dict]:
        """Get Pinterest analytics archive history"""
        try:
            archive_file = Path("ledger_pinterest.jsonl")
            if not archive_file.exists():
                return []

            history = []
            with open(archive_file, "r") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        history.append(entry)
                    except json.JSONDecodeError:
                        continue

            # Sort by timestamp, most recent first
            history.sort(key=lambda x: x.get("ts", ""), reverse=True)
            return history[:limit]

        except Exception as e:
            logger.error(f"Error reading Pinterest archive: {e}")
            return []


# Standalone functions for dashboard integration
def pinterest_metrics() -> Dict[str, Any]:
    """Get Pinterest metrics - standalone function for dashboard"""
    system = CodexPinterestCapsule()
    return system.pinterest_metrics()


def pinterest_pin(
    title: str,
    link: str,
    image_url: str,
    board_id: Optional[str] = None,
    description: str = "",
) -> Dict[str, Any]:
    """Create Pinterest pin - standalone function for dashboard"""
    system = CodexPinterestCapsule()
    return system.pinterest_pin(title, link, image_url, board_id, description)


def pinterest_batch_pin(pins_data: List[Dict]) -> Dict[str, Any]:
    """Create multiple Pinterest pins - standalone function for dashboard"""
    system = CodexPinterestCapsule()
    return system.pinterest_batch_pin(pins_data)


def archive_pinterest(report: Dict[str, Any]) -> bool:
    """Archive Pinterest analytics report"""
    try:
        archive_entry = {"ts": datetime.datetime.utcnow().isoformat(), **report}

        with open("ledger_pinterest.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(archive_entry) + "\n")

        return True

    except Exception as e:
        logger.error(f"Error archiving Pinterest data: {e}")
        return False


def get_pinterest_capsule_summary(user_id: Optional[str] = None) -> Dict[str, Any]:
    """Get comprehensive Pinterest Capsule summary for dashboard"""
    try:
        system = CodexPinterestCapsule()
        metrics = system.pinterest_metrics()

        # Add summary metadata
        metrics["system_status"] = "operational"
        metrics["last_check"] = datetime.datetime.utcnow().isoformat()

        return metrics

    except Exception as e:
        logger.error(f"Error getting Pinterest summary: {e}")
        return {"error": str(e), "system_status": "error", "demo": True}


if __name__ == "__main__":
    # Test Pinterest Capsule system
    print("🔥 Testing Pinterest Capsule System...")

    pinterest_system = CodexPinterestCapsule()

    # Test connection
    if pinterest_system.test_connection():
        print("✅ Pinterest API Connected!")
    else:
        print("⚠️ Using Demo Mode")

    # Test metrics
    metrics = pinterest_system.pinterest_metrics()
    print(f"📊 Impressions: {metrics['impressions']:,}")
    print(f"👆 Clicks: {metrics['clicks']:,}")
    print(f"💰 Affiliate Revenue: ${metrics['affiliate_revenue']:.2f}")
    print(f"⚡ Performance Score: {metrics['performance_score']}/100")

    # Test archiving
    success = archive_pinterest(metrics)
    print(f"💾 Archive: {'✅ Success' if success else '❌ Failed'}")
