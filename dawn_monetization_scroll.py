"""
🔥 DAWN MONETIZATION SCROLL 📜
Unified Multi-Platform Monetization Report Generator

The Merritt Method™ - Complete Revenue Analytics Sovereignty
"""

import os
import datetime
import json
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def dawn_monetization_scroll():
    """
    🔥 Dawn Monetization Scroll - Complete Multi-Platform Revenue Analytics
    
    Reads the latest entries from all platform JSONL ledgers and produces 
    a comprehensive monetization report with revenue insights, trend analysis, 
    and performance scoring across all creator economy platforms.
    
    Returns:
        dict: Comprehensive monetization report with analytics
    """
    
    def tail(path, n=1):
        """Read the last n entries from a JSONL file"""
        try:
            file_path = Path(path)
            if not file_path.exists():
                logger.warning(f"Ledger file not found: {path}")
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if not lines:
                    return []
                
                # Parse the last n lines as JSON
                entries = []
                for line in lines[-n:]:
                    try:
                        entry = json.loads(line.strip())
                        entries.append(entry)
                    except json.JSONDecodeError as e:
                        logger.warning(f"Failed to parse JSON line in {path}: {e}")
                        continue
                
                return entries
                
        except Exception as e:
            logger.error(f"Error reading ledger {path}: {e}")
            return []
    
    def calculate_platform_revenue(platform_data, platform_name):
        """Calculate revenue metrics for a specific platform"""
        if not platform_data:
            return {
                "revenue": 0,
                "status": "no_data",
                "last_update": None,
                "performance_score": 0
            }
        
        latest_entry = platform_data[-1] if platform_data else {}
        
        # Revenue extraction based on platform type
        revenue = 0
        performance_score = 0
        
        if platform_name == "youtube":
            revenue = latest_entry.get("estimated_revenue", 0)
            performance_score = latest_entry.get("creator_score", 0)
        elif platform_name == "tiktok":
            revenue = latest_entry.get("creator_fund_earnings", 0)
            performance_score = latest_entry.get("engagement_score", 0)
        elif platform_name == "threads":
            revenue = latest_entry.get("monetization_potential", 0)
            performance_score = latest_entry.get("community_score", 0)
        elif platform_name == "whatsapp":
            revenue = latest_entry.get("estimated_revenue", 0) - latest_entry.get("messaging_cost_usd", 0)
            performance_score = latest_entry.get("business_performance_score", 0)
        elif platform_name == "pinterest":
            revenue = latest_entry.get("affiliate_revenue", 0)
            performance_score = latest_entry.get("performance_score", 0)
        elif platform_name == "affiliate":
            revenue = latest_entry.get("commission", 0)
            performance_score = latest_entry.get("performance_score", 0)
        
        return {
            "revenue": revenue,
            "status": "active" if revenue > 0 else "inactive",
            "last_update": latest_entry.get("ts") or latest_entry.get("last_updated"),
            "performance_score": performance_score,
            "raw_data": latest_entry
        }
    
    def generate_monetization_insights(platform_revenues):
        """Generate comprehensive monetization insights"""
        total_revenue = sum(p["revenue"] for p in platform_revenues.values())
        active_platforms = sum(1 for p in platform_revenues.values() if p["status"] == "active")
        avg_performance = sum(p["performance_score"] for p in platform_revenues.values()) / len(platform_revenues) if platform_revenues else 0
        
        # Determine top performing platform
        top_platform = max(platform_revenues.items(), key=lambda x: x[1]["revenue"]) if platform_revenues else (None, {"revenue": 0})
        
        # Revenue distribution analysis
        revenue_distribution = {}
        if total_revenue > 0:
            for platform, data in platform_revenues.items():
                percentage = (data["revenue"] / total_revenue) * 100
                revenue_distribution[platform] = round(percentage, 1)
        
        # Performance tier classification
        if total_revenue >= 1000:
            tier = "elite"
        elif total_revenue >= 500:
            tier = "advanced"
        elif total_revenue >= 100:
            tier = "growing"
        elif total_revenue >= 10:
            tier = "emerging"
        else:
            tier = "startup"
        
        # Growth potential assessment
        growth_potential = "high" if avg_performance > 75 else "moderate" if avg_performance > 50 else "developing"
        
        return {
            "total_revenue": round(total_revenue, 2),
            "active_platforms": active_platforms,
            "average_performance_score": round(avg_performance, 1),
            "top_platform": top_platform[0] if top_platform[0] else None,
            "top_platform_revenue": round(top_platform[1]["revenue"], 2),
            "revenue_distribution": revenue_distribution,
            "performance_tier": tier,
            "growth_potential": growth_potential,
            "diversification_score": round((active_platforms / 6) * 100, 1)  # Updated for 6 platforms including affiliate
        }
    
    try:
        # Read latest entries from all platform ledgers
        logger.info("🔥 Generating Dawn Monetization Scroll...")
        
        raw_report = {
            "youtube": tail("ledger_youtube.jsonl"),
            "tiktok": tail("ledger_tiktok.jsonl"),
            "threads": tail("ledger_threads.jsonl"),
            "whatsapp": tail("ledger_whatsapp.jsonl"),
            "pinterest": tail("ledger_pinterest.jsonl"),
            "affiliate": tail("ledger_affiliate.jsonl"),
        }
        
        # Calculate revenue metrics for each platform
        platform_revenues = {}
        for platform, data in raw_report.items():
            platform_revenues[platform] = calculate_platform_revenue(data, platform)
        
        # Generate comprehensive insights
        insights = generate_monetization_insights(platform_revenues)
        
        # Compile final monetization report
        monetization_report = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "report_type": "dawn_monetization_scroll",
            "platforms": platform_revenues,
            "insights": insights,
            "raw_ledger_data": raw_report,
            "report_id": f"dawn_{int(datetime.datetime.utcnow().timestamp())}",
            "sovereignty_status": "active" if insights["total_revenue"] > 0 else "building"
        }
        
        # Archive the monetization report
        try:
            archive_entry = {
                "ts": datetime.datetime.utcnow().isoformat(),
                "monetization": monetization_report
            }
            
            with open("completed_archives.jsonl", "a", encoding='utf-8') as f:
                f.write(json.dumps(archive_entry) + "\n")
            
            logger.info("✅ Dawn Monetization Scroll archived successfully")
            
        except Exception as e:
            logger.error(f"Error archiving monetization report: {e}")
        
        # Generate summary report for display
        summary = {
            "total_revenue": insights["total_revenue"],
            "active_platforms": insights["active_platforms"],
            "top_platform": insights["top_platform"],
            "performance_tier": insights["performance_tier"],
            "growth_potential": insights["growth_potential"],
            "diversification_score": insights["diversification_score"],
            "sovereignty_status": monetization_report["sovereignty_status"],
            "last_generated": monetization_report["timestamp"]
        }
        
        logger.info(f"🔥 Dawn Monetization Scroll completed - Total Revenue: ${insights['total_revenue']:.2f}")
        
        return {
            "success": True,
            "report": monetization_report,
            "summary": summary,
            "message": "Dawn Monetization Scroll generated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error generating Dawn Monetization Scroll: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to generate Dawn Monetization Scroll"
        }

def get_monetization_history(limit=10):
    """Get historical monetization reports from completed archives"""
    try:
        archive_file = Path("completed_archives.jsonl")
        if not archive_file.exists():
            return []
        
        history = []
        with open(archive_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if entry.get("monetization"):
                        history.append(entry)
                except json.JSONDecodeError:
                    continue
        
        # Sort by timestamp, most recent first
        history.sort(key=lambda x: x.get('ts', ''), reverse=True)
        return history[:limit]
        
    except Exception as e:
        logger.error(f"Error reading monetization history: {e}")
        return []

def calculate_revenue_growth(current_revenue, historical_data):
    """Calculate revenue growth from historical data"""
    if len(historical_data) < 2:
        return 0
    
    try:
        previous_revenue = historical_data[1]["monetization"]["insights"]["total_revenue"]
        if previous_revenue == 0:
            return 0
        
        growth_rate = ((current_revenue - previous_revenue) / previous_revenue) * 100
        return round(growth_rate, 1)
        
    except (KeyError, ZeroDivisionError, IndexError):
        return 0

def generate_revenue_forecast(historical_data, periods=3):
    """Generate simple revenue forecast based on historical trends"""
    if len(historical_data) < 2:
        return {"forecast": [], "trend": "insufficient_data"}
    
    try:
        revenues = []
        for entry in historical_data[:5]:  # Use last 5 entries
            revenue = entry["monetization"]["insights"]["total_revenue"]
            revenues.append(revenue)
        
        # Simple trend calculation
        if len(revenues) >= 2:
            recent_avg = sum(revenues[:2]) / 2
            older_avg = sum(revenues[2:]) / len(revenues[2:]) if len(revenues) > 2 else revenues[0]
            
            trend = "growing" if recent_avg > older_avg else "declining" if recent_avg < older_avg else "stable"
            
            # Simple linear projection
            if len(revenues) >= 3:
                growth_rate = (revenues[0] - revenues[2]) / 2
                forecast = []
                last_revenue = revenues[0]
                
                for i in range(periods):
                    projected = last_revenue + (growth_rate * (i + 1))
                    forecast.append(max(0, round(projected, 2)))
                
                return {"forecast": forecast, "trend": trend}
        
        return {"forecast": [], "trend": "stable"}
        
    except Exception as e:
        logger.error(f"Error generating revenue forecast: {e}")
        return {"forecast": [], "trend": "error"}

if __name__ == "__main__":
    # Test the Dawn Monetization Scroll
    print("🔥 Testing Dawn Monetization Scroll...")
    
    result = dawn_monetization_scroll()
    
    if result["success"]:
        print("✅ Dawn Monetization Scroll generated successfully!")
        summary = result["summary"]
        print(f"💰 Total Revenue: ${summary['total_revenue']:.2f}")
        print(f"🚀 Active Platforms: {summary['active_platforms']}/5")
        print(f"👑 Top Platform: {summary['top_platform'] or 'None'}")
        print(f"⭐ Performance Tier: {summary['performance_tier'].title()}")
        print(f"📈 Growth Potential: {summary['growth_potential'].title()}")
        print(f"🎯 Diversification Score: {summary['diversification_score']:.1f}%")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Test history retrieval
    print("\n📚 Testing monetization history...")
    history = get_monetization_history(3)
    print(f"📈 Found {len(history)} historical reports")