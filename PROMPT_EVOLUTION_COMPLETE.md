# 🧬 Prompt Evolution System - Complete Implementation

## 🎯 Overview

The **Prompt Evolution System** transforms prompts from static text into "living organisms" that evolve based on team usage patterns and implicit feedback. The system tracks prompt lineage, calculates effectiveness scores, and generates evolved variants to amplify what works.

## ✅ What Was Built

### 1. Database Schema (`flask_dashboard.py` lines 102-136)

#### **PromptHistory Model**
Tracks prompts independently as evolutionary organisms:

```python
class PromptHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt_text = db.Column(db.Text, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Lineage tracking
    parent_id = db.Column(db.Integer, db.ForeignKey('prompt_history.id'))
    generation = db.Column(db.Integer, default=1)
    evolution_reason = db.Column(db.String(100))
    
    # Context that shaped this prompt
    mood = db.Column(db.String(50))
    color_palette = db.Column(db.String(50))
    tags = db.Column(db.Text)
    category = db.Column(db.String(100))
    
    # Effectiveness metrics (calculated from usage)
    times_used = db.Column(db.Integer, default=0)
    times_saved = db.Column(db.Integer, default=0)
    times_reused = db.Column(db.Integer, default=0)
    avg_engagement = db.Column(db.Float, default=0.0)
    effectiveness_score = db.Column(db.Float, default=0.0)
    
    # Status flags
    is_template = db.Column(db.Boolean, default=False)
    is_evolved = db.Column(db.Boolean, default=False)
```

**Key Fields:**
- **Lineage:** `parent_id` (self-referential), `generation` (1, 2, 3...), `evolution_reason`
- **Metrics:** Calculated from implicit user behavior (saves, reuse, engagement time)
- **Context:** Mood, palette, tags, category that shaped the prompt

#### **GraphicsProject Extensions** (lines 52-75)
Extended with prompt evolution tracking:

```python
# Prompt Evolution - Lineage Tracking
parent_prompt_id = db.Column(db.Integer, db.ForeignKey('prompt_history.id'))
prompt_source = db.Column(db.String(50))  # 'user_written', 'ai_suggested', 'evolved', 'template'
was_prompt_reused = db.Column(db.Boolean, default=False)
engagement_score = db.Column(db.Float, default=0.0)

# Project-to-Project Evolution (remixing/forking)
original_prompt = db.Column(db.Text)  # Immutable base prompt
prompt_version = db.Column(db.Integer, default=1)  # Version number
parent_project_id = db.Column(db.Integer, db.ForeignKey("graphics_project.id"))
```

**Dual Lineage System:**
1. **PromptHistory → Project:** AI-suggested prompts
2. **Project → Project:** User remixes/forks

---

### 2. Core Functions (lines 4111-4260)

#### **evolve_prompt()**
Generates 3-5 evolved variants of a prompt:

```python
def evolve_prompt(original_prompt, project=None, reason="refinement", count=5):
    """Generate evolved variants - the prompt evolution engine.
    
    Evolution reasons:
    - refinement: Enhance specificity, add atmospheric depth
    - exploration: Dramatic perspective shifts, contrasting elements
    - remix: Blend themes, invert characteristics, add symbolic depth
    
    Returns: List of evolved prompt variants with metadata
    """
```

**Evolution Strategies:**
- **Refinement:** "Enhance specificity and detail", "Add atmospheric depth"
- **Exploration:** "Shift perspective dramatically", "Introduce contrasting elements"
- **Remix:** "Blend with complementary themes", "Invert dominant characteristics"

**Output Format:**
```python
{
    "prompt": "Evolved prompt text with atmosphere and detail layers",
    "strategy": "Enhance specificity and detail",
    "generation": 2,  # Incremented version
    "mood": "cinematic",
    "palette": "jewel tones",
    "lighting": "neon glow",
    "evolution_reason": "refinement"
}
```

#### **calculate_prompt_effectiveness()**
Scores prompts 0.0-100.0 based on usage patterns:

```python
def calculate_prompt_effectiveness(prompt_history):
    """Calculate effectiveness score from implicit feedback.
    
    Scoring factors:
    - times_used × 5 (max 30 points)
    - times_saved × 10 (max 30 points)
    - times_reused × 15 (max 25 points)
    - avg_engagement × 3 (max 15 points)
    
    Total: 100 points
    """
```

#### **get_team_strongest_prompts()**
Identifies top N prompts for team-level evolution:

```python
def get_team_strongest_prompts(team_id, limit=10):
    """Identify team's strongest prompts based on effectiveness scores.
    
    Returns: Top N prompts ordered by:
    1. effectiveness_score (primary)
    2. times_saved (secondary)
    3. times_reused (tertiary)
    """
```

---

### 3. Routes & Endpoints

#### **POST `/studio/graphics/project/<int:project_id>/evolve`**
Generate evolved prompt variants (the "Refine this prompt" action):

```python
@app.route("/studio/graphics/project/<int:project_id>/evolve", methods=["POST"])
def evolve_project_prompt(project_id):
    """
    Request body:
    {
        "reason": "refinement",  # or "exploration", "remix"
        "count": 5
    }
    
    Response:
    {
        "success": true,
        "original_prompt": "...",
        "variants": [
            {"prompt": "...", "generation": 2, "mood": "...", ...},
            ...
        ],
        "project_id": 123
    }
    """
```

#### **GET `/studio/graphics/prompt/<int:prompt_id>/lineage`**
Show evolutionary lineage tree (ancestors → current → descendants):

```python
@app.route("/studio/graphics/prompt/<int:prompt_id>/lineage")
def prompt_lineage(prompt_id):
    """
    Displays:
    - Ancestral prompts (walk up parent_id chain)
    - Current prompt with effectiveness metrics
    - Descendant prompts (children)
    - Projects using this prompt
    
    Template: prompt_lineage.html
    """
```

#### **GET `/studio/graphics/team/<int:team_id>/evolved-prompts`**
Team-level evolved prompts based on strongest collective work:

```python
@app.route("/studio/graphics/team/<int:team_id>/evolved-prompts")
def team_evolved_prompts(team_id):
    """
    1. Get top 10 strongest prompts
    2. Generate 3 evolved variants for top 3
    3. Display with effectiveness scores
    
    Template: team_evolved_prompts.html
    """
```

#### **POST `/studio/graphics/project/<int:project_id>/clone`**
Clone/remix a project (tracks prompt reuse):

```python
@app.route("/studio/graphics/project/<int:project_id>/clone", methods=["POST"])
def clone_graphics_project(project_id):
    """
    Creates:
    - New project with parent_project_id set
    - Incremented prompt_version
    - was_prompt_reused = True
    
    Updates:
    - times_reused on original prompt
    - effectiveness_score recalculated
    
    Logs: "cloned a project" activity
    """
```

---

### 4. Usage Signal Tracking

Enhanced existing routes to capture implicit feedback:

#### **save_graphics_project()** (lines 3971-4085)
```python
# Creates or updates PromptHistory entry
# Increments: times_used, times_saved
# Recalculates: effectiveness_score
# Logs: "saved a project" with usage_signal="saved"
```

#### **export_graphics_json()** (lines 4087-4122)
```python
# Updates: times_saved
# Recalculates: effectiveness_score
# Logs: "exported a project" with usage_signal="exported"
```

#### **edit_graphics_project()** (lines 5086-5142)
```python
# On GET (reopen): Increments times_used, avg_engagement
# Recalculates: effectiveness_score
# Logs: "reopened a project" with usage_signal="reopened"
```

#### **clone_graphics_project()** (lines 5146-5202)
```python
# Increments: times_reused
# Recalculates: effectiveness_score
# Logs: "cloned a project" with usage_signal="cloned"
```

---

### 5. Templates

#### **prompt_lineage.html** (363 lines)
Beautiful evolutionary tree visualization:

**Features:**
- **Ancestor nodes:** Blue gradient indicators (🔵)
- **Current node:** Pink gradient, highlighted (🟣)
- **Descendant nodes:** Cyan gradient (🔵)
- **Connecting lines:** Visual lineage flow
- **Metrics display:** times_used, times_saved, times_reused, effectiveness_score
- **Projects grid:** Shows all projects using this prompt

**Visual Design:**
```css
.node-indicator.ancestor { background: linear-gradient(135deg, #6a89cc, #4a69bd); }
.node-indicator.current { background: linear-gradient(135deg, #f093fb, #f5576c); }
.node-indicator.descendant { background: linear-gradient(135deg, #4facfe, #00f2fe); }
```

#### **team_evolved_prompts.html** (355 lines)
Team-level evolution dashboard:

**Sections:**
1. **Intro Banner:** Explains how system works
2. **Strongest Prompts Grid:** Top 10 with effectiveness bars
3. **Evolved Sets:** 3 sets of evolved variants (3 each = 9 total)

**Features:**
- **Rank badges:** #1, #2, #3 with gradient backgrounds
- **Effectiveness bars:** Animated progress bars
- **Variant cards:** Clickable with "Use This Prompt" button
- **Pre-fill studio:** Redirects to graphics studio with prompt loaded

---

### 6. Migration Script

**migrate_prompt_evolution.py** (94 lines)

Run to update existing database:

```bash
python migrate_prompt_evolution.py
```

**What it does:**
1. Creates `prompt_history` table if missing
2. Adds 7 new columns to `graphics_project` table
3. Validates schema
4. Prints confirmation

**Safe to run multiple times** - checks for existing tables/columns first.

---

## 🚀 How to Use

### 1. Run Migration
```bash
python migrate_prompt_evolution.py
```

Expected output:
```
🔄 Running Prompt Evolution Migration...
📋 Current tables: ['user', 'team', 'team_member', 'graphics_project', 'team_activity']
✅ Creating PromptHistory table...
   ✅ PromptHistory table created!
✅ Adding new columns to GraphicsProject table...
   ✅ Added column: parent_prompt_id
   ✅ Added column: prompt_source
   ... (7 columns total)
🎉 Migration complete!
```

### 2. Restart Flask
```powershell
# Stop current Flask app
# Restart:
python flask_dashboard.py
```

### 3. Create Projects
- Save projects to team library
- System automatically creates PromptHistory entries
- Tracks usage signals (saved, exported, reopened, cloned)

### 4. View Evolution

**A. Individual Project Evolution:**
1. Go to project library: `/studio/graphics/team/<team_id>`
2. Open a project: Click "Edit" → `/studio/graphics/project/<id>/edit`
3. Click "Refine this prompt" (needs UI button added)
4. Select evolved variant

**B. View Prompt Lineage:**
- Navigate to: `/studio/graphics/prompt/<prompt_id>/lineage`
- See: Ancestors → Current → Descendants tree
- Track: Version history, effectiveness metrics

**C. Team-Level Evolution:**
- Navigate to: `/studio/graphics/team/<team_id>/evolved-prompts`
- See: Top 10 strongest prompts
- Get: 9 evolved variants (3 sets × 3 variants)
- Use: Click "Use This Prompt" → auto-fills studio

---

## 📊 Effectiveness Scoring

### Implicit Feedback Signals

**1. Saved (30 points max)**
- User clicks "Save Project"
- Indicates: Prompt produced worthwhile result
- Weight: 10 points per save

**2. Used (30 points max)**
- Prompt selected/reopened
- Indicates: Returning to this prompt
- Weight: 5 points per use

**3. Reused (25 points max)**
- Project cloned/remixed
- Indicates: High-value prompt worth iterating
- Weight: 15 points per reuse

**4. Engagement (15 points max)**
- Time spent editing/refining
- Indicates: Deep creative investment
- Weight: 3 points per engagement unit

**Total: 100 points**

### Score Interpretation
- **0-25:** Experimental/untested
- **26-50:** Moderately effective
- **51-75:** Strong performer
- **76-100:** Elite prompt (team's best)

---

## 🎨 Evolution Strategies

### Refinement
**Goal:** Polish and enhance existing prompt

**Techniques:**
- "Enhance specificity and detail"
- "Add atmospheric depth"
- "Introduce subtle complexity"
- "Refine emotional tone"
- "Sharpen visual focus"

**Example:**
```
Original: "A futuristic cityscape at night"
Refined: "A futuristic cityscape at night, bathed in ethereal mist, 
          intricate patterns woven throughout, layered transparencies 
          revealing depth"
```

### Exploration
**Goal:** Dramatic creative shifts

**Techniques:**
- "Shift perspective dramatically"
- "Introduce contrasting elements"
- "Explore alternate moods"
- "Transform scale and proportion"
- "Reimagine through different medium"

**Example:**
```
Original: "A serene forest scene with soft lighting"
Explored: "A serene forest scene — viewed from an impossible angle, 
           charged with electric energy, neon palette, backlit"
```

### Remix
**Goal:** Blend and invert for creative tension

**Techniques:**
- "Blend with complementary themes"
- "Invert dominant characteristics"
- "Layer in symbolic depth"
- "Fuse with fresh palette"
- "Add narrative complexity"

**Example:**
```
Original: "A minimalist portrait in monochrome"
Remixed: "A minimalist portrait — mysterious shadows meeting playful energy, 
          jewel tones palette, geometric precision meets natural chaos, 
          hidden symbolic objects"
```

---

## 🧬 Lineage System

### Two-Tier Architecture

#### **Tier 1: PromptHistory → GraphicsProject**
AI-suggested prompts and their usage:

```
PromptHistory(id=1, generation=1)
    ↓
GraphicsProject(id=5, parent_prompt_id=1)
GraphicsProject(id=8, parent_prompt_id=1)
    ↓
times_used += 2
```

#### **Tier 2: GraphicsProject → GraphicsProject**
User remixes and forks:

```
GraphicsProject(id=5, prompt_version=1)
    ↓ [clone]
GraphicsProject(id=12, parent_project_id=5, prompt_version=2)
    ↓ [clone]
GraphicsProject(id=18, parent_project_id=12, prompt_version=3)
```

### Lineage Queries

**Find all descendants:**
```python
descendants = PromptHistory.query.filter_by(parent_id=prompt_id).all()
```

**Find all ancestors:**
```python
ancestors = []
current = prompt
while current.parent_id:
    parent = PromptHistory.query.get(current.parent_id)
    ancestors.insert(0, parent)
    current = parent
```

**Find project remixes:**
```python
remixes = GraphicsProject.query.filter_by(parent_project_id=project_id).all()
```

---

## 🔗 Navigation Integration

### Add Links to Team Library (team_library.html)

After "AI Prompts" button:
```html
<a href="/studio/graphics/team/{{ team.id }}/evolved-prompts" class="nav-button">
    🧬 Evolved Prompts
</a>
```

### Add "Refine" Button to Project Edit Page (edit_project.html)

In project details section:
```html
<button onclick="evolvePrompt({{ project.id }})" class="evolve-button">
    ✨ Refine this prompt
</button>

<script>
async function evolvePrompt(projectId) {
    const response = await fetch(`/studio/graphics/project/${projectId}/evolve`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({reason: 'refinement', count: 5})
    });
    
    const data = await response.json();
    
    // Display variants in modal or below
    displayVariants(data.variants);
}
</script>
```

### Add Lineage Link (where prompts are displayed)

```html
<a href="/studio/graphics/prompt/{{ project.parent_prompt_id }}/lineage">
    View Lineage 🌳
</a>
```

---

## 📈 Usage Analytics

### Track Evolution Engagement

**Activity types added:**
- `"evolved a prompt"` - User clicked "Refine this prompt"
- `"viewed evolved prompts"` - Team-level evolution page viewed
- `"saved a project"` - Now includes `usage_signal="saved"`
- `"exported a project"` - Now includes `usage_signal="exported"`
- `"reopened a project"` - New signal when editing
- `"cloned a project"` - New signal when remixing

### Query Examples

**Most evolved prompts:**
```python
most_evolved = PromptHistory.query.filter(
    PromptHistory.generation > 1
).order_by(PromptHistory.generation.desc()).all()
```

**Most reused prompts:**
```python
most_reused = PromptHistory.query.order_by(
    PromptHistory.times_reused.desc()
).limit(10).all()
```

**Team evolution activity:**
```python
evolution_activity = TeamActivity.query.filter(
    TeamActivity.team_id == team_id,
    TeamActivity.action.in_(['evolved a prompt', 'cloned a project'])
).all()
```

---

## 🎯 Philosophy

### Prompts as Living Organisms

**Core Principle:**
> "Prompts stop being static text and start behaving like growing organisms — they evolve, adapt, and carry lineage."

**Implicit vs Explicit Feedback:**
- ❌ Don't ask users to rate prompts (1-5 stars)
- ✅ Infer value from behavior (saves, reuse, time spent)

**Evolution, Not Replacement:**
- Original prompts preserved in `original_prompt` field
- Lineage tracked through `parent_id` chains
- Versions numbered: v1 → v2 → v3

**Team DNA:**
- Strongest prompts reflect collective taste
- Evolution amplifies what already works
- Fresh directions introduced gradually

---

## 🐛 Troubleshooting

### Migration Fails
```bash
# Error: "Database locked"
# Solution: Stop Flask app first, then run migration
```

### Effectiveness Score Always 0
```bash
# Cause: No usage signals captured yet
# Solution: Save, export, or reopen projects to generate signals
```

### Lineage Tree Empty
```bash
# Cause: Projects created before migration
# Solution: New projects will automatically populate PromptHistory
```

### "Use This Prompt" Button Doesn't Work
```bash
# Cause: graphics_studio.html needs sessionStorage integration
# Solution: Add preset detection in graphics studio route
```

---

## 🔮 Future Enhancements

### Phase 2 (Next Steps)
1. **Variant selection modal** in edit_project.html
2. **Preset detection** in graphics_studio route
3. **Lineage visualization** with interactive D3.js tree
4. **Prompt templates** (mark high-scoring prompts as templates)
5. **Cross-team learning** (anonymized prompt sharing)

### Phase 3 (Advanced)
1. **Semantic clustering** - group similar prompts
2. **Style transfer** - apply Team A's style to Team B's prompts
3. **Prompt compression** - distill long prompts into shorter versions
4. **Auto-evolution** - system generates variants nightly for top prompts
5. **A/B testing** - compare evolved vs original prompt performance

---

## 📚 Files Modified

### Python Backend
1. **flask_dashboard.py**
   - Lines 102-136: PromptHistory model
   - Lines 52-75: GraphicsProject extensions
   - Lines 4111-4260: Evolution functions (evolve_prompt, calculate_effectiveness, get_strongest)
   - Lines 4556-4655: Evolution routes (/evolve, /lineage, /evolved-prompts, /clone)
   - Lines 3971-4122: Enhanced save/export with signal tracking
   - Lines 5086-5202: Enhanced edit/clone routes

### Templates
1. **prompt_lineage.html** (NEW) - 363 lines
2. **team_evolved_prompts.html** (NEW) - 355 lines

### Migration
1. **migrate_prompt_evolution.py** (NEW) - 94 lines

---

## ✅ Testing Checklist

### Basic Functionality
- [ ] Migration runs successfully
- [ ] PromptHistory entries created on save
- [ ] Effectiveness scores calculated correctly
- [ ] Lineage tree displays ancestors/descendants
- [ ] Evolved variants generated with proper formatting

### Usage Signal Tracking
- [ ] Save increments times_saved
- [ ] Export increments times_saved
- [ ] Reopen increments times_used
- [ ] Clone increments times_reused
- [ ] Effectiveness score updates after each signal

### UI/UX
- [ ] Lineage tree renders beautifully
- [ ] Effectiveness bars animate smoothly
- [ ] Variant cards display all metadata
- [ ] "Use This Prompt" button works
- [ ] Activity feed shows evolution events

### Edge Cases
- [ ] Handle prompts with no lineage (root prompts)
- [ ] Handle projects with no parent_prompt_id
- [ ] Handle teams with < 10 projects (empty state)
- [ ] Handle concurrent updates to effectiveness_score

---

## 🎉 Success Metrics

### Adoption
- **Target:** 50% of team projects use evolved prompts within 30 days
- **Measure:** `prompt_source = 'evolved'` count

### Engagement
- **Target:** Average 2 prompt evolutions per active user per week
- **Measure:** `TeamActivity.action = 'evolved a prompt'` count

### Effectiveness
- **Target:** Evolved prompts score 20% higher than originals
- **Measure:** Compare `effectiveness_score` for `is_evolved=True` vs `False`

### Retention
- **Target:** Prompts reused 3+ times become templates
- **Measure:** `times_reused >= 3` promoted to `is_template=True`

---

**🔥 The prompt evolution system is now live!** 🧬

Your prompts are no longer static text—they're living, breathing organisms that grow stronger with every creative cycle. The Dominion is becoming a living chronicle.

