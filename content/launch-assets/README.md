# CodexDominion Launch Assets - Master Index

> **Location:** `content/launch-assets/`  
> **Status:** Production Ready  
> **Last Updated:** December 24, 2025

---

## 📁 Available Assets

### 1. **LAUNCH_DAY_SOCIAL_PACK.md**
**Purpose:** 50 ready-to-post social media captions  
**Categories:** Hero, Creator, Youth, Diaspora, Brand, Marketplace, Hype  
**Usage:** Copy-paste directly to Instagram, TikTok, X, Facebook, LinkedIn  
**Features:**
- Launch moment posts (critical priority)
- Audience-specific messaging
- Hashtag strategy included
- Posting schedule recommendations

**Quick Access:**
```bash
# View in terminal
cat content/launch-assets/LAUNCH_DAY_SOCIAL_PACK.md

# Open in editor
code content/launch-assets/LAUNCH_DAY_SOCIAL_PACK.md
```

---

### 2. **PROMO_TEMPLATES.md**
**Purpose:** Customizable templates for Creators, Youth, and Diaspora  
**Templates:** 15 total (5 per audience)  
**Features:**
- [Bracketed] customization points
- Platform-specific guidance
- Best practices for timing and frequency
- Engagement strategies

**Quick Access:**
```bash
cat content/launch-assets/PROMO_TEMPLATES.md
```

---

### 3. **LAUNCH_RUNBOOK.md**
**Purpose:** Complete operational guide for launch execution  
**Sections:**
- Vision & Strategy (The Why)
- Platform Architecture (The What)
- 4-Phase Launch Plan (The How)
- Hour-by-Hour Timeline (The Execution)
- Metrics & KPIs (The Measurement)
- Culture & Values (The Movement)

**Target Audience:** Internal team, leadership, operations  
**Quick Access:**
```bash
cat content/launch-assets/LAUNCH_RUNBOOK.md
```

---

### 4. **launch_social_posts.json**
**Purpose:** Machine-readable version of all 50 posts  
**Format:** JSON with metadata  
**Features:**
- Post ID, text, hashtags
- Priority levels (critical, high, medium, low)
- Audience targeting
- Scheduling recommendations
- Category grouping

**Integration:** Use with social media automation scripts  

**Quick Access:**
```bash
# View JSON

---

### 5. **KEYNOTE_SLIDE_DECK.md**
**Purpose:** 15-slide launch keynote presentation  
**Duration:** 10-12 minutes  
**Audience:** Creators, Youth, Diaspora, Press, Partners  
**Features:**
- Complete slide-by-slide breakdown
- Visual design specifications (layout, colors, typography)
- Voiceover script with timing
- Technical production specs (1920x1080, 30fps, MP4)
- Music and animation guidance
- Distribution plan for launch day

**Quick Access:**
```bash
cat content/launch-assets/KEYNOTE_SLIDE_DECK.md
```

---

### 6. **CREATOR_SPOTLIGHT_SCRIPTS.md**
**Purpose:** 5 episodic video scripts featuring real creators  
**Duration:** 60-90 seconds per episode  
**Format:** Vertical video (9:16 for Instagram Reels/TikTok)  
**Episodes:**
- Episode 1: The Writer (Caribbean children's stories)
- Episode 2: The Designer (Instagram templates)
- Episode 3: The Music Producer (Sample packs)
- Episode 4: The Educator (Digital courses)
- Episode 5: The Diaspora Creator (Cultural bridge)

**Features:**
- Full visual storyboards with timestamps
- Voiceover scripts
- On-screen text overlays
- Music and color grading specifications
- Distribution strategy and release schedule

**Quick Access:**
```bash
cat content/launch-assets/CREATOR_SPOTLIGHT_SCRIPTS.md
```

---

### 7. **DOMINIONYOUTH_90DAY_CHALLENGE.md**
**Purpose:** 12-week progressive earning challenge for Caribbean youth  
**Goal:** $500+ earned in 90 days through structured tasks  
**Structure:**
- 12 weeks of challenges (5 tasks per week)
- Progressive difficulty: Starter → Intermediate → Advanced → Elite
- Badge and leaderboard system
- 6,000+ total points available
- Weekly completion bonuses

**Features:**
- Daily task breakdowns with XP values
- Earning potential estimates per task
- Badge system (60+ unique badges)
- Leaderboard tiers (Bronze → Platinum → Elite)
- Technical implementation specs for dashboard
- Mobile app integration guidelines

**Quick Access:**
```bash
cat content/launch-assets/DOMINIONYOUTH_90DAY_CHALLENGE.md
```

---

### 8. **INVESTOR_NARRATIVE_DECK.md**
**Purpose:** 15-slide investor pitch deck for seed fundraising  
**Raise Target:** $500K-$2M seed round  
**Audience:** Angel investors, VCs, strategic partners  
**Key Slides:**
- Problem/Solution (market validation)
- Business model (80% gross margins)
- Market size (TAM: $250B, SAM: $15B, SOM: $500M)
- Traction metrics (200+ creators, 500+ youth, $25K GMV)
- Competitive landscape (category creator positioning)
- 3-year financial projections (path to $10M revenue)
- Go-to-market strategy (flywheel-driven growth)
- The Ask (use of funds breakdown)

**Features:**
- Complete slide content with data visualizations
- Investor FAQ (anticipated questions + answers)
- Pitch delivery notes (12-15 min presentation)
- Appendix slides (detailed financials, testimonials, tech architecture)

**Quick Access:**
```bash
cat content/launch-assets/INVESTOR_NARRATIVE_DECK.md
cat content/launch-assets/launch_social_posts.json | jq '.'

# Load in Python
python -c "import json; print(json.load(open('content/launch-assets/launch_social_posts.json'))['meta'])"
```

---

## 🚀 Quick Start Guide

### For Social Media Managers

**Day of Launch:**
1. Open `LAUNCH_DAY_SOCIAL_PACK.md`
2. Start with Hero Posts (#1-5) at launch moment
3. Deploy Hype Posts (#46-50) throughout the day
4. Monitor engagement and adjust

**Week 1:**
- Focus on Creator Posts (#6-15)
- Use Marketplace Posts (#41-45)
- Share creator testimonials

**Week 2+:**
- Rotate Youth Posts (#16-25)
- Deploy Diaspora Posts (#26-35)
- Use Brand Anthem Posts (#36-40) for storytelling

### For Creators

**Promote Your Products:**
1. Open `PROMO_TEMPLATES.md`
2. Choose "Creator Promo Templates"
3. Select template matching your goal
4. Replace [bracketed] content with your specifics
5. Add your product link
6. Post during peak times (6-9 PM EST)

### For Youth Promoters

**Earn Commissions:**
1. Open `PROMO_TEMPLATES.md`
2. Choose "Youth Promo Templates"
3. Get your affiliate link from dashboard
4. Update template with your rank/sales
5. Post daily during challenges

### For Diaspora Advocates

**Support Home:**
1. Open `PROMO_TEMPLATES.md`
2. Choose "Diaspora Promo Templates"
3. Share in diaspora communities
4. Tag diaspora influencers
5. Use geo-tags for major cities (NYC, Toronto, London)

### For Leadership/Operations

**Execute Launch:**
1. Open `LAUNCH_RUNBOOK.md`
2. Review Section 4 (Hour-by-Hour Timeline)
3. Assign teams to roles (Section 7)
4. Monitor metrics (Section 5)
5. Follow contingency plans if needed (Section 8)

---

## 🔧 Integration with Existing Systems

### Flask Dashboard Integration
```python
# Add to flask_dashboard.py social routes

@app.route('/api/launch-posts')
def get_launch_posts():
    """Get all 50 launch posts with metadata"""
    data = load_json("content/launch-assets/launch_social_posts.json")
    return jsonify(data)

@app.route('/api/launch-posts/<category>')
def get_posts_by_category(category):
    """Get posts by category (hero, creator, youth, etc.)"""
    data = load_json("content/launch-assets/launch_social_posts.json")
    return jsonify(data["posts"].get(category, []))
```

### Social Media Dashboard
Add new tab to http://localhost:5000/social:
- "Launch Posts" section
- Category filters
- Quick copy buttons
- Scheduling interface
- Performance tracking

### Automated Posting
```python
# Use with existing social media automation
from social_media_automation import post_to_platform

posts = load_json("content/launch-assets/launch_social_posts.json")
hero_posts = posts["posts"]["hero"]

for post in hero_posts:
    post_to_platform("instagram", post["text"], post["hashtags"])
```

---

## 📊 Metrics & Tracking

**Track These KPIs:**
- Post impressions by category
- Engagement rate (likes, comments, shares)
- Click-through rate on links
- Conversion from post to signup/purchase
- Best performing posts (save for retargeting)

**Dashboard Integration:**
- Add "Launch Campaign" section to analytics
- Real-time engagement tracking
- A/B test different posts
- Identify top-performing content

---

## ✏️ Customization Guidelines

### Editing Posts
**DO:**
- Adjust for platform-specific character limits
- Add emojis where appropriate
- Include relevant images/videos
- Test links before posting

**DON'T:**
- Change core messaging
- Remove hashtags
- Skip priority/critical posts
- Ignore timing recommendations

### Creating New Posts
**Follow This Structure:**
1. Lead with impact (first line hooks)
2. Clear call-to-action
3. Relevant hashtags (3-5 max)
4. Brand voice: Bold, direct, inspiring
5. Cultural authenticity

---

## 🎯 Success Criteria

**Launch Day (Day 0):**
- ✅ All Hero posts deployed
- ✅ Hype posts scheduled
- ✅ 100k+ impressions
- ✅ 5k+ engagements
- ✅ Trending in Caribbean social

**Week 1:**
- ✅ Creator engagement rate >8%
- ✅ Youth signup conversion >10%
- ✅ Diaspora click-through >5%
- ✅ 500k+ total impressions

**Month 1:**
- ✅ 2M+ impressions across all platforms
- ✅ 50k+ profile visits
- ✅ 10k+ link clicks
- ✅ Featured in 20+ media outlets

---

## 📞 Support & Questions

**Internal Team:**
- Slack: #launch-social-media
- Email: social@codexdominion.com

**External Partners:**
- Press inquiries: press@codexdominion.com
- Creator support: creators@codexdominion.com
- Youth support: youth@codexdominion.com

---

## 🔄 Version History

- **v1.0** (Dec 24, 2025): Initial launch pack creation
  - 50 social posts
  - 15 promo templates
  - Full launch runbook
  - JSON integration ready

---

**🔥 The Caribbean's digital economy begins now.**  
**Build the future. Own the system.**

👑 *CodexDominion*
