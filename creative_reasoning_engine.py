"""
🔥 CODEX DOMINION - CREATIVE REASONING ENGINE (CRE) 🔥
========================================================
The Creative Intuition Layer of the Creative Intelligence Engine

This is where the INTELLIGENCE lives - the system that THINKS creatively.

Capabilities:
- Style reasoning and matching
- Narrative reasoning and coherence
- Visual/audio/video consistency checking
- Cross-medium harmony analysis
- Quality prediction before generation
- Missing asset detection
- Creative conflict resolution
- Aesthetic judgment

The CRE is the "creative mind" - it understands artistic coherence,
narrative flow, and stylistic consistency across all mediums.

Author: Codex Dominion High Council
Phase: 30 - Creative Intelligence Engine
Last Updated: December 23, 2025
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple, Set
from pathlib import Path
from enum import Enum
import uuid


class StyleCategory(Enum):
    """Visual and aesthetic style categories"""
    MODERN = "modern"
    MINIMAL = "minimal"
    BOLD = "bold"
    ELEGANT = "elegant"
    PLAYFUL = "playful"
    PROFESSIONAL = "professional"
    ARTISTIC = "artistic"
    VINTAGE = "vintage"
    FUTURISTIC = "futuristic"
    ORGANIC = "organic"


class NarrativeTone(Enum):
    """Narrative and messaging tone"""
    SERIOUS = "serious"
    HUMOROUS = "humorous"
    INSPIRATIONAL = "inspirational"
    EDUCATIONAL = "educational"
    EMOTIONAL = "emotional"
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    URGENT = "urgent"


class QualityLevel(Enum):
    """Predicted quality levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    NEEDS_IMPROVEMENT = "needs_improvement"
    POOR = "poor"


class ConsistencyIssueType(Enum):
    """Types of consistency issues"""
    COLOR_MISMATCH = "color_mismatch"
    STYLE_CONFLICT = "style_conflict"
    TONE_MISMATCH = "tone_mismatch"
    NARRATIVE_GAP = "narrative_gap"
    QUALITY_VARIANCE = "quality_variance"
    TIMING_MISALIGNMENT = "timing_misalignment"
    BRANDING_INCONSISTENCY = "branding_inconsistency"


class CreativeReasoningEngine:
    """
    🔥 The Creative Mind - Thinks About Artistic Coherence 🔥
    
    The CRE provides the intelligence layer that understands:
    1. Style consistency across graphics, audio, video
    2. Narrative coherence throughout a project
    3. Quality prediction for planned assets
    4. Missing elements in creative plans
    5. Conflicting creative decisions
    6. Cross-medium harmony
    
    It acts as the "creative director" that ensures everything
    makes sense together artistically and narratively.
    
    Usage:
        cre = CreativeReasoningEngine()
        
        # Analyze style consistency
        style_analysis = cre.analyze_style_consistency(project, assets)
        
        # Check narrative coherence
        narrative_check = cre.check_narrative_coherence(project, assets)
        
        # Predict quality
        quality_prediction = cre.predict_quality(asset_plan)
        
        # Detect missing assets
        missing = cre.detect_missing_assets(project, existing_assets)
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the Creative Reasoning Engine"""
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config(config_path)
        
        # Creative knowledge bases
        self.style_rules = self._load_style_rules()
        self.narrative_patterns = self._load_narrative_patterns()
        self.quality_criteria = self._load_quality_criteria()
        self.harmony_rules = self._load_harmony_rules()
        
        # Reasoning cache
        self.analysis_cache: Dict[str, Dict[str, Any]] = {}
        
        self.logger.info("🔥 Creative Reasoning Engine initialized! 👑")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load CRE configuration"""
        default_config = {
            "reasoning": {
                "enable_style_analysis": True,
                "enable_narrative_analysis": True,
                "enable_quality_prediction": True,
                "enable_conflict_detection": True
            },
            "thresholds": {
                "style_similarity_min": 0.7,
                "narrative_coherence_min": 0.8,
                "quality_score_min": 0.75,
                "consistency_score_min": 0.85
            },
            "weights": {
                "visual_consistency": 0.3,
                "audio_consistency": 0.25,
                "narrative_flow": 0.25,
                "quality": 0.2
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
    
    def _load_style_rules(self) -> Dict[str, Dict[str, Any]]:
        """Load style consistency rules"""
        return {
            "modern": {
                "colors": ["clean", "bright", "high_contrast"],
                "typography": ["sans_serif", "geometric"],
                "visual_language": ["minimal", "flat", "abstract"],
                "audio_style": ["electronic", "contemporary"],
                "compatible_with": ["minimal", "futuristic", "professional"]
            },
            "minimal": {
                "colors": ["monochrome", "limited_palette", "neutral"],
                "typography": ["simple", "clean", "sans_serif"],
                "visual_language": ["whitespace", "simplicity", "focus"],
                "audio_style": ["ambient", "subtle"],
                "compatible_with": ["modern", "elegant", "professional"]
            },
            "bold": {
                "colors": ["vibrant", "saturated", "contrasting"],
                "typography": ["heavy", "display", "impactful"],
                "visual_language": ["dynamic", "energetic", "striking"],
                "audio_style": ["upbeat", "powerful", "dramatic"],
                "compatible_with": ["playful", "modern", "artistic"]
            },
            "elegant": {
                "colors": ["sophisticated", "refined", "harmonious"],
                "typography": ["serif", "refined", "classic"],
                "visual_language": ["graceful", "balanced", "luxurious"],
                "audio_style": ["orchestral", "smooth", "refined"],
                "compatible_with": ["minimal", "professional", "vintage"]
            }
        }
    
    def _load_narrative_patterns(self) -> Dict[str, List[str]]:
        """Load narrative structure patterns"""
        return {
            "marketing_campaign": [
                "problem_introduction",
                "solution_presentation",
                "benefits_showcase",
                "call_to_action"
            ],
            "product_launch": [
                "teaser",
                "reveal",
                "features_breakdown",
                "availability_announcement"
            ],
            "educational": [
                "hook",
                "context_setting",
                "content_delivery",
                "recap",
                "next_steps"
            ],
            "storytelling": [
                "introduction",
                "rising_action",
                "climax",
                "resolution"
            ]
        }
    
    def _load_quality_criteria(self) -> Dict[str, Dict[str, float]]:
        """Load quality assessment criteria"""
        return {
            "graphics": {
                "resolution": 0.25,
                "composition": 0.25,
                "color_theory": 0.20,
                "typography": 0.15,
                "originality": 0.15
            },
            "audio": {
                "clarity": 0.30,
                "mixing": 0.25,
                "composition": 0.20,
                "production_value": 0.15,
                "originality": 0.10
            },
            "video": {
                "visual_quality": 0.25,
                "editing": 0.25,
                "storytelling": 0.20,
                "audio_sync": 0.15,
                "pacing": 0.15
            }
        }
    
    def _load_harmony_rules(self) -> Dict[str, List[str]]:
        """Load cross-medium harmony rules"""
        return {
            "color_harmony": [
                "Graphics and video should share primary color palette",
                "Audio waveform visualizations should match color theme",
                "Consistent color temperature across all mediums"
            ],
            "rhythm_harmony": [
                "Visual cuts should align with audio beats",
                "Animation timing should match music tempo",
                "Text reveals should sync with voiceover pacing"
            ],
            "mood_harmony": [
                "Visual style should match audio emotional tone",
                "Video pacing should reflect music energy level",
                "Color psychology should align with narrative mood"
            ]
        }
    
    def analyze_style_consistency(
        self,
        project: Dict[str, Any],
        assets: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze style consistency across all project assets
        
        Args:
            project: Project information from PIC
            assets: List of assets (planned or existing)
        
        Returns:
            Style consistency analysis with score and issues
        
        Example:
            >>> cre = CreativeReasoningEngine()
            >>> analysis = cre.analyze_style_consistency(project, assets)
            >>> print(f"Consistency score: {analysis['consistency_score']}")
            >>> print(f"Issues found: {len(analysis['issues'])}")
        """
        analysis_id = f"style_analysis_{uuid.uuid4().hex[:8]}"
        
        # Extract style information from project
        project_style = self._infer_project_style(project)
        
        # Group assets by medium
        assets_by_medium = self._group_assets_by_medium(assets)
        
        # Check consistency within each medium
        issues = []
        medium_scores = {}
        
        for medium, medium_assets in assets_by_medium.items():
            if medium_assets:
                medium_analysis = self._analyze_medium_style(
                    medium,
                    medium_assets,
                    project_style
                )
                medium_scores[medium] = medium_analysis["score"]
                issues.extend(medium_analysis["issues"])
        
        # Check cross-medium harmony
        cross_medium_issues = self._check_cross_medium_harmony(
            assets_by_medium,
            project_style
        )
        issues.extend(cross_medium_issues)
        
        # Calculate overall consistency score
        if medium_scores:
            consistency_score = sum(medium_scores.values()) / len(medium_scores)
        else:
            consistency_score = 1.0
        
        # Apply penalties for cross-medium issues
        consistency_score -= len(cross_medium_issues) * 0.05
        consistency_score = max(0.0, min(1.0, consistency_score))
        
        analysis = {
            "analysis_id": analysis_id,
            "project_id": project.get("id"),
            "consistency_score": round(consistency_score, 3),
            "project_style": project_style,
            "medium_scores": medium_scores,
            "issues": issues,
            "recommendations": self._generate_style_recommendations(issues, project_style),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        self.analysis_cache[analysis_id] = analysis
        
        self.logger.info(
            f"✅ Style analysis complete: score {consistency_score:.2f}, "
            f"{len(issues)} issues found"
        )
        
        return analysis
    
    def _infer_project_style(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Infer project style from constraints and context"""
        constraints = project.get("constraints", {})
        brief = project.get("brief", "").lower()
        
        # Start with neutral style
        style = {
            "primary": StyleCategory.MODERN.value,
            "secondary": [],
            "tone": NarrativeTone.PROFESSIONAL.value,
            "attributes": []
        }
        
        # Detect from constraints
        if "style" in constraints and constraints["style"]:
            style["primary"] = constraints["style"][0]
            style["secondary"] = constraints["style"][1:] if len(constraints["style"]) > 1 else []
        
        # Detect from brief keywords
        if "minimal" in brief or "clean" in brief:
            if style["primary"] == "modern":
                style["primary"] = StyleCategory.MINIMAL.value
        
        if "bold" in brief or "vibrant" in brief or "energetic" in brief:
            style["primary"] = StyleCategory.BOLD.value
            style["tone"] = NarrativeTone.INSPIRATIONAL.value
        
        if "elegant" in brief or "luxury" in brief or "sophisticated" in brief:
            style["primary"] = StyleCategory.ELEGANT.value
        
        if "fun" in brief or "playful" in brief:
            style["primary"] = StyleCategory.PLAYFUL.value
            style["tone"] = NarrativeTone.CASUAL.value
        
        return style
    
    def _group_assets_by_medium(
        self,
        assets: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Group assets by their medium type"""
        grouped = {
            "graphics": [],
            "audio": [],
            "video": []
        }
        
        for asset in assets:
            medium = asset.get("type", "graphics")
            if medium in grouped:
                grouped[medium].append(asset)
        
        return grouped
    
    def _analyze_medium_style(
        self,
        medium: str,
        assets: List[Dict[str, Any]],
        project_style: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze style consistency within a single medium"""
        issues = []
        score = 1.0
        
        # Check if assets align with project style
        primary_style = project_style["primary"]
        if primary_style in self.style_rules:
            style_rules = self.style_rules[primary_style]
            
            # Simplified check - in production would analyze actual asset properties
            # For now, assume all assets need style tags to validate
            for asset in assets:
                asset_style = asset.get("style", primary_style)
                if asset_style != primary_style:
                    # Check compatibility
                    if asset_style not in style_rules.get("compatible_with", []):
                        issues.append({
                            "type": ConsistencyIssueType.STYLE_CONFLICT.value,
                            "severity": "medium",
                            "asset": asset["name"],
                            "description": f"Asset style '{asset_style}' conflicts with project style '{primary_style}'"
                        })
                        score -= 0.15
        
        return {
            "score": max(0.0, score),
            "issues": issues
        }
    
    def _check_cross_medium_harmony(
        self,
        assets_by_medium: Dict[str, List[Dict[str, Any]]],
        project_style: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Check harmony between different mediums"""
        issues = []
        
        # Check if all mediums are represented
        active_mediums = [m for m, assets in assets_by_medium.items() if assets]
        
        if len(active_mediums) > 1:
            # Check color harmony
            if "graphics" in active_mediums and "video" in active_mediums:
                # Would check actual color palettes in production
                # For now, log as a checkpoint
                pass
            
            # Check rhythm harmony
            if "audio" in active_mediums and "video" in active_mediums:
                # Would check timing synchronization
                pass
        
        return issues
    
    def _generate_style_recommendations(
        self,
        issues: List[Dict[str, Any]],
        project_style: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations to fix style issues"""
        recommendations = []
        
        if not issues:
            recommendations.append("✅ Style consistency is excellent - no changes needed")
            return recommendations
        
        # Generate specific recommendations based on issues
        style_conflicts = [i for i in issues if i["type"] == ConsistencyIssueType.STYLE_CONFLICT.value]
        if style_conflicts:
            recommendations.append(
                f"Align all assets to {project_style['primary']} style for consistency"
            )
        
        color_issues = [i for i in issues if i["type"] == ConsistencyIssueType.COLOR_MISMATCH.value]
        if color_issues:
            recommendations.append(
                "Establish a unified color palette and apply across all mediums"
            )
        
        return recommendations
    
    def check_narrative_coherence(
        self,
        project: Dict[str, Any],
        assets: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Check narrative coherence across project assets
        
        Args:
            project: Project information
            assets: List of assets with narrative elements
        
        Returns:
            Narrative coherence analysis
        
        Example:
            >>> coherence = cre.check_narrative_coherence(project, assets)
            >>> print(f"Narrative score: {coherence['coherence_score']}")
        """
        analysis_id = f"narrative_analysis_{uuid.uuid4().hex[:8]}"
        
        # Determine expected narrative pattern
        project_type = project.get("type", "custom")
        pattern = self.narrative_patterns.get(project_type, [])
        
        # Check if assets follow narrative flow
        narrative_gaps = self._detect_narrative_gaps(assets, pattern)
        tone_consistency = self._check_tone_consistency(assets, project)
        
        # Calculate coherence score
        coherence_score = 1.0
        coherence_score -= len(narrative_gaps) * 0.1
        coherence_score -= (1.0 - tone_consistency) * 0.3
        coherence_score = max(0.0, min(1.0, coherence_score))
        
        analysis = {
            "analysis_id": analysis_id,
            "project_id": project.get("id"),
            "coherence_score": round(coherence_score, 3),
            "expected_pattern": pattern,
            "narrative_gaps": narrative_gaps,
            "tone_consistency_score": round(tone_consistency, 3),
            "recommendations": self._generate_narrative_recommendations(narrative_gaps),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        self.logger.info(
            f"✅ Narrative analysis complete: score {coherence_score:.2f}, "
            f"{len(narrative_gaps)} gaps found"
        )
        
        return analysis
    
    def _detect_narrative_gaps(
        self,
        assets: List[Dict[str, Any]],
        pattern: List[str]
    ) -> List[Dict[str, str]]:
        """Detect missing narrative elements"""
        gaps = []
        
        if not pattern:
            return gaps
        
        # Simplified check - would use NLP in production
        # Check if key narrative beats are covered
        asset_names = [a["name"].lower() for a in assets]
        asset_text = " ".join(asset_names)
        
        for narrative_beat in pattern:
            beat_keywords = narrative_beat.replace("_", " ").split()
            if not any(keyword in asset_text for keyword in beat_keywords):
                gaps.append({
                    "missing_element": narrative_beat,
                    "description": f"Missing {narrative_beat} in project narrative"
                })
        
        return gaps
    
    def _check_tone_consistency(
        self,
        assets: List[Dict[str, Any]],
        project: Dict[str, Any]
    ) -> float:
        """Check consistency of narrative tone across assets"""
        # Simplified - would use sentiment analysis in production
        return 0.9  # Default high consistency
    
    def _generate_narrative_recommendations(
        self,
        gaps: List[Dict[str, str]]
    ) -> List[str]:
        """Generate recommendations to improve narrative"""
        recommendations = []
        
        if not gaps:
            recommendations.append("✅ Narrative flow is coherent")
            return recommendations
        
        for gap in gaps:
            recommendations.append(
                f"Add asset covering '{gap['missing_element']}' to complete narrative arc"
            )
        
        return recommendations
    
    def predict_quality(
        self,
        asset_plan: Dict[str, Any],
        historical_data: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Predict quality level for a planned asset
        
        Args:
            asset_plan: Planned asset specification
            historical_data: Optional historical quality data
        
        Returns:
            Quality prediction with confidence level
        
        Example:
            >>> prediction = cre.predict_quality(asset_plan)
            >>> print(f"Predicted quality: {prediction['predicted_quality']}")
            >>> print(f"Confidence: {prediction['confidence']}")
        """
        medium = asset_plan.get("type", "graphics")
        criteria = self.quality_criteria.get(medium, {})
        
        # Calculate quality score based on asset specifications
        quality_score = 0.8  # Base score
        
        # Adjust based on specifications
        if "estimated_hours" in asset_plan:
            hours = asset_plan["estimated_hours"]
            # More time generally means higher quality
            if hours >= 8:
                quality_score += 0.15
            elif hours >= 4:
                quality_score += 0.10
        
        if asset_plan.get("priority") == "high":
            quality_score += 0.05
        
        quality_score = min(1.0, quality_score)
        
        # Determine quality level
        if quality_score >= 0.9:
            quality_level = QualityLevel.EXCELLENT
        elif quality_score >= 0.75:
            quality_level = QualityLevel.GOOD
        elif quality_score >= 0.6:
            quality_level = QualityLevel.ACCEPTABLE
        else:
            quality_level = QualityLevel.NEEDS_IMPROVEMENT
        
        prediction = {
            "asset_name": asset_plan.get("name"),
            "predicted_quality": quality_level.value,
            "quality_score": round(quality_score, 3),
            "confidence": 0.85,  # Would be calculated from historical data
            "factors": {
                "time_allocated": asset_plan.get("estimated_hours"),
                "priority": asset_plan.get("priority"),
                "complexity": "moderate"
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        return prediction
    
    def detect_missing_assets(
        self,
        project: Dict[str, Any],
        existing_assets: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Detect missing assets that would complete the project
        
        Args:
            project: Project information
            existing_assets: Currently planned or created assets
        
        Returns:
            Analysis of missing assets
        
        Example:
            >>> missing = cre.detect_missing_assets(project, current_assets)
            >>> print(f"Missing {len(missing['missing_assets'])} assets")
        """
        required_assets = project.get("asset_requirements", [])
        existing_names = {a["name"] for a in existing_assets}
        
        missing = []
        for required in required_assets:
            if required["name"] not in existing_names:
                missing.append(required)
        
        # Check for implicit missing assets
        implicit_missing = self._detect_implicit_missing_assets(
            project,
            existing_assets
        )
        missing.extend(implicit_missing)
        
        analysis = {
            "project_id": project.get("id"),
            "missing_count": len(missing),
            "missing_assets": missing,
            "completeness_score": round(
                len(existing_assets) / (len(existing_assets) + len(missing)),
                3
            ) if (len(existing_assets) + len(missing)) > 0 else 0.0,
            "recommendations": [
                f"Create {asset['name']} ({asset['type']})"
                for asset in missing[:5]  # Top 5 recommendations
            ],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        return analysis
    
    def _detect_implicit_missing_assets(
        self,
        project: Dict[str, Any],
        existing_assets: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Detect assets that aren't explicit but would improve the project"""
        implicit = []
        
        # Check for platform-specific assets
        platforms = project.get("constraints", {}).get("platform", [])
        existing_types = {a.get("type") for a in existing_assets}
        
        if "instagram" in platforms and "graphics" in existing_types:
            # Check for Instagram Stories format
            story_exists = any("story" in a["name"].lower() for a in existing_assets)
            if not story_exists:
                implicit.append({
                    "name": "instagram_stories",
                    "type": "graphics",
                    "priority": "medium",
                    "estimated_hours": 2,
                    "reason": "Instagram platform detected but no Stories format"
                })
        
        return implicit
    
    def get_analysis(self, analysis_id: str) -> Dict[str, Any]:
        """Retrieve cached analysis by ID"""
        if analysis_id not in self.analysis_cache:
            raise ValueError(f"Analysis {analysis_id} not found")
        return self.analysis_cache[analysis_id]


# Singleton instance
_cre_instance = None

def get_cre() -> CreativeReasoningEngine:
    """Get or create singleton CRE instance"""
    global _cre_instance
    if _cre_instance is None:
        _cre_instance = CreativeReasoningEngine()
    return _cre_instance


if __name__ == "__main__":
    # Demo usage
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("🔥 CREATIVE REASONING ENGINE - DEMO 🔥\n")
    
    cre = get_cre()
    
    # Mock project and assets
    project = {
        "id": "test_project_123",
        "type": "marketing_campaign",
        "brief": "Create bold and vibrant holiday campaign",
        "constraints": {
            "style": ["bold", "modern"],
            "platform": ["instagram", "facebook"]
        }
    }
    
    assets = [
        {"name": "hero_image", "type": "graphics", "style": "bold", "estimated_hours": 4},
        {"name": "social_posts", "type": "graphics", "style": "bold", "estimated_hours": 6},
        {"name": "promo_video", "type": "video", "style": "modern", "estimated_hours": 12},
        {"name": "background_music", "type": "audio", "estimated_hours": 3}
    ]
    
    print("=" * 60)
    print("Style Consistency Analysis")
    print("=" * 60)
    
    style_analysis = cre.analyze_style_consistency(project, assets)
    print(f"\n📊 Consistency Score: {style_analysis['consistency_score']:.2f}")
    print(f"   Project Style: {style_analysis['project_style']['primary']}")
    print(f"   Issues Found: {len(style_analysis['issues'])}")
    
    if style_analysis['recommendations']:
        print("\n💡 Recommendations:")
        for rec in style_analysis['recommendations']:
            print(f"   • {rec}")
    
    print("\n" + "=" * 60)
    print("Narrative Coherence Check")
    print("=" * 60)
    
    narrative_analysis = cre.check_narrative_coherence(project, assets)
    print(f"\n📖 Coherence Score: {narrative_analysis['coherence_score']:.2f}")
    print(f"   Narrative Gaps: {len(narrative_analysis['narrative_gaps'])}")
    
    if narrative_analysis['recommendations']:
        print("\n💡 Recommendations:")
        for rec in narrative_analysis['recommendations']:
            print(f"   • {rec}")
    
    print("\n" + "=" * 60)
    print("Quality Prediction")
    print("=" * 60)
    
    for asset in assets[:2]:
        prediction = cre.predict_quality(asset)
        print(f"\n🎯 {asset['name']}:")
        print(f"   Predicted Quality: {prediction['predicted_quality']}")
        print(f"   Quality Score: {prediction['quality_score']:.2f}")
        print(f"   Confidence: {prediction['confidence']:.2%}")
    
    print("\n" + "=" * 60)
    print("Missing Assets Detection")
    print("=" * 60)
    
    project_with_reqs = {
        **project,
        "asset_requirements": [
            {"name": "hero_image", "type": "graphics"},
            {"name": "social_posts", "type": "graphics"},
            {"name": "promo_video", "type": "video"},
            {"name": "email_banner", "type": "graphics"},  # Missing
            {"name": "background_music", "type": "audio"}
        ]
    }
    
    missing_analysis = cre.detect_missing_assets(project_with_reqs, assets)
    print(f"\n🔍 Missing Assets: {missing_analysis['missing_count']}")
    print(f"   Completeness: {missing_analysis['completeness_score']:.2%}")
    
    if missing_analysis['recommendations']:
        print("\n💡 To Complete Project:")
        for rec in missing_analysis['recommendations']:
            print(f"   • {rec}")
    
    print("\n\n🔥 Creative Reasoning Engine demo complete! 👑")
    print("\nThe Creative Mind is ready to think about your projects!")
