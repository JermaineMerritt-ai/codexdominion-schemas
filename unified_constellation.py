"""
Unified Constellation System - Cross-Medium Clustering

Link and discover creative assets across graphics, audio, and video mediums.
Enables cross-medium similarity search and unified creative exploration.

Features:
- Cross-medium cluster mapping (graphics ↔ audio ↔ video)
- Unified similarity search across all mediums
- Multi-medium constellation visualization
- Cross-reference discovery engine

Author: Codex Dominion Creative Platform
Created: December 22, 2025
Version: 1.0.0 (Tri-Medium Integration)
"""

import json
from typing import Dict, Any, List, Optional, Tuple, Set
from datetime import datetime
from collections import defaultdict


# =============================================================================
# CROSS-MEDIUM CLUSTER MAPPINGS
# =============================================================================

# Define cross-medium cluster relationships
# Graphics style → Audio genre → Video style
CROSS_MEDIUM_CLUSTERS = {
    # Vibrant/Energetic cluster
    'vibrant_energetic': {
        'graphics_styles': ['vibrant', 'colorful', 'dynamic'],
        'audio_genres': ['electronic', 'pop', 'dance'],
        'video_styles': ['fast_paced', 'dynamic', 'stylized'],
        'mood': 'energetic',
        'color_palette': ['#FF5733', '#FFC300', '#33FF57', '#3366FF']
    },
    
    # Calm/Serene cluster
    'calm_serene': {
        'graphics_styles': ['minimalist', 'pastel', 'soft'],
        'audio_genres': ['ambient', 'classical', 'meditation'],
        'video_styles': ['slow_burn', 'contemplative', 'minimalist'],
        'mood': 'calm',
        'color_palette': ['#B3E5FC', '#C8E6C9', '#F8BBD0', '#E1BEE7']
    },
    
    # Dark/Moody cluster
    'dark_moody': {
        'graphics_styles': ['dark', 'moody', 'dramatic'],
        'audio_genres': ['dark_ambient', 'industrial', 'cinematic'],
        'video_styles': ['horror', 'dramatic', 'noir'],
        'mood': 'dark',
        'color_palette': ['#263238', '#37474F', '#455A64', '#546E7A']
    },
    
    # Cinematic/Epic cluster
    'cinematic_epic': {
        'graphics_styles': ['epic', 'cinematic', 'dramatic'],
        'audio_genres': ['orchestral', 'cinematic', 'epic'],
        'video_styles': ['cinematic', 'action', 'sci_fi'],
        'mood': 'epic',
        'color_palette': ['#D32F2F', '#1976D2', '#FBC02D', '#455A64']
    },
    
    # Retro/Nostalgic cluster
    'retro_nostalgic': {
        'graphics_styles': ['retro', 'vintage', 'analog'],
        'audio_genres': ['synthwave', 'lo_fi', 'jazz'],
        'video_styles': ['retro', 'raw', 'documentary'],
        'mood': 'nostalgic',
        'color_palette': ['#FF6B6B', '#4ECDC4', '#FFE66D', '#A8E6CF']
    },
    
    # Abstract/Artistic cluster
    'abstract_artistic': {
        'graphics_styles': ['abstract', 'artistic', 'experimental'],
        'audio_genres': ['experimental', 'avant_garde', 'abstract'],
        'video_styles': ['surreal', 'stylized', 'abstract'],
        'mood': 'creative',
        'color_palette': ['#E91E63', '#9C27B0', '#FF9800', '#00BCD4']
    },
    
    # Natural/Organic cluster
    'natural_organic': {
        'graphics_styles': ['natural', 'organic', 'earthy'],
        'audio_genres': ['acoustic', 'folk', 'nature_sounds'],
        'video_styles': ['documentary', 'contemplative', 'raw'],
        'mood': 'natural',
        'color_palette': ['#8BC34A', '#CDDC39', '#FFC107', '#795548']
    },
    
    # Futuristic/Tech cluster
    'futuristic_tech': {
        'graphics_styles': ['futuristic', 'cyber', 'sleek'],
        'audio_genres': ['electronic', 'techno', 'synthwave'],
        'video_styles': ['sci_fi', 'cinematic', 'stylized'],
        'mood': 'futuristic',
        'color_palette': ['#00E5FF', '#FF00FF', '#00FF41', '#1A237E']
    }
}


# =============================================================================
# UNIFIED CONSTELLATION SYSTEM
# =============================================================================

class UnifiedConstellationSystem:
    """
    Unified Constellation System for cross-medium discovery
    
    Features:
    - Link assets across graphics, audio, and video
    - Cross-medium similarity search
    - Multi-medium visualization
    - Unified cluster navigation
    - Cross-reference discovery
    
    Integration:
    - graphics_constellation_integration.py (Graphics Phase 8)
    - video_constellation_integration.py (Video Phase 8)
    - Audio constellation (if available)
    """
    
    def __init__(
        self,
        graphics_constellation=None,
        audio_constellation=None,
        video_constellation=None
    ):
        """
        Initialize unified constellation system
        
        Args:
            graphics_constellation: GraphicsConstellationIntegration instance
            audio_constellation: AudioConstellationIntegration instance
            video_constellation: VideoConstellationIntegration instance
        """
        self.graphics_constellation = graphics_constellation
        self.audio_constellation = audio_constellation
        self.video_constellation = video_constellation
        
        # Cross-medium cluster cache
        self.cross_references = defaultdict(list)
    
    def link_assets_cross_medium(
        self,
        graphics_asset_id: Optional[str] = None,
        audio_asset_id: Optional[str] = None,
        video_asset_id: Optional[str] = None,
        unified_cluster: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Link assets from different mediums into unified cluster
        
        Args:
            graphics_asset_id: Graphics asset ID
            audio_asset_id: Audio asset ID
            video_asset_id: Video asset ID
            unified_cluster: Target unified cluster name
        
        Returns:
            {
                'unified_cluster': str,
                'linked_assets': {
                    'graphics': str,
                    'audio': str,
                    'video': str
                },
                'cluster_metadata': dict
            }
        """
        # Auto-detect unified cluster if not provided
        if unified_cluster is None:
            unified_cluster = self._detect_unified_cluster(
                graphics_asset_id,
                audio_asset_id,
                video_asset_id
            )
        
        # Create cross-reference
        link_id = f"link_{int(datetime.utcnow().timestamp())}"
        
        self.cross_references[unified_cluster].append({
            'link_id': link_id,
            'graphics_asset_id': graphics_asset_id,
            'audio_asset_id': audio_asset_id,
            'video_asset_id': video_asset_id,
            'created_at': datetime.utcnow().isoformat()
        })
        
        cluster_metadata = CROSS_MEDIUM_CLUSTERS.get(unified_cluster, {})
        
        return {
            'link_id': link_id,
            'unified_cluster': unified_cluster,
            'linked_assets': {
                'graphics': graphics_asset_id,
                'audio': audio_asset_id,
                'video': video_asset_id
            },
            'cluster_metadata': cluster_metadata
        }
    
    def find_cross_medium_matches(
        self,
        asset_id: str,
        source_medium: str,
        target_mediums: Optional[List[str]] = None,
        similarity_threshold: float = 0.6
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Find matching assets in other mediums
        
        Args:
            asset_id: Source asset ID
            source_medium: Source medium ('graphics', 'audio', 'video')
            target_mediums: Target mediums to search (all if None)
            similarity_threshold: Minimum similarity score
        
        Returns:
            {
                'graphics': [{'asset_id': str, 'similarity': float, ...}],
                'audio': [{'asset_id': str, 'similarity': float, ...}],
                'video': [{'asset_id': str, 'similarity': float, ...}]
            }
        """
        if target_mediums is None:
            target_mediums = [m for m in ['graphics', 'audio', 'video'] if m != source_medium]
        
        # Get source asset clusters
        source_clusters = self._get_asset_clusters(asset_id, source_medium)
        
        # Find matches in target mediums
        matches = {}
        
        for target_medium in target_mediums:
            target_matches = self._find_matches_in_medium(
                source_clusters,
                target_medium,
                similarity_threshold
            )
            matches[target_medium] = target_matches
        
        return matches
    
    def query_unified_constellation(
        self,
        mood: Optional[str] = None,
        style: Optional[str] = None,
        mediums: Optional[List[str]] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Query constellation across all mediums
        
        Args:
            mood: Mood filter
            style: Style filter
            mediums: Mediums to include (all if None)
            limit: Max results per medium
        
        Returns:
            {
                'query': dict,
                'results': {
                    'graphics': [...],
                    'audio': [...],
                    'video': [...]
                },
                'total_count': int
            }
        """
        if mediums is None:
            mediums = ['graphics', 'audio', 'video']
        
        results = {}
        total_count = 0
        
        # Query graphics constellation
        if 'graphics' in mediums and self.graphics_constellation:
            graphics_results = self._query_graphics_constellation(mood, style, limit)
            results['graphics'] = graphics_results
            total_count += len(graphics_results)
        
        # Query audio constellation
        if 'audio' in mediums and self.audio_constellation:
            audio_results = self._query_audio_constellation(mood, style, limit)
            results['audio'] = audio_results
            total_count += len(audio_results)
        
        # Query video constellation
        if 'video' in mediums and self.video_constellation:
            video_results = self._query_video_constellation(mood, style, limit)
            results['video'] = video_results
            total_count += len(video_results)
        
        return {
            'query': {
                'mood': mood,
                'style': style,
                'mediums': mediums,
                'limit': limit
            },
            'results': results,
            'total_count': total_count
        }
    
    def get_unified_cluster_map(self) -> Dict[str, Any]:
        """
        Get complete unified constellation map
        
        Returns:
            {
                'clusters': [
                    {
                        'cluster_id': str,
                        'cluster_name': str,
                        'mood': str,
                        'graphics_count': int,
                        'audio_count': int,
                        'video_count': int,
                        'cross_references': int
                    }
                ],
                'total_clusters': int,
                'total_cross_references': int
            }
        """
        clusters = []
        total_cross_refs = 0
        
        for cluster_id, cluster_data in CROSS_MEDIUM_CLUSTERS.items():
            cross_refs = len(self.cross_references.get(cluster_id, []))
            total_cross_refs += cross_refs
            
            clusters.append({
                'cluster_id': cluster_id,
                'cluster_name': cluster_id.replace('_', ' ').title(),
                'mood': cluster_data.get('mood', 'neutral'),
                'graphics_styles': cluster_data.get('graphics_styles', []),
                'audio_genres': cluster_data.get('audio_genres', []),
                'video_styles': cluster_data.get('video_styles', []),
                'color_palette': cluster_data.get('color_palette', []),
                'cross_references': cross_refs
            })
        
        return {
            'clusters': clusters,
            'total_clusters': len(clusters),
            'total_cross_references': total_cross_refs
        }
    
    def visualize_cross_medium_graph(
        self,
        asset_id: str,
        medium: str,
        depth: int = 2
    ) -> Dict[str, Any]:
        """
        Generate D3.js graph for cross-medium relationships
        
        Args:
            asset_id: Starting asset ID
            medium: Starting medium
            depth: Relationship depth to traverse
        
        Returns:
            {
                'nodes': [
                    {
                        'id': str,
                        'type': 'graphics' | 'audio' | 'video',
                        'label': str,
                        'cluster': str
                    }
                ],
                'edges': [
                    {
                        'source': str,
                        'target': str,
                        'relationship': 'similar' | 'linked' | 'derived'
                    }
                ]
            }
        """
        nodes = []
        edges = []
        visited = set()
        
        # Add starting node
        nodes.append({
            'id': asset_id,
            'type': medium,
            'label': f"{medium}_{asset_id}",
            'cluster': 'unknown',
            'level': 0
        })
        visited.add((asset_id, medium))
        
        # Traverse relationships
        self._traverse_relationships(
            asset_id,
            medium,
            depth,
            visited,
            nodes,
            edges
        )
        
        return {
            'nodes': nodes,
            'edges': edges,
            'node_count': len(nodes),
            'edge_count': len(edges)
        }
    
    def get_cross_medium_recommendations(
        self,
        asset_id: str,
        medium: str,
        recommendation_type: str = "complementary"
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get recommendations across mediums for creative projects
        
        Args:
            asset_id: Source asset ID
            medium: Source medium
            recommendation_type: Type ('complementary', 'similar', 'contrasting')
        
        Returns:
            {
                'graphics': [...],
                'audio': [...],
                'video': [...]
            }
        """
        # Get asset clusters
        source_clusters = self._get_asset_clusters(asset_id, medium)
        
        recommendations = {}
        
        for target_medium in ['graphics', 'audio', 'video']:
            if target_medium == medium:
                continue
            
            target_recs = self._generate_recommendations(
                source_clusters,
                target_medium,
                recommendation_type
            )
            recommendations[target_medium] = target_recs
        
        return recommendations
    
    # =============================================================================
    # PRIVATE HELPER METHODS
    # =============================================================================
    
    def _detect_unified_cluster(
        self,
        graphics_asset_id: Optional[str],
        audio_asset_id: Optional[str],
        video_asset_id: Optional[str]
    ) -> str:
        """Auto-detect unified cluster from assets"""
        # Would analyze assets and map to unified cluster
        # For now, return default
        return 'vibrant_energetic'
    
    def _get_asset_clusters(self, asset_id: str, medium: str) -> List[str]:
        """Get clusters for asset"""
        # Would query medium-specific constellation
        return ['vibrant', 'energetic', 'modern']
    
    def _find_matches_in_medium(
        self,
        source_clusters: List[str],
        target_medium: str,
        similarity_threshold: float
    ) -> List[Dict[str, Any]]:
        """Find matching assets in target medium"""
        # Simulated matches
        return [
            {
                'asset_id': f"{target_medium}_match_1",
                'similarity': 0.85,
                'shared_clusters': ['vibrant', 'energetic']
            },
            {
                'asset_id': f"{target_medium}_match_2",
                'similarity': 0.72,
                'shared_clusters': ['vibrant']
            }
        ]
    
    def _query_graphics_constellation(
        self,
        mood: Optional[str],
        style: Optional[str],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Query graphics constellation"""
        if not self.graphics_constellation:
            return []
        
        # Would use graphics_constellation.query_constellation()
        return [
            {'asset_id': f"graphics_{i}", 'mood': mood, 'style': style}
            for i in range(min(3, limit))
        ]
    
    def _query_audio_constellation(
        self,
        mood: Optional[str],
        style: Optional[str],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Query audio constellation"""
        if not self.audio_constellation:
            return []
        
        return [
            {'asset_id': f"audio_{i}", 'mood': mood, 'style': style}
            for i in range(min(3, limit))
        ]
    
    def _query_video_constellation(
        self,
        mood: Optional[str],
        style: Optional[str],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Query video constellation"""
        if not self.video_constellation:
            return []
        
        # Would use video_constellation.query_constellation()
        return [
            {'asset_id': f"video_{i}", 'mood': mood, 'style': style}
            for i in range(min(3, limit))
        ]
    
    def _traverse_relationships(
        self,
        asset_id: str,
        medium: str,
        depth: int,
        visited: Set[Tuple[str, str]],
        nodes: List[Dict],
        edges: List[Dict]
    ):
        """Recursively traverse cross-medium relationships"""
        if depth <= 0:
            return
        
        # Find related assets in other mediums
        matches = self.find_cross_medium_matches(asset_id, medium)
        
        for target_medium, match_list in matches.items():
            for match in match_list[:3]:  # Limit per medium
                match_id = match['asset_id']
                
                if (match_id, target_medium) not in visited:
                    # Add node
                    nodes.append({
                        'id': match_id,
                        'type': target_medium,
                        'label': f"{target_medium}_{match_id}",
                        'cluster': 'unknown',
                        'level': depth
                    })
                    visited.add((match_id, target_medium))
                    
                    # Add edge
                    edges.append({
                        'source': asset_id,
                        'target': match_id,
                        'relationship': 'similar',
                        'similarity': match['similarity']
                    })
                    
                    # Recurse
                    self._traverse_relationships(
                        match_id,
                        target_medium,
                        depth - 1,
                        visited,
                        nodes,
                        edges
                    )
    
    def _generate_recommendations(
        self,
        source_clusters: List[str],
        target_medium: str,
        recommendation_type: str
    ) -> List[Dict[str, Any]]:
        """Generate recommendations for target medium"""
        # Simulated recommendations
        return [
            {
                'asset_id': f"{target_medium}_rec_{i}",
                'reason': f"{recommendation_type} match",
                'confidence': 0.8 - (i * 0.1)
            }
            for i in range(3)
        ]


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def get_unified_cluster_for_mood(mood: str) -> str:
    """Get unified cluster name for mood"""
    mood_map = {
        'energetic': 'vibrant_energetic',
        'calm': 'calm_serene',
        'dark': 'dark_moody',
        'epic': 'cinematic_epic',
        'nostalgic': 'retro_nostalgic',
        'creative': 'abstract_artistic',
        'natural': 'natural_organic',
        'futuristic': 'futuristic_tech'
    }
    
    return mood_map.get(mood.lower(), 'vibrant_energetic')


def get_cross_medium_color_palette(cluster: str) -> List[str]:
    """Get color palette for unified cluster"""
    cluster_data = CROSS_MEDIUM_CLUSTERS.get(cluster, {})
    return cluster_data.get('color_palette', ['#FFFFFF'])


# =============================================================================
# MAIN - DEMO/TEST
# =============================================================================

if __name__ == "__main__":
    print("🌐 Unified Constellation System")
    print("=" * 80)
    
    system = UnifiedConstellationSystem()
    
    # Get unified cluster map
    cluster_map = system.get_unified_cluster_map()
    
    print(f"\n✅ Unified Constellation System initialized")
    print(f"Total unified clusters: {cluster_map['total_clusters']}")
    print(f"\nUnified Clusters:")
    for cluster in cluster_map['clusters']:
        print(f"  • {cluster['cluster_name']}: {cluster['mood']} mood")
        print(f"    Graphics: {', '.join(cluster['graphics_styles'])}")
        print(f"    Audio: {', '.join(cluster['audio_genres'])}")
        print(f"    Video: {', '.join(cluster['video_styles'])}")
