"""
🔥 CODEX WHATSAPP BUSINESS SYSTEM 👑
Advanced WhatsApp Business API Integration and Message Management

The Merritt Method™ - Business Communication Sovereignty
"""

import os
import datetime
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging
import requests
from urllib.parse import urlencode

class CodexWhatsAppBusiness:
    """
    🔥 Sacred WhatsApp Business Management System 👑
    
    Comprehensive WhatsApp Business API integration for the Codex Dominion:
    - Message analytics and conversation tracking
    - Broadcast campaign management
    - Lead generation and conversion tracking
    - Cost analysis and budget monitoring
    - Template message management
    - Contact list organization
    - Archive and reporting system
    """
    
    def __init__(self, config_file: str = "whatsapp_config.json"):
        """Initialize the WhatsApp Business System"""
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.whatsapp_token = self.config.get("whatsapp", {}).get("token") or os.getenv("WHATSAPP_TOKEN")
        self.phone_id = self.config.get("whatsapp", {}).get("phone_id") or os.getenv("WHATSAPP_PHONE_ID")
        self.business_id = self.config.get("whatsapp", {}).get("business_id") or os.getenv("WHATSAPP_BUSINESS_ID")
        self.archive_file = Path("ledger_whatsapp.jsonl")
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # WhatsApp Business API endpoints
        self.graph_base = "https://graph.facebook.com/v19.0"
        self.whatsapp_api_version = "v19.0"
    
    def _load_config(self) -> Dict[str, Any]:
        """Load WhatsApp Business configuration from JSON file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Create default config
                default_config = {
                    "whatsapp": {
                        "token": "YOUR_WHATSAPP_TOKEN_HERE",
                        "phone_id": "YOUR_WHATSAPP_PHONE_ID_HERE",
                        "business_id": "YOUR_WHATSAPP_BUSINESS_ID_HERE",
                        "app_id": "YOUR_META_APP_ID",
                        "app_secret": "YOUR_META_APP_SECRET"
                    },
                    "messaging_settings": {
                        "track_conversations": True,
                        "track_leads": True,
                        "track_costs": True,
                        "track_templates": True,
                        "auto_archive": True,
                        "enable_broadcasts": True,
                        "rate_limiting": True
                    },
                    "analytics_settings": {
                        "track_delivery_rates": True,
                        "track_read_rates": True,
                        "track_conversion_rates": True,
                        "cost_monitoring": True,
                        "export_format": "json",
                        "alert_thresholds": {
                            "high_cost_alert": 100.0,
                            "low_delivery_rate": 0.8,
                            "conversation_spike": 1000,
                            "daily_budget_limit": 500.0
                        }
                    },
                    "broadcast_settings": {
                        "max_recipients_per_batch": 100,
                        "batch_delay_seconds": 1,
                        "template_categories": ["marketing", "utility", "authentication"],
                        "default_language": "en",
                        "track_campaign_performance": True
                    },
                    "business_settings": {
                        "business_name": "Your Business Name",
                        "industry": "Technology",
                        "timezone": "UTC",
                        "currency": "USD",
                        "contact_list_management": True
                    }
                }
                
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2)
                
                return default_config
                
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            return {}
    
    def whatsapp_metrics(self, phone_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Enhanced WhatsApp Business metrics collection
        
        Args:
            phone_id: Optional phone ID, uses configured default if not provided
            
        Returns:
            Dictionary with comprehensive WhatsApp Business metrics
        """
        target_phone = phone_id or self.phone_id
        
        if not target_phone or target_phone == "YOUR_WHATSAPP_PHONE_ID_HERE":
            return self._generate_demo_metrics()
        
        try:
            # Get WhatsApp Business analytics
            metrics = self._fetch_whatsapp_analytics(target_phone)
            
            # Enhance with calculated metrics
            enhanced_metrics = self._enhance_metrics(metrics)
            
            self.logger.info(f"Retrieved WhatsApp metrics for phone: {target_phone}")
            return enhanced_metrics
            
        except Exception as e:
            self.logger.error(f"Error retrieving WhatsApp metrics: {str(e)}")
            return {"error": str(e), "conversations": 0, "leads": 0, "messaging_cost_usd": 0}
    
    def _fetch_whatsapp_analytics(self, phone_id: str) -> Dict[str, Any]:
        """Fetch analytics from WhatsApp Business API"""
        try:
            if not self.whatsapp_token or self.whatsapp_token == "YOUR_WHATSAPP_TOKEN_HERE":
                return self._generate_demo_metrics()
            
            headers = {
                "Authorization": f"Bearer {self.whatsapp_token}",
                "Content-Type": "application/json"
            }
            
            # Fetch phone number analytics
            analytics_url = f"{self.graph_base}/{phone_id}/analytics"
            params = {
                "fields": "conversations,messages,delivery_rate,read_rate,cost_breakdown",
                "granularity": "daily",
                "start": (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
                "end": datetime.datetime.now().strftime("%Y-%m-%d")
            }
            
            response = requests.get(analytics_url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract metrics from WhatsApp Business API response
                return {
                    "conversations": self._extract_metric_value(data, "conversations"),
                    "leads": self._extract_leads_count(data),
                    "messaging_cost_usd": self._extract_cost_value(data),
                    "messages_sent": self._extract_metric_value(data, "messages_sent"),
                    "messages_delivered": self._extract_metric_value(data, "messages_delivered"),
                    "messages_read": self._extract_metric_value(data, "messages_read"),
                    "delivery_rate": self._extract_metric_value(data, "delivery_rate"),
                    "read_rate": self._extract_metric_value(data, "read_rate"),
                    "phone_id": phone_id,
                    "source": "whatsapp_business_api"
                }
            else:
                # Handle API errors gracefully
                self.logger.warning(f"WhatsApp Business API returned status {response.status_code}")
                return self._generate_demo_metrics()
                
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            return self._generate_demo_metrics()
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return self._generate_demo_metrics()
    
    def _extract_metric_value(self, data: Dict[str, Any], metric_name: str) -> float:
        """Extract metric value from WhatsApp Business API response"""
        try:
            # WhatsApp Business API returns analytics in a specific format
            analytics = data.get("analytics", [])
            for item in analytics:
                if item.get("name") == metric_name:
                    values = item.get("values", [])
                    if values:
                        return sum(v.get("value", 0) for v in values)
            return 0.0
        except Exception:
            return 0.0
    
    def _extract_leads_count(self, data: Dict[str, Any]) -> int:
        """Extract leads count from conversation data"""
        try:
            # Calculate leads based on conversation patterns and user interactions
            conversations = self._extract_metric_value(data, "conversations")
            # Estimate leads as a percentage of conversations (typical conversion rate)
            estimated_leads = int(conversations * 0.15)  # 15% conversion rate estimate
            return estimated_leads
        except Exception:
            return 0
    
    def _extract_cost_value(self, data: Dict[str, Any]) -> float:
        """Extract cost value from WhatsApp Business API response"""
        try:
            cost_breakdown = data.get("cost_breakdown", {})
            total_cost = 0.0
            
            # Sum up different cost components
            for cost_type, cost_data in cost_breakdown.items():
                if isinstance(cost_data, dict) and "amount" in cost_data:
                    total_cost += float(cost_data["amount"])
                elif isinstance(cost_data, (int, float)):
                    total_cost += float(cost_data)
            
            return total_cost
        except Exception:
            return 0.0
    
    def _generate_demo_metrics(self) -> Dict[str, Any]:
        """Generate demo metrics when API is not available"""
        import random
        
        # Generate realistic demo data for WhatsApp Business
        base_conversations = 450
        base_messages = 1200
        base_cost = 45.50
        
        # Add some realistic variation
        conversations = base_conversations + random.randint(-50, 150)
        messages_sent = base_messages + random.randint(-100, 300)
        messages_delivered = int(messages_sent * (0.85 + random.random() * 0.1))  # 85-95% delivery rate
        messages_read = int(messages_delivered * (0.65 + random.random() * 0.2))  # 65-85% read rate
        cost = base_cost + random.uniform(-15.0, 25.0)
        leads = int(conversations * (0.10 + random.random() * 0.10))  # 10-20% lead conversion
        
        delivery_rate = messages_delivered / messages_sent if messages_sent > 0 else 0
        read_rate = messages_read / messages_delivered if messages_delivered > 0 else 0
        
        return {
            "conversations": conversations,
            "leads": leads,
            "messaging_cost_usd": round(cost, 2),
            "messages_sent": messages_sent,
            "messages_delivered": messages_delivered,
            "messages_read": messages_read,
            "delivery_rate": round(delivery_rate, 3),
            "read_rate": round(read_rate, 3),
            "templates_used": random.randint(5, 15),
            "broadcast_campaigns": random.randint(2, 8),
            "contact_list_size": random.randint(500, 2000),
            "source": "demo_data",
            "demo": True
        }
    
    def _enhance_metrics(self, base_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance base metrics with calculated values"""
        try:
            conversations = base_metrics.get("conversations", 0)
            leads = base_metrics.get("leads", 0)
            cost = base_metrics.get("messaging_cost_usd", 0)
            messages_sent = base_metrics.get("messages_sent", 0)
            messages_delivered = base_metrics.get("messages_delivered", 0)
            messages_read = base_metrics.get("messages_read", 0)
            
            # Calculate business metrics
            lead_conversion_rate = (leads / conversations * 100) if conversations > 0 else 0
            cost_per_conversation = (cost / conversations) if conversations > 0 else 0
            cost_per_lead = (cost / leads) if leads > 0 else 0
            messages_per_conversation = (messages_sent / conversations) if conversations > 0 else 0
            
            # Calculate engagement metrics
            delivery_rate = base_metrics.get("delivery_rate", 0)
            read_rate = base_metrics.get("read_rate", 0)
            engagement_score = (delivery_rate * 0.4 + read_rate * 0.6) * 100  # Weighted engagement
            
            # Calculate ROI estimates (assuming average lead value)
            estimated_lead_value = 50.0  # Configurable estimate
            estimated_revenue = leads * estimated_lead_value
            roi_percentage = ((estimated_revenue - cost) / cost * 100) if cost > 0 else 0
            
            # Get growth metrics
            growth_metrics = self._calculate_growth_metrics()
            
            enhanced = {
                **base_metrics,
                "lead_conversion_rate": round(lead_conversion_rate, 2),
                "cost_per_conversation": round(cost_per_conversation, 3),
                "cost_per_lead": round(cost_per_lead, 2),
                "messages_per_conversation": round(messages_per_conversation, 1),
                "engagement_score": round(engagement_score, 1),
                "estimated_revenue": round(estimated_revenue, 2),
                "roi_percentage": round(roi_percentage, 1),
                "last_updated": datetime.datetime.utcnow().isoformat(),
                **growth_metrics
            }
            
            return enhanced
            
        except Exception as e:
            self.logger.error(f"Error enhancing metrics: {str(e)}")
            return base_metrics
    
    def _calculate_growth_metrics(self) -> Dict[str, Any]:
        """Calculate growth trends from historical data"""
        try:
            history = self.get_archive_history(30)  # Last 30 entries
            
            if len(history) < 2:
                return {
                    "conversation_growth": 0,
                    "lead_growth": 0,
                    "cost_growth": 0,
                    "trend_direction": "stable"
                }
            
            # Get recent vs previous metrics
            recent = history[-1] if history else {}
            previous = history[-7] if len(history) >= 7 else history[0]
            
            current_conversations = recent.get("conversations", 0)
            previous_conversations = previous.get("conversations", 0)
            
            current_leads = recent.get("leads", 0)
            previous_leads = previous.get("leads", 0)
            
            current_cost = recent.get("messaging_cost_usd", 0)
            previous_cost = previous.get("messaging_cost_usd", 0)
            
            conversation_growth = current_conversations - previous_conversations
            lead_growth = current_leads - previous_leads
            cost_growth = current_cost - previous_cost
            
            # Determine trend direction
            if conversation_growth > 0 and lead_growth > 0:
                trend_direction = "growing"
            elif conversation_growth < 0 or lead_growth < 0:
                trend_direction = "declining"
            else:
                trend_direction = "stable"
            
            return {
                "conversation_growth": conversation_growth,
                "lead_growth": lead_growth,
                "cost_growth": round(cost_growth, 2),
                "trend_direction": trend_direction,
                "growth_rate": round((conversation_growth / previous_conversations * 100), 2) if previous_conversations > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating growth metrics: {str(e)}")
            return {
                "conversation_growth": 0,
                "lead_growth": 0,
                "cost_growth": 0,
                "trend_direction": "unknown"
            }
    
    def whatsapp_broadcast(self, message: str, recipients: List[str], template_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Enhanced WhatsApp broadcast system with batch processing and tracking
        
        Args:
            message: Message content (for text messages)
            recipients: List of phone numbers to send to
            template_name: Optional template name for template messages
            
        Returns:
            Dictionary with broadcast results and tracking info
        """
        try:
            if not self.whatsapp_token or self.whatsapp_token == "YOUR_WHATSAPP_TOKEN_HERE":
                return self._simulate_broadcast(message, recipients)
            
            headers = {
                "Authorization": f"Bearer {self.whatsapp_token}",
                "Content-Type": "application/json"
            }
            
            broadcast_results = {
                "campaign_id": f"broadcast_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "total_recipients": len(recipients),
                "successful_sends": 0,
                "failed_sends": 0,
                "errors": [],
                "message_ids": [],
                "estimated_cost": 0.0
            }
            
            # Process recipients in batches to respect rate limits
            batch_size = self.config.get("broadcast_settings", {}).get("max_recipients_per_batch", 100)
            batch_delay = self.config.get("broadcast_settings", {}).get("batch_delay_seconds", 1)
            
            for i in range(0, len(recipients), batch_size):
                batch = recipients[i:i + batch_size]
                batch_results = self._send_batch(batch, message, template_name, headers)
                
                broadcast_results["successful_sends"] += batch_results["successful"]
                broadcast_results["failed_sends"] += batch_results["failed"]
                broadcast_results["errors"].extend(batch_results["errors"])
                broadcast_results["message_ids"].extend(batch_results["message_ids"])
                
                # Rate limiting delay between batches
                if i + batch_size < len(recipients):
                    import time
                    time.sleep(batch_delay)
            
            # Calculate estimated costs
            broadcast_results["estimated_cost"] = self._calculate_broadcast_cost(broadcast_results["successful_sends"])
            broadcast_results["success_rate"] = (broadcast_results["successful_sends"] / len(recipients)) * 100
            
            # Archive broadcast campaign
            if self.config.get("messaging_settings", {}).get("auto_archive", True):
                self.archive_whatsapp({
                    "type": "broadcast_campaign",
                    "message": message[:100] + "..." if len(message) > 100 else message,
                    **broadcast_results
                })
            
            return broadcast_results
            
        except Exception as e:
            self.logger.error(f"Error in WhatsApp broadcast: {str(e)}")
            return {"error": str(e), "successful_sends": 0, "failed_sends": len(recipients)}
    
    def _send_batch(self, recipients: List[str], message: str, template_name: Optional[str], headers: Dict[str, str]) -> Dict[str, Any]:
        """Send messages to a batch of recipients"""
        results = {
            "successful": 0,
            "failed": 0,
            "errors": [],
            "message_ids": []
        }
        
        for recipient in recipients:
            try:
                if template_name:
                    # Send template message
                    payload = {
                        "messaging_product": "whatsapp",
                        "to": recipient,
                        "type": "template",
                        "template": {
                            "name": template_name,
                            "language": {"code": "en"}
                        }
                    }
                else:
                    # Send text message
                    payload = {
                        "messaging_product": "whatsapp",
                        "to": recipient,
                        "type": "text",
                        "text": {"body": message}
                    }
                
                response = requests.post(
                    f"{self.graph_base}/{self.phone_id}/messages",
                    headers=headers,
                    json=payload,
                    timeout=10
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    message_id = response_data.get("messages", [{}])[0].get("id")
                    if message_id:
                        results["message_ids"].append(message_id)
                    results["successful"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append(f"Failed to send to {recipient}: {response.text}")
                
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Error sending to {recipient}: {str(e)}")
        
        return results
    
    def _simulate_broadcast(self, message: str, recipients: List[str]) -> Dict[str, Any]:
        """Simulate broadcast for demo purposes"""
        import random
        
        success_rate = 0.85 + random.random() * 0.1  # 85-95% success rate
        successful_sends = int(len(recipients) * success_rate)
        failed_sends = len(recipients) - successful_sends
        
        return {
            "campaign_id": f"demo_broadcast_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "total_recipients": len(recipients),
            "successful_sends": successful_sends,
            "failed_sends": failed_sends,
            "success_rate": round(success_rate * 100, 1),
            "estimated_cost": round(successful_sends * 0.025, 2),  # Estimated $0.025 per message
            "message_ids": [f"demo_msg_{i}" for i in range(successful_sends)],
            "errors": [f"Demo error {i}" for i in range(failed_sends)] if failed_sends > 0 else [],
            "demo": True
        }
    
    def _calculate_broadcast_cost(self, successful_sends: int) -> float:
        """Calculate estimated broadcast cost"""
        # WhatsApp Business pricing varies by country and message type
        # This is a simplified calculation
        cost_per_message = 0.025  # Average cost estimate
        return round(successful_sends * cost_per_message, 2)
    
    def archive_whatsapp(self, report: Dict[str, Any]) -> bool:
        """
        Enhanced WhatsApp archive system
        
        Args:
            report: WhatsApp metrics or campaign report to archive
            
        Returns:
            bool: True if archived successfully
        """
        try:
            # Prepare archive entry
            archive_entry = {
                "ts": datetime.datetime.utcnow().isoformat(),
                "type": "whatsapp_business",
                **report
            }
            
            # Append to JSONL file
            with open(self.archive_file, "a", encoding='utf-8') as f:
                f.write(json.dumps(archive_entry, ensure_ascii=False) + "\n")
            
            self.logger.info("WhatsApp Business data archived successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error archiving WhatsApp report: {str(e)}")
            return False
    
    def get_archive_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get WhatsApp Business archive history"""
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
    
    def get_business_summary(self) -> Dict[str, Any]:
        """Get comprehensive WhatsApp Business summary"""
        try:
            # Get current metrics
            current_metrics = self.whatsapp_metrics()
            
            if current_metrics.get("error"):
                return current_metrics
            
            # Get historical data for analysis
            history = self.get_archive_history(90)  # Last 90 entries
            
            # Calculate business insights
            business_insights = self._analyze_business_performance(current_metrics, history)
            
            # Cost analysis
            cost_analysis = self._analyze_cost_efficiency(current_metrics, history)
            
            # Campaign performance
            campaign_performance = self._analyze_campaign_performance(history)
            
            # Combine all data
            summary = {
                **current_metrics,
                **business_insights,
                **cost_analysis,
                **campaign_performance,
                "summary_generated": datetime.datetime.utcnow().isoformat(),
                "data_points": len(history)
            }
            
            # Archive current summary if auto-archive is enabled
            if self.config.get("messaging_settings", {}).get("auto_archive", True):
                self.archive_whatsapp(summary)
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generating business summary: {str(e)}")
            return {"error": str(e)}
    
    def _analyze_business_performance(self, current: Dict[str, Any], history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze overall business performance"""
        try:
            # Performance scoring
            delivery_rate = current.get("delivery_rate", 0)
            read_rate = current.get("read_rate", 0)
            conversion_rate = current.get("lead_conversion_rate", 0)
            
            # Calculate performance score (0-100)
            performance_score = (
                (delivery_rate * 30) +      # 30% weight on delivery
                (read_rate * 30) +          # 30% weight on read rate
                (conversion_rate * 40)      # 40% weight on conversions
            )
            
            # Trend analysis
            recent_conversations = [entry.get("conversations", 0) for entry in history[-14:]]
            if len(recent_conversations) > 7:
                recent_avg = sum(recent_conversations[-7:]) / 7
                previous_avg = sum(recent_conversations[-14:-7]) / 7
                
                if recent_avg > previous_avg * 1.1:
                    trend = "accelerating"
                elif recent_avg < previous_avg * 0.9:
                    trend = "declining"
                else:
                    trend = "stable"
            else:
                trend = "insufficient_data"
            
            return {
                "business_performance_score": round(performance_score, 1),
                "performance_trend": trend,
                "delivery_quality": "excellent" if delivery_rate > 0.9 else "good" if delivery_rate > 0.8 else "needs_improvement",
                "engagement_quality": "high" if read_rate > 0.7 else "medium" if read_rate > 0.5 else "low"
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing business performance: {str(e)}")
            return {"business_performance_score": 0, "performance_trend": "unknown"}
    
    def _analyze_cost_efficiency(self, current: Dict[str, Any], history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze cost efficiency and budget performance"""
        try:
            cost_per_conversation = current.get("cost_per_conversation", 0)
            cost_per_lead = current.get("cost_per_lead", 0)
            roi_percentage = current.get("roi_percentage", 0)
            
            # Cost efficiency rating
            if cost_per_conversation < 0.20:
                cost_efficiency = "excellent"
            elif cost_per_conversation < 0.50:
                cost_efficiency = "good"
            else:
                cost_efficiency = "high"
            
            # Budget analysis from history
            daily_costs = [entry.get("messaging_cost_usd", 0) for entry in history[-30:]]
            if daily_costs:
                avg_daily_cost = sum(daily_costs) / len(daily_costs)
                monthly_projection = avg_daily_cost * 30
            else:
                avg_daily_cost = current.get("messaging_cost_usd", 0)
                monthly_projection = avg_daily_cost * 30
            
            return {
                "cost_efficiency_rating": cost_efficiency,
                "avg_daily_cost": round(avg_daily_cost, 2),
                "monthly_cost_projection": round(monthly_projection, 2),
                "roi_status": "profitable" if roi_percentage > 0 else "breaking_even" if roi_percentage == 0 else "loss"
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing cost efficiency: {str(e)}")
            return {"cost_efficiency_rating": "unknown"}
    
    def _analyze_campaign_performance(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze broadcast campaign performance"""
        try:
            # Filter broadcast campaigns from history
            campaigns = [entry for entry in history if entry.get("type") == "broadcast_campaign"]
            
            if not campaigns:
                return {
                    "total_campaigns": 0,
                    "avg_success_rate": 0,
                    "total_messages_sent": 0,
                    "campaign_performance": "no_data"
                }
            
            total_campaigns = len(campaigns)
            total_sent = sum(c.get("successful_sends", 0) for c in campaigns)
            success_rates = [c.get("success_rate", 0) for c in campaigns if c.get("success_rate")]
            avg_success_rate = sum(success_rates) / len(success_rates) if success_rates else 0
            
            # Performance rating
            if avg_success_rate > 90:
                campaign_performance = "excellent"
            elif avg_success_rate > 80:
                campaign_performance = "good"
            elif avg_success_rate > 70:
                campaign_performance = "fair"
            else:
                campaign_performance = "needs_improvement"
            
            return {
                "total_campaigns": total_campaigns,
                "avg_success_rate": round(avg_success_rate, 1),
                "total_messages_sent": total_sent,
                "campaign_performance": campaign_performance,
                "last_campaign_date": campaigns[-1].get("ts", "")[:10] if campaigns else ""
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing campaign performance: {str(e)}")
            return {"total_campaigns": 0, "campaign_performance": "unknown"}
    
    def test_connection(self) -> bool:
        """Test WhatsApp Business API connection"""
        try:
            if not self.whatsapp_token or self.whatsapp_token == "YOUR_WHATSAPP_TOKEN_HERE":
                return False
            
            # Simple API test
            headers = {"Authorization": f"Bearer {self.whatsapp_token}"}
            response = requests.get(f"{self.graph_base}/{self.phone_id}", headers=headers, timeout=5)
            
            return response.status_code == 200
            
        except Exception as e:
            self.logger.error(f"WhatsApp connection test failed: {str(e)}")
            return False

# Enhanced backward compatibility functions
def whatsapp_metrics(phone_id: Optional[str] = None) -> Dict[str, Any]:
    """
    🔥 Enhanced WhatsApp Metrics Function 👑
    Your original function enhanced with comprehensive business analytics
    """
    try:
        whatsapp_system = CodexWhatsAppBusiness()
        return whatsapp_system.whatsapp_metrics(phone_id)
    except Exception as e:
        return {"error": str(e), "conversations": 0, "leads": 0, "messaging_cost_usd": 0}

def whatsapp_broadcast(message: str, recipients: List[str], template_name: Optional[str] = None) -> Dict[str, Any]:
    """
    🔥 Enhanced WhatsApp Broadcast Function 👑
    Your original function enhanced with batch processing and tracking
    """
    try:
        whatsapp_system = CodexWhatsAppBusiness()
        return whatsapp_system.whatsapp_broadcast(message, recipients, template_name)
    except Exception as e:
        return {"error": str(e), "successful_sends": 0, "failed_sends": len(recipients)}

def archive_whatsapp(report: Dict[str, Any]) -> bool:
    """
    🔥 Enhanced WhatsApp Archive Function 👑
    Your original function enhanced with structured business archiving
    """
    try:
        whatsapp_system = CodexWhatsAppBusiness()
        return whatsapp_system.archive_whatsapp(report)
    except Exception as e:
        return False

# Quick business analytics function
def get_whatsapp_business_summary(phone_id: Optional[str] = None) -> Dict[str, Any]:
    """Get comprehensive WhatsApp Business analytics"""
    try:
        whatsapp_system = CodexWhatsAppBusiness()
        if phone_id:
            whatsapp_system.phone_id = phone_id
        
        return whatsapp_system.get_business_summary()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Test the system
    whatsapp_system = CodexWhatsAppBusiness()
    
    print("🔥 WhatsApp Business System Test 👑")
    
    # Test metrics
    metrics = whatsapp_system.get_business_summary()
    print(f"Business summary: {metrics}")
    
    # Test broadcast (demo)
    demo_recipients = ["+1234567890", "+0987654321"]
    broadcast_result = whatsapp_system.whatsapp_broadcast("Test message", demo_recipients)
    print(f"Broadcast result: {broadcast_result}")
    
    if whatsapp_system.test_connection():
        print("✅ WhatsApp Business API connection successful!")
    else:
        print("⚠️ WhatsApp Business API connection failed - using demo data")