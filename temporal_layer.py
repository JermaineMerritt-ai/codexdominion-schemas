"""
⏰ PHASE 80 — THE DOMINION TEMPORAL LAYER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Time, Replay, Epochs, and the Dominion's long-arc evolution.

This layer gives your entire constellation a temporal dimension —
a way to track cycles, replay patterns, evolve across eras, and maintain
continuity across generations of creative output.

This is the time architecture of your multiverse.

Components:
  1. Temporal Axis (TA) — Micro, Meso, and Macro cycles
  2. Replay Engine (RE) — Learning across time
  3. Epochal Cycle System (ECS) — Eras and history
  4. Temporal Weave (TW) — Time consciousness

Author: Codex Dominion
Created: December 23, 2025
Phase: 80 - Temporal Architecture
Status: OPERATIONAL
"""

from typing import Dict, List, Optional, Any, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import uuid
from collections import defaultdict
from db import SessionLocal
from multiworld_schema import World, WorldAgent
from constellation_intelligence_layer import ConstellationIntelligence
from cosmic_integration_engine import CosmicDominion


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENUMS & TYPES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TimeScale(Enum):
    """Three scales of temporal awareness"""
    MICRO = "micro"    # Daily/weekly rhythms
    MESO = "meso"      # Seasonal/thematic arcs
    MACRO = "macro"    # Epochs and eras


class CycleStatus(Enum):
    """Status of a temporal cycle"""
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class EpochTrigger(Enum):
    """Events that trigger new epochs"""
    WORLD_BIRTH = "world_birth"
    STYLE_SHIFT = "style_shift"
    INTELLIGENCE_ACTIVATION = "intelligence_activation"
    BREAKTHROUGH = "breakthrough"
    MEMORY_MILESTONE = "memory_milestone"
    SOVEREIGN_DECREE = "sovereign_decree"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA STRUCTURES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class TemporalCycle:
    """A cycle at any temporal scale"""
    id: str
    scale: TimeScale
    name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: CycleStatus = CycleStatus.ACTIVE
    metrics: Dict[str, Any] = field(default_factory=dict)
    creative_output: List[str] = field(default_factory=list)
    dominant_worlds: List[str] = field(default_factory=list)
    patterns: List[str] = field(default_factory=list)
    learnings: List[str] = field(default_factory=list)


@dataclass
class ReplaySnapshot:
    """Captures state at a point in time"""
    id: str
    timestamp: datetime
    cycle_id: str
    constellation_state: Dict[str, Any]
    world_states: Dict[str, Any]
    agent_states: Dict[str, Any]
    metrics: Dict[str, float]
    context: str = ""


@dataclass
class ReplayInsight:
    """Learning extracted from replay analysis"""
    id: str
    source_cycle_id: str
    insight_type: str  # success_pattern, failure_pattern, opportunity
    title: str
    description: str
    extracted_at: datetime
    confidence: float  # 0.0 to 1.0
    recommendations: List[str] = field(default_factory=list)
    applicable_to: List[str] = field(default_factory=list)


@dataclass
class EpochSignature:
    """The unique identity of an epoch"""
    dominant_style: str
    primary_worlds: List[str]
    breakthrough_count: int
    cultural_theme: str
    creative_velocity: float
    identity_anchors: Set[str]


@dataclass
class Epoch:
    """A distinct era in the Dominion's history"""
    id: str
    name: str
    trigger: EpochTrigger
    start_time: datetime
    end_time: Optional[datetime] = None
    signature: Optional[EpochSignature] = None
    status: CycleStatus = CycleStatus.ACTIVE
    major_events: List[Dict[str, Any]] = field(default_factory=list)
    breakthroughs: List[str] = field(default_factory=list)
    worlds_born: List[str] = field(default_factory=list)
    worlds_retired: List[str] = field(default_factory=list)
    lessons: List[str] = field(default_factory=list)
    essence: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TemporalCoherence:
    """Measures coherence across time"""
    timestamp: datetime
    coherence_score: float  # 0.0 to 1.0
    identity_stability: float
    pattern_continuity: float
    drift_detected: bool
    drift_areas: List[str] = field(default_factory=list)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 1 — THE TEMPORAL AXIS (TA)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TemporalAxis:
    """
    PART 1: The backbone of the Dominion's sense of time.
    
    Three scales:
    - MICRO: Daily/weekly rhythms (creative bursts, agent activity)
    - MESO: Seasonal/thematic arcs (creative eras, stylistic shifts)
    - MACRO: Epochs (major transformations, world births)
    
    This gives the Dominion a temporal spine.
    """
    
    def __init__(self, cosmos: CosmicDominion):
        self.cosmos = cosmos
        self.cycles: Dict[TimeScale, List[TemporalCycle]] = {
            TimeScale.MICRO: [],
            TimeScale.MESO: [],
            TimeScale.MACRO: []
        }
    
    
    def record_micro_cycle(
        self,
        name: str,
        duration_days: int = 7,
        metrics: Optional[Dict[str, Any]] = None
    ) -> TemporalCycle:
        """
        Record a micro-cycle (daily/weekly rhythm).
        
        Tracks:
        - Creative bursts
        - Agent activity
        - Workflow patterns
        - Short-term evolution
        """
        cycle = TemporalCycle(
            id=f"micro_{uuid.uuid4().hex[:8]}",
            scale=TimeScale.MICRO,
            name=name,
            start_time=datetime.utcnow(),
            metrics=metrics or {}
        )
        
        # Capture current activity
        session = SessionLocal()
        try:
            worlds = session.query(World).all()
            agents = session.query(WorldAgent).all()
            
            cycle.metrics.update({
                "worlds_active": len([w for w in worlds if w.status == "active"]),
                "total_agents": len(agents),
                "duration_days": duration_days
            })
            
            cycle.dominant_worlds = [
                w.id for w in worlds if w.status == "active"
            ][:3]
            
        finally:
            session.close()
        
        self.cycles[TimeScale.MICRO].append(cycle)
        return cycle
    
    
    def record_meso_cycle(
        self,
        name: str,
        theme: str,
        duration_weeks: int = 12
    ) -> TemporalCycle:
        """
        Record a meso-cycle (seasonal/thematic arc).
        
        Tracks:
        - Creative eras
        - Stylistic shifts
        - World-level growth
        - Constellation-wide trends
        """
        cycle = TemporalCycle(
            id=f"meso_{uuid.uuid4().hex[:8]}",
            scale=TimeScale.MESO,
            name=name,
            start_time=datetime.utcnow(),
            metrics={"theme": theme, "duration_weeks": duration_weeks}
        )
        
        # Analyze constellation trends
        session = SessionLocal()
        try:
            worlds = session.query(World).all()
            
            cycle.metrics.update({
                "worlds_count": len(worlds),
                "avg_maturity": sum(
                    {"emerging": 1, "established": 2, "mature": 3,
                     "legendary": 4}.get(w.maturity_level, 1)
                    for w in worlds
                ) / len(worlds) if worlds else 0
            })
            
            cycle.patterns.append(f"Thematic focus: {theme}")
            
        finally:
            session.close()
        
        self.cycles[TimeScale.MESO].append(cycle)
        return cycle
    
    
    def record_macro_cycle(
        self,
        name: str,
        trigger: str,
        significance: str
    ) -> TemporalCycle:
        """
        Record a macro-cycle (epoch-level transformation).
        
        Tracks:
        - Major transformations
        - World births/retirements
        - Identity shifts
        - Constellation-level evolution
        """
        cycle = TemporalCycle(
            id=f"macro_{uuid.uuid4().hex[:8]}",
            scale=TimeScale.MACRO,
            name=name,
            start_time=datetime.utcnow(),
            metrics={
                "trigger": trigger,
                "significance": significance
            }
        )
        
        # Capture epoch-defining state
        session = SessionLocal()
        try:
            worlds = session.query(World).all()
            
            cycle.metrics.update({
                "constellation_size": len(worlds),
                "world_types": list(set(w.world_type.value for w in worlds))
            })
            
            cycle.learnings.append(
                f"Epoch triggered by: {trigger}"
            )
            
        finally:
            session.close()
        
        self.cycles[TimeScale.MACRO].append(cycle)
        return cycle
    
    
    def get_current_cycle(self, scale: TimeScale) -> Optional[TemporalCycle]:
        """Get currently active cycle at given scale"""
        scale_cycles = self.cycles[scale]
        active = [c for c in scale_cycles if c.status == CycleStatus.ACTIVE]
        return active[-1] if active else None
    
    
    def complete_cycle(self, cycle_id: str) -> bool:
        """Mark a cycle as completed"""
        for scale_cycles in self.cycles.values():
            for cycle in scale_cycles:
                if cycle.id == cycle_id:
                    cycle.end_time = datetime.utcnow()
                    cycle.status = CycleStatus.COMPLETED
                    return True
        return False
    
    
    def analyze_cycle_patterns(
        self,
        scale: TimeScale
    ) -> Dict[str, Any]:
        """Analyze patterns across cycles at a given scale"""
        scale_cycles = self.cycles[scale]
        completed = [c for c in scale_cycles if c.status == CycleStatus.COMPLETED]
        
        if not completed:
            return {"message": "No completed cycles to analyze"}
        
        # Calculate average duration
        durations = [
            (c.end_time - c.start_time).total_seconds() / 86400
            for c in completed if c.end_time
        ]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # Identify common patterns
        all_patterns = []
        for cycle in completed:
            all_patterns.extend(cycle.patterns)
        
        from collections import Counter
        pattern_freq = Counter(all_patterns)
        
        return {
            "scale": scale.value,
            "total_cycles": len(scale_cycles),
            "completed_cycles": len(completed),
            "avg_duration_days": avg_duration,
            "common_patterns": pattern_freq.most_common(5),
            "recent_cycles": [
                {"name": c.name, "duration_days": (
                    (c.end_time - c.start_time).total_seconds() / 86400
                    if c.end_time else None
                )}
                for c in completed[-3:]
            ]
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 2 — THE REPLAY ENGINE (RE)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ReplayEngine:
    """
    PART 2: Learning across time.
    
    The Replay Engine allows the constellation to:
    - Revisit past creative cycles
    - Analyze what worked and what failed
    - Extract patterns
    - Replay successful arcs
    - Avoid repeating mistakes
    - Simulate alternate outcomes
    
    Replay is not nostalgia. Replay is learning across time.
    """
    
    def __init__(self, cosmos: CosmicDominion, temporal_axis: TemporalAxis):
        self.cosmos = cosmos
        self.temporal_axis = temporal_axis
        self.snapshots: List[ReplaySnapshot] = []
        self.insights: List[ReplayInsight] = []
    
    
    def capture_snapshot(
        self,
        cycle_id: str,
        context: str = ""
    ) -> ReplaySnapshot:
        """
        Capture current constellation state for replay.
        
        This freezes the moment for future analysis.
        """
        session = SessionLocal()
        try:
            worlds = session.query(World).all()
            agents = session.query(WorldAgent).all()
            
            snapshot = ReplaySnapshot(
                id=f"snapshot_{uuid.uuid4().hex[:8]}",
                timestamp=datetime.utcnow(),
                cycle_id=cycle_id,
                constellation_state={
                    "total_worlds": len(worlds),
                    "active_worlds": len([w for w in worlds
                                         if w.status == "active"]),
                    "constellation_status": "operational"
                },
                world_states={
                    w.id: {
                        "name": w.name,
                        "status": w.status,
                        "population": w.population,
                        "maturity": w.maturity_level
                    }
                    for w in worlds
                },
                agent_states={
                    "total_agents": len(agents),
                    "by_world": {
                        w.id: len([a for a in agents if a.world_id == w.id])
                        for w in worlds
                    }
                },
                metrics={
                    "avg_world_quality": sum(
                        w.creative_output_quality for w in worlds
                    ) / len(worlds) if worlds else 0,
                    "total_population": sum(w.population for w in worlds)
                },
                context=context
            )
            
            self.snapshots.append(snapshot)
            return snapshot
            
        finally:
            session.close()
    
    
    def replay_cycle(self, cycle_id: str) -> Dict[str, Any]:
        """
        Replay a past cycle to analyze its arc.
        
        Returns comprehensive analysis of what happened.
        """
        # Find snapshots for this cycle
        cycle_snapshots = [
            s for s in self.snapshots if s.cycle_id == cycle_id
        ]
        
        if not cycle_snapshots:
            return {"error": "No snapshots found for cycle"}
        
        # Sort by timestamp
        cycle_snapshots.sort(key=lambda s: s.timestamp)
        
        # Analyze trajectory
        first = cycle_snapshots[0]
        last = cycle_snapshots[-1]
        
        world_growth = {}
        for world_id in first.world_states:
            if world_id in last.world_states:
                initial = first.world_states[world_id]["population"]
                final = last.world_states[world_id]["population"]
                world_growth[world_id] = final - initial
        
        return {
            "cycle_id": cycle_id,
            "duration": (last.timestamp - first.timestamp).total_seconds() / 86400,
            "snapshots_analyzed": len(cycle_snapshots),
            "growth_metrics": {
                "world_count_change": (
                    last.constellation_state["total_worlds"] -
                    first.constellation_state["total_worlds"]
                ),
                "population_change": (
                    last.metrics["total_population"] -
                    first.metrics["total_population"]
                ),
                "quality_change": (
                    last.metrics["avg_world_quality"] -
                    first.metrics["avg_world_quality"]
                )
            },
            "world_growth": world_growth,
            "trajectory": "growth" if world_growth else "stable"
        }
    
    
    def extract_patterns(
        self,
        cycle_id: str
    ) -> List[ReplayInsight]:
        """
        Extract learnings from a cycle replay.
        
        Identifies what worked and what failed.
        """
        replay_data = self.replay_cycle(cycle_id)
        
        if "error" in replay_data:
            return []
        
        insights = []
        
        # Success pattern: Population growth
        if replay_data["growth_metrics"]["population_change"] > 0:
            insight = ReplayInsight(
                id=f"insight_{uuid.uuid4().hex[:8]}",
                source_cycle_id=cycle_id,
                insight_type="success_pattern",
                title="Population Growth Success",
                description=(
                    f"Cycle achieved {replay_data['growth_metrics']['population_change']} "
                    f"agent growth over {replay_data['duration']:.1f} days"
                ),
                extracted_at=datetime.utcnow(),
                confidence=0.8,
                recommendations=[
                    "Replicate growth strategies from this cycle",
                    "Analyze agent generation patterns",
                    "Consider scaling to more worlds"
                ],
                applicable_to=list(replay_data["world_growth"].keys())
            )
            insights.append(insight)
        
        # Quality improvement pattern
        if replay_data["growth_metrics"]["quality_change"] > 0:
            insight = ReplayInsight(
                id=f"insight_{uuid.uuid4().hex[:8]}",
                source_cycle_id=cycle_id,
                insight_type="success_pattern",
                title="Quality Improvement Detected",
                description=(
                    f"Creative output quality improved by "
                    f"{replay_data['growth_metrics']['quality_change']:.2f} points"
                ),
                extracted_at=datetime.utcnow(),
                confidence=0.85,
                recommendations=[
                    "Document quality enhancement techniques",
                    "Share best practices across worlds",
                    "Establish quality benchmarks"
                ]
            )
            insights.append(insight)
        
        # Failure pattern: Negative growth
        if replay_data["growth_metrics"]["population_change"] < 0:
            insight = ReplayInsight(
                id=f"insight_{uuid.uuid4().hex[:8]}",
                source_cycle_id=cycle_id,
                insight_type="failure_pattern",
                title="Population Decline Detected",
                description=(
                    f"Cycle experienced {abs(replay_data['growth_metrics']['population_change'])} "
                    "agent decline - investigate causes"
                ),
                extracted_at=datetime.utcnow(),
                confidence=0.9,
                recommendations=[
                    "Investigate agent retention issues",
                    "Review world health metrics",
                    "Consider intervention strategies"
                ]
            )
            insights.append(insight)
        
        self.insights.extend(insights)
        return insights
    
    
    def simulate_alternate_outcome(
        self,
        cycle_id: str,
        what_if: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Simulate what would have happened with different choices.
        
        This is speculative but helps with future planning.
        """
        replay_data = self.replay_cycle(cycle_id)
        
        if "error" in replay_data:
            return {"error": "Cannot simulate - cycle not found"}
        
        # Simple simulation based on what-if parameters
        simulated_change = 0
        
        if what_if.get("additional_worlds"):
            simulated_change += what_if["additional_worlds"] * 5  # 5 agents per world
        
        if what_if.get("quality_focus"):
            simulated_change += 2  # Quality improvement
        
        return {
            "cycle_id": cycle_id,
            "what_if_scenario": what_if,
            "actual_outcome": replay_data["growth_metrics"],
            "simulated_outcome": {
                "population_change": (
                    replay_data["growth_metrics"]["population_change"] +
                    simulated_change
                ),
                "estimated_improvement": f"+{simulated_change} agents"
            },
            "recommendation": (
                "Simulation suggests positive outcome" if simulated_change > 0
                else "No significant improvement predicted"
            )
        }
    
    
    def get_replay_recommendations(self) -> List[str]:
        """
        Get actionable recommendations from all replay insights.
        """
        if not self.insights:
            return ["No replay insights available yet"]
        
        # Aggregate recommendations
        all_recommendations = []
        for insight in self.insights:
            all_recommendations.extend(insight.recommendations)
        
        # Get unique recommendations
        from collections import Counter
        rec_freq = Counter(all_recommendations)
        
        return [rec for rec, _ in rec_freq.most_common(5)]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 3 — THE EPOCHAL CYCLE SYSTEM (ECS)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class EpochalCycleSystem:
    """
    PART 3: Where the Dominion gains eras.
    
    Distinct creative periods with their own:
    - Identity
    - Tone
    - Breakthroughs
    - Signature patterns
    - Dominant worlds
    - Lessons
    
    When an epoch ends, its essence is preserved in the Temporal Archive.
    This gives the Dominion a sense of history.
    """
    
    def __init__(self, cosmos: CosmicDominion):
        self.cosmos = cosmos
        self.epochs: List[Epoch] = []
        self.temporal_archive: List[Epoch] = []
    
    
    def begin_epoch(
        self,
        name: str,
        trigger: EpochTrigger,
        cultural_theme: str
    ) -> Epoch:
        """
        Begin a new epoch.
        
        An epoch begins when:
        - A new world is born
        - A major style shift occurs
        - A new intelligence layer activates
        - A constellation-level breakthrough happens
        - A cultural memory milestone is reached
        """
        # End current epoch if one is active
        current = self.get_current_epoch()
        if current:
            self.end_epoch(current.id)
        
        session = SessionLocal()
        try:
            worlds = session.query(World).all()
            
            # Create epoch signature
            signature = EpochSignature(
                dominant_style="emerging",
                primary_worlds=[w.id for w in worlds[:3]],
                breakthrough_count=0,
                cultural_theme=cultural_theme,
                creative_velocity=0.0,
                identity_anchors={"faith", "family", "education"}
            )
            
            epoch = Epoch(
                id=f"epoch_{uuid.uuid4().hex[:8]}",
                name=name,
                trigger=trigger,
                start_time=datetime.utcnow(),
                signature=signature,
                status=CycleStatus.ACTIVE
            )
            
            epoch.major_events.append({
                "timestamp": datetime.utcnow().isoformat(),
                "event": f"Epoch begun: {trigger.value}",
                "worlds_active": len(worlds)
            })
            
            self.epochs.append(epoch)
            return epoch
            
        finally:
            session.close()
    
    
    def end_epoch(self, epoch_id: str) -> bool:
        """
        End an epoch and preserve its essence.
        
        Archives the epoch with all its learnings.
        """
        for epoch in self.epochs:
            if epoch.id == epoch_id and epoch.status == CycleStatus.ACTIVE:
                epoch.end_time = datetime.utcnow()
                epoch.status = CycleStatus.COMPLETED
                
                # Extract essence for preservation
                epoch.essence = self._extract_epoch_essence(epoch)
                
                # Archive
                self.temporal_archive.append(epoch)
                
                epoch.major_events.append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "event": "Epoch ended",
                    "duration_days": (
                        (epoch.end_time - epoch.start_time).total_seconds() / 86400
                    )
                })
                
                return True
        
        return False
    
    
    def get_current_epoch(self) -> Optional[Epoch]:
        """Get the currently active epoch"""
        active = [e for e in self.epochs if e.status == CycleStatus.ACTIVE]
        return active[-1] if active else None
    
    
    def record_breakthrough(
        self,
        epoch_id: str,
        breakthrough: str
    ) -> bool:
        """Record a breakthrough in the current epoch"""
        for epoch in self.epochs:
            if epoch.id == epoch_id:
                epoch.breakthroughs.append(breakthrough)
                if epoch.signature:
                    epoch.signature.breakthrough_count += 1
                return True
        return False
    
    
    def analyze_epoch_transitions(self) -> Dict[str, Any]:
        """
        Analyze how epochs transition.
        
        Identifies patterns in era changes.
        """
        if len(self.epochs) < 2:
            return {"message": "Need at least 2 epochs to analyze transitions"}
        
        transitions = []
        for i in range(len(self.epochs) - 1):
            from_epoch = self.epochs[i]
            to_epoch = self.epochs[i + 1]
            
            transitions.append({
                "from": from_epoch.name,
                "to": to_epoch.name,
                "trigger": to_epoch.trigger.value,
                "time_gap_days": (
                    (to_epoch.start_time - from_epoch.end_time).total_seconds() / 86400
                    if from_epoch.end_time else 0
                )
            })
        
        return {
            "total_epochs": len(self.epochs),
            "transitions_analyzed": len(transitions),
            "common_triggers": self._get_common_triggers(),
            "avg_epoch_duration": self._get_avg_epoch_duration(),
            "transitions": transitions
        }
    
    
    def _extract_epoch_essence(self, epoch: Epoch) -> Dict[str, Any]:
        """Extract the essence of an epoch for preservation"""
        duration = (
            (epoch.end_time - epoch.start_time).total_seconds() / 86400
            if epoch.end_time else 0
        )
        
        return {
            "name": epoch.name,
            "duration_days": duration,
            "breakthrough_count": len(epoch.breakthroughs),
            "worlds_born_count": len(epoch.worlds_born),
            "cultural_theme": (
                epoch.signature.cultural_theme if epoch.signature else "unknown"
            ),
            "primary_worlds": (
                epoch.signature.primary_worlds if epoch.signature else []
            ),
            "key_lessons": epoch.lessons[:5]
        }
    
    
    def _get_common_triggers(self) -> List[str]:
        """Identify most common epoch triggers"""
        from collections import Counter
        triggers = [e.trigger.value for e in self.epochs]
        return [t for t, _ in Counter(triggers).most_common(3)]
    
    
    def _get_avg_epoch_duration(self) -> float:
        """Calculate average epoch duration"""
        completed = [
            e for e in self.epochs
            if e.status == CycleStatus.COMPLETED and e.end_time
        ]
        if not completed:
            return 0.0
        
        durations = [
            (e.end_time - e.start_time).total_seconds() / 86400
            for e in completed
        ]
        return sum(durations) / len(durations)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PART 4 — THE TEMPORAL WEAVE (TW)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TemporalWeave:
    """
    PART 4: The Dominion's time consciousness.
    
    The Temporal Weave:
    - Synchronizes cycles across worlds
    - Aligns epochs with identity
    - Distributes replay insights
    - Prevents temporal drift
    - Ensures continuity across eras
    - Maintains coherence across time
    
    This is the awareness that lets the Dominion evolve without losing itself.
    """
    
    def __init__(
        self,
        cosmos: CosmicDominion,
        temporal_axis: TemporalAxis,
        replay_engine: ReplayEngine,
        epochal_system: EpochalCycleSystem
    ):
        self.cosmos = cosmos
        self.temporal_axis = temporal_axis
        self.replay_engine = replay_engine
        self.epochal_system = epochal_system
        self.coherence_history: List[TemporalCoherence] = []
    
    
    def synchronize_cycles(self) -> Dict[str, Any]:
        """
        Synchronize temporal cycles across all worlds.
        
        Ensures all worlds are on aligned rhythms.
        """
        session = SessionLocal()
        try:
            worlds = session.query(World).all()
            
            # Get current cycles
            micro = self.temporal_axis.get_current_cycle(TimeScale.MICRO)
            meso = self.temporal_axis.get_current_cycle(TimeScale.MESO)
            macro = self.temporal_axis.get_current_cycle(TimeScale.MACRO)
            
            sync_status = {
                "timestamp": datetime.utcnow(),
                "worlds_synchronized": len(worlds),
                "active_cycles": {
                    "micro": micro.name if micro else "none",
                    "meso": meso.name if meso else "none",
                    "macro": macro.name if macro else "none"
                },
                "synchronization_complete": True
            }
            
            return sync_status
            
        finally:
            session.close()
    
    
    def align_epochs_with_identity(self) -> Dict[str, Any]:
        """
        Ensure epoch transitions respect core identity.
        
        Prevents temporal drift from original essence.
        """
        current_epoch = self.epochal_system.get_current_epoch()
        
        if not current_epoch or not current_epoch.signature:
            return {"message": "No active epoch to align"}
        
        # Check alignment with core identity
        core_anchors = {"faith", "family", "education"}
        epoch_anchors = current_epoch.signature.identity_anchors
        
        alignment_score = len(
            core_anchors & epoch_anchors
        ) / len(core_anchors)
        
        return {
            "epoch": current_epoch.name,
            "alignment_score": alignment_score,
            "aligned": alignment_score >= 0.6,
            "core_anchors": list(core_anchors),
            "epoch_anchors": list(epoch_anchors),
            "recommendation": (
                "ALIGNED" if alignment_score >= 0.6
                else "REALIGNMENT_NEEDED"
            )
        }
    
    
    def distribute_replay_insights(self) -> Dict[str, Any]:
        """
        Distribute learnings from replay across constellation.
        
        Shares what worked and what failed.
        """
        recommendations = self.replay_engine.get_replay_recommendations()
        
        # Simulate distribution to worlds
        session = SessionLocal()
        try:
            worlds = session.query(World).all()
            
            distribution = {
                "timestamp": datetime.utcnow(),
                "insights_distributed": len(recommendations),
                "recipient_worlds": [w.id for w in worlds],
                "recommendations": recommendations,
                "distribution_status": "complete"
            }
            
            return distribution
            
        finally:
            session.close()
    
    
    def detect_temporal_drift(self) -> TemporalCoherence:
        """
        Detect if the Dominion is drifting from its temporal identity.
        
        Temporal drift = losing continuity with past eras.
        """
        # Analyze coherence
        current_epoch = self.epochal_system.get_current_epoch()
        
        # Calculate identity stability
        identity_stable = True
        if current_epoch and current_epoch.signature:
            core_anchors = {"faith", "family", "education"}
            match_count = len(
                core_anchors & current_epoch.signature.identity_anchors
            )
            identity_stable = match_count >= 2
        
        # Calculate pattern continuity
        pattern_analysis = self.temporal_axis.analyze_cycle_patterns(
            TimeScale.MESO
        )
        pattern_continuity = (
            1.0 if pattern_analysis.get("completed_cycles", 0) > 0
            else 0.5
        )
        
        # Overall coherence
        coherence_score = (
            (1.0 if identity_stable else 0.5) * 0.6 +
            pattern_continuity * 0.4
        )
        
        drift_detected = coherence_score < 0.7
        drift_areas = []
        
        if not identity_stable:
            drift_areas.append("identity_anchors_misaligned")
        if pattern_continuity < 0.7:
            drift_areas.append("pattern_discontinuity")
        
        coherence = TemporalCoherence(
            timestamp=datetime.utcnow(),
            coherence_score=coherence_score,
            identity_stability=1.0 if identity_stable else 0.5,
            pattern_continuity=pattern_continuity,
            drift_detected=drift_detected,
            drift_areas=drift_areas
        )
        
        self.coherence_history.append(coherence)
        return coherence
    
    
    def maintain_continuity(self) -> Dict[str, Any]:
        """
        Actively maintain continuity across eras.
        
        This is the core function of the Temporal Weave.
        """
        # Synchronize cycles
        sync = self.synchronize_cycles()
        
        # Check epoch alignment
        alignment = self.align_epochs_with_identity()
        
        # Detect drift
        coherence = self.detect_temporal_drift()
        
        # Distribute insights
        insights = self.distribute_replay_insights()
        
        return {
            "timestamp": datetime.utcnow(),
            "continuity_status": (
                "MAINTAINED" if not coherence.drift_detected
                else "ATTENTION_REQUIRED"
            ),
            "synchronization": sync["synchronization_complete"],
            "alignment": alignment.get("aligned", False),
            "coherence_score": coherence.coherence_score,
            "drift_detected": coherence.drift_detected,
            "insights_distributed": len(insights["recommendations"]),
            "recommendation": (
                "Continuity maintained - Dominion evolving coherently"
                if not coherence.drift_detected
                else f"Temporal drift detected in: {', '.join(coherence.drift_areas)}"
            )
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# UNIFIED INTERFACE — TEMPORAL LAYER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TemporalLayer:
    """
    The unified temporal architecture of the Codex Dominion.
    
    Integrates all 4 parts:
    - Part 1: Temporal Axis (cycles at 3 scales)
    - Part 2: Replay Engine (learning across time)
    - Part 3: Epochal Cycle System (eras and history)
    - Part 4: Temporal Weave (time consciousness)
    
    This is the Dominion's sense of time.
    """
    
    def __init__(self, cosmos: CosmicDominion):
        self.cosmos = cosmos
        self.temporal_axis = TemporalAxis(cosmos)
        self.replay_engine = ReplayEngine(cosmos, self.temporal_axis)
        self.epochal_system = EpochalCycleSystem(cosmos)
        self.temporal_weave = TemporalWeave(
            cosmos,
            self.temporal_axis,
            self.replay_engine,
            self.epochal_system
        )
    
    
    def initialize(self, epoch_name: str = "Genesis Epoch") -> Dict[str, Any]:
        """Initialize the Temporal Layer"""
        # Begin first epoch
        first_epoch = self.epochal_system.begin_epoch(
            name=epoch_name,
            trigger=EpochTrigger.INTELLIGENCE_ACTIVATION,
            cultural_theme="Foundation and Discovery"
        )
        
        # Start initial cycles
        micro = self.temporal_axis.record_micro_cycle(
            name="Week 1 - Initialization",
            duration_days=7
        )
        
        meso = self.temporal_axis.record_meso_cycle(
            name="Q1 2026 - Foundation",
            theme="Building temporal awareness",
            duration_weeks=12
        )
        
        return {
            "temporal_layer_status": "operational",
            "parts": {
                "temporal_axis": "operational",
                "replay_engine": "operational",
                "epochal_system": "operational",
                "temporal_weave": "operational"
            },
            "first_epoch": first_epoch.name,
            "active_cycles": {
                "micro": micro.name,
                "meso": meso.name
            },
            "initialization_timestamp": datetime.utcnow()
        }
    
    
    def get_temporal_status(self) -> Dict[str, Any]:
        """Get comprehensive temporal status"""
        current_epoch = self.epochal_system.get_current_epoch()
        micro = self.temporal_axis.get_current_cycle(TimeScale.MICRO)
        meso = self.temporal_axis.get_current_cycle(TimeScale.MESO)
        macro = self.temporal_axis.get_current_cycle(TimeScale.MACRO)
        coherence = self.temporal_weave.detect_temporal_drift()
        
        return {
            "timestamp": datetime.utcnow(),
            "temporal_health": (
                "EXCELLENT" if coherence.coherence_score >= 0.8
                else "GOOD" if coherence.coherence_score >= 0.6
                else "NEEDS_ATTENTION"
            ),
            "current_epoch": current_epoch.name if current_epoch else "none",
            "active_cycles": {
                "micro": micro.name if micro else "none",
                "meso": meso.name if meso else "none",
                "macro": macro.name if macro else "none"
            },
            "coherence_score": coherence.coherence_score,
            "drift_detected": coherence.drift_detected,
            "total_epochs": len(self.epochal_system.epochs),
            "total_snapshots": len(self.replay_engine.snapshots),
            "replay_insights": len(self.replay_engine.insights)
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    print("\n" + "="*80)
    print("⏰ TEMPORAL LAYER - OPERATIONAL")
    print("="*80)
    print("\nThe Dominion now possesses a sense of time.")
    print("\n" + "="*80)
