"""
CodexDominion Launch Social Media Integration
==============================================

Provides programmatic access to launch social posts and templates.
Integrates with existing social media automation systems.

Usage:
    from launch_social_integration import LaunchSocialManager
    
    manager = LaunchSocialManager()
    
    # Get all posts
    all_posts = manager.get_all_posts()
    
    # Get posts by category
    hero_posts = manager.get_posts_by_category("hero")
    
    # Get posts by priority
    critical_posts = manager.get_posts_by_priority("critical")
    
    # Get posts for specific audience
    youth_posts = manager.get_posts_by_audience("youth")
    
    # Schedule posts
    manager.schedule_launch_day_posts()
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

class LaunchSocialManager:
    """Manages CodexDominion launch social media content"""
    
    def __init__(self, data_path: Optional[Path] = None):
        """
        Initialize the Launch Social Manager
        
        Args:
            data_path: Path to launch_social_posts.json (optional)
        """
        if data_path is None:
            # Get the directory where this script is located
            base_dir = Path(__file__).parent
            data_path = base_dir / "content" / "launch-assets" / "launch_social_posts.json"
        
        self.data_path = data_path
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Load social posts data from JSON"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Launch social posts file not found: {self.data_path}")
            return {"meta": {}, "posts": {}, "scheduling": {}}
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parse error: {e}")
            return {"meta": {}, "posts": {}, "scheduling": {}}
    
    def get_all_posts(self) -> Dict[str, List[Dict]]:
        """Get all posts organized by category"""
        return self.data.get("posts", {})
    
    def get_posts_by_category(self, category: str) -> List[Dict]:
        """
        Get posts for a specific category
        
        Args:
            category: One of: hero, creator, youth, diaspora, brand, marketplace, hype
        
        Returns:
            List of post dictionaries
        """
        return self.data.get("posts", {}).get(category, [])
    
    def get_posts_by_priority(self, priority: str) -> List[Dict]:
        """
        Get posts by priority level
        
        Args:
            priority: One of: critical, high, medium, low
        
        Returns:
            List of post dictionaries matching priority
        """
        posts = []
        for category, category_posts in self.data.get("posts", {}).items():
            for post in category_posts:
                if post.get("priority") == priority:
                    posts.append({**post, "category": category})
        return posts
    
    def get_posts_by_audience(self, audience: str) -> List[Dict]:
        """
        Get posts targeting a specific audience
        
        Args:
            audience: One of: creators, youth, diaspora
        
        Returns:
            List of post dictionaries
        """
        posts = []
        for category, category_posts in self.data.get("posts", {}).items():
            for post in category_posts:
                if post.get("audience") == audience:
                    posts.append({**post, "category": category})
        return posts
    
    def get_launch_day_posts(self) -> Dict[str, List[Dict]]:
        """Get posts scheduled for launch day organized by wave"""
        scheduling = self.data.get("scheduling", {}).get("launch_day", {})
        all_posts = self.get_all_posts()
        
        waves = {}
        for wave_name, post_ids in scheduling.items():
            wave_posts = []
            for post_id in post_ids:
                # Find post by ID across all categories
                for category, posts in all_posts.items():
                    for post in posts:
                        if post.get("id") == post_id:
                            wave_posts.append({**post, "category": category})
            waves[wave_name] = wave_posts
        
        return waves
    
    def get_week_posts(self, week: int) -> Dict[str, List[Dict]]:
        """
        Get posts for a specific week
        
        Args:
            week: Week number (1, 2, or 3+)
        
        Returns:
            Dictionary of focus areas with posts
        """
        week_key = f"week_{week}" if week < 3 else "week_3_plus"
        scheduling = self.data.get("scheduling", {}).get(week_key, {})
        all_posts = self.get_all_posts()
        
        week_content = {}
        for focus_area, post_ids in scheduling.items():
            if focus_area == "rotation":
                continue
            
            focus_posts = []
            for post_id in post_ids:
                for category, posts in all_posts.items():
                    for post in posts:
                        if post.get("id") == post_id:
                            focus_posts.append({**post, "category": category})
            week_content[focus_area] = focus_posts
        
        return week_content
    
    def format_for_platform(self, post: Dict, platform: str) -> str:
        """
        Format post text for specific platform
        
        Args:
            post: Post dictionary
            platform: One of: instagram, tiktok, twitter, facebook, linkedin
        
        Returns:
            Formatted post text with hashtags
        """
        text = post.get("text", "")
        hashtags = " ".join(post.get("hashtags", []))
        
        if platform == "twitter":
            # Twitter has character limit
            max_length = 280 - len(hashtags) - 1
            if len(text) > max_length:
                text = text[:max_length-3] + "..."
        
        elif platform == "linkedin":
            # LinkedIn: More professional, hashtags at end
            return f"{text}\n\n{hashtags}"
        
        elif platform in ["instagram", "tiktok", "facebook"]:
            # Instagram/TikTok/Facebook: Hashtags on same line or new line
            return f"{text}\n\n{hashtags}"
        
        return f"{text} {hashtags}"
    
    def get_post_by_id(self, post_id: int) -> Optional[Dict]:
        """
        Get a specific post by ID
        
        Args:
            post_id: Post ID (1-50)
        
        Returns:
            Post dictionary or None if not found
        """
        for category, posts in self.get_all_posts().items():
            for post in posts:
                if post.get("id") == post_id:
                    return {**post, "category": category}
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the launch content"""
        meta = self.data.get("meta", {})
        all_posts = self.get_all_posts()
        
        return {
            "total_posts": meta.get("total_posts", 0),
            "categories": list(all_posts.keys()),
            "posts_by_category": {cat: len(posts) for cat, posts in all_posts.items()},
            "critical_posts": len(self.get_posts_by_priority("critical")),
            "high_priority_posts": len(self.get_posts_by_priority("high")),
            "version": meta.get("version", "unknown"),
            "last_updated": meta.get("last_updated", "unknown")
        }
    
    def export_to_csv(self, output_path: Path):
        """
        Export all posts to CSV for spreadsheet use
        
        Args:
            output_path: Path to save CSV file
        """
        import csv
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['id', 'category', 'text', 'hashtags', 'priority', 'audience', 'timing']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for category, posts in self.get_all_posts().items():
                for post in posts:
                    writer.writerow({
                        'id': post.get('id'),
                        'category': category,
                        'text': post.get('text', '').replace('\n', ' '),
                        'hashtags': ' '.join(post.get('hashtags', [])),
                        'priority': post.get('priority', ''),
                        'audience': post.get('audience', ''),
                        'timing': post.get('timing', '')
                    })
        
        print(f"✅ Exported to {output_path}")


# Example usage and CLI interface
if __name__ == "__main__":
    import sys
    
    manager = LaunchSocialManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "stats":
            stats = manager.get_stats()
            print("\n📊 Launch Social Content Stats:")
            print(f"   Total Posts: {stats['total_posts']}")
            print(f"   Categories: {', '.join(stats['categories'])}")
            print(f"   Critical Posts: {stats['critical_posts']}")
            print(f"   High Priority: {stats['high_priority_posts']}")
            print(f"   Version: {stats['version']}")
        
        elif command == "category" and len(sys.argv) > 2:
            category = sys.argv[2]
            posts = manager.get_posts_by_category(category)
            print(f"\n📱 {category.upper()} Posts ({len(posts)}):\n")
            for post in posts:
                print(f"#{post['id']}: {post['text'][:60]}...")
        
        elif command == "launch":
            waves = manager.get_launch_day_posts()
            print("\n🚀 Launch Day Schedule:\n")
            for wave, posts in waves.items():
                print(f"{wave.upper()}: {len(posts)} posts")
                for post in posts:
                    print(f"  - #{post['id']}: {post['text'][:50]}...")
        
        elif command == "export" and len(sys.argv) > 2:
            output_path = Path(sys.argv[2])
            manager.export_to_csv(output_path)
        
        else:
            print("Usage:")
            print("  python launch_social_integration.py stats")
            print("  python launch_social_integration.py category <category>")
            print("  python launch_social_integration.py launch")
            print("  python launch_social_integration.py export <output.csv>")
    
    else:
        # Default: Show quick overview
        stats = manager.get_stats()
        print("\n🔥 CodexDominion Launch Social Manager")
        print(f"   {stats['total_posts']} posts ready for deployment")
        print(f"   {stats['critical_posts']} critical launch posts")
        print("\n   Run with --help for usage examples")
