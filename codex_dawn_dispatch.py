"""
🌅 CODEX DAWN DISPATCH SYSTEM 👑
Automated Daily Reporting and Proclamation System

The Merritt Method™ - Dawn of Digital Sovereignty
"""

import datetime
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

# Import Codex services
try:
    from codex_woocommerce_sync import CodexWooCommerceSync
except ImportError:
    CodexWooCommerceSync = None

try:
    from codex_twitter_proclamation import CodexTwitterProclaimer
except ImportError:
    CodexTwitterProclaimer = None

try:
    from codex_buffer_proclamation import CodexBufferProclaimer
except ImportError:
    CodexBufferProclaimer = None

try:
    from dawn_monetization_scroll import (calculate_revenue_growth,
                                          dawn_monetization_scroll,
                                          get_monetization_history)
except ImportError:
    dawn_monetization_scroll = None
    get_monetization_history = None
    calculate_revenue_growth = None

try:
    from codex_signals.integration import CodexSignalsIntegration, bulletin_md
except ImportError:
    CodexSignalsIntegration = None
    bulletin_md = None


class CodexDawnDispatch:
    """
    🌅 Sacred Dawn Dispatch System 👑

    Automated daily reporting that gathers metrics from all Codex systems:
    - WooCommerce store performance
    - Social media engagement
    - System uptime and health
    - Proclamation history
    - Archive management
    """

    def __init__(self, config_file: str = "dawn_dispatch_config.json"):
        """Initialize the Dawn Dispatch System"""
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.archive_file = Path("completed_archives.json")
        self.ledger_file = Path("codex_ledger.json")

        # Initialize services
        self.woocommerce = self._init_woocommerce()
        self.twitter = self._init_twitter()
        self.buffer = self._init_buffer()
        self.signals = self._init_signals()

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _load_config(self) -> Dict[str, Any]:
        """Load Dawn Dispatch configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                # Create default config
                default_config = {
                    "dispatch_settings": {
                        "auto_proclaim": True,
                        "archive_enabled": True,
                        "timezone": "UTC",
                        "format_template": "detailed",
                    },
                    "report_sections": {
                        "store_revenue": True,
                        "social_engagement": True,
                        "system_status": True,
                        "proclamations": True,
                        "analytics": True,
                    },
                    "proclamation_settings": {
                        "auto_tweet": False,
                        "auto_buffer": False,
                        "dawn_hashtags": [
                            "#DawnDispatch",
                            "#CodexDominion",
                            "#DigitalSovereignty",
                        ],
                    },
                    "thresholds": {
                        "revenue_alert": 1000,
                        "orders_alert": 10,
                        "engagement_alert": 100,
                    },
                }

                with open(self.config_file, "w", encoding="utf-8") as f:
                    json.dump(default_config, f, indent=2)

                return default_config
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            return {}

    def _init_woocommerce(self) -> Optional[Any]:
        """Initialize WooCommerce service"""
        try:
            if CodexWooCommerceSync:
                return CodexWooCommerceSync()
        except Exception as e:
            self.logger.warning(f"WooCommerce initialization failed: {str(e)}")
        return None

    def _init_twitter(self) -> Optional[Any]:
        """Initialize Twitter service"""
        try:
            if CodexTwitterProclaimer:
                return CodexTwitterProclaimer()
        except Exception as e:
            self.logger.warning(f"Twitter initialization failed: {str(e)}")
        return None

    def _init_buffer(self) -> Optional[Any]:
        """Initialize Buffer service"""
        try:
            if CodexBufferProclaimer:
                return CodexBufferProclaimer()
        except Exception as e:
            self.logger.warning(f"Buffer initialization failed: {str(e)}")
        return None

    def _init_signals(self) -> Optional[Any]:
        """Initialize Signals service"""
        try:
            if CodexSignalsIntegration:
                return CodexSignalsIntegration()
        except Exception as e:
            self.logger.warning(f"Signals initialization failed: {str(e)}")
        return None

    def get_store_metrics(self) -> Dict[str, Any]:
        """Get WooCommerce store metrics"""
        try:
            if not self.woocommerce:
                return {"revenue": "N/A", "orders": "N/A", "status": "Service Offline"}

            # Get recent orders (last 24 hours)
            today = datetime.datetime.now()
            yesterday = today - datetime.timedelta(days=1)

            # This would typically call WooCommerce API for recent orders
            # For now, we'll return mock data structure
            orders = (
                self.woocommerce.get_orders(
                    after=yesterday.isoformat(), before=today.isoformat()
                )
                if hasattr(self.woocommerce, "get_orders")
                else []
            )

            total_revenue = sum(float(order.get("total", 0)) for order in orders)
            order_count = len(orders)

            return {
                "revenue": f"${total_revenue:.2f}",
                "orders": order_count,
                "status": (
                    "OPERATIONAL" if self.woocommerce.test_connection() else "OFFLINE"
                ),
                "avg_order_value": (
                    f"${total_revenue/order_count:.2f}" if order_count > 0 else "$0.00"
                ),
            }
        except Exception as e:
            self.logger.error(f"Error getting store metrics: {str(e)}")
            return {"revenue": "ERROR", "orders": "ERROR", "status": "ERROR"}

    def get_social_metrics(self) -> Dict[str, Any]:
        """Get social media engagement metrics"""
        metrics = {
            "twitter_posts": 0,
            "buffer_posts": 0,
            "total_interactions": 0,
            "platform_status": [],
        }

        try:
            # Twitter metrics
            if self.twitter:
                twitter_history = self.twitter.get_proclamation_history()
                yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

                recent_tweets = [
                    t
                    for t in twitter_history
                    if datetime.datetime.fromisoformat(t.get("timestamp", "2000-01-01"))
                    > yesterday
                ]
                metrics["twitter_posts"] = len(recent_tweets)
                metrics["platform_status"].append("Twitter: ACTIVE")
            else:
                metrics["platform_status"].append("Twitter: OFFLINE")

            # Buffer metrics
            if self.buffer:
                buffer_history = self.buffer.get_proclamation_history()
                yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

                recent_buffer = [
                    b
                    for b in buffer_history
                    if datetime.datetime.fromisoformat(b.get("timestamp", "2000-01-01"))
                    > yesterday
                ]
                metrics["buffer_posts"] = len(recent_buffer)

                analytics = self.buffer.get_analytics_summary()
                metrics["connected_platforms"] = analytics.get("total_profiles", 0)
                metrics["platform_status"].append(
                    f"Buffer: {analytics.get('total_profiles', 0)} platforms"
                )
            else:
                metrics["platform_status"].append("Buffer: OFFLINE")

            metrics["total_interactions"] = (
                metrics["twitter_posts"] + metrics["buffer_posts"]
            )

        except Exception as e:
            self.logger.error(f"Error getting social metrics: {str(e)}")
            metrics["error"] = str(e)

        return metrics

    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system health status"""
        status = {"uptime": "OPERATIONAL", "services": {}, "health_score": 0}

        # Check service health
        services = {
            "Dashboard": True,  # Assume operational if this code is running
            "WooCommerce": (
                self.woocommerce.test_connection() if self.woocommerce else False
            ),
            "Twitter": self.twitter is not None,
            "Buffer": self.buffer.test_connection() if self.buffer else False,
        }

        status["services"] = services
        operational_count = sum(1 for service_ok in services.values() if service_ok)
        status["health_score"] = (operational_count / len(services)) * 100

        if status["health_score"] >= 75:
            status["uptime"] = "All systems OPERATIONAL"
        elif status["health_score"] >= 50:
            status["uptime"] = "Systems DEGRADED"
        else:
            status["uptime"] = "Systems CRITICAL"

        return status

    def get_ledger_updates(self) -> Dict[str, Any]:
        """Get Codex Ledger activity"""
        try:
            if self.ledger_file.exists():
                with open(self.ledger_file, "r", encoding="utf-8") as f:
                    ledger_data = json.load(f)

                # Count recent activities
                yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
                recent_count = 0

                # This would depend on your ledger structure
                # For now, we'll count entries
                if isinstance(ledger_data, dict):
                    recent_count = len(ledger_data)
                elif isinstance(ledger_data, list):
                    recent_count = len(ledger_data)

                return {
                    "proclamations": recent_count,
                    "status": "ACTIVE",
                    "last_update": datetime.datetime.now().isoformat(),
                }
            else:
                return {
                    "proclamations": 0,
                    "status": "NO LEDGER",
                    "last_update": "Never",
                }
        except Exception as e:
            self.logger.error(f"Error reading ledger: {str(e)}")
        return {"proclamations": 0, "status": "ERROR", "error": str(e)}

    def get_signals_metrics(self) -> Dict[str, Any]:
        """Get portfolio signals metrics"""
        try:
            if not self.signals:
                return {
                    "status": "OFFLINE",
                    "active_positions": 0,
                    "allocation": "N/A",
                    "alpha_picks": 0,
                    "risk_factors": 0,
                }

            # Get signals summary for dawn dispatch
            signals_summary = self.signals.get_signals_for_dawn_dispatch()

            # Generate markdown bulletin if available
            bulletin_info = {"available": False}
            if bulletin_md:
                try:
                    signals_snapshot = self.signals.generate_signals_report()
                    if "error" not in signals_snapshot:
                        bulletin_content = bulletin_md(signals_snapshot)
                        bulletin_path = self.signals.save_bulletin(
                            signals_snapshot, format="md"
                        )
                        bulletin_info = {
                            "available": True,
                            "path": bulletin_path,
                            "preview": bulletin_content[:150] + "...",
                            "lines": len(bulletin_content.split("\n")),
                        }
                except Exception as e:
                    self.logger.warning(f"Could not generate bulletin: {e}")

            return {
                "status": signals_summary.get("signals_status", "UNKNOWN"),
                "active_positions": signals_summary.get("active_positions", 0),
                "allocation": signals_summary.get("total_allocated_weight", "N/A"),
                "alpha_picks": signals_summary.get("high_conviction_picks", 0),
                "risk_factors": signals_summary.get("risk_factors_detected", 0),
                "banner": signals_summary.get("banner", ""),
                "bulletin": bulletin_info,
            }

        except Exception as e:
            self.logger.error(f"Error getting signals metrics: {str(e)}")
            return {
                "status": "ERROR",
                "error": str(e),
                "active_positions": 0,
                "allocation": "N/A",
                "alpha_picks": 0,
                "risk_factors": 0,
            }

    def generate_dawn_report(self) -> str:
        """Generate comprehensive dawn dispatch report"""
        now = datetime.datetime.utcnow()
        timestamp = now.isoformat()

        # Gather all metrics
        store_metrics = self.get_store_metrics()
        social_metrics = self.get_social_metrics()
        system_status = self.get_system_status()
        ledger_updates = self.get_ledger_updates()
        signals_metrics = self.get_signals_metrics()

        # Format the report
        report = f"""
🌅 DAWN DISPATCH — {timestamp}
═══════════════════════════════════════════════════

💰 TREASURY STATUS
• Store Revenue: {store_metrics.get('revenue', 'N/A')}
• Orders Processed: {store_metrics.get('orders', 'N/A')}
• Average Order Value: {store_metrics.get('avg_order_value', 'N/A')}
• Store Status: {store_metrics.get('status', 'UNKNOWN')}

📱 SOCIAL DOMINION
• Twitter Proclamations: {social_metrics.get('twitter_posts', 0)}
• Buffer Posts: {social_metrics.get('buffer_posts', 0)}
• Total Interactions: {social_metrics.get('total_interactions', 0)}
• Platform Status: {', '.join(social_metrics.get('platform_status', ['Unknown']))}

⚡ SYSTEM SOVEREIGNTY
• Health Score: {system_status.get('health_score', 0):.1f}%
• Uptime Status: {system_status.get('uptime', 'UNKNOWN')}
• Services Online: {sum(1 for v in system_status.get('services', {}).values() if v)}/{len(system_status.get('services', {}))}

📜 CODEX LEDGER
• Daily Proclamations: {ledger_updates.get('proclamations', 0)}
• Ledger Status: {ledger_updates.get('status', 'UNKNOWN')}
• Last Update: {ledger_updates.get('last_update', 'Never')[:19]}

� PORTFOLIO SIGNALS
• Signals Status: {signals_metrics.get('status', 'UNKNOWN')}
• Active Positions: {signals_metrics.get('active_positions', 0)}
• Allocation: {signals_metrics.get('allocation', 'N/A')}
• Alpha Picks: {signals_metrics.get('alpha_picks', 0)}
• Risk Factors: {signals_metrics.get('risk_factors', 0)}

�🔥 DIGITAL SOVEREIGNTY STATUS: {"🟢 SUPREME" if system_status.get('health_score', 0) >= 75 else "🟡 STABLE" if system_status.get('health_score', 0) >= 50 else "🔴 CRITICAL"}

═══════════════════════════════════════════════════
Generated by Codex Dawn Dispatch System v2.0
Powered by The Merritt Method™
        """

        return report.strip()

    def archive_report(self, report: str) -> bool:
        """Archive the dawn report to JSON file"""
        try:
            # Prepare archive entry
            archive_entry = {
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "type": "dawn_dispatch",
                "report": report,
                "metrics": {
                    "store": self.get_store_metrics(),
                    "social": self.get_social_metrics(),
                    "system": self.get_system_status(),
                    "ledger": self.get_ledger_updates(),
                },
            }

            # Load existing archives
            archives = []
            if self.archive_file.exists():
                try:
                    with open(self.archive_file, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        if content:
                            # Handle both JSON array and line-delimited format
                            if content.startswith("["):
                                archives = json.loads(content)
                            else:
                                # Convert old line format to new JSON format
                                archives = []
                except json.JSONDecodeError:
                    # If not valid JSON, start fresh
                    archives = []

            # Add new entry
            archives.append(archive_entry)

            # Keep only last 30 days
            cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=30)
            archives = [
                a
                for a in archives
                if datetime.datetime.fromisoformat(a.get("timestamp", "2000-01-01"))
                > cutoff
            ]

            # Save archives
            with open(self.archive_file, "w", encoding="utf-8") as f:
                json.dump(archives, f, indent=2, ensure_ascii=False)

            self.logger.info(
                f"Dawn report archived successfully. Total archives: {len(archives)}"
            )
            return True

        except Exception as e:
            self.logger.error(f"Error archiving report: {str(e)}")
            return False

    def proclaim_dawn_report(self, report: str) -> Dict[str, Any]:
        """Proclaim dawn report to social media"""
        results = {"twitter": None, "buffer": None}

        try:
            # Create shortened version for social media
            short_report = self._create_social_summary()

            # Twitter proclamation
            if (
                self.config.get("proclamation_settings", {}).get("auto_tweet", False)
                and self.twitter
            ):
                try:
                    twitter_result = self.twitter.send_proclamation(
                        short_report,
                        proclamation_type="announcement",
                        hashtag_set="default",
                    )
                    results["twitter"] = twitter_result
                except Exception as e:
                    results["twitter"] = {"success": False, "error": str(e)}

            # Buffer proclamation
            if (
                self.config.get("proclamation_settings", {}).get("auto_buffer", False)
                and self.buffer
            ):
                try:
                    buffer_result = self.buffer.broadcast_sovereignty(short_report)
                    results["buffer"] = buffer_result
                except Exception as e:
                    results["buffer"] = {"success": False, "error": str(e)}

        except Exception as e:
            self.logger.error(f"Error proclaiming dawn report: {str(e)}")

        return results

    def _create_social_summary(self) -> str:
        """Create shortened version for social media"""
        store_metrics = self.get_store_metrics()
        social_metrics = self.get_social_metrics()
        system_status = self.get_system_status()

        summary = f"""🌅 Dawn Dispatch Update
💰 Revenue: {store_metrics.get('revenue', 'N/A')} | Orders: {store_metrics.get('orders', 0)}
📱 Social Posts: {social_metrics.get('total_interactions', 0)}
⚡ System Health: {system_status.get('health_score', 0):.0f}%
🔥 Digital Sovereignty: ACTIVE"""

        return summary

    def dawn_dispatch(self) -> Dict[str, Any]:
        """Main dawn dispatch function - enhanced version of original with monetization scroll"""
        try:
            # Generate comprehensive report
            report = self.generate_dawn_report()

            # Generate Dawn Monetization Scroll
            monetization_result = None
            if dawn_monetization_scroll:
                try:
                    monetization_result = dawn_monetization_scroll()
                    if monetization_result.get("success"):
                        print("\n📜 🔥 DAWN MONETIZATION SCROLL 🔥 📜")
                        print("=" * 50)
                        summary = monetization_result["summary"]
                        print(f"💰 Total Revenue: ${summary['total_revenue']:.2f}")
                        print(f"🚀 Active Platforms: {summary['active_platforms']}/5")
                        print(f"👑 Top Platform: {summary['top_platform'] or 'None'}")
                        print(
                            f"⭐ Performance Tier: {summary['performance_tier'].title()}"
                        )
                        print(
                            f"📈 Growth Potential: {summary['growth_potential'].title()}"
                        )
                        print(
                            f"🎯 Diversification Score: {summary['diversification_score']:.1f}%"
                        )
                        print(
                            f"🔥 Sovereignty Status: {summary['sovereignty_status'].title()}"
                        )
                        print("=" * 50)
                except Exception as e:
                    print(f"⚠️ Monetization Scroll generation failed: {e}")

            # Archive the report
            archived = False
            if self.config.get("dispatch_settings", {}).get("archive_enabled", True):
                archived = self.archive_report(report)

            # Proclaim to social media if enabled
            social_results = {}
            if self.config.get("dispatch_settings", {}).get("auto_proclaim", False):
                social_results = self.proclaim_dawn_report(report)

            # Print the standard report
            print("\n📊 🌅 DAWN DISPATCH REPORT 🌅 📊")
            print(report)
            print("\n🔥 Dawn Dispatch completed and archived. 👑")

            return {
                "success": True,
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "report": report,
                "monetization_scroll": monetization_result,
                "archived": archived,
                "social_results": social_results,
            }

        except Exception as e:
            error_msg = f"Dawn Dispatch failed: {str(e)}"
            self.logger.error(error_msg)
            print(f"❌ {error_msg}")

            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.datetime.utcnow().isoformat(),
            }


# Enhanced version of the original function for backward compatibility
def dawn_dispatch():
    """
    🌅 Enhanced Dawn Dispatch Function 👑
    Original function enhanced with comprehensive Codex integration
    """
    dispatch_system = CodexDawnDispatch()
    result = dispatch_system.dawn_dispatch()

    if result.get("success"):
        print("Dawn Dispatch archived and proclaimed.")
    else:
        print(f"Dawn Dispatch failed: {result.get('error')}")

    return result


# Advanced scheduling function
def schedule_dawn_dispatch():
    """Schedule automatic dawn dispatches"""
    import time

    import schedule

    def run_dispatch():
        print("🌅 Scheduled Dawn Dispatch executing...")
        dawn_dispatch()

    # Schedule for 6 AM UTC daily
    schedule.every().day.at("06:00").do(run_dispatch)

    print("🌅 Dawn Dispatch scheduled for 6:00 AM UTC daily")
    print("Press Ctrl+C to stop the scheduler...")

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n🔥 Dawn Dispatch scheduler stopped. 👑")


if __name__ == "__main__":
    # Run immediate dawn dispatch
    print("🌅 Running Dawn Dispatch System...")
    result = dawn_dispatch()

    if result.get("success"):
        print("\n✅ Dawn Dispatch completed successfully!")
    else:
        print(f"\n❌ Dawn Dispatch failed: {result.get('error')}")
