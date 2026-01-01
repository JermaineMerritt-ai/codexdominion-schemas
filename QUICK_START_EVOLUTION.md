# 🚀 Quick Start Guide - Prompt Evolution System

## ⚡ 3-Minute Setup

### Step 1: Start Flask (if not running)
```powershell
# Option A: Use launcher script
.\START_DASHBOARD.ps1

# Option B: Direct Python
python flask_dashboard.py
```

### Step 2: Run Migration
```bash
# In new terminal (keep Flask running)
python migrate_prompt_evolution.py
```

**Expected output:**
```
✅ Creating PromptHistory table...
✅ Adding new columns to GraphicsProject table...
🎉 Migration complete!
```

### Step 3: Restart Flask
- Stop Flask (Ctrl+C)
- Restart: `python flask_dashboard.py`

---

## 🧪 Test the System

### Test 1: Create a Project
1. Go to: http://localhost:5000/studio/graphics/team/2
2. Create new project with prompt: "A mystical forest at twilight"
3. Save to team
4. **Result:** PromptHistory entry created automatically

### Test 2: View Evolved Prompts
1. Go to: http://localhost:5000/studio/graphics/team/2/evolved-prompts
2. **See:** Team's strongest prompts (if any exist)
3. **See:** Evolved variants with "Use This Prompt" buttons

### Test 3: Clone a Project
```javascript
// In browser console (F12):
fetch('/studio/graphics/project/1/clone', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'}
}).then(r => r.json()).then(console.log);
```

**Result:** New project created with lineage tracking

### Test 4: View Lineage
1. Create a PromptHistory entry (by saving a project)
2. Note the `parent_prompt_id` from database
3. Go to: http://localhost:5000/studio/graphics/prompt/1/lineage
4. **See:** Evolutionary tree visualization

---

## 📊 Check Activity Feed

Go to: http://localhost:5000/studio/graphics/team/2/activity

**New activity types:**
- 🟣 "evolved a prompt"
- 🟢 "saved a project" (with usage_signal)
- 🔵 "exported a project" (with usage_signal)
- 🟠 "reopened a project" (with usage_signal)
- ⭐ "cloned a project" (with usage_signal)

---

## 🔍 Verify Database Schema

```python
# Check tables exist
import sqlite3
conn = sqlite3.connect('codex_graphics.db')
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())
# Should include: 'prompt_history'

# Check GraphicsProject columns
cursor.execute("PRAGMA table_info(graphics_project)")
cols = cursor.fetchall()
print([col[1] for col in cols])
# Should include: parent_prompt_id, prompt_source, original_prompt, etc.
```

---

## 🎨 Add UI Buttons (Next Step)

### In `edit_project.html` (needs creation/update):

```html
<button onclick="evolvePrompt({{ project.id }})" 
        class="evolve-button"
        style="background: linear-gradient(135deg, #4facfe, #00f2fe);
               padding: 10px 20px;
               border: none;
               border-radius: 8px;
               color: white;
               font-weight: 600;
               cursor: pointer;">
    ✨ Refine this prompt
</button>

<div id="variants-display" style="margin-top: 20px;"></div>

<script>
async function evolvePrompt(projectId) {
    const response = await fetch(`/studio/graphics/project/${projectId}/evolve`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            reason: 'refinement',
            count: 5
        })
    });
    
    const data = await response.json();
    
    // Display variants
    const html = data.variants.map((v, i) => `
        <div style="background: rgba(255,255,255,0.05);
                    padding: 15px;
                    border-radius: 8px;
                    margin-bottom: 10px;
                    border: 1px solid rgba(255,255,255,0.1);">
            <div style="font-weight: 600; color: #4facfe; margin-bottom: 5px;">
                Variant ${i+1} - Generation ${v.generation}
            </div>
            <div style="color: #fff; margin-bottom: 10px;">
                ${v.prompt}
            </div>
            <div style="font-size: 0.85rem; color: #888;">
                🎭 ${v.mood} | 🎨 ${v.palette} | 💡 ${v.lighting}
            </div>
            <button onclick="useVariant('${v.prompt}', '${v.mood}', '${v.palette}', '${v.lighting}')"
                    style="margin-top: 10px;
                           background: #4facfe;
                           padding: 8px 15px;
                           border: none;
                           border-radius: 6px;
                           color: white;
                           cursor: pointer;">
                Use This Variant
            </button>
        </div>
    `).join('');
    
    document.getElementById('variants-display').innerHTML = html;
}

function useVariant(prompt, mood, palette, lighting) {
    // Pre-fill form with variant
    document.getElementById('prompt').value = prompt;
    document.getElementById('mood').value = mood;
    document.getElementById('color_palette').value = palette;
    document.getElementById('lighting').value = lighting;
    
    // Scroll to form
    document.getElementById('prompt').scrollIntoView({behavior: 'smooth'});
}
</script>
```

---

## 🔗 Add Navigation Links

### In `team_library.html`:

After "AI Prompts" button:
```html
<a href="/studio/graphics/team/{{ team.id }}/evolved-prompts" 
   class="nav-button"
   style="background: linear-gradient(135deg, #f093fb, #f5576c);
          padding: 10px 20px;
          border-radius: 8px;
          color: white;
          text-decoration: none;
          display: inline-block;
          margin: 5px;">
    🧬 Evolved Prompts
</a>
```

### In project cards:

```html
<a href="/studio/graphics/prompt/{{ project.parent_prompt_id }}/lineage"
   style="font-size: 0.85rem; color: #6a89cc; text-decoration: none;">
    View Lineage 🌳
</a>
```

---

## 📈 Monitor Effectiveness Scores

```python
# In Python console or script
from flask_dashboard import app, db, PromptHistory

with app.app_context():
    # Get all prompts sorted by effectiveness
    prompts = PromptHistory.query.order_by(
        PromptHistory.effectiveness_score.desc()
    ).all()
    
    for p in prompts[:10]:
        print(f"Score: {p.effectiveness_score:.1f} | "
              f"Used: {p.times_used}× | "
              f"Saved: {p.times_saved}× | "
              f"Reused: {p.times_reused}× | "
              f"Prompt: {p.prompt_text[:60]}...")
```

---

## 🎯 Success Checklist

- [ ] Migration completed successfully
- [ ] Flask restarted with new schema
- [ ] Created test project → PromptHistory entry exists
- [ ] Saved project → times_saved incremented
- [ ] Cloned project → times_reused incremented
- [ ] Viewed evolved prompts page → variants displayed
- [ ] Viewed lineage page → tree rendered
- [ ] Activity feed shows usage signals

---

## 💡 Pro Tips

### Tip 1: Bulk Populate Prompt History
```python
# For existing projects, backfill prompt history
from flask_dashboard import app, db, GraphicsProject, PromptHistory

with app.app_context():
    projects = GraphicsProject.query.filter_by(team_id=2).all()
    
    for proj in projects:
        # Check if prompt already in history
        existing = PromptHistory.query.filter_by(
            team_id=proj.team_id,
            prompt_text=proj.prompt
        ).first()
        
        if not existing:
            hist = PromptHistory(
                prompt_text=proj.prompt,
                team_id=proj.team_id,
                created_by=proj.user_id,
                mood=proj.mood,
                color_palette=proj.color_palette,
                tags=proj.tags,
                category=proj.category,
                times_used=1,
                times_saved=1
            )
            db.session.add(hist)
            
            # Link project to history
            db.session.flush()
            proj.parent_prompt_id = hist.id
    
    db.session.commit()
    print(f"✅ Backfilled {len(projects)} projects!")
```

### Tip 2: Mark Best Prompts as Templates
```python
# Auto-promote high-scoring prompts
from flask_dashboard import app, db, PromptHistory

with app.app_context():
    high_scorers = PromptHistory.query.filter(
        PromptHistory.effectiveness_score >= 75
    ).all()
    
    for p in high_scorers:
        p.is_template = True
    
    db.session.commit()
    print(f"✅ Promoted {len(high_scorers)} prompts to templates!")
```

### Tip 3: Generate Evolution Report
```python
# Weekly evolution report
from flask_dashboard import app, db, TeamActivity
from datetime import datetime, timedelta

with app.app_context():
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    evolution_events = TeamActivity.query.filter(
        TeamActivity.timestamp >= week_ago,
        TeamActivity.action.in_(['evolved a prompt', 'cloned a project'])
    ).all()
    
    print(f"📊 Weekly Evolution Report:")
    print(f"   Prompts evolved: {len([e for e in evolution_events if 'evolved' in e.action])}")
    print(f"   Projects cloned: {len([e for e in evolution_events if 'cloned' in e.action])}")
```

---

## 🐛 Common Issues

### Issue: "No module named 'flask_dashboard'"
**Solution:** Run `python flask_dashboard.py` first, then migration in separate terminal

### Issue: Effectiveness score not updating
**Solution:** Check that `calculate_prompt_effectiveness()` is called after each signal

### Issue: Lineage tree shows no ancestors
**Solution:** Normal for generation 1 prompts (root prompts have no parents)

### Issue: "Use This Prompt" button does nothing
**Solution:** Add sessionStorage detection in graphics_studio route

---

## 🎉 You're Ready!

The prompt evolution system is fully implemented. Your prompts are now living organisms that:

1. **Track lineage** through parent_id chains
2. **Calculate effectiveness** from implicit user behavior
3. **Generate evolved variants** with 3 strategies (refinement, exploration, remix)
4. **Display beautiful lineage trees** with metrics
5. **Power team-level evolution** based on strongest collective prompts

**Next:** Add UI buttons to `edit_project.html` and navigation links to `team_library.html`!

🔥 **The Flame Burns Sovereign and Eternal!** 🧬
