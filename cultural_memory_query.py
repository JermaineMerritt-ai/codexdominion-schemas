"""
LAYER 3: Memory-to-Action Engine
Query the Cultural Memory Architecture for decision-making
"""

from typing import List, Dict, Any, Optional
from sqlalchemy import desc, or_, and_
from db import SessionLocal
from models import (
    IdentityCodex, StylePattern, CulturalMemory, 
    CreativeProject, CreativeDecision
)


class CulturalMemoryEngine:
    """Query and apply cultural memory to decisions"""
    
    def __init__(self):
        self.session = SessionLocal()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
    
    def query_identity(self, category: Optional[str] = None, 
                       applies_to: Optional[str] = None) -> List[Dict[str, Any]]:
        """Query the Identity Codex - What are our core principles?"""
        query = self.session.query(IdentityCodex).filter_by(is_active="active")
        
        if category:
            query = query.filter(IdentityCodex.category == category)
        
        results = query.order_by(desc(IdentityCodex.priority)).all()
        
        # Filter by applies_to if specified
        if applies_to:
            results = [r for r in results if applies_to in r.applies_to]
        
        return [{
            "principle": r.principle,
            "category": r.category,
            "description": r.description,
            "examples": r.examples,
            "anti_examples": r.anti_examples,
            "priority": r.priority
        } for r in results]
    
    def find_patterns(self, pattern_type: Optional[str] = None,
                     audience: Optional[str] = None,
                     min_success_rate: float = 0.7) -> List[Dict[str, Any]]:
        """Find proven creative patterns - What has worked before?"""
        query = self.session.query(StylePattern).filter(
            StylePattern.success_rate >= min_success_rate
        )
        
        if pattern_type:
            query = query.filter(StylePattern.pattern_type == pattern_type)
        
        results = query.order_by(desc(StylePattern.success_rate)).all()
        
        # Filter by audience if specified
        if audience:
            results = [r for r in results if audience in r.audience_fit]
        
        return [{
            "pattern_name": r.pattern_name,
            "type": r.pattern_type,
            "description": r.description,
            "when_to_use": r.when_to_use,
            "success_rate": r.success_rate,
            "times_used": r.times_used,
            "elements": r.elements
        } for r in results]
    
    def recall_memories(self, tags: Optional[List[str]] = None,
                       memory_type: Optional[str] = None,
                       min_relevance: float = 0.5) -> List[Dict[str, Any]]:
        """Recall cultural memories - What have we learned?"""
        query = self.session.query(CulturalMemory).filter(
            CulturalMemory.relevance_score >= min_relevance
        )
        
        if memory_type:
            query = query.filter(CulturalMemory.memory_type == memory_type)
        
        results = query.order_by(desc(CulturalMemory.relevance_score)).all()
        
        # Filter by tags if specified
        if tags:
            results = [r for r in results if any(tag in r.tags for tag in tags)]
        
        # Update reference tracking
        for memory in results:
            memory.times_referenced += 1
        
        self.session.commit()
        
        return [{
            "title": r.title,
            "type": r.memory_type,
            "content": r.content,
            "tags": r.tags,
            "context": r.context,
            "times_referenced": r.times_referenced
        } for r in results]
    
    def find_similar_projects(self, project_type: str,
                              target_audience: Optional[str] = None) -> List[Dict[str, Any]]:
        """Find historical projects similar to current need"""
        query = self.session.query(CreativeProject).filter(
            CreativeProject.project_type == project_type
        )
        
        if target_audience:
            query = query.filter(CreativeProject.target_audience == target_audience)
        
        results = query.order_by(desc(CreativeProject.completed_at)).all()
        
        return [{
            "name": r.name,
            "completed": r.completed_at.strftime("%Y-%m-%d") if r.completed_at else None,
            "styles_used": r.styles_used,
            "emotional_tone": r.emotional_tone,
            "success_metrics": r.success_metrics,
            "lessons_learned": r.lessons_learned,
            "would_repeat": r.would_repeat
        } for r in results]
    
    def get_decision_context(self, decision_type: str,
                            project_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Comprehensive context for a decision
        Combines identity, patterns, memories, and history
        """
        context = {
            "identity_principles": [],
            "proven_patterns": [],
            "relevant_memories": [],
            "similar_projects": []
        }
        
        # What do our principles say?
        if decision_type in ["style", "visual", "aesthetic"]:
            context["identity_principles"] = self.query_identity(category="aesthetic")
        elif decision_type in ["narrative", "story", "content"]:
            context["identity_principles"] = self.query_identity(category="narrative")
        elif decision_type in ["tone", "voice"]:
            context["identity_principles"] = self.query_identity(category="tone")
        elif decision_type in ["brand", "marketing"]:
            context["identity_principles"] = self.query_identity(category="ethics")
        
        # What patterns have worked?
        pattern_type_map = {
            "visual": "visual",
            "style": "visual",
            "narrative": "narrative",
            "story": "narrative"
        }
        if decision_type in pattern_type_map:
            context["proven_patterns"] = self.find_patterns(
                pattern_type=pattern_type_map[decision_type]
            )
        
        # What have we learned?
        memory_tags = decision_type.split("_")
        context["relevant_memories"] = self.recall_memories(tags=memory_tags)
        
        # What similar projects exist?
        if project_type:
            context["similar_projects"] = self.find_similar_projects(project_type)
        
        return context
    
    def validate_against_identity(self, proposal: str,
                                  category: Optional[str] = None) -> Dict[str, Any]:
        """
        Check if a proposal aligns with Dominion identity
        Returns alignment score and conflicting principles
        """
        principles = self.query_identity(category=category)
        
        # Simple keyword matching (can be enhanced with ML)
        proposal_lower = proposal.lower()
        
        aligned = []
        conflicts = []
        
        for principle in principles:
            # Check examples
            example_match = any(
                ex.lower() in proposal_lower 
                for ex in principle.get("examples", [])
            )
            
            # Check anti-examples
            anti_match = any(
                anti.lower() in proposal_lower 
                for anti in principle.get("anti_examples", [])
            )
            
            if example_match:
                aligned.append(principle["principle"])
            if anti_match:
                conflicts.append(principle["principle"])
        
        alignment_score = len(aligned) / max(len(principles), 1)
        
        return {
            "alignment_score": alignment_score,
            "aligned_principles": aligned,
            "conflicting_principles": conflicts,
            "recommendation": "approve" if alignment_score > 0.5 and not conflicts else "review"
        }


def demonstrate_memory_engine():
    """Show the Memory-to-Action Engine in action"""
    
    print("\n" + "=" * 60)
    print("🔥 CULTURAL MEMORY ENGINE - DEMONSTRATION")
    print("=" * 60)
    
    with CulturalMemoryEngine() as engine:
        # Example 1: Designing kids content
        print("\n📋 SCENARIO 1: Designing a new children's Bible story book")
        print("-" * 60)
        
        context = engine.get_decision_context(
            decision_type="visual",
            project_type="coloring_book"
        )
        
        print(f"\n✓ Found {len(context['identity_principles'])} aesthetic principles")
        print(f"✓ Found {len(context['proven_patterns'])} successful patterns")
        print(f"✓ Found {len(context['relevant_memories'])} relevant memories")
        print(f"✓ Found {len(context['similar_projects'])} similar projects")
        
        if context['proven_patterns']:
            top_pattern = context['proven_patterns'][0]
            print(f"\n🎨 Recommended Pattern: {top_pattern['pattern_name']}")
            print(f"   Success Rate: {top_pattern['success_rate']:.0%}")
            print(f"   When to use: {top_pattern['when_to_use']}")
        
        # Example 2: Validating a marketing proposal
        print("\n\n📋 SCENARIO 2: Validating marketing copy")
        print("-" * 60)
        
        proposal = "Amazing Bible stories with vibrant, colorful illustrations that make learning fun! Preview pages included."
        validation = engine.validate_against_identity(proposal, category="ethics")
        
        print(f"\nProposal: \"{proposal}\"")
        print(f"\n✓ Alignment Score: {validation['alignment_score']:.0%}")
        print(f"✓ Recommendation: {validation['recommendation'].upper()}")
        
        if validation['aligned_principles']:
            print(f"✓ Aligned with: {', '.join(validation['aligned_principles'])}")
        
        if validation['conflicting_principles']:
            print(f"⚠ Conflicts with: {', '.join(validation['conflicting_principles'])}")
        
        # Example 3: Learning from history
        print("\n\n📋 SCENARIO 3: Planning Christmas content")
        print("-" * 60)
        
        memories = engine.recall_memories(tags=["christmas", "seasonal"])
        
        for memory in memories:
            print(f"\n💡 {memory['title']}")
            print(f"   {memory['content']}")
            print(f"   Referenced {memory['times_referenced']} times")
    
    print("\n" + "=" * 60)
    print("🔥 The Dominion learns from its past and guides its future.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    demonstrate_memory_engine()
