"""
Display the Cultural Memory Architecture
The soul of the Dominion
"""

from db import SessionLocal
from models import (
    IdentityCodex, StylePattern, CulturalMemory,
    CreativeProject, BrandEvolution
)
from sqlalchemy import func


def show_cultural_memory():
    """Display complete CMA status"""
    session = SessionLocal()
    
    try:
        print("\n" + "=" * 70)
        print("🔥 CULTURAL MEMORY ARCHITECTURE - COMPLETE STATUS")
        print("=" * 70)
        
        # LAYER 2: Identity Codex
        print("\n📜 LAYER 2: IDENTITY CODEX (Cultural DNA)")
        print("-" * 70)
        
        principles = session.query(IdentityCodex).filter_by(is_active="active").all()
        
        # Group by category
        categories = {}
        for principle in principles:
            if principle.category not in categories:
                categories[principle.category] = []
            categories[principle.category].append(principle)
        
        for category, items in sorted(categories.items()):
            print(f"\n🎭 {category.upper()}")
            for item in sorted(items, key=lambda x: x.priority, reverse=True):
                print(f"   • {item.principle} (Priority: {item.priority}/10)")
                print(f"     {item.description[:80]}...")
        
        print(f"\n✓ Total Principles: {len(principles)}")
        
        # LAYER 1: Style Patterns
        print("\n\n🎨 LAYER 1: STYLE PATTERNS (What Works)")
        print("-" * 70)
        
        patterns = session.query(StylePattern).all()
        
        # Group by type
        pattern_types = {}
        for pattern in patterns:
            if pattern.pattern_type not in pattern_types:
                pattern_types[pattern.pattern_type] = []
            pattern_types[pattern.pattern_type].append(pattern)
        
        for ptype, items in sorted(pattern_types.items()):
            print(f"\n🔹 {ptype.upper()} PATTERNS")
            for item in sorted(items, key=lambda x: x.success_rate, reverse=True):
                print(f"   • {item.pattern_name}")
                print(f"     Success: {item.success_rate:.0%} | Used: {item.times_used} times")
                print(f"     When: {item.when_to_use[:60]}...")
        
        print(f"\n✓ Total Patterns: {len(patterns)}")
        
        # LAYER 1: Historical Projects
        print("\n\n📂 LAYER 1: CREATIVE LINEAGE (Historical Projects)")
        print("-" * 70)
        
        projects = session.query(CreativeProject).all()
        
        for project in projects:
            status = "✅" if project.would_repeat == "yes" else "🔄" if project.would_repeat == "with_modifications" else "❌"
            print(f"\n{status} {project.name}")
            print(f"   Type: {project.project_type} | Audience: {project.target_audience}")
            print(f"   Tone: {project.emotional_tone} | Completed: {project.completed_at.strftime('%Y-%m-%d') if project.completed_at else 'In Progress'}")
            
            if project.success_metrics:
                metrics = ", ".join([f"{k}: {v}" for k, v in project.success_metrics.items()])
                print(f"   Metrics: {metrics}")
            
            if project.lessons_learned:
                print(f"   Lesson: {project.lessons_learned[:70]}...")
        
        print(f"\n✓ Total Projects: {len(projects)}")
        
        # LAYER 3: Cultural Memories
        print("\n\n💡 LAYER 3: CULTURAL MEMORIES (Wisdom)")
        print("-" * 70)
        
        memories = session.query(CulturalMemory).all()
        
        # Group by type
        memory_types = {}
        for memory in memories:
            if memory.memory_type not in memory_types:
                memory_types[memory.memory_type] = []
            memory_types[memory.memory_type].append(memory)
        
        for mtype, items in sorted(memory_types.items()):
            print(f"\n🧠 {mtype.upper()}")
            for item in sorted(items, key=lambda x: x.times_referenced, reverse=True):
                print(f"   • {item.title}")
                print(f"     {item.content[:80]}...")
                print(f"     Referenced: {item.times_referenced} times | Relevance: {item.relevance_score:.0%}")
        
        print(f"\n✓ Total Memories: {len(memories)}")
        
        # Summary Statistics
        print("\n\n" + "=" * 70)
        print("📊 CULTURAL MEMORY ARCHITECTURE SUMMARY")
        print("=" * 70)
        
        print(f"\n🏛️ IDENTITY:")
        print(f"   • {len(principles)} core principles across {len(categories)} categories")
        print(f"   • Average priority: {sum(p.priority for p in principles) / len(principles):.1f}/10")
        
        print(f"\n🎨 PATTERNS:")
        print(f"   • {len(patterns)} proven patterns")
        avg_success = sum(p.success_rate for p in patterns) / len(patterns) if patterns else 0
        print(f"   • Average success rate: {avg_success:.0%}")
        total_uses = sum(p.times_used for p in patterns)
        print(f"   • Total uses: {total_uses}")
        
        print(f"\n📂 HISTORY:")
        print(f"   • {len(projects)} projects archived")
        repeat_worthy = sum(1 for p in projects if p.would_repeat == "yes")
        print(f"   • Repeat-worthy: {repeat_worthy}/{len(projects)}")
        
        print(f"\n💡 WISDOM:")
        print(f"   • {len(memories)} cultural memories")
        total_refs = sum(m.times_referenced for m in memories)
        print(f"   • Total references: {total_refs}")
        avg_relevance = sum(m.relevance_score for m in memories) / len(memories) if memories else 0
        print(f"   • Average relevance: {avg_relevance:.0%}")
        
        print("\n" + "=" * 70)
        print("🔥 The Dominion has a soul.")
        print("👑 The civilization remembers, learns, and evolves.")
        print("=" * 70 + "\n")
        
    finally:
        session.close()


if __name__ == "__main__":
    show_cultural_memory()
