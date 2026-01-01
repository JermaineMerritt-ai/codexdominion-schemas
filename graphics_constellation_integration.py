"""
🎨 Graphics Constellation Integration - Creative Universe Mapping
==================================================================

Maps AI-generated images to creative universe clusters for exploration and discovery.
Similar to Audio Studio Phase 8's constellation system but for images.

Features:
- Color palette clustering (warm, cool, monochrome, vibrant, etc.)
- Style family grouping (photographic, artistic, abstract, etc.)
- Composition patterns (portrait, landscape, close-up, etc.)
- Similar image search using visual embeddings
- Constellation visualization for D3.js/Cytoscape

Usage:
------
from graphics_constellation_integration import GraphicsConstellationIntegration

constellation = GraphicsConstellationIntegration()

# Auto-assign image to clusters
constellation.auto_assign_cluster(asset_id="img_123")

# Query constellation
results = constellation.query_constellation(
    style_family="photographic",
    color_palette="warm",
    tags=["portrait", "outdoor"]
)

# Find similar images
similar = constellation.find_similar_images(asset_id="img_123", limit=10)

# Visualize lineage
graph_data = constellation.visualize_lineage(asset_id="img_123")
"""

import os
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from db import SessionLocal
from models import GraphicsProject
from graphics_evolution_engine import GraphicsEvolutionEngine


class GraphicsConstellationIntegration:
    """
    Creative universe mapping for AI-generated images
    
    Organizes images into thematic clusters:
    - Color Palette Clusters (12): warm, cool, monochrome, vibrant, pastel, neon, earth, jewel, vintage, muted, bright, dark
    - Style Family Clusters (8): photographic, painterly, abstract, minimalist, surrealist, fantasy, sci-fi, vintage
    - Composition Clusters (6): portrait, landscape, close-up, wide-shot, symmetrical, dynamic
    """
    
    def __init__(self, session=None):
        self.session = session or SessionLocal()
        self.evolution_engine = GraphicsEvolutionEngine(session=self.session)
        
        # Predefined constellation clusters
        self.color_clusters = {
            "warm_palette": {"keywords": ["warm", "orange", "red", "yellow", "sunset", "fire"], "color": "#F97316"},
            "cool_palette": {"keywords": ["cool", "blue", "cyan", "ice", "ocean", "winter"], "color": "#3B82F6"},
            "monochrome": {"keywords": ["black", "white", "gray", "noir", "minimal"], "color": "#6B7280"},
            "vibrant": {"keywords": ["vibrant", "saturated", "bold", "bright", "colorful"], "color": "#EC4899"},
            "pastel": {"keywords": ["pastel", "soft", "gentle", "muted", "subtle"], "color": "#C084FC"},
            "neon": {"keywords": ["neon", "electric", "glow", "fluorescent", "bright"], "color": "#22D3EE"},
            "earth_tones": {"keywords": ["earth", "brown", "tan", "natural", "organic"], "color": "#92400E"},
            "jewel_tones": {"keywords": ["jewel", "rich", "deep", "emerald", "sapphire", "ruby"], "color": "#7C3AED"},
            "vintage": {"keywords": ["vintage", "sepia", "aged", "retro", "old"], "color": "#78350F"},
            "muted": {"keywords": ["muted", "desaturated", "faded", "washed"], "color": "#9CA3AF"},
            "bright": {"keywords": ["bright", "luminous", "radiant", "brilliant"], "color": "#FCD34D"},
            "dark": {"keywords": ["dark", "shadow", "noir", "mysterious", "moody"], "color": "#1F2937"}
        }
        
        self.style_clusters = {
            "photographic": {"keywords": ["photo", "realistic", "photograph", "portrait", "candid"], "color": "#10B981"},
            "painterly": {"keywords": ["painted", "oil", "watercolor", "brush", "artistic"], "color": "#F59E0B"},
            "abstract": {"keywords": ["abstract", "geometric", "pattern", "shapes"], "color": "#8B5CF6"},
            "minimalist": {"keywords": ["minimal", "simple", "clean", "sparse"], "color": "#64748B"},
            "surrealist": {"keywords": ["surreal", "dream", "fantasy", "impossible"], "color": "#EC4899"},
            "fantasy": {"keywords": ["fantasy", "magical", "mythical", "enchanted"], "color": "#A855F7"},
            "sci_fi": {"keywords": ["sci-fi", "futuristic", "cyberpunk", "tech"], "color": "#06B6D4"},
            "vintage": {"keywords": ["vintage", "retro", "classic", "nostalgic"], "color": "#EF4444"}
        }
        
        self.composition_clusters = {
            "portrait": {"keywords": ["portrait", "headshot", "face", "person"], "color": "#F97316"},
            "landscape": {"keywords": ["landscape", "panorama", "vista", "scenery"], "color": "#10B981"},
            "close_up": {"keywords": ["close-up", "macro", "detail", "zoom"], "color": "#EC4899"},
            "wide_shot": {"keywords": ["wide", "panoramic", "expansive", "aerial"], "color": "#3B82F6"},
            "symmetrical": {"keywords": ["symmetrical", "balanced", "centered", "mirror"], "color": "#8B5CF6"},
            "dynamic": {"keywords": ["dynamic", "action", "motion", "diagonal"], "color": "#EF4444"}
        }
    
    def auto_assign_cluster(self, asset_id: str) -> List[str]:
        """
        Automatically assign image to appropriate clusters
        
        Analyzes:
        - Color palette from metadata
        - Style keywords from prompt
        - Composition hints from tags
        
        Args:
            asset_id: ID of image to cluster
        
        Returns:
            List of assigned cluster names
        """
        project = self.session.query(GraphicsProject).filter_by(id=asset_id).first()
        
        if not project:
            return []
        
        assigned_clusters = []
        
        # Analyze color palette
        if project.color_palette:
            color_matches = self._match_color_clusters(project.color_palette)
            assigned_clusters.extend(color_matches)
        
        # Analyze style from prompt and tags
        style_text = f"{project.prompt} {project.tags or ''} {project.mood or ''}".lower()
        style_matches = self._match_style_clusters(style_text)
        assigned_clusters.extend(style_matches)
        
        # Analyze composition from camera angle and tags
        composition_text = f"{project.camera_angle or ''} {project.tags or ''}".lower()
        composition_matches = self._match_composition_clusters(composition_text)
        assigned_clusters.extend(composition_matches)
        
        # Store cluster assignments in project tags
        if assigned_clusters:
            existing_tags = set(project.tags.split(',')) if project.tags else set()
            cluster_tags = set([f"cluster:{c}" for c in assigned_clusters])
            all_tags = existing_tags.union(cluster_tags)
            project.tags = ','.join(all_tags)
            self.session.commit()
        
        return assigned_clusters
    
    def _match_color_clusters(self, color_palette: str) -> List[str]:
        """Match color palette to color clusters"""
        matches = []
        palette_lower = color_palette.lower()
        
        for cluster_name, cluster_data in self.color_clusters.items():
            for keyword in cluster_data["keywords"]:
                if keyword in palette_lower:
                    matches.append(cluster_name)
                    break
        
        return matches
    
    def _match_style_clusters(self, text: str) -> List[str]:
        """Match text to style clusters"""
        matches = []
        
        for cluster_name, cluster_data in self.style_clusters.items():
            for keyword in cluster_data["keywords"]:
                if keyword in text:
                    matches.append(cluster_name)
                    break
        
        return matches
    
    def _match_composition_clusters(self, text: str) -> List[str]:
        """Match text to composition clusters"""
        matches = []
        
        for cluster_name, cluster_data in self.composition_clusters.items():
            for keyword in cluster_data["keywords"]:
                if keyword in text:
                    matches.append(cluster_name)
                    break
        
        return matches
    
    def query_constellation(
        self,
        style_family: Optional[str] = None,
        color_palette: Optional[str] = None,
        composition: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Query constellation for matching images
        
        Args:
            style_family: Style cluster name (e.g., "photographic")
            color_palette: Color cluster name (e.g., "warm_palette")
            composition: Composition cluster name (e.g., "portrait")
            tags: Additional tags to filter by
            limit: Max number of results
        
        Returns:
            {
                "total_found": 25,
                "clusters": {
                    "warm_palette": [{"id": "img_1", "prompt": "...", ...}, ...],
                    "photographic": [...]
                },
                "query": {...}
            }
        """
        # Build query
        query = self.session.query(GraphicsProject)
        
        # Filter by cluster tags
        cluster_filters = []
        if style_family:
            cluster_filters.append(f"cluster:{style_family}")
        if color_palette:
            cluster_filters.append(f"cluster:{color_palette}")
        if composition:
            cluster_filters.append(f"cluster:{composition}")
        
        if cluster_filters:
            for cluster_tag in cluster_filters:
                query = query.filter(GraphicsProject.tags.contains(cluster_tag))
        
        # Filter by additional tags
        if tags:
            for tag in tags:
                query = query.filter(GraphicsProject.tags.contains(tag))
        
        # Execute query
        projects = query.limit(limit).all()
        
        # Group by clusters
        clustered_results = {}
        for project in projects:
            project_data = {
                "id": str(project.id),
                "prompt": project.prompt,
                "thumbnail_url": project.thumbnail_url,
                "mood": project.mood,
                "color_palette": project.color_palette,
                "tags": project.tags,
                "timestamp": project.timestamp.isoformat() + "Z"
            }
            
            # Extract cluster assignments
            if project.tags:
                project_clusters = [tag.replace("cluster:", "") for tag in project.tags.split(',') if tag.startswith("cluster:")]
                for cluster in project_clusters:
                    if cluster not in clustered_results:
                        clustered_results[cluster] = []
                    clustered_results[cluster].append(project_data)
        
        return {
            "total_found": len(projects),
            "clusters": clustered_results,
            "query": {
                "style_family": style_family,
                "color_palette": color_palette,
                "composition": composition,
                "tags": tags
            }
        }
    
    def find_similar_images(
        self,
        asset_id: str,
        limit: int = 10,
        similarity_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Find images similar to given image
        
        Uses:
        - Shared cluster assignments (color, style, composition)
        - Common tags
        - Same mood/palette
        - Visual embedding similarity (if available)
        
        Args:
            asset_id: Source image ID
            limit: Max number of similar images
            similarity_threshold: Minimum similarity score (0.0-1.0)
        
        Returns:
            List of similar images with similarity scores
        """
        source_project = self.session.query(GraphicsProject).filter_by(id=asset_id).first()
        
        if not source_project:
            return []
        
        # Extract source clusters
        source_clusters = set()
        if source_project.tags:
            source_clusters = set([tag.replace("cluster:", "") for tag in source_project.tags.split(',') if tag.startswith("cluster:")])
        
        # Extract source tags (non-cluster)
        source_tags = set()
        if source_project.tags:
            source_tags = set([tag for tag in source_project.tags.split(',') if not tag.startswith("cluster:")])
        
        # Find candidates with shared clusters
        candidates = self.session.query(GraphicsProject).filter(
            GraphicsProject.id != asset_id
        ).all()
        
        # Calculate similarity scores
        similarities = []
        for candidate in candidates:
            score = self._calculate_similarity(
                source_project, candidate,
                source_clusters, source_tags
            )
            
            if score >= similarity_threshold:
                similarities.append({
                    "id": str(candidate.id),
                    "prompt": candidate.prompt,
                    "thumbnail_url": candidate.thumbnail_url,
                    "similarity_score": round(score, 3),
                    "shared_clusters": self._get_shared_clusters(source_project, candidate),
                    "shared_tags": self._get_shared_tags(source_tags, candidate.tags),
                    "timestamp": candidate.timestamp.isoformat() + "Z"
                })
        
        # Sort by similarity score (descending)
        similarities.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        return similarities[:limit]
    
    def _calculate_similarity(
        self,
        source: GraphicsProject,
        candidate: GraphicsProject,
        source_clusters: set,
        source_tags: set
    ) -> float:
        """Calculate similarity score between two images"""
        score = 0.0
        
        # Cluster similarity (40% weight)
        if candidate.tags:
            candidate_clusters = set([tag.replace("cluster:", "") for tag in candidate.tags.split(',') if tag.startswith("cluster:")])
            if source_clusters and candidate_clusters:
                cluster_overlap = len(source_clusters.intersection(candidate_clusters))
                cluster_total = len(source_clusters.union(candidate_clusters))
                score += (cluster_overlap / cluster_total) * 0.4
        
        # Tag similarity (30% weight)
        if candidate.tags:
            candidate_tags = set([tag for tag in candidate.tags.split(',') if not tag.startswith("cluster:")])
            if source_tags and candidate_tags:
                tag_overlap = len(source_tags.intersection(candidate_tags))
                tag_total = len(source_tags.union(candidate_tags))
                score += (tag_overlap / tag_total) * 0.3
        
        # Mood match (15% weight)
        if source.mood and candidate.mood and source.mood.lower() == candidate.mood.lower():
            score += 0.15
        
        # Color palette match (15% weight)
        if source.color_palette and candidate.color_palette:
            if source.color_palette.lower() == candidate.color_palette.lower():
                score += 0.15
            elif any(word in candidate.color_palette.lower() for word in source.color_palette.lower().split()):
                score += 0.075
        
        return score
    
    def _get_shared_clusters(self, source: GraphicsProject, candidate: GraphicsProject) -> List[str]:
        """Get shared cluster assignments"""
        if not source.tags or not candidate.tags:
            return []
        
        source_clusters = set([tag.replace("cluster:", "") for tag in source.tags.split(',') if tag.startswith("cluster:")])
        candidate_clusters = set([tag.replace("cluster:", "") for tag in candidate.tags.split(',') if tag.startswith("cluster:")])
        
        return list(source_clusters.intersection(candidate_clusters))
    
    def _get_shared_tags(self, source_tags: set, candidate_tags_str: Optional[str]) -> List[str]:
        """Get shared non-cluster tags"""
        if not candidate_tags_str:
            return []
        
        candidate_tags = set([tag for tag in candidate_tags_str.split(',') if not tag.startswith("cluster:")])
        
        return list(source_tags.intersection(candidate_tags))
    
    def visualize_lineage(self, asset_id: str) -> Dict[str, Any]:
        """
        Generate D3.js/Cytoscape visualization data for lineage
        
        Args:
            asset_id: ID of image to visualize
        
        Returns:
            {
                "nodes": [{id, label, type, generation, cluster_color}, ...],
                "edges": [{source, target, relationship, method}, ...],
                "layout": "hierarchical"
            }
        """
        # Get lineage from evolution engine
        lineage = self.evolution_engine.get_lineage_tree(asset_id)
        
        if "error" in lineage:
            return {"error": lineage["error"]}
        
        nodes = []
        edges = []
        
        # Current node
        current_project = self.session.query(GraphicsProject).filter_by(id=asset_id).first()
        if current_project:
            nodes.append({
                "id": asset_id,
                "label": current_project.prompt[:40] + "..." if len(current_project.prompt) > 40 else current_project.prompt,
                "type": "current",
                "generation": lineage.get("generation", 1),
                "cluster_color": self._get_primary_cluster_color(current_project),
                "thumbnail": current_project.thumbnail_url
            })
        
        # Ancestor nodes
        for ancestor in lineage.get("ancestors", []):
            nodes.append({
                "id": ancestor["asset_id"],
                "label": ancestor["prompt"][:40] + "..." if len(ancestor["prompt"]) > 40 else ancestor["prompt"],
                "type": "ancestor",
                "generation": ancestor["generation"],
                "depth": ancestor["depth"],
                "cluster_color": "#94A3B8"
            })
            
            # Edge from ancestor to child
            edges.append({
                "source": ancestor["asset_id"],
                "target": asset_id if ancestor["depth"] == 1 else "child_id",  # Simplified
                "relationship": ancestor["relationship"],
                "method": ancestor.get("source", "unknown")
            })
        
        # Descendant nodes
        def add_descendants(parent_id: str, descendants: List[Dict]):
            for desc in descendants:
                nodes.append({
                    "id": desc["asset_id"],
                    "label": desc["prompt"][:40] + "..." if len(desc["prompt"]) > 40 else desc["prompt"],
                    "type": "descendant",
                    "generation": desc["generation"],
                    "depth": desc["depth"],
                    "cluster_color": "#94A3B8"
                })
                
                edges.append({
                    "source": parent_id,
                    "target": desc["asset_id"],
                    "relationship": desc["relationship"],
                    "method": desc.get("source", "unknown")
                })
                
                # Recursive for grandchildren
                if "children" in desc and desc["children"]:
                    add_descendants(desc["asset_id"], desc["children"])
        
        add_descendants(asset_id, lineage.get("descendants", []))
        
        return {
            "nodes": nodes,
            "edges": edges,
            "layout": "hierarchical",
            "total_nodes": len(nodes),
            "total_edges": len(edges)
        }
    
    def _get_primary_cluster_color(self, project: GraphicsProject) -> str:
        """Get color for primary cluster assignment"""
        if not project.tags:
            return "#64748B"
        
        clusters = [tag.replace("cluster:", "") for tag in project.tags.split(',') if tag.startswith("cluster:")]
        
        if not clusters:
            return "#64748B"
        
        # Check style clusters first
        for cluster in clusters:
            if cluster in self.style_clusters:
                return self.style_clusters[cluster]["color"]
        
        # Then color clusters
        for cluster in clusters:
            if cluster in self.color_clusters:
                return self.color_clusters[cluster]["color"]
        
        # Finally composition clusters
        for cluster in clusters:
            if cluster in self.composition_clusters:
                return self.composition_clusters[cluster]["color"]
        
        return "#64748B"
    
    def get_constellation_map(
        self,
        cluster_type: str = "all"
    ) -> Dict[str, Any]:
        """
        Get complete constellation map for visualization
        
        Args:
            cluster_type: "color", "style", "composition", or "all"
        
        Returns:
            {
                "clusters": {
                    "warm_palette": {
                        "name": "Warm Palette",
                        "color": "#F97316",
                        "image_count": 45,
                        "sample_images": [...]
                    },
                    ...
                },
                "total_clusters": 26,
                "total_images": 523
            }
        """
        constellation_data = {}
        
        # Select which cluster types to include
        cluster_sets = []
        if cluster_type == "all" or cluster_type == "color":
            cluster_sets.append(("color", self.color_clusters))
        if cluster_type == "all" or cluster_type == "style":
            cluster_sets.append(("style", self.style_clusters))
        if cluster_type == "all" or cluster_type == "composition":
            cluster_sets.append(("composition", self.composition_clusters))
        
        total_images = 0
        
        for cluster_category, clusters_dict in cluster_sets:
            for cluster_name, cluster_info in clusters_dict.items():
                # Query images in this cluster
                cluster_tag = f"cluster:{cluster_name}"
                images = self.session.query(GraphicsProject).filter(
                    GraphicsProject.tags.contains(cluster_tag)
                ).limit(5).all()
                
                image_count = self.session.query(GraphicsProject).filter(
                    GraphicsProject.tags.contains(cluster_tag)
                ).count()
                
                total_images += image_count
                
                constellation_data[cluster_name] = {
                    "name": cluster_name.replace("_", " ").title(),
                    "category": cluster_category,
                    "color": cluster_info["color"],
                    "image_count": image_count,
                    "sample_images": [
                        {
                            "id": str(img.id),
                            "thumbnail_url": img.thumbnail_url,
                            "prompt": img.prompt[:50] + "..." if len(img.prompt) > 50 else img.prompt
                        }
                        for img in images
                    ]
                }
        
        return {
            "clusters": constellation_data,
            "total_clusters": len(constellation_data),
            "total_images": total_images
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    constellation = GraphicsConstellationIntegration()
    
    print("🎨 Graphics Constellation Integration\n")
    print(f"Color clusters: {len(constellation.color_clusters)}")
    print(f"Style clusters: {len(constellation.style_clusters)}")
    print(f"Composition clusters: {len(constellation.composition_clusters)}")
    print(f"Total clusters: {len(constellation.color_clusters) + len(constellation.style_clusters) + len(constellation.composition_clusters)}")
