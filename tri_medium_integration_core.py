"""
🔥 CODEX DOMINION - TRI-MEDIUM INTEGRATION CORE 🔥
====================================================
Unified integration layer for Graphics, Audio, and Video mediums

This core system enables:
- Cross-medium project synchronization
- Unified asset management across all three mediums
- Intelligent medium selection and routing
- Integrated workflow orchestration
- Real-time status tracking across mediums

Architecture:
    Graphics (Cluster Workflow) ←→ Tri-Medium Core ←→ Audio (Service Layer)
                                        ↕
                                   Video (Tiered)

Author: Codex Dominion High Council
Last Updated: December 23, 2025
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from enum import Enum
import uuid

# Import existing medium engines
try:
    from graphics_cluster_workflow import GraphicsClusterWorkflow
    GRAPHICS_AVAILABLE = True
except ImportError:
    GRAPHICS_AVAILABLE = False
    logging.warning("⚠️ Graphics engine not available")

try:
    from audio_service_layer import AudioServiceLayer
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    logging.warning("⚠️ Audio engine not available")

try:
    from video_tier_system import VideoTierSystem
    VIDEO_AVAILABLE = True
except ImportError:
    VIDEO_AVAILABLE = False
    logging.warning("⚠️ Video engine not available")

# Import cross-medium components
try:
    from cross_medium_evolution import CrossMediumEvolution
    from unified_constellation import UnifiedConstellation
    from master_project_timeline import MasterProjectTimeline
    INTEGRATION_COMPONENTS_AVAILABLE = True
except ImportError:
    INTEGRATION_COMPONENTS_AVAILABLE = False
    logging.warning("⚠️ Integration components not fully available")


class MediumType(Enum):
    """Available medium types"""
    GRAPHICS = "graphics"
    AUDIO = "audio"
    VIDEO = "video"
    HYBRID = "hybrid"  # Multi-medium project


class IntegrationMode(Enum):
    """Integration operation modes"""
    SEQUENTIAL = "sequential"  # One medium after another
    PARALLEL = "parallel"      # All mediums simultaneously
    ADAPTIVE = "adaptive"      # AI-driven medium selection
    CUSTOM = "custom"          # User-defined workflow


class ProjectPriority(Enum):
    """Project priority levels"""
    URGENT = "urgent"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TriMediumIntegrationCore:
    """
    🔥 Central integration system for all three creative mediums 🔥
    
    Responsibilities:
    - Coordinate projects across Graphics, Audio, Video
    - Manage cross-medium asset dependencies
    - Provide unified API for all medium operations
    - Track project status across mediums
    - Enable seamless medium transitions
    
    Usage:
        core = TriMediumIntegrationCore()
        project_id = core.create_integrated_project(
            name="Marketing Campaign 2025",
            mediums=["graphics", "audio", "video"],
            mode=IntegrationMode.PARALLEL
        )
        status = core.get_project_status(project_id)
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize Tri-Medium Integration Core
        
        Args:
            config_path: Optional path to configuration file
        """
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config(config_path)
        
        # Initialize medium engines
        self.graphics_engine = GraphicsClusterWorkflow() if GRAPHICS_AVAILABLE else None
        self.audio_engine = AudioServiceLayer() if AUDIO_AVAILABLE else None
        self.video_engine = VideoTierSystem() if VIDEO_AVAILABLE else None
        
        # Initialize integration components
        if INTEGRATION_COMPONENTS_AVAILABLE:
            self.evolution_engine = CrossMediumEvolution()
            self.constellation = UnifiedConstellation()
            self.timeline = MasterProjectTimeline()
        else:
            self.evolution_engine = None
            self.constellation = None
            self.timeline = None
        
        # Project tracking
        self.active_projects: Dict[str, Dict[str, Any]] = {}
        self.project_history: List[Dict[str, Any]] = []
        
        # Load persisted state
        self._load_state()
        
        self.logger.info("🔥 Tri-Medium Integration Core initialized successfully! 👑")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        default_config = {
            "graphics": {
                "enabled": GRAPHICS_AVAILABLE,
                "max_concurrent_projects": 5,
                "default_cluster": "social_media"
            },
            "audio": {
                "enabled": AUDIO_AVAILABLE,
                "max_concurrent_projects": 3,
                "default_service": "podcast_production"
            },
            "video": {
                "enabled": VIDEO_AVAILABLE,
                "max_concurrent_projects": 2,
                "default_tier": "standard"
            },
            "integration": {
                "auto_sync": True,
                "sync_interval_seconds": 60,
                "enable_cross_medium_assets": True,
                "enable_intelligent_routing": True
            },
            "storage": {
                "state_file": "tri_medium_state.json",
                "asset_cache_dir": "assets/integrated/",
                "max_cache_size_mb": 5000
            }
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                # Merge with defaults
                default_config.update(user_config)
            except Exception as e:
                self.logger.warning(f"⚠️ Could not load config from {config_path}: {e}")
        
        return default_config
    
    def _load_state(self):
        """Load persisted project state"""
        state_file = self.config["storage"]["state_file"]
        if Path(state_file).exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    self.active_projects = state.get("active_projects", {})
                    self.project_history = state.get("project_history", [])
                self.logger.info(f"✅ Loaded {len(self.active_projects)} active projects")
            except Exception as e:
                self.logger.error(f"❌ Failed to load state: {e}")
    
    def _save_state(self):
        """Persist current project state"""
        state_file = self.config["storage"]["state_file"]
        try:
            state = {
                "active_projects": self.active_projects,
                "project_history": self.project_history,
                "last_updated": datetime.utcnow().isoformat() + "Z"
            }
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
            self.logger.debug(f"💾 State saved to {state_file}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save state: {e}")
    
    def create_integrated_project(
        self,
        name: str,
        mediums: List[str],
        mode: IntegrationMode = IntegrationMode.SEQUENTIAL,
        priority: ProjectPriority = ProjectPriority.MEDIUM,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new integrated project spanning multiple mediums
        
        Args:
            name: Project name
            mediums: List of mediums to use ["graphics", "audio", "video"]
            mode: Integration mode (sequential, parallel, adaptive, custom)
            priority: Project priority level
            metadata: Additional project metadata
        
        Returns:
            project_id: Unique project identifier
        
        Example:
            >>> project_id = core.create_integrated_project(
            ...     name="Product Launch Campaign",
            ...     mediums=["graphics", "video"],
            ...     mode=IntegrationMode.PARALLEL,
            ...     priority=ProjectPriority.HIGH
            ... )
        """
        project_id = f"tri_medium_{uuid.uuid4().hex[:12]}"
        
        # Validate mediums
        valid_mediums = []
        for medium in mediums:
            medium_lower = medium.lower()
            if medium_lower == "graphics" and self.graphics_engine:
                valid_mediums.append("graphics")
            elif medium_lower == "audio" and self.audio_engine:
                valid_mediums.append("audio")
            elif medium_lower == "video" and self.video_engine:
                valid_mediums.append("video")
            else:
                self.logger.warning(f"⚠️ Medium '{medium}' not available or invalid")
        
        if not valid_mediums:
            raise ValueError("No valid mediums available for project")
        
        # Create project structure
        project = {
            "id": project_id,
            "name": name,
            "mediums": valid_mediums,
            "mode": mode.value,
            "priority": priority.value,
            "status": "created",
            "created_at": datetime.utcnow().isoformat() + "Z",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "metadata": metadata or {},
            "medium_tasks": {},
            "dependencies": [],
            "completion_percentage": 0
        }
        
        # Initialize tasks for each medium
        for medium in valid_mediums:
            project["medium_tasks"][medium] = {
                "status": "pending",
                "task_id": None,
                "progress": 0,
                "errors": []
            }
        
        self.active_projects[project_id] = project
        self._save_state()
        
        self.logger.info(f"🔥 Created integrated project '{name}' (ID: {project_id}) with mediums: {valid_mediums}")
        
        # Register with constellation if available
        if self.constellation:
            self.constellation.register_project(project_id, valid_mediums)
        
        return project_id
    
    def execute_project(self, project_id: str) -> Dict[str, Any]:
        """
        Execute an integrated project across all specified mediums
        
        Args:
            project_id: Project identifier
        
        Returns:
            Execution status for each medium
        """
        if project_id not in self.active_projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.active_projects[project_id]
        mode = IntegrationMode(project["mode"])
        
        self.logger.info(f"🚀 Executing project {project_id} in {mode.value} mode")
        
        project["status"] = "executing"
        project["updated_at"] = datetime.utcnow().isoformat() + "Z"
        
        results = {}
        
        if mode == IntegrationMode.SEQUENTIAL:
            # Execute mediums one after another
            results = self._execute_sequential(project)
        elif mode == IntegrationMode.PARALLEL:
            # Execute all mediums simultaneously
            results = self._execute_parallel(project)
        elif mode == IntegrationMode.ADAPTIVE:
            # AI-driven execution
            results = self._execute_adaptive(project)
        else:
            # Custom execution flow
            results = self._execute_custom(project)
        
        # Update project status
        all_success = all(r.get("status") == "completed" for r in results.values())
        project["status"] = "completed" if all_success else "partial"
        project["completion_percentage"] = self._calculate_completion(results)
        
        self._save_state()
        
        return results
    
    def _execute_sequential(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Execute project mediums sequentially"""
        results = {}
        
        for medium in project["mediums"]:
            self.logger.info(f"📋 Executing {medium} for project {project['id']}")
            
            try:
                if medium == "graphics" and self.graphics_engine:
                    result = self._execute_graphics_task(project)
                elif medium == "audio" and self.audio_engine:
                    result = self._execute_audio_task(project)
                elif medium == "video" and self.video_engine:
                    result = self._execute_video_task(project)
                else:
                    result = {"status": "skipped", "reason": "engine not available"}
                
                results[medium] = result
                project["medium_tasks"][medium] = result
                
            except Exception as e:
                self.logger.error(f"❌ Error executing {medium}: {e}")
                results[medium] = {"status": "error", "error": str(e)}
        
        return results
    
    def _execute_parallel(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Execute project mediums in parallel (simplified synchronous version)"""
        results = {}
        
        # In a real implementation, use threading or asyncio
        # For now, execute sequentially but mark as parallel
        for medium in project["mediums"]:
            self.logger.info(f"🔄 Parallel executing {medium} for project {project['id']}")
            
            try:
                if medium == "graphics" and self.graphics_engine:
                    result = self._execute_graphics_task(project)
                elif medium == "audio" and self.audio_engine:
                    result = self._execute_audio_task(project)
                elif medium == "video" and self.video_engine:
                    result = self._execute_video_task(project)
                else:
                    result = {"status": "skipped", "reason": "engine not available"}
                
                results[medium] = result
                project["medium_tasks"][medium] = result
                
            except Exception as e:
                self.logger.error(f"❌ Error executing {medium}: {e}")
                results[medium] = {"status": "error", "error": str(e)}
        
        return results
    
    def _execute_adaptive(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Execute with AI-driven medium selection"""
        self.logger.info(f"🤖 Adaptive execution for project {project['id']}")
        
        # Use evolution engine to determine optimal medium order
        if self.evolution_engine:
            optimal_order = self.evolution_engine.suggest_medium_order(project)
            project["mediums"] = optimal_order
        
        return self._execute_sequential(project)
    
    def _execute_custom(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Execute with custom user-defined workflow"""
        self.logger.info(f"⚙️ Custom execution for project {project['id']}")
        
        # Check if custom workflow is defined in metadata
        custom_workflow = project.get("metadata", {}).get("custom_workflow", [])
        
        if custom_workflow:
            project["mediums"] = custom_workflow
            return self._execute_sequential(project)
        else:
            return self._execute_parallel(project)
    
    def _execute_graphics_task(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Execute graphics medium task"""
        # Placeholder for actual graphics execution
        return {
            "status": "completed",
            "medium": "graphics",
            "task_id": f"gfx_{uuid.uuid4().hex[:8]}",
            "progress": 100,
            "output": "graphics_output.png"
        }
    
    def _execute_audio_task(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Execute audio medium task"""
        # Placeholder for actual audio execution
        return {
            "status": "completed",
            "medium": "audio",
            "task_id": f"aud_{uuid.uuid4().hex[:8]}",
            "progress": 100,
            "output": "audio_output.mp3"
        }
    
    def _execute_video_task(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Execute video medium task"""
        # Placeholder for actual video execution
        return {
            "status": "completed",
            "medium": "video",
            "task_id": f"vid_{uuid.uuid4().hex[:8]}",
            "progress": 100,
            "output": "video_output.mp4"
        }
    
    def _calculate_completion(self, results: Dict[str, Any]) -> int:
        """Calculate overall project completion percentage"""
        if not results:
            return 0
        
        total_progress = sum(r.get("progress", 0) for r in results.values())
        return int(total_progress / len(results))
    
    def get_project_status(self, project_id: str) -> Dict[str, Any]:
        """
        Get detailed status of a project
        
        Args:
            project_id: Project identifier
        
        Returns:
            Complete project status
        """
        if project_id not in self.active_projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.active_projects[project_id]
        
        # Enrich with real-time status if timeline available
        if self.timeline:
            timeline_status = self.timeline.get_project_timeline(project_id)
            project["timeline"] = timeline_status
        
        return project
    
    def list_projects(
        self,
        status_filter: Optional[str] = None,
        medium_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List all projects with optional filtering
        
        Args:
            status_filter: Filter by status (created, executing, completed, partial)
            medium_filter: Filter by medium (graphics, audio, video)
        
        Returns:
            List of projects matching filters
        """
        projects = list(self.active_projects.values())
        
        if status_filter:
            projects = [p for p in projects if p["status"] == status_filter]
        
        if medium_filter:
            projects = [p for p in projects if medium_filter in p["mediums"]]
        
        return projects
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get overall system status across all mediums
        
        Returns:
            System health and capacity metrics
        """
        return {
            "mediums": {
                "graphics": {
                    "available": GRAPHICS_AVAILABLE,
                    "active_projects": len([p for p in self.active_projects.values() if "graphics" in p["mediums"]])
                },
                "audio": {
                    "available": AUDIO_AVAILABLE,
                    "active_projects": len([p for p in self.active_projects.values() if "audio" in p["mediums"]])
                },
                "video": {
                    "available": VIDEO_AVAILABLE,
                    "active_projects": len([p for p in self.active_projects.values() if "video" in p["mediums"]])
                }
            },
            "total_active_projects": len(self.active_projects),
            "integration_components": {
                "evolution_engine": self.evolution_engine is not None,
                "constellation": self.constellation is not None,
                "timeline": self.timeline is not None
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }


# Singleton instance
_tri_medium_core = None

def get_tri_medium_core(config_path: Optional[str] = None) -> TriMediumIntegrationCore:
    """Get or create the singleton Tri-Medium Integration Core instance"""
    global _tri_medium_core
    if _tri_medium_core is None:
        _tri_medium_core = TriMediumIntegrationCore(config_path)
    return _tri_medium_core


if __name__ == "__main__":
    # Demo usage
    logging.basicConfig(level=logging.INFO)
    
    core = get_tri_medium_core()
    
    # Create integrated project
    project_id = core.create_integrated_project(
        name="Holiday Marketing Campaign",
        mediums=["graphics", "audio", "video"],
        mode=IntegrationMode.PARALLEL,
        priority=ProjectPriority.HIGH
    )
    
    print(f"\n🔥 Created project: {project_id}")
    
    # Execute project
    results = core.execute_project(project_id)
    print(f"\n✅ Execution results: {json.dumps(results, indent=2)}")
    
    # Get status
    status = core.get_project_status(project_id)
    print(f"\n📊 Project status: {json.dumps(status, indent=2)}")
    
    # System overview
    system_status = core.get_system_status()
    print(f"\n🌐 System status: {json.dumps(system_status, indent=2)}")
    
    print("\n🔥 Tri-Medium Integration Core demo complete! 👑")
