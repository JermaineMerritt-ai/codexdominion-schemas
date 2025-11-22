"""
🔥 YOUTUBE CHARTS SETUP GUIDE 👑
Complete setup instructions for YouTube API integration

The Merritt Method™ - YouTube Analytics Mastery
"""

import json
import os
from pathlib import Path

def setup_youtube_api():
    """Complete YouTube API setup guide and checker"""
    
    print("🔥 CODEX YOUTUBE CHARTS SETUP 👑")
    print("=" * 50)
    
    # Step 1: API Key Setup
    print("\n📋 STEP 1: YouTube API Key Setup")
    print("-" * 30)
    print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
    print("2. Create a new project or select existing project")
    print("3. Enable YouTube Data API v3")
    print("4. Create credentials (API Key)")
    print("5. Copy your API key")
    
    # Check for API key
    api_key = os.getenv("YOUTUBE_API_KEY")
    config_file = Path("youtube_config.json")
    
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            config_api_key = config.get("youtube", {}).get("api_key")
            
            if config_api_key and config_api_key != "YOUR_YOUTUBE_API_KEY_HERE":
                print("✅ API Key found in config file")
            else:
                print("❌ API Key not configured in youtube_config.json")
                print("   Please edit youtube_config.json and add your API key")
        except Exception as e:
            print(f"❌ Error reading config: {e}")
    else:
        print("❌ Configuration file not found")
    
    if api_key and api_key != "YOUR_YOUTUBE_API_KEY_HERE":
        print("✅ API Key found in environment variables")
    else:
        print("❌ YOUTUBE_API_KEY environment variable not set")
        print("   You can set it with: set YOUTUBE_API_KEY=your_key_here")
    
    # Step 2: Channel ID Setup
    print("\n📺 STEP 2: Channel ID Setup")
    print("-" * 30)
    print("To find your Channel ID:")
    print("1. Go to YouTube Studio: https://studio.youtube.com/")
    print("2. Click Settings (gear icon)")
    print("3. Click Channel > Basic info")
    print("4. Copy your Channel ID")
    print("\nAlternatively:")
    print("1. Go to your channel page")
    print("2. Look at the URL: youtube.com/channel/YOUR_CHANNEL_ID")
    print("3. Copy the ID after '/channel/'")
    
    # Step 3: Dependencies
    print("\n📦 STEP 3: Install Dependencies")
    print("-" * 30)
    print("Install required packages:")
    print("pip install google-api-python-client")
    print("pip install google-auth-oauthlib")
    print("pip install google-auth-httplib2")
    
    # Test imports
    try:
        from googleapiclient.discovery import build
        print("✅ google-api-python-client is installed")
    except ImportError:
        print("❌ google-api-python-client not installed")
        print("   Run: pip install google-api-python-client")
    
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        print("✅ google-auth-oauthlib is installed")
    except ImportError:
        print("❌ google-auth-oauthlib not installed")
        print("   Run: pip install google-auth-oauthlib")
    
    # Step 4: Test Configuration
    print("\n🧪 STEP 4: Test Your Setup")
    print("-" * 30)
    
    try:
        from codex_youtube_charts import CodexYouTubeCharts
        
        youtube_system = CodexYouTubeCharts()
        
        # Test basic initialization
        print("✅ YouTube Charts system initialized")
        
        # Test API connection
        if youtube_system.test_connection():
            print("✅ YouTube API connection successful!")
        else:
            print("❌ YouTube API connection failed")
            print("   Check your API key and internet connection")
        
        # Test metrics (with dummy channel ID)
        test_metrics = youtube_system.youtube_metrics("UCBJycsmduvYEL83R_U4JriQ")  # YouTube's own channel
        if not test_metrics.get("error"):
            print("✅ YouTube metrics retrieval working")
        else:
            print(f"❌ YouTube metrics test failed: {test_metrics.get('error')}")
    
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
    
    # Step 5: Usage Examples
    print("\n💡 STEP 5: Usage Examples")
    print("-" * 30)
    print("Basic usage in your code:")
    print("""
# Import the functions
from codex_youtube_charts import youtube_metrics, archive_youtube, get_youtube_analytics

# Get channel metrics
metrics = youtube_metrics("YOUR_CHANNEL_ID")
print(f"Subscribers: {metrics['subscribers']}")

# Get comprehensive analytics
analytics = get_youtube_analytics("YOUR_CHANNEL_ID")

# Archive the results
archive_youtube(analytics)
""")
    
    print("\n🎯 Quick Start Checklist:")
    print("□ API Key obtained from Google Cloud Console")
    print("□ API Key added to youtube_config.json")
    print("□ Channel ID added to youtube_config.json")
    print("□ Dependencies installed (google-api-python-client, etc.)")
    print("□ Test connection successful")
    print("□ Dashboard accessible at http://127.0.0.1:18080")
    
    print("\n🔥 Your YouTube Charts system is ready for digital sovereignty! 👑")

if __name__ == "__main__":
    setup_youtube_api()