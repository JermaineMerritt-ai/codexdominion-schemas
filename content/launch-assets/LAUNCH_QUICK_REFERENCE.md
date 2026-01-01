# 🚀 CODEXDOMINION LAUNCH - QUICK COMMAND REFERENCE

> **For:** Social Media Managers, Creators, Youth, Operations Team  
> **Print This:** Keep at desk during launch  
> **Updated:** December 24, 2025

---

## 📱 ACCESSING LAUNCH CONTENT

### View All 50 Social Posts
```bash
cat content/launch-assets/LAUNCH_DAY_SOCIAL_PACK.md
```

### View Promo Templates
```bash
cat content/launch-assets/PROMO_TEMPLATES.md
```

### View Full Launch Runbook
```bash
cat content/launch-assets/LAUNCH_RUNBOOK.md
```

### Open in Editor
```bash
code content/launch-assets/  # Opens entire folder
```

---

## 🐍 PYTHON INTEGRATION

### Quick Stats
```bash
python launch_social_integration.py stats
```

### Get Posts by Category
```bash
python launch_social_integration.py category hero
python launch_social_integration.py category creator
python launch_social_integration.py category youth
python launch_social_integration.py category diaspora
```

### View Launch Day Schedule
```bash
python launch_social_integration.py launch
```

### Export to Spreadsheet
```bash
python launch_social_integration.py export launch_posts.csv
```

---

## 🌐 FLASK DASHBOARD INTEGRATION

### Add to flask_dashboard.py
```python
from launch_social_integration import LaunchSocialManager

manager = LaunchSocialManager()

@app.route('/api/launch-posts')
def get_launch_posts():
    return jsonify(manager.get_all_posts())

@app.route('/api/launch-posts/category/<category>')
def get_category_posts(category):
    return jsonify(manager.get_posts_by_category(category))

@app.route('/api/launch-posts/priority/<priority>')
def get_priority_posts(priority):
    return jsonify(manager.get_posts_by_priority(priority))
```

### View in Browser
```
http://localhost:5000/api/launch-posts
http://localhost:5000/api/launch-posts/category/hero
http://localhost:5000/api/launch-posts/priority/critical
```

---

## ⏰ LAUNCH DAY TIMELINE

### Hour-by-Hour (Eastern Time)

**8:00 AM** - Systems check  
```bash
python codex_unified_launcher.py status
curl http://localhost:5000/health
```

**10:00 AM** - Keynote premiere  
- YouTube live stream
- Cross-post to all platforms
- Deploy Hero Posts #1-5

**10:30 AM** - Marketplace opens  
- Test checkout flow
- Verify all creator products live

**11:00 AM** - Youth Challenge #1 begins  
- Deploy Youth Posts #16-25
- Monitor leaderboard

**12:00 PM** - Press release drops  
- Email to media list
- Post to LinkedIn, X

**1:00 PM** - Social storm  
- Deploy Hype Posts #46-50
- Creator wave begins

**6:00 PM** - Metrics review  
```bash
python codex_unified_launcher.py report
```

**8:00 PM** - Day 1 recap  
- Share success metrics
- Highlight top creators/youth
- Tease tomorrow

---

## 📊 MONITORING COMMANDS

### System Health
```bash
python codex_unified_launcher.py status
```

### Treasury Summary
```bash
python codex_unified_launcher.py treasury summary --days 1
```

### Social Engagement (if integrated)
```bash
python launch_social_integration.py stats
```

### Database Check
```bash
python -c "from db import SessionLocal; session = SessionLocal(); print('✅ DB Connected')"
```

### Redis Check
```bash
redis-cli ping  # Should return PONG
```

---

## 🎯 POST CATEGORIES AT A GLANCE

| Category | Posts | Priority | When to Use |
|----------|-------|----------|-------------|
| Hero | 1-5 | CRITICAL | Launch moment only |
| Creator | 6-15 | HIGH | Week 1, product launches |
| Youth | 16-25 | HIGH | Daily during challenges |
| Diaspora | 26-35 | MEDIUM | Ongoing, diaspora campaigns |
| Brand | 36-40 | MEDIUM | Storytelling, culture |
| Marketplace | 41-45 | HIGH | Product drops, new creators |
| Hype | 46-50 | CRITICAL | Launch day, major milestones |

---

## 🚨 EMERGENCY CONTACTS

**Technical Issues:**
- DevOps: Slack #launch-war-room
- Database: Check connection pooling

**Content Issues:**
- Social Media Lead: [email]
- Marketing Director: [email]

**Platform Issues:**
- Support: support@codexdominion.com
- Emergency: Check flask_dashboard.py logs

---

## ✅ PRE-LAUNCH CHECKLIST

**Technical:**
- [ ] Flask dashboard running (port 5000)
- [ ] Database connected (PostgreSQL or SQLite)
- [ ] Redis queue active (RQ worker running)
- [ ] All API endpoints tested
- [ ] Payment gateway verified

**Content:**
- [ ] All 50 posts reviewed
- [ ] Hashtags verified
- [ ] Links tested
- [ ] Images/videos prepared
- [ ] Creator content ready

**Team:**
- [ ] War room Slack active
- [ ] All roles assigned
- [ ] Backup plans reviewed
- [ ] Metrics dashboard live
- [ ] Support team briefed

---

## 🔧 TROUBLESHOOTING

### "Posts not loading"
```bash
# Check file exists
ls content/launch-assets/launch_social_posts.json

# Verify JSON format
python -c "import json; json.load(open('content/launch-assets/launch_social_posts.json'))"
```

### "Integration script fails"
```bash
# Check Python version (need 3.10+)
python --version

# Install dependencies if needed
pip install -r requirements.txt
```

### "Dashboard not showing launch content"
```bash
# Restart Flask
python flask_dashboard.py

# Clear JSON cache
python -c "from flask_dashboard import clear_json_cache; clear_json_cache()"
```

---

## 📞 SUPPORT CHANNELS

**Internal (Launch Day):**
- Primary: Slack #launch-war-room
- Secondary: Zoom war room (standing link)
- Escalation: Direct to Launch Director

**External:**
- Creators: creators@codexdominion.com
- Youth: youth@codexdominion.com
- General: support@codexdominion.com

---

## 🔥 LAUNCH DAY MANTRAS

✅ "We built our own system."  
✅ "This is culture as infrastructure."  
✅ "The Caribbean's digital economy begins today."  
✅ "Build the future. Own the system."

---

**🔥 The Flame Burns Sovereign and Eternal! 👑**

*Print this card and keep it handy during launch operations.*
