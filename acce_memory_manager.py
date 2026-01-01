"""
🧠 ACCE Cultural Memory Manager

The civilization's living archive - enabling agents to:
- Learn from historical patterns
- Access relevant context for creative work
- Contribute new insights to collective knowledge
- Recognize and replicate success patterns
"""

from sqlalchemy import func, or_, and_
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import json
import re
from collections import Counter

from acce_models import (
    CulturalMemory, Agent, ProjectHistory, 
    PerformanceMetric, SystemLog, MemoryType
)
from db import SessionLocal


class MemoryManager:
    """Manage the civilization's cultural memory and learning systems"""
    
    def __init__(self, db_session: Session = None):
        self.session = db_session or SessionLocal()
    
    # ==================== MEMORY RETRIEVAL ====================
    
    def search_memories(
        self,
        query: str = None,
        memory_types: List[MemoryType] = None,
        tags: List[str] = None,
        min_impact_score: int = 0,
        limit: int = 10
    ) -> List[CulturalMemory]:
        """
        Search cultural memories by keywords, type, tags, or relevance
        
        Args:
            query: Text search across title, description, insights
            memory_types: Filter by memory type (STYLE, LESSON, TECHNIQUE, etc.)
            tags: Filter by tags
            min_impact_score: Minimum impact score (0-100)
            limit: Maximum results to return
            
        Returns:
            List of matching memories, ordered by relevance
        """
        query_filter = self.session.query(CulturalMemory)
        
        # Text search
        if query:
            search_pattern = f"%{query}%"
            query_filter = query_filter.filter(
                or_(
                    CulturalMemory.title.ilike(search_pattern),
                    CulturalMemory.description.ilike(search_pattern)
                )
            )
        
        # Type filter
        if memory_types:
            query_filter = query_filter.filter(CulturalMemory.memory_type.in_(memory_types))
        
        # Tag filter (JSON search)
        if tags:
            for tag in tags:
                query_filter = query_filter.filter(
                    func.json_extract(CulturalMemory.tags, '$').like(f'%{tag}%')
                )
        
        # Impact score filter
        if min_impact_score > 0:
            query_filter = query_filter.filter(CulturalMemory.impact_score >= min_impact_score)
        
        # Order by impact score and reference count
        memories = query_filter.order_by(
            CulturalMemory.impact_score.desc(),
            CulturalMemory.reference_count.desc()
        ).limit(limit).all()
        
        # Increment reference counts
        for memory in memories:
            memory.reference_count += 1
        self.session.commit()
        
        return memories
    
    def get_contextual_memories(
        self,
        agent_id: str,
        task_context: Dict,
        limit: int = 5
    ) -> List[CulturalMemory]:
        """
        Get memories most relevant to an agent's current task
        
        Args:
            agent_id: Agent requesting context
            task_context: Dict with keys like 'type', 'domain', 'goals', 'constraints'
            limit: Maximum memories to return
            
        Returns:
            List of relevant memories for the task
        """
        agent = self.session.query(Agent).get(agent_id)
        if not agent:
            return []
        
        # Extract context keywords
        context_text = " ".join(str(v) for v in task_context.values())
        keywords = self._extract_keywords(context_text)
        
        # Search by keywords and agent specialization
        relevant_types = self._map_agent_to_memory_types(agent.agent_type)
        
        memories = self.search_memories(
            query=" ".join(keywords),
            memory_types=relevant_types,
            min_impact_score=60,
            limit=limit
        )
        
        # Log memory access
        self._log_memory_access(agent_id, [m.id for m in memories], task_context)
        
        return memories
    
    def get_pattern_memories(
        self,
        pattern_type: str,
        min_success_rating: int = 70
    ) -> List[CulturalMemory]:
        """
        Retrieve memories containing specific patterns
        
        Args:
            pattern_type: Type of pattern to search for (e.g., 'color_scheme', 'narrative_structure')
            min_success_rating: Minimum success rating (0-100)
            
        Returns:
            Memories with matching patterns
        """
        memories = self.session.query(CulturalMemory).filter(
            CulturalMemory.success_rating >= min_success_rating
        ).all()
        
        # Filter by pattern content
        pattern_matches = []
        for memory in memories:
            if memory.patterns:
                patterns = memory.patterns if isinstance(memory.patterns, dict) else json.loads(memory.patterns)
                if pattern_type in patterns:
                    pattern_matches.append(memory)
        
        return pattern_matches
    
    def get_related_memories(
        self,
        memory_id: str,
        limit: int = 5
    ) -> List[CulturalMemory]:
        """
        Get memories related to a specific memory
        
        Args:
            memory_id: ID of the source memory
            limit: Maximum results
            
        Returns:
            Related memories
        """
        source_memory = self.session.query(CulturalMemory).get(memory_id)
        if not source_memory or not source_memory.related_memories:
            return []
        
        related_ids = source_memory.related_memories if isinstance(source_memory.related_memories, list) else json.loads(source_memory.related_memories)
        
        return self.session.query(CulturalMemory).filter(
            CulturalMemory.id.in_(related_ids[:limit])
        ).all()
    
    # ==================== MEMORY CONTRIBUTION ====================
    
    def contribute_memory(
        self,
        contributor_id: str,
        title: str,
        memory_type: MemoryType,
        description: str,
        key_insights: List[str],
        lessons_learned: List[str],
        patterns: Dict = None,
        tags: List[str] = None,
        project_id: str = None,
        success_rating: int = 75
    ) -> CulturalMemory:
        """
        Agent contributes a new memory to the collective knowledge
        
        Args:
            contributor_id: Agent who discovered/created this memory
            title: Memory title
            memory_type: Type of memory (STYLE, LESSON, TECHNIQUE, etc.)
            description: Detailed description
            key_insights: Main takeaways
            lessons_learned: What was learned
            patterns: Reusable patterns discovered
            tags: Classification tags
            project_id: Related project (if any)
            success_rating: How successful was this (0-100)
            
        Returns:
            Created memory
        """
        # Create memory
        memory = CulturalMemory(
            title=title,
            memory_type=memory_type,
            description=description,
            key_insights=key_insights,
            lessons_learned=lessons_learned,
            patterns=patterns or {},
            tags=tags or [],
            project_id=project_id,
            success_rating=success_rating,
            impact_score=self._calculate_initial_impact(key_insights, patterns),
            reference_count=0
        )
        
        self.session.add(memory)
        self.session.commit()
        
        # Update agent's contribution count
        agent = self.session.query(Agent).get(contributor_id)
        if agent:
            agent.innovations_created += 1
            self.session.commit()
        
        # Log contribution
        self._log_event(
            "MEMORY_CONTRIBUTED",
            f"Agent {contributor_id} contributed new {memory_type.value} memory: {title}",
            {"memory_id": memory.id, "agent_id": contributor_id}
        )
        
        print(f"💾 New memory archived: {title} ({memory_type.value})")
        print(f"   Contributor: {agent.name if agent else 'Unknown'}")
        print(f"   Insights: {len(key_insights)}, Lessons: {len(lessons_learned)}")
        print(f"   Impact Score: {memory.impact_score}/100")
        
        return memory
    
    def update_memory_impact(
        self,
        memory_id: str,
        impact_delta: int,
        reason: str
    ):
        """
        Update a memory's impact score based on usage
        
        Args:
            memory_id: Memory to update
            impact_delta: Change in impact score (+/-)
            reason: Why the impact changed
        """
        memory = self.session.query(CulturalMemory).get(memory_id)
        if not memory:
            return
        
        old_impact = memory.impact_score
        memory.impact_score = max(0, min(100, memory.impact_score + impact_delta))
        self.session.commit()
        
        self._log_event(
            "MEMORY_IMPACT_UPDATED",
            f"Memory '{memory.title}' impact: {old_impact} → {memory.impact_score}",
            {"memory_id": memory_id, "reason": reason, "delta": impact_delta}
        )
    
    def link_memories(
        self,
        memory_id_1: str,
        memory_id_2: str,
        relationship: str = "related"
    ):
        """
        Create a relationship between two memories
        
        Args:
            memory_id_1: First memory
            memory_id_2: Second memory
            relationship: Type of relationship
        """
        memory1 = self.session.query(CulturalMemory).get(memory_id_1)
        memory2 = self.session.query(CulturalMemory).get(memory_id_2)
        
        if not memory1 or not memory2:
            return
        
        # Add bidirectional links
        related1 = memory1.related_memories or []
        if memory_id_2 not in related1:
            related1.append(memory_id_2)
            memory1.related_memories = related1
        
        related2 = memory2.related_memories or []
        if memory_id_1 not in related2:
            related2.append(memory_id_1)
            memory2.related_memories = related2
        
        self.session.commit()
        
        print(f"🔗 Linked memories: '{memory1.title}' ↔ '{memory2.title}'")
    
    # ==================== PATTERN RECOGNITION ====================
    
    def analyze_success_patterns(
        self,
        min_success_rating: int = 80,
        min_occurrences: int = 3
    ) -> Dict[str, List[Dict]]:
        """
        Identify patterns that consistently lead to success
        
        Args:
            min_success_rating: Minimum success rating to consider
            min_occurrences: Minimum times pattern must occur
            
        Returns:
            Dict of pattern categories with successful patterns
        """
        successful_memories = self.session.query(CulturalMemory).filter(
            CulturalMemory.success_rating >= min_success_rating
        ).all()
        
        # Collect all patterns
        pattern_categories = {}
        
        for memory in successful_memories:
            if not memory.patterns:
                continue
            
            patterns = memory.patterns if isinstance(memory.patterns, dict) else json.loads(memory.patterns)
            
            for category, pattern_data in patterns.items():
                if category not in pattern_categories:
                    pattern_categories[category] = []
                
                pattern_categories[category].append({
                    "memory_id": memory.id,
                    "memory_title": memory.title,
                    "pattern": pattern_data,
                    "success_rating": memory.success_rating,
                    "impact_score": memory.impact_score
                })
        
        # Filter by minimum occurrences
        filtered_patterns = {}
        for category, patterns in pattern_categories.items():
            if len(patterns) >= min_occurrences:
                # Sort by success rating
                patterns.sort(key=lambda x: x['success_rating'], reverse=True)
                filtered_patterns[category] = patterns
        
        return filtered_patterns
    
    def extract_common_techniques(
        self,
        agent_type: str = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        Extract the most commonly used successful techniques
        
        Args:
            agent_type: Filter by agent type (STORY, DESIGN, etc.)
            limit: Maximum techniques to return
            
        Returns:
            List of common techniques with usage counts
        """
        # Get technique memories
        techniques = self.session.query(CulturalMemory).filter(
            CulturalMemory.memory_type == MemoryType.TECHNIQUE
        ).all()
        
        # Count occurrences of technique keywords
        technique_keywords = Counter()
        
        for memory in techniques:
            # Extract keywords from title and insights
            words = self._extract_keywords(memory.title + " " + memory.description)
            technique_keywords.update(words)
        
        # Get top techniques
        common_techniques = []
        for keyword, count in technique_keywords.most_common(limit):
            # Find memories containing this technique
            related_memories = [
                m for m in techniques 
                if keyword.lower() in (m.title + m.description).lower()
            ]
            
            avg_success = sum(m.success_rating for m in related_memories) / len(related_memories) if related_memories else 0
            
            common_techniques.append({
                "technique": keyword,
                "usage_count": count,
                "avg_success_rating": round(avg_success, 1),
                "memory_count": len(related_memories)
            })
        
        return common_techniques
    
    # ==================== LEARNING & ADAPTATION ====================
    
    def generate_learning_insights(
        self,
        agent_id: str,
        time_period_days: int = 30
    ) -> Dict:
        """
        Generate personalized learning insights for an agent
        
        Args:
            agent_id: Agent to analyze
            time_period_days: Look back period
            
        Returns:
            Learning insights and recommendations
        """
        agent = self.session.query(Agent).get(agent_id)
        if not agent:
            return {}
        
        # Get agent's recent memory accesses
        since_date = datetime.utcnow() - timedelta(days=time_period_days)
        
        # Analyze which memories the agent referenced
        # This would require tracking in a memory_access_log table
        # For now, return general insights based on agent type
        
        relevant_types = self._map_agent_to_memory_types(agent.agent_type)
        recent_memories = self.session.query(CulturalMemory).filter(
            CulturalMemory.memory_type.in_(relevant_types),
            CulturalMemory.created_at >= since_date
        ).order_by(CulturalMemory.impact_score.desc()).limit(10).all()
        
        insights = {
            "agent_id": agent_id,
            "agent_name": agent.name,
            "period_days": time_period_days,
            "relevant_new_memories": len(recent_memories),
            "top_memories": [
                {
                    "title": m.title,
                    "type": m.memory_type.value,
                    "impact": m.impact_score,
                    "key_insight": m.key_insights[0] if m.key_insights else None
                }
                for m in recent_memories[:5]
            ],
            "recommended_focus": self._generate_focus_recommendations(agent, recent_memories),
            "skill_gaps": self._identify_skill_gaps(agent, recent_memories)
        }
        
        return insights
    
    def apply_memory_to_task(
        self,
        memory_id: str,
        task_description: str,
        agent_id: str
    ) -> Dict:
        """
        Apply a memory's patterns/lessons to a specific task
        
        Args:
            memory_id: Memory to apply
            task_description: Description of the task
            agent_id: Agent performing the task
            
        Returns:
            Guidance on how to apply the memory
        """
        memory = self.session.query(CulturalMemory).get(memory_id)
        if not memory:
            return {"error": "Memory not found"}
        
        agent = self.session.query(Agent).get(agent_id)
        
        # Generate application guidance
        guidance = {
            "memory_title": memory.title,
            "memory_type": memory.memory_type.value,
            "task": task_description,
            "applicable_insights": memory.key_insights,
            "applicable_lessons": memory.lessons_learned,
            "patterns_to_follow": memory.patterns,
            "success_probability": self._estimate_success_probability(memory, task_description),
            "recommended_approach": self._generate_approach(memory, task_description, agent)
        }
        
        # Update memory reference count
        memory.reference_count += 1
        self.session.commit()
        
        return guidance
    
    # ==================== ANALYTICS ====================
    
    def get_memory_statistics(self) -> Dict:
        """Get overall memory archive statistics"""
        total_memories = self.session.query(func.count(CulturalMemory.id)).scalar()
        
        # By type
        by_type = {}
        for memory_type in MemoryType:
            count = self.session.query(func.count(CulturalMemory.id)).filter(
                CulturalMemory.memory_type == memory_type
            ).scalar()
            by_type[memory_type.value] = count
        
        # Most referenced
        most_referenced = self.session.query(CulturalMemory).order_by(
            CulturalMemory.reference_count.desc()
        ).limit(5).all()
        
        # Highest impact
        highest_impact = self.session.query(CulturalMemory).order_by(
            CulturalMemory.impact_score.desc()
        ).limit(5).all()
        
        # Average scores
        avg_success = self.session.query(func.avg(CulturalMemory.success_rating)).scalar() or 0
        avg_impact = self.session.query(func.avg(CulturalMemory.impact_score)).scalar() or 0
        
        return {
            "total_memories": total_memories,
            "by_type": by_type,
            "most_referenced": [{"title": m.title, "count": m.reference_count} for m in most_referenced],
            "highest_impact": [{"title": m.title, "score": m.impact_score} for m in highest_impact],
            "average_success_rating": round(avg_success, 1),
            "average_impact_score": round(avg_impact, 1)
        }
    
    # ==================== HELPER METHODS ====================
    
    def _extract_keywords(self, text: str, min_length: int = 4) -> List[str]:
        """Extract meaningful keywords from text"""
        # Remove common stop words
        stop_words = {'the', 'and', 'for', 'with', 'this', 'that', 'from', 'have', 'will', 'your'}
        
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [w for w in words if len(w) >= min_length and w not in stop_words]
        
        return list(set(keywords))
    
    def _map_agent_to_memory_types(self, agent_type: str) -> List[MemoryType]:
        """Map agent type to relevant memory types"""
        mapping = {
            "STORY": [MemoryType.STYLE, MemoryType.TECHNIQUE, MemoryType.PATTERN],
            "DESIGN": [MemoryType.STYLE, MemoryType.TECHNIQUE, MemoryType.PATTERN],
            "AUDIO": [MemoryType.TECHNIQUE, MemoryType.PATTERN],
            "VIDEO": [MemoryType.TECHNIQUE, MemoryType.PATTERN],
            "BRANDING": [MemoryType.STYLE, MemoryType.PATTERN],
            "CONTINUITY": [MemoryType.LESSON, MemoryType.PATTERN],
            "QUALITY": [MemoryType.LESSON, MemoryType.SUCCESS, MemoryType.FAILURE],
            "INNOVATION": [MemoryType.TECHNIQUE, MemoryType.SUCCESS, MemoryType.PATTERN]
        }
        return mapping.get(agent_type, [MemoryType.LESSON])
    
    def _calculate_initial_impact(self, insights: List[str], patterns: Dict) -> int:
        """Calculate initial impact score for a new memory"""
        base_score = 50
        
        # More insights = higher score
        insight_bonus = min(len(insights) * 5, 25)
        
        # Presence of patterns increases score
        pattern_bonus = min(len(patterns) * 3, 25) if patterns else 0
        
        return base_score + insight_bonus + pattern_bonus
    
    def _generate_focus_recommendations(self, agent: Agent, memories: List[CulturalMemory]) -> List[str]:
        """Generate focus recommendations for an agent"""
        recommendations = []
        
        # Analyze memory themes
        themes = Counter()
        for memory in memories:
            if memory.tags:
                themes.update(memory.tags if isinstance(memory.tags, list) else json.loads(memory.tags))
        
        top_themes = themes.most_common(3)
        for theme, count in top_themes:
            recommendations.append(f"Explore more about '{theme}' (trending in {count} recent memories)")
        
        return recommendations
    
    def _identify_skill_gaps(self, agent: Agent, memories: List[CulturalMemory]) -> List[str]:
        """Identify potential skill gaps for an agent"""
        gaps = []
        
        # Compare agent's skills to memory requirements
        agent_skills = set(agent.skills if isinstance(agent.skills, list) else json.loads(agent.skills))
        
        # Extract skills mentioned in memories
        memory_skills = set()
        for memory in memories:
            if memory.patterns:
                patterns = memory.patterns if isinstance(memory.patterns, dict) else json.loads(memory.patterns)
                if 'required_skills' in patterns:
                    memory_skills.update(patterns['required_skills'])
        
        # Find gaps
        missing_skills = memory_skills - agent_skills
        if missing_skills:
            gaps.append(f"Consider developing: {', '.join(list(missing_skills)[:3])}")
        
        return gaps
    
    def _estimate_success_probability(self, memory: CulturalMemory, task_description: str) -> float:
        """Estimate probability of success when applying this memory"""
        base_probability = memory.success_rating / 100.0
        
        # Adjust based on reference count (proven track record)
        reference_boost = min(memory.reference_count * 0.01, 0.15)
        
        # Adjust based on impact score
        impact_boost = (memory.impact_score / 100.0) * 0.1
        
        return min(base_probability + reference_boost + impact_boost, 1.0)
    
    def _generate_approach(
        self,
        memory: CulturalMemory,
        task_description: str,
        agent: Agent
    ) -> str:
        """Generate recommended approach for applying memory to task"""
        approach = f"Based on '{memory.title}' ({memory.memory_type.value}):\n\n"
        
        if memory.key_insights:
            approach += "Key Insights to Apply:\n"
            for i, insight in enumerate(memory.key_insights[:3], 1):
                approach += f"{i}. {insight}\n"
            approach += "\n"
        
        if memory.lessons_learned:
            approach += "Lessons to Remember:\n"
            for i, lesson in enumerate(memory.lessons_learned[:3], 1):
                approach += f"{i}. {lesson}\n"
            approach += "\n"
        
        if memory.patterns:
            approach += "Patterns to Follow:\n"
            patterns = memory.patterns if isinstance(memory.patterns, dict) else json.loads(memory.patterns)
            for key, value in list(patterns.items())[:3]:
                approach += f"- {key}: {value}\n"
        
        return approach.strip()
    
    def _log_memory_access(self, agent_id: str, memory_ids: List[str], context: Dict):
        """Log memory access for learning analytics"""
        self._log_event(
            "MEMORY_ACCESSED",
            f"Agent {agent_id} accessed {len(memory_ids)} memories",
            {
                "agent_id": agent_id,
                "memory_ids": memory_ids,
                "context": context
            }
        )
    
    def _log_event(self, event_type: str, description: str, metadata: Dict):
        """Log an event to the system log"""
        log = SystemLog(
            event_type=event_type,
            description=description,
            metadata=metadata,
            timestamp=datetime.utcnow()
        )
        self.session.add(log)
        self.session.commit()


def demonstrate_memory_system():
    """Demonstrate the cultural memory system capabilities"""
    manager = MemoryManager()
    
    print("=" * 60)
    print("🧠 CULTURAL MEMORY SYSTEM DEMONSTRATION")
    print("=" * 60)
    print()
    
    # 1. Search existing memories
    print("📚 STEP 1: Searching Existing Memories")
    print("-" * 60)
    memories = manager.search_memories(query="quality", limit=3)
    print(f"Found {len(memories)} memories related to 'quality':")
    for mem in memories:
        print(f"   • {mem.title} ({mem.memory_type.value})")
        print(f"     Impact: {mem.impact_score}/100, References: {mem.reference_count}")
    print()
    
    # 2. Contribute new memory
    print("💾 STEP 2: Contributing New Memory")
    print("-" * 60)
    agents = manager.session.query(Agent).filter(Agent.agent_type == "DESIGN").first()
    if agents:
        new_memory = manager.contribute_memory(
            contributor_id=agents.id,
            title="Minimalist Design Principles",
            memory_type=MemoryType.STYLE,
            description="Less is more - focus on essential elements and generous whitespace",
            key_insights=[
                "Remove all non-essential elements",
                "Use whitespace as a design element",
                "Limit color palette to 2-3 colors",
                "Choose typography carefully - usually 1-2 fonts maximum"
            ],
            lessons_learned=[
                "Cluttered designs confuse users",
                "Whitespace increases comprehension",
                "Restraint creates sophistication"
            ],
            patterns={
                "color_palette": "2-3 colors maximum",
                "typography": "1-2 fonts",
                "whitespace_ratio": "40-60%"
            },
            tags=["design", "minimalism", "visual", "branding"],
            success_rating=92
        )
    print()
    
    # 3. Get contextual memories
    print("🎯 STEP 3: Getting Contextual Memories for Task")
    print("-" * 60)
    story_agent = manager.session.query(Agent).filter(Agent.agent_type == "STORY").first()
    if story_agent:
        task_context = {
            "type": "story_creation",
            "domain": "bible_stories",
            "goals": ["engage children", "teach moral lesson"],
            "constraints": ["age_appropriate", "accurate"]
        }
        relevant = manager.get_contextual_memories(story_agent.id, task_context, limit=3)
        print(f"Found {len(relevant)} relevant memories for {story_agent.name}:")
        for mem in relevant:
            print(f"   • {mem.title}")
            if mem.key_insights:
                print(f"     Key Insight: {mem.key_insights[0]}")
    print()
    
    # 4. Analyze success patterns
    print("🔍 STEP 4: Analyzing Success Patterns")
    print("-" * 60)
    patterns = manager.analyze_success_patterns(min_success_rating=80, min_occurrences=1)
    print(f"Found {len(patterns)} pattern categories:")
    for category, pattern_list in list(patterns.items())[:3]:
        print(f"   {category}: {len(pattern_list)} successful patterns")
    print()
    
    # 5. Generate learning insights
    print("📊 STEP 5: Generating Learning Insights")
    print("-" * 60)
    if story_agent:
        insights = manager.generate_learning_insights(story_agent.id, time_period_days=30)
        print(f"Learning insights for {insights.get('agent_name', 'Agent')}:")
        print(f"   New relevant memories: {insights['relevant_new_memories']}")
        if insights['top_memories']:
            print(f"   Top memory: {insights['top_memories'][0]['title']}")
        if insights['recommended_focus']:
            print(f"   Recommendation: {insights['recommended_focus'][0]}")
    print()
    
    # 6. Statistics
    print("📈 STEP 6: Memory Archive Statistics")
    print("-" * 60)
    stats = manager.get_memory_statistics()
    print(f"Total memories: {stats['total_memories']}")
    print(f"Average success rating: {stats['average_success_rating']}/100")
    print(f"Average impact score: {stats['average_impact_score']}/100")
    print("\nBy type:")
    for mem_type, count in stats['by_type'].items():
        if count > 0:
            print(f"   {mem_type}: {count}")
    print()
    
    print("=" * 60)
    print("✅ CULTURAL MEMORY SYSTEM OPERATIONAL!")
    print("=" * 60)
    print()
    print("The civilization can now:")
    print("  ✓ Search and retrieve relevant memories")
    print("  ✓ Learn from historical patterns")
    print("  ✓ Contribute new insights")
    print("  ✓ Adapt based on success/failure")
    print("  ✓ Provide context-aware guidance")
    print()
    print("🔥 The civilization remembers and learns! 👑")


if __name__ == "__main__":
    demonstrate_memory_system()
