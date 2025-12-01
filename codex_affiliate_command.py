"""
🔥 CODEX AFFILIATE COMMAND CENTER 💎
Advanced Affiliate Marketing Analytics & Commission Tracking

The Merritt Method™ - Affiliate Revenue Sovereignty
"""

import datetime
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CodexAffiliateCommand:
    """
    🔥 Advanced Affiliate Marketing Command Center

    Features:
    - Multi-network affiliate tracking
    - Commission analytics and optimization
    - Conversion funnel analysis
    - Revenue attribution modeling
    - Performance trend analysis
    - ROI and profitability tracking
    """

    def __init__(self, config_file: str = "affiliate_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.api_key = self.config.get(
            "affiliate_api_key", os.getenv("AFFILIATE_API_KEY", "")
        )

    def load_config(self) -> Dict[str, Any]:
        """Load affiliate configuration with fallback to environment variables"""
        try:
            config_path = Path(self.config_file)
            if config_path.exists():
                with open(config_path, "r") as f:
                    config = json.load(f)
            else:
                config = {}

            # Environment variable fallbacks
            config.setdefault("affiliate_api_key", os.getenv("AFFILIATE_API_KEY", ""))
            config.setdefault("affiliate_networks", {})
            config.setdefault("tracking_settings", {})

            # Default settings
            config.setdefault("analytics_days", 30)
            config.setdefault("min_commission_threshold", 1.00)
            config.setdefault("conversion_window_days", 30)
            config.setdefault("demo_mode", not config.get("affiliate_api_key"))

            return config

        except Exception as e:
            logger.error(f"Error loading affiliate config: {e}")
            return {
                "affiliate_api_key": os.getenv("AFFILIATE_API_KEY", ""),
                "demo_mode": True,
                "analytics_days": 30,
                "min_commission_threshold": 1.00,
                "conversion_window_days": 30,
            }

    def test_connection(self) -> bool:
        """Test affiliate network API connection"""
        try:
            if not self.api_key:
                return False

            response = requests.get(
                "https://api.affiliatenetwork.com/v1/account",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10,
            )

            return response.status_code == 200

        except Exception as e:
            logger.error(f"Affiliate API connection test failed: {e}")
            return False

    def fetch_affiliate_metrics(self) -> Dict[str, Any]:
        """Enhanced affiliate metrics with comprehensive analytics"""
        try:
            if self.config.get("demo_mode", True):
                return self._get_demo_affiliate_metrics()

            # Primary affiliate network stats
            response = requests.get(
                "https://api.affiliatenetwork.com/v1/stats",
                headers={"Authorization": f"Bearer {self.api_key}"},
                params={
                    "days": self.config.get("analytics_days", 30),
                    "include_sub_affiliates": True,
                    "detailed_breakdown": True,
                },
                timeout=15,
            )

            if response.status_code != 200:
                logger.warning(f"Affiliate API error: {response.status_code}")
                return self._get_demo_affiliate_metrics()

            data = response.json()

            # Process affiliate analytics
            metrics = self._process_affiliate_analytics(data)

            return metrics

        except Exception as e:
            logger.error(f"Error fetching affiliate metrics: {e}")
            return self._get_demo_affiliate_metrics()

    def _process_affiliate_analytics(self, data: Dict) -> Dict[str, Any]:
        """Process affiliate analytics data into comprehensive metrics"""

        # Core metrics
        clicks = data.get("clicks", 0)
        conversions = data.get("conversions", 0)
        commission_usd = data.get("commission_usd", 0)

        # Calculate rates and performance
        conversion_rate = (conversions / clicks * 100) if clicks > 0 else 0
        earnings_per_click = commission_usd / clicks if clicks > 0 else 0
        average_commission = commission_usd / conversions if conversions > 0 else 0

        # Advanced metrics
        revenue_per_mille = (commission_usd / clicks * 1000) if clicks > 0 else 0

        # Performance scoring
        performance_score = self._calculate_affiliate_performance_score(
            conversion_rate, earnings_per_click, commission_usd
        )

        # Trend analysis
        growth_analysis = self._analyze_affiliate_growth(data)

        # Network performance
        network_breakdown = data.get("network_breakdown", {})
        top_network = (
            max(network_breakdown.items(), key=lambda x: x[1].get("commission", 0))
            if network_breakdown
            else (None, {})
        )

        return {
            # Core metrics
            "clicks": clicks,
            "conversions": conversions,
            "commission": commission_usd,
            # Performance rates
            "conversion_rate": round(conversion_rate, 2),
            "earnings_per_click": round(earnings_per_click, 3),
            "average_commission": round(average_commission, 2),
            "revenue_per_mille": round(revenue_per_mille, 2),
            # Advanced analytics
            "performance_score": performance_score,
            "profitability_tier": self._determine_profitability_tier(commission_usd),
            "optimization_potential": self._assess_optimization_potential(
                conversion_rate, earnings_per_click
            ),
            # Growth metrics
            "monthly_projection": round(
                commission_usd * 30 / self.config.get("analytics_days", 30), 2
            ),
            "growth_trend": growth_analysis.get("trend", "stable"),
            "growth_rate": growth_analysis.get("rate", 0),
            # Network analysis
            "active_networks": len(network_breakdown),
            "top_network": top_network[0] if top_network[0] else None,
            "top_network_commission": round(top_network[1].get("commission", 0), 2),
            "network_diversification": self._calculate_diversification_score(
                network_breakdown
            ),
            # Quality metrics
            "conversion_quality": self._assess_conversion_quality(conversion_rate),
            "revenue_consistency": self._assess_revenue_consistency(
                data.get("daily_breakdown", [])
            ),
            "traffic_quality": self._assess_traffic_quality(clicks, conversions),
            # Metadata
            "last_updated": datetime.datetime.utcnow().isoformat(),
            "analytics_period_days": self.config.get("analytics_days", 30),
            "demo": False,
        }

    def _calculate_affiliate_performance_score(
        self, conversion_rate: float, epc: float, commission: float
    ) -> float:
        """Calculate comprehensive affiliate performance score"""

        # Weight factors
        conversion_weight = 0.4
        epc_weight = 0.35
        volume_weight = 0.25

        # Normalize metrics (industry benchmarks)
        conversion_score = min(
            conversion_rate / 3.0 * 100, 100
        )  # 3% is excellent conversion rate
        epc_score = min(epc / 0.50 * 100, 100)  # $0.50 EPC is excellent
        volume_score = min(commission / 500 * 100, 100)  # $500 monthly is good volume

        total_score = (
            conversion_score * conversion_weight
            + epc_score * epc_weight
            + volume_score * volume_weight
        )

        return round(total_score, 1)

    def _determine_profitability_tier(self, commission: float) -> str:
        """Determine profitability tier based on commission volume"""
        if commission >= 2000:
            return "elite"
        elif commission >= 1000:
            return "professional"
        elif commission >= 500:
            return "advanced"
        elif commission >= 100:
            return "developing"
        elif commission >= 10:
            return "emerging"
        else:
            return "startup"

    def _assess_optimization_potential(self, conversion_rate: float, epc: float) -> str:
        """Assess optimization potential based on current performance"""
        if conversion_rate < 1.0 or epc < 0.10:
            return "high"
        elif conversion_rate < 2.0 or epc < 0.25:
            return "moderate"
        elif conversion_rate < 3.0 or epc < 0.40:
            return "low"
        else:
            return "optimized"

    def _analyze_affiliate_growth(self, data: Dict) -> Dict[str, Any]:
        """Analyze affiliate growth trends"""
        daily_data = data.get("daily_breakdown", [])

        if len(daily_data) < 7:
            return {"trend": "insufficient_data", "rate": 0}

        # Compare recent week to previous week
        recent_week = daily_data[-7:]
        previous_week = daily_data[-14:-7] if len(daily_data) >= 14 else []

        recent_commission = sum(day.get("commission", 0) for day in recent_week)
        previous_commission = (
            sum(day.get("commission", 0) for day in previous_week)
            if previous_week
            else recent_commission
        )

        if previous_commission == 0:
            growth_rate = 0
            trend = "new"
        else:
            growth_rate = (
                (recent_commission - previous_commission) / previous_commission
            ) * 100

            if growth_rate > 20:
                trend = "accelerating"
            elif growth_rate > 5:
                trend = "growing"
            elif growth_rate > -5:
                trend = "stable"
            elif growth_rate > -20:
                trend = "declining"
            else:
                trend = "concerning"

        return {"trend": trend, "rate": round(growth_rate, 1)}

    def _calculate_diversification_score(self, network_breakdown: Dict) -> float:
        """Calculate network diversification score"""
        if not network_breakdown or len(network_breakdown) == 1:
            return 0.0

        total_commission = sum(
            net.get("commission", 0) for net in network_breakdown.values()
        )
        if total_commission == 0:
            return 0.0

        # Calculate Herfindahl index for diversification
        shares = [
            (net.get("commission", 0) / total_commission) ** 2
            for net in network_breakdown.values()
        ]
        herfindahl = sum(shares)

        # Convert to diversification score (0-100)
        max_herfindahl = 1.0  # Completely concentrated
        diversification = (1 - herfindahl) * 100

        return round(diversification, 1)

    def _assess_conversion_quality(self, conversion_rate: float) -> str:
        """Assess conversion quality level"""
        if conversion_rate >= 5.0:
            return "exceptional"
        elif conversion_rate >= 3.0:
            return "excellent"
        elif conversion_rate >= 2.0:
            return "good"
        elif conversion_rate >= 1.0:
            return "fair"
        else:
            return "needs_improvement"

    def _assess_revenue_consistency(self, daily_data: List[Dict]) -> str:
        """Assess revenue consistency over time"""
        if len(daily_data) < 7:
            return "insufficient_data"

        daily_commissions = [day.get("commission", 0) for day in daily_data[-7:]]

        if all(c == 0 for c in daily_commissions):
            return "no_revenue"

        # Calculate coefficient of variation
        avg_commission = sum(daily_commissions) / len(daily_commissions)
        if avg_commission == 0:
            return "no_revenue"

        variance = sum((c - avg_commission) ** 2 for c in daily_commissions) / len(
            daily_commissions
        )
        std_dev = variance**0.5
        cv = std_dev / avg_commission

        if cv < 0.3:
            return "very_consistent"
        elif cv < 0.6:
            return "consistent"
        elif cv < 1.0:
            return "moderate"
        else:
            return "volatile"

    def _assess_traffic_quality(self, clicks: int, conversions: int) -> str:
        """Assess traffic quality based on engagement"""
        if clicks == 0:
            return "no_traffic"

        conversion_rate = conversions / clicks * 100

        if conversion_rate >= 4.0:
            return "premium"
        elif conversion_rate >= 2.5:
            return "high"
        elif conversion_rate >= 1.5:
            return "good"
        elif conversion_rate >= 0.5:
            return "average"
        else:
            return "low"

    def _get_demo_affiliate_metrics(self) -> Dict[str, Any]:
        """Generate comprehensive demo affiliate data"""
        import random

        base_clicks = random.randint(2500, 12000)
        base_conversions = random.randint(
            int(base_clicks * 0.01), int(base_clicks * 0.05)
        )
        base_commission = random.uniform(base_conversions * 15, base_conversions * 45)

        conversion_rate = base_conversions / base_clicks * 100
        earnings_per_click = base_commission / base_clicks
        average_commission = (
            base_commission / base_conversions if base_conversions > 0 else 0
        )

        return {
            # Core metrics
            "clicks": base_clicks,
            "conversions": base_conversions,
            "commission": round(base_commission, 2),
            # Performance rates
            "conversion_rate": round(conversion_rate, 2),
            "earnings_per_click": round(earnings_per_click, 3),
            "average_commission": round(average_commission, 2),
            "revenue_per_mille": round(base_commission / base_clicks * 1000, 2),
            # Advanced analytics
            "performance_score": round(random.uniform(65, 92), 1),
            "profitability_tier": random.choice(
                ["advanced", "professional", "developing"]
            ),
            "optimization_potential": random.choice(["moderate", "low", "high"]),
            # Growth metrics
            "monthly_projection": round(base_commission * 1.1, 2),
            "growth_trend": random.choice(["growing", "stable", "accelerating"]),
            "growth_rate": round(random.uniform(-5, 25), 1),
            # Network analysis
            "active_networks": random.randint(3, 8),
            "top_network": random.choice(
                ["ShareASale", "Commission Junction", "ClickBank", "Amazon Associates"]
            ),
            "top_network_commission": round(base_commission * 0.4, 2),
            "network_diversification": round(random.uniform(45, 85), 1),
            # Quality metrics
            "conversion_quality": random.choice(["excellent", "good", "fair"]),
            "revenue_consistency": random.choice(
                ["consistent", "very_consistent", "moderate"]
            ),
            "traffic_quality": random.choice(["high", "good", "premium"]),
            # Metadata
            "last_updated": datetime.datetime.utcnow().isoformat(),
            "analytics_period_days": 30,
            "demo": True,
        }

    def get_archive_history(self, limit: int = 50) -> List[Dict]:
        """Get affiliate analytics archive history"""
        try:
            archive_file = Path("ledger_affiliate.jsonl")
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
            logger.error(f"Error reading affiliate archive: {e}")
            return []


# Standalone functions for dashboard integration
def fetch_affiliate_metrics() -> Dict[str, Any]:
    """Enhanced affiliate metrics - standalone function for dashboard"""
    system = CodexAffiliateCommand()
    return system.fetch_affiliate_metrics()


def archive_affiliate(report: Dict[str, Any]) -> bool:
    """Archive affiliate analytics report"""
    try:
        archive_entry = {"ts": datetime.datetime.utcnow().isoformat(), **report}

        with open("ledger_affiliate.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(archive_entry) + "\n")

        return True

    except Exception as e:
        logger.error(f"Error archiving affiliate data: {e}")
        return False


def get_affiliate_command_summary() -> Dict[str, Any]:
    """Get comprehensive affiliate command summary for dashboard"""
    try:
        system = CodexAffiliateCommand()
        metrics = system.fetch_affiliate_metrics()

        # Add summary metadata
        metrics["system_status"] = "operational"
        metrics["last_check"] = datetime.datetime.utcnow().isoformat()

        return metrics

    except Exception as e:
        logger.error(f"Error getting affiliate summary: {e}")
        return {"error": str(e), "system_status": "error", "demo": True}


if __name__ == "__main__":
    # Test Affiliate Command system
    print("🔥 Testing Affiliate Command Center...")

    affiliate_system = CodexAffiliateCommand()

    # Test connection
    if affiliate_system.test_connection():
        print("✅ Affiliate API Connected!")
    else:
        print("⚠️ Using Demo Data")

    # Test metrics
    metrics = affiliate_system.fetch_affiliate_metrics()
    print(f"👆 Clicks: {metrics['clicks']:,}")
    print(f"🎯 Conversions: {metrics['conversions']:,}")
    print(f"💰 Commission: ${metrics['commission']:.2f}")
    print(f"📈 Conversion Rate: {metrics['conversion_rate']:.2f}%")
    print(f"⚡ Performance Score: {metrics['performance_score']}/100")

    # Test archiving
    success = archive_affiliate(metrics)
    print(f"💾 Archive: {'✅ Success' if success else '❌ Failed'}")
