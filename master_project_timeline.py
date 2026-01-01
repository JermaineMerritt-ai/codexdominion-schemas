"""
Master Project Timeline - Unified Multi-Medium Editing

Synchronize graphics, audio, and video on a single unified timeline.
Enables coordinated editing across all three creative mediums.

Features:
- Multi-medium track management
- Automatic synchronization
- Cross-medium effects and transitions
- Timeline export to industry formats

Author: Codex Dominion Creative Platform
Created: December 22, 2025
Version: 1.0.0 (Tri-Medium Integration)
"""

import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field


# =============================================================================
# MASTER TIMELINE ENUMS
# =============================================================================

class MediumType(str, Enum):
    """Creative medium types"""
    GRAPHICS = "graphics"
    AUDIO = "audio"
    VIDEO = "video"


class SyncMode(str, Enum):
    """Timeline synchronization modes"""
    STRICT = "strict"  # Frame-perfect sync
    LOOSE = "loose"  # Approximate sync with tolerance
    BEAT_SYNC = "beat_sync"  # Sync to audio beats
    MANUAL = "manual"  # No automatic sync


class TransitionBehavior(str, Enum):
    """Cross-medium transition handling"""
    SIMULTANEOUS = "simultaneous"  # All mediums transition together
    SEQUENTIAL = "sequential"  # Mediums transition in sequence
    AUDIO_FIRST = "audio_first"  # Audio leads, others follow
    VIDEO_FIRST = "video_first"  # Video leads, others follow


# =============================================================================
# MASTER PROJECT TIMELINE
# =============================================================================

@dataclass
class TimelineAsset:
    """Asset on master timeline"""
    asset_id: str
    medium: MediumType
    start_time: float  # seconds
    duration: float  # seconds
    track_number: int
    asset_url: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SyncPoint:
    """Synchronization point across mediums"""
    sync_id: str
    timestamp: float  # seconds
    graphics_asset_ids: List[str] = field(default_factory=list)
    audio_asset_ids: List[str] = field(default_factory=list)
    video_asset_ids: List[str] = field(default_factory=list)
    description: str = ""


class MasterProjectTimeline:
    """
    Master timeline for unified multi-medium projects
    
    Features:
    - Unified timeline for graphics, audio, and video
    - Multi-track editing per medium
    - Automatic synchronization
    - Cross-medium effects
    - Export to industry formats
    - Real-time collaboration support
    
    Structure:
    - Graphics tracks: Static images, animated sequences
    - Audio tracks: Music, voiceover, SFX
    - Video tracks: Main footage, B-roll, overlays
    - Sync points: Cross-medium synchronization markers
    """
    
    def __init__(self, project_id: Optional[str] = None):
        """Initialize master timeline"""
        self.project_id = project_id or f"project_{int(datetime.utcnow().timestamp())}"
        self.assets: List[TimelineAsset] = []
        self.sync_points: List[SyncPoint] = []
        self.total_duration: float = 0.0
        self.fps: int = 24
        self.sample_rate: int = 48000  # Audio sample rate
        self.resolution: Tuple[int, int] = (1920, 1080)
        self.sync_mode: SyncMode = SyncMode.STRICT
    
    def add_asset(
        self,
        asset_id: str,
        medium: MediumType,
        start_time: float,
        duration: float,
        track_number: int = 0,
        asset_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> TimelineAsset:
        """
        Add asset to timeline
        
        Args:
            asset_id: Asset ID
            medium: Medium type (graphics, audio, video)
            start_time: Start time in seconds
            duration: Duration in seconds
            track_number: Track number (0 = bottom/main track)
            asset_url: Asset file URL
            metadata: Additional asset metadata
        
        Returns:
            TimelineAsset object
        """
        asset = TimelineAsset(
            asset_id=asset_id,
            medium=medium,
            start_time=start_time,
            duration=duration,
            track_number=track_number,
            asset_url=asset_url or f"{medium.value}_{asset_id}",
            metadata=metadata or {}
        )
        
        self.assets.append(asset)
        
        # Update total duration
        asset_end = start_time + duration
        if asset_end > self.total_duration:
            self.total_duration = asset_end
        
        return asset
    
    def add_sync_point(
        self,
        timestamp: float,
        description: str = "",
        graphics_assets: Optional[List[str]] = None,
        audio_assets: Optional[List[str]] = None,
        video_assets: Optional[List[str]] = None
    ) -> SyncPoint:
        """
        Add synchronization point linking assets across mediums
        
        Args:
            timestamp: Timeline position in seconds
            description: Sync point description
            graphics_assets: Graphics asset IDs at this point
            audio_assets: Audio asset IDs at this point
            video_assets: Video asset IDs at this point
        
        Returns:
            SyncPoint object
        """
        sync_point = SyncPoint(
            sync_id=f"sync_{len(self.sync_points)}",
            timestamp=timestamp,
            graphics_asset_ids=graphics_assets or [],
            audio_asset_ids=audio_assets or [],
            video_asset_ids=video_assets or [],
            description=description
        )
        
        self.sync_points.append(sync_point)
        
        return sync_point
    
    def auto_sync_to_audio(
        self,
        audio_asset_id: str,
        beat_detection: bool = True
    ) -> List[SyncPoint]:
        """
        Automatically create sync points based on audio beats
        
        Args:
            audio_asset_id: Source audio asset ID
            beat_detection: Use beat detection for sync points
        
        Returns:
            List of created SyncPoint objects
        """
        # Get audio asset
        audio_asset = self._get_asset(audio_asset_id, MediumType.AUDIO)
        
        if not audio_asset:
            raise ValueError(f"Audio asset not found: {audio_asset_id}")
        
        # Detect beats (simulated)
        beats = self._detect_beats(audio_asset) if beat_detection else []
        
        # Create sync points at beats
        sync_points = []
        for i, beat_time in enumerate(beats):
            sync_point = self.add_sync_point(
                timestamp=beat_time,
                description=f"Beat {i+1}",
                audio_assets=[audio_asset_id]
            )
            sync_points.append(sync_point)
        
        return sync_points
    
    def align_assets_to_sync_points(
        self,
        medium: MediumType,
        transition_behavior: TransitionBehavior = TransitionBehavior.SIMULTANEOUS
    ):
        """
        Align assets of specified medium to sync points
        
        Args:
            medium: Medium to align
            transition_behavior: How to handle transitions
        """
        medium_assets = [a for a in self.assets if a.medium == medium]
        
        if not self.sync_points or not medium_assets:
            return
        
        # Sort sync points by timestamp
        sorted_sync_points = sorted(self.sync_points, key=lambda sp: sp.timestamp)
        
        # Align assets to sync points
        for i, sync_point in enumerate(sorted_sync_points):
            if i < len(medium_assets):
                asset = medium_assets[i]
                asset.start_time = sync_point.timestamp
                
                # Update sync point reference
                if medium == MediumType.GRAPHICS:
                    sync_point.graphics_asset_ids.append(asset.asset_id)
                elif medium == MediumType.AUDIO:
                    sync_point.audio_asset_ids.append(asset.asset_id)
                elif medium == MediumType.VIDEO:
                    sync_point.video_asset_ids.append(asset.asset_id)
    
    def get_assets_at_time(
        self,
        timestamp: float,
        medium: Optional[MediumType] = None
    ) -> List[TimelineAsset]:
        """
        Get all assets active at specific time
        
        Args:
            timestamp: Timeline position in seconds
            medium: Filter by medium (all if None)
        
        Returns:
            List of active TimelineAsset objects
        """
        active_assets = []
        
        for asset in self.assets:
            asset_start = asset.start_time
            asset_end = asset_start + asset.duration
            
            if asset_start <= timestamp <= asset_end:
                if medium is None or asset.medium == medium:
                    active_assets.append(asset)
        
        return active_assets
    
    def get_timeline_summary(self) -> Dict[str, Any]:
        """
        Get timeline statistics
        
        Returns:
            {
                'project_id': str,
                'total_duration': float,
                'asset_count': int,
                'sync_point_count': int,
                'assets_by_medium': dict,
                'resolution': str,
                'fps': int
            }
        """
        assets_by_medium = {
            'graphics': len([a for a in self.assets if a.medium == MediumType.GRAPHICS]),
            'audio': len([a for a in self.assets if a.medium == MediumType.AUDIO]),
            'video': len([a for a in self.assets if a.medium == MediumType.VIDEO])
        }
        
        return {
            'project_id': self.project_id,
            'total_duration': self.total_duration,
            'asset_count': len(self.assets),
            'sync_point_count': len(self.sync_points),
            'assets_by_medium': assets_by_medium,
            'resolution': f"{self.resolution[0]}x{self.resolution[1]}",
            'fps': self.fps,
            'sample_rate': self.sample_rate,
            'sync_mode': self.sync_mode.value
        }
    
    def export_timeline(
        self,
        format: str = "json",
        include_assets: bool = True,
        include_sync_points: bool = True
    ) -> str:
        """
        Export timeline to file format
        
        Args:
            format: Export format ("json", "xml", "edl", "fcpxml")
            include_assets: Include asset details
            include_sync_points: Include sync point data
        
        Returns:
            Serialized timeline string
        """
        timeline_data = {
            'project_id': self.project_id,
            'total_duration': self.total_duration,
            'fps': self.fps,
            'sample_rate': self.sample_rate,
            'resolution': {
                'width': self.resolution[0],
                'height': self.resolution[1]
            },
            'sync_mode': self.sync_mode.value
        }
        
        if include_assets:
            timeline_data['assets'] = [
                {
                    'asset_id': asset.asset_id,
                    'medium': asset.medium.value,
                    'start_time': asset.start_time,
                    'duration': asset.duration,
                    'track_number': asset.track_number,
                    'asset_url': asset.asset_url,
                    'metadata': asset.metadata
                }
                for asset in self.assets
            ]
        
        if include_sync_points:
            timeline_data['sync_points'] = [
                {
                    'sync_id': sp.sync_id,
                    'timestamp': sp.timestamp,
                    'description': sp.description,
                    'graphics_assets': sp.graphics_asset_ids,
                    'audio_assets': sp.audio_asset_ids,
                    'video_assets': sp.video_asset_ids
                }
                for sp in self.sync_points
            ]
        
        if format == "json":
            return json.dumps(timeline_data, indent=2)
        elif format == "xml":
            return self._export_xml(timeline_data)
        elif format == "edl":
            return self._export_edl(timeline_data)
        elif format == "fcpxml":
            return self._export_fcpxml(timeline_data)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def visualize_timeline(
        self,
        time_range: Optional[Tuple[float, float]] = None
    ) -> Dict[str, Any]:
        """
        Generate timeline visualization data for UI rendering
        
        Args:
            time_range: Optional (start, end) time range in seconds
        
        Returns:
            {
                'tracks': [
                    {
                        'track_id': str,
                        'medium': str,
                        'track_number': int,
                        'clips': [
                            {
                                'asset_id': str,
                                'start_time': float,
                                'duration': float,
                                'thumbnail_url': str
                            }
                        ]
                    }
                ],
                'sync_points': [
                    {'timestamp': float, 'label': str}
                ]
            }
        """
        if time_range:
            start, end = time_range
            visible_assets = [
                a for a in self.assets
                if a.start_time < end and (a.start_time + a.duration) > start
            ]
            visible_sync_points = [
                sp for sp in self.sync_points
                if start <= sp.timestamp <= end
            ]
        else:
            visible_assets = self.assets
            visible_sync_points = self.sync_points
        
        # Group assets by medium and track
        tracks = {}
        for asset in visible_assets:
            track_key = (asset.medium.value, asset.track_number)
            
            if track_key not in tracks:
                tracks[track_key] = {
                    'track_id': f"{asset.medium.value}_track_{asset.track_number}",
                    'medium': asset.medium.value,
                    'track_number': asset.track_number,
                    'clips': []
                }
            
            tracks[track_key]['clips'].append({
                'asset_id': asset.asset_id,
                'start_time': asset.start_time,
                'duration': asset.duration,
                'thumbnail_url': asset.metadata.get('thumbnail_url', ''),
                'asset_url': asset.asset_url
            })
        
        return {
            'tracks': sorted(tracks.values(), key=lambda t: (t['medium'], t['track_number'])),
            'sync_points': [
                {
                    'timestamp': sp.timestamp,
                    'label': sp.description or sp.sync_id
                }
                for sp in visible_sync_points
            ],
            'time_range': time_range or (0, self.total_duration)
        }
    
    # =============================================================================
    # PRIVATE HELPER METHODS
    # =============================================================================
    
    def _get_asset(self, asset_id: str, medium: MediumType) -> Optional[TimelineAsset]:
        """Get asset by ID and medium"""
        for asset in self.assets:
            if asset.asset_id == asset_id and asset.medium == medium:
                return asset
        return None
    
    def _detect_beats(self, audio_asset: TimelineAsset) -> List[float]:
        """Detect beat timestamps in audio (simulated)"""
        # Simulated beat detection
        duration = audio_asset.duration
        bpm = 120  # Assumed BPM
        beat_interval = 60.0 / bpm
        
        beats = []
        current_time = audio_asset.start_time
        while current_time < audio_asset.start_time + duration:
            beats.append(current_time)
            current_time += beat_interval
        
        return beats
    
    def _export_xml(self, timeline_data: Dict[str, Any]) -> str:
        """Export to XML format"""
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<master_timeline>',
            f'  <project_id>{timeline_data["project_id"]}</project_id>',
            f'  <duration>{timeline_data["total_duration"]}</duration>',
            '  <assets>'
        ]
        
        for asset in timeline_data.get('assets', []):
            xml_lines.append(f'    <asset id="{asset["asset_id"]}" medium="{asset["medium"]}" start="{asset["start_time"]}" duration="{asset["duration"]}" />')
        
        xml_lines.append('  </assets>')
        xml_lines.append('</master_timeline>')
        
        return '\n'.join(xml_lines)
    
    def _export_edl(self, timeline_data: Dict[str, Any]) -> str:
        """Export to EDL format"""
        edl_lines = [
            "TITLE: Codex Dominion Master Timeline",
            f"FCM: NON-DROP FRAME",
            ""
        ]
        
        event_num = 1
        for asset in timeline_data.get('assets', []):
            if asset['medium'] == 'video':  # EDL primarily for video
                edl_lines.append(
                    f"{event_num:03d}  {asset['asset_id'][:8].upper()}  V     C        "
                    f"{self._seconds_to_timecode(asset['start_time'])} "
                    f"{self._seconds_to_timecode(asset['start_time'] + asset['duration'])} "
                    f"{self._seconds_to_timecode(asset['start_time'])} "
                    f"{self._seconds_to_timecode(asset['start_time'] + asset['duration'])}"
                )
                event_num += 1
        
        return '\n'.join(edl_lines)
    
    def _export_fcpxml(self, timeline_data: Dict[str, Any]) -> str:
        """Export to Final Cut Pro XML"""
        # Simplified FCPXML export
        return self._export_xml(timeline_data)
    
    def _seconds_to_timecode(self, seconds: float) -> str:
        """Convert seconds to SMPTE timecode"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        frames = int((seconds % 1) * self.fps)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}:{frames:02d}"


# =============================================================================
# MAIN - DEMO/TEST
# =============================================================================

if __name__ == "__main__":
    print("🎬 Master Project Timeline")
    print("=" * 80)
    
    # Create timeline
    timeline = MasterProjectTimeline()
    
    # Add graphics assets
    timeline.add_asset(
        asset_id="graphics_intro",
        medium=MediumType.GRAPHICS,
        start_time=0.0,
        duration=3.0,
        track_number=0
    )
    
    # Add audio assets
    timeline.add_asset(
        asset_id="background_music",
        medium=MediumType.AUDIO,
        start_time=0.0,
        duration=30.0,
        track_number=0
    )
    
    # Add video assets
    timeline.add_asset(
        asset_id="main_video",
        medium=MediumType.VIDEO,
        start_time=3.0,
        duration=25.0,
        track_number=0
    )
    
    # Add sync points
    timeline.add_sync_point(
        timestamp=0.0,
        description="Project start",
        graphics_assets=["graphics_intro"],
        audio_assets=["background_music"]
    )
    
    timeline.add_sync_point(
        timestamp=3.0,
        description="Video begins",
        video_assets=["main_video"]
    )
    
    # Get summary
    summary = timeline.get_timeline_summary()
    
    print(f"\n✅ Master timeline created: {summary['project_id']}")
    print(f"Total duration: {summary['total_duration']}s")
    print(f"Total assets: {summary['asset_count']}")
    print(f"Sync points: {summary['sync_point_count']}")
    print(f"\nAssets by medium:")
    for medium, count in summary['assets_by_medium'].items():
        print(f"  • {medium.capitalize()}: {count}")
    
    # Export to JSON
    timeline_json = timeline.export_timeline(format="json")
    print(f"\n📄 Timeline JSON export: {len(timeline_json)} bytes")
