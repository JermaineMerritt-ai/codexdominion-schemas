"""
🔥 Codex Dominion - Twitter/X Proclamation Integration
Enhanced Twitter/X API integration for sacred scroll proclamations
"""

import json
import os
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import tweepy


class CodexTwitterProclaimer:
    """Enhanced Twitter/X proclamation system for Codex Dominion"""

    def __init__(
        self,
        bearer_token: str = None,
        api_key: str = None,
        api_secret: str = None,
        access_token: str = None,
        access_token_secret: str = None,
    ):

        # Load configuration
        config = self.load_config()

        # Twitter API credentials
        self.bearer_token = (
            bearer_token
            or config.get("bearer_token")
            or os.getenv("TWITTER_BEARER_TOKEN")
        )
        self.api_key = api_key or config.get("api_key") or os.getenv("TWITTER_API_KEY")
        self.api_secret = (
            api_secret or config.get("api_secret") or os.getenv("TWITTER_API_SECRET")
        )
        self.access_token = (
            access_token
            or config.get("access_token")
            or os.getenv("TWITTER_ACCESS_TOKEN")
        )
        self.access_token_secret = (
            access_token_secret
            or config.get("access_token_secret")
            or os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        )

        # Initialize Twitter clients
        self.client_v2 = None
        self.api_v1 = None

        self._initialize_clients()

        # Proclamation templates
        self.proclamation_templates = {
            "sovereignty": [
                "🔥 Digital Sovereignty Alert: {text}",
                "👑 Codex Proclamation: {text} #DigitalSovereignty",
                "⚡ Sacred Scroll: {text} #CodexDominion",
                "🛡️ Sovereign Declaration: {text}",
                "✨ By flame and code: {text}",
            ],
            "wisdom": [
                "💎 Wisdom from the Codex: {text}",
                "🧠 Digital Enlightenment: {text} #Wisdom",
                "📜 Ancient Code Wisdom: {text}",
                "🔮 Oracle Speaks: {text} #DigitalOracle",
            ],
            "celebration": [
                "🎉 Celebrating: {text} #Victory",
                "🏆 Achievement Unlocked: {text}",
                "✨ Sacred Milestone: {text} #Success",
                "🔥 Eternal Flame Burns Brighter: {text}",
            ],
            "announcement": [
                "📢 Codex Update: {text}",
                "🚀 New Horizons: {text} #Innovation",
                "⚡ Breaking: {text} #CodexNews",
                "🌟 Sovereign Alert: {text}",
            ],
        }

        # Hashtags for different content types
        self.hashtag_sets = {
            "default": ["#CodexDominion", "#DigitalSovereignty", "#TherrittMethod"],
            "ai": ["#AI", "#MachineLearning", "#FutureOfWork", "#CodexAI"],
            "business": ["#Entrepreneurship", "#DigitalBusiness", "#Innovation"],
            "tech": ["#Technology", "#SoftwareDevelopment", "#TechLeadership"],
            "personal": ["#PersonalDevelopment", "#Mindset", "#Success"],
        }

    def load_config(self) -> Dict:
        """Load Twitter configuration from file"""
        try:
            config_path = Path("twitter_config.json")
            if config_path.exists():
                with open(config_path, "r") as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Could not load Twitter config: {e}")
        return {}

    def save_config(self, config: Dict):
        """Save Twitter configuration to file"""
        try:
            with open("twitter_config.json", "w") as f:
                json.dump(config, f, indent=2)
            print("✅ Twitter configuration saved")
        except Exception as e:
            print(f"❌ Could not save config: {e}")

    def _initialize_clients(self):
        """Initialize Twitter API clients"""
        try:
            # Initialize v2 client (newer API)
            if self.bearer_token:
                self.client_v2 = tweepy.Client(
                    bearer_token=self.bearer_token,
                    consumer_key=self.api_key,
                    consumer_secret=self.api_secret,
                    access_token=self.access_token,
                    access_token_secret=self.access_token_secret,
                    wait_on_rate_limit=True,
                )
                print("✅ Twitter v2 client initialized")

            # Initialize v1 client (for media uploads and legacy features)
            if all(
                [
                    self.api_key,
                    self.api_secret,
                    self.access_token,
                    self.access_token_secret,
                ]
            ):
                auth = tweepy.OAuth1UserHandler(
                    self.api_key,
                    self.api_secret,
                    self.access_token,
                    self.access_token_secret,
                )
                self.api_v1 = tweepy.API(auth, wait_on_rate_limit=True)
                print("✅ Twitter v1 API initialized")

        except Exception as e:
            print(f"❌ Error initializing Twitter clients: {e}")

    def test_connection(self) -> bool:
        """Test Twitter API connection"""
        try:
            if self.client_v2:
                # Test with a simple user lookup
                user = self.client_v2.get_me()
                if user.data:
                    print(
                        f"✅ Twitter connection successful! Account: @{user.data.username}"
                    )
                    return True

            print("❌ No valid Twitter client available")
            return False

        except Exception as e:
            print(f"❌ Twitter connection failed: {e}")
            return False

    def proclaim_scroll(
        self,
        text: str,
        scroll_type: str = "sovereignty",
        hashtags: List[str] = None,
        auto_hashtag: bool = True,
    ) -> Optional[Dict]:
        """Enhanced scroll proclamation with templates and hashtags"""

        if not self.client_v2:
            print("❌ Cannot proclaim: Twitter client not initialized")
            return None

        try:
            # Apply proclamation template
            template = random.choice(
                self.proclamation_templates.get(
                    scroll_type, self.proclamation_templates["sovereignty"]
                )
            )
            formatted_text = template.format(text=text)

            # Add hashtags if enabled
            if auto_hashtag:
                if not hashtags:
                    hashtags = self.hashtag_sets["default"]

                # Ensure tweet doesn't exceed character limit
                available_chars = 280 - len(formatted_text) - 1  # -1 for space
                hashtag_text = " " + " ".join(hashtags)

                if len(hashtag_text) <= available_chars:
                    formatted_text += hashtag_text
                else:
                    # Truncate hashtags if needed
                    truncated_hashtags = []
                    chars_used = 1  # for initial space
                    for tag in hashtags:
                        if chars_used + len(tag) + 1 <= available_chars:  # +1 for space
                            truncated_hashtags.append(tag)
                            chars_used += len(tag) + 1
                        else:
                            break
                    if truncated_hashtags:
                        formatted_text += " " + " ".join(truncated_hashtags)

            # Create tweet
            response = self.client_v2.create_tweet(text=formatted_text)

            if response.data:
                tweet_id = response.data["id"]
                tweet_url = f"https://twitter.com/user/status/{tweet_id}"

                result = {
                    "success": True,
                    "tweet_id": tweet_id,
                    "tweet_url": tweet_url,
                    "text": formatted_text,
                    "timestamp": datetime.now().isoformat(),
                    "type": scroll_type,
                }

                print(f"✅ Scroll proclaimed to Twitter/X!")
                print(f"🔗 URL: {tweet_url}")

                # Save to proclamation history
                self.save_proclamation_history(result)

                return result
            else:
                print("❌ Failed to create tweet")
                return None

        except Exception as e:
            print(f"❌ Error proclaiming scroll: {e}")
            return None

    def proclaim_thread(
        self, texts: List[str], thread_type: str = "sovereignty"
    ) -> List[Dict]:
        """Create a Twitter thread for longer proclamations"""

        if not self.client_v2:
            print("❌ Cannot create thread: Twitter client not initialized")
            return []

        thread_results = []
        previous_tweet_id = None

        try:
            for i, text in enumerate(texts):
                # Format thread numbering
                if len(texts) > 1:
                    thread_text = f"{i+1}/{len(texts)} {text}"
                else:
                    thread_text = text

                # Create tweet (reply to previous if part of thread)
                if previous_tweet_id:
                    response = self.client_v2.create_tweet(
                        text=thread_text, in_reply_to_tweet_id=previous_tweet_id
                    )
                else:
                    response = self.client_v2.create_tweet(text=thread_text)

                if response.data:
                    tweet_id = response.data["id"]
                    tweet_url = f"https://twitter.com/user/status/{tweet_id}"

                    result = {
                        "success": True,
                        "tweet_id": tweet_id,
                        "tweet_url": tweet_url,
                        "text": thread_text,
                        "thread_position": i + 1,
                        "thread_total": len(texts),
                        "timestamp": datetime.now().isoformat(),
                    }

                    thread_results.append(result)
                    previous_tweet_id = tweet_id

                    print(f"✅ Thread {i+1}/{len(texts)} posted")

                    # Rate limiting - wait between tweets
                    if i < len(texts) - 1:
                        time.sleep(2)
                else:
                    print(f"❌ Failed to post thread {i+1}")
                    break

            if thread_results:
                print(f"🧵 Thread completed! {len(thread_results)} tweets posted")
                self.save_thread_history(thread_results, thread_type)

            return thread_results

        except Exception as e:
            print(f"❌ Error creating thread: {e}")
            return thread_results

    def proclaim_with_media(
        self, text: str, media_path: str, scroll_type: str = "sovereignty"
    ) -> Optional[Dict]:
        """Proclaim scroll with attached media (image/video)"""

        if not self.api_v1 or not self.client_v2:
            print("❌ Cannot post with media: Both v1 and v2 APIs required")
            return None

        try:
            # Upload media using v1 API
            media = self.api_v1.media_upload(media_path)

            # Create tweet with media using v2 API
            response = self.client_v2.create_tweet(
                text=text, media_ids=[media.media_id]
            )

            if response.data:
                tweet_id = response.data["id"]
                tweet_url = f"https://twitter.com/user/status/{tweet_id}"

                result = {
                    "success": True,
                    "tweet_id": tweet_id,
                    "tweet_url": tweet_url,
                    "text": text,
                    "media_path": media_path,
                    "timestamp": datetime.now().isoformat(),
                    "type": scroll_type,
                }

                print(f"✅ Media scroll proclaimed!")
                print(f"🔗 URL: {tweet_url}")

                self.save_proclamation_history(result)
                return result

        except Exception as e:
            print(f"❌ Error posting media: {e}")
            return None

    def schedule_proclamation(
        self, text: str, schedule_time: datetime, scroll_type: str = "sovereignty"
    ) -> Dict:
        """Schedule a future proclamation (requires Twitter API Pro/Enterprise)"""
        # Note: Scheduling requires higher-tier Twitter API access
        # This is a placeholder for the feature

        scheduled_post = {
            "text": text,
            "scroll_type": scroll_type,
            "scheduled_time": schedule_time.isoformat(),
            "status": "scheduled",
            "created": datetime.now().isoformat(),
        }

        # Save to scheduled posts file
        try:
            scheduled_file = Path("scheduled_proclamations.json")
            if scheduled_file.exists():
                with open(scheduled_file, "r") as f:
                    scheduled_posts = json.load(f)
            else:
                scheduled_posts = []

            scheduled_posts.append(scheduled_post)

            with open(scheduled_file, "w") as f:
                json.dump(scheduled_posts, f, indent=2)

            print(f"📅 Proclamation scheduled for {schedule_time}")
            return scheduled_post

        except Exception as e:
            print(f"❌ Error scheduling proclamation: {e}")
            return {"error": str(e)}

    def get_proclamation_history(self, limit: int = 50) -> List[Dict]:
        """Get recent proclamation history"""
        try:
            history_file = Path("proclamation_history.json")
            if history_file.exists():
                with open(history_file, "r") as f:
                    history = json.load(f)
                return history[-limit:] if len(history) > limit else history
        except Exception as e:
            print(f"❌ Error loading history: {e}")
        return []

    def save_proclamation_history(self, proclamation: Dict):
        """Save proclamation to history"""
        try:
            history_file = Path("proclamation_history.json")
            if history_file.exists():
                with open(history_file, "r") as f:
                    history = json.load(f)
            else:
                history = []

            history.append(proclamation)

            # Keep only last 1000 proclamations
            if len(history) > 1000:
                history = history[-1000:]

            with open(history_file, "w") as f:
                json.dump(history, f, indent=2)

        except Exception as e:
            print(f"⚠️ Could not save to history: {e}")

    def save_thread_history(self, thread_results: List[Dict], thread_type: str):
        """Save thread to history"""
        thread_record = {
            "thread_id": thread_results[0]["tweet_id"] if thread_results else None,
            "thread_type": thread_type,
            "tweets": thread_results,
            "created": datetime.now().isoformat(),
            "total_tweets": len(thread_results),
        }

        try:
            threads_file = Path("thread_history.json")
            if threads_file.exists():
                with open(threads_file, "r") as f:
                    threads = json.load(f)
            else:
                threads = []

            threads.append(thread_record)

            with open(threads_file, "w") as f:
                json.dump(threads, f, indent=2)

        except Exception as e:
            print(f"⚠️ Could not save thread history: {e}")


# Convenience function for backward compatibility
def proclaim_scroll(text: str, bearer_token: str = None):
    """Simple proclamation function for backward compatibility"""
    proclaimer = CodexTwitterProclaimer(
        bearer_token=bearer_token or "YOUR_TWITTER_BEARER"
    )
    return proclaimer.proclaim_scroll(text)


# Advanced proclamation functions
def proclaim_sovereignty(text: str):
    """Proclaim with sovereignty template"""
    proclaimer = CodexTwitterProclaimer()
    return proclaimer.proclaim_scroll(text, scroll_type="sovereignty")


def proclaim_wisdom(text: str):
    """Proclaim with wisdom template"""
    proclaimer = CodexTwitterProclaimer()
    return proclaimer.proclaim_scroll(text, scroll_type="wisdom")


def proclaim_celebration(text: str):
    """Proclaim with celebration template"""
    proclaimer = CodexTwitterProclaimer()
    return proclaimer.proclaim_scroll(text, scroll_type="celebration")


def proclaim_thread(texts: List[str]):
    """Create a proclamation thread"""
    proclaimer = CodexTwitterProclaimer()
    return proclaimer.proclaim_thread(texts)


# Example usage and testing
if __name__ == "__main__":
    print("🔥 Codex Dominion Twitter/X Proclamation System")

    # Initialize proclaimer
    proclaimer = CodexTwitterProclaimer()

    # Test connection
    if proclaimer.test_connection():
        print("✅ Ready to proclaim sacred scrolls!")

        # Example proclamations
        example_texts = [
            "The sacred flames of digital sovereignty burn eternal! 🔥",
            "New pathways to digital independence have been revealed.",
            "The Codex grows stronger with each passing moment.",
        ]

        print("\n🧪 Example proclamations (not posted):")
        for i, text in enumerate(example_texts, 1):
            print(f"{i}. {text}")

        # Uncomment to test actual posting (requires valid credentials)
        # result = proclaimer.proclaim_scroll("Testing Codex Dominion integration! 🔥")
        # print(f"Result: {result}")

    else:
        print("❌ Cannot connect to Twitter. Please check credentials.")
        print("💡 Update twitter_config.json or set environment variables.")
