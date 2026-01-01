# Cultural Memory Architecture - Quick Reference Guide

## 🚀 Quick Start

### Initialize CMA (First Time Only)
```bash
# Create database tables
python create_cma_tables.py

# Initialize with sample data
python cultural_memory_protocol.py
```

### View Complete Status
```bash
python show_cultural_memory.py
```

### Run Query Engine Demo
```bash
python cultural_memory_query.py
```

### See Council Integration Example
```bash
python example_council_cma_decision.py
```

---

## 💻 Using the CulturalMemoryEngine

### Basic Import
```python
from cultural_memory_query import CulturalMemoryEngine

with CulturalMemoryEngine() as engine:
    # Your queries here
    pass
```

### Common Queries

#### 1. Check Identity Alignment
```python
validation = engine.validate_against_identity(
    proposal="Amazing Bible stories with vibrant illustrations!",
    category="tone"  # or "aesthetic", "narrative", "ethics", "values"
)

print(f"Alignment: {validation['alignment_score']:.0%}")
print(f"Recommendation: {validation['recommendation']}")
# Returns: alignment_score, aligned_principles, conflicting_principles, recommendation
```

#### 2. Find Identity Principles
```python
# All principles in a category
principles = engine.query_identity(category="tone")

# Principles for specific audience
principles = engine.query_identity(applies_to="kids_content")

# Both filters
principles = engine.query_identity(
    category="aesthetic",
    applies_to="families"
)
```

#### 3. Find Proven Patterns
```python
# By type and audience
patterns = engine.find_patterns(
    pattern_type="visual",
    audience="kids_3_8",
    min_success_rate=0.85
)

# Best performing patterns
patterns = engine.find_patterns(min_success_rate=0.90)

# All narrative patterns
patterns = engine.find_patterns(pattern_type="narrative")
```

#### 4. Recall Cultural Memories
```python
# By tags
memories = engine.recall_memories(tags=["kids", "seasonal"])

# By type
memories = engine.recall_memories(memory_type="lesson")

# High relevance only
memories = engine.recall_memories(min_relevance=0.8)
```

#### 5. Find Similar Projects
```python
# By type
projects = engine.find_similar_projects(project_type="coloring_book")

# By type and audience
projects = engine.find_similar_projects(
    project_type="printable_cards",
    target_audience="families"
)
```

#### 6. Get Complete Decision Context
```python
# Returns all relevant data for a decision
context = engine.get_decision_context(
    decision_type="visual",  # or "narrative", "style", "tone", "brand"
    project_type="coloring_book"
)

# Context includes:
# - identity_principles
# - proven_patterns
# - relevant_memories
# - similar_projects
```

---

## 📊 Working with Models Directly

### Add New Identity Principle
```python
from db import SessionLocal
from models import IdentityCodex
from datetime import datetime

session = SessionLocal()

principle = IdentityCodex(
    id="custom_principle_id",
    category="tone",  # tone, values, aesthetic, narrative, ethics
    principle="Your Principle Name",
    description="Detailed explanation",
    examples=["Example 1", "Example 2"],
    anti_examples=["What not to do"],
    priority=8,  # 1-10
    applies_to=["kids", "families"],
    created_by="sovereign_architect",
    is_active="active"
)

session.add(principle)
session.commit()
session.close()
```

### Record New Style Pattern
```python
from models import StylePattern

pattern = StylePattern(
    id="pattern_unique_id",
    pattern_name="Your Pattern Name",
    pattern_type="visual",  # visual, narrative, audio, structural
    description="What makes this pattern work",
    elements=["element1", "element2"],
    when_to_use="When to apply this pattern",
    audience_fit=["kids_3_8", "families"],
    times_used=0,
    success_rate=0.0,
    avg_engagement=None
)

session.add(pattern)
session.commit()
```

### Archive Completed Project
```python
from models import CreativeProject
from datetime import datetime

project = CreativeProject(
    id="project_unique_id",
    name="Project Name",
    project_type="video",  # video, ebook, bundle, coloring_book, etc.
    completed_at=datetime.utcnow(),
    target_audience="kids_3_8",
    styles_used=["watercolor", "bold_typography"],
    narrative_structure="hero_journey",
    emotional_tone="joyful",
    brand_elements=["warm_colors", "playful_fonts"],
    success_metrics={"views": 1000, "rating": 4.5},
    audience_response="Very positive feedback",
    lessons_learned="Key lessons from this project",
    would_repeat="yes"  # yes, no, with_modifications
)

session.add(project)
session.commit()
```

### Add Cultural Memory
```python
from models import CulturalMemory

memory = CulturalMemory(
    id="memory_unique_id",
    memory_type="lesson",  # lesson, pattern, milestone, rule, insight
    title="Memory Title",
    content="Detailed wisdom content",
    tags=["tag1", "tag2", "tag3"],
    context={"applies_to": ["context1"], "learned_from": "source"},
    times_referenced=0,
    relevance_score=1.0
)

session.add(memory)
session.commit()
```

---

## 🎯 Common Use Cases

### Use Case 1: Validate New Content Idea
```python
with CulturalMemoryEngine() as engine:
    # Check if idea aligns with identity
    validation = engine.validate_against_identity(
        proposal="Your content proposal text",
        category="tone"
    )
    
    if validation['recommendation'] == 'approve':
        print("✅ Aligned with Dominion identity")
    else:
        print("⚠️ Review needed")
        print(f"Conflicts: {validation['conflicting_principles']}")
```

### Use Case 2: Find Best Pattern for Audience
```python
with CulturalMemoryEngine() as engine:
    patterns = engine.find_patterns(
        audience="kids_3_8",
        min_success_rate=0.85
    )
    
    # Sort by success rate
    best_pattern = patterns[0]
    print(f"Use: {best_pattern['pattern_name']}")
    print(f"Success: {best_pattern['success_rate']:.0%}")
```

### Use Case 3: Learn from Past Projects
```python
with CulturalMemoryEngine() as engine:
    similar = engine.find_similar_projects(
        project_type="coloring_book",
        target_audience="kids_3_8"
    )
    
    for project in similar:
        print(f"Project: {project['name']}")
        print(f"Lesson: {project['lessons_learned']}")
        print(f"Repeat: {project['would_repeat']}")
```

### Use Case 4: Apply Seasonal Wisdom
```python
with CulturalMemoryEngine() as engine:
    # Planning Christmas content in October
    memories = engine.recall_memories(tags=["seasonal", "christmas"])
    
    for memory in memories:
        print(f"💡 {memory['title']}")
        print(f"   {memory['content']}")
```

### Use Case 5: Complete Decision Context
```python
with CulturalMemoryEngine() as engine:
    # Get everything relevant for a visual design decision
    context = engine.get_decision_context(
        decision_type="visual",
        project_type="coloring_book"
    )
    
    print(f"Principles: {len(context['identity_principles'])}")
    print(f"Patterns: {len(context['proven_patterns'])}")
    print(f"Memories: {len(context['relevant_memories'])}")
    print(f"Projects: {len(context['similar_projects'])}")
```

---

## 🔍 Query Return Structures

### Identity Principle
```python
{
    "principle": "Joyful Wonder",
    "category": "tone",
    "description": "Content should spark curiosity...",
    "examples": ["Example 1", "Example 2"],
    "anti_examples": ["Anti 1", "Anti 2"],
    "priority": 10
}
```

### Style Pattern
```python
{
    "pattern_name": "Watercolor Warmth",
    "type": "visual",
    "description": "Soft watercolor illustrations...",
    "when_to_use": "Children's Bible stories...",
    "success_rate": 0.89,
    "times_used": 12,
    "elements": ["element1", "element2"]
}
```

### Cultural Memory
```python
{
    "title": "Seasonal Content Must Launch 6-8 Weeks Early",
    "type": "lesson",
    "content": "Christmas content needs to be ready...",
    "tags": ["seasonal", "timing", "christmas"],
    "context": {"applies_to": ["seasonal_products"]},
    "times_referenced": 5
}
```

### Historical Project
```python
{
    "name": "Christmas Bible Story Coloring Book",
    "completed": "2024-11-15",
    "styles_used": ["watercolor", "bold_typography"],
    "emotional_tone": "joyful",
    "success_metrics": {"downloads": 1240, "rating": 4.8},
    "lessons_learned": "Watercolor style resonated...",
    "would_repeat": "yes"
}
```

### Validation Result
```python
{
    "alignment_score": 0.75,  # 0-1
    "aligned_principles": ["Joyful Wonder", "Honest Marketing"],
    "conflicting_principles": [],
    "recommendation": "approve"  # approve or review
}
```

---

## 📈 Tracking & Analytics

### Update Pattern Usage
```python
from db import SessionLocal
from models import StylePattern

session = SessionLocal()
pattern = session.query(StylePattern).filter_by(id="pattern_id").first()

pattern.times_used += 1
# Update success_rate based on outcome
# Update avg_engagement if applicable

session.commit()
session.close()
```

### Track Memory References
Memory references are automatically incremented when using `recall_memories()`.

### Record Brand Evolution
```python
from models import BrandEvolution

evolution = BrandEvolution(
    id="evolution_unique_id",
    evolution_type="refinement",  # refinement, expansion, pivot, consolidation
    what_changed="What aspect of the brand changed",
    why_changed="Rationale for the change",
    previous_state={"key": "old_value"},
    new_state={"key": "new_value"},
    affected_principles=["principle_id_1"],
    affected_patterns=["pattern_id_1"],
    transition_period="3_months",
    architect_approval="approved"
)

session.add(evolution)
session.commit()
```

---

## 🎓 Integration Patterns

### Council Decision Integration
```python
with CulturalMemoryEngine() as engine:
    # Get comprehensive context
    context = engine.get_decision_context(
        decision_type="visual",
        project_type="coloring_book"
    )
    
    # Council reviews principles
    for principle in context['identity_principles']:
        # Present to council for consideration
        pass
    
    # Council selects pattern
    best_pattern = context['proven_patterns'][0]
    
    # Council recalls relevant lessons
    for memory in context['relevant_memories']:
        # Apply institutional wisdom
        pass
```

### Agent Onboarding Integration
```python
def train_new_agent(agent_id: str):
    """Train new agent on Dominion culture"""
    
    with CulturalMemoryEngine() as engine:
        # Study all identity principles
        principles = engine.query_identity()
        
        # Learn proven patterns
        patterns = engine.find_patterns()
        
        # Review historical projects
        projects = engine.find_similar_projects("all")
        
        # Absorb cultural memories
        memories = engine.recall_memories()
        
        # Agent now understands Dominion culture
        return {
            "principles_learned": len(principles),
            "patterns_learned": len(patterns),
            "projects_studied": len(projects),
            "memories_absorbed": len(memories)
        }
```

---

## 🔧 Maintenance Tasks

### Regular Updates
- Update pattern success rates after each project
- Add new memories from completed projects
- Review and update principle priority scores
- Archive completed projects with lessons learned

### Quality Checks
- Ensure all memories have relevant tags
- Verify pattern success rates are current
- Check that principles apply to correct audiences
- Validate historical project data is complete

### Optimization
- Decay relevance scores for old, unused memories
- Identify patterns that consistently fail
- Update examples/anti-examples based on real cases
- Consolidate duplicate or overlapping principles

---

## 📞 Support & Resources

**Core Files:**
- `cultural_memory_query.py` - Query engine
- `show_cultural_memory.py` - Status display
- `example_council_cma_decision.py` - Integration example

**Documentation:**
- `CULTURAL_MEMORY_COMPLETE.md` - Complete implementation guide
- `CMA_QUICK_REFERENCE.md` - This file

**Database Models:**
- CreativeProject, CreativeDecision, IdentityCodex
- StylePattern, CulturalMemory, BrandEvolution

---

👑 **The Dominion Remembers. The Dominion Learns. The Dominion Evolves.** 🔥
