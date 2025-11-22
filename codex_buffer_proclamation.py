"""
🔥 CODEX BUFFER PROCLAMATION SYSTEM 👑
Advanced Buffer API Integration for Multi-Platform Social Media Dominion

The Merritt Method™ - Digital Sovereignty Through Strategic Social Presence
"""

import requests
import json
from datetime import datetime, timedelta
import time
from typing import List, Dict, Optional, Any
import logging
from pathlib import Path

class CodexBufferProclaimer:
    """
    🔥 Sacred Buffer API Integration System 👑
    
    Multi-platform social media proclamation system using Buffer's scheduling API.
    Enables simultaneous posting across Twitter, Facebook, LinkedIn, Instagram, and more.
    """
    
    def __init__(self, config_file: str = "buffer_config.json"):
        """Initialize the Buffer Proclamation System"""
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.base_url = "https://api.bufferapp.com/1"
        self.token = self.config.get("buffer", {}).get("access_token")
        self.profiles = self._load_profiles()
        self.proclamation_history = self._load_proclamation_history()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def _load_config(self) -> Dict[str, Any]:
        """Load Buffer configuration from JSON file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Create default config
                default_config = {
                    "buffer": {
                        "access_token": "YOUR_BUFFER_ACCESS_TOKEN",
                        "client_id": "YOUR_BUFFER_CLIENT_ID",
                        "client_secret": "YOUR_BUFFER_CLIENT_SECRET"
                    },
                    "proclamation_settings": {
                        "auto_schedule": False,
                        "default_delay_minutes": 15,
                        "max_history": 1000,
                        "rate_limit_delay": 2
                    },
                    "templates": {
                        "sovereignty": [
                            "🔥 Digital Sovereignty Proclamation: {text}",
                            "👑 Sacred Decree from the Codex: {text}",
                            "⚡ Dominion Alert: {text}"
                        ],
                        "wisdom": [
                            "💎 Wisdom from the Digital Throne: {text}",
                            "🧠 Sacred Knowledge: {text}",
                            "✨ Enlightenment Scroll: {text}"
                        ],
                        "celebration": [
                            "🎉 Victory Celebration: {text}",
                            "🏆 Sacred Triumph: {text}",
                            "✨ Dominion Achievement: {text}"
                        ],
                        "announcement": [
                            "📢 Official Proclamation: {text}",
                            "🔔 Codex Announcement: {text}",
                            "📯 Royal Decree: {text}"
                        ]
                    },
                    "hashtags": {
                        "default": ["#CodexDominion", "#DigitalSovereignty", "#MerrittMethod"],
                        "business": ["#Entrepreneurship", "#DigitalBusiness", "#Innovation"],
                        "tech": ["#Technology", "#AI", "#SoftwareDevelopment"],
                        "leadership": ["#Leadership", "#DigitalTransformation", "#Strategy"]
                    }
                }
                
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2)
                
                return default_config
                
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            return {}
    
    def _load_profiles(self) -> List[Dict[str, Any]]:
        """Load user's Buffer profiles"""
        try:
            if not self.token or self.token == "YOUR_BUFFER_ACCESS_TOKEN":
                return []
                
            response = requests.get(
                f"{self.base_url}/profiles.json",
                params={"access_token": self.token}
            )
            
            if response.status_code == 200:
                profiles = response.json()
                self.logger.info(f"Loaded {len(profiles)} Buffer profiles")
                return profiles
            else:
                self.logger.error(f"Failed to load profiles: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"Error loading profiles: {str(e)}")
            return []
    
    def _load_proclamation_history(self) -> List[Dict[str, Any]]:
        """Load proclamation history from file"""
        try:
            history_file = Path("buffer_proclamation_history.json")
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            self.logger.error(f"Error loading history: {str(e)}")
            return []
    
    def _save_proclamation_history(self):
        """Save proclamation history to file"""
        try:
            history_file = Path("buffer_proclamation_history.json")
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.proclamation_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving history: {str(e)}")
    
    def get_profiles(self) -> List[Dict[str, Any]]:
        """Get available Buffer profiles"""
        return self.profiles
    
    def get_profile_by_service(self, service: str) -> List[Dict[str, Any]]:
        """Get profiles for specific social media service"""
        return [p for p in self.profiles if p.get('service') == service]
    
    def format_proclamation(self, text: str, proclamation_type: str = "sovereignty") -> str:
        """Format proclamation text using templates"""
        templates = self.config.get("templates", {}).get(proclamation_type, ["{text}"])
        
        if templates:
            template = templates[0]  # Use first template
            return template.format(text=text)
        
        return text
    
    def add_hashtags(self, text: str, hashtag_set: str = "default") -> str:
        """Add hashtags to proclamation text"""
        hashtags = self.config.get("hashtags", {}).get(hashtag_set, [])
        
        if hashtags:
            # Add hashtags if not already present
            hashtag_text = " ".join(hashtags)
            if not any(tag in text for tag in hashtags):
                text += f"\n\n{hashtag_text}"
        
        return text
    
    def send_proclamation(
        self, 
        text: str, 
        profile_ids: List[str] = None,
        proclamation_type: str = "sovereignty",
        hashtag_set: str = "default",
        scheduled_at: Optional[datetime] = None,
        media_urls: List[str] = None
    ) -> Dict[str, Any]:
        """
        Send proclamation to Buffer profiles
        
        Args:
            text: The proclamation content
            profile_ids: List of Buffer profile IDs to post to
            proclamation_type: Type of proclamation for formatting
            hashtag_set: Set of hashtags to include
            scheduled_at: Optional datetime to schedule post
            media_urls: Optional list of media URLs to attach
            
        Returns:
            Dict with success status and details
        """
        try:
            if not self.token or self.token == "YOUR_BUFFER_ACCESS_TOKEN":
                return {
                    "success": False,
                    "error": "Buffer access token not configured"
                }
            
            # Format the proclamation
            formatted_text = self.format_proclamation(text, proclamation_type)
            formatted_text = self.add_hashtags(formatted_text, hashtag_set)
            
            # Use all profiles if none specified
            if not profile_ids:
                profile_ids = [p['id'] for p in self.profiles]
            
            if not profile_ids:
                return {
                    "success": False,
                    "error": "No Buffer profiles available"
                }
            
            # Prepare the update data
            update_data = {
                "text": formatted_text,
                "profile_ids": profile_ids,
                "access_token": self.token
            }
            
            # Add scheduled time if provided
            if scheduled_at:
                update_data["scheduled_at"] = int(scheduled_at.timestamp())
            
            # Add media if provided
            if media_urls:
                update_data["media"] = {"link": media_urls[0]}  # Buffer supports one media item
            
            # Send the update
            response = requests.post(
                f"{self.base_url}/updates/create.json",
                data=update_data
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Log to history
                history_entry = {
                    "id": result.get("id", "unknown"),
                    "text": formatted_text,
                    "type": proclamation_type,
                    "profile_ids": profile_ids,
                    "scheduled_at": scheduled_at.isoformat() if scheduled_at else None,
                    "timestamp": datetime.now().isoformat(),
                    "success": True
                }
                
                self.proclamation_history.append(history_entry)
                self._save_proclamation_history()
                
                self.logger.info(f"Proclamation sent successfully: {result.get('id')}")
                
                return {
                    "success": True,
                    "update_id": result.get("id"),
                    "message": "Scroll dispatched to social profiles",
                    "profiles_count": len(profile_ids),
                    "scheduled": scheduled_at is not None
                }
            else:
                error_msg = f"Buffer API error: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                return {
                    "success": False,
                    "error": error_msg
                }
                
        except Exception as e:
            error_msg = f"Error sending proclamation: {str(e)}"
            self.logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
    
    def schedule_proclamation(
        self,
        text: str,
        schedule_time: datetime,
        profile_ids: List[str] = None,
        proclamation_type: str = "sovereignty",
        hashtag_set: str = "default"
    ) -> Dict[str, Any]:
        """Schedule a proclamation for future posting"""
        return self.send_proclamation(
            text=text,
            profile_ids=profile_ids,
            proclamation_type=proclamation_type,
            hashtag_set=hashtag_set,
            scheduled_at=schedule_time
        )
    
    def send_to_specific_platforms(
        self,
        text: str,
        platforms: List[str],
        proclamation_type: str = "sovereignty",
        hashtag_set: str = "default"
    ) -> Dict[str, Any]:
        """Send proclamation to specific social media platforms"""
        
        # Get profile IDs for requested platforms
        target_profiles = []
        for platform in platforms:
            platform_profiles = self.get_profile_by_service(platform.lower())
            target_profiles.extend([p['id'] for p in platform_profiles])
        
        if not target_profiles:
            return {
                "success": False,
                "error": f"No profiles found for platforms: {platforms}"
            }
        
        return self.send_proclamation(
            text=text,
            profile_ids=target_profiles,
            proclamation_type=proclamation_type,
            hashtag_set=hashtag_set
        )
    
    def broadcast_sovereignty(
        self,
        text: str,
        exclude_platforms: List[str] = None
    ) -> Dict[str, Any]:
        """Broadcast to all platforms except excluded ones"""
        
        if exclude_platforms is None:
            exclude_platforms = []
        
        # Get all profiles except excluded platforms
        target_profiles = []
        for profile in self.profiles:
            if profile.get('service') not in exclude_platforms:
                target_profiles.append(profile['id'])
        
        return self.send_proclamation(
            text=text,
            profile_ids=target_profiles,
            proclamation_type="sovereignty",
            hashtag_set="default"
        )
    
    def get_pending_updates(self) -> List[Dict[str, Any]]:
        """Get pending scheduled updates from Buffer"""
        try:
            if not self.token or self.token == "YOUR_BUFFER_ACCESS_TOKEN":
                return []
            
            pending_updates = []
            
            for profile in self.profiles:
                response = requests.get(
                    f"{self.base_url}/profiles/{profile['id']}/updates/pending.json",
                    params={"access_token": self.token}
                )
                
                if response.status_code == 200:
                    updates = response.json().get('updates', [])
                    for update in updates:
                        update['profile_service'] = profile.get('service')
                        pending_updates.append(update)
                
                # Rate limiting
                time.sleep(0.5)
            
            return pending_updates
            
        except Exception as e:
            self.logger.error(f"Error getting pending updates: {str(e)}")
            return []
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get analytics summary from Buffer"""
        try:
            if not self.token or self.token == "YOUR_BUFFER_ACCESS_TOKEN":
                return {}
            
            analytics = {
                "total_profiles": len(self.profiles),
                "profiles_by_platform": {},
                "recent_posts": len([h for h in self.proclamation_history if h.get('success', False)]),
                "pending_posts": len(self.get_pending_updates())
            }
            
            # Count profiles by platform
            for profile in self.profiles:
                service = profile.get('service', 'unknown')
                analytics["profiles_by_platform"][service] = analytics["profiles_by_platform"].get(service, 0) + 1
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"Error getting analytics: {str(e)}")
            return {}
    
    def get_proclamation_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent proclamation history"""
        return self.proclamation_history[-limit:] if limit else self.proclamation_history
    
    def test_connection(self) -> bool:
        """Test Buffer API connection"""
        try:
            if not self.token or self.token == "YOUR_BUFFER_ACCESS_TOKEN":
                return False
            
            response = requests.get(
                f"{self.base_url}/user.json",
                params={"access_token": self.token}
            )
            
            return response.status_code == 200
            
        except Exception:
            return False

def proclaim_social(text: str, profile_ids: List[str] = None) -> Dict[str, Any]:
    """
    🔥 Quick Proclamation Function 👑
    Simplified function for immediate social media posting
    """
    try:
        buffer_client = CodexBufferProclaimer()
        
        result = buffer_client.send_proclamation(
            text=text,
            profile_ids=profile_ids,
            proclamation_type="sovereignty"
        )
        
        if result.get("success"):
            print("🔥 Scroll dispatched to social profiles! 👑")
            return result
        else:
            print(f"❌ Proclamation failed: {result.get('error')}")
            return result
            
    except Exception as e:
        error_msg = f"Error in proclamation: {str(e)}"
        print(f"❌ {error_msg}")
        return {"success": False, "error": error_msg}

# Backward compatibility function
def proclaim_social_legacy(text: str, profile_ids: List[str]):
    """Legacy function for backward compatibility"""
    result = proclaim_social(text, profile_ids)
    if result.get("success"):
        print("Scroll dispatched to social profiles.")
    else:
        print(f"Failed to dispatch scroll: {result.get('error')}")

if __name__ == "__main__":
    # Test the system
    buffer_client = CodexBufferProclaimer()
    
    if buffer_client.test_connection():
        print("🔥 Buffer connection successful! 👑")
        
        # Test proclamation
        result = buffer_client.send_proclamation(
            "Testing the Codex Dominion Buffer integration system! 🔥👑",
            proclamation_type="sovereignty"
        )
        
        print(f"Test result: {result}")
    else:
        print("❌ Buffer connection failed. Check your configuration.")