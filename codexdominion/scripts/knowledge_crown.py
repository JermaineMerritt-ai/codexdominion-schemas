#!/usr/bin/env python3
"""
Knowledge Crown - Sovereign Knowledge Distribution System

Indexes knowledge artifacts and distributes them to Councils,
Schools, and Archives across the Codex Dominion network.
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class KnowledgeIndex:
    """Index and catalog knowledge artifacts"""

    def __init__(self, index_path: str = "manifests/knowledge_index.json"):
        self.index_path = Path(index_path)
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.index: Dict[str, Any] = {}
        self._load_index()

    def _load_index(self) -> None:
        """Load the knowledge index from disk"""
        if self.index_path.exists():
            with open(self.index_path, "r", encoding="utf-8") as f:
                self.index = json.load(f)
        else:
            self._initialize_index()

    def _initialize_index(self) -> None:
        """Initialize a new knowledge index"""
        self.index = {
            "index_version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "total_artifacts": 0,
            "categories": {},
            "tags": {},
            "artifacts": []
        }
        self._save_index()

    def _save_index(self) -> None:
        """Save the index to disk"""
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(self.index, f, indent=2)

    def add_artifact(
        self,
        artifact_id: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add an artifact to the knowledge index"""
        # Extract indexable fields
        category = metadata.get("metadata", {}).get("category", "general")
        tags = metadata.get("metadata", {}).get("tags", [])
        crown = metadata.get("crown", [])

        # Create index entry
        entry = {
            "artifact_id": artifact_id,
            "title": metadata.get("title", "Untitled"),
            "category": category,
            "tags": tags,
            "crown": crown,
            "authors": metadata.get("authors", []),
            "version": metadata.get("version", "1.0.0"),
            "indexed_at": datetime.now().isoformat(),
            "search_terms": self._generate_search_terms(metadata)
        }

        # Update category index
        if category not in self.index["categories"]:
            self.index["categories"][category] = []
        self.index["categories"][category].append(artifact_id)

        # Update tag index
        for tag in tags:
            if tag not in self.index["tags"]:
                self.index["tags"][tag] = []
            self.index["tags"][tag].append(artifact_id)

        # Add to artifacts list
        self.index["artifacts"].append(entry)
        self.index["total_artifacts"] = len(self.index["artifacts"])

        self._save_index()
        return entry

    def _generate_search_terms(self, metadata: Dict[str, Any]) -> List[str]:
        """Generate searchable terms from artifact metadata"""
        terms = []

        # Title words
        title = metadata.get("title", "")
        terms.extend(title.lower().split())

        # Tags
        tags = metadata.get("metadata", {}).get("tags", [])
        terms.extend([tag.lower() for tag in tags])

        # Crown alignments
        crown = metadata.get("crown", [])
        terms.extend([c.lower() for c in crown])

        # Category
        category = metadata.get("metadata", {}).get("category", "")
        if category:
            terms.append(category.lower())

        # Remove duplicates
        return list(set(terms))

    def search(
        self,
        query: str = "",
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        crown: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Search the knowledge index"""
        results = self.index["artifacts"].copy()

        # Filter by query
        if query:
            query_terms = query.lower().split()
            results = [
                a for a in results
                if any(
                    term in a["search_terms"]
                    for term in query_terms
                )
            ]

        # Filter by category
        if category:
            results = [
                a for a in results
                if a["category"] == category
            ]

        # Filter by tags
        if tags:
            results = [
                a for a in results
                if any(tag in a["tags"] for tag in tags)
            ]

        # Filter by crown
        if crown:
            results = [
                a for a in results
                if any(c in a["crown"] for c in crown)
            ]

        return results


class CouncilDistributor:
    """Distribute knowledge artifacts to councils and channels"""

    def __init__(
        self, distribution_path: str = "manifests/distribution_log.json"
    ):
        self.distribution_path = Path(distribution_path)
        self.distribution_path.parent.mkdir(parents=True, exist_ok=True)
        self.councils = self._initialize_councils()
        self.distribution_log: List[Dict[str, Any]] = []
        self._load_log()

    def _initialize_councils(self) -> Dict[str, Dict[str, Any]]:
        """Initialize council registry"""
        return {
            "planetary_schools": {
                "name": "Planetary Schools",
                "type": "education",
                "priority": "high",
                "channels": ["api", "cdn", "email"],
                "artifacts_received": 0
            },
            "sovereign_corporations": {
                "name": "Sovereign Corporations",
                "type": "enterprise",
                "priority": "high",
                "channels": ["api", "cdn"],
                "artifacts_received": 0
            },
            "diaspora_councils": {
                "name": "Diaspora Councils",
                "type": "community",
                "priority": "medium",
                "channels": ["api", "cdn", "social"],
                "artifacts_received": 0
            },
            "ministries_archives": {
                "name": "Ministries & Archives",
                "type": "government",
                "priority": "high",
                "channels": ["api", "secure_transfer"],
                "artifacts_received": 0
            }
        }

    def _load_log(self) -> None:
        """Load distribution log from disk"""
        if self.distribution_path.exists():
            with open(self.distribution_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.distribution_log = data.get("distributions", [])
        else:
            self._save_log()

    def _save_log(self) -> None:
        """Save distribution log to disk"""
        log_data = {
            "log_version": "1.0.0",
            "total_distributions": len(self.distribution_log),
            "councils": self.councils,
            "distributions": self.distribution_log
        }
        with open(self.distribution_path, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2)

    def distribute(
        self,
        artifact_id: str,
        artifact_metadata: Dict[str, Any],
        target_councils: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Distribute an artifact to councils

        Args:
            artifact_id: ID of the artifact to distribute
            artifact_metadata: Artifact metadata
            target_councils: Specific councils (None for all)

        Returns:
            Distribution result with status per council
        """
        if target_councils is None:
            target_councils = list(self.councils.keys())

        distribution = {
            "artifact_id": artifact_id,
            "title": artifact_metadata.get("title", "Untitled"),
            "distributed_at": datetime.now().isoformat(),
            "target_councils": target_councils,
            "results": {}
        }

        for council_id in target_councils:
            if council_id not in self.councils:
                distribution["results"][council_id] = {
                    "status": "error",
                    "message": f"Council not found: {council_id}"
                }
                continue

            council = self.councils[council_id]

            # Simulate distribution based on channels
            channels_used = council["channels"]
            distribution["results"][council_id] = {
                "status": "success",
                "council_name": council["name"],
                "channels": channels_used,
                "priority": council["priority"],
                "delivered_at": datetime.now().isoformat()
            }

            # Update council stats
            council["artifacts_received"] += 1

        # Log distribution
        self.distribution_log.append(distribution)
        self._save_log()

        return distribution

    def get_council_stats(
        self, council_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get distribution statistics for councils"""
        if council_id:
            if council_id in self.councils:
                return self.councils[council_id]
            return {"error": f"Council not found: {council_id}"}

        return {
            "total_councils": len(self.councils),
            "total_distributions": len(self.distribution_log),
            "councils": self.councils
        }


class KnowledgeCrown:
    """
    Knowledge Crown - Sovereign Knowledge Distribution System

    Core capabilities:
    - indexKnowledge(artifact): Index artifacts for search and discovery
    - distributeToCouncils(): Distribute knowledge to councils/channels
    """

    def __init__(self):
        self.knowledge_index = KnowledgeIndex()
        self.council_distributor = CouncilDistributor()
        print("📚 Knowledge Crown initialized")

    def index_knowledge(
        self, artifact_id: str, artifact_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Index a knowledge artifact for search and discovery

        Args:
            artifact_id: Unique identifier for the artifact
            artifact_metadata: Full artifact metadata

        Returns:
            Dictionary with indexing result
        """
        print(f"📖 INDEXING KNOWLEDGE: {artifact_id}")
        print("=" * 60)

        # Add to knowledge index
        entry = self.knowledge_index.add_artifact(
            artifact_id, artifact_metadata
        )

        print(f"✅ Artifact indexed")
        print(f"   Title: {entry['title']}")
        print(f"   Category: {entry['category']}")
        print(f"   Tags: {', '.join(entry['tags'])}")
        print(f"   Crown: {', '.join(entry['crown'])}")
        print(f"   Search terms: {len(entry['search_terms'])} terms")
        print()

        # Get index stats
        stats = {
            "total_artifacts": self.knowledge_index.index["total_artifacts"],
            "categories": len(self.knowledge_index.index["categories"]),
            "tags": len(self.knowledge_index.index["tags"])
        }

        print(f"📊 Index Statistics:")
        print(f"   Total artifacts: {stats['total_artifacts']}")
        print(f"   Categories: {stats['categories']}")
        print(f"   Tags: {stats['tags']}")
        print()

        return {
            "status": "indexed",
            "artifact_id": artifact_id,
            "entry": entry,
            "stats": stats
        }

    def distribute_to_councils(
        self,
        artifact_id: str,
        artifact_metadata: Dict[str, Any],
        target_councils: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Distribute knowledge artifact to councils

        Args:
            artifact_id: ID of the artifact
            artifact_metadata: Artifact metadata
            target_councils: Specific councils (None for all)

        Returns:
            Dictionary with distribution results
        """
        print(f"🌐 DISTRIBUTING TO COUNCILS: {artifact_id}")
        print("=" * 60)

        # Distribute to councils
        distribution = self.council_distributor.distribute(
            artifact_id, artifact_metadata, target_councils
        )

        print(f"✅ Distribution complete")
        print(f"   Artifact: {distribution['title']}")
        print(f"   Councils targeted: {len(distribution['target_councils'])}")
        print()

        # Show results per council
        for council_id, result in distribution["results"].items():
            if result["status"] == "success":
                print(f"   ✅ {result['council_name']}")
                print(f"      Channels: {', '.join(result['channels'])}")
                print(f"      Priority: {result['priority']}")
            else:
                print(f"   ❌ {council_id}: {result['message']}")

        print()

        # Get overall stats
        stats = self.council_distributor.get_council_stats()
        print(f"📊 Distribution Statistics:")
        print(f"   Total councils: {stats['total_councils']}")
        print(f"   Total distributions: {stats['total_distributions']}")
        print()

        return {
            "status": "distributed",
            "distribution": distribution,
            "stats": stats
        }

    def search_knowledge(
        self,
        query: str = "",
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        crown: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Search the knowledge index"""
        return self.knowledge_index.search(query, category, tags, crown)


def main() -> None:
    """Main execution for testing"""
    print("📚 KNOWLEDGE CROWN - SOVEREIGN KNOWLEDGE SYSTEM")
    print("=" * 60)
    print()

    crown = KnowledgeCrown()

    # Example: Index an artifact
    artifact_metadata = {
        "artifactId": "eternal-ledger-001",
        "title": "Eternal Ledger Financial Dashboard",
        "version": "1.0.0",
        "crown": ["Efficiency", "Knowledge", "Commerce"],
        "authors": ["Jermaine Merritt"],
        "metadata": {
            "category": "financial-sovereignty",
            "tags": ["treasury", "ledger", "blockchain", "dashboard"],
            "visibility": "public"
        }
    }

    crown.index_knowledge("eternal-ledger-001", artifact_metadata)

    # Example: Distribute to councils
    crown.distribute_to_councils("eternal-ledger-001", artifact_metadata)

    # Example: Search knowledge
    print("🔍 SEARCHING KNOWLEDGE")
    print("=" * 60)
    results = crown.search_knowledge(query="ledger", crown=["Knowledge"])
    print(f"Found {len(results)} artifacts matching query")
    for result in results:
        print(f"   📄 {result['title']} ({result['artifact_id']})")
    print()


if __name__ == "__main__":
    main()
