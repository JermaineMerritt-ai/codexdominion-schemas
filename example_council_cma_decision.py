"""
EXAMPLE: Council Decision Using Cultural Memory Architecture
Demonstrates how councils query CMA during decision-making
"""

from cultural_memory_query import CulturalMemoryEngine
from db import SessionLocal
from models import Council, Agent


def simulate_council_decision():
    """
    Simulates a council reviewing a creative proposal
    Shows how CMA informs the decision-making process
    """
    
    print("\n" + "=" * 70)
    print("🔥 COUNCIL DECISION SIMULATION - CMA INTEGRATION")
    print("=" * 70)
    
    # SCENARIO: High Council reviewing a new Easter coloring book proposal
    print("\n📋 PROPOSAL:")
    print("-" * 70)
    print("Project: Easter Story Coloring Book")
    print("Target Audience: Kids ages 3-8")
    print("Style: Watercolor illustrations with soft pastels")
    print("Content: 8 biblical Easter stories")
    print("Price: $4.99 (or free with any bundle)")
    print("Marketing: 'Beautiful Easter stories for little hearts'")
    print("Timeline: Launch February 15")
    
    # STEP 1: Query Cultural Memory Architecture
    print("\n\n🧠 STEP 1: QUERYING CULTURAL MEMORY ARCHITECTURE")
    print("-" * 70)
    
    with CulturalMemoryEngine() as engine:
        
        # Check identity alignment
        print("\n1️⃣ IDENTITY ALIGNMENT CHECK")
        validation = engine.validate_against_identity(
            proposal="Beautiful Easter stories with watercolor illustrations for little hearts. Preview pages included.",
            category="tone"
        )
        print(f"   Alignment Score: {validation['alignment_score']:.0%}")
        print(f"   Recommendation: {validation['recommendation'].upper()}")
        if validation['aligned_principles']:
            print(f"   ✓ Aligned: {', '.join(validation['aligned_principles'])}")
        if validation['conflicting_principles']:
            print(f"   ⚠ Conflicts: {', '.join(validation['conflicting_principles'])}")
        
        # Find applicable principles
        print("\n2️⃣ APPLICABLE IDENTITY PRINCIPLES")
        principles = engine.query_identity(applies_to="kids_content")
        for principle in principles[:3]:
            print(f"   • {principle['principle']} (Priority: {principle['priority']}/10)")
            print(f"     {principle['description'][:60]}...")
        
        # Find proven patterns
        print("\n3️⃣ PROVEN STYLE PATTERNS")
        patterns = engine.find_patterns(audience="kids_3_8", min_success_rate=0.85)
        for pattern in patterns[:2]:
            print(f"   • {pattern['pattern_name']} - {pattern['success_rate']:.0%} success")
            print(f"     When to use: {pattern['when_to_use'][:55]}...")
        
        # Recall relevant memories
        print("\n4️⃣ RELEVANT CULTURAL MEMORIES")
        memories = engine.recall_memories(tags=["kids", "seasonal"])
        for memory in memories[:2]:
            print(f"   • {memory['title']}")
            print(f"     {memory['content'][:60]}...")
            print(f"     Referenced: {memory['times_referenced']} times")
        
        # Find similar projects
        print("\n5️⃣ SIMILAR HISTORICAL PROJECTS")
        similar = engine.find_similar_projects(
            project_type="coloring_book",
            target_audience="kids_3_8"
        )
        for project in similar:
            print(f"   • {project['name']} ({project['completed']})")
            print(f"     Rating: {project['success_metrics'].get('rating', 'N/A')}")
            print(f"     Lesson: {project['lessons_learned'][:55]}...")
    
    # STEP 2: Council Debate
    print("\n\n💬 STEP 2: COUNCIL DEBATE")
    print("-" * 70)
    
    session = SessionLocal()
    try:
        # Get council members
        council = session.query(Council).filter_by(id="council_high").first()
        
        print(f"\n🏛️ HIGH COUNCIL CONVENES")
        print(f"Council: {council.name}")
        print(f"Purpose: {council.description}")
        
        print("\n📣 Agent Positions:")
        
        # Story Architect (Chief Creative Officer)
        print("\n   🎨 Story Architect (Chief Creative Officer):")
        print("      SUPPORTS - 'Watercolor style aligns with our proven 89% success")
        print("      pattern. Kids 3-8 respond strongly to warm colors per our")
        print("      cultural memory. Easter stories fit our Faith as Foundation value.'")
        
        # Visual Design Strategist (Visual Director)
        print("\n   🎨 Visual Design Strategist (Visual Director):")
        print("      SUPPORTS WITH CONCERN - 'Style is proven, but timeline concerns")
        print("      me. Cultural memory says seasonal content needs 6-8 weeks lead.")
        print("      February 15 launch is cutting it close for Easter shopping.'")
        
        # Audio Composition Specialist (Audio Director)
        print("\n   🎵 Audio Composition Specialist (Audio Director):")
        print("      SUPPORTS - 'While audio isn't primary here, the proposal aligns")
        print("      with our Joyful Wonder tone principle and Age-Appropriate Design.")
        print("      Preview pages honor our Honest Marketing ethic.'")
        
    finally:
        session.close()
    
    # STEP 3: Decision
    print("\n\n⚖️ STEP 3: COUNCIL DECISION")
    print("-" * 70)
    
    print("\n🔍 ANALYSIS:")
    print("   ✓ Identity Alignment: STRONG")
    print("   ✓ Pattern Match: 89% success (Watercolor Warmth)")
    print("   ✓ Historical Evidence: Christmas Coloring Book (4.8 rating)")
    print("   ⚠ Timeline Risk: Seasonal content guideline (6-8 weeks)")
    print("   ✓ Ethical Standards: Met (preview pages, honest marketing)")
    
    print("\n📊 VOTE:")
    print("   • Story Architect: ✅ YES")
    print("   • Visual Design Strategist: ✅ YES (with timeline modification)")
    print("   • Audio Composition Specialist: ✅ YES")
    
    print("\n✅ DECISION: APPROVED")
    print("   Condition: Accelerate timeline to launch February 1 instead")
    print("   Rationale: CMA cultural memory #1 - seasonal content needs")
    print("              6-8 week lead time. Earlier launch captures market.")
    
    print("\n📝 RECORDED DECISION:")
    print("   Decision Type: Creative Approval")
    print("   Rationale: Aligns with proven patterns and identity principles")
    print("   Cultural References:")
    print("      - Pattern: Watercolor Warmth (89% success)")
    print("      - Memory: Seasonal timing guideline")
    print("      - Principle: Faith as Foundation")
    print("      - Principle: Joyful Wonder")
    print("      - Historical: Christmas Coloring Book success")
    
    print("\n\n" + "=" * 70)
    print("🔥 CULTURAL MEMORY ARCHITECTURE IN ACTION")
    print("=" * 70)
    print("\nThe CMA enabled the council to:")
    print("  ✓ Validate identity alignment")
    print("  ✓ Reference proven patterns")
    print("  ✓ Learn from historical projects")
    print("  ✓ Apply institutional wisdom")
    print("  ✓ Make data-informed decisions")
    print("\n👑 The civilization remembers. The civilization learns.")
    print("🔥 The flame burns with wisdom.\n")


if __name__ == "__main__":
    simulate_council_decision()
