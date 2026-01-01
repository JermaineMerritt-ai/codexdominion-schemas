# 🌠 Creative Constellation - Quick Start Guide

## ✅ System Status: OPERATIONAL

**Flask Dashboard**: Running on http://localhost:5000

## 🚀 How to Access the Constellation

### Option 1: Demo Account (Fastest)
1. Go to: **http://localhost:5000/login**
2. Login with demo credentials:
   - Email: `demo@codex.ai`
   - Password: `demo123`
3. Navigate to your constellation:
   - **Team ID 2**: http://localhost:5000/studio/graphics/team/2/constellation
   - **AI Prompts**: http://localhost:5000/studio/graphics/recommendations/2/prompts
   - **Team Library**: http://localhost:5000/studio/graphics/team/2

### Option 2: Create New Account
1. Go to: **http://localhost:5000/signup**
2. Create an account
3. Create a new team
4. Add some projects with tags and categories
5. Click **🌠 Creative Constellation** button

## 🌌 What You'll See

The constellation is a **force-directed graph** that shows:

- **🌟 Projects** (8px stars) - Colored by mood
  - Dramatic = Red
  - Serene = Cyan
  - Vibrant = Amber
  - Mysterious = Purple
  - Ethereal = Pink
  - And more!

- **⚡ Tags** (5-20px nodes) - Amber glow, size by frequency
  - Example: fantasy, scifi, nature, urban, surreal, minimal, detailed, colorful

- **🔮 Categories** (20-40px clusters) - Purple, size by usage
  - Example: Character Art, Landscape, Concept Art, Portrait, Abstract

## 🎮 Interactive Features

### Hover Over Nodes:
- **Projects**: See mood, palette, category, and prompt preview
- **Tags**: See "Tag used in X projects"
- **Categories**: See "X projects in this category"

### Click on Nodes:
- **Projects**: Opens directly in graphics studio
- **Tags/Categories**: Reserved for future filtering

### Controls:
- **Zoom**: Mouse wheel or pinch
- **Pan**: Click and drag
- **Auto-Rotate**: Watch the constellation breathe!

### Legend:
- Bottom-left shows node type indicators
- Bottom-right shows stats (project/tag/category counts)

## 📊 Demo Data

The demo team (ID: 2) includes:
- **25 sample projects**
- **5 moods**: dramatic, serene, vibrant, mysterious, ethereal
- **5 color palettes**: warm, cool, monochrome, vibrant, pastel
- **5 categories**: Character Art, Landscape, Concept Art, Portrait, Abstract
- **8 tags**: fantasy, scifi, nature, urban, surreal, minimal, detailed, colorful

## 🎨 Full Feature Set

1. **Team Library** - Grid view of all projects
2. **Creative Universe** - Tag cloud + category bubbles
3. **AI Prompt Suggestions** - 8 sophisticated templates based on team DNA
4. **Creative Constellation** - Force-directed graph (NEW!)

## 🔥 Next Steps

### To Add More Projects:
1. Go to graphics studio: http://localhost:5000/studio/graphics
2. Enter a prompt and select options
3. Click "Generate" or "Save to Team"
4. Your constellation updates automatically!

### To Generate AI Prompts:
1. Visit: http://localhost:5000/studio/graphics/recommendations/2/prompts
2. See team's creative DNA breakdown
3. Click "Use This Prompt" to pre-fill studio
4. Click "Generate 5 More Prompts" for unlimited inspiration

### To Explore Universe:
1. Visit: http://localhost:5000/studio/graphics/team/2/universe
2. See tag cloud (larger = more used)
3. See category bubbles with mood/palette indicators
4. Click "Creative Constellation" to switch views

## 🐛 Troubleshooting

**If Flask stops:**
```powershell
python flask_dashboard.py
```

**If you need to create more demo data:**
```powershell
python create_demo_constellation.py
```

**If database needs reset:**
```powershell
Remove-Item codex_graphics.db
python -c "from flask_dashboard import db, app; app.app_context().push(); db.create_all()"
python create_demo_constellation.py
```

## 🎯 What Makes This Special

The constellation isn't just a visualization—it's a **creative mirror** that reveals:
- **Dominant themes** (large clusters)
- **Hidden patterns** (connection density)
- **Unexplored edges** (isolated nodes)
- **Creative gravity** (node attraction)
- **Stylistic DNA** (team fingerprint)

It's a **ritual map** for witnessing your team's imagination as a living constellation! 🌌

---

**🔥 The Flame Burns Sovereign and Eternal!** 👑
