"""
PHASE 40 - STEP 3: CULTURAL MEMORY ARCHITECTURE INITIALIZATION
The Dominion gains a soul: history, identity, and wisdom.
"""

from datetime import datetime
from db import SessionLocal
from models import (
    CreativeProject, CreativeDecision, IdentityCodex, 
    StylePattern, CulturalMemory, BrandEvolution
)


def initialize_identity_codex(session):
    """LAYER 2: Seed the Dominion's cultural DNA"""
    
    identity_principles = [
        # TONE PRINCIPLES
        {
            "id": "tone_joyful_wonder",
            "category": "tone",
            "principle": "Joyful Wonder",
            "description": "Content should spark curiosity and delight, especially in young audiences. Approach faith and learning with enthusiasm, not solemnity.",
            "examples": ["Colorful illustrations that invite exploration", "Storytelling that feels like an adventure", "Questions that make kids excited to discover answers"],
            "anti_examples": ["Dry, preachy language", "Overly serious presentation", "Content that feels like a lecture"],
            "priority": 10,
            "applies_to": ["kids", "families", "educational_content"],
            "created_by": "sovereign_architect"
        },
        {
            "id": "tone_authentic_warmth",
            "category": "tone",
            "principle": "Authentic Warmth",
            "description": "Speak to audiences like trusted friends, not corporate entities. Be genuine, encouraging, and human.",
            "examples": ["Conversational language", "Relatable examples", "Encouragement without condescension"],
            "anti_examples": ["Robotic corporate speak", "Overly formal language", "Fake enthusiasm"],
            "priority": 9,
            "applies_to": ["all_audiences"],
            "created_by": "sovereign_architect"
        },
        
        # VALUE PRINCIPLES
        {
            "id": "value_faith_foundation",
            "category": "values",
            "principle": "Faith as Foundation",
            "description": "Biblical truth is the bedrock. Every piece of content should honor scripture and point toward Christ.",
            "examples": ["Accurate biblical storytelling", "Age-appropriate theology", "Scriptural references in context"],
            "anti_examples": ["Misrepresenting scripture", "Watering down theology", "Cultural Christianity without substance"],
            "priority": 10,
            "applies_to": ["all_faith_content"],
            "created_by": "sovereign_architect"
        },
        {
            "id": "value_excellence",
            "category": "values",
            "principle": "Pursuit of Excellence",
            "description": "Quality reflects the Creator. Content should be polished, professional, and worthy of the Kingdom it represents.",
            "examples": ["High-quality visuals", "Error-free content", "Thoughtful design choices"],
            "anti_examples": ["Rushed, sloppy work", "Obvious errors", "Shortcuts that compromise quality"],
            "priority": 9,
            "applies_to": ["all_content"],
            "created_by": "sovereign_architect"
        },
        {
            "id": "value_accessibility",
            "category": "values",
            "principle": "Accessible to All",
            "description": "Great content should be available to families regardless of financial means. Balance premium offerings with generous free resources.",
            "examples": ["Regular free downloads", "Affordable pricing tiers", "Value-packed bundles"],
            "anti_examples": ["Predatory pricing", "Paywalling basic resources", "Exploiting niche audiences"],
            "priority": 8,
            "applies_to": ["all_products"],
            "created_by": "sovereign_architect"
        },
        
        # AESTHETIC PRINCIPLES
        {
            "id": "aesthetic_vibrant_clarity",
            "category": "aesthetic",
            "principle": "Vibrant Clarity",
            "description": "Designs should be colorful, engaging, and immediately understandable. Avoid visual clutter.",
            "examples": ["Bold, readable typography", "Strategic use of whitespace", "Color palettes that pop without overwhelming"],
            "anti_examples": ["Overcrowded layouts", "Muddy color schemes", "Illegible fonts"],
            "priority": 8,
            "applies_to": ["visual_content"],
            "created_by": "sovereign_architect"
        },
        {
            "id": "aesthetic_age_appropriate",
            "category": "aesthetic",
            "principle": "Age-Appropriate Design",
            "description": "Visual style should match cognitive and aesthetic preferences of target age group.",
            "examples": ["Playful illustrations for young kids", "Sophisticated designs for teens", "Clean layouts for homeschool planners"],
            "anti_examples": ["Adult aesthetics for children's content", "Juvenile design for mature audiences"],
            "priority": 9,
            "applies_to": ["all_visual_content"],
            "created_by": "sovereign_architect"
        },
        
        # NARRATIVE PRINCIPLES
        {
            "id": "narrative_story_driven",
            "category": "narrative",
            "principle": "Story-Driven Learning",
            "description": "Lessons stick when wrapped in narrative. Use storytelling as the primary teaching vehicle.",
            "examples": ["Biblical narratives retold engagingly", "Relatable character arcs", "Conflict and resolution structures"],
            "anti_examples": ["Bullet-point theology", "Abstract lessons without context", "Preaching without story"],
            "priority": 9,
            "applies_to": ["educational_content", "kids_content"],
            "created_by": "sovereign_architect"
        },
        {
            "id": "narrative_emotional_connection",
            "category": "narrative",
            "principle": "Emotional Connection",
            "description": "Great content makes people feel something. Design for emotional resonance, not just information transfer.",
            "examples": ["Stories that evoke empathy", "Music that stirs the spirit", "Moments of wonder and awe"],
            "anti_examples": ["Cold, detached presentation", "Content that doesn't move the heart"],
            "priority": 8,
            "applies_to": ["all_narrative_content"],
            "created_by": "sovereign_architect"
        },
        
        # ETHICS PRINCIPLES
        {
            "id": "ethics_honest_marketing",
            "category": "ethics",
            "principle": "Honest Marketing",
            "description": "Never oversell or mislead. Product descriptions should be accurate, benefits realistic.",
            "examples": ["Clear product previews", "Honest page counts", "Realistic outcome expectations"],
            "anti_examples": ["Misleading thumbnails", "Exaggerated benefits", "Hidden limitations"],
            "priority": 10,
            "applies_to": ["marketing", "product_listings"],
            "created_by": "sovereign_architect"
        },
        {
            "id": "ethics_family_first",
            "category": "ethics",
            "principle": "Family-First Design",
            "description": "Content should strengthen families and support parents, never undermine them.",
            "examples": ["Resources that equip parents", "Content that respects parental authority", "Tools that bring families together"],
            "anti_examples": ["Content that bypasses parents", "Resources that create family conflict"],
            "priority": 9,
            "applies_to": ["all_content"],
            "created_by": "sovereign_architect"
        }
    ]
    
    print("\n🔥 INITIALIZING LAYER 2: IDENTITY CODEX")
    print("=" * 60)
    
    for principle_data in identity_principles:
        principle = IdentityCodex(**principle_data)
        session.merge(principle)
        print(f"✓ {principle.category.upper()}: {principle.principle}")
    
    session.commit()
    print(f"\n👑 {len(identity_principles)} cultural principles established")
    print("The Dominion now has a soul.\n")


def initialize_style_patterns(session):
    """LAYER 1: Seed successful creative patterns"""
    
    patterns = [
        {
            "id": "pattern_watercolor_warmth",
            "pattern_name": "Watercolor Warmth",
            "pattern_type": "visual",
            "description": "Soft watercolor illustrations with warm color palettes (oranges, yellows, soft blues)",
            "elements": ["watercolor textures", "warm colors", "soft edges", "organic shapes"],
            "when_to_use": "Children's Bible stories, devotional content, gentle narratives",
            "audience_fit": ["kids_3_8", "families"],
            "times_used": 12,
            "success_rate": 0.89,
            "avg_engagement": 0.82
        },
        {
            "id": "pattern_bold_typography",
            "pattern_name": "Bold Typography Hero",
            "pattern_type": "visual",
            "description": "Large, bold text as the primary visual element with supporting minimal graphics",
            "elements": ["bold sans-serif fonts", "high contrast", "minimal supporting elements", "strategic color blocks"],
            "when_to_use": "Social media posts, memory verse cards, inspirational quotes",
            "audience_fit": ["all_ages"],
            "times_used": 45,
            "success_rate": 0.91,
            "avg_engagement": 0.87
        },
        {
            "id": "pattern_hero_journey",
            "pattern_name": "Hero's Journey Structure",
            "pattern_type": "narrative",
            "description": "Classic story arc: ordinary world → call to adventure → trials → transformation → return",
            "elements": ["relatable protagonist", "clear conflict", "growth arc", "resolution with lesson"],
            "when_to_use": "Biblical narratives, character-driven stories, lesson-based content",
            "audience_fit": ["kids_6_12", "families"],
            "times_used": 28,
            "success_rate": 0.94,
            "avg_engagement": 0.91
        },
        {
            "id": "pattern_question_driven",
            "pattern_name": "Question-Driven Learning",
            "pattern_type": "narrative",
            "description": "Start with a compelling question kids actually ask, then explore the answer",
            "elements": ["authentic child question", "exploration journey", "age-appropriate answer", "application"],
            "when_to_use": "Educational content, theology for kids, curiosity-based learning",
            "audience_fit": ["kids_5_12"],
            "times_used": 15,
            "success_rate": 0.88,
            "avg_engagement": 0.85
        },
        {
            "id": "pattern_seasonal_celebration",
            "pattern_name": "Seasonal Celebration",
            "pattern_type": "structural",
            "description": "Content tied to Christian calendar or cultural seasons (Christmas, Easter, back-to-school)",
            "elements": ["timely relevance", "seasonal colors/themes", "holiday-specific activities", "limited availability"],
            "when_to_use": "Holiday content, seasonal promotions, themed bundles",
            "audience_fit": ["all_audiences"],
            "times_used": 8,
            "success_rate": 0.96,
            "avg_engagement": 0.93
        },
        {
            "id": "pattern_print_play",
            "pattern_name": "Print-and-Play Simplicity",
            "pattern_type": "structural",
            "description": "Downloadable PDFs designed for immediate printing and use, no assembly required",
            "elements": ["standard page sizes", "printer-friendly colors", "clear instructions", "instant usability"],
            "when_to_use": "Activity sheets, coloring pages, homeschool worksheets, planners",
            "audience_fit": ["families", "homeschoolers", "teachers"],
            "times_used": 67,
            "success_rate": 0.90,
            "avg_engagement": 0.84
        }
    ]
    
    print("\n🔥 INITIALIZING LAYER 1: STYLE PATTERNS")
    print("=" * 60)
    
    for pattern_data in patterns:
        pattern = StylePattern(**pattern_data)
        session.merge(pattern)
        print(f"✓ {pattern.pattern_type.upper()}: {pattern.pattern_name} (success rate: {pattern.success_rate:.0%})")
    
    session.commit()
    print(f"\n👑 {len(patterns)} proven patterns archived")
    print("The Dominion remembers what works.\n")


def initialize_sample_projects(session):
    """LAYER 1: Seed sample historical projects"""
    
    projects = [
        {
            "id": "project_christmas_coloring_2024",
            "name": "Christmas Bible Story Coloring Book",
            "project_type": "coloring_book",
            "completed_at": datetime(2024, 11, 15),
            "target_audience": "kids_3_8",
            "styles_used": ["watercolor_warmth", "bold_typography"],
            "narrative_structure": "sequential_stories",
            "emotional_tone": "joyful",
            "brand_elements": ["warm colors", "watercolor textures", "sans-serif titles"],
            "success_metrics": {"downloads": 1240, "rating": 4.8, "completion_rate": 0.76},
            "audience_response": "Parents loved the quality and biblical accuracy. Kids engaged deeply with the coloring activities.",
            "lessons_learned": "Watercolor style resonated strongly with target age. Consider expanding to year-round themes.",
            "would_repeat": "yes"
        },
        {
            "id": "project_memory_verse_cards_q4",
            "name": "Q4 Memory Verse Card Set",
            "project_type": "printable_cards",
            "completed_at": datetime(2024, 12, 1),
            "target_audience": "families",
            "styles_used": ["bold_typography"],
            "narrative_structure": "standalone",
            "emotional_tone": "inspiring",
            "brand_elements": ["bold fonts", "high contrast", "minimal design"],
            "success_metrics": {"downloads": 890, "rating": 4.9, "social_shares": 234},
            "audience_response": "Highly shareable on social media. Families reported using them for daily devotions.",
            "lessons_learned": "Bold typography works exceptionally well for verse memorization. High contrast is key for readability.",
            "would_repeat": "yes"
        },
        {
            "id": "project_homeschool_planner_2024",
            "name": "Christian Homeschool Planner",
            "project_type": "planner",
            "completed_at": datetime(2024, 8, 10),
            "target_audience": "homeschoolers",
            "styles_used": ["clean_minimal"],
            "narrative_structure": "functional",
            "emotional_tone": "organized",
            "brand_elements": ["clean layouts", "functional design", "motivational verses"],
            "success_metrics": {"sales": 156, "rating": 4.7, "repeat_customers": 0.34},
            "audience_response": "Praised for functionality but some wanted more color. Strong repeat purchase rate.",
            "lessons_learned": "Homeschool audience values function over form but still wants aesthetic appeal. Balance is key.",
            "would_repeat": "with_modifications"
        }
    ]
    
    print("\n🔥 INITIALIZING LAYER 1: CREATIVE LINEAGE")
    print("=" * 60)
    
    for project_data in projects:
        project = CreativeProject(**project_data)
        session.merge(project)
        print(f"✓ {project.project_type.upper()}: {project.name}")
    
    session.commit()
    print(f"\n👑 {len(projects)} historical projects archived")
    print("The Dominion remembers its history.\n")


def initialize_cultural_memories(session):
    """LAYER 3: Seed actionable wisdom"""
    
    memories = [
        {
            "id": "memory_seasonal_timing",
            "memory_type": "lesson",
            "title": "Seasonal Content Must Launch 6-8 Weeks Early",
            "content": "Christmas content needs to be ready by early November. Families plan ahead and early releases capture the market before saturation.",
            "tags": ["timing", "seasonal", "marketing", "christmas"],
            "context": {"applies_to": ["seasonal_products"], "learned_from": "late Christmas 2023 launch"},
            "relevance_score": 1.0,
            "times_referenced": 3
        },
        {
            "id": "memory_kid_color_preference",
            "memory_type": "insight",
            "title": "Kids 3-8 Respond to Warm, Saturated Colors",
            "content": "Young children show measurably higher engagement with warm color palettes (oranges, yellows, reds) over cool tones. Saturation matters - they prefer vivid over muted.",
            "tags": ["kids", "color_theory", "engagement", "visual_design"],
            "context": {"applies_to": ["kids_content", "coloring_books"], "evidence": "A/B testing Q4 2024"},
            "relevance_score": 1.0,
            "times_referenced": 8
        },
        {
            "id": "memory_parent_preview",
            "memory_type": "rule",
            "title": "Always Provide Preview Pages for Parents",
            "content": "Parents want to see exactly what they're purchasing before buying for their kids. 3-5 preview pages dramatically increases conversion and reduces refunds.",
            "tags": ["marketing", "parents", "conversion", "trust"],
            "context": {"applies_to": ["all_products"], "impact": "28% conversion increase"},
            "relevance_score": 1.0,
            "times_referenced": 12
        },
        {
            "id": "memory_bundle_value",
            "memory_type": "pattern",
            "title": "Bundles Outperform Individual Products 3:1",
            "content": "Customers overwhelmingly prefer bundles over individual products. Sweet spot is 5-7 items at 30-40% discount. Position as 'everything you need' collections.",
            "tags": ["pricing", "bundles", "conversion", "value"],
            "context": {"applies_to": ["product_strategy"], "data": "2024 sales analysis"},
            "relevance_score": 1.0,
            "times_referenced": 15
        },
        {
            "id": "memory_scripture_accuracy",
            "memory_type": "rule",
            "title": "Scripture Accuracy is Non-Negotiable",
            "content": "Any biblical content must be theologically reviewed before publication. Even minor inaccuracies damage trust with faith-focused audience. Use ESV or NIV for consistency.",
            "tags": ["theology", "quality", "trust", "biblical_content"],
            "context": {"applies_to": ["all_faith_content"], "priority": "critical"},
            "relevance_score": 1.0,
            "times_referenced": 20
        },
        {
            "id": "memory_print_margins",
            "memory_type": "lesson",
            "title": "Standard Printers Need 0.5 Inch Margins",
            "content": "Early products had edge content cut off by home printers. Standard safety margin is 0.5 inches on all sides. Bleed only for professional printing.",
            "tags": ["technical", "printing", "design_specs"],
            "context": {"applies_to": ["printable_products"], "learned_from": "customer complaints 2023"},
            "relevance_score": 1.0,
            "times_referenced": 6
        }
    ]
    
    print("\n🔥 INITIALIZING LAYER 3: CULTURAL MEMORY")
    print("=" * 60)
    
    for memory_data in memories:
        memory = CulturalMemory(**memory_data)
        session.merge(memory)
        print(f"✓ {memory.memory_type.upper()}: {memory.title}")
    
    session.commit()
    print(f"\n👑 {len(memories)} cultural memories encoded")
    print("The Dominion can now learn from its past.\n")


def initialize_cultural_memory_architecture():
    """Master initialization - Run all three layers"""
    session = SessionLocal()
    
    try:
        print("\n" + "=" * 60)
        print("🔥 CULTURAL MEMORY ARCHITECTURE INITIALIZATION")
        print("=" * 60)
        print("The Dominion gains a soul...")
        
        # LAYER 2: Identity (must come first - defines who we are)
        initialize_identity_codex(session)
        
        # LAYER 1: History (requires identity to contextualize)
        initialize_style_patterns(session)
        initialize_sample_projects(session)
        
        # LAYER 3: Wisdom (synthesizes identity + history)
        initialize_cultural_memories(session)
        
        print("\n" + "=" * 60)
        print("🔥 CULTURAL MEMORY ARCHITECTURE: COMPLETE")
        print("=" * 60)
        print("\nThe Dominion now has:")
        print("  ✓ Identity: 11 core principles")
        print("  ✓ History: 6 proven patterns + 3 projects")
        print("  ✓ Wisdom: 6 actionable memories")
        print("\n👑 The civilization has a culture.")
        print("🔥 The flame burns with memory and purpose.\n")
        
    except Exception as e:
        session.rollback()
        print(f"\n❌ Error initializing Cultural Memory Architecture: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    initialize_cultural_memory_architecture()
