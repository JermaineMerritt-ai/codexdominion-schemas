"""
🔥 CODEX DOMINION - PROJECT INTELLIGENCE CORE (PIC) 🔥
=======================================================
🔥🔥 HYBRID INTELLIGENCE MODE ACTIVATED 🔥🔥

The Director Brain of the Creative Intelligence Engine with DUAL INTELLIGENCE LAYERS:

1. GENERAL-PURPOSE INTELLIGENCE LAYER
   - Interprets ANY creative request
   - Universal project understanding
   - Ads, trailers, podcasts, courses, anything

2. DOMINION-OPTIMIZED INTELLIGENCE LAYER
   - YOUR signature style and workflows
   - Youth entrepreneurship, faith-based, kids content
   - POD design, AI tool demos, multi-medium packs
   - Automatic brand alignment

3. HYBRID INTELLIGENCE BEHAVIOR
   - Interpret any project
   - Check if it matches a Dominion pattern
   - If YES → apply optimized workflows
   - If NO → fall back to general-purpose logic
   - If MIXED → blend both intelligently

This gives you:
✅ Faster project planning for YOUR content
✅ Higher creative consistency across YOUR empire
✅ Cross-medium coherence (Kids → Faith → Youth → POD → AI tools)
✅ Automatic brand alignment with YOUR color palettes and tone
✅ Universal flexibility for anything outside your empire

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
    """General-purpose project types (Layer 1)"""
    MARKETING_CAMPAIGN = "marketing_campaign"
    PRODUCT_LAUNCH = "product_launch"
    SOCIAL_CONTENT = "social_content"
    BRAND_IDENTITY = "brand_identity"
    VIDEO_SERIES = "video_series"
    PODCAST_SERIES = "podcast_series"
    EDUCATIONAL_CONTENT = "educational_content"
    ENTERTAINMENT = "entertainment"
    ADVERTISING = "advertising"
    TRAILER = "trailer"
    ANIMATED_SHORT = "animated_short"
    MUSIC_TRACK = "music_track"
    SOCIAL_MEDIA_PACK = "social_media_pack"
    BRAND_KIT = "brand_kit"
    STORY_DRIVEN = "story_driven"
    COURSE = "course"
    MULTI_PLATFORM_BUNDLE = "multi_platform_bundle"
    CUSTOM = "custom"


class DominionProjectType(Enum):
    """Dominion-optimized project types (Layer 2)"""
    YOUTH_ENTREPRENEURSHIP = "youth_entrepreneurship"
    FAITH_BASED = "faith_based"
    KIDS_CONTENT = "kids_content"
    POD_DESIGN = "pod_design"
    AI_TOOL_DEMO = "ai_tool_demo"
    MULTI_MEDIUM_PACK = "multi_medium_pack"
    BRAND_STORYTELLING = "brand_storytelling"
    CROSS_MEDIUM_EMPIRE = "cross_medium_empire"
    DOMINION_SIGNATURE = "dominion_signature"


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
    🔥🔥 HYBRID INTELLIGENCE MODE - The Director Brain 🔥🔥
    
    Dual-layer intelligence system:
    - Layer 1: General-purpose (understands anything)
    - Layer 2: Dominion-optimized (your signature workflows)
    
    The PIC takes a creative brief and:
    1. Interprets project goals (with Dominion pattern matching)
    2. Identifies required assets (with your signature deliverables)
    3. Creates multi-step execution plan (with your optimized workflows)
    4. Maps dependencies (with brand consistency rules)
    5. Sequences tasks (with your preferred timelines)
    6. Estimates resources (with your typical hours)
    
    Usage:
        pic = ProjectIntelligenceCore()
        
        # Interpret project (automatically detects Dominion patterns)
        project_plan = pic.interpret_project(
            brief="Create a youth entrepreneurship video series with "
                  "graphics and motivational music"
        )
        
        # Generate execution plan (applies optimized workflows if Dominion project)
        blueprint = pic.generate_execution_plan(project_plan, strategy="auto")
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize Hybrid Intelligence Mode"""
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config(config_path)
        
        # 🔥 DOMINION BRAND CONFIGURATION 🔥
        self.dominion_config = {
            "color_palettes": {
                "youth_entrepreneurship": ["#FF6B35", "#004E89", "#F7B32B", "#FFFFFF"],
                "faith_based": ["#2C3E50", "#ECF0F1", "#E74C3C", "#F39C12"],
                "kids_content": ["#FF6B9D", "#C44569", "#F8B500", "#4ECDC4"],
                "pod_design": ["#000000", "#FFFFFF", "#FF0000", "#00FF00"],
                "ai_tools": ["#667EEA", "#764BA2", "#F093FB", "#4FACFE"]
            },
            "tone_profiles": {
                "youth_entrepreneurship": "empowering, action-oriented, visionary, bold",
                "faith_based": "warm, uplifting, hopeful, grounded, peaceful",
                "kids_content": "playful, imaginative, colorful, fun, educational",
                "pod_design": "bold, minimal, print-ready, commercial, scalable",
                "ai_tools": "innovative, futuristic, clear, technical, professional"
            },
            "content_structures": {
                "youth_entrepreneurship": ["hero_section", "value_props", "call_to_action", "testimonials", "success_stories"],
                "faith_based": ["scripture_intro", "story", "reflection", "prayer", "application"],
                "kids_content": ["hook", "adventure", "lesson", "fun_activity", "recap"],
                "pod_design": ["mockup", "variants", "print_specs", "marketing", "listing_images"],
                "ai_tools": ["problem", "demo", "features", "results", "cta"]
            },
            "signature_deliverables": {
                "multi_medium_pack": ["hero_video", "5_social_graphics", "background_music", "social_assets"],
                "cross_platform": ["instagram", "tiktok", "youtube", "pinterest"],
                "brand_consistency": True,
                "dominion_watermark": True
            }
        }
        
        # Load intelligence layers
        self.asset_templates = self._load_asset_templates()
        self.project_patterns = self._load_project_patterns()
        self.dominion_patterns = self._load_dominion_patterns()  # NEW
        
        # Project registry
        self.projects = {}
        
        self.logger.info("🔥 Project Intelligence Core initialized with HYBRID INTELLIGENCE MODE 🔥")
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration"""
        default_config = {
            "default_complexity_hours": {
                "simple": 8,
                "moderate": 16,
                "complex": 32,
                "epic": 64
            },
            "studio_hourly_rates": {
                "graphics": 2.0,
                "audio": 1.5,
                "video": 3.0
            },
            "parallel_execution_discount": 0.8,
            "complexity_multiplier": {
                "simple": 1.0,
                "moderate": 1.5,
                "complex": 2.0,
                "epic": 3.0
            }
        }
        
        if config_path and Path(config_path).exists():
            with open(config_path) as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def _load_dominion_patterns(self) -> Dict:
        """
        🔥 DOMINION-OPTIMIZED INTELLIGENCE LAYER 🔥
        Your signature workflows and patterns
        """
        return {
            DominionProjectType.YOUTH_ENTREPRENEURSHIP: {
                "typical_mediums": ["video", "graphics", "social_media"],
                "signature_assets": [
                    "hero_intro_video",
                    "value_prop_graphics",
                    "social_quote_cards",
                    "cta_graphics",
                    "testimonial_video",
                    "mobile_wallpaper",
                    "success_story_slides"
                ],
                "style_keywords": ["bold", "modern", "energetic", "aspirational", "empowering"],
                "default_platforms": ["instagram", "tiktok", "youtube", "linkedin"],
                "estimated_hours": 18,
                "brand_alignment": "very_high",
                "execution_pattern": "parallel"
            },
            DominionProjectType.FAITH_BASED: {
                "typical_mediums": ["audio", "graphics", "video"],
                "signature_assets": [
                    "devotional_audio",
                    "scripture_graphics",
                    "prayer_video",
                    "reflection_music",
                    "verse_cards",
                    "worship_visuals",
                    "testimony_video"
                ],
                "style_keywords": ["warm", "peaceful", "uplifting", "reverent", "hopeful"],
                "default_platforms": ["youtube", "pinterest", "instagram", "facebook"],
                "estimated_hours": 15,
                "brand_alignment": "very_high",
                "execution_pattern": "sequential"
            },
            DominionProjectType.KIDS_CONTENT: {
                "typical_mediums": ["video", "graphics", "audio"],
                "signature_assets": [
                    "animated_story",
                    "coloring_pages",
                    "fun_music",
                    "character_graphics",
                    "activity_sheets",
                    "sing_along_video",
                    "educational_graphics"
                ],
                "style_keywords": ["colorful", "playful", "fun", "educational", "imaginative"],
                "default_platforms": ["youtube", "pinterest", "tiktok", "instagram"],
                "estimated_hours": 20,
                "brand_alignment": "very_high",
                "execution_pattern": "cascading"
            },
            DominionProjectType.POD_DESIGN: {
                "typical_mediums": ["graphics"],
                "signature_assets": [
                    "main_design",
                    "mockup_renders",
                    "variant_colors",
                    "print_specs",
                    "marketing_graphics",
                    "listing_images",
                    "size_charts"
                ],
                "style_keywords": ["commercial", "scalable", "print-ready", "bold", "minimal"],
                "default_platforms": ["etsy", "amazon", "redbubble", "printful"],
                "estimated_hours": 8,
                "brand_alignment": "medium",
                "execution_pattern": "sequential"
            },
            DominionProjectType.AI_TOOL_DEMO: {
                "typical_mediums": ["video", "graphics"],
                "signature_assets": [
                    "demo_video",
                    "feature_graphics",
                    "results_showcase",
                    "comparison_slides",
                    "ui_screenshots",
                    "tutorial_graphics",
                    "thumbnail"
                ],
                "style_keywords": ["tech", "clean", "modern", "innovative", "professional"],
                "default_platforms": ["youtube", "linkedin", "twitter", "instagram"],
                "estimated_hours": 12,
                "brand_alignment": "medium",
                "execution_pattern": "parallel"
            },
            DominionProjectType.MULTI_MEDIUM_PACK: {
                "typical_mediums": ["video", "graphics", "audio"],
                "signature_assets": [
                    "hero_video",
                    "5_social_graphics",
                    "background_music",
                    "thumbnail",
                    "quote_cards",
                    "audio_stinger",
                    "social_stories"
                ],
                "style_keywords": ["cohesive", "branded", "multi-format", "versatile"],
                "default_platforms": ["instagram", "tiktok", "youtube", "pinterest", "facebook"],
                "estimated_hours": 24,
                "brand_alignment": "very_high",
                "execution_pattern": "parallel"
            }
        }
    
    def _load_asset_templates(self) -> Dict:
        """Load general-purpose asset templates"""
        return {
            "marketing_campaign": [
                "hero_video", "social_graphics", "email_graphics",
                "landing_page_assets", "ad_creatives", "thumbnail"
            ],
            "product_launch": [
                "hero_video", "product_showcase", "feature_graphics",
                "testimonial_videos", "social_media_pack", "launch_announcement"
            ],
            "social_content": [
                "post_graphics", "story_templates", "reel_video",
                "carousel_slides", "quote_cards"
            ],
            "educational": [
                "intro_video", "lesson_slides", "infographics",
                "worksheet_graphics", "quiz_graphics", "summary_video"
            ],
            "entertainment": [
                "episode_video", "thumbnail", "promo_graphics",
                "background_music", "intro_outro", "social_teasers"
            ]
        }
    
    def _load_project_patterns(self) -> Dict:
        """Load general-purpose execution patterns"""
        return {
            "sequential": {
                "description": "Linear execution - one medium at a time",
                "best_for": ["narrative-driven", "story-heavy", "dependent assets"],
                "risk": "low",
                "speed": "slow"
            },
            "parallel": {
                "description": "All mediums execute simultaneously",
                "best_for": ["tight deadlines", "independent assets", "high urgency"],
                "risk": "medium",
                "speed": "fast"
            },
            "cascading": {
                "description": "Staggered start with overlapping execution",
                "best_for": ["balanced projects", "moderate dependencies"],
                "risk": "low",
                "speed": "medium"
            },
            "iterative": {
                "description": "Prototype → Refine → Finalize cycles",
                "best_for": ["experimental", "high-quality", "client feedback"],
                "risk": "high",
                "speed": "slow"
            }
        }
    
    # ===================================================================
    # 🔥 SUBSYSTEM 1: PROJECT INTENT INTERPRETER (PII) 🔥
    # ===================================================================
    
    def interpret_project(
        self,
        brief: str,
        project_type: Optional[ProjectType] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        🔥 PROJECT INTENT INTERPRETER (PII) 🔥
        Converts natural language project brief into structured understanding.
        
        HYBRID INTELLIGENCE MODE:
        1. Detect general project type
        2. Check for Dominion patterns (NEW)
        3. Apply optimized intelligence if matched (NEW)
        4. Fall back to general-purpose if not (NEW)
        
        Returns:
            Structured project dict with interpretation results
        """
        metadata = metadata or {}
        
        self.logger.info(f"🔥 Interpreting project brief: {brief[:100]}...")
        
        # Step 1: Detect general project type
        if not project_type:
            project_type = self._detect_project_type(brief, metadata)
        
        # Step 2: Check for Dominion patterns 🔥 NEW 🔥
        dominion_type = self._detect_dominion_pattern(brief, metadata)
        is_dominion_project = dominion_type is not None
        
        if is_dominion_project:
            self.logger.info(f"🔥 DOMINION PATTERN DETECTED: {dominion_type.value} 🔥")
        else:
            self.logger.info("General-purpose project detected")
        
        # Step 3: Extract mediums (with Dominion optimization)
        mediums = self._extract_mediums(brief, metadata, dominion_type)
        
        # Step 4: Extract constraints (with Dominion defaults)
        constraints = self._extract_constraints(brief, metadata, dominion_type)
        
        # Step 5: Detect complexity
        complexity = self._detect_complexity(brief, mediums, metadata)
        
        # Step 6: Build structured project object
        project = {
            "project_id": f"pic_{uuid.uuid4().hex[:12]}",
            "brief": brief,
            "project_type": project_type.value,
            "dominion_type": dominion_type.value if dominion_type else None,  # 🔥 NEW 🔥
            "is_dominion_optimized": is_dominion_project,  # 🔥 NEW 🔥
            "complexity": complexity.value,
            "mediums": mediums,
            "constraints": constraints,
            "metadata": metadata,
            "interpreted_at": datetime.utcnow().isoformat() + "Z",
            "status": "interpreted"
        }
        
        # Step 7: Apply Dominion branding if applicable 🔥 NEW 🔥
        if is_dominion_project:
            project = self._apply_dominion_branding(project, dominion_type)
            self.logger.info("🔥 Dominion branding applied 🔥")
        
        # Store project
        self.projects[project["project_id"]] = project
        
        self.logger.info(f"✅ Project interpreted: {project['project_id']}")
        return project
    
    def _detect_project_type(self, brief: str, metadata: Dict) -> ProjectType:
        """Detect general project type from brief"""
        brief_lower = brief.lower()
        
        # Pattern matching for project types
        type_keywords = {
            ProjectType.MARKETING_CAMPAIGN: ["campaign", "marketing", "promotion"],
            ProjectType.PRODUCT_LAUNCH: ["launch", "product", "release"],
            ProjectType.SOCIAL_CONTENT: ["social", "post", "instagram", "tiktok"],
            ProjectType.TRAILER: ["trailer", "teaser", "preview"],
            ProjectType.COURSE: ["course", "training", "lesson", "tutorial"],
            ProjectType.PODCAST_SERIES: ["podcast", "episode", "audio series"],
            ProjectType.VIDEO_SERIES: ["series", "episode", "show"],
            ProjectType.ADVERTISING: ["ad", "commercial", "advertisement"]
        }
        
        for proj_type, keywords in type_keywords.items():
            if any(word in brief_lower for word in keywords):
                return proj_type
        
        return ProjectType.CUSTOM
    
    def _detect_dominion_pattern(
        self, 
        brief: str, 
        metadata: Dict[str, Any]
    ) -> Optional[DominionProjectType]:
        """
        🔥 DOMINION PATTERN DETECTOR 🔥
        Checks if project matches YOUR signature patterns.
        """
        brief_lower = brief.lower()
        
        # Youth entrepreneurship keywords
        if any(word in brief_lower for word in [
            "entrepreneur", "business", "startup", "hustle", "young", 
            "youth", "millionaire", "success", "mindset"
        ]):
            return DominionProjectType.YOUTH_ENTREPRENEURSHIP
        
        # Faith-based keywords
        if any(word in brief_lower for word in [
            "faith", "devotional", "prayer", "scripture", "bible", 
            "worship", "christian", "spiritual", "religious"
        ]):
            return DominionProjectType.FAITH_BASED
        
        # Kids content keywords
        if any(word in brief_lower for word in [
            "kids", "children", "coloring", "activity", "story", 
            "fun", "educational", "learning", "preschool"
        ]):
            return DominionProjectType.KIDS_CONTENT
        
        # POD design keywords
        if any(word in brief_lower for word in [
            "pod", "print on demand", "tshirt", "mug", "etsy", 
            "printable", "design", "merch"
        ]):
            return DominionProjectType.POD_DESIGN
        
        # AI tool demo keywords
        if any(word in brief_lower for word in [
            "ai tool", "demo", "tutorial", "software", "app demo", 
            "feature showcase", "walkthrough"
        ]):
            return DominionProjectType.AI_TOOL_DEMO
        
        # Multi-medium pack keywords
        if any(word in brief_lower for word in [
            "pack", "bundle", "multi-medium", "content pack", 
            "social media pack", "brand kit"
        ]):
            return DominionProjectType.MULTI_MEDIUM_PACK
        
        return None  # Not a Dominion-optimized project
    
    def _extract_mediums(
        self, 
        brief: str, 
        metadata: Dict[str, Any],
        dominion_type: Optional[DominionProjectType] = None
    ) -> List[str]:
        """
        Extract which mediums are needed.
        🔥 Dominion-optimized: Uses typical mediums as baseline 🔥
        """
        brief_lower = brief.lower()
        mediums = []
        
        # If Dominion-optimized, use typical mediums as baseline
        if dominion_type and dominion_type in self.dominion_patterns:
            mediums = self.dominion_patterns[dominion_type]["typical_mediums"].copy()
            self.logger.info(f"Using Dominion typical mediums: {mediums}")
        
        # Graphics indicators (extend/override)
        if any(word in brief_lower for word in [
            "graphic", "image", "design", "visual", "poster", 
            "banner", "infographic", "slides"
        ]):
            if "graphics" not in mediums:
                mediums.append("graphics")
        
        # Audio indicators (extend/override)
        if any(word in brief_lower for word in [
            "audio", "music", "sound", "voice", "podcast", 
            "narration", "voiceover", "soundtrack"
        ]):
            if "audio" not in mediums:
                mediums.append("audio")
        
        # Video indicators (extend/override)
        if any(word in brief_lower for word in [
            "video", "film", "animation", "motion", "trailer", 
            "commercial", "reel", "short"
        ]):
            if "video" not in mediums:
                mediums.append("video")
        
        # If no mediums detected, default to graphics
        if not mediums:
            mediums.append("graphics")
        
        return mediums
    
    def _extract_constraints(
        self,
        brief: str,
        metadata: Dict[str, Any],
        dominion_type: Optional[DominionProjectType] = None
    ) -> Dict[str, Any]:
        """
        Extract project constraints.
        🔥 Dominion-optimized: Applies your signature defaults 🔥
        """
        constraints = {
            "deadline": metadata.get("deadline"),
            "budget": metadata.get("budget"),
            "style_preferences": [],
            "platform_targets": [],
            "technical_requirements": []
        }
        
        brief_lower = brief.lower()
        
        # Apply Dominion defaults if applicable 🔥
        if dominion_type and dominion_type in self.dominion_patterns:
            pattern = self.dominion_patterns[dominion_type]
            constraints["style_preferences"] = pattern["style_keywords"].copy()
            constraints["platform_targets"] = pattern["default_platforms"].copy()
            self.logger.info(f"Applied Dominion style: {pattern['style_keywords']}")
        
        # Style detection (extend Dominion defaults)
        style_keywords = {
            "modern": ["modern", "contemporary", "sleek"],
            "minimal": ["minimal", "clean", "simple"],
            "bold": ["bold", "vibrant", "energetic"],
            "elegant": ["elegant", "sophisticated", "refined"]
        }
        
        for style, keywords in style_keywords.items():
            if any(word in brief_lower for word in keywords):
                if style not in constraints["style_preferences"]:
                    constraints["style_preferences"].append(style)
        
        # Platform detection (extend Dominion defaults)
        platforms = [
            "instagram", "tiktok", "youtube", "facebook", 
            "twitter", "linkedin", "pinterest", "snapchat"
        ]
        for platform in platforms:
            if platform in brief_lower:
                if platform not in constraints["platform_targets"]:
                    constraints["platform_targets"].append(platform)
        
        return constraints
    
    def _detect_complexity(
        self, 
        brief: str, 
        mediums: List[str], 
        metadata: Dict
    ) -> ProjectComplexity:
        """Detect project complexity"""
        # Count indicators
        brief_words = len(brief.split())
        medium_count = len(mediums)
        
        # Complexity scoring
        score = 0
        score += medium_count * 10
        score += min(brief_words / 10, 20)
        
        if score < 15:
            return ProjectComplexity.SIMPLE
        elif score < 30:
            return ProjectComplexity.MODERATE
        elif score < 50:
            return ProjectComplexity.COMPLEX
        else:
            return ProjectComplexity.EPIC
    
    def _apply_dominion_branding(
        self,
        project: Dict[str, Any],
        dominion_type: DominionProjectType
    ) -> Dict[str, Any]:
        """
        🔥 Apply YOUR signature branding to the project 🔥
        Ensures brand consistency across all Dominion projects.
        """
        if dominion_type not in self.dominion_patterns:
            return project
        
        pattern = self.dominion_patterns[dominion_type]
        
        # Add Dominion-specific metadata
        project["dominion_metadata"] = {
            "brand_alignment": pattern["brand_alignment"],
            "signature_deliverables": self.dominion_config["signature_deliverables"],
            "estimated_hours": pattern["estimated_hours"],
            "typical_assets": pattern["signature_assets"],
            "execution_pattern": pattern["execution_pattern"]
        }
        
        # Add color palette
        dominion_key = dominion_type.value
        if dominion_key in self.dominion_config["color_palettes"]:
            project["dominion_metadata"]["color_palette"] = self.dominion_config["color_palettes"][dominion_key]
        
        # Add tone profile
        if dominion_key in self.dominion_config["tone_profiles"]:
            project["dominion_metadata"]["tone_profile"] = self.dominion_config["tone_profiles"][dominion_key]
        
        # Add content structure
        if dominion_key in self.dominion_config["content_structures"]:
            project["dominion_metadata"]["content_structure"] = self.dominion_config["content_structures"][dominion_key]
        
        return project
    
    # ===================================================================
    # 🔥 SUBSYSTEM 2: PROJECT DECOMPOSITION ENGINE (PDE) 🔥
    # ===================================================================
    
    def generate_execution_plan(
        self,
        project: Dict[str, Any],
        strategy: str = "auto"
    ) -> Dict[str, Any]:
        """
        🔥 PRODUCTION BLUEPRINT BUILDER 🔥
        Generates complete execution plan.
        
        🔥 Dominion-optimized: Uses YOUR optimized workflows 🔥
        
        Args:
            project: Interpreted project dict
            strategy: Execution strategy ("auto", "sequential", "parallel", etc.)
        
        Returns:
            Complete production blueprint with phases, tasks, dependencies, timeline
        """
        self.logger.info(f"Generating execution plan for {project['project_id']}")
        
        # Determine execution strategy
        if strategy == "auto":
            strategy = self._determine_strategy(project)
        
        # Build asset list (with Dominion optimization)
        assets = self._generate_asset_requirements(project)
        
        # Build execution phases
        phases = self._build_execution_phases(project, assets, strategy)
        
        # Map dependencies
        dependencies = self._map_dependencies(project, phases, assets)
        
        # Estimate timeline (with Dominion hours)
        timeline = self._estimate_timeline(project, phases, dependencies)
        
        # Build resource requirements
        resources = self._calculate_resources(project, phases)
        
        # Identify risk factors
        risks = self._identify_risks(project, phases, timeline)
        
        # Build complete blueprint
        blueprint = {
            "project_id": project["project_id"],
            "strategy": strategy,
            "pattern": self.project_patterns.get(strategy, {}),
            "phases": phases,
            "dependencies": dependencies,
            "timeline": timeline,
            "resource_requirements": resources,
            "risk_factors": risks,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        
        self.logger.info(f"✅ Execution plan generated: {len(phases)} phases, {len(dependencies)} dependencies")
        
        return blueprint
    
    def _determine_strategy(self, project: Dict[str, Any]) -> str:
        """
        Determine best execution strategy.
        🔥 Dominion-optimized: Uses YOUR preferred patterns 🔥
        """
        # If Dominion project, use optimized pattern
        if project.get("is_dominion_optimized"):
            dominion_type = DominionProjectType(project["dominion_type"])
            if dominion_type in self.dominion_patterns:
                return self.dominion_patterns[dominion_type]["execution_pattern"]
        
        # General-purpose logic
        mediums = project["mediums"]
        complexity = project["complexity"]
        
        if len(mediums) == 1:
            return "sequential"
        elif complexity in ["simple", "moderate"]:
            return "parallel"
        elif complexity == "complex":
            return "cascading"
        else:
            return "iterative"
    
    def _generate_asset_requirements(self, project: Dict[str, Any]) -> List[Dict]:
        """
        🔥 ASSET REQUIREMENTS GENERATOR (ARG) 🔥
        Generates complete asset list.
        🔥 Dominion-optimized: Uses YOUR signature deliverables 🔥
        """
        assets = []
        
        # If Dominion project, use signature assets
        if project.get("is_dominion_optimized"):
            dominion_type = DominionProjectType(project["dominion_type"])
            if dominion_type in self.dominion_patterns:
                signature_assets = self.dominion_patterns[dominion_type]["signature_assets"]
                
                for i, asset_name in enumerate(signature_assets):
                    # Determine medium for asset
                    medium = self._determine_asset_medium(asset_name)
                    
                    assets.append({
                        "asset_id": f"asset_{i+1}",
                        "name": asset_name,
                        "medium": medium,
                        "description": f"Dominion signature: {asset_name}",
                        "estimated_hours": 2.0,
                        "priority": "high" if i < 3 else "medium"
                    })
                
                return assets
        
        # General-purpose asset generation
        project_type = project["project_type"]
        templates = self.asset_templates.get(project_type.split("_")[0], [])
        
        for i, template in enumerate(templates):
            medium = self._determine_asset_medium(template)
            
            assets.append({
                "asset_id": f"asset_{i+1}",
                "name": template,
                "medium": medium,
                "description": f"General asset: {template}",
                "estimated_hours": 2.0,
                "priority": "medium"
            })
        
        return assets
    
    def _determine_asset_medium(self, asset_name: str) -> str:
        """Determine which medium creates this asset"""
        name_lower = asset_name.lower()
        
        if any(word in name_lower for word in ["video", "animation", "film", "trailer"]):
            return "video"
        elif any(word in name_lower for word in ["audio", "music", "sound", "voice"]):
            return "audio"
        else:
            return "graphics"
    
    def _build_execution_phases(
        self, 
        project: Dict, 
        assets: List[Dict], 
        strategy: str
    ) -> List[Dict]:
        """
        🔥 PROJECT DECOMPOSITION ENGINE (PDE) 🔥
        Breaks project into executable phases.
        """
        phases = []
        
        if strategy == "sequential":
            # One phase per medium
            mediums = project["mediums"]
            for i, medium in enumerate(mediums):
                medium_assets = [a for a in assets if a["medium"] == medium]
                phases.append({
                    "phase_number": i + 1,
                    "name": f"{medium.capitalize()} Production",
                    "mediums": [medium],
                    "tasks": medium_assets,
                    "parallel": False,
                    "estimated_hours": sum(a["estimated_hours"] for a in medium_assets)
                })
        
        elif strategy == "parallel":
            # Single phase with all mediums
            phases.append({
                "phase_number": 1,
                "name": "Multi-Medium Production",
                "mediums": project["mediums"],
                "tasks": assets,
                "parallel": True,
                "estimated_hours": max(
                    sum(a["estimated_hours"] for a in assets if a["medium"] == m)
                    for m in project["mediums"]
                )
            })
        
        elif strategy == "cascading":
            # Multiple overlapping phases
            phases.append({
                "phase_number": 1,
                "name": "Foundation Phase",
                "mediums": ["graphics"],
                "tasks": [a for a in assets if a["medium"] == "graphics"],
                "parallel": False,
                "estimated_hours": sum(a["estimated_hours"] for a in assets if a["medium"] == "graphics")
            })
            
            phases.append({
                "phase_number": 2,
                "name": "Production Phase",
                "mediums": ["audio", "video"],
                "tasks": [a for a in assets if a["medium"] in ["audio", "video"]],
                "parallel": True,
                "estimated_hours": max(
                    sum(a["estimated_hours"] for a in assets if a["medium"] == m)
                    for m in ["audio", "video"] if m in project["mediums"]
                )
            })
        
        return phases
    
    def _map_dependencies(
        self, 
        project: Dict, 
        phases: List[Dict], 
        assets: List[Dict]
    ) -> List[Dict]:
        """
        🔥 DEPENDENCY MAPPING SYSTEM (DMS) 🔥
        Creates dependency graph between assets and phases.
        """
        dependencies = []
        
        # Phase dependencies (sequential phases depend on previous)
        for i in range(1, len(phases)):
            dependencies.append({
                "type": "phase_dependency",
                "source": phases[i-1]["phase_number"],
                "target": phases[i]["phase_number"],
                "reason": "Sequential execution pattern"
            })
        
        # Asset dependencies (video often needs graphics first)
        video_assets = [a for a in assets if a["medium"] == "video"]
        graphics_assets = [a for a in assets if a["medium"] == "graphics"]
        
        if video_assets and graphics_assets:
            for video_asset in video_assets:
                dependencies.append({
                    "type": "asset_dependency",
                    "source": graphics_assets[0]["asset_id"],
                    "target": video_asset["asset_id"],
                    "reason": "Video production typically requires graphic assets"
                })
        
        return dependencies
    
    def _estimate_timeline(
        self, 
        project: Dict, 
        phases: List[Dict], 
        dependencies: List[Dict]
    ) -> Dict:
        """Estimate project timeline"""
        # If Dominion project, use optimized hours
        if project.get("is_dominion_optimized"):
            estimated_hours = project["dominion_metadata"]["estimated_hours"]
        else:
            # Calculate from phases
            if phases[0].get("parallel"):
                estimated_hours = phases[0]["estimated_hours"]
            else:
                estimated_hours = sum(p["estimated_hours"] for p in phases)
        
        # Apply complexity multiplier
        complexity = project["complexity"]
        multiplier = self.config["complexity_multiplier"][complexity]
        total_hours = estimated_hours * multiplier
        
        # Convert to work days (8 hours/day)
        work_days = total_hours / 8
        
        # Estimate completion date (assuming 5 work days/week)
        completion_date = datetime.utcnow() + timedelta(days=work_days * 1.4)
        
        return {
            "total_hours": total_hours,
            "work_days": work_days,
            "estimated_completion": completion_date.isoformat() + "Z",
            "complexity_multiplier": multiplier
        }
    
    def _calculate_resources(self, project: Dict, phases: List[Dict]) -> Dict:
        """Calculate resource requirements"""
        mediums = project["mediums"]
        
        resources = {
            "graphics_studio": "graphics" in mediums,
            "audio_studio": "audio" in mediums,
            "video_studio": "video" in mediums,
            "total_assets": sum(len(p["tasks"]) for p in phases),
            "peak_concurrent_tasks": max(len(p["tasks"]) for p in phases)
        }
        
        return resources
    
    def _identify_risks(
        self, 
        project: Dict, 
        phases: List[Dict], 
        timeline: Dict
    ) -> List[str]:
        """Identify potential risk factors"""
        risks = []
        
        if timeline["work_days"] > 10:
            risks.append("Extended timeline may cause resource conflicts")
        
        if len(project["mediums"]) >= 3:
            risks.append("Multi-medium coordination complexity")
        
        if project["complexity"] in ["complex", "epic"]:
            risks.append("High complexity increases iteration risk")
        
        return risks


# ===================================================================
# 🔥 SINGLETON PATTERN 🔥
# ===================================================================

_pic_instance = None

def get_pic() -> ProjectIntelligenceCore:
    """Get singleton instance of Project Intelligence Core"""
    global _pic_instance
    if _pic_instance is None:
        _pic_instance = ProjectIntelligenceCore()
    return _pic_instance


# ===================================================================
# 🔥 DEMO CODE 🔥
# ===================================================================

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("🔥🔥🔥 PROJECT INTELLIGENCE CORE - HYBRID INTELLIGENCE MODE DEMO 🔥🔥🔥\n")
    
    pic = get_pic()
    
    # Test 1: Dominion-optimized project (Youth Entrepreneurship)
    print("=" * 80)
    print("TEST 1: DOMINION-OPTIMIZED PROJECT (Youth Entrepreneurship)")
    print("=" * 80)
    
    project1 = pic.interpret_project(
        brief="Create a youth entrepreneur video series with motivational graphics "
              "and energetic background music for Instagram and TikTok"
    )
    
    print(json.dumps(project1, indent=2))
    
    blueprint1 = pic.generate_execution_plan(project1, strategy="auto")
    
    print("\n📋 PRODUCTION BLUEPRINT:")
    print(json.dumps(blueprint1, indent=2))
    
    # Test 2: General-purpose project
    print("\n" + "=" * 80)
    print("TEST 2: GENERAL-PURPOSE PROJECT (Product Launch)")
    print("=" * 80)
    
    project2 = pic.interpret_project(
        brief="Create a product launch campaign with hero video, 5 social media graphics, "
              "and background music"
    )
    
    print(json.dumps(project2, indent=2))
    
    blueprint2 = pic.generate_execution_plan(project2, strategy="auto")
    
    print("\n📋 PRODUCTION BLUEPRINT:")
    print(json.dumps(blueprint2, indent=2))
    
    # Test 3: Faith-based Dominion project
    print("\n" + "=" * 80)
    print("TEST 3: DOMINION-OPTIMIZED PROJECT (Faith-Based)")
    print("=" * 80)
    
    project3 = pic.interpret_project(
        brief="Create a daily devotional series with scripture graphics, "
              "prayer audio, and worship visuals for YouTube and Pinterest"
    )
    
    print(json.dumps(project3, indent=2))
    
    blueprint3 = pic.generate_execution_plan(project3, strategy="auto")
    
    print("\n📋 PRODUCTION BLUEPRINT:")
    print(json.dumps(blueprint3, indent=2))
    
    print("\n🔥 HYBRID INTELLIGENCE MODE: FULLY OPERATIONAL 🔥")
    print("✅ General-purpose intelligence: ACTIVE")
    print("✅ Dominion-optimized intelligence: ACTIVE")
    print("✅ Automatic pattern detection: ACTIVE")
    print("✅ Brand consistency: ACTIVE")
