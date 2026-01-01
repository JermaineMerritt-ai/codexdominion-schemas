# ============================================================================================
# AUDIO CONSTELLATION INTEGRATION - Audio Universe Mapping
# ============================================================================================
"""
Map audio assets to constellation clusters for creative exploration.

Clusters:
- **Music**: Mood clusters (energetic, calm, dark, bright, dramatic, playful)
- **Voice**: Narrative clusters (authoritative, casual, dramatic, educational, commercial)
- **SFX**: Environmental clusters (nature, urban, mechanical, ambient, impact)

Features:
- Automatic cluster assignment based on metadata
- Similarity search within clusters
- Lineage visualization
- Creative constellation maps
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import json
import math


class AudioConstellationIntegration:
    """Integrate audio assets into constellation system."""
    
    def __init__(self, db):
        """Initialize constellation integration with database."""
        self.db = db
        
        # Define cluster types for each audio category
        self.music_clusters = {
            "energetic": ["high energy", "upbeat", "exciting", "intense", "powerful"],
            "calm": ["peaceful", "relaxing", "gentle", "soft", "serene"],
            "dark": ["ominous", "mysterious", "haunting", "eerie", "brooding"],
            "bright": ["cheerful", "optimistic", "joyful", "light", "sunny"],
            "dramatic": ["epic", "cinematic", "emotional", "soaring", "grand"],
            "playful": ["fun", "quirky", "bouncy", "whimsical", "silly"]
        }
        
        self.voice_clusters = {
            "authoritative": ["confident", "commanding", "professional", "strong"],
            "casual": ["friendly", "conversational", "relaxed", "natural"],
            "dramatic": ["intense", "emotional", "theatrical", "expressive"],
            "educational": ["clear", "instructional", "patient", "informative"],
            "commercial": ["persuasive", "engaging", "polished", "promotional"],
            "narrative": ["storytelling", "descriptive", "immersive", "vocal"]
        }
        
        self.sfx_clusters = {
            "nature": ["outdoor", "wildlife", "weather", "organic", "environmental"],
            "urban": ["city", "traffic", "crowd", "industrial", "street"],
            "mechanical": ["machine", "motor", "electronic", "technical", "robotic"],
            "ambient": ["background", "atmosphere", "room tone", "texture"],
            "impact": ["hit", "crash", "bang", "thud", "slam"],
            "musical": ["tonal", "melodic", "harmonic", "rhythmic"]
        }
    
    # ========== CLUSTER MANAGEMENT ==========
    
    def create_cluster(
        self,
        cluster_name: str,
        cluster_type: str,  # mood, genre, style
        audio_type: str,  # music, voice, sfx
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new constellation cluster.
        
        Args:
            cluster_name: Name of cluster (e.g., "Energetic Music")
            cluster_type: Type of cluster (mood, genre, style)
            audio_type: Audio type (music, voice, sfx)
            metadata: Additional cluster metadata
        
        Returns:
            Dict with cluster info
        """
        from flask_dashboard import ConstellationCluster
        
        try:
            # Create cluster
            cluster = ConstellationCluster(
                name=cluster_name,
                cluster_type=cluster_type,
                audio_type=audio_type,
                metadata_json=json.dumps(metadata or {})
            )
            
            self.db.session.add(cluster)
            self.db.session.commit()
            
            return {
                "success": True,
                "cluster_id": cluster.id,
                "name": cluster.name,
                "type": cluster_type,
                "audio_type": audio_type
            }
        
        except Exception as e:
            self.db.session.rollback()
            return {"success": False, "error": str(e)}
    
    def auto_assign_cluster(self, asset_id: int) -> Dict[str, Any]:
        """Automatically assign asset to appropriate clusters.
        
        Args:
            asset_id: Audio asset ID
        
        Returns:
            Dict with assigned clusters
        """
        from flask_dashboard import AudioAsset, ConstellationCluster, ConstellationNode
        
        try:
            # Get asset
            asset = AudioAsset.query.get(asset_id)
            if not asset:
                return {"success": False, "error": "Asset not found"}
            
            # Parse metadata
            metadata = json.loads(asset.metadata_json or "{}")
            tags = metadata.get("tags", [])
            
            # Determine clusters based on audio type and tags
            assigned_clusters = []
            
            if asset.asset_type == "music":
                clusters = self._assign_music_clusters(tags, metadata)
            elif asset.asset_type == "voice" or asset.asset_type == "voiceover":
                clusters = self._assign_voice_clusters(tags, metadata)
            elif asset.asset_type == "sfx" or asset.asset_type == "ambient":
                clusters = self._assign_sfx_clusters(tags, metadata)
            else:
                clusters = []
            
            # Create or get clusters and add asset
            for cluster_name in clusters:
                cluster = ConstellationCluster.query.filter_by(
                    name=cluster_name,
                    audio_type=asset.asset_type
                ).first()
                
                if not cluster:
                    # Create cluster if it doesn't exist
                    cluster = ConstellationCluster(
                        name=cluster_name,
                        cluster_type="mood",
                        audio_type=asset.asset_type
                    )
                    self.db.session.add(cluster)
                    self.db.session.flush()
                
                # Check if node already exists
                existing_node = ConstellationNode.query.filter_by(
                    cluster_id=cluster.id,
                    asset_id=asset_id
                ).first()
                
                if not existing_node:
                    # Create constellation node
                    node = ConstellationNode(
                        cluster_id=cluster.id,
                        asset_id=asset_id,
                        position_x=0.0,  # Will be calculated for visualization
                        position_y=0.0
                    )
                    self.db.session.add(node)
                
                assigned_clusters.append(cluster_name)
            
            self.db.session.commit()
            
            return {
                "success": True,
                "asset_id": asset_id,
                "assigned_clusters": assigned_clusters,
                "cluster_count": len(assigned_clusters)
            }
        
        except Exception as e:
            self.db.session.rollback()
            return {"success": False, "error": str(e)}
    
    def _assign_music_clusters(self, tags: List[str], metadata: Dict[str, Any]) -> List[str]:
        """Assign music to mood clusters based on tags and metadata."""
        assigned = []
        tags_lower = [t.lower() for t in tags]
        
        # Check each music cluster
        for cluster_name, keywords in self.music_clusters.items():
            # Check if any keywords match tags
            for keyword in keywords:
                if any(keyword in tag for tag in tags_lower):
                    assigned.append(f"{cluster_name.capitalize()} Music")
                    break
        
        # Also check tempo
        tempo = metadata.get("tempo")
        if tempo:
            if tempo > 140:
                assigned.append("Energetic Music")
            elif tempo < 80:
                assigned.append("Calm Music")
        
        # Default if no match
        if not assigned:
            assigned.append("General Music")
        
        return list(set(assigned))  # Remove duplicates
    
    def _assign_voice_clusters(self, tags: List[str], metadata: Dict[str, Any]) -> List[str]:
        """Assign voice to narrative clusters based on tags and metadata."""
        assigned = []
        tags_lower = [t.lower() for t in tags]
        
        # Check each voice cluster
        for cluster_name, keywords in self.voice_clusters.items():
            for keyword in keywords:
                if any(keyword in tag for tag in tags_lower):
                    assigned.append(f"{cluster_name.capitalize()} Voice")
                    break
        
        # Check emotion if available
        emotion = metadata.get("emotion")
        if emotion:
            if emotion in ["confident", "strong"]:
                assigned.append("Authoritative Voice")
            elif emotion in ["happy", "cheerful"]:
                assigned.append("Casual Voice")
            elif emotion in ["sad", "angry"]:
                assigned.append("Dramatic Voice")
        
        # Default if no match
        if not assigned:
            assigned.append("General Voice")
        
        return list(set(assigned))
    
    def _assign_sfx_clusters(self, tags: List[str], metadata: Dict[str, Any]) -> List[str]:
        """Assign SFX to environmental clusters based on tags and metadata."""
        assigned = []
        tags_lower = [t.lower() for t in tags]
        
        # Check each SFX cluster
        for cluster_name, keywords in self.sfx_clusters.items():
            for keyword in keywords:
                if any(keyword in tag for tag in tags_lower):
                    assigned.append(f"{cluster_name.capitalize()} SFX")
                    break
        
        # Check impact strength
        impact_strength = metadata.get("impact_strength")
        if impact_strength and impact_strength > 0.7:
            assigned.append("Impact SFX")
        
        # Default if no match
        if not assigned:
            assigned.append("General SFX")
        
        return list(set(assigned))
    
    # ========== CONSTELLATION QUERIES ==========
    
    def query_constellation(
        self,
        audio_type: Optional[str] = None,
        cluster_name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """Query constellation for audio assets.
        
        Args:
            audio_type: Filter by audio type
            cluster_name: Filter by cluster name
            tags: Filter by tags
            limit: Max results
        
        Returns:
            Dict with matching assets grouped by cluster
        """
        from flask_dashboard import ConstellationCluster, ConstellationNode, AudioAsset
        
        try:
            # Build query
            query = self.db.session.query(
                ConstellationNode,
                ConstellationCluster,
                AudioAsset
            ).join(
                ConstellationCluster,
                ConstellationNode.cluster_id == ConstellationCluster.id
            ).join(
                AudioAsset,
                ConstellationNode.asset_id == AudioAsset.id
            )
            
            # Apply filters
            if audio_type:
                query = query.filter(ConstellationCluster.audio_type == audio_type)
            
            if cluster_name:
                query = query.filter(ConstellationCluster.name.ilike(f"%{cluster_name}%"))
            
            # Execute query
            results = query.limit(limit).all()
            
            # Group by cluster
            clusters_data = {}
            for node, cluster, asset in results:
                if cluster.name not in clusters_data:
                    clusters_data[cluster.name] = {
                        "cluster_id": cluster.id,
                        "cluster_type": cluster.cluster_type,
                        "audio_type": cluster.audio_type,
                        "assets": []
                    }
                
                # Filter by tags if specified
                if tags:
                    asset_tags = json.loads(asset.metadata_json or "{}").get("tags", [])
                    if not any(tag.lower() in [t.lower() for t in asset_tags] for tag in tags):
                        continue
                
                clusters_data[cluster.name]["assets"].append({
                    "asset_id": asset.id,
                    "name": asset.name,
                    "duration": asset.duration,
                    "audio_url": asset.audio_url,
                    "waveform_url": asset.waveform_url
                })
            
            return {
                "success": True,
                "clusters": clusters_data,
                "total_clusters": len(clusters_data)
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_similar_assets(
        self,
        asset_id: int,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Find similar assets in the same constellation clusters.
        
        Args:
            asset_id: Source asset ID
            limit: Max similar assets to return
        
        Returns:
            Dict with similar assets
        """
        from flask_dashboard import AudioAsset, ConstellationNode, ConstellationCluster
        
        try:
            # Get source asset
            source_asset = AudioAsset.query.get(asset_id)
            if not source_asset:
                return {"success": False, "error": "Asset not found"}
            
            # Get clusters for source asset
            source_nodes = ConstellationNode.query.filter_by(asset_id=asset_id).all()
            cluster_ids = [node.cluster_id for node in source_nodes]
            
            if not cluster_ids:
                return {
                    "success": True,
                    "similar_assets": [],
                    "message": "Asset not in any clusters"
                }
            
            # Find other assets in the same clusters
            similar_nodes = ConstellationNode.query.filter(
                ConstellationNode.cluster_id.in_(cluster_ids),
                ConstellationNode.asset_id != asset_id
            ).limit(limit).all()
            
            # Get asset details
            similar_assets = []
            for node in similar_nodes:
                asset = AudioAsset.query.get(node.asset_id)
                if asset:
                    cluster = ConstellationCluster.query.get(node.cluster_id)
                    similar_assets.append({
                        "asset_id": asset.id,
                        "name": asset.name,
                        "audio_type": asset.asset_type,
                        "duration": asset.duration,
                        "audio_url": asset.audio_url,
                        "waveform_url": asset.waveform_url,
                        "shared_cluster": cluster.name if cluster else "Unknown"
                    })
            
            return {
                "success": True,
                "source_asset_id": asset_id,
                "similar_assets": similar_assets,
                "count": len(similar_assets)
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ========== LINEAGE VISUALIZATION ==========
    
    def visualize_lineage(self, asset_id: int) -> Dict[str, Any]:
        """Generate lineage visualization data for constellation view.
        
        Args:
            asset_id: Asset ID to visualize
        
        Returns:
            Dict with D3.js/Cytoscape-ready visualization data
        """
        from audio_evolution_engine import AudioEvolutionEngine
        
        try:
            # Get lineage tree
            evolution_engine = AudioEvolutionEngine(self.db)
            lineage_tree = evolution_engine.get_lineage_tree(asset_id)
            
            if not lineage_tree.get("success"):
                return lineage_tree
            
            # Convert to graph format
            nodes = []
            edges = []
            
            # Add root node
            nodes.append({
                "id": f"asset_{asset_id}",
                "label": lineage_tree["asset_name"],
                "type": "current",
                "generation": lineage_tree["generation_number"]
            })
            
            # Add ancestors
            for ancestor in lineage_tree.get("ancestors", []):
                node_id = f"asset_{ancestor['asset_id']}"
                nodes.append({
                    "id": node_id,
                    "label": ancestor["name"],
                    "type": "ancestor",
                    "generation": ancestor["generation"]
                })
                edges.append({
                    "source": node_id,
                    "target": f"asset_{asset_id}",
                    "relationship": ancestor["relationship"],
                    "method": ancestor["method"]
                })
            
            # Add descendants
            for descendant in lineage_tree.get("descendants", []):
                node_id = f"asset_{descendant['asset_id']}"
                nodes.append({
                    "id": node_id,
                    "label": descendant["name"],
                    "type": "descendant",
                    "generation": descendant["generation"]
                })
                edges.append({
                    "source": f"asset_{asset_id}",
                    "target": node_id,
                    "relationship": descendant["relationship"],
                    "method": descendant["method"]
                })
            
            return {
                "success": True,
                "graph": {
                    "nodes": nodes,
                    "edges": edges
                },
                "layout": "hierarchical",
                "center_node": f"asset_{asset_id}"
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_constellation_map(
        self,
        audio_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get full constellation map for visualization.
        
        Args:
            audio_type: Filter by audio type (music, voice, sfx)
        
        Returns:
            Dict with constellation map data
        """
        from flask_dashboard import ConstellationCluster, ConstellationNode, AudioAsset
        
        try:
            # Get all clusters
            query = ConstellationCluster.query
            if audio_type:
                query = query.filter_by(audio_type=audio_type)
            
            clusters = query.all()
            
            # Build constellation map
            constellation_data = []
            
            for cluster in clusters:
                # Get nodes in this cluster
                nodes = ConstellationNode.query.filter_by(cluster_id=cluster.id).all()
                
                assets = []
                for node in nodes:
                    asset = AudioAsset.query.get(node.asset_id)
                    if asset:
                        assets.append({
                            "asset_id": asset.id,
                            "name": asset.name,
                            "audio_url": asset.audio_url,
                            "position_x": node.position_x,
                            "position_y": node.position_y
                        })
                
                constellation_data.append({
                    "cluster_id": cluster.id,
                    "name": cluster.name,
                    "type": cluster.cluster_type,
                    "audio_type": cluster.audio_type,
                    "asset_count": len(assets),
                    "assets": assets
                })
            
            return {
                "success": True,
                "constellations": constellation_data,
                "total_clusters": len(constellation_data)
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ========== STATISTICS ==========
    
    def get_constellation_stats(self) -> Dict[str, Any]:
        """Get overall constellation statistics.
        
        Returns:
            Dict with constellation stats
        """
        from flask_dashboard import ConstellationCluster, ConstellationNode
        
        try:
            # Count clusters by type
            music_clusters = ConstellationCluster.query.filter_by(audio_type="music").count()
            voice_clusters = ConstellationCluster.query.filter_by(audio_type="voice").count()
            sfx_clusters = ConstellationCluster.query.filter_by(audio_type="sfx").count()
            
            # Count total nodes
            total_nodes = ConstellationNode.query.count()
            
            # Get largest clusters
            from sqlalchemy import func
            largest_clusters = self.db.session.query(
                ConstellationCluster.name,
                func.count(ConstellationNode.id).label("asset_count")
            ).join(
                ConstellationNode,
                ConstellationCluster.id == ConstellationNode.cluster_id
            ).group_by(
                ConstellationCluster.id,
                ConstellationCluster.name
            ).order_by(
                func.count(ConstellationNode.id).desc()
            ).limit(10).all()
            
            return {
                "success": True,
                "total_clusters": music_clusters + voice_clusters + sfx_clusters,
                "music_clusters": music_clusters,
                "voice_clusters": voice_clusters,
                "sfx_clusters": sfx_clusters,
                "total_assets_in_constellation": total_nodes,
                "largest_clusters": [
                    {"name": name, "asset_count": count}
                    for name, count in largest_clusters
                ]
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
