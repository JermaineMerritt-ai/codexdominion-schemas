"""
🔥 CODEX YOUTUBE CHARTS SYSTEM 👑
Advanced YouTube Analytics and Content Management Integration

The Merritt Method™ - Digital Video Sovereignty
"""

import os
import datetime
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

# Safe imports for YouTube API
try:
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import google.auth.exceptions
    YOUTUBE_API_AVAILABLE = True
except ImportError:
    YOUTUBE_API_AVAILABLE = False

class CodexYouTubeCharts:
    """
    🔥 Sacred YouTube Charts Management System 👑
    
    Comprehensive YouTube integration for the Codex Dominion:
    - Channel analytics and metrics
    - Video upload and management
    - Subscriber and engagement tracking
    - Archive management system
    - Performance analytics
    """
    
    def __init__(self, config_file: str = "youtube_config.json"):
        """Initialize the YouTube Charts System"""
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.api_key = self.config.get("youtube", {}).get("api_key") or os.getenv("YOUTUBE_API_KEY")
        self.channel_id = self.config.get("youtube", {}).get("channel_id", "")
        self.archive_file = Path("ledger_youtube.jsonl")
        self.youtube_service = None
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize YouTube service
        self._initialize_youtube_service()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load YouTube configuration from JSON file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Create default config
                default_config = {
                    "youtube": {
                        "api_key": "YOUR_YOUTUBE_API_KEY_HERE",
                        "channel_id": "YOUR_CHANNEL_ID_HERE",
                        "oauth_credentials": "client_secrets.json"
                    },
                    "chart_settings": {
                        "auto_archive": True,
                        "metrics_interval": "daily",
                        "track_competitors": False,
                        "export_format": "json"
                    },
                    "upload_settings": {
                        "default_privacy": "unlisted",
                        "auto_tags": ["#CodexDominion", "#DigitalSovereignty", "#MerrittMethod"],
                        "default_category": "22",
                        "auto_thumbnail": True
                    },
                    "analytics_settings": {
                        "track_engagement": True,
                        "track_revenue": False,
                        "competitor_channels": [],
                        "alert_thresholds": {
                            "subscriber_milestone": 1000,
                            "view_spike": 10000,
                            "engagement_drop": 0.02
                        }
                    }
                }
                
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2)
                
                return default_config
                
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            return {}
    
    def _initialize_youtube_service(self):
        """Initialize YouTube API service"""
        try:
            if not YOUTUBE_API_AVAILABLE:
                self.logger.warning("YouTube API libraries not available")
                return
            
            if not self.api_key or self.api_key == "YOUR_YOUTUBE_API_KEY_HERE":
                self.logger.warning("YouTube API key not configured")
                return
            
            self.youtube_service = build("youtube", "v3", developerKey=self.api_key)
            self.logger.info("YouTube API service initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize YouTube service: {str(e)}")
            self.youtube_service = None
    
    def youtube_metrics(self, channel_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Enhanced YouTube metrics collection
        
        Args:
            channel_id: Optional channel ID, uses configured default if not provided
            
        Returns:
            Dictionary with comprehensive channel metrics
        """
        if not self.youtube_service:
            return {"error": "YouTube service not available", "subscribers": 0, "views": 0, "videos": 0}
        
        try:
            target_channel = channel_id or self.channel_id
            
            if not target_channel or target_channel == "YOUR_CHANNEL_ID_HERE":
                return {"error": "Channel ID not configured", "subscribers": 0, "views": 0, "videos": 0}
            
            # Get channel statistics
            stats_response = self.youtube_service.channels().list(
                part="statistics,snippet,brandingSettings",
                id=target_channel
            ).execute()
            
            if not stats_response.get("items"):
                return {"error": "Channel not found", "subscribers": 0, "views": 0, "videos": 0}
            
            channel_data = stats_response["items"][0]
            stats = channel_data.get("statistics", {})
            snippet = channel_data.get("snippet", {})
            
            # Enhanced metrics
            metrics = {
                "subscribers": int(stats.get("subscriberCount", 0)),
                "views": int(stats.get("viewCount", 0)),
                "videos": int(stats.get("videoCount", 0)),
                "channel_title": snippet.get("title", "Unknown"),
                "created_date": snippet.get("publishedAt", ""),
                "description": snippet.get("description", "")[:200] + "..." if len(snippet.get("description", "")) > 200 else snippet.get("description", ""),
                "country": snippet.get("country", ""),
                "custom_url": snippet.get("customUrl", ""),
                "thumbnail": snippet.get("thumbnails", {}).get("default", {}).get("url", "")
            }
            
            # Get recent videos performance
            recent_videos = self._get_recent_video_metrics(target_channel)
            metrics.update(recent_videos)
            
            # Calculate engagement metrics
            engagement_metrics = self._calculate_engagement_metrics(metrics)
            metrics.update(engagement_metrics)
            
            self.logger.info(f"Retrieved metrics for channel: {metrics.get('channel_title')}")
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error retrieving YouTube metrics: {str(e)}")
            return {"error": str(e), "subscribers": 0, "views": 0, "videos": 0}
    
    def _get_recent_video_metrics(self, channel_id: str, max_results: int = 10) -> Dict[str, Any]:
        """Get metrics for recent videos"""
        try:
            # Get recent uploads
            channel_response = self.youtube_service.channels().list(
                part="contentDetails",
                id=channel_id
            ).execute()
            
            uploads_playlist = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            
            playlist_response = self.youtube_service.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist,
                maxResults=max_results
            ).execute()
            
            video_ids = [item["snippet"]["resourceId"]["videoId"] for item in playlist_response.get("items", [])]
            
            if not video_ids:
                return {"recent_videos": [], "avg_views_per_video": 0, "total_recent_views": 0}
            
            # Get video statistics
            videos_response = self.youtube_service.videos().list(
                part="statistics,snippet",
                id=",".join(video_ids)
            ).execute()
            
            recent_videos = []
            total_views = 0
            
            for video in videos_response.get("items", []):
                video_stats = video.get("statistics", {})
                video_snippet = video.get("snippet", {})
                
                video_data = {
                    "video_id": video["id"],
                    "title": video_snippet.get("title", ""),
                    "published_at": video_snippet.get("publishedAt", ""),
                    "views": int(video_stats.get("viewCount", 0)),
                    "likes": int(video_stats.get("likeCount", 0)),
                    "comments": int(video_stats.get("commentCount", 0))
                }
                
                recent_videos.append(video_data)
                total_views += video_data["views"]
            
            avg_views = total_views // len(recent_videos) if recent_videos else 0
            
            return {
                "recent_videos": recent_videos,
                "avg_views_per_video": avg_views,
                "total_recent_views": total_views,
                "recent_video_count": len(recent_videos)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting recent video metrics: {str(e)}")
            return {"recent_videos": [], "avg_views_per_video": 0, "total_recent_views": 0}
    
    def _calculate_engagement_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate engagement and performance metrics"""
        try:
            subscribers = metrics.get("subscribers", 0)
            total_views = metrics.get("views", 0)
            video_count = metrics.get("videos", 0)
            
            # Basic calculations
            avg_views_per_video = total_views // video_count if video_count > 0 else 0
            views_per_subscriber = total_views // subscribers if subscribers > 0 else 0
            
            # Recent performance
            recent_videos = metrics.get("recent_videos", [])
            recent_engagement = 0
            
            if recent_videos:
                total_recent_engagement = sum(
                    video.get("likes", 0) + video.get("comments", 0) 
                    for video in recent_videos
                )
                total_recent_views = sum(video.get("views", 0) for video in recent_videos)
                recent_engagement = (total_recent_engagement / total_recent_views * 100) if total_recent_views > 0 else 0
            
            return {
                "avg_views_per_video": avg_views_per_video,
                "views_per_subscriber": views_per_subscriber,
                "engagement_rate": round(recent_engagement, 2),
                "channel_score": self._calculate_channel_score(subscribers, avg_views_per_video, recent_engagement)
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating engagement metrics: {str(e)}")
            return {"avg_views_per_video": 0, "views_per_subscriber": 0, "engagement_rate": 0, "channel_score": 0}
    
    def _calculate_channel_score(self, subscribers: int, avg_views: int, engagement: float) -> int:
        """Calculate overall channel performance score (0-100)"""
        try:
            # Scoring algorithm
            subscriber_score = min(subscribers / 10000 * 30, 30)  # Max 30 points for subscribers
            view_score = min(avg_views / 5000 * 40, 40)          # Max 40 points for views
            engagement_score = min(engagement * 3, 30)           # Max 30 points for engagement
            
            total_score = subscriber_score + view_score + engagement_score
            return min(int(total_score), 100)
            
        except Exception:
            return 0
    
    def archive_youtube(self, report: Dict[str, Any]) -> bool:
        """
        Enhanced YouTube archive system
        
        Args:
            report: YouTube metrics report to archive
            
        Returns:
            bool: True if archived successfully
        """
        try:
            # Prepare archive entry
            archive_entry = {
                "ts": datetime.datetime.utcnow().isoformat(),
                "type": "youtube_metrics",
                **report
            }
            
            # Append to JSONL file
            with open(self.archive_file, "a", encoding='utf-8') as f:
                f.write(json.dumps(archive_entry, ensure_ascii=False) + "\n")
            
            self.logger.info("YouTube metrics archived successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error archiving YouTube report: {str(e)}")
            return False
    
    def get_archive_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get YouTube archive history"""
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
    
    def upload_video(self, video_file: str, title: str, description: str = "", tags: List[str] = None, privacy: str = "unlisted") -> Dict[str, Any]:
        """
        Upload video to YouTube
        
        Args:
            video_file: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
            privacy: Privacy setting (public, unlisted, private)
            
        Returns:
            Dict with upload result
        """
        try:
            if not self.youtube_service:
                return {"success": False, "error": "YouTube service not available"}
            
            if not Path(video_file).exists():
                return {"success": False, "error": "Video file not found"}
            
            # Prepare video metadata
            video_tags = tags or self.config.get("upload_settings", {}).get("auto_tags", [])
            
            body = {
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": video_tags,
                    "categoryId": self.config.get("upload_settings", {}).get("default_category", "22")
                },
                "status": {
                    "privacyStatus": privacy
                }
            }
            
            # Note: Actual upload would require OAuth authentication
            # This is a placeholder for the upload logic
            self.logger.info(f"Upload prepared for video: {title}")
            
            return {
                "success": True,
                "message": "Video upload prepared (OAuth authentication required for actual upload)",
                "video_id": "placeholder_id",
                "title": title
            }
            
        except Exception as e:
            self.logger.error(f"Error preparing video upload: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_channel_analytics_summary(self) -> Dict[str, Any]:
        """Get comprehensive channel analytics summary"""
        try:
            # Get current metrics
            current_metrics = self.youtube_metrics()
            
            if current_metrics.get("error"):
                return current_metrics
            
            # Get historical data for trends
            history = self.get_archive_history(30)  # Last 30 entries
            
            # Calculate trends
            trends = self._calculate_trends(history, current_metrics)
            
            # Combine current metrics with trends
            summary = {
                **current_metrics,
                **trends,
                "last_updated": datetime.datetime.utcnow().isoformat(),
                "data_points": len(history)
            }
            
            # Archive current summary if auto-archive is enabled
            if self.config.get("chart_settings", {}).get("auto_archive", True):
                self.archive_youtube(summary)
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generating analytics summary: {str(e)}")
            return {"error": str(e)}
    
    def _calculate_trends(self, history: List[Dict[str, Any]], current: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate growth trends from historical data"""
        try:
            if len(history) < 2:
                return {"subscriber_growth": 0, "view_growth": 0, "video_growth": 0, "trend_direction": "stable"}
            
            # Get previous metrics (7 days ago if available)
            previous = history[-7] if len(history) >= 7 else history[0]
            
            # Calculate growth
            current_subs = current.get("subscribers", 0)
            previous_subs = previous.get("subscribers", 0)
            
            current_views = current.get("views", 0)
            previous_views = previous.get("views", 0)
            
            current_videos = current.get("videos", 0)
            previous_videos = previous.get("videos", 0)
            
            subscriber_growth = current_subs - previous_subs
            view_growth = current_views - previous_views
            video_growth = current_videos - previous_videos
            
            # Determine trend direction
            if subscriber_growth > 0 and view_growth > 0:
                trend_direction = "growing"
            elif subscriber_growth < 0 or view_growth < 0:
                trend_direction = "declining"
            else:
                trend_direction = "stable"
            
            return {
                "subscriber_growth": subscriber_growth,
                "view_growth": view_growth,
                "video_growth": video_growth,
                "trend_direction": trend_direction,
                "growth_rate": round((subscriber_growth / previous_subs * 100), 2) if previous_subs > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating trends: {str(e)}")
            return {"subscriber_growth": 0, "view_growth": 0, "video_growth": 0, "trend_direction": "unknown"}
    
    def test_connection(self) -> bool:
        """Test YouTube API connection"""
        try:
            if not self.youtube_service:
                return False
            
            # Simple API test
            test_response = self.youtube_service.search().list(
                part="snippet",
                q="test",
                maxResults=1,
                type="video"
            ).execute()
            
            return bool(test_response.get("items"))
            
        except Exception as e:
            self.logger.error(f"YouTube connection test failed: {str(e)}")
            return False

# Enhanced backward compatibility functions
def youtube_metrics(channel_id: str) -> Dict[str, Any]:
    """
    🔥 Enhanced YouTube Metrics Function 👑
    Your original function enhanced with comprehensive analytics
    """
    try:
        youtube_system = CodexYouTubeCharts()
        return youtube_system.youtube_metrics(channel_id)
    except Exception as e:
        return {"error": str(e), "subscribers": 0, "views": 0, "videos": 0}

def archive_youtube(report: Dict[str, Any]) -> bool:
    """
    🔥 Enhanced YouTube Archive Function 👑
    Your original function enhanced with structured archiving
    """
    try:
        youtube_system = CodexYouTubeCharts()
        return youtube_system.archive_youtube(report)
    except Exception as e:
        return False

# Quick analytics function
def get_youtube_analytics(channel_id: Optional[str] = None) -> Dict[str, Any]:
    """Get comprehensive YouTube analytics"""
    try:
        youtube_system = CodexYouTubeCharts()
        if channel_id:
            youtube_system.channel_id = channel_id
        
        return youtube_system.get_channel_analytics_summary()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Test the system
    youtube_system = CodexYouTubeCharts()
    
    if youtube_system.test_connection():
        print("🔥 YouTube API connection successful! 👑")
        
        # Test metrics
        metrics = youtube_system.get_channel_analytics_summary()
        print(f"Analytics result: {metrics}")
    else:
        print("❌ YouTube API connection failed. Check your configuration.")