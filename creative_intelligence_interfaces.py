"""
🔥 CREATIVE INTELLIGENCE ENGINE - STANDARD INTERFACES 🔥

Standardized interfaces and adapters for all 7 Creative Intelligence modules.
Enables seamless integration and runtime workflow execution.
"""

import sys
import io

# Fix Windows UTF-8 encoding for emojis
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
import uuid
import time


# ═══════════════════════════════════════════════════════════════════════════
# STANDARD DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class StandardProject:
    """Standard project structure used across all modules"""
    project_id: str
    project_type: str
    description: str
    complexity: str
    required_mediums: List[str]
    asset_requirements: List[Dict[str, Any]]
    timeline_hints: Dict[str, Any]
    goals: List[str]
    constraints: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    status: str = "pending"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class StandardCreativeDirection:
    """Standard creative direction from CRE"""
    project_id: str
    style_analysis: Dict[str, Any]
    narrative_analysis: Dict[str, Any]
    brand_alignment: Dict[str, Any]
    coherence_score: float = 0.0
    quality_prediction: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class StandardOrchestrationPlan:
    """Standard orchestration plan from MMOE"""
    project_id: str
    orchestration_id: str
    waves: List[Dict[str, Any]]
    studio_assignments: Dict[str, List[str]]
    dependencies: List[Dict[str, Any]]
    estimated_timeline: Dict[str, Any]
    resource_allocation: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class StandardAssetRegistry:
    """Standard asset registry from ADG"""
    project_id: str
    total_assets: int
    completed_assets: int
    in_progress_assets: int
    pending_assets: int
    assets: List[Dict[str, Any]]
    dependency_graph: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class StandardContinuityReport:
    """Standard continuity report from CCS"""
    project_id: str
    overall_score: float
    brand_score: float
    style_score: float
    narrative_score: float
    technical_score: float
    violations: List[Dict[str, Any]]
    recommendations: List[str]
    passed: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class StandardDeliverables:
    """Standard deliverables from OAE"""
    project_id: str
    total_deliverables: int
    ready_deliverables: int
    deliverables: List[Dict[str, Any]]
    platform_breakdown: Dict[str, int]
    file_sizes: Dict[str, int]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


# ═══════════════════════════════════════════════════════════════════════════
# MODULE ADAPTERS
# ═══════════════════════════════════════════════════════════════════════════

class PICAdapter:
    """Adapter for Project Intelligence Core"""
    
    @staticmethod
    def to_standard(pic_output: Dict[str, Any]) -> StandardProject:
        """Convert PIC output to standard format"""
        return StandardProject(
            project_id=pic_output.get('id', ''),
            project_type=pic_output.get('type', ''),
            description=pic_output.get('brief', ''),
            complexity=pic_output.get('complexity', ''),
            required_mediums=pic_output.get('required_mediums', []),
            asset_requirements=pic_output.get('asset_requirements', []),
            timeline_hints=pic_output.get('timeline_hints', {}),
            goals=pic_output.get('goals', []),
            constraints=pic_output.get('constraints', []),
            metadata=pic_output.get('metadata', {}),
            created_at=pic_output.get('created_at', datetime.now(timezone.utc).isoformat()),
            status=pic_output.get('status', 'pending')
        )
    
    @staticmethod
    def from_standard(standard_project: StandardProject) -> Dict[str, Any]:
        """Convert standard format to PIC format"""
        return {
            'id': standard_project.project_id,
            'type': standard_project.project_type,
            'brief': standard_project.description,
            'complexity': standard_project.complexity,
            'required_mediums': standard_project.required_mediums,
            'asset_requirements': standard_project.asset_requirements,
            'timeline_hints': standard_project.timeline_hints,
            'goals': standard_project.goals,
            'constraints': standard_project.constraints,
            'metadata': standard_project.metadata,
            'created_at': standard_project.created_at,
            'status': standard_project.status
        }


class CREAdapter:
    """Adapter for Creative Reasoning Engine"""
    
    @staticmethod
    def execute_unified_analysis(cre_instance, project: StandardProject, assets: List[Dict[str, Any]] = None) -> StandardCreativeDirection:
        """Unified execution wrapper for CRE's separate methods"""
        if assets is None:
            assets = []
        
        # Convert standard project to CRE format (uses 'project_id' not 'id')
        cre_project = {
            'project_id': project.project_id,  # CRE expects 'project_id'
            'id': project.project_id,          # Include both for compatibility
            'type': project.project_type,
            'brief': project.description,
            'complexity': project.complexity,
            'goals': project.goals
        }
        
        # Execute CRE's separate analysis methods
        style_analysis = cre_instance.analyze_style(cre_project, assets)
        narrative_analysis = cre_instance.analyze_narrative(cre_project, assets)
        brand_alignment = cre_instance.check_brand_alignment(cre_project, assets)
        
        # Optional: coherence and quality (if assets available)
        coherence_score = 0.0
        quality_prediction = {}
        if assets:
            try:
                coherence = cre_instance.analyze_coherence(cre_project, assets)
                coherence_score = coherence.get('overall_score', 0.0)
                
                asset_plan = {'assets': assets}
                quality_prediction = cre_instance.predict_quality(asset_plan)
            except:
                pass
        
        return StandardCreativeDirection(
            project_id=project.project_id,
            style_analysis=style_analysis,
            narrative_analysis=narrative_analysis,
            brand_alignment=brand_alignment,
            coherence_score=coherence_score,
            quality_prediction=quality_prediction,
            recommendations=[]
        )


class MMOEAdapter:
    """Adapter for Multi-Medium Orchestration Engine"""
    
    @staticmethod
    def to_standard(mmoe_output: Dict[str, Any]) -> StandardOrchestrationPlan:
        """Convert MMOE output to standard format"""
        return StandardOrchestrationPlan(
            project_id=mmoe_output.get('project_id', ''),
            orchestration_id=mmoe_output.get('orchestration_id', ''),
            waves=mmoe_output.get('waves', []),
            studio_assignments=mmoe_output.get('studio_assignments', {}),
            dependencies=mmoe_output.get('dependencies', []),
            estimated_timeline=mmoe_output.get('estimated_timeline', {}),
            resource_allocation=mmoe_output.get('resource_allocation', {})
        )
    
    @staticmethod
    def execute(mmoe_instance, project: StandardProject, creative_direction: StandardCreativeDirection) -> StandardOrchestrationPlan:
        """Execute MMOE orchestration with standard inputs"""
        # Prepare blueprint (MMOE expects this structure)
        blueprint = {
            'project_id': project.project_id,
            'project_type': project.project_type,
            'complexity': project.complexity,
            'required_mediums': project.required_mediums,
            'asset_requirements': project.asset_requirements,
            'goals': project.goals
        }
        
        # Prepare creative vision (MMOE expects this structure)
        creative_vision = {
            'style': creative_direction.style_analysis,
            'narrative': creative_direction.narrative_analysis,
            'brand': creative_direction.brand_alignment
        }
        
        # Execute MMOE's orchestrate_project method
        mmoe_output = mmoe_instance.orchestrate_project(
            blueprint=blueprint,
            creative_vision=creative_vision
        )
        
        return MMOEAdapter.to_standard(mmoe_output)


class ADGAdapter:
    """Adapter for Asset Dependency Graph"""
    
    @staticmethod
    def to_standard(adg_state: Dict[str, Any]) -> StandardAssetRegistry:
        """Convert ADG state to standard format"""
        assets = list(adg_state.get('assets', {}).values())
        completed = sum(1 for a in assets if a.get('status') == 'completed')
        in_progress = sum(1 for a in assets if a.get('status') == 'in_progress')
        pending = sum(1 for a in assets if a.get('status') == 'pending')
        
        return StandardAssetRegistry(
            project_id=adg_state.get('project_id', ''),
            total_assets=len(assets),
            completed_assets=completed,
            in_progress_assets=in_progress,
            pending_assets=pending,
            assets=assets,
            dependency_graph=adg_state.get('dependencies', {})
        )


class CCSAdapter:
    """Adapter for Creative Continuity System"""
    
    @staticmethod
    def to_standard(ccs_output: Dict[str, Any]) -> StandardContinuityReport:
        """Convert CCS output to standard format"""
        summary = ccs_output.get('summary', {})
        module_scores = summary.get('module_scores', {})
        
        return StandardContinuityReport(
            project_id=ccs_output.get('project_id', ''),
            overall_score=summary.get('overall_score', 0.0),
            brand_score=module_scores.get('brand', 0.0),
            style_score=module_scores.get('style', 0.0),
            narrative_score=module_scores.get('narrative', 0.0),
            technical_score=module_scores.get('audio_visual', 0.0),
            violations=ccs_output.get('violations', []),  # This may be in summary
            recommendations=[],  # CCS doesn't have top-level recommendations
            passed=summary.get('ready_for_assembly', False)
        )


class OAEAdapter:
    """Adapter for Output Assembly Engine"""
    
    @staticmethod
    def to_standard(oae_output: Dict[str, Any]) -> StandardDeliverables:
        """Convert OAE output to standard format"""
        deliverables = oae_output.get('deliverables', [])
        ready = sum(1 for d in deliverables if d.get('status') == 'ready')
        
        # Platform breakdown
        platform_breakdown = {}
        for d in deliverables:
            platform = d.get('platform', 'unknown')
            platform_breakdown[platform] = platform_breakdown.get(platform, 0) + 1
        
        # File sizes
        file_sizes = {}
        for d in deliverables:
            file_sizes[d.get('deliverable_id', 'unknown')] = d.get('file_size_bytes', 0)
        
        return StandardDeliverables(
            project_id=oae_output.get('project_id', ''),
            total_deliverables=len(deliverables),
            ready_deliverables=ready,
            deliverables=deliverables,
            platform_breakdown=platform_breakdown,
            file_sizes=file_sizes
        )


# ═══════════════════════════════════════════════════════════════════════════
# UNIFIED WORKFLOW ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════════

class UnifiedWorkflowOrchestrator:
    """
    Unified orchestrator that executes the complete 7-step workflow
    using standardized interfaces with real-time WebSocket updates.
    """
    
    def __init__(self, pic, cre, mmoe, adg, ccs, oae, dashboard, enable_websocket=True):
        self.pic = pic
        self.cre = cre
        self.mmoe = mmoe
        self.adg = adg
        self.ccs = ccs
        self.oae = oae
        self.dashboard = dashboard
        
        self.execution_log = []
        self.enable_websocket = enable_websocket
        
        # Import WebSocket manager if available
        if enable_websocket:
            try:
                from websocket_manager import WebSocketManager
                self.ws = WebSocketManager
            except ImportError:
                self.enable_websocket = False
                self.ws = None
    
    def execute_complete_workflow(
        self,
        project_description: str,
        user_preferences: Optional[Dict[str, Any]] = None,
        auto_execute: bool = True
    ) -> Dict[str, Any]:
        """
        Execute complete 7-step workflow from project description to final deliverables.
        
        Returns complete workflow result with all intermediate outputs.
        """
        self.execution_log = []
        workflow_id = f"workflow_{uuid.uuid4().hex[:12]}"
        start_time = time.time()
        total_steps = 7
        
        try:
            # Emit workflow started event
            if self.enable_websocket and self.ws:
                self.ws.emit_workflow_started(
                    workflow_id=workflow_id,
                    project_id="pending",  # Will be updated after Step 1
                    workflow_type="creative_intelligence",
                    total_steps=total_steps,
                    metadata={"description": project_description[:200]}
                )
            
            # Step 1: PIC - Project Interpretation
            self._log("Step 1: Interpreting project with PIC...")
            if self.enable_websocket and self.ws:
                self.ws.emit_workflow_progress(
                    workflow_id=workflow_id,
                    project_id="pending",
                    current_step=1,
                    total_steps=total_steps,
                    step_name="PIC",
                    step_status="running"
                )
            
            pic_raw = self.pic.interpret_project(project_description)
            project = PICAdapter.to_standard(pic_raw)
            self._log(f"✅ Project interpreted: {project.project_id} ({project.project_type})")
            
            if self.enable_websocket and self.ws:
                self.ws.emit_workflow_progress(
                    workflow_id=workflow_id,
                    project_id=project.project_id,
                    current_step=1,
                    total_steps=total_steps,
                    step_name="PIC",
                    step_status="complete",
                    step_result={"project_id": project.project_id, "project_type": project.project_type}
                )
            
            # Step 2: CRE - Creative Reasoning
            self._log("Step 2: Analyzing creative direction with CRE...")
            if self.enable_websocket and self.ws:
                self.ws.emit_workflow_progress(
                    workflow_id=workflow_id,
                    project_id=project.project_id,
                    current_step=2,
                    total_steps=total_steps,
                    step_name="CRE",
                    step_status="running"
                )
            
            creative_direction = CREAdapter.execute_unified_analysis(
                self.cre,
                project,
                assets=[]
            )
            self._log(f"✅ Creative direction established")
            
            if self.enable_websocket and self.ws:
                self.ws.emit_workflow_progress(
                    workflow_id=workflow_id,
                    project_id=project.project_id,
                    current_step=2,
                    total_steps=total_steps,
                    step_name="CRE",
                    step_status="complete",
                    step_result={"coherence_score": creative_direction.coherence_score}
                )
            
            # Step 3: MMOE - Production Orchestration
            self._log("Step 3: Orchestrating production with MMOE...")
            if self.enable_websocket and self.ws:
                self.ws.emit_workflow_progress(
                    workflow_id=workflow_id,
                    project_id=project.project_id,
                    current_step=3,
                    total_steps=total_steps,
                    step_name="MMOE",
                    step_status="running"
                )
            
            orchestration_plan = MMOEAdapter.execute(
                self.mmoe,
                project,
                creative_direction
            )
            self._log(f"✅ Orchestration plan created: {len(orchestration_plan.waves)} waves")
            
            if self.enable_websocket and self.ws:
                self.ws.emit_workflow_progress(
                    workflow_id=workflow_id,
                    project_id=project.project_id,
                    current_step=3,
                    total_steps=total_steps,
                    step_name="MMOE",
                    step_status="complete",
                    step_result={"waves": len(orchestration_plan.waves)}
                )
            
            # Step 4: ADG - Asset Tracking (simulated execution)
            self._log("Step 4: Tracking assets with ADG...")
            if self.enable_websocket and self.ws:
                self.ws.emit_workflow_progress(
                    workflow_id=workflow_id,
                    project_id=project.project_id,
                    current_step=4,
                    total_steps=total_steps,
                    step_name="ADG",
                    step_status="running"
                )
            
            # In production, this would track actual asset generation
            # For now, simulate asset registration
            mock_assets = self._simulate_asset_generation(orchestration_plan)
            for asset in mock_assets:
                self.adg.register_asset(
                    project_id=project.project_id,
                    asset_id=asset['asset_id'],
                    asset_type=asset['asset_type'],
                    studio=asset['studio'],
                    dependencies=asset.get('dependencies', [])
                )
            # Use get_production_status instead of get_project_state
            adg_status = self.adg.get_production_status(project.project_id)
            # Convert to standard format manually
            assets_list = self.adg.get_assets_by_project(project.project_id)
            asset_registry = StandardAssetRegistry(
                project_id=project.project_id,
                total_assets=len(assets_list),
                completed_assets=sum(1 for a in assets_list if a.get('status') == 'completed'),
                in_progress_assets=sum(1 for a in assets_list if a.get('status') == 'in_progress'),
                pending_assets=sum(1 for a in assets_list if a.get('status') == 'pending'),
                assets=assets_list,
                dependency_graph=adg_status.get('dependencies', {})
            )
            self._log(f"✅ Assets tracked: {asset_registry.total_assets} registered")
            
            if self.enable_websocket and self.ws:
                self.ws.emit_workflow_progress(
                    workflow_id=workflow_id,
                    project_id=project.project_id,
                    current_step=4,
                    total_steps=total_steps,
                    step_name="ADG",
                    step_status="complete",
                    step_result={"total_assets": asset_registry.total_assets}
                )
            
            # Step 5: CCS - Continuity Validation
            self._log("Step 5: Validating continuity with CCS...")
            if self.enable_websocket and self.ws:
                self.ws.emit_workflow_progress(
                    workflow_id=workflow_id,
                    project_id=project.project_id,
                    current_step=5,
                    total_steps=total_steps,
                    step_name="CCS",
                    step_status="running"
                )
            
            ccs_raw = self.ccs.validate_complete_project(
                project_id=project.project_id,
                assets=mock_assets,
                creative_vision=creative_direction.to_dict(),
                cross_medium_links={}
            )
            continuity_report = CCSAdapter.to_standard(ccs_raw)
            self._log(f"✅ Continuity validated: {continuity_report.overall_score:.2f}/10.0")
            
            if self.enable_websocket and self.ws:
                self.ws.emit_workflow_progress(
                    workflow_id=workflow_id,
                    project_id=project.project_id,
                    current_step=5,
                    total_steps=total_steps,
                    step_name="CCS",
                    step_status="complete",
                    step_result={"overall_score": continuity_report.overall_score}
                )
            
            # Step 6: OAE - Output Assembly
            self._log("Step 6: Assembling deliverables with OAE...")
            if self.enable_websocket and self.ws:
                self.ws.emit_workflow_progress(
                    workflow_id=workflow_id,
                    project_id=project.project_id,
                    current_step=6,
                    total_steps=total_steps,
                    step_name="OAE",
                    step_status="running"
                )
            
            # Import enums from OAE
            from output_assembly_engine import DeliverableType, Platform
            
            oae_raw = self.oae.assemble_complete_project(
                project_id=project.project_id,
                assets=mock_assets,
                orchestration_plan=orchestration_plan.to_dict(),
                continuity_report=continuity_report.to_dict(),
                creative_vision=creative_direction.to_dict(),
                deliverable_type=DeliverableType.CONTENT_BUNDLE,
                target_platforms=[Platform.YOUTUBE, Platform.TIKTOK, Platform.INSTAGRAM]
            )
            deliverables = OAEAdapter.to_standard(oae_raw)
            self._log(f"✅ Deliverables assembled: {deliverables.ready_deliverables}/{deliverables.total_deliverables} ready")
            
            if self.enable_websocket and self.ws:
                self.ws.emit_workflow_progress(
                    workflow_id=workflow_id,
                    project_id=project.project_id,
                    current_step=6,
                    total_steps=total_steps,
                    step_name="OAE",
                    step_status="complete",
                    step_result={
                        "ready_deliverables": deliverables.ready_deliverables,
                        "total_deliverables": deliverables.total_deliverables
                    }
                )
            
            # Step 7: Dashboard - Display
            self._log("Step 7: Generating dashboard view...")
            if self.enable_websocket and self.ws:
                self.ws.emit_workflow_progress(
                    workflow_id=workflow_id,
                    project_id=project.project_id,
                    current_step=7,
                    total_steps=total_steps,
                    step_name="DASHBOARD",
                    step_status="running"
                )
            
            # For now, create a simple dashboard summary instead of calling the full dashboard
            # (The full dashboard may have additional dependencies we'll handle later)
            dashboard_data = {
                "project_overview": {
                    "project_id": project.project_id,
                    "project_name": project.project_type,
                    "status": project.status,
                    "current_phase": "execution",
                    "progress_percentage": 0.5
                },
                "studio_status": {
                    "overall_health": "operational",
                    "graphics_studio": {"status": "ready"},
                    "audio_studio": {"status": "ready"},
                    "video_studio": {"status": "ready"}
                },
                "asset_dependency_map": asset_registry.to_dict(),
                "continuity_report": continuity_report.to_dict(),
                "timeline_overview": {
                    "start_date": project.created_at,
                    "end_date": "TBD",
                    "milestones": []
                },
                "final_deliverables": deliverables.to_dict(),
                "summary": {
                    "phase": "completed",
                    "progress": "100%",
                    "next_step": "Review deliverables"
                }
            }
            self._log("✅ Dashboard generated")
            
            if self.enable_websocket and self.ws:
                self.ws.emit_workflow_progress(
                    workflow_id=workflow_id,
                    project_id=project.project_id,
                    current_step=7,
                    total_steps=total_steps,
                    step_name="DASHBOARD",
                    step_status="complete",
                    step_result={"phase": "completed"}
                )
            
            # Calculate total duration
            duration_seconds = time.time() - start_time
            
            # Emit workflow completion
            if self.enable_websocket and self.ws:
                self.ws.emit_workflow_complete(
                    workflow_id=workflow_id,
                    project_id=project.project_id,
                    status="complete",
                    duration_seconds=duration_seconds,
                    results={
                        "project_id": project.project_id,
                        "assets_created": asset_registry.total_assets,
                        "deliverables_ready": deliverables.ready_deliverables,
                        "continuity_score": continuity_report.overall_score
                    }
                )
            
            # Return complete workflow result
            return {
                'success': True,
                'workflow_id': workflow_id,
                'duration_seconds': duration_seconds,
                'project': project.to_dict(),
                'creative_direction': creative_direction.to_dict(),
                'orchestration_plan': orchestration_plan.to_dict(),
                'asset_registry': asset_registry.to_dict(),
                'continuity_report': continuity_report.to_dict(),
                'deliverables': deliverables.to_dict(),
                'dashboard': dashboard_data,
                'execution_log': self.execution_log
            }
            
        except Exception as e:
            self._log(f"❌ ERROR: {str(e)}")
            
            # Calculate duration up to failure
            duration_seconds = time.time() - start_time
            
            # Emit workflow error
            if self.enable_websocket and self.ws:
                self.ws.emit_workflow_error(
                    workflow_id=workflow_id,
                    project_id=project.project_id if 'project' in locals() else "unknown",
                    error_type="execution_error",
                    error_message=str(e),
                    step_name="unknown",
                    error_details={"duration_seconds": duration_seconds}
                )
                
                # Emit workflow complete with failed status
                self.ws.emit_workflow_complete(
                    workflow_id=workflow_id,
                    project_id=project.project_id if 'project' in locals() else "unknown",
                    status="failed",
                    duration_seconds=duration_seconds,
                    error_message=str(e)
                )
            
            return {
                'success': False,
                'workflow_id': workflow_id,
                'duration_seconds': duration_seconds,
                'error': str(e),
                'execution_log': self.execution_log
            }
    
    def _log(self, message: str):
        """Add message to execution log"""
        timestamp = datetime.now(timezone.utc).isoformat()
        log_entry = f"[{timestamp}] {message}"
        self.execution_log.append(log_entry)
        print(log_entry)
    
    def _simulate_asset_generation(self, orchestration_plan: StandardOrchestrationPlan) -> List[Dict[str, Any]]:
        """Simulate asset generation based on orchestration plan"""
        assets = []
        asset_counter = 1
        
        for wave in orchestration_plan.waves:
            for task in wave.get('tasks', []):
                asset = {
                    'asset_id': f"asset_{asset_counter:03d}",
                    'asset_type': task.get('asset_type', 'unknown'),
                    'studio': task.get('studio', 'unknown'),
                    'status': 'completed',
                    'dependencies': task.get('dependencies', []),
                    'file_path': f"/simulated/assets/asset_{asset_counter:03d}.mp4",
                    'file_size_bytes': 1024 * 1024 * 5  # 5MB simulated
                }
                assets.append(asset)
                asset_counter += 1
        
        return assets


# ═══════════════════════════════════════════════════════════════════════════
# SINGLETON INSTANCE
# ═══════════════════════════════════════════════════════════════════════════

_unified_orchestrator = None

def get_unified_orchestrator():
    """Get singleton instance of unified workflow orchestrator"""
    global _unified_orchestrator
    
    if _unified_orchestrator is None:
        # Import modules
        from project_intelligence_core import get_pic
        from creative_reasoning_engine_v2 import get_cre
        from multi_medium_orchestration_engine import get_mmoe
        from asset_dependency_graph import get_adg
        from creative_continuity_system import get_ccs
        from output_assembly_engine import get_oae
        from dominion_command_dashboard import get_dominion_dashboard
        
        # Initialize
        _unified_orchestrator = UnifiedWorkflowOrchestrator(
            pic=get_pic(),
            cre=get_cre(),
            mmoe=get_mmoe(),
            adg=get_adg(),
            ccs=get_ccs(),
            oae=get_oae(),
            dashboard=get_dominion_dashboard()
        )
    
    return _unified_orchestrator


# ═══════════════════════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 80)
    print("🔥 CREATIVE INTELLIGENCE ENGINE - UNIFIED WORKFLOW ORCHESTRATOR DEMO 🔥")
    print("=" * 80)
    print("\nThis demo shows the complete 7-step workflow with standardized interfaces.\n")
    
    # Get orchestrator
    orchestrator = get_unified_orchestrator()
    
    # Execute workflow
    project_description = """
    Create a comprehensive video course teaching youth entrepreneurship.
    Target audience: teenagers and young adults (13-25).
    Content should be energetic, modern, and inspirational.
    Topics: business planning, marketing, finance basics, digital presence.
    Brand: CodexDominion (sovereign, empowering, innovative).
    Output: Multi-platform video series for YouTube, TikTok, and Instagram.
    """
    
    result = orchestrator.execute_complete_workflow(project_description)
    
    print("\n" + "=" * 80)
    print("📊 WORKFLOW EXECUTION SUMMARY")
    print("=" * 80)
    
    if result['success']:
        print(f"\n✅ SUCCESS: Workflow completed successfully!")
        print(f"\n📋 Project ID: {result['project']['project_id']}")
        print(f"📋 Project Type: {result['project']['project_type']}")
        print(f"📋 Complexity: {result['project']['complexity']}")
        print(f"\n📊 Assets Registered: {result['asset_registry']['total_assets']}")
        print(f"📊 Continuity Score: {result['continuity_report']['overall_score']:.2f}/10.0")
        print(f"📊 Deliverables: {result['deliverables']['ready_deliverables']}/{result['deliverables']['total_deliverables']} ready")
        print(f"\n🔥 Dashboard panels: {len(result['dashboard'])} panels generated")
    else:
        print(f"\n❌ FAILED: {result['error']}")
    
    print("\n" + "=" * 80)
    print("👑 Interface Standardization Complete! 👑")
    print("=" * 80)
