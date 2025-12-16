# API Keys Configuration Guide

## Configured Status (Run connect-api-keys.ps1 to update)

This file tracks which APIs have been configured with real credentials.

### Current Status
- ❌ YouTube Data API: Not configured (using placeholder)
- ❌ TikTok Business API: Not configured (using placeholder)
- ❌ Pinterest API: Not configured (using placeholder)
- ✅ ShareASale Affiliate: Demo mode (switch to real when credentials added)
- ❌ Instagram Basic Display: Not configured

### Quick Setup Instructions

Run the interactive configuration wizard:
```powershell
.\connect-api-keys.ps1
```

Or manually update config files:
- `youtube_config.json` - Add YouTube API key and channel ID
- `tiktok_config.json` - Add TikTok client credentials
- `pinterest_config.json` - Add Pinterest app credentials
- `affiliate_config.json` - Add ShareASale merchant/affiliate IDs
- `instagram_config.json` - Create with Instagram credentials

### API Documentation Links
- YouTube: https://developers.google.com/youtube/v3/getting-started
- TikTok: https://developers.tiktok.com/
- Pinterest: https://developers.pinterest.com/docs/getting-started/introduction/
- ShareASale: https://www.shareasale.com/info/affiliates/api-introduction/
- Instagram: https://developers.facebook.com/docs/instagram-basic-display-api

**Note**: Until real API keys are added, dashboards will display demo/mock data.
