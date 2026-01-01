# 🎬 VIDEO STUDIO - QUICK REFERENCE

## 🚀 Getting Started (5 Minutes)

### 1. Run Migration
```bash
python migrate_video_studio.py
```

### 2. Start Dashboard
```bash
python flask_dashboard.py
```

### 3. Open Studio
```
http://localhost:5000/studio/video
```

---

## 📍 Key URLs

| Resource | URL |
|----------|-----|
| **Main Studio** | `/studio/video` |
| **Library** | `/studio/video/library` |
| **Team Library** | `/studio/video/team/<team_id>` |
| **Generate Scene** | `POST /api/video/generate-scene` |
| **Save Project** | `POST /api/video/save-project` |
| **Get Project** | `GET /api/video/project/<id>` |

---

## 🎨 Interface Layout

```
┌───────────┬─────────────────┬──────────┐
│ Storyboard│    Preview      │ Assets   │
│  (Scenes) │   (Player)      │ (Clips)  │
├───────────┴─────────────────┴──────────┤
│          Timeline (Tracks)             │
├────────────────────────────────────────┤
│    Prompt Input + Generate Button      │
└────────────────────────────────────────┘
```

---

## 🤖 AI Engines

| Engine | Best For | Speed | Quality |
|--------|----------|-------|---------|
| **Runway Gen-3** | General purpose | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ |
| **Pika Labs** | Creative effects | ⚡⚡ | ⭐⭐⭐⭐ |
| **Luma AI** | Cinematic shots | ⚡ | ⭐⭐⭐⭐⭐ |
| **Stability Video** | Stylized art | ⚡⚡⚡ | ⭐⭐⭐⭐ |

---

## 📊 Data Models

### VideoProject
```python
{
  "id": "proj_001",
  "title": "My Video",
  "storyboard": [
    {"scene_id": 1, "prompt": "...", "video_url": "..."}
  ],
  "timeline": {
    "layers": [
      {"id": 1, "clips": [{"start": 0, "end": 5, "asset_id": 1}]}
    ]
  },
  "audio_tracks": [
    {"id": 1, "url": "...", "start": 0, "volume": 0.8}
  ]
}
```

### VideoAsset
```python
{
  "id": "asset_001",
  "asset_type": "video",  # or "audio", "image", "overlay"
  "file_url": "https://...",
  "duration": 5.0,
  "prompt": "Mystical forest"
}
```

---

## 🔧 Environment Variables

### Storage
```bash
VIDEO_STORAGE_PROVIDER=local  # or s3, gcs, azure

# S3
AWS_S3_BUCKET=...
AWS_S3_ACCESS_KEY=...
AWS_S3_SECRET_KEY=...

# GCS
GCS_BUCKET=...
GCS_CREDENTIALS=...

# Azure
AZURE_CONTAINER=...
AZURE_CONNECTION_STRING=...
```

### Generation
```bash
VIDEO_GEN_ENGINE=runway  # default engine

# API Keys (at least one)
RUNWAY_API_KEY=...
PIKA_API_KEY=...
LUMA_API_KEY=...
STABILITY_API_KEY=...
```

---

## 💻 Code Examples

### Generate a Scene
```python
import requests

response = requests.post('http://localhost:5000/api/video/generate-scene', json={
    "prompt": "A mystical forest at dawn",
    "engine": "runway",
    "duration": 5.0
})

result = response.json()
print(f"Video URL: {result['video_url']}")
```

### Save a Project
```python
import requests

response = requests.post('http://localhost:5000/api/video/save-project', json={
    "title": "My Epic Video",
    "description": "A cinematic journey",
    "storyboard": [
        {
            "scene_id": 1,
            "prompt": "Opening scene",
            "duration": 5.0,
            "video_url": "https://..."
        }
    ],
    "timeline": {
        "layers": [
            {
                "id": 1,
                "clips": [{"start": 0, "end": 5, "asset_id": 1}]
            }
        ]
    },
    "tags": ["epic", "cinematic"],
    "category": "narrative"
})

project_id = response.json()['project_id']
```

### Get Project Library
```python
import requests

response = requests.get('http://localhost:5000/studio/video/library')
projects = response.json()['projects']

for project in projects:
    print(f"{project['title']} - {project['duration']}s")
```

---

## 🎯 Workflow Example

### Creating Your First Video

**1. Generate Opening Scene**
```
Prompt: "A majestic mountain at sunrise"
Engine: Runway Gen-3
Duration: 5s
→ Click "Generate"
```

**2. Generate Middle Scene**
```
Prompt: "A flowing river through the valley"
Engine: Runway Gen-3
Duration: 5s
→ Click "Generate"
```

**3. Generate Closing Scene**
```
Prompt: "Eagles soaring in the sky"
Engine: Luma AI
Duration: 5s
→ Click "Generate"
```

**4. Arrange on Timeline**
- Drag Scene 1 to Video Layer 1 (0-5s)
- Drag Scene 2 to Video Layer 1 (5-10s)
- Drag Scene 3 to Video Layer 1 (10-15s)

**5. Add Audio**
- Upload background music
- Drag to Audio Track (0-15s)
- Adjust volume to 0.7

**6. Save Project**
```
Title: "Nature's Symphony"
Category: "cinematic"
Tags: ["nature", "mountains", "inspiring"]
→ Click "Save"
```

---

## 🐛 Troubleshooting

### Database Not Found
```bash
# Run migration
python migrate_video_studio.py
```

### "Generation failed"
- Check API keys in .env
- Verify engine is spelled correctly
- Ensure engine API is reachable

### Assets Not Loading
- Check VIDEO_STORAGE_PROVIDER setting
- For S3: Verify AWS credentials
- For local: Check uploads/videos/ directory exists

### Timeline Not Working
- Browser console may show errors
- Ensure jQuery/drag-and-drop libraries loaded
- Check network tab for failed API calls

---

## 📈 Performance Tips

### For Fast Generation
- Use Runway Gen-3 (fastest)
- Keep scenes under 5 seconds
- Generate scenes in parallel

### For Best Quality
- Use Luma AI for cinematic shots
- Use detailed prompts (20+ words)
- Specify camera angles and lighting

### For Storage Efficiency
- Use S3 with lifecycle policies
- Compress videos to H.264/MP4
- Delete unused assets regularly

---

## 🔗 Related Systems

| System | Integration Point |
|--------|-------------------|
| **Graphics Studio** | Share prompts, evolution DNA |
| **Prompt Evolution** | Video prompts can evolve |
| **Team Workspace** | Collaborative video editing |
| **Treasury** | Track video generation costs |

---

## 📚 Documentation

- [VIDEO_STUDIO_DOCUMENTATION.md](VIDEO_STUDIO_DOCUMENTATION.md) - Full architecture guide
- [flask_dashboard.py](flask_dashboard.py) - Model definitions (lines 143-540)
- [migrate_video_studio.py](migrate_video_studio.py) - Database migration

---

## 🔥 Status

**Phase 1**: ✅ COMPLETE  
**Database**: ✅ Ready  
**Interface**: ✅ Operational  
**API**: ✅ Functional  
**Storage**: ✅ Multi-provider  
**Generation**: ⏳ Placeholders (awaiting API keys)

---

## 🎉 Quick Win

```bash
# Complete setup in 3 commands:
python migrate_video_studio.py
python flask_dashboard.py
# Open: http://localhost:5000/studio/video
```

**The Temple of Motion Awaits! 🎬**

---

**Last Updated**: December 22, 2025  
**Version**: 1.0.0
