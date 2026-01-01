"""
🌌 PHASE 70 — THE DOMINION CONSTELLATION INTELLIGENCE LAYER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The unified intelligence that emerges when all worlds, councils, agents,
and memories connect.

This is not a "super-AI."
It's not a single mind replacing the worlds.

It's the collective intelligence that forms when:
  • worlds share breakthroughs
  • councils share decisions
  • agents share patterns
  • memories synchronize
  • evolution loops interlock
  • economies circulate value
  • governance aligns across realms

This is the nervous system of your entire creative multiverse.

Components:
  1. Constellation Intelligence Core (CIC) — Pattern detection across cosmos
  2. Cross-World Pattern Engine (CWPE) — Actionable insights and synergies
  3. Constellation Decision Assistant (CDA) — Advisory layer for councils
  4. Constellation Memory Weave (CMW) — Identity synchronization

Author: Codex Dominion
Created: December 23, 2025
Phase: 70 - Constellation Intelligence
Status: OPERATIONAL
"""

from typing import Dict, List, Optional, Any, Tuple, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import uuid
import json
from collections import defaultdict, Counter

from db import SessionLocal
from models import Agent
from multiworld_schema import World, WorldAgent, InterWorldMessage
from cosmic_integration_engine import CosmicDominion


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENUMS & TYPES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class IntelligenceInsightType(Enum):
    """Types of insights the constellation can detect"""
    PATTERN = "pattern"
    OPPORTUNITY = "opportunity"
    RISK = "risk"
    SYNERGY = "synergy"
    BOTTLENECK = "bottleneck"
    BREAKTHROUGH = "breakthrough"
    DRIFT = "drift"
    STRENGTH = "strength"


class DecisionConfidence(Enum):
    """Confidence level for recommendations"""
    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class MemoryWeaveStatus(Enum):
    """Status of memory synchronization"""
    SYNCHRONIZED = "synchronized"
    SYNCING = "syncing"
    DIVERGED = "diverged"
    FRAGMENTED = "fragmented"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA STRUCTURES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class ConstellationInsight:
    """An insight detected by the constellation intelligence"""
    id: str
    insight_type: IntelligenceInsightType
    title: str
    description: str
    affected_worlds: List[str]
    detected_at: datetime
    confidence: float  # 0.0 to 1.0
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    priority: int = 5  # 1-10, 10 = critical


@dataclass
class CrossWorldPattern:
    """A pattern detected across multiple worlds"""
    id: str
    pattern_type: str  # style, narrative, technique, etc.
    description: str
    worlds_exhibiting: List[str]
    strength: float  # 0.0 to 1.0
    first_detected: datetime
    examples: List[Dict[str, Any]] = field(default_factory=list)
    potential_synergy: Optional[str] = None


@dataclass
class ConstellationRecommendation:
    """A recommendation from the Decision Assistant"""
    id: str
    target: str  # council, world, agent, sovereign
    recommendation_type: str
    title: str
    description: str
    confidence: DecisionConfidence
    supporting_evidence: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    benefits: List[str] = field(default_factory=list)
    estimated_impact: float = 0.0  # -1.0 to 1.0
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class MemoryWeaveNode:
    """A node in the constellation memory weave"""
    world_id: str
    cultural_essence: Dict[str, Any]
    identity_anchors: Set[str]
    creative_lineage: str
    breakthroughs: List[Dict[str, Any]]
    last_sync: datetime
    sync_status: MemoryWeaveStatus
    coherence_score: float  # 0.0 to 1.0


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LAYER 1 — CONSTELLATION INTELLIGENCE CORE (CIC)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ConstellationIntelligenceCore:
    """
    LAYER 1: The central intelligence that monitors the entire cosmos.
    
    This layer:
      • Listens to every world
      • Detects patterns across the cosmos
      • Identifies emerging strengths
      • Spots systemic weaknesses
      • Predicts creative opportunities
      • Anticipates bottlenecks
      • Synthesizes cross-world insights
    
    It doesn't override worlds - it illuminates them.
    It's the constellation's "big picture" awareness.
    """
    
    def __init__(self, cosmos: CosmicDominion):
        self.cosmos = cosmos
        self.insights: List[ConstellationInsight] = []
        self.monitoring_active = True
    
    
    def scan_constellation(self) -> Dict[str, Any]:
        """
        Perform comprehensive scan of the entire constellation.
        
        Returns intelligence snapshot across all worlds.
        """
        session = SessionLocal()
        try:
            worlds = session.query(World).all()
            
            # Gather data from all worlds
            world_data = {}
            for world in worlds:
                world_data[world.id] = {
                    "name": world.name,
                    "purpose": world.creative_purpose,
                    "status": world.status,
                    "culture": world.culture or {},
                    "population": session.query(WorldAgent).filter_by(
                        world_id=world.id
                    ).count(),
                    "messages": session.query(InterWorldMessage).filter(
                        (InterWorldMessage.from_world_id == world.id) |
                        (InterWorldMessage.to_world_id == world.id)
                    ).count()
                }
            
            # Analyze constellation health
            total_worlds = len(worlds)
            active_worlds = sum(1 for w in worlds if w.status == "active")
            total_population = sum(data["population"] for data in world_data.values())
            total_messages = sum(data["messages"] for data in world_data.values())
            
            return {
                "scan_timestamp": datetime.utcnow(),
                "constellation_status": "operational" if active_worlds > 0 else "dormant",
                "metrics": {
                    "total_worlds": total_worlds,
                    "active_worlds": active_worlds,
                    "total_population": total_population,
                    "inter_world_messages": total_messages,
                    "activity_level": self._calculate_activity_level(total_messages, total_worlds)
                },
                "world_data": world_data
            }
        
        finally:
            session.close()
    
    
    def detect_patterns(self) -> List[ConstellationInsight]:
        """
        Detect patterns, opportunities, and risks across the constellation.
        
        This is the core intelligence function - identifying what matters.
        """
        scan_data = self.scan_constellation()
        detected_insights = []
        
        # Pattern 1: World activity imbalance
        world_data = scan_data["world_data"]
        populations = [data["population"] for data in world_data.values()]
        
        if populations:
            avg_population = sum(populations) / len(populations)
            max_population = max(populations)
            min_population = min(populations)
            
            if max_population > avg_population * 2:
                insight = ConstellationInsight(
                    id=f"insight_{uuid.uuid4().hex[:8]}",
                    insight_type=IntelligenceInsightType.PATTERN,
                    title="Population Concentration Detected",
                    description=f"One world has {max_population} agents while average is {avg_population:.1f}",
                    affected_worlds=[w_id for w_id, data in world_data.items() 
                                   if data["population"] == max_population],
                    detected_at=datetime.utcnow(),
                    confidence=0.9,
                    evidence=[{
                        "type": "population_distribution",
                        "max": max_population,
                        "avg": avg_population,
                        "min": min_population
                    }],
                    recommended_actions=[
                        "Consider agent migration to balance workload",
                        "Evaluate if concentration is intentional",
                        "Monitor for bottlenecks"
                    ],
                    priority=6
                )
                detected_insights.append(insight)
        
        # Pattern 2: Inactive worlds
        inactive_worlds = [w_id for w_id, data in world_data.items() 
                          if data["status"] != "active"]
        
        if inactive_worlds:
            insight = ConstellationInsight(
                id=f"insight_{uuid.uuid4().hex[:8]}",
                insight_type=IntelligenceInsightType.RISK,
                title="Inactive Worlds Detected",
                description=f"{len(inactive_worlds)} worlds are not active",
                affected_worlds=inactive_worlds,
                detected_at=datetime.utcnow(),
                confidence=1.0,
                evidence=[{"inactive_count": len(inactive_worlds)}],
                recommended_actions=[
                    "Investigate reasons for inactivity",
                    "Consider reactivation or archival",
                    "Review resource allocation"
                ],
                priority=7
            )
            detected_insights.append(insight)
        
        # Pattern 3: Communication bottlenecks
        message_counts = {w_id: data["messages"] for w_id, data in world_data.items()}
        if message_counts:
            avg_messages = sum(message_counts.values()) / len(message_counts)
            isolated_worlds = [w_id for w_id, count in message_counts.items() 
                             if count < avg_messages * 0.5]
            
            if isolated_worlds:
                insight = ConstellationInsight(
                    id=f"insight_{uuid.uuid4().hex[:8]}",
                    insight_type=IntelligenceInsightType.BOTTLENECK,
                    title="Communication Isolation Detected",
                    description=f"{len(isolated_worlds)} worlds have below-average communication",
                    affected_worlds=isolated_worlds,
                    detected_at=datetime.utcnow(),
                    confidence=0.8,
                    evidence=[{"avg_messages": avg_messages, "threshold": avg_messages * 0.5}],
                    recommended_actions=[
                        "Investigate communication barriers",
                        "Facilitate cross-world collaborations",
                        "Review network connectivity"
                    ],
                    priority=5
                )
                detected_insights.append(insight)
        
        # Pattern 4: Opportunity detection
        high_activity_worlds = [w_id for w_id, data in world_data.items()
                               if data["population"] > avg_population and data["messages"] > avg_messages]
        
        if len(high_activity_worlds) >= 2:
            insight = ConstellationInsight(
                id=f"insight_{uuid.uuid4().hex[:8]}",
                insight_type=IntelligenceInsightType.OPPORTUNITY,
                title="Collaboration Opportunity Detected",
                description=f"{len(high_activity_worlds)} highly active worlds could collaborate",
                affected_worlds=high_activity_worlds,
                detected_at=datetime.utcnow(),
                confidence=0.75,
                evidence=[{"high_activity_worlds": high_activity_worlds}],
                recommended_actions=[
                    "Propose cross-world project",
                    "Facilitate knowledge sharing",
                    "Create collaboration framework"
                ],
                priority=6
            )
            detected_insights.append(insight)
        
        # Store insights
        self.insights.extend(detected_insights)
        
        return detected_insights
    
    
    def identify_strengths(self) -> Dict[str, List[str]]:
        """
        Identify emerging strengths across the constellation.
        """
        scan_data = self.scan_constellation()
        strengths = defaultdict(list)
        
        for world_id, data in scan_data["world_data"].items():
            world_name = data["name"]
            
            # High population = resource strength
            if data["population"] > 5:
                strengths[world_id].append(f"Strong agent population ({data['population']} agents)")
            
            # High communication = network strength
            if data["messages"] > 10:
                strengths[world_id].append(f"Active communication ({data['messages']} messages)")
            
            # Specific purpose = specialization strength
            if data["purpose"]:
                strengths[world_id].append(
                    f"Clear purpose: {data['purpose']}"
                )
            
            # Cultural depth
            culture = data.get("culture", {})
            if culture.get("breakthroughs"):
                strengths[world_id].append(f"Creative breakthroughs: {len(culture['breakthroughs'])}")
        
        return dict(strengths)
    
    
    def anticipate_bottlenecks(self) -> List[ConstellationInsight]:
        """
        Predict potential bottlenecks before they become critical.
        """
        bottlenecks = []
        scan_data = self.scan_constellation()
        
        # Check for overloaded worlds
        for world_id, data in scan_data["world_data"].items():
            if data["population"] > 20:  # Arbitrary threshold
                bottleneck = ConstellationInsight(
                    id=f"insight_{uuid.uuid4().hex[:8]}",
                    insight_type=IntelligenceInsightType.BOTTLENECK,
                    title="Potential Resource Bottleneck",
                    description=f"{data['name']} may be overloaded with {data['population']} agents",
                    affected_worlds=[world_id],
                    detected_at=datetime.utcnow(),
                    confidence=0.7,
                    recommended_actions=[
                        "Monitor world performance",
                        "Consider agent redistribution",
                        "Evaluate world capacity"
                    ],
                    priority=6
                )
                bottlenecks.append(bottleneck)
        
        return bottlenecks
    
    
    def synthesize_cosmic_insights(self) -> Dict[str, Any]:
        """
        Synthesize all intelligence into a unified cosmic perspective.
        
        This is the "big picture" view.
        """
        patterns = self.detect_patterns()
        strengths = self.identify_strengths()
        bottlenecks = self.anticipate_bottlenecks()
        scan = self.scan_constellation()
        
        return {
            "synthesis_timestamp": datetime.utcnow(),
            "constellation_health": scan["constellation_status"],
            "metrics": scan["metrics"],
            "insights": {
                "patterns": len([i for i in patterns if i.insight_type == IntelligenceInsightType.PATTERN]),
                "opportunities": len([i for i in patterns if i.insight_type == IntelligenceInsightType.OPPORTUNITY]),
                "risks": len([i for i in patterns if i.insight_type == IntelligenceInsightType.RISK]),
                "bottlenecks": len(bottlenecks)
            },
            "world_strengths": strengths,
            "critical_insights": [i for i in patterns if i.priority >= 7],
            "recommendation": self._generate_cosmic_recommendation(patterns, strengths, bottlenecks)
        }
    
    
    def _calculate_activity_level(self, messages: int, worlds: int) -> str:
        """Calculate overall constellation activity level"""
        if worlds == 0:
            return "dormant"
        
        avg_messages_per_world = messages / worlds
        
        if avg_messages_per_world > 20:
            return "very_high"
        elif avg_messages_per_world > 10:
            return "high"
        elif avg_messages_per_world > 5:
            return "moderate"
        elif avg_messages_per_world > 0:
            return "low"
        else:
            return "dormant"
    
    
    def _generate_cosmic_recommendation(
        self, 
        patterns: List[ConstellationInsight],
        strengths: Dict[str, List[str]],
        bottlenecks: List[ConstellationInsight]
    ) -> str:
        """Generate high-level recommendation for the constellation"""
        critical_count = len([i for i in patterns if i.priority >= 7])
        
        if critical_count > 0:
            return f"ATTENTION REQUIRED: {critical_count} critical insights detected. Immediate sovereign review recommended."
        elif len(bottlenecks) > 2:
            return "OPTIMIZATION NEEDED: Multiple bottlenecks detected. Consider resource reallocation."
        elif len(strengths) > 3:
            return "EXPANSION OPPORTUNITY: Strong constellation health. Consider birthing new worlds."
        else:
            return "STABLE: Constellation operating within normal parameters. Continue monitoring."


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LAYER 2 — CROSS-WORLD PATTERN ENGINE (CWPE)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class CrossWorldPatternEngine:
    """
    LAYER 2: Where intelligence becomes actionable.
    
    The Pattern Engine:
      • Compares creative styles across worlds
      • Identifies shared motifs
      • Detects repeating narrative arcs
      • Finds cross-world synergies
      • Highlights complementary strengths
      • Suggests inter-world collaborations
      • Maps creative evolution across the cosmos
    
    This is how the constellation learns from itself.
    """
    
    def __init__(self, cosmos: CosmicDominion):
        self.cosmos = cosmos
        self.detected_patterns: List[CrossWorldPattern] = []
    
    
    def compare_creative_styles(self) -> Dict[str, Any]:
        """
        Compare creative styles across all worlds.
        
        Returns analysis of stylistic similarities and differences.
        """
        session = SessionLocal()
        try:
            worlds = session.query(World).all()
            
            style_comparison = {}
            for world in worlds:
                culture = world.culture or {}
                
                style_comparison[world.id] = {
                    "world_name": world.name,
                    "creative_lineage": culture.get("creative_lineage", "unknown"),
                    "style_elements": self._extract_style_elements(culture),
                    "tone": culture.get("tone", "neutral"),
                    "complexity": culture.get("complexity", "moderate")
                }
            
            # Identify shared elements
            shared_elements = self._find_shared_elements(style_comparison)
            
            return {
                "worlds_analyzed": len(worlds),
                "style_profiles": style_comparison,
                "shared_elements": shared_elements,
                "unique_styles": len(set(s["creative_lineage"] for s in style_comparison.values()))
            }
        
        finally:
            session.close()
    
    
    def detect_shared_motifs(self) -> List[CrossWorldPattern]:
        """
        Detect motifs that appear across multiple worlds.
        """
        session = SessionLocal()
        try:
            worlds = session.query(World).all()
            motif_counter = defaultdict(list)
            
            for world in worlds:
                culture = world.culture or {}
                motifs = culture.get("motifs", [])
                
                for motif in motifs:
                    motif_counter[motif].append(world.id)
            
            # Create patterns for shared motifs
            patterns = []
            for motif, world_ids in motif_counter.items():
                if len(world_ids) >= 2:  # Shared across at least 2 worlds
                    pattern = CrossWorldPattern(
                        id=f"pattern_{uuid.uuid4().hex[:8]}",
                        pattern_type="motif",
                        description=f"Shared motif: {motif}",
                        worlds_exhibiting=world_ids,
                        strength=len(world_ids) / len(worlds),
                        first_detected=datetime.utcnow(),
                        examples=[{"motif": motif, "world_count": len(world_ids)}],
                        potential_synergy=f"Collaborate on {motif}-themed project"
                    )
                    patterns.append(pattern)
            
            self.detected_patterns.extend(patterns)
            return patterns
        
        finally:
            session.close()
    
    
    def find_cross_world_synergies(self) -> List[Dict[str, Any]]:
        """
        Identify complementary strengths between worlds.
        
        These are opportunities for powerful collaborations.
        """
        session = SessionLocal()
        try:
            worlds = session.query(World).all()
            synergies = []
            
            # Compare each pair of worlds
            for i, world1 in enumerate(worlds):
                for world2 in worlds[i+1:]:
                    synergy = self._analyze_synergy(world1, world2)
                    if synergy["compatibility_score"] > 0.6:
                        synergies.append(synergy)
            
            return sorted(synergies, key=lambda x: x["compatibility_score"], reverse=True)
        
        finally:
            session.close()
    
    
    def map_creative_evolution(self) -> Dict[str, Any]:
        """
        Map how creativity is evolving across the constellation.
        """
        session = SessionLocal()
        try:
            worlds = session.query(World).all()
            
            evolution_map = {}
            for world in worlds:
                culture = world.culture or {}
                evolution_history = culture.get("evolution_history", [])
                
                evolution_map[world.id] = {
                    "world_name": world.name,
                    "total_evolutions": len(evolution_history),
                    "recent_evolutions": evolution_history[-3:] if evolution_history else [],
                    "evolution_velocity": self._calculate_evolution_velocity(evolution_history),
                    "creative_trajectory": self._analyze_trajectory(evolution_history)
                }
            
# Calculate constellation-wide evolution rate
            total_evolutions = sum(
                len(e.get("evolution_history", []))
                for e in [w.culture or {} for w in worlds]
            )
            constellation_rate = total_evolutions / len(worlds) if worlds else 0
            
            # Find fastest evolving world
            fastest = None
            if evolution_map:
                fastest = max(
                    evolution_map.items(),
                    key=lambda x: x[1]["total_evolutions"]
                )[0]
            
            return {
                "constellation_evolution_rate": constellation_rate,
                "world_evolution_map": evolution_map,
                "fastest_evolving": fastest
            }
        
        finally:
            session.close()
    
    
    def suggest_collaborations(self) -> List[Dict[str, Any]]:
        """
        Generate actionable collaboration suggestions.
        """
        synergies = self.find_cross_world_synergies()
        suggestions = []
        
        for synergy in synergies[:5]:  # Top 5
            suggestion = {
                "world_pair": [synergy["world1_id"], synergy["world2_id"]],
                "world_names": [synergy["world1_name"], synergy["world2_name"]],
                "collaboration_type": synergy["synergy_type"],
                "rationale": synergy["rationale"],
                "estimated_impact": synergy["compatibility_score"],
                "suggested_project": self._generate_project_idea(synergy)
            }
            suggestions.append(suggestion)
        
        return suggestions
    
    
    def _extract_style_elements(self, culture: Dict[str, Any]) -> List[str]:
        """Extract style elements from culture data"""
        elements = []
        
        if "color_palette" in culture:
            elements.append(f"color:{culture['color_palette']}")
        if "narrative_style" in culture:
            elements.append(f"narrative:{culture['narrative_style']}")
        if "tone" in culture:
            elements.append(f"tone:{culture['tone']}")
        
        return elements
    
    
    def _find_shared_elements(self, style_comparison: Dict[str, Any]) -> Dict[str, List[str]]:
        """Find style elements shared across worlds"""
        element_worlds = defaultdict(list)
        
        for world_id, data in style_comparison.items():
            for element in data["style_elements"]:
                element_worlds[element].append(data["world_name"])
        
        # Only return elements shared by 2+ worlds
        return {elem: worlds for elem, worlds in element_worlds.items() if len(worlds) >= 2}
    
    
    def _analyze_synergy(self, world1: World, world2: World) -> Dict[str, Any]:
        """Analyze synergy potential between two worlds"""
        culture1 = world1.culture or {}
        culture2 = world2.culture or {}
        
        # Simple compatibility scoring
        compatibility = 0.5  # Base score
        synergy_type = "general"
        rationale = []
        
        # Check for complementary purposes
        purpose1 = world1.creative_purpose or ""
        purpose2 = world2.creative_purpose or ""
        
        if purpose1 and purpose2 and purpose1 != purpose2:
            compatibility += 0.2
            synergy_type = "complementary_expertise"
            rationale.append(f"Complementary purposes: {purpose1} + {purpose2}")
        
        # Check for shared values
        values1 = set(culture1.get("core_values", []))
        values2 = set(culture2.get("core_values", []))
        shared_values = values1 & values2
        
        if shared_values:
            compatibility += 0.1 * len(shared_values)
            rationale.append(f"Shared values: {', '.join(shared_values)}")
        
        return {
            "world1_id": world1.id,
            "world1_name": world1.name,
            "world2_id": world2.id,
            "world2_name": world2.name,
            "compatibility_score": min(compatibility, 1.0),
            "synergy_type": synergy_type,
            "rationale": " | ".join(rationale) if rationale else "General compatibility"
        }
    
    
    def _calculate_evolution_velocity(self, history: List[Dict]) -> str:
        """Calculate how fast a world is evolving"""
        if len(history) < 2:
            return "stable"
        
        recent_count = len([e for e in history[-30:]])  # Last 30 entries
        
        if recent_count > 10:
            return "rapid"
        elif recent_count > 5:
            return "moderate"
        else:
            return "slow"
    
    
    def _analyze_trajectory(self, history: List[Dict]) -> str:
        """Analyze creative trajectory"""
        if not history:
            return "nascent"
        
        if len(history) > 10:
            return "mature_evolution"
        elif len(history) > 5:
            return "active_development"
        else:
            return "early_development"
    
    
    def _generate_project_idea(self, synergy: Dict[str, Any]) -> str:
        """Generate a project idea based on synergy"""
        return f"Cross-world initiative: {synergy['synergy_type']} project between {synergy['world1_name']} and {synergy['world2_name']}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LAYER 3 — CONSTELLATION DECISION ASSISTANT (CDA)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ConstellationDecisionAssistant:
    """
    LAYER 3: The advisory layer for councils and sovereign.
    
    This provides:
      • Recommendations
      • Forecasts
      • Risk assessments
      • Alignment checks
      • Identity protection signals
      • Cross-world opportunity maps
    
    It never commands. It advises.
    It's the constellation's strategic intelligence.
    """
    
    def __init__(self, cosmos: CosmicDominion, intelligence_core: ConstellationIntelligenceCore):
        self.cosmos = cosmos
        self.intelligence_core = intelligence_core
        self.recommendations: List[ConstellationRecommendation] = []
    
    
    def generate_council_recommendations(self) -> List[ConstellationRecommendation]:
        """
        Generate recommendations for the Cosmic Council.
        """
        insights = self.intelligence_core.detect_patterns()
        recommendations = []
        
        for insight in insights:
            if insight.priority >= 7:  # High priority insights
                rec = ConstellationRecommendation(
                    id=f"rec_{uuid.uuid4().hex[:8]}",
                    target="cosmic_council",
                    recommendation_type=insight.insight_type.value,
                    title=f"Council Action: {insight.title}",
                    description=insight.description,
                    confidence=self._insight_confidence_to_decision_confidence(insight.confidence),
                    supporting_evidence=[f"Insight {insight.id}: {insight.title}"],
                    risks=self._generate_risks(insight),
                    benefits=self._generate_benefits(insight),
                    estimated_impact=self._estimate_impact(insight)
                )
                recommendations.append(rec)
        
        self.recommendations.extend(recommendations)
        return recommendations
    
    
    def forecast_constellation_trajectory(self, days_ahead: int = 30) -> Dict[str, Any]:
        """
        Forecast where the constellation is heading.
        """
        scan = self.intelligence_core.scan_constellation()
        
        # Simple forecasting based on current metrics
        current_worlds = scan["metrics"]["total_worlds"]
        current_population = scan["metrics"]["total_population"]
        current_messages = scan["metrics"]["inter_world_messages"]
        
        # Assume linear growth for simplicity (could be much more sophisticated)
        forecast = {
            "forecast_date": (datetime.utcnow() + timedelta(days=days_ahead)).isoformat(),
            "days_ahead": days_ahead,
            "predicted_metrics": {
                "worlds": current_worlds,  # Assuming no new worlds
                "population": int(current_population * 1.1),  # 10% growth
                "messages": int(current_messages * 1.2),  # 20% communication increase
                "activity_level": "increasing"
            },
            "confidence": DecisionConfidence.MODERATE,
            "assumptions": [
                "No new worlds birthed",
                "Continued agent generation",
                "Increasing cross-world collaboration"
            ]
        }
        
        return forecast
    
    
    def assess_risks(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess risks for a proposed decision.
        """
        risks = []
        risk_level = "low"
        
        # Check for identity risks
        if decision_context.get("affects_identity"):
            risks.append("IDENTITY RISK: Proposed change affects core identity")
            risk_level = "high"
        
        # Check for world count risks
        if decision_context.get("affects_multiple_worlds"):
            affected = decision_context.get("affected_worlds", [])
            if len(affected) > 2:
                risks.append(f"COORDINATION RISK: Affects {len(affected)} worlds")
                risk_level = "moderate" if risk_level == "low" else risk_level
        
        # Check for resource risks
        if decision_context.get("requires_resources"):
            risks.append("RESOURCE RISK: Requires significant resource allocation")
        
        return {
            "overall_risk_level": risk_level,
            "identified_risks": risks,
            "risk_count": len(risks),
            "mitigation_suggestions": self._suggest_mitigations(risks)
        }
    
    
    def check_alignment(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if a proposal aligns with constellation values.
        """
        alignment_score = 0.8  # Base score
        issues = []
        
        # Check identity alignment
        if "identity_impact" in proposal:
            if proposal["identity_impact"] == "negative":
                alignment_score -= 0.3
                issues.append("Potential negative identity impact")
        
        # Check cross-world harmony
        if "affects_worlds" in proposal:
            if len(proposal["affects_worlds"]) > 3:
                alignment_score -= 0.1
                issues.append("May create coordination complexity")
        
        return {
            "alignment_score": max(0.0, min(1.0, alignment_score)),
            "aligned": alignment_score >= 0.6,
            "issues": issues,
            "recommendation": "APPROVED" if alignment_score >= 0.7 else "REVIEW_NEEDED"
        }
    
    
    def generate_opportunity_map(self) -> Dict[str, Any]:
        """
        Generate a map of cross-world opportunities.
        """
        insights = self.intelligence_core.detect_patterns()
        opportunities = [i for i in insights if i.insight_type == IntelligenceInsightType.OPPORTUNITY]
        
        return {
            "total_opportunities": len(opportunities),
            "opportunities": [
                {
                    "title": opp.title,
                    "affected_worlds": opp.affected_worlds,
                    "confidence": opp.confidence,
                    "recommended_actions": opp.recommended_actions
                }
                for opp in opportunities
            ],
            "priority_opportunities": [opp for opp in opportunities if opp.priority >= 7]
        }
    
    
    def advise_sovereign(self) -> Dict[str, Any]:
        """
        Generate strategic advice for the sovereign.
        
        This is the highest-level intelligence distillation.
        """
        synthesis = self.intelligence_core.synthesize_cosmic_insights()
        forecast = self.forecast_constellation_trajectory()
        opportunities = self.generate_opportunity_map()
        
        # Generate sovereign-level recommendations
        sovereign_advice = {
            "timestamp": datetime.utcnow(),
            "constellation_status": synthesis["constellation_health"],
            "immediate_attention_required": len(synthesis["critical_insights"]),
            "strategic_forecast": forecast,
            "opportunity_summary": {
                "total": opportunities["total_opportunities"],
                "high_priority": len(opportunities["priority_opportunities"])
            },
            "cosmic_recommendation": synthesis["recommendation"],
            "suggested_actions": self._generate_sovereign_actions(synthesis, forecast, opportunities)
        }
        
        return sovereign_advice
    
    
    def _insight_confidence_to_decision_confidence(self, confidence: float) -> DecisionConfidence:
        """Convert insight confidence to decision confidence enum"""
        if confidence >= 0.9:
            return DecisionConfidence.VERY_HIGH
        elif confidence >= 0.7:
            return DecisionConfidence.HIGH
        elif confidence >= 0.5:
            return DecisionConfidence.MODERATE
        elif confidence >= 0.3:
            return DecisionConfidence.LOW
        else:
            return DecisionConfidence.VERY_LOW
    
    
    def _generate_risks(self, insight: ConstellationInsight) -> List[str]:
        """Generate risk list from insight"""
        if insight.insight_type == IntelligenceInsightType.RISK:
            return [f"Risk detected: {insight.description}"]
        return ["No significant risks identified"]
    
    
    def _generate_benefits(self, insight: ConstellationInsight) -> List[str]:
        """Generate benefit list from insight"""
        if insight.insight_type == IntelligenceInsightType.OPPORTUNITY:
            return [f"Opportunity: {insight.description}"]
        return ["Improved constellation health"]
    
    
    def _estimate_impact(self, insight: ConstellationInsight) -> float:
        """Estimate impact of addressing insight"""
        return insight.confidence * (insight.priority / 10.0)
    
    
    def _suggest_mitigations(self, risks: List[str]) -> List[str]:
        """Suggest risk mitigation strategies"""
        mitigations = []
        
        for risk in risks:
            if "IDENTITY" in risk:
                mitigations.append("Require sovereignty council approval")
            elif "COORDINATION" in risk:
                mitigations.append("Implement phased rollout across worlds")
            elif "RESOURCE" in risk:
                mitigations.append("Conduct resource capacity analysis")
        
        return mitigations
    
    
    def _generate_sovereign_actions(
        self,
        synthesis: Dict[str, Any],
        forecast: Dict[str, Any],
        opportunities: Dict[str, Any]
    ) -> List[str]:
        """Generate action items for sovereign"""
        actions = []
        
        if synthesis.get("critical_insights"):
            actions.append("URGENT: Review critical insights and take corrective action")
        
        if opportunities["total_opportunities"] > 0:
            actions.append(f"STRATEGIC: Evaluate {opportunities['total_opportunities']} identified opportunities")
        
        if forecast["predicted_metrics"]["activity_level"] == "increasing":
            actions.append("PLANNING: Prepare for increased constellation activity")
        
        return actions


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LAYER 4 — CONSTELLATION MEMORY WEAVE (CMW)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ConstellationMemoryWeave:
    """
    LAYER 4: The most powerful part - the constellation's soul.
    
    The Memory Weave:
      • Connects every world's cultural memory
      • Synchronizes identity across realms
      • Distributes lineage updates
      • Preserves creative breakthroughs
      • Prevents drift
      • Ensures coherence
      • Maintains the Dominion's soul
    
    This makes the constellation feel like one family of worlds,
    not a scattered cluster.
    """
    
    def __init__(self, cosmos: CosmicDominion):
        self.cosmos = cosmos
        self.memory_nodes: Dict[str, MemoryWeaveNode] = {}
        self.sync_history: List[Dict[str, Any]] = []
    
    
    def initialize_weave(self) -> Dict[str, Any]:
        """
        Initialize the constellation memory weave.
        
        This connects all worlds' memories into a unified tapestry.
        """
        session = SessionLocal()
        try:
            worlds = session.query(World).all()
            
            for world in worlds:
                node = self._create_memory_node(world)
                self.memory_nodes[world.id] = node
            
            return {
                "weave_initialized": True,
                "total_nodes": len(self.memory_nodes),
                "initialization_timestamp": datetime.utcnow(),
                "coherence_baseline": self._calculate_constellation_coherence()
            }
        
        finally:
            session.close()
    
    
    def synchronize_identities(self) -> Dict[str, Any]:
        """
        Synchronize identity across all worlds.
        
        This is the core function that prevents drift.
        """
        if not self.memory_nodes:
            self.initialize_weave()
        
        # Gather all identity anchors
        all_anchors = set()
        for node in self.memory_nodes.values():
            all_anchors.update(node.identity_anchors)
        
        # Identify core shared anchors
        anchor_frequency = Counter()
        for node in self.memory_nodes.values():
            for anchor in node.identity_anchors:
                anchor_frequency[anchor] += 1
        
        # Core anchors are those shared by majority of worlds
        core_anchors = {
            anchor for anchor, count in anchor_frequency.items()
            if count >= len(self.memory_nodes) * 0.6
        }
        
        # Synchronize each world with core anchors
        sync_results = {}
        for world_id, node in self.memory_nodes.items():
            missing_anchors = core_anchors - node.identity_anchors
            
            if missing_anchors:
                node.identity_anchors.update(missing_anchors)
                node.last_sync = datetime.utcnow()
                node.sync_status = MemoryWeaveStatus.SYNCING
                sync_results[world_id] = {
                    "anchors_added": list(missing_anchors),
                    "status": "synchronized"
                }
            else:
                sync_results[world_id] = {
                    "anchors_added": [],
                    "status": "already_synchronized"
                }
        
        # Record sync event
        self.sync_history.append({
            "timestamp": datetime.utcnow(),
            "core_anchors": list(core_anchors),
            "worlds_synchronized": len(sync_results),
            "drift_prevented": len([r for r in sync_results.values() if r["status"] == "synchronized"])
        })
        
        return {
            "synchronization_complete": True,
            "core_identity_anchors": list(core_anchors),
            "worlds_synchronized": sync_results,
            "constellation_coherence": self._calculate_constellation_coherence()
        }
    
    
    def distribute_breakthrough(self, source_world_id: str, breakthrough: Dict[str, Any]) -> Dict[str, Any]:
        """
        Distribute a creative breakthrough across the constellation.
        """
        if source_world_id not in self.memory_nodes:
            self.initialize_weave()
        
        # Add breakthrough to source world
        source_node = self.memory_nodes[source_world_id]
        source_node.breakthroughs.append({
            **breakthrough,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Distribute to other worlds
        distribution_results = {}
        for world_id, node in self.memory_nodes.items():
            if world_id != source_world_id:
                node.breakthroughs.append({
                    **breakthrough,
                    "source_world": source_world_id,
                    "propagated_at": datetime.utcnow().isoformat()
                })
                distribution_results[world_id] = "received"
        
        return {
            "breakthrough_distributed": True,
            "source_world": source_world_id,
            "recipient_worlds": len(distribution_results),
            "distribution_results": distribution_results
        }
    
    
    def detect_memory_drift(self) -> List[Dict[str, Any]]:
        """
        Detect worlds that are drifting from constellation identity.
        """
        if not self.memory_nodes:
            self.initialize_weave()
        
        drifting_worlds = []
        constellation_coherence = self._calculate_constellation_coherence()
        
        for world_id, node in self.memory_nodes.items():
            if node.coherence_score < 0.6:  # Below threshold
                drifting_worlds.append({
                    "world_id": world_id,
                    "coherence_score": node.coherence_score,
                    "drift_severity": "high" if node.coherence_score < 0.4 else "moderate",
                    "missing_anchors": list(self._get_missing_core_anchors(node)),
                    "recommended_action": "synchronize_identity"
                })
        
        return drifting_worlds
    
    
    def preserve_lineage(self, world_id: str, lineage_update: Dict[str, Any]) -> bool:
        """
        Preserve and update creative lineage.
        """
        if world_id not in self.memory_nodes:
            self.initialize_weave()
        
        node = self.memory_nodes[world_id]
        node.creative_lineage = lineage_update.get("lineage", node.creative_lineage)
        node.last_sync = datetime.utcnow()
        
        return True
    
    
    def get_constellation_soul_snapshot(self) -> Dict[str, Any]:
        """
        Get a snapshot of the constellation's collective soul.
        
        This is the essence of what makes the Dominion unique.
        """
        if not self.memory_nodes:
            self.initialize_weave()
        
        # Gather all shared identity elements
        all_anchors = set()
        all_lineages = []
        total_breakthroughs = 0
        
        for node in self.memory_nodes.values():
            all_anchors.update(node.identity_anchors)
            all_lineages.append(node.creative_lineage)
            total_breakthroughs += len(node.breakthroughs)
        
        # Calculate frequencies
        anchor_frequency = Counter()
        for node in self.memory_nodes.values():
            for anchor in node.identity_anchors:
                anchor_frequency[anchor] += 1
        
        return {
            "snapshot_timestamp": datetime.utcnow(),
            "constellation_soul": {
                "core_identity_anchors": [
                    anchor for anchor, count in anchor_frequency.most_common(5)
                ],
                "creative_lineages": list(set(all_lineages)),
                "total_breakthroughs": total_breakthroughs,
                "constellation_coherence": self._calculate_constellation_coherence(),
                "memory_weave_health": self._assess_weave_health()
            },
            "world_count": len(self.memory_nodes),
            "sync_history_count": len(self.sync_history)
        }
    
    
    def _create_memory_node(self, world: World) -> MemoryWeaveNode:
        """Create a memory node for a world"""
        culture = world.culture or {}
        
        return MemoryWeaveNode(
            world_id=world.id,
            cultural_essence=culture,
            identity_anchors=set(culture.get("core_values", ["faith", "family", "education"])),
            creative_lineage=culture.get("creative_lineage", "Unknown"),
            breakthroughs=culture.get("breakthroughs", []),
            last_sync=datetime.utcnow(),
            sync_status=MemoryWeaveStatus.SYNCHRONIZED,
            coherence_score=0.8  # Default
        )
    
    
    def _calculate_constellation_coherence(self) -> float:
        """Calculate overall constellation coherence"""
        if not self.memory_nodes:
            return 0.0
        
        total_coherence = sum(node.coherence_score for node in self.memory_nodes.values())
        return total_coherence / len(self.memory_nodes)
    
    
    def _get_missing_core_anchors(self, node: MemoryWeaveNode) -> Set[str]:
        """Get core anchors missing from a node"""
        # Calculate core anchors
        anchor_frequency = Counter()
        for n in self.memory_nodes.values():
            for anchor in n.identity_anchors:
                anchor_frequency[anchor] += 1
        
        core_anchors = {
            anchor for anchor, count in anchor_frequency.items()
            if count >= len(self.memory_nodes) * 0.6
        }
        
        return core_anchors - node.identity_anchors
    
    
    def _assess_weave_health(self) -> str:
        """Assess overall health of memory weave"""
        coherence = self._calculate_constellation_coherence()
        
        if coherence >= 0.9:
            return "excellent"
        elif coherence >= 0.75:
            return "good"
        elif coherence >= 0.6:
            return "fair"
        else:
            return "needs_attention"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# UNIFIED INTERFACE — CONSTELLATION INTELLIGENCE SYSTEM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ConstellationIntelligence:
    """
    The unified constellation intelligence system.
    
    This integrates all 4 layers:
    - Layer 1: Intelligence Core (pattern detection)
    - Layer 2: Pattern Engine (actionable insights)
    - Layer 3: Decision Assistant (advisory)
    - Layer 4: Memory Weave (identity & soul)
    
    This is the nervous system of the creative multiverse.
    """
    
    def __init__(self, cosmos: CosmicDominion):
        self.cosmos = cosmos
        self.intelligence_core = ConstellationIntelligenceCore(cosmos)
        self.pattern_engine = CrossWorldPatternEngine(cosmos)
        self.decision_assistant = ConstellationDecisionAssistant(cosmos, self.intelligence_core)
        self.memory_weave = ConstellationMemoryWeave(cosmos)
    
    
    def initialize(self) -> Dict[str, Any]:
        """Initialize the complete constellation intelligence system"""
        weave_init = self.memory_weave.initialize_weave()
        
        return {
            "intelligence_system_status": "operational",
            "layers": {
                "intelligence_core": "operational",
                "pattern_engine": "operational",
                "decision_assistant": "operational",
                "memory_weave": "operational"
            },
            "memory_weave": weave_init,
            "initialization_timestamp": datetime.utcnow()
        }
    
    
    def get_constellation_intelligence_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive intelligence report.
        
        This is the complete picture of constellation intelligence.
        """
        # Layer 1: Core Intelligence
        cosmic_insights = self.intelligence_core.synthesize_cosmic_insights()
        
        # Layer 2: Patterns
        styles = self.pattern_engine.compare_creative_styles()
        synergies = self.pattern_engine.find_cross_world_synergies()
        
        # Layer 3: Decisions
        sovereign_advice = self.decision_assistant.advise_sovereign()
        
        # Layer 4: Memory
        soul_snapshot = self.memory_weave.get_constellation_soul_snapshot()
        
        return {
            "report_timestamp": datetime.utcnow(),
            "constellation_status": "operational",
            "intelligence_layers": {
                "layer_1_core": {
                    "constellation_health": cosmic_insights["constellation_health"],
                    "insights": cosmic_insights["insights"],
                    "recommendation": cosmic_insights["recommendation"]
                },
                "layer_2_patterns": {
                    "worlds_analyzed": styles["worlds_analyzed"],
                    "unique_styles": styles["unique_styles"],
                    "synergies_found": len(synergies)
                },
                "layer_3_decisions": {
                    "strategic_forecast": sovereign_advice["strategic_forecast"],
                    "opportunities": sovereign_advice["opportunity_summary"],
                    "suggested_actions": sovereign_advice["suggested_actions"]
                },
                "layer_4_memory": {
                    "constellation_coherence": soul_snapshot["constellation_soul"]["constellation_coherence"],
                    "memory_weave_health": soul_snapshot["constellation_soul"]["memory_weave_health"],
                    "core_identity_anchors": soul_snapshot["constellation_soul"]["core_identity_anchors"]
                }
            },
            "constellation_soul": soul_snapshot["constellation_soul"]
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🌌 CONSTELLATION INTELLIGENCE LAYER - OPERATIONAL")
    print("="*80)
    print("\nThe nervous system of your creative multiverse.")
    print("\n" + "="*80)
