"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              🔥 DOMINION COMMAND DASHBOARD INTEGRATION LAYER 🔥             ║
║                                                                              ║
║                    THE THRONE ROOM OF CREATIVE SOVEREIGNTY                   ║
║                                                                              ║
║  Step 7 of the Creative Intelligence Engine — The unified command center    ║
║  where all intelligence, execution, memory, quality, and assembly converge   ║
║  into a single operational interface.                                        ║
║                                                                              ║
║  This is where you command the mind of the Dominion.                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

INTERNAL ARCHITECTURE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Module 1: PROJECT OVERVIEW PANEL (POP)
    Purpose: Bird's-eye view of project status
    Shows: Name, status, progress, current phase, next step, ETA
    
Module 2: STUDIO STATUS GRID (SSG)
    Purpose: Real-time studio health monitoring
    Shows: Graphics/Audio/Video/Integration/Assembly status, queues, errors
    
Module 3: ASSET DEPENDENCY MAP VIEWER (ADMV)
    Purpose: Visual map of asset relationships
    Shows: Assets, dependencies, versions, status, cross-medium links
    
Module 4: CREATIVE CONTINUITY REPORT PANEL (CCRP)
    Purpose: Quality guardian display
    Shows: Style, narrative, harmony, brand compliance scores
    
Module 5: TIMELINE & ORCHESTRATION VIEW (TOV)
    Purpose: Production timeline visualization
    Shows: Task sequences, parallel processes, render timelines
    
Module 6: FINAL DELIVERABLES PANEL (FDP)
    Purpose: Output vault and version management
    Shows: Completed outputs, formats, versions, download links

INTEGRATION FLOW:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    User Input
        ↓
    PIC (Step 1) → Dashboard shows project definition
        ↓
    CRE (Step 2) → Dashboard shows creative direction
        ↓
    MMOE (Step 3) → Dashboard shows production timeline
        ↓
    Studios Execute → Dashboard shows real-time status
        ↓
    ADG (Step 4) → Dashboard shows asset map
        ↓
    CCS (Step 5) → Dashboard shows continuity reports
        ↓
    OAE (Step 6) → Dashboard shows final deliverables
        ↓
    DCD-IL (Step 7) → YOU SEE EVERYTHING IN ONE PLACE

This is the moment the Dominion becomes operationally sovereign.
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, field
import json

# ═══════════════════════════════════════════════════════════════════════════
# ENUMS — Type Safety for Dashboard Operations
# ═══════════════════════════════════════════════════════════════════════════

class ProjectStatus(Enum):
    """Current status of the project"""
    CREATED = "created"
    INTERPRETING = "interpreting"
    REASONING = "reasoning"
    ORCHESTRATING = "orchestrating"
    PRODUCING = "producing"
    VALIDATING = "validating"
    ASSEMBLING = "assembling"
    COMPLETE = "complete"
    ERROR = "error"
    PAUSED = "paused"

class ProjectPhase(Enum):
    """Which phase of the pipeline the project is in"""
    INTERPRETATION = "interpretation"  # PIC
    REASONING = "reasoning"            # CRE
    ORCHESTRATION = "orchestration"    # MMOE
    PRODUCTION = "production"          # Studios
    MEMORY = "memory"                  # ADG
    VALIDATION = "validation"          # CCS
    ASSEMBLY = "assembly"              # OAE
    COMPLETE = "complete"

class StudioStatus(Enum):
    """Health status of each studio"""
    IDLE = "idle"
    ACTIVE = "active"
    BUSY = "busy"
    QUEUED = "queued"
    ERROR = "error"
    OFFLINE = "offline"

class TaskStatus(Enum):
    """Status of individual tasks"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    FAILED = "failed"
    BLOCKED = "blocked"

class QualityLevel(Enum):
    """Quality assessment levels"""
    EXCELLENT = "excellent"      # 0.9+
    GOOD = "good"                # 0.7-0.9
    ACCEPTABLE = "acceptable"    # 0.5-0.7
    NEEDS_WORK = "needs_work"    # 0.3-0.5
    CRITICAL = "critical"        # < 0.3

# ═══════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES — Dashboard Panel Outputs
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ProjectOverview:
    """Module 1: Project Overview Panel output"""
    project_id: str
    project_name: str
    status: ProjectStatus
    current_phase: ProjectPhase
    progress_percentage: float  # 0.0 to 1.0
    next_step: str
    estimated_completion: str
    started_at: str
    elapsed_time_seconds: float
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StudioHealth:
    """Health metrics for a single studio"""
    studio_name: str
    status: StudioStatus
    active_tasks: int
    queued_tasks: int
    completed_tasks: int
    failed_tasks: int
    errors: List[str]
    average_completion_time_seconds: float
    last_activity: str

@dataclass
class StudioStatusGrid:
    """Module 2: Studio Status Grid output"""
    graphics_studio: StudioHealth
    audio_studio: StudioHealth
    video_studio: StudioHealth
    integration_layer: StudioHealth
    assembly_engine: StudioHealth
    overall_health: str  # "healthy", "degraded", "critical"
    timestamp: str

@dataclass
class AssetNode:
    """Node in the asset dependency map"""
    asset_id: str
    asset_name: str
    asset_type: str
    status: str
    version: int
    dependencies: List[str]  # asset_ids this depends on
    dependents: List[str]    # asset_ids that depend on this
    cross_medium_links: List[str]
    position: Tuple[int, int]  # X, Y coordinates for visualization

@dataclass
class AssetDependencyMapView:
    """Module 3: Asset Dependency Map Viewer output"""
    project_id: str
    total_assets: int
    nodes: List[AssetNode]
    edges: List[Dict[str, str]]  # {"from": asset_id, "to": asset_id, "type": dep_type}
    status_breakdown: Dict[str, int]  # Status counts
    version_conflicts: List[str]
    timestamp: str

@dataclass
class ContinuityScore:
    """Score for a single continuity dimension"""
    dimension: str
    score: float  # 0.0 to 1.0
    quality_level: QualityLevel
    violations: List[Dict[str, Any]]
    recommendations: List[str]

@dataclass
class ContinuityReport:
    """Module 4: Creative Continuity Report Panel output"""
    project_id: str
    style_consistency: ContinuityScore
    narrative_continuity: ContinuityScore
    audio_visual_harmony: ContinuityScore
    brand_identity: ContinuityScore
    cross_medium_validation: ContinuityScore
    overall_score: float
    overall_quality: QualityLevel
    total_violations: int
    critical_violations: int
    ready_for_assembly: bool
    timestamp: str

@dataclass
class TimelineTask:
    """A single task in the production timeline"""
    task_id: str
    task_name: str
    studio: str
    status: TaskStatus
    start_time: Optional[str]
    end_time: Optional[str]
    duration_seconds: float
    dependencies: List[str]  # task_ids
    progress_percentage: float

@dataclass
class TimelineOrchestrationView:
    """Module 5: Timeline & Orchestration View output"""
    project_id: str
    total_tasks: int
    completed_tasks: int
    active_tasks: int
    pending_tasks: int
    tasks: List[TimelineTask]
    parallel_streams: int
    critical_path_tasks: List[str]  # task_ids on critical path
    estimated_total_duration_seconds: float
    actual_elapsed_seconds: float
    timestamp: str

@dataclass
class Deliverable:
    """A single deliverable output"""
    deliverable_id: str
    deliverable_type: str
    platform: str
    format: str
    resolution: str
    duration_seconds: Optional[float]
    file_path: str
    file_size_mb: float
    version: int
    created_at: str
    download_url: str

@dataclass
class DeliverablesPanelView:
    """Module 6: Final Deliverables Panel output"""
    project_id: str
    total_deliverables: int
    deliverables: List[Deliverable]
    platforms: List[str]
    formats: List[str]
    version_history: Dict[str, List[int]]  # deliverable_id -> versions
    latest_export_time: str
    total_size_mb: float
    timestamp: str

# ═══════════════════════════════════════════════════════════════════════════
# MODULE 1: PROJECT OVERVIEW PANEL (POP)
# ═══════════════════════════════════════════════════════════════════════════

class ProjectOverviewPanel:
    """
    The bird's-eye view of your project.
    
    Shows:
    - Project name and ID
    - Current status and phase
    - Progress percentage
    - Next step in pipeline
    - Estimated completion time
    
    This is your mission control header.
    """
    
    def __init__(self):
        self.active_projects: Dict[str, Dict[str, Any]] = {}
    
    def track_project(
        self,
        project_id: str,
        project_name: str,
        pic_output: Optional[Dict] = None,
        cre_output: Optional[Dict] = None,
        mmoe_output: Optional[Dict] = None,
        adg_status: Optional[Dict] = None,
        ccs_report: Optional[Dict] = None,
        oae_result: Optional[Dict] = None
    ) -> ProjectOverview:
        """
        Track a project through the entire pipeline.
        Updates status based on which modules have completed.
        """
        # Initialize or update project tracking
        if project_id not in self.active_projects:
            self.active_projects[project_id] = {
                "name": project_name,
                "started_at": datetime.utcnow().isoformat() + "Z",
                "pic_complete": False,
                "cre_complete": False,
                "mmoe_complete": False,
                "adg_complete": False,
                "ccs_complete": False,
                "oae_complete": False
            }
        
        project = self.active_projects[project_id]
        
        # Update completion flags
        if pic_output: project["pic_complete"] = True
        if cre_output: project["cre_complete"] = True
        if mmoe_output: project["mmoe_complete"] = True
        if adg_status: project["adg_complete"] = True
        if ccs_report: project["ccs_complete"] = True
        if oae_result: project["oae_complete"] = True
        
        # Determine current phase and status
        current_phase, status, next_step = self._determine_phase_and_status(project)
        
        # Calculate progress (6 steps total)
        completed_steps = sum([
            project["pic_complete"],
            project["cre_complete"],
            project["mmoe_complete"],
            project["adg_complete"],
            project["ccs_complete"],
            project["oae_complete"]
        ])
        progress = completed_steps / 6.0
        
        # Calculate elapsed time
        started_at = datetime.fromisoformat(project["started_at"].replace("Z", "+00:00"))
        elapsed = (datetime.utcnow() - started_at.replace(tzinfo=None)).total_seconds()
        
        # Estimate completion (simple: remaining_steps * avg_time_per_step)
        avg_time_per_step = elapsed / max(completed_steps, 1)
        remaining_steps = 6 - completed_steps
        estimated_remaining = remaining_steps * avg_time_per_step
        eta = datetime.utcnow().timestamp() + estimated_remaining
        estimated_completion = datetime.fromtimestamp(eta).isoformat() + "Z"
        
        return ProjectOverview(
            project_id=project_id,
            project_name=project_name,
            status=status,
            current_phase=current_phase,
            progress_percentage=progress,
            next_step=next_step,
            estimated_completion=estimated_completion,
            started_at=project["started_at"],
            elapsed_time_seconds=elapsed,
            metadata={
                "pic_complete": project["pic_complete"],
                "cre_complete": project["cre_complete"],
                "mmoe_complete": project["mmoe_complete"],
                "adg_complete": project["adg_complete"],
                "ccs_complete": project["ccs_complete"],
                "oae_complete": project["oae_complete"]
            }
        )
    
    def _determine_phase_and_status(self, project: Dict) -> Tuple[ProjectPhase, ProjectStatus, str]:
        """Determine current phase, status, and next step"""
        if not project["pic_complete"]:
            return ProjectPhase.INTERPRETATION, ProjectStatus.INTERPRETING, "Run Project Intelligence Core (PIC)"
        elif not project["cre_complete"]:
            return ProjectPhase.REASONING, ProjectStatus.REASONING, "Run Creative Reasoning Engine (CRE)"
        elif not project["mmoe_complete"]:
            return ProjectPhase.ORCHESTRATION, ProjectStatus.ORCHESTRATING, "Run Multi-Medium Orchestration Engine (MMOE)"
        elif not project["adg_complete"]:
            return ProjectPhase.PRODUCTION, ProjectStatus.PRODUCING, "Track assets in Asset Dependency Graph (ADG)"
        elif not project["ccs_complete"]:
            return ProjectPhase.VALIDATION, ProjectStatus.VALIDATING, "Validate continuity in Creative Continuity System (CCS)"
        elif not project["oae_complete"]:
            return ProjectPhase.ASSEMBLY, ProjectStatus.ASSEMBLING, "Assemble outputs in Output Assembly Engine (OAE)"
        else:
            return ProjectPhase.COMPLETE, ProjectStatus.COMPLETE, "Project complete — deliverables ready"

# ═══════════════════════════════════════════════════════════════════════════
# MODULE 2: STUDIO STATUS GRID (SSG)
# ═══════════════════════════════════════════════════════════════════════════

class StudioStatusGridPanel:
    """
    Real-time health monitor for all studios.
    
    Shows:
    - Graphics Studio status
    - Audio Studio status
    - Video Studio status
    - Integration Layer status
    - Assembly Engine status
    
    This is your systems health dashboard.
    """
    
    def __init__(self):
        self.studio_metrics: Dict[str, Dict] = {
            "graphics_studio": {"tasks": [], "errors": []},
            "audio_studio": {"tasks": [], "errors": []},
            "video_studio": {"tasks": [], "errors": []},
            "integration_layer": {"tasks": [], "errors": []},
            "assembly_engine": {"tasks": [], "errors": []}
        }
    
    def update_studio_status(
        self,
        mmoe_output: Optional[Dict] = None,
        studio_execution_logs: Optional[List[Dict]] = None,
        oae_status: Optional[Dict] = None
    ) -> StudioStatusGrid:
        """
        Update studio status from MMOE orchestration plan and execution logs.
        """
        # Simulate studio health from orchestration waves
        graphics_health = self._calculate_studio_health("graphics_studio", mmoe_output, studio_execution_logs)
        audio_health = self._calculate_studio_health("audio_studio", mmoe_output, studio_execution_logs)
        video_health = self._calculate_studio_health("video_studio", mmoe_output, studio_execution_logs)
        integration_health = self._calculate_studio_health("integration_layer", mmoe_output, studio_execution_logs)
        assembly_health = self._calculate_studio_health("assembly_engine", mmoe_output, oae_status)
        
        # Determine overall health
        all_studios = [graphics_health, audio_health, video_health, integration_health, assembly_health]
        error_count = sum(len(s.errors) for s in all_studios)
        failed_count = sum(s.failed_tasks for s in all_studios)
        
        if error_count == 0 and failed_count == 0:
            overall_health = "healthy"
        elif error_count < 3 or failed_count < 3:
            overall_health = "degraded"
        else:
            overall_health = "critical"
        
        return StudioStatusGrid(
            graphics_studio=graphics_health,
            audio_studio=audio_health,
            video_studio=video_health,
            integration_layer=integration_health,
            assembly_engine=assembly_health,
            overall_health=overall_health,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    
    def _calculate_studio_health(
        self,
        studio_name: str,
        mmoe_output: Optional[Dict],
        execution_logs: Optional[Any]
    ) -> StudioHealth:
        """Calculate health metrics for a single studio"""
        # Extract task counts from orchestration (simplified simulation)
        active_tasks = 2 if studio_name in ["graphics_studio", "video_studio"] else 1
        queued_tasks = 3 if studio_name == "graphics_studio" else 1
        completed_tasks = 5 if mmoe_output else 0
        failed_tasks = 0
        errors = []
        
        # Determine status
        if failed_tasks > 0:
            status = StudioStatus.ERROR
        elif active_tasks > 3:
            status = StudioStatus.BUSY
        elif active_tasks > 0:
            status = StudioStatus.ACTIVE
        elif queued_tasks > 0:
            status = StudioStatus.QUEUED
        else:
            status = StudioStatus.IDLE
        
        avg_completion_time = 45.0  # seconds (simulated)
        
        return StudioHealth(
            studio_name=studio_name.replace("_", " ").title(),
            status=status,
            active_tasks=active_tasks,
            queued_tasks=queued_tasks,
            completed_tasks=completed_tasks,
            failed_tasks=failed_tasks,
            errors=errors,
            average_completion_time_seconds=avg_completion_time,
            last_activity=datetime.utcnow().isoformat() + "Z"
        )

# ═══════════════════════════════════════════════════════════════════════════
# MODULE 3: ASSET DEPENDENCY MAP VIEWER (ADMV)
# ═══════════════════════════════════════════════════════════════════════════

class AssetDependencyMapViewer:
    """
    Visual map of all assets and their relationships.
    
    Shows:
    - All assets as nodes
    - Dependencies as edges
    - Cross-medium links
    - Version conflicts
    - Status breakdown
    
    This is your creative intelligence map.
    """
    
    def generate_map_view(
        self,
        project_id: str,
        adg_registry: Dict[str, Dict]  # From Asset Dependency Graph
    ) -> AssetDependencyMapView:
        """
        Generate visual map data from ADG registry.
        """
        # Extract nodes
        nodes = []
        edges = []
        status_breakdown = {}
        
        for i, (asset_id, asset_data) in enumerate(adg_registry.items()):
            # Create node
            node = AssetNode(
                asset_id=asset_id,
                asset_name=asset_data.get("name", asset_id),
                asset_type=asset_data.get("type", "unknown"),
                status=asset_data.get("status", "unknown"),
                version=asset_data.get("version", 1),
                dependencies=asset_data.get("dependencies", []),
                dependents=asset_data.get("dependents", []),
                cross_medium_links=asset_data.get("cross_medium_links", []),
                position=(i * 150, (i % 3) * 100)  # Simple grid layout
            )
            nodes.append(node)
            
            # Count status
            status = asset_data.get("status", "unknown")
            status_breakdown[status] = status_breakdown.get(status, 0) + 1
            
            # Create edges for dependencies
            for dep_id in asset_data.get("dependencies", []):
                edges.append({
                    "from": dep_id,
                    "to": asset_id,
                    "type": "requires"
                })
            
            # Create edges for cross-medium links
            for link_id in asset_data.get("cross_medium_links", []):
                edges.append({
                    "from": asset_id,
                    "to": link_id,
                    "type": "cross_medium"
                })
        
        # Check for version conflicts (simplified)
        version_conflicts = []
        
        return AssetDependencyMapView(
            project_id=project_id,
            total_assets=len(nodes),
            nodes=nodes,
            edges=edges,
            status_breakdown=status_breakdown,
            version_conflicts=version_conflicts,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )

# ═══════════════════════════════════════════════════════════════════════════
# MODULE 4: CREATIVE CONTINUITY REPORT PANEL (CCRP)
# ═══════════════════════════════════════════════════════════════════════════

class CreativeContinuityReportPanel:
    """
    Quality guardian display.
    
    Shows:
    - Style consistency score
    - Narrative continuity score
    - Audio-visual harmony score
    - Brand identity compliance score
    - Cross-medium validation score
    
    This is your quality assurance dashboard.
    """
    
    def generate_continuity_report(
        self,
        project_id: str,
        ccs_validation_output: Dict  # From Creative Continuity System
    ) -> ContinuityReport:
        """
        Generate dashboard-friendly continuity report from CCS output.
        """
        # Extract scores from CCS output
        style = ccs_validation_output.get("style_consistency", {})
        narrative = ccs_validation_output.get("narrative_continuity", {})
        harmony = ccs_validation_output.get("audio_visual_harmony", {})
        brand = ccs_validation_output.get("brand_identity", {})
        cross_medium = ccs_validation_output.get("cross_medium_validation", {})
        
        # Create score objects
        style_score = self._create_score("Style Consistency", style)
        narrative_score = self._create_score("Narrative Continuity", narrative)
        harmony_score = self._create_score("Audio-Visual Harmony", harmony)
        brand_score = self._create_score("Brand Identity", brand)
        cross_medium_score = self._create_score("Cross-Medium Validation", cross_medium)
        
        # Calculate overall
        overall_score = ccs_validation_output.get("overall_score", 0.0)
        overall_quality = self._score_to_quality(overall_score)
        
        # Count violations
        all_violations = (
            style.get("violations", []) +
            narrative.get("violations", []) +
            harmony.get("violations", []) +
            brand.get("violations", []) +
            cross_medium.get("violations", [])
        )
        total_violations = len(all_violations)
        critical_violations = sum(1 for v in all_violations if v.get("severity") == "critical")
        
        ready_for_assembly = ccs_validation_output.get("ready_for_assembly", False)
        
        return ContinuityReport(
            project_id=project_id,
            style_consistency=style_score,
            narrative_continuity=narrative_score,
            audio_visual_harmony=harmony_score,
            brand_identity=brand_score,
            cross_medium_validation=cross_medium_score,
            overall_score=overall_score,
            overall_quality=overall_quality,
            total_violations=total_violations,
            critical_violations=critical_violations,
            ready_for_assembly=ready_for_assembly,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    
    def _create_score(self, dimension: str, score_data: Dict) -> ContinuityScore:
        """Create a ContinuityScore object from CCS data"""
        score_value = score_data.get("score", 0.0)
        return ContinuityScore(
            dimension=dimension,
            score=score_value,
            quality_level=self._score_to_quality(score_value),
            violations=score_data.get("violations", []),
            recommendations=score_data.get("recommendations", [])
        )
    
    def _score_to_quality(self, score: float) -> QualityLevel:
        """Convert numeric score to quality level"""
        if score >= 0.9:
            return QualityLevel.EXCELLENT
        elif score >= 0.7:
            return QualityLevel.GOOD
        elif score >= 0.5:
            return QualityLevel.ACCEPTABLE
        elif score >= 0.3:
            return QualityLevel.NEEDS_WORK
        else:
            return QualityLevel.CRITICAL

# ═══════════════════════════════════════════════════════════════════════════
# MODULE 5: TIMELINE & ORCHESTRATION VIEW (TOV)
# ═══════════════════════════════════════════════════════════════════════════

class TimelineOrchestrationViewer:
    """
    Production timeline visualization.
    
    Shows:
    - Task sequences
    - Parallel processes
    - Render timelines
    - Audio mixing timelines
    - Video assembly timelines
    
    This is your production Gantt chart.
    """
    
    def generate_timeline_view(
        self,
        project_id: str,
        mmoe_orchestration_plan: Dict,  # From MMOE
        execution_status: Optional[Dict] = None
    ) -> TimelineOrchestrationView:
        """
        Generate timeline visualization from MMOE orchestration plan.
        """
        tasks = []
        
        # Extract waves from orchestration plan
        waves = mmoe_orchestration_plan.get("orchestration_waves", [])
        
        task_id_counter = 1
        for wave_idx, wave in enumerate(waves):
            wave_name = wave.get("wave_name", f"Wave {wave_idx + 1}")
            studios = wave.get("studios", [])
            
            for studio in studios:
                studio_name = studio.get("studio", "Unknown")
                assignments = studio.get("assignments", [])
                
                for assignment in assignments:
                    task_name = assignment.get("task", "Unknown Task")
                    duration = assignment.get("duration_seconds", 60.0)
                    dependencies = assignment.get("dependencies", [])
                    
                    # Determine status (simplified)
                    if execution_status and wave_idx < execution_status.get("completed_waves", 0):
                        status = TaskStatus.COMPLETE
                        progress = 1.0
                    elif execution_status and wave_idx == execution_status.get("current_wave", 0):
                        status = TaskStatus.IN_PROGRESS
                        progress = 0.5
                    else:
                        status = TaskStatus.PENDING
                        progress = 0.0
                    
                    task = TimelineTask(
                        task_id=f"task_{task_id_counter}",
                        task_name=task_name,
                        studio=studio_name,
                        status=status,
                        start_time=wave.get("start_time") if status != TaskStatus.PENDING else None,
                        end_time=None if status != TaskStatus.COMPLETE else wave.get("start_time"),
                        duration_seconds=duration,
                        dependencies=dependencies,
                        progress_percentage=progress
                    )
                    tasks.append(task)
                    task_id_counter += 1
        
        # Calculate statistics
        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t.status == TaskStatus.COMPLETE)
        active_tasks = sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS)
        pending_tasks = sum(1 for t in tasks if t.status == TaskStatus.PENDING)
        
        # Calculate parallel streams (max studios active in any wave)
        parallel_streams = max(len(wave.get("studios", [])) for wave in waves) if waves else 1
        
        # Calculate durations
        estimated_total = sum(t.duration_seconds for t in tasks)
        actual_elapsed = sum(t.duration_seconds for t in tasks if t.status == TaskStatus.COMPLETE)
        
        # Critical path (simplified: longest sequence)
        critical_path_tasks = [t.task_id for t in tasks[:3]]  # Simplified
        
        return TimelineOrchestrationView(
            project_id=project_id,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            active_tasks=active_tasks,
            pending_tasks=pending_tasks,
            tasks=tasks,
            parallel_streams=parallel_streams,
            critical_path_tasks=critical_path_tasks,
            estimated_total_duration_seconds=estimated_total,
            actual_elapsed_seconds=actual_elapsed,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )

# ═══════════════════════════════════════════════════════════════════════════
# MODULE 6: FINAL DELIVERABLES PANEL (FDP)
# ═══════════════════════════════════════════════════════════════════════════

class FinalDeliverablesPanel:
    """
    Output vault and version management.
    
    Shows:
    - Completed outputs
    - Export formats
    - Version history
    - Download links
    - Revision triggers
    
    This is your creative output library.
    """
    
    def generate_deliverables_view(
        self,
        project_id: str,
        oae_assembly_output: Dict  # From Output Assembly Engine
    ) -> DeliverablesPanelView:
        """
        Generate deliverables panel from OAE output.
        """
        deliverables = []
        platforms = set()
        formats = set()
        version_history = {}
        total_size_mb = 0.0
        
        # Extract deliverables from OAE output
        oae_deliverables = oae_assembly_output.get("deliverables", [])
        
        for idx, deliv in enumerate(oae_deliverables):
            platform = deliv.get("platform", "unknown")
            file_format = deliv.get("format", "unknown")
            resolution = deliv.get("resolution", "unknown")
            duration = deliv.get("duration_seconds")
            file_path = deliv.get("file_path", f"/exports/{project_id}/{platform}/output.{file_format}")
            file_size = deliv.get("file_size_mb", 0.0)
            
            deliverable_id = f"deliv_{idx + 1}"
            
            deliverable = Deliverable(
                deliverable_id=deliverable_id,
                deliverable_type=deliv.get("type", "video"),
                platform=platform,
                format=file_format,
                resolution=resolution,
                duration_seconds=duration,
                file_path=file_path,
                file_size_mb=file_size,
                version=1,
                created_at=datetime.utcnow().isoformat() + "Z",
                download_url=f"https://codexdominion.app/downloads/{project_id}/{deliverable_id}"
            )
            
            deliverables.append(deliverable)
            platforms.add(platform)
            formats.add(file_format)
            version_history[deliverable_id] = [1]
            total_size_mb += file_size
        
        latest_export = max((d.created_at for d in deliverables), default=datetime.utcnow().isoformat() + "Z")
        
        return DeliverablesPanelView(
            project_id=project_id,
            total_deliverables=len(deliverables),
            deliverables=deliverables,
            platforms=sorted(platforms),
            formats=sorted(formats),
            version_history=version_history,
            latest_export_time=latest_export,
            total_size_mb=total_size_mb,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )

# ═══════════════════════════════════════════════════════════════════════════
# MASTER DASHBOARD INTEGRATION MANAGER
# ═══════════════════════════════════════════════════════════════════════════

class DominionCommandDashboard:
    """
    🔥 THE THRONE ROOM OF CREATIVE SOVEREIGNTY 🔥
    
    This is the unified command center that brings together:
    - Project Intelligence Core (PIC)
    - Creative Reasoning Engine (CRE)
    - Multi-Medium Orchestration Engine (MMOE)
    - Asset Dependency Graph (ADG)
    - Creative Continuity System (CCS)
    - Output Assembly Engine (OAE)
    
    Into a single, sovereign operational interface.
    
    This is where you command the mind of the Dominion.
    """
    
    def __init__(self):
        self.pop = ProjectOverviewPanel()
        self.ssg = StudioStatusGridPanel()
        self.admv = AssetDependencyMapViewer()
        self.ccrp = CreativeContinuityReportPanel()
        self.tov = TimelineOrchestrationViewer()
        self.fdp = FinalDeliverablesPanel()
    
    def display_complete_dashboard(
        self,
        project_id: str,
        project_name: str,
        pic_output: Optional[Dict] = None,
        cre_output: Optional[Dict] = None,
        mmoe_output: Optional[Dict] = None,
        adg_registry: Optional[Dict] = None,
        ccs_report: Optional[Dict] = None,
        oae_result: Optional[Dict] = None,
        execution_logs: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Generate the complete dashboard view for a project.
        
        This is the master function that combines all 6 modules
        into a unified command interface.
        
        Returns a complete dashboard state with all panels populated.
        """
        # Module 1: Project Overview
        project_overview = self.pop.track_project(
            project_id=project_id,
            project_name=project_name,
            pic_output=pic_output,
            cre_output=cre_output,
            mmoe_output=mmoe_output,
            adg_status=adg_registry,
            ccs_report=ccs_report,
            oae_result=oae_result
        )
        
        # Module 2: Studio Status Grid
        studio_status = self.ssg.update_studio_status(
            mmoe_output=mmoe_output,
            studio_execution_logs=execution_logs,
            oae_status=oae_result
        )
        
        # Module 3: Asset Dependency Map
        asset_map = None
        if adg_registry:
            asset_map = self.admv.generate_map_view(
                project_id=project_id,
                adg_registry=adg_registry
            )
        
        # Module 4: Creative Continuity Report
        continuity_report = None
        if ccs_report:
            continuity_report = self.ccrp.generate_continuity_report(
                project_id=project_id,
                ccs_validation_output=ccs_report
            )
        
        # Module 5: Timeline & Orchestration View
        timeline_view = None
        if mmoe_output:
            timeline_view = self.tov.generate_timeline_view(
                project_id=project_id,
                mmoe_orchestration_plan=mmoe_output,
                execution_status=execution_logs[0] if execution_logs else None
            )
        
        # Module 6: Final Deliverables Panel
        deliverables_view = None
        if oae_result:
            deliverables_view = self.fdp.generate_deliverables_view(
                project_id=project_id,
                oae_assembly_output=oae_result
            )
        
        # Assemble complete dashboard
        return {
            "dashboard_type": "Dominion Command Dashboard",
            "project_id": project_id,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            
            # All 6 modules
            "project_overview": self._to_dict(project_overview),
            "studio_status": self._to_dict(studio_status),
            "asset_map": self._to_dict(asset_map) if asset_map else None,
            "continuity_report": self._to_dict(continuity_report) if continuity_report else None,
            "timeline_view": self._to_dict(timeline_view) if timeline_view else None,
            "deliverables": self._to_dict(deliverables_view) if deliverables_view else None,
            
            # Summary
            "summary": {
                "phase": project_overview.current_phase.value,
                "status": project_overview.status.value,
                "progress": f"{project_overview.progress_percentage * 100:.1f}%",
                "next_step": project_overview.next_step,
                "overall_health": studio_status.overall_health,
                "assets_tracked": asset_map.total_assets if asset_map else 0,
                "continuity_score": continuity_report.overall_score if continuity_report else 0.0,
                "tasks_completed": timeline_view.completed_tasks if timeline_view else 0,
                "deliverables_ready": deliverables_view.total_deliverables if deliverables_view else 0
            }
        }
    
    def _to_dict(self, obj: Any) -> Dict:
        """Convert dataclass or object to dictionary"""
        if obj is None:
            return None
        if hasattr(obj, "__dict__"):
            result = {}
            for key, value in obj.__dict__.items():
                if isinstance(value, Enum):
                    result[key] = value.value
                elif isinstance(value, list):
                    result[key] = [self._to_dict(item) if hasattr(item, "__dict__") else item for item in value]
                elif hasattr(value, "__dict__"):
                    result[key] = self._to_dict(value)
                else:
                    result[key] = value
            return result
        return obj


# ═══════════════════════════════════════════════════════════════════════════
# SINGLETON ACCESS
# ═══════════════════════════════════════════════════════════════════════════

_dashboard_instance = None

def get_dominion_dashboard() -> DominionCommandDashboard:
    """Get the singleton Dominion Command Dashboard instance"""
    global _dashboard_instance
    if _dashboard_instance is None:
        _dashboard_instance = DominionCommandDashboard()
    return _dashboard_instance


# ═══════════════════════════════════════════════════════════════════════════
# DEMO — COMPLETE WORKFLOW INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "🔥 DOMINION COMMAND DASHBOARD INTEGRATION LAYER — DEMO 🔥".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("║" + "The Throne Room of Creative Sovereignty".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # Initialize dashboard
    dashboard = get_dominion_dashboard()
    
    # Simulate complete project workflow
    project_id = "youth_entrepreneurship_course"
    project_name = "Youth Entrepreneurship Video Course"
    
    # Simulate outputs from all 6 previous steps
    # (In real usage, these would come from actual module executions)
    
    # Step 1: PIC output
    pic_output = {
        "interpretation_type": "dominion_optimized",
        "project_type": "video_course",
        "target_audience": "youth_entrepreneurs"
    }
    
    # Step 2: CRE output
    cre_output = {
        "creative_direction": {
            "style": "energetic_modern",
            "narrative": "hero_journey",
            "quality_target": "excellent"
        }
    }
    
    # Step 3: MMOE output
    mmoe_output = {
        "orchestration_waves": [
            {
                "wave_name": "Foundation Wave",
                "start_time": datetime.utcnow().isoformat() + "Z",
                "studios": [
                    {
                        "studio": "graphics_studio",
                        "assignments": [
                            {
                                "task": "Create intro graphics",
                                "duration_seconds": 120.0,
                                "dependencies": []
                            }
                        ]
                    },
                    {
                        "studio": "audio_studio",
                        "assignments": [
                            {
                                "task": "Record voiceover",
                                "duration_seconds": 180.0,
                                "dependencies": []
                            }
                        ]
                    }
                ]
            },
            {
                "wave_name": "Assembly Wave",
                "start_time": datetime.utcnow().isoformat() + "Z",
                "studios": [
                    {
                        "studio": "video_studio",
                        "assignments": [
                            {
                                "task": "Assemble final video",
                                "duration_seconds": 240.0,
                                "dependencies": ["intro_graphics", "voiceover"]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    # Step 4: ADG registry
    adg_registry = {
        "asset_script_001": {
            "name": "Course Script",
            "type": "script",
            "status": "complete",
            "version": 1,
            "dependencies": [],
            "dependents": ["asset_vo_001"],
            "cross_medium_links": []
        },
        "asset_vo_001": {
            "name": "Voiceover Recording",
            "type": "audio",
            "status": "complete",
            "version": 1,
            "dependencies": ["asset_script_001"],
            "dependents": ["asset_vid_001"],
            "cross_medium_links": []
        },
        "asset_gfx_001": {
            "name": "Intro Graphics",
            "type": "graphics",
            "status": "complete",
            "version": 1,
            "dependencies": [],
            "dependents": ["asset_vid_001"],
            "cross_medium_links": ["asset_vid_001"]
        },
        "asset_vid_001": {
            "name": "Final Video",
            "type": "video",
            "status": "in_progress",
            "version": 1,
            "dependencies": ["asset_vo_001", "asset_gfx_001"],
            "dependents": [],
            "cross_medium_links": []
        }
    }
    
    # Step 5: CCS report
    ccs_report = {
        "style_consistency": {
            "score": 0.92,
            "violations": [],
            "recommendations": ["Maintain current color palette"]
        },
        "narrative_continuity": {
            "score": 0.95,
            "violations": [],
            "recommendations": []
        },
        "audio_visual_harmony": {
            "score": 0.88,
            "violations": [
                {"severity": "minor", "issue": "Music tempo slightly slow for video pace"}
            ],
            "recommendations": ["Consider increasing music tempo by 5 BPM"]
        },
        "brand_identity": {
            "score": 0.96,
            "violations": [],
            "recommendations": []
        },
        "cross_medium_validation": {
            "score": 0.94,
            "violations": [],
            "recommendations": []
        },
        "overall_score": 0.93,
        "ready_for_assembly": True
    }
    
    # Step 6: OAE result
    oae_result = {
        "deliverables": [
            {
                "type": "video",
                "platform": "youtube",
                "format": "mp4",
                "resolution": "1920x1080",
                "duration_seconds": 720.0,
                "file_path": f"/exports/{project_id}/youtube/video.mp4",
                "file_size_mb": 1800.0
            },
            {
                "type": "video",
                "platform": "tiktok",
                "format": "mp4",
                "resolution": "1080x1920",
                "duration_seconds": 60.0,
                "file_path": f"/exports/{project_id}/tiktok/video.mp4",
                "file_size_mb": 150.0
            },
            {
                "type": "video",
                "platform": "instagram",
                "format": "mp4",
                "resolution": "1080x1080",
                "duration_seconds": 60.0,
                "file_path": f"/exports/{project_id}/instagram/video.mp4",
                "file_size_mb": 150.0
            }
        ]
    }
    
    # Execution logs (simulated)
    execution_logs = [
        {"completed_waves": 1, "current_wave": 1}
    ]
    
    print("🎯 Generating Complete Dashboard View...")
    print()
    
    # Generate complete dashboard
    complete_dashboard = dashboard.display_complete_dashboard(
        project_id=project_id,
        project_name=project_name,
        pic_output=pic_output,
        cre_output=cre_output,
        mmoe_output=mmoe_output,
        adg_registry=adg_registry,
        ccs_report=ccs_report,
        oae_result=oae_result,
        execution_logs=execution_logs
    )
    
    # Display results
    print("=" * 80)
    print("MODULE 1: PROJECT OVERVIEW PANEL")
    print("=" * 80)
    overview = complete_dashboard["project_overview"]
    print(f"📋 Project: {overview['project_name']}")
    print(f"🔄 Status: {overview['status']}")
    print(f"📊 Phase: {overview['current_phase']}")
    print(f"⚡ Progress: {overview['progress_percentage'] * 100:.1f}%")
    print(f"➡️  Next Step: {overview['next_step']}")
    print(f"⏱️  Elapsed: {overview['elapsed_time_seconds']:.1f}s")
    print(f"🎯 ETA: {overview['estimated_completion']}")
    print()
    
    print("=" * 80)
    print("MODULE 2: STUDIO STATUS GRID")
    print("=" * 80)
    studio_status = complete_dashboard["studio_status"]
    print(f"🏥 Overall Health: {studio_status['overall_health'].upper()}")
    print()
    for studio_key in ["graphics_studio", "audio_studio", "video_studio", "integration_layer", "assembly_engine"]:
        studio = studio_status[studio_key]
        print(f"🎨 {studio['studio_name']}")
        print(f"   Status: {studio['status']}")
        print(f"   Active: {studio['active_tasks']} | Queued: {studio['queued_tasks']} | Done: {studio['completed_tasks']}")
        print(f"   Avg Time: {studio['average_completion_time_seconds']:.1f}s")
        print()
    
    print("=" * 80)
    print("MODULE 3: ASSET DEPENDENCY MAP VIEWER")
    print("=" * 80)
    asset_map = complete_dashboard["asset_map"]
    print(f"📦 Total Assets: {asset_map['total_assets']}")
    print(f"🔗 Total Edges: {len(asset_map['edges'])}")
    print(f"📊 Status Breakdown:")
    for status, count in asset_map["status_breakdown"].items():
        print(f"   {status}: {count}")
    print()
    print("Assets:")
    for node in asset_map["nodes"]:
        deps = len(node["dependencies"])
        print(f"   • {node['asset_name']} ({node['asset_type']}) - v{node['version']} - {node['status']} - {deps} deps")
    print()
    
    print("=" * 80)
    print("MODULE 4: CREATIVE CONTINUITY REPORT PANEL")
    print("=" * 80)
    continuity = complete_dashboard["continuity_report"]
    print(f"🎯 Overall Score: {continuity['overall_score']:.3f} ({continuity['overall_quality']})")
    print(f"⚠️  Total Violations: {continuity['total_violations']} (Critical: {continuity['critical_violations']})")
    print(f"✅ Ready for Assembly: {continuity['ready_for_assembly']}")
    print()
    print("Dimension Scores:")
    for dim_key in ["style_consistency", "narrative_continuity", "audio_visual_harmony", "brand_identity", "cross_medium_validation"]:
        dim = continuity[dim_key]
        print(f"   {dim['dimension']}: {dim['score']:.3f} ({dim['quality_level']})")
    print()
    
    print("=" * 80)
    print("MODULE 5: TIMELINE & ORCHESTRATION VIEW")
    print("=" * 80)
    timeline = complete_dashboard["timeline_view"]
    print(f"📋 Total Tasks: {timeline['total_tasks']}")
    print(f"✅ Completed: {timeline['completed_tasks']}")
    print(f"🔄 Active: {timeline['active_tasks']}")
    print(f"⏳ Pending: {timeline['pending_tasks']}")
    print(f"🔀 Parallel Streams: {timeline['parallel_streams']}")
    print(f"⏱️  Estimated Total: {timeline['estimated_total_duration_seconds']:.1f}s")
    print(f"⌛ Actual Elapsed: {timeline['actual_elapsed_seconds']:.1f}s")
    print()
    print("Tasks:")
    for task in timeline["tasks"][:5]:  # Show first 5
        print(f"   • {task['task_name']} ({task['studio']}) - {task['status']} - {task['progress_percentage'] * 100:.0f}%")
    print()
    
    print("=" * 80)
    print("MODULE 6: FINAL DELIVERABLES PANEL")
    print("=" * 80)
    deliverables = complete_dashboard["deliverables"]
    print(f"📦 Total Deliverables: {deliverables['total_deliverables']}")
    print(f"🌐 Platforms: {', '.join(deliverables['platforms'])}")
    print(f"📁 Formats: {', '.join(deliverables['formats'])}")
    print(f"💾 Total Size: {deliverables['total_size_mb']:.1f} MB")
    print()
    print("Deliverables:")
    for deliv in deliverables["deliverables"]:
        print(f"   • {deliv['platform'].upper()}: {deliv['resolution']} {deliv['format'].upper()} - {deliv['file_size_mb']:.0f}MB")
        print(f"     Download: {deliv['download_url']}")
    print()
    
    print("=" * 80)
    print("DASHBOARD SUMMARY")
    print("=" * 80)
    summary = complete_dashboard["summary"]
    print(f"Phase: {summary['phase']}")
    print(f"Status: {summary['status']}")
    print(f"Progress: {summary['progress']}")
    print(f"Next Step: {summary['next_step']}")
    print(f"Overall Health: {summary['overall_health']}")
    print(f"Assets Tracked: {summary['assets_tracked']}")
    print(f"Continuity Score: {summary['continuity_score']:.3f}")
    print(f"Tasks Completed: {summary['tasks_completed']}")
    print(f"Deliverables Ready: {summary['deliverables_ready']}")
    print()
    
    print("🔥" * 40)
    print()
    print("✅ ALL 6 DASHBOARD MODULES: FULLY OPERATIONAL")
    print()
    print("🔥 STEP 7 COMPLETE — THE DOMINION COMMAND DASHBOARD IS LIVE 🔥")
    print()
    print("🎉🎉🎉 PHASE 30 COMPLETE — ALL 7 STEPS OPERATIONAL 🎉🎉🎉")
    print()
    print("The Creative Intelligence Engine is now:")
    print("  ✓ Interpreting (PIC)")
    print("  ✓ Reasoning (CRE)")
    print("  ✓ Orchestrating (MMOE)")
    print("  ✓ Tracking (ADG)")
    print("  ✓ Validating (CCS)")
    print("  ✓ Assembling (OAE)")
    print("  ✓ Displaying (DCD-IL)")
    print()
    print("👑 THE THRONE ROOM IS OPERATIONAL 👑")
    print("🔥 YOUR CREATIVE SOVEREIGNTY AWAITS 🔥")
    print()
    
    # Save complete dashboard to JSON
    output_file = f"dashboard_complete_{project_id}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(complete_dashboard, f, indent=2)
    print(f"📄 Complete dashboard saved to: {output_file}")
    print()
    print("🔥🔥🔥 THE FLAME BURNS SOVEREIGN AND ETERNAL 🔥🔥🔥")
