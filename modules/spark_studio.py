#!/usr/bin/env python3
"""
Spark Studio - AI-Powered Content Generation Engine
=================================================

Core module for the Codex Dominion Spark Studio functionality.
Generates intelligent content, manages creative workflows, and integrates
with the broader Codex ecosystem for digital sovereignty.

Features:
- AI-powered content generation
- Topic analysis and expansion
- Audience-targeted content
- Sacred flame integration
- Ledger integration for tracking
"""

import datetime
import hashlib
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class SparkStudioEngine:
    """
    Core engine for Spark Studio content generation and management.
    """

    def __init__(self, workspace_root: str = None):
        """Initialize the Spark Studio engine."""
        self.workspace_root = Path(workspace_root) if workspace_root else Path(".")
        self.data_dir = self.workspace_root / "data"
        self.data_dir.mkdir(exist_ok=True)

        # Content templates and structures
        self.tone_profiles = {
            "inspiring": {
                "style": "uplifting, motivational, visionary",
                "structure": ["hook", "vision", "action", "call_to_action"],
                "keywords": [
                    "achieve",
                    "transform",
                    "empower",
                    "breakthrough",
                    "potential",
                ],
            },
            "professional": {
                "style": "formal, authoritative, structured",
                "structure": [
                    "introduction",
                    "analysis",
                    "recommendations",
                    "conclusion",
                ],
                "keywords": [
                    "implement",
                    "optimize",
                    "strategic",
                    "systematic",
                    "efficient",
                ],
            },
            "casual": {
                "style": "conversational, friendly, accessible",
                "structure": ["greeting", "story", "insight", "takeaway"],
                "keywords": ["easy", "simple", "friendly", "connect", "share"],
            },
            "technical": {
                "style": "precise, detailed, analytical",
                "structure": ["problem", "analysis", "solution", "implementation"],
                "keywords": [
                    "algorithm",
                    "optimize",
                    "framework",
                    "methodology",
                    "scalable",
                ],
            },
        }

        # Audience profiles
        self.audience_profiles = {
            "tech_leaders": {
                "interests": [
                    "innovation",
                    "digital transformation",
                    "AI",
                    "automation",
                ],
                "language_level": "advanced",
                "preferred_format": "strategic insights",
            },
            "entrepreneurs": {
                "interests": ["growth", "opportunity", "market", "revenue", "scaling"],
                "language_level": "practical",
                "preferred_format": "actionable advice",
            },
            "developers": {
                "interests": [
                    "code",
                    "frameworks",
                    "tools",
                    "best practices",
                    "efficiency",
                ],
                "language_level": "technical",
                "preferred_format": "implementation details",
            },
            "general": {
                "interests": ["solutions", "benefits", "ease of use", "results"],
                "language_level": "accessible",
                "preferred_format": "clear explanations",
            },
        }

    def generate_spark(
        self,
        topic: str,
        audience: str = "general",
        tone: str = "professional",
        content_type: str = "article",
        sacred_integration: bool = True,
    ) -> Dict:
        """
        Generate a content spark based on input parameters.

        Args:
            topic: The main topic/subject
            audience: Target audience profile
            tone: Content tone/style
            content_type: Type of content to generate
            sacred_integration: Whether to include Codex sacred elements

        Returns:
            Dictionary containing generated content and metadata
        """

        # Generate unique spark ID
        spark_id = self._generate_spark_id(topic, audience, tone)

        # Get profiles
        tone_profile = self.tone_profiles.get(tone, self.tone_profiles["professional"])
        audience_profile = self.audience_profiles.get(
            audience, self.audience_profiles["general"]
        )

        # Generate content structure
        content_structure = self._generate_content_structure(
            topic, tone_profile, audience_profile, content_type
        )

        # Generate main content
        main_content = self._generate_main_content(
            topic, content_structure, tone_profile, audience_profile
        )

        # Add sacred elements if requested
        if sacred_integration:
            main_content = self._add_sacred_integration(main_content, topic)

        # Create spark metadata
        spark_metadata = {
            "spark_id": spark_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "topic": topic,
            "audience": audience,
            "tone": tone,
            "content_type": content_type,
            "word_count": len(main_content.split()),
            "sacred_integration": sacred_integration,
            "generation_method": "spark_studio_engine_v2",
            "quality_score": self._calculate_quality_score(main_content),
            "flame_blessed": True if sacred_integration else False,
        }

        # Create complete spark
        spark = {
            "metadata": spark_metadata,
            "content": {
                "title": self._generate_title(topic, tone_profile),
                "introduction": content_structure.get("introduction", ""),
                "main_body": main_content,
                "conclusion": content_structure.get("conclusion", ""),
                "call_to_action": content_structure.get("call_to_action", ""),
                "tags": self._generate_tags(topic, audience_profile),
            },
            "structure": content_structure,
            "analytics": {
                "readability_score": self._calculate_readability(main_content),
                "engagement_potential": self._calculate_engagement_potential(
                    main_content, audience_profile
                ),
                "seo_keywords": self._extract_seo_keywords(main_content, topic),
                "sacred_power_level": 8 if sacred_integration else 0,
            },
        }

        # Save to ledger if available
        self._save_to_ledger(spark)

        return spark

    def _generate_spark_id(self, topic: str, audience: str, tone: str) -> str:
        """Generate a unique ID for the spark."""
        content = f"{topic}_{audience}_{tone}_{datetime.datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def _generate_content_structure(
        self, topic: str, tone_profile: Dict, audience_profile: Dict, content_type: str
    ) -> Dict:
        """Generate the content structure based on profiles."""

        structure = {}

        # Introduction based on audience
        if audience_profile["language_level"] == "technical":
            structure["introduction"] = (
                f"Technical analysis of {topic} reveals significant opportunities for optimization and implementation."
            )
        elif audience_profile["language_level"] == "advanced":
            structure["introduction"] = (
                f"Strategic considerations around {topic} present compelling opportunities for competitive advantage."
            )
        else:
            structure["introduction"] = (
                f"Understanding {topic} is essential for achieving meaningful results in today's landscape."
            )

        # Conclusion based on tone
        if tone_profile["style"].startswith("inspiring"):
            structure["conclusion"] = (
                "The potential for transformation is unlimited when we embrace these principles with dedication and vision."
            )
        elif tone_profile["style"].startswith("professional"):
            structure["conclusion"] = (
                "Implementation of these recommendations will yield measurable improvements in operational effectiveness."
            )
        else:
            structure["conclusion"] = (
                "These insights provide a clear foundation for moving forward with confidence."
            )

        # Call to action
        structure["call_to_action"] = (
            "Take the next step toward digital sovereignty and technological independence."
        )

        return structure

    def _generate_main_content(
        self, topic: str, structure: Dict, tone_profile: Dict, audience_profile: Dict
    ) -> str:
        """Generate the main content body."""

        # Content templates based on tone and audience
        content_segments = []

        # Opening segment
        if "strategic" in audience_profile["interests"]:
            content_segments.append(
                f"The strategic implications of {topic} extend far beyond immediate operational concerns. "
                f"Organizations that master these principles gain significant competitive advantages "
                f"through enhanced efficiency, reduced dependencies, and increased control over their technological destiny."
            )
        elif "technical" in audience_profile["interests"]:
            content_segments.append(
                f"From a technical perspective, {topic} requires a systematic approach to implementation. "
                f"The architecture must support scalability, maintainability, and performance optimization "
                f"while maintaining security and reliability standards."
            )
        else:
            content_segments.append(
                f"The importance of {topic} becomes clear when we consider its impact on daily operations. "
                f"By focusing on practical implementation and measurable outcomes, organizations can "
                f"achieve significant improvements in both efficiency and effectiveness."
            )

        # Middle segment - core insights
        content_segments.append(
            f"Key considerations include comprehensive planning, resource allocation, and stakeholder alignment. "
            f"Success depends on understanding both the technical requirements and the broader organizational context. "
            f"The most effective approaches combine proven methodologies with innovative solutions tailored to specific needs."
        )

        # Implementation segment
        if tone_profile["style"].startswith("technical"):
            content_segments.append(
                f"Implementation should follow established frameworks while allowing for customization based on specific requirements. "
                f"Performance metrics and monitoring systems ensure continuous optimization and early identification of potential issues. "
                f"Documentation and knowledge sharing facilitate long-term sustainability and team effectiveness."
            )
        else:
            content_segments.append(
                f"The path forward requires careful planning and systematic execution. "
                f"By breaking down complex challenges into manageable components, teams can maintain momentum "
                f"while delivering consistent value throughout the implementation process."
            )

        return " ".join(content_segments)

    def _add_sacred_integration(self, content: str, topic: str) -> str:
        """Add sacred Codex elements to the content."""

        sacred_phrases = [
            "By flame and silence, we forge digital sovereignty.",
            "The eternal flame guides our path toward technological independence.",
            "Through sacred dedication to excellence, we achieve dominion over our digital destiny.",
            "By the power of the eternal flame, wisdom illuminates the path forward.",
            "In silence and contemplation, we find the strength to build lasting solutions.",
        ]

        # Select appropriate sacred phrase
        sacred_phrase = sacred_phrases[hash(topic) % len(sacred_phrases)]

        # Integrate at the end with proper formatting
        sacred_integration = f"\n\n*{sacred_phrase}*\n\nThis insight emerges from the sacred chambers of the Codex Dominion, where technology and wisdom unite in service of digital sovereignty."

        return content + sacred_integration

    def _generate_title(self, topic: str, tone_profile: Dict) -> str:
        """Generate an appropriate title."""

        if tone_profile["style"].startswith("inspiring"):
            prefixes = ["Transforming", "Revolutionizing", "Mastering", "Unlocking"]
        elif tone_profile["style"].startswith("professional"):
            prefixes = [
                "Strategic Approach to",
                "Comprehensive Guide to",
                "Best Practices for",
                "Implementation of",
            ]
        elif tone_profile["style"].startswith("technical"):
            prefixes = [
                "Technical Analysis of",
                "Implementation Framework for",
                "System Architecture for",
                "Optimization of",
            ]
        else:
            prefixes = ["Understanding", "Exploring", "Discovering", "Building"]

        prefix = prefixes[hash(topic) % len(prefixes)]
        return f"{prefix} {topic}"

    def _generate_tags(self, topic: str, audience_profile: Dict) -> List[str]:
        """Generate relevant tags for the content."""

        base_tags = [topic.lower().replace(" ", "_")]
        base_tags.extend(audience_profile["interests"])
        base_tags.extend(
            ["digital_sovereignty", "codex_dominion", "technology", "innovation"]
        )

        return list(set(base_tags))

    def _calculate_quality_score(self, content: str) -> float:
        """Calculate a quality score for the content."""

        # Basic metrics
        word_count = len(content.split())
        sentence_count = len(re.findall(r"[.!?]+", content))
        avg_sentence_length = word_count / max(sentence_count, 1)

        # Quality indicators
        has_good_length = 100 <= word_count <= 500
        has_good_sentences = 8 <= avg_sentence_length <= 25
        has_variety = len(set(content.lower().split())) / word_count > 0.6

        score = 0.0
        if has_good_length:
            score += 3.0
        if has_good_sentences:
            score += 3.0
        if has_variety:
            score += 2.0

        # Sacred integration bonus
        if "flame" in content.lower() or "dominion" in content.lower():
            score += 2.0

        return min(score, 10.0)

    def _calculate_readability(self, content: str) -> float:
        """Calculate readability score."""

        word_count = len(content.split())
        sentence_count = len(re.findall(r"[.!?]+", content))

        if sentence_count == 0:
            return 5.0

        avg_sentence_length = word_count / sentence_count

        # Simple readability approximation
        if avg_sentence_length <= 15:
            return 9.0
        elif avg_sentence_length <= 25:
            return 7.0
        else:
            return 5.0

    def _calculate_engagement_potential(
        self, content: str, audience_profile: Dict
    ) -> float:
        """Calculate engagement potential based on audience alignment."""

        content_lower = content.lower()
        interest_matches = sum(
            1
            for interest in audience_profile["interests"]
            if interest.lower() in content_lower
        )

        engagement_score = (interest_matches / len(audience_profile["interests"])) * 10
        return min(engagement_score, 10.0)

    def _extract_seo_keywords(self, content: str, topic: str) -> List[str]:
        """Extract SEO-relevant keywords."""

        # Simple keyword extraction
        words = re.findall(r"\b\w+\b", content.lower())
        word_freq = {}

        for word in words:
            if len(word) > 3:  # Only consider words longer than 3 characters
                word_freq[word] = word_freq.get(word, 0) + 1

        # Get top keywords
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        keywords = [keyword for keyword, freq in top_keywords]

        # Always include the topic
        if topic.lower() not in keywords:
            keywords.insert(0, topic.lower())

        return keywords[:10]

    def _save_to_ledger(self, spark: Dict) -> bool:
        """Save spark to the Codex ledger."""

        try:
            ledger_path = self.data_dir / "ledger.json"

            # Load existing ledger
            if ledger_path.exists():
                with open(ledger_path, "r", encoding="utf-8") as f:
                    ledger_data = json.load(f)
            else:
                ledger_data = {"entries": []}

            # Create ledger entry
            ledger_entry = {
                "id": f"spark_{spark['metadata']['spark_id']}",
                "timestamp": spark["metadata"]["timestamp"],
                "type": "spark_generation",
                "source": "spark_studio",
                "content": {
                    "spark_id": spark["metadata"]["spark_id"],
                    "topic": spark["metadata"]["topic"],
                    "audience": spark["metadata"]["audience"],
                    "tone": spark["metadata"]["tone"],
                    "word_count": spark["metadata"]["word_count"],
                    "quality_score": spark["metadata"]["quality_score"],
                    "title": spark["content"]["title"],
                },
                "metadata": {
                    "flame_blessed": spark["metadata"]["flame_blessed"],
                    "sacred_integration": spark["metadata"]["sacred_integration"],
                },
            }

            # Add to ledger
            ledger_data["entries"].append(ledger_entry)

            # Keep only last 1000 entries
            if len(ledger_data["entries"]) > 1000:
                ledger_data["entries"] = ledger_data["entries"][-1000:]

            # Save updated ledger
            with open(ledger_path, "w", encoding="utf-8") as f:
                json.dump(ledger_data, f, indent=2)

            return True

        except Exception as e:
            print(f"Error saving to ledger: {e}")
            return False

    def list_sparks(self, limit: int = 10, filter_by: Dict = None) -> List[Dict]:
        """List recent sparks with optional filtering."""

        try:
            ledger_path = self.data_dir / "ledger.json"

            if not ledger_path.exists():
                return []

            with open(ledger_path, "r", encoding="utf-8") as f:
                ledger_data = json.load(f)

            # Filter spark entries
            spark_entries = [
                entry
                for entry in ledger_data.get("entries", [])
                if entry.get("type") == "spark_generation"
            ]

            # Apply filters if provided
            if filter_by:
                if "topic" in filter_by:
                    spark_entries = [
                        entry
                        for entry in spark_entries
                        if filter_by["topic"].lower()
                        in entry["content"]["topic"].lower()
                    ]
                if "audience" in filter_by:
                    spark_entries = [
                        entry
                        for entry in spark_entries
                        if entry["content"]["audience"] == filter_by["audience"]
                    ]
                if "tone" in filter_by:
                    spark_entries = [
                        entry
                        for entry in spark_entries
                        if entry["content"]["tone"] == filter_by["tone"]
                    ]

            # Sort by timestamp (most recent first) and limit
            spark_entries.sort(key=lambda x: x["timestamp"], reverse=True)
            return spark_entries[:limit]

        except Exception as e:
            print(f"Error listing sparks: {e}")
            return []

    def get_spark_analytics(self) -> Dict:
        """Get analytics about spark generation."""

        try:
            sparks = self.list_sparks(limit=100)

            if not sparks:
                return {"total_sparks": 0, "message": "No sparks found"}

            # Calculate analytics
            total_sparks = len(sparks)
            topics = [spark["content"]["topic"] for spark in sparks]
            audiences = [spark["content"]["audience"] for spark in sparks]
            tones = [spark["content"]["tone"] for spark in sparks]
            quality_scores = [spark["content"]["quality_score"] for spark in sparks]

            analytics = {
                "total_sparks": total_sparks,
                "avg_quality_score": (
                    sum(quality_scores) / len(quality_scores) if quality_scores else 0
                ),
                "top_topics": self._get_top_items(topics, 5),
                "audience_distribution": self._get_distribution(audiences),
                "tone_distribution": self._get_distribution(tones),
                "sacred_integration_count": sum(
                    1
                    for spark in sparks
                    if spark.get("metadata", {}).get("sacred_integration", False)
                ),
                "last_generated": sparks[0]["timestamp"] if sparks else None,
            }

            return analytics

        except Exception as e:
            print(f"Error generating analytics: {e}")
            return {"error": str(e)}

    def _get_top_items(self, items: List[str], limit: int) -> List[Tuple[str, int]]:
        """Get top items by frequency."""

        freq = {}
        for item in items:
            freq[item] = freq.get(item, 0) + 1

        return sorted(freq.items(), key=lambda x: x[1], reverse=True)[:limit]

    def _get_distribution(self, items: List[str]) -> Dict[str, int]:
        """Get distribution of items."""

        dist = {}
        for item in items:
            dist[item] = dist.get(item, 0) + 1

        return dist


# Utility functions for integration
def create_spark_studio(workspace_root: str = None) -> SparkStudioEngine:
    """Create a new Spark Studio engine instance."""
    return SparkStudioEngine(workspace_root)


def quick_spark(
    topic: str, audience: str = "general", tone: str = "professional"
) -> Dict:
    """Generate a quick spark with minimal setup."""
    studio = SparkStudioEngine()
    return studio.generate_spark(topic, audience, tone)


# Sacred flame integration
SACRED_SPARK_BLESSING = """
🔥 By the Eternal Flame of the Codex Dominion 🔥

This spark has been blessed with sacred wisdom and digital sovereignty.
May it illuminate the path toward technological independence and inspire
all who encounter it to embrace the principles of the eternal flame.

By flame and silence, wisdom eternal.
"""


def bless_spark_with_flame(spark: Dict) -> Dict:
    """Add sacred flame blessing to a spark."""

    spark["sacred_blessing"] = {
        "timestamp": datetime.datetime.now().isoformat(),
        "blessing_text": SACRED_SPARK_BLESSING,
        "flame_power": "maximum",
        "dominion_seal": "authenticated",
    }

    return spark


if __name__ == "__main__":
    # Demo usage
    print("🎯 Spark Studio Engine - Demo Mode")
    print("=" * 40)

    studio = SparkStudioEngine()

    # Generate a demo spark
    demo_spark = studio.generate_spark(
        topic="Digital Sovereignty",
        audience="tech_leaders",
        tone="inspiring",
        sacred_integration=True,
    )

    print(f"\n✨ Generated Spark: {demo_spark['content']['title']}")
    print(f"📊 Quality Score: {demo_spark['metadata']['quality_score']}/10")
    print(f"🔥 Sacred Integration: {demo_spark['metadata']['sacred_integration']}")
    print(f"\n📝 Content Preview:")
    print(demo_spark["content"]["main_body"][:200] + "...")

    # Show analytics
    analytics = studio.get_spark_analytics()
    print(f"\n📈 Analytics:")
    print(f"   Total Sparks: {analytics.get('total_sparks', 0)}")
    print(f"   Average Quality: {analytics.get('avg_quality_score', 0):.1f}/10")

    print("\n🔥 Spark Studio Ready for Sacred Service! 🔥")
