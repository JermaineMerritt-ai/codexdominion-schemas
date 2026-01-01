"""
🔥 CODEX DOMINION - PROJECT INTELLIGENCE CORE (PIC) 🔥
=======================================================
The Director Brain of the Creative Intelligence Engine

This is the heart of Phase 30 - the system that UNDERSTANDS projects.

Capabilities:
- Project goal interpretation from natural language
- Asset requirement generation across all mediums
- Multi-step creative planning
- Dependency mapping and sequencing
- Cross-medium task breakdown
- Timeline estimation
- Resource allocation planning

The PIC is the "director" - it reads a creative brief and breaks it down
into an executable multi-medium production plan.

Author: Codex Dominion High Council
Phase: 30 - Creative Intelligence Engine
Last Updated: December 23, 2025
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from enum import Enum
import uuid
import re


class ProjectType(Enum):
    """Types of creative projects"""
    MARKETING_CAMPAIGN = "marketing_campaign"
    PRODUCT_LAUNCH = "product_launch"
    SOCIAL_CONTENT = "social_content"
    BRAND_IDENTITY = "brand_identity"
    VIDEO_SERIES = "video_series"
    PODCAST_SERIES = "podcast_series"
    EDUCATIONAL_CONTENT = "educational_content"
    ENTERTAINMENT = "entertainment"
    CUSTOM = "custom"


class ProjectComplexity(Enum):
    """Project complexity levels"""
    SIMPLE = "simple"          # Single medium, few assets
    MODERATE = "moderate"      # 2 mediums, multiple assets
    COMPLEX = "complex"        # All mediums, many assets
    EPIC = "epic"             # Large-scale multi-phase project


class MediumRequirement(Enum):
    """Required creative mediums"""
    GRAPHICS = "graphics"
    AUDIO = "audio"
    VIDEO = "video"
    TEXT = "text"
    ANIMATION = "animation"


class ProjectIntelligenceCore:
    """
    🔥 The Director Brain - Understands and Plans Creative Projects 🔥
    
    The PIC takes a creative brief (natural language or structured) and:
    1. Interprets the project goals
    2. Identifies required assets across all mediums
    3. Creates a multi-step execution plan
    4. Maps dependencies between assets
    5. Sequences tasks across Graphics, Audio, Video studios
    6. Estimates timelines and resource needs
    
    Usage:
        pic = ProjectIntelligenceCore()
        
        # Interpret project from natural language
        project_plan = pic.interpret_project(
            brief="Create a product launch campaign with hero video, "
                  "social media graphics, and podcast announcement",
            project_type=ProjectType.PRODUCT_LAUNCH
        )
        
        # Get detailed execution plan
        execution_plan = pic.generate_execution_plan(project_plan)
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the Project Intelligence Core"""
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config(config_path)
        
        # Intelligence models (simplified - would use actual AI in production)
        self.asset_templates = self._load_asset_templates()
        self.project_patterns = self._load_project_patterns()
        
        # Project registry
        self.projects: Dict[str, Dict[str, Any]] = {}
        self.execution_plans: Dict[str, Dict[str, Any]] = {}
        
        self.logger.info("🔥 Project Intelligence Core initialized! 👑")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load PIC configuration"""
        default_config = {
            "intelligence": {
                "enable_ai_planning": True,
                "enable_dependency_detection": True,
                "enable_timeline_optimization": True
            },
            "complexity_thresholds": {
                "simple": {"max_assets": 5, "max_mediums": 1},
                "moderate": {"max_assets": 15, "max_mediums": 2},
                "complex": {"max_assets": 50, "max_mediums": 3},
                "epic": {"max_assets": 999, "max_mediums": 3}
            },
            "estimation": {
                "graphics_base_hours": 2,
                "audio_base_hours": 3,
                "video_base_hours": 8,
                "complexity_multipliers": {
                    "simple": 1.0,
                    "moderate": 2.0,
                    "complex": 4.0,
                    "epic": 8.0
                }
            }
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                self.logger.warning(f"⚠️ Could not load config: {e}")
        
        return default_config
    
    def _load_asset_templates(self) -> Dict[str, List[str]]:
        """Load templates for common asset types"""
        return {
            "marketing_campaign": [
                "hero_image", "social_media_posts", "email_banner",
                "landing_page_graphics", "promotional_video",
                "background_music", "voiceover"
            ],
            "product_launch": [
                "product_showcase_video", "feature_highlights",
                "comparison_graphics", "demo_video", "launch_announcement",
                "social_teasers", "press_kit_graphics"
            ],
            "social_content": [
                "instagram_posts", "instagram_stories", "facebook_posts",
                "twitter_graphics", "tiktok_video", "youtube_thumbnail"
            ],
            "brand_identity": [
                "logo_variations", "color_palette", "typography_guide",
                "brand_video", "sound_signature", "usage_guidelines"
            ],
            "video_series": [
                "intro_animation", "outro_animation", "episode_thumbnails",
                "background_music", "sound_effects", "episode_videos"
            ],
            "podcast_series": [
                "podcast_intro", "podcast_outro", "episode_audio",
                "cover_art", "social_media_audiograms", "show_notes_graphics"
            ]
        }
    
    def _load_project_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load common project execution patterns"""
        return {
            "sequential": {
                "description": "Complete one medium at a time",
                "order": ["graphics", "audio", "video"],
                "parallelism": False
            },
            "parallel": {
                "description": "All mediums execute simultaneously",
                "order": ["graphics", "audio", "video"],
                "parallelism": True
            },
            "graphics_first": {
                "description": "Graphics → Audio → Video (dependency chain)",
                "order": ["graphics", "audio", "video"],
                "parallelism": False,
                "reason": "Video needs graphics as source material"
            },
            "audio_first": {
                "description": "Audio → Graphics → Video (audio-driven)",
                "order": ["audio", "graphics", "video"],
                "parallelism": False,
                "reason": "Graphics sync to audio beats/voiceover"
            }
        }
    
    def interpret_project(
        self,
        brief: str,
        project_type: Optional[ProjectType] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Interpret a creative project brief and generate initial understanding
        
        Args:
            brief: Natural language project description
            project_type: Type of project (auto-detected if not provided)
            metadata: Additional project metadata
        
        Returns:
            Project understanding with goals, requirements, and complexity
        
        Example:
            >>> pic = ProjectIntelligenceCore()
            >>> project = pic.interpret_project(
            ...     brief="Create a holiday marketing campaign with "
            ...           "Instagram graphics, Facebook ads, and a 30-second promo video",
            ...     project_type=ProjectType.MARKETING_CAMPAIGN
            ... )
            >>> print(project['complexity'])
            'moderate'
        """
        project_id = f"pic_project_{uuid.uuid4().hex[:12]}"
        
        # Auto-detect project type if not provided
        if not project_type:
            project_type = self._detect_project_type(brief)
        
        # Extract key information from brief
        required_mediums = self._extract_mediums(brief)
        asset_requirements = self._extract_asset_requirements(brief, project_type)
        timeline_hints = self._extract_timeline_hints(brief)
        
        # Determine complexity
        complexity = self._determine_complexity(
            len(asset_requirements),
            len(required_mediums)
        )
        
        # Build project understanding
        project = {
            "id": project_id,
            "brief": brief,
            "type": project_type.value,
            "complexity": complexity.value,
            "required_mediums": required_mediums,
            "asset_requirements": asset_requirements,
            "timeline_hints": timeline_hints,
            "goals": self._extract_goals(brief),
            "constraints": self._extract_constraints(brief),
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat() + "Z",
            "status": "interpreted"
        }
        
        # Store project
        self.projects[project_id] = project
        
        self.logger.info(
            f"🔥 Interpreted project {project_id}: "
            f"{project_type.value} ({complexity.value}) "
            f"with {len(required_mediums)} mediums, {len(asset_requirements)} assets"
        )
        
        return project
    
    def _detect_project_type(self, brief: str) -> ProjectType:
        """Auto-detect project type from brief text"""
        brief_lower = brief.lower()
        
        # Pattern matching for project types
        if any(word in brief_lower for word in ["campaign", "marketing", "promotion"]):
            return ProjectType.MARKETING_CAMPAIGN
        elif any(word in brief_lower for word in ["launch", "product", "release"]):
            return ProjectType.PRODUCT_LAUNCH
        elif any(word in brief_lower for word in ["social", "instagram", "tiktok", "facebook"]):
            return ProjectType.SOCIAL_CONTENT
        elif any(word in brief_lower for word in ["brand", "identity", "logo", "rebrand"]):
            return ProjectType.BRAND_IDENTITY
        elif any(word in brief_lower for word in ["video series", "youtube series", "episodes"]):
            return ProjectType.VIDEO_SERIES
        elif any(word in brief_lower for word in ["podcast", "audio series"]):
            return ProjectType.PODCAST_SERIES
        elif any(word in brief_lower for word in ["education", "tutorial", "course"]):
            return ProjectType.EDUCATIONAL_CONTENT
        
        return ProjectType.CUSTOM
    
    def _extract_mediums(self, brief: str) -> List[str]:
        """Extract required creative mediums from brief"""
        brief_lower = brief.lower()
        mediums = []
        
        # Graphics indicators
        if any(word in brief_lower for word in [
            "graphic", "image", "poster", "banner", "logo", "illustration",
            "instagram", "social media", "ad", "design"
        ]):
            mediums.append("graphics")
        
        # Audio indicators
        if any(word in brief_lower for word in [
            "audio", "music", "sound", "voiceover", "podcast", "song",
            "soundtrack", "jingle", "narration"
        ]):
            mediums.append("audio")
        
        # Video indicators
        if any(word in brief_lower for word in [
            "video", "animation", "motion", "film", "commercial", "promo",
            "youtube", "tiktok", "reel", "story"
        ]):
            mediums.append("video")
        
        # Default to graphics if nothing detected
        if not mediums:
            mediums.append("graphics")
        
        return mediums
    
    def _extract_asset_requirements(
        self,
        brief: str,
        project_type: ProjectType
    ) -> List[Dict[str, Any]]:
        """Generate list of required assets based on brief and project type"""
        assets = []
        
        # Start with template assets for this project type
        template_key = project_type.value
        if template_key in self.asset_templates:
            template_assets = self.asset_templates[template_key]
            for asset_name in template_assets:
                assets.append({
                    "name": asset_name,
                    "type": self._infer_asset_medium(asset_name),
                    "priority": "high" if "hero" in asset_name or "main" in asset_name else "medium",
                    "estimated_hours": self._estimate_asset_hours(asset_name),
                    "dependencies": []
                })
        
        # Extract specific asset mentions from brief
        brief_lower = brief.lower()
        
        # Number-based assets (e.g., "5 Instagram posts")
        number_pattern = r'(\d+)\s+([a-z\s]+(?:post|graphic|video|image|ad)s?)'
        matches = re.findall(number_pattern, brief_lower)
        for count, asset_type in matches:
            for i in range(int(count)):
                assets.append({
                    "name": f"{asset_type}_{i+1}",
                    "type": self._infer_asset_medium(asset_type),
                    "priority": "medium",
                    "estimated_hours": 2,
                    "dependencies": []
                })
        
        return assets
    
    def _infer_asset_medium(self, asset_name: str) -> str:
        """Infer the medium type from asset name"""
        asset_lower = asset_name.lower()
        
        if any(word in asset_lower for word in ["video", "animation", "film", "commercial"]):
            return "video"
        elif any(word in asset_lower for word in ["audio", "music", "sound", "podcast", "voiceover"]):
            return "audio"
        else:
            return "graphics"
    
    def _estimate_asset_hours(self, asset_name: str) -> float:
        """Estimate production hours for an asset"""
        asset_lower = asset_name.lower()
        
        # Video assets take longest
        if "video" in asset_lower:
            if "hero" in asset_lower or "main" in asset_lower:
                return 16.0
            return 8.0
        
        # Audio assets are moderate
        elif "audio" in asset_lower or "music" in asset_lower:
            return 4.0
        
        # Graphics are fastest
        else:
            if "hero" in asset_lower or "main" in asset_lower:
                return 4.0
            return 2.0
    
    def _extract_timeline_hints(self, brief: str) -> Dict[str, Any]:
        """Extract timeline information from brief"""
        brief_lower = brief.lower()
        hints = {
            "deadline": None,
            "urgency": "normal",
            "milestones": []
        }
        
        # Urgency indicators
        if any(word in brief_lower for word in ["urgent", "asap", "rush", "immediately"]):
            hints["urgency"] = "urgent"
        elif any(word in brief_lower for word in ["quick", "fast", "soon"]):
            hints["urgency"] = "high"
        
        # Timeline patterns
        if "by" in brief_lower or "before" in brief_lower:
            # Would extract actual dates in production
            hints["deadline"] = "specified"
        
        return hints
    
    def _extract_goals(self, brief: str) -> List[str]:
        """Extract project goals from brief"""
        goals = []
        brief_lower = brief.lower()
        
        # Common goal patterns
        goal_indicators = [
            ("increase", "Increase engagement/awareness"),
            ("launch", "Successfully launch product/service"),
            ("promote", "Promote offering to target audience"),
            ("educate", "Educate audience about topic"),
            ("entertain", "Entertain and engage viewers"),
            ("convert", "Convert audience to customers"),
            ("brand", "Build brand awareness/identity")
        ]
        
        for indicator, goal in goal_indicators:
            if indicator in brief_lower:
                goals.append(goal)
        
        if not goals:
            goals.append("Create high-quality creative content")
        
        return goals
    
    def _extract_constraints(self, brief: str) -> Dict[str, Any]:
        """Extract project constraints from brief"""
        brief_lower = brief.lower()
        
        constraints = {
            "budget": None,
            "timeline": None,
            "style": [],
            "platform": [],
            "restrictions": []
        }
        
        # Platform constraints
        platforms = ["instagram", "facebook", "youtube", "tiktok", "twitter", "linkedin"]
        for platform in platforms:
            if platform in brief_lower:
                constraints["platform"].append(platform)
        
        # Style constraints
        if "modern" in brief_lower:
            constraints["style"].append("modern")
        if "minimal" in brief_lower:
            constraints["style"].append("minimalist")
        if "bold" in brief_lower or "vibrant" in brief_lower:
            constraints["style"].append("bold")
        
        return constraints
    
    def _determine_complexity(
        self,
        asset_count: int,
        medium_count: int
    ) -> ProjectComplexity:
        """Determine project complexity based on asset and medium counts"""
        thresholds = self.config["complexity_thresholds"]
        
        if asset_count <= thresholds["simple"]["max_assets"] and \
           medium_count <= thresholds["simple"]["max_mediums"]:
            return ProjectComplexity.SIMPLE
        
        elif asset_count <= thresholds["moderate"]["max_assets"] and \
             medium_count <= thresholds["moderate"]["max_mediums"]:
            return ProjectComplexity.MODERATE
        
        elif asset_count <= thresholds["complex"]["max_assets"]:
            return ProjectComplexity.COMPLEX
        
        else:
            return ProjectComplexity.EPIC
    
    def generate_execution_plan(
        self,
        project: Dict[str, Any],
        strategy: str = "auto"
    ) -> Dict[str, Any]:
        """
        Generate detailed multi-step execution plan for a project
        
        Args:
            project: Project understanding from interpret_project()
            strategy: Execution strategy (auto, sequential, parallel, graphics_first, audio_first)
        
        Returns:
            Detailed execution plan with phases, tasks, dependencies, timeline
        
        Example:
            >>> plan = pic.generate_execution_plan(project, strategy="parallel")
            >>> print(f"Total phases: {len(plan['phases'])}")
            >>> print(f"Estimated duration: {plan['estimated_duration_hours']} hours")
        """
        project_id = project["id"]
        
        # Select execution pattern
        if strategy == "auto":
            strategy = self._select_optimal_strategy(project)
        
        pattern = self.project_patterns.get(strategy, self.project_patterns["parallel"])
        
        # Build execution phases
        phases = self._build_execution_phases(project, pattern)
        
        # Calculate dependencies
        dependencies = self._map_dependencies(project, phases)
        
        # Estimate timeline
        timeline = self._estimate_timeline(project, phases, pattern)
        
        # Build complete execution plan
        execution_plan = {
            "project_id": project_id,
            "strategy": strategy,
            "pattern": pattern,
            "phases": phases,
            "dependencies": dependencies,
            "timeline": timeline,
            "estimated_duration_hours": timeline["total_hours"],
            "estimated_completion_date": timeline["estimated_completion"],
            "resource_requirements": self._calculate_resource_requirements(project, phases),
            "risk_factors": self._identify_risk_factors(project),
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        
        # Store execution plan
        self.execution_plans[project_id] = execution_plan
        
        self.logger.info(
            f"✅ Generated execution plan for {project_id}: "
            f"{len(phases)} phases, {timeline['total_hours']:.1f} hours, "
            f"strategy: {strategy}"
        )
        
        return execution_plan
    
    def _select_optimal_strategy(self, project: Dict[str, Any]) -> str:
        """Select optimal execution strategy based on project characteristics"""
        mediums = project["required_mediums"]
        complexity = project["complexity"]
        urgency = project["timeline_hints"]["urgency"]
        
        # Simple projects with urgency: parallel
        if complexity == "simple" and urgency in ["urgent", "high"]:
            return "parallel"
        
        # Video projects often need graphics first
        if "video" in mediums and "graphics" in mediums:
            return "graphics_first"
        
        # Audio-first for podcast/music projects
        if "audio" in mediums and len(mediums) > 1:
            project_type = project.get("type", "")
            if "podcast" in project_type or "music" in project_type:
                return "audio_first"
        
        # Default to parallel for efficiency
        return "parallel"
    
    def _build_execution_phases(
        self,
        project: Dict[str, Any],
        pattern: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Build execution phases based on project and pattern"""
        phases = []
        assets = project["asset_requirements"]
        
        # Group assets by medium
        assets_by_medium = {
            "graphics": [],
            "audio": [],
            "video": []
        }
        
        for asset in assets:
            medium = asset["type"]
            if medium in assets_by_medium:
                assets_by_medium[medium].append(asset)
        
        # Build phases according to pattern
        if pattern["parallelism"]:
            # Single phase with all mediums
            phases.append({
                "phase_number": 1,
                "name": "Multi-Medium Production",
                "mediums": project["required_mediums"],
                "tasks": assets,
                "parallel": True,
                "estimated_hours": max(
                    sum(a["estimated_hours"] for a in assets_by_medium["graphics"]),
                    sum(a["estimated_hours"] for a in assets_by_medium["audio"]),
                    sum(a["estimated_hours"] for a in assets_by_medium["video"])
                )
            })
        else:
            # Sequential phases by medium order
            phase_num = 1
            for medium in pattern["order"]:
                if medium in project["required_mediums"]:
                    medium_assets = assets_by_medium[medium]
                    if medium_assets:
                        phases.append({
                            "phase_number": phase_num,
                            "name": f"{medium.capitalize()} Production",
                            "mediums": [medium],
                            "tasks": medium_assets,
                            "parallel": False,
                            "estimated_hours": sum(a["estimated_hours"] for a in medium_assets)
                        })
                        phase_num += 1
        
        return phases
    
    def _map_dependencies(
        self,
        project: Dict[str, Any],
        phases: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Map dependencies between assets and phases"""
        dependencies = []
        
        # Sequential phases have implicit dependencies
        for i in range(len(phases) - 1):
            dependencies.append({
                "type": "phase_dependency",
                "source": phases[i]["phase_number"],
                "target": phases[i + 1]["phase_number"],
                "reason": "Sequential execution pattern"
            })
        
        return dependencies
    
    def _estimate_timeline(
        self,
        project: Dict[str, Any],
        phases: List[Dict[str, Any]],
        pattern: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Estimate project timeline"""
        complexity_multiplier = self.config["estimation"]["complexity_multipliers"][
            project["complexity"]
        ]
        
        if pattern["parallelism"]:
            # Parallel: max of all phases
            total_hours = max(phase["estimated_hours"] for phase in phases) * complexity_multiplier
        else:
            # Sequential: sum of all phases
            total_hours = sum(phase["estimated_hours"] for phase in phases) * complexity_multiplier
        
        # Calculate completion date (assuming 8-hour work days)
        work_days = total_hours / 8
        estimated_completion = datetime.utcnow() + timedelta(days=work_days)
        
        return {
            "total_hours": total_hours,
            "work_days": work_days,
            "estimated_completion": estimated_completion.isoformat() + "Z",
            "complexity_multiplier": complexity_multiplier
        }
    
    def _calculate_resource_requirements(
        self,
        project: Dict[str, Any],
        phases: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate required resources for project"""
        return {
            "graphics_studio": "graphics" in project["required_mediums"],
            "audio_studio": "audio" in project["required_mediums"],
            "video_studio": "video" in project["required_mediums"],
            "total_assets": len(project["asset_requirements"]),
            "peak_concurrent_tasks": max(
                len(phase["tasks"]) for phase in phases
            ) if phases else 0
        }
    
    def _identify_risk_factors(self, project: Dict[str, Any]) -> List[Dict[str, str]]:
        """Identify potential risk factors for the project"""
        risks = []
        
        # Complexity risks
        if project["complexity"] in ["complex", "epic"]:
            risks.append({
                "type": "complexity",
                "level": "high",
                "description": "Large-scale project with many assets"
            })
        
        # Timeline risks
        if project["timeline_hints"]["urgency"] == "urgent":
            risks.append({
                "type": "timeline",
                "level": "high",
                "description": "Tight deadline may impact quality"
            })
        
        # Cross-medium risks
        if len(project["required_mediums"]) >= 3:
            risks.append({
                "type": "coordination",
                "level": "medium",
                "description": "Multiple mediums require careful synchronization"
            })
        
        return risks
    
    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project by ID"""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        return self.projects[project_id]
    
    def get_execution_plan(self, project_id: str) -> Dict[str, Any]:
        """Get execution plan by project ID"""
        if project_id not in self.execution_plans:
            raise ValueError(f"Execution plan for {project_id} not found")
        return self.execution_plans[project_id]


# Singleton instance
_pic_instance = None

def get_pic() -> ProjectIntelligenceCore:
    """Get or create singleton PIC instance"""
    global _pic_instance
    if _pic_instance is None:
        _pic_instance = ProjectIntelligenceCore()
    return _pic_instance


if __name__ == "__main__":
    # Demo usage
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("🔥 PROJECT INTELLIGENCE CORE - DEMO 🔥\n")
    
    pic = get_pic()
    
    # Example 1: Marketing campaign
    print("=" * 60)
    print("Example 1: Marketing Campaign")
    print("=" * 60)
    
    project1 = pic.interpret_project(
        brief="Create a holiday marketing campaign with 5 Instagram posts, "
              "3 Facebook ads, hero image, and 30-second promotional video",
        project_type=ProjectType.MARKETING_CAMPAIGN
    )
    
    print(f"\n📋 Project Interpreted:")
    print(f"   ID: {project1['id']}")
    print(f"   Type: {project1['type']}")
    print(f"   Complexity: {project1['complexity']}")
    print(f"   Mediums: {', '.join(project1['required_mediums'])}")
    print(f"   Assets: {len(project1['asset_requirements'])} total")
    
    # Generate execution plan
    plan1 = pic.generate_execution_plan(project1, strategy="auto")
    
    print(f"\n🚀 Execution Plan:")
    print(f"   Strategy: {plan1['strategy']}")
    print(f"   Phases: {len(plan1['phases'])}")
    print(f"   Duration: {plan1['estimated_duration_hours']:.1f} hours")
    print(f"   Work Days: {plan1['timeline']['work_days']:.1f} days")
    
    for phase in plan1['phases']:
        print(f"\n   Phase {phase['phase_number']}: {phase['name']}")
        print(f"      Mediums: {', '.join(phase['mediums'])}")
        print(f"      Tasks: {len(phase['tasks'])}")
        print(f"      Hours: {phase['estimated_hours']:.1f}")
    
    # Example 2: Product launch
    print("\n\n" + "=" * 60)
    print("Example 2: Product Launch")
    print("=" * 60)
    
    project2 = pic.interpret_project(
        brief="Launch new tech product with showcase video, feature graphics, "
              "demo video, social media content, and podcast announcement",
        project_type=ProjectType.PRODUCT_LAUNCH
    )
    
    print(f"\n📋 Project Interpreted:")
    print(f"   ID: {project2['id']}")
    print(f"   Type: {project2['type']}")
    print(f"   Complexity: {project2['complexity']}")
    print(f"   Mediums: {', '.join(project2['required_mediums'])}")
    print(f"   Assets: {len(project2['asset_requirements'])} total")
    
    plan2 = pic.generate_execution_plan(project2, strategy="parallel")
    
    print(f"\n🚀 Execution Plan:")
    print(f"   Strategy: {plan2['strategy']}")
    print(f"   Phases: {len(plan2['phases'])}")
    print(f"   Duration: {plan2['estimated_duration_hours']:.1f} hours")
    
    print("\n\n🔥 Project Intelligence Core demo complete! 👑")
    print("\nThe Director Brain is ready to understand any creative project!")
