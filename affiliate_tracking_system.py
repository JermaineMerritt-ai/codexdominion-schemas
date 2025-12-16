#!/usr/bin/env python3
"""
Affiliate Marketing Tracking System - Real Platform Integration
================================================================

Integrates with major affiliate networks:
- Amazon Associates
- ClickBank
- ShareASale
- CJ Affiliate (Commission Junction)
- Impact
- Rakuten Advertising

Features:
- Automated link generation with tracking
- Click tracking and conversion analytics
- Commission reporting
- Product search and recommendations
- Deep link creation
- Performance dashboards
"""

import json
import os
import hashlib
import hmac
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from urllib.parse import urlencode, quote
import requests


# =============================================================================
# AFFILIATE CONFIGURATION
# =============================================================================

class AffiliateConfig:
    """Manage affiliate network credentials"""

    def __init__(self):
        self.config_file = "affiliate_config.json"
        self.load_config()

    def load_config(self):
        """Load affiliate credentials"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = self.get_default_config()
            self.save_config()

    def save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get_default_config(self) -> Dict:
        """Default configuration structure"""
        return {
            "amazon": {
                "access_key": os.getenv("AMAZON_ACCESS_KEY", ""),
                "secret_key": os.getenv("AMAZON_SECRET_KEY", ""),
                "partner_tag": os.getenv("AMAZON_PARTNER_TAG", ""),
                "marketplace": "US",
                "enabled": False
            },
            "clickbank": {
                "api_key": os.getenv("CLICKBANK_API_KEY", ""),
                "account_nickname": os.getenv("CLICKBANK_ACCOUNT", ""),
                "enabled": False
            },
            "shareasale": {
                "api_token": os.getenv("SHAREASALE_API_TOKEN", ""),
                "api_secret": os.getenv("SHAREASALE_API_SECRET", ""),
                "affiliate_id": os.getenv("SHAREASALE_AFFILIATE_ID", ""),
                "enabled": False
            },
            "cj": {
                "website_id": os.getenv("CJ_WEBSITE_ID", ""),
                "personal_access_token": os.getenv("CJ_ACCESS_TOKEN", ""),
                "enabled": False
            },
            "impact": {
                "account_sid": os.getenv("IMPACT_ACCOUNT_SID", ""),
                "auth_token": os.getenv("IMPACT_AUTH_TOKEN", ""),
                "enabled": False
            },
            "tracking": {
                "database_file": "affiliate_tracking.json",
                "utm_source": "codexdominion",
                "utm_medium": "affiliate",
                "default_campaign": "2025q1"
            }
        }


# =============================================================================
# AMAZON ASSOCIATES API
# =============================================================================

class AmazonAffiliateAPI:
    """Amazon Product Advertising API 5.0"""

    def __init__(self, config: Dict):
        self.config = config
        self.base_url = "https://webservices.amazon.com/paapi5"
        self.access_key = config.get("access_key", "")
        self.secret_key = config.get("secret_key", "")
        self.partner_tag = config.get("partner_tag", "")
        self.marketplace = config.get("marketplace", "US")

    def generate_affiliate_link(self, asin: str, custom_id: str = "") -> str:
        """Generate Amazon affiliate link"""
        base_url = "https://www.amazon.com/dp/"
        params = {
            "tag": self.partner_tag,
            "linkCode": "osi",
            "th": "1",
            "psc": "1"
        }

        if custom_id:
            params["custId"] = custom_id

        return f"{base_url}{asin}?{urlencode(params)}"

    def search_products(self, keywords: str, category: str = "All") -> Dict:
        """Search for products (requires PA-API 5.0)"""
        # Note: Actual implementation requires AWS signature v4
        return {
            "success": False,
            "error": "PA-API 5.0 requires AWS signature authentication",
            "note": "Use generate_affiliate_link() with known ASINs"
        }

    def get_product_details(self, asin: str) -> Dict:
        """Get product details"""
        return {
            "success": False,
            "error": "Requires PA-API 5.0 authentication",
            "affiliate_link": self.generate_affiliate_link(asin)
        }


# =============================================================================
# CLICKBANK API
# =============================================================================

class ClickBankAPI:
    """ClickBank API integration"""

    def __init__(self, config: Dict):
        self.config = config
        self.base_url = "https://api.clickbank.com/rest/1.3"
        self.api_key = config.get("api_key", "")
        self.account = config.get("account_nickname", "")

    def generate_hoplink(self, vendor: str, product_id: str, tracking_id: str = "") -> str:
        """Generate ClickBank HopLink"""
        base_url = f"https://{vendor}.{product_id}.hop.clickbank.net"

        if tracking_id:
            return f"{base_url}?tid={tracking_id}"
        return base_url

    def search_marketplace(self, keywords: str, category: str = "") -> Dict:
        """Search ClickBank marketplace"""
        url = f"{self.base_url}/products"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"query": keywords}

        if category:
            params["category"] = category

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def get_product_info(self, product_id: str) -> Dict:
        """Get product information"""
        url = f"{self.base_url}/products/{product_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            product_data = response.json()

            # Add generated hoplink
            product_data["hoplink"] = self.generate_hoplink(
                product_data.get("vendor", ""),
                product_id
            )

            return {"success": True, "data": product_data}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}


# =============================================================================
# SHAREASALE API
# =============================================================================

class ShareASaleAPI:
    """ShareASale API integration"""

    def __init__(self, config: Dict):
        self.config = config
        self.base_url = "https://api.shareasale.com/w.cfm"
        self.api_token = config.get("api_token", "")
        self.api_secret = config.get("api_secret", "")
        self.affiliate_id = config.get("affiliate_id", "")

    def generate_signature(self, action: str, timestamp: str) -> str:
        """Generate API signature"""
        sig_string = f"{self.api_token}:{timestamp}:{action}:{self.api_secret}"
        return hashlib.sha256(sig_string.encode()).hexdigest()

    def generate_affiliate_link(self, merchant_id: str, product_url: str,
                                tracking_code: str = "") -> str:
        """Generate ShareASale affiliate link"""
        base_url = "https://shareasale.com/m-pr.cfm"
        params = {
            "merchantID": merchant_id,
            "userID": self.affiliate_id,
            "productURL": product_url
        }

        if tracking_code:
            params["tracking"] = tracking_code

        return f"{base_url}?{urlencode(params)}"

    def get_merchant_list(self) -> Dict:
        """Get list of merchants"""
        action = "merchantList"
        timestamp = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        signature = self.generate_signature(action, timestamp)

        headers = {
            "x-ShareASale-Date": timestamp,
            "x-ShareASale-Authentication": signature
        }

        params = {
            "affiliateId": self.affiliate_id,
            "token": self.api_token,
            "version": "2.4",
            "action": action
        }

        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            return {"success": True, "data": response.text}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}


# =============================================================================
# CJ AFFILIATE API
# =============================================================================

class CJAffiliateAPI:
    """Commission Junction (CJ) Affiliate API"""

    def __init__(self, config: Dict):
        self.config = config
        self.base_url = "https://advertiser-lookup.api.cj.com/v2"
        self.website_id = config.get("website_id", "")
        self.access_token = config.get("personal_access_token", "")

    def search_advertisers(self, keywords: str) -> Dict:
        """Search for advertisers"""
        url = f"{self.base_url}/advertiser-lookup"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        params = {
            "keywords": keywords,
            "advertiser-ids": "joined"
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def generate_deep_link(self, destination_url: str, website_id: str = "") -> str:
        """Generate CJ deep link"""
        if not website_id:
            website_id = self.website_id

        # CJ deep link format
        base_url = "https://www.anrdoezrs.net/links"
        return f"{base_url}/{website_id}/type/dlg/{destination_url}"


# =============================================================================
# AFFILIATE TRACKING SYSTEM
# =============================================================================

class AffiliateTracker:
    """Track affiliate clicks and conversions"""

    def __init__(self, database_file: str = "affiliate_tracking.json"):
        self.database_file = database_file
        self.load_data()

    def load_data(self):
        """Load tracking data"""
        if os.path.exists(self.database_file):
            with open(self.database_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "clicks": [],
                "conversions": [],
                "earnings": [],
                "stats": {
                    "total_clicks": 0,
                    "total_conversions": 0,
                    "total_earnings": 0.0,
                    "conversion_rate": 0.0
                }
            }

    def save_data(self):
        """Save tracking data"""
        with open(self.database_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def track_click(self, platform: str, product_id: str, affiliate_link: str,
                    source: str = "", campaign: str = "") -> str:
        """Track affiliate link click"""
        click_id = hashlib.md5(
            f"{datetime.now().isoformat()}{platform}{product_id}".encode()
        ).hexdigest()[:12]

        click_data = {
            "click_id": click_id,
            "platform": platform,
            "product_id": product_id,
            "affiliate_link": affiliate_link,
            "source": source,
            "campaign": campaign,
            "timestamp": datetime.now().isoformat(),
            "converted": False
        }

        self.data["clicks"].append(click_data)
        self.data["stats"]["total_clicks"] += 1
        self.save_data()

        return click_id

    def track_conversion(self, click_id: str, commission: float, order_id: str = "") -> bool:
        """Track conversion"""
        for click in self.data["clicks"]:
            if click["click_id"] == click_id:
                click["converted"] = True
                click["conversion_timestamp"] = datetime.now().isoformat()

                conversion_data = {
                    "click_id": click_id,
                    "commission": commission,
                    "order_id": order_id,
                    "timestamp": datetime.now().isoformat(),
                    "platform": click["platform"]
                }

                self.data["conversions"].append(conversion_data)
                self.data["stats"]["total_conversions"] += 1
                self.data["stats"]["total_earnings"] += commission
                self.update_conversion_rate()
                self.save_data()

                return True
        return False

    def update_conversion_rate(self):
        """Update conversion rate"""
        if self.data["stats"]["total_clicks"] > 0:
            rate = (self.data["stats"]["total_conversions"] /
                   self.data["stats"]["total_clicks"]) * 100
            self.data["stats"]["conversion_rate"] = round(rate, 2)

    def get_stats(self, days: int = 30) -> Dict:
        """Get statistics for last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)

        recent_clicks = [
            c for c in self.data["clicks"]
            if datetime.fromisoformat(c["timestamp"]) > cutoff_date
        ]

        recent_conversions = [
            c for c in self.data["conversions"]
            if datetime.fromisoformat(c["timestamp"]) > cutoff_date
        ]

        total_earnings = sum(c["commission"] for c in recent_conversions)
        conversion_rate = 0.0

        if len(recent_clicks) > 0:
            conversion_rate = (len(recent_conversions) / len(recent_clicks)) * 100

        return {
            "period_days": days,
            "total_clicks": len(recent_clicks),
            "total_conversions": len(recent_conversions),
            "total_earnings": round(total_earnings, 2),
            "conversion_rate": round(conversion_rate, 2),
            "average_commission": round(total_earnings / max(len(recent_conversions), 1), 2)
        }


# =============================================================================
# UNIFIED AFFILIATE MANAGER
# =============================================================================

class AffiliateManager:
    """Unified affiliate marketing manager"""

    def __init__(self):
        self.config_manager = AffiliateConfig()
        self.tracker = AffiliateTracker()
        self.initialize_apis()

    def initialize_apis(self):
        """Initialize API clients"""
        self.apis = {}

        config = self.config_manager.config

        if config["amazon"].get("enabled"):
            self.apis["amazon"] = AmazonAffiliateAPI(config["amazon"])

        if config["clickbank"].get("enabled"):
            self.apis["clickbank"] = ClickBankAPI(config["clickbank"])

        if config["shareasale"].get("enabled"):
            self.apis["shareasale"] = ShareASaleAPI(config["shareasale"])

        if config["cj"].get("enabled"):
            self.apis["cj"] = CJAffiliateAPI(config["cj"])

    def generate_tracked_link(self, platform: str, product_id: str,
                             **kwargs) -> Dict:
        """Generate affiliate link with tracking"""
        if platform not in self.apis:
            return {"success": False, "error": f"Platform {platform} not enabled"}

        api = self.apis[platform]

        try:
            if platform == "amazon":
                link = api.generate_affiliate_link(product_id, kwargs.get("custom_id", ""))
            elif platform == "clickbank":
                link = api.generate_hoplink(
                    kwargs.get("vendor", ""),
                    product_id,
                    kwargs.get("tracking_id", "")
                )
            elif platform == "shareasale":
                link = api.generate_affiliate_link(
                    kwargs.get("merchant_id", ""),
                    kwargs.get("product_url", ""),
                    kwargs.get("tracking_code", "")
                )
            elif platform == "cj":
                link = api.generate_deep_link(kwargs.get("destination_url", ""))
            else:
                return {"success": False, "error": "Platform not implemented"}

            # Track the link generation
            click_id = self.tracker.track_click(
                platform=platform,
                product_id=product_id,
                affiliate_link=link,
                source=kwargs.get("source", ""),
                campaign=kwargs.get("campaign", "")
            )

            return {
                "success": True,
                "platform": platform,
                "affiliate_link": link,
                "click_id": click_id,
                "tracking_enabled": True
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_dashboard_stats(self, days: int = 30) -> Dict:
        """Get affiliate dashboard statistics"""
        stats = self.tracker.get_stats(days)
        stats["enabled_platforms"] = list(self.apis.keys())
        stats["total_platforms"] = len(self.apis)

        return stats

    def record_conversion(self, click_id: str, commission: float,
                         order_id: str = "") -> Dict:
        """Record a conversion"""
        success = self.tracker.track_conversion(click_id, commission, order_id)

        if success:
            return {
                "success": True,
                "message": "Conversion tracked successfully",
                "click_id": click_id,
                "commission": commission
            }
        else:
            return {
                "success": False,
                "error": "Click ID not found"
            }


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """Main CLI interface"""
    print("=" * 70)
    print("AFFILIATE MARKETING TRACKING SYSTEM")
    print("=" * 70)

    manager = AffiliateManager()
    stats = manager.get_dashboard_stats(30)

    print(f"\n📊 30-Day Statistics:")
    print(f"   Total Clicks: {stats['total_clicks']}")
    print(f"   Conversions: {stats['total_conversions']}")
    print(f"   Earnings: ${stats['total_earnings']:,.2f}")
    print(f"   Conversion Rate: {stats['conversion_rate']}%")
    print(f"   Avg Commission: ${stats['average_commission']:,.2f}")

    print(f"\n🔗 Enabled Platforms: {stats['enabled_platforms']}")
    print(f"   Total Active: {stats['total_platforms']}")

    print("\nTo enable platforms, configure affiliate_config.json")

    print("\nExample usage:")
    print("  manager = AffiliateManager()")
    print("  result = manager.generate_tracked_link('amazon', 'B08N5WRWNW')")
    print("  print(result['affiliate_link'])")


if __name__ == "__main__":
    main()
