# ============================================================================================
# AUDIO TIMELINE ENGINE - Multi-Track Editing & Manipulation
# ============================================================================================
"""
Professional-level audio timeline engine with:
- Multi-track clip placement
- Trim, split, ripple delete operations
- Crossfades and transitions
- Snap-to-grid functionality
- Zoom and scrubbing
- Clip duplication and arrangement

This is the core editing experience of the Audio Studio.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import math


@dataclass
class TimelineClip:
    """Represents a clip on the timeline."""
    id: int
    track_id: int
    asset_id: int
    start_time: float
    end_time: float
    source_start: float
    source_end: float
    clip_gain: float = 0.0
    pitch_shift: float = 0.0
    time_stretch: float = 1.0
    fade_in_duration: float = 0.0
    fade_out_duration: float = 0.0
    clip_color: str = "#00D9FF"
    is_locked: bool = False


class AudioTimelineEngine:
    """Complete timeline engine for multi-track audio editing."""
    
    def __init__(self, db):
        """Initialize timeline engine with database connection."""
        self.db = db
        self.snap_grid_size = 0.1  # Snap to 100ms by default
        self.snap_enabled = True
    
    # ========== CLIP PLACEMENT ==========
    
    def place_clip(
        self,
        project_id: int,
        track_id: int,
        asset_id: int,
        start_time: float,
        duration: float,
        **clip_properties
    ) -> Dict[str, Any]:
        """Place an audio clip on the timeline.
        
        Args:
            project_id: Project ID
            track_id: Track to place clip on
            asset_id: Audio asset to place
            start_time: Where to place on timeline (seconds)
            duration: How long the clip should be
            **clip_properties: Additional clip properties (gain, pitch, etc.)
        
        Returns:
            Dict with success status and clip_id
        """
        from flask_dashboard import AudioClip, AudioAsset
        
        # Snap to grid if enabled
        if self.snap_enabled:
            start_time = self._snap_to_grid(start_time)
        
        # Get asset to determine source duration
        asset = AudioAsset.query.get(asset_id)
        if not asset:
            return {"success": False, "error": "Asset not found"}
        
        # Create clip
        clip = AudioClip(
            project_id=project_id,
            track_id=track_id,
            asset_id=asset_id,
            start_time=start_time,
            end_time=start_time + duration,
            source_start=clip_properties.get('source_start', 0.0),
            source_end=clip_properties.get('source_end', asset.duration),
            clip_gain=clip_properties.get('clip_gain', 0.0),
            pitch_shift=clip_properties.get('pitch_shift', 0.0),
            time_stretch=clip_properties.get('time_stretch', 1.0),
            fade_in_duration=clip_properties.get('fade_in_duration', 0.0),
            fade_out_duration=clip_properties.get('fade_out_duration', 0.0),
            clip_color=clip_properties.get('clip_color', '#00D9FF')
        )
        
        self.db.session.add(clip)
        self.db.session.commit()
        
        return {
            "success": True,
            "clip_id": clip.id,
            "start_time": clip.start_time,
            "end_time": clip.end_time
        }
    
    def move_clip(
        self,
        clip_id: int,
        new_start_time: float,
        new_track_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Move a clip to a new position on timeline.
        
        Args:
            clip_id: Clip to move
            new_start_time: New start position
            new_track_id: Optional new track to move to
        
        Returns:
            Dict with success status
        """
        from flask_dashboard import AudioClip
        
        clip = AudioClip.query.get(clip_id)
        if not clip:
            return {"success": False, "error": "Clip not found"}
        
        if clip.is_locked:
            return {"success": False, "error": "Clip is locked"}
        
        # Snap to grid if enabled
        if self.snap_enabled:
            new_start_time = self._snap_to_grid(new_start_time)
        
        # Calculate duration
        duration = clip.end_time - clip.start_time
        
        # Update position
        clip.start_time = new_start_time
        clip.end_time = new_start_time + duration
        
        if new_track_id is not None:
            clip.track_id = new_track_id
        
        self.db.session.commit()
        
        return {
            "success": True,
            "clip_id": clip.id,
            "start_time": clip.start_time,
            "end_time": clip.end_time,
            "track_id": clip.track_id
        }
    
    # ========== CLIP TRIMMING ==========
    
    def trim_clip_start(
        self,
        clip_id: int,
        new_start_time: float
    ) -> Dict[str, Any]:
        """Trim the start of a clip (non-destructive).
        
        Args:
            clip_id: Clip to trim
            new_start_time: New start position
        
        Returns:
            Dict with success status and new clip bounds
        """
        from flask_dashboard import AudioClip
        
        clip = AudioClip.query.get(clip_id)
        if not clip:
            return {"success": False, "error": "Clip not found"}
        
        if clip.is_locked:
            return {"success": False, "error": "Clip is locked"}
        
        if new_start_time >= clip.end_time:
            return {"success": False, "error": "Start time must be before end time"}
        
        # Snap to grid
        if self.snap_enabled:
            new_start_time = self._snap_to_grid(new_start_time)
        
        # Calculate how much was trimmed
        trim_amount = new_start_time - clip.start_time
        
        # Update source start (non-destructive trimming)
        clip.source_start += trim_amount
        clip.start_time = new_start_time
        
        self.db.session.commit()
        
        return {
            "success": True,
            "clip_id": clip.id,
            "start_time": clip.start_time,
            "end_time": clip.end_time,
            "source_start": clip.source_start
        }
    
    def trim_clip_end(
        self,
        clip_id: int,
        new_end_time: float
    ) -> Dict[str, Any]:
        """Trim the end of a clip (non-destructive).
        
        Args:
            clip_id: Clip to trim
            new_end_time: New end position
        
        Returns:
            Dict with success status and new clip bounds
        """
        from flask_dashboard import AudioClip
        
        clip = AudioClip.query.get(clip_id)
        if not clip:
            return {"success": False, "error": "Clip not found"}
        
        if clip.is_locked:
            return {"success": False, "error": "Clip is locked"}
        
        if new_end_time <= clip.start_time:
            return {"success": False, "error": "End time must be after start time"}
        
        # Snap to grid
        if self.snap_enabled:
            new_end_time = self._snap_to_grid(new_end_time)
        
        # Calculate how much was trimmed
        trim_amount = clip.end_time - new_end_time
        
        # Update source end (non-destructive trimming)
        clip.source_end -= trim_amount
        clip.end_time = new_end_time
        
        self.db.session.commit()
        
        return {
            "success": True,
            "clip_id": clip.id,
            "start_time": clip.start_time,
            "end_time": clip.end_time,
            "source_end": clip.source_end
        }
    
    # ========== CLIP SPLITTING ==========
    
    def split_clip(
        self,
        clip_id: int,
        split_time: float
    ) -> Dict[str, Any]:
        """Split a clip into two clips at the specified time.
        
        Args:
            clip_id: Clip to split
            split_time: Where to split (timeline position)
        
        Returns:
            Dict with both clip IDs
        """
        from flask_dashboard import AudioClip
        
        clip = AudioClip.query.get(clip_id)
        if not clip:
            return {"success": False, "error": "Clip not found"}
        
        if clip.is_locked:
            return {"success": False, "error": "Clip is locked"}
        
        if split_time <= clip.start_time or split_time >= clip.end_time:
            return {"success": False, "error": "Split time must be within clip bounds"}
        
        # Snap to grid
        if self.snap_enabled:
            split_time = self._snap_to_grid(split_time)
        
        # Calculate split point in source audio
        clip_duration = clip.end_time - clip.start_time
        source_duration = clip.source_end - clip.source_start
        split_offset = (split_time - clip.start_time) / clip_duration
        source_split = clip.source_start + (source_duration * split_offset)
        
        # Create second clip (right side)
        clip2 = AudioClip(
            project_id=clip.project_id,
            track_id=clip.track_id,
            asset_id=clip.asset_id,
            start_time=split_time,
            end_time=clip.end_time,
            source_start=source_split,
            source_end=clip.source_end,
            clip_gain=clip.clip_gain,
            pitch_shift=clip.pitch_shift,
            time_stretch=clip.time_stretch,
            fade_in_duration=0.0,  # Remove fade from split
            fade_out_duration=clip.fade_out_duration,
            clip_color=clip.clip_color
        )
        
        # Update first clip (left side)
        clip.end_time = split_time
        clip.source_end = source_split
        clip.fade_out_duration = 0.0  # Remove fade from split
        
        self.db.session.add(clip2)
        self.db.session.commit()
        
        return {
            "success": True,
            "clip1_id": clip.id,
            "clip2_id": clip2.id,
            "split_time": split_time
        }
    
    # ========== RIPPLE DELETE ==========
    
    def ripple_delete(
        self,
        clip_id: int,
        track_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Delete clip and shift all clips after it to fill the gap.
        
        Args:
            clip_id: Clip to delete
            track_id: Optional - only ripple on this track (None = all tracks)
        
        Returns:
            Dict with clips that were moved
        """
        from flask_dashboard import AudioClip
        
        clip = AudioClip.query.get(clip_id)
        if not clip:
            return {"success": False, "error": "Clip not found"}
        
        if clip.is_locked:
            return {"success": False, "error": "Clip is locked"}
        
        # Get clip duration (gap to fill)
        gap_duration = clip.end_time - clip.start_time
        gap_start = clip.start_time
        
        # Find all clips after this one on the same track (or all tracks)
        query = AudioClip.query.filter(
            AudioClip.project_id == clip.project_id,
            AudioClip.start_time >= clip.end_time
        )
        
        if track_id is not None:
            query = query.filter(AudioClip.track_id == track_id)
        
        clips_to_move = query.all()
        
        # Delete the clip
        self.db.session.delete(clip)
        
        # Shift all clips after it
        moved_clips = []
        for c in clips_to_move:
            if not c.is_locked:
                c.start_time -= gap_duration
                c.end_time -= gap_duration
                moved_clips.append({
                    "clip_id": c.id,
                    "new_start": c.start_time,
                    "new_end": c.end_time
                })
        
        self.db.session.commit()
        
        return {
            "success": True,
            "deleted_clip_id": clip_id,
            "gap_filled": gap_duration,
            "moved_clips": moved_clips
        }
    
    # ========== CROSSFADES ==========
    
    def create_crossfade(
        self,
        clip1_id: int,
        clip2_id: int,
        duration: float = 0.5
    ) -> Dict[str, Any]:
        """Create a crossfade between two adjacent clips.
        
        Args:
            clip1_id: First clip (will fade out)
            clip2_id: Second clip (will fade in)
            duration: Crossfade duration in seconds
        
        Returns:
            Dict with success status
        """
        from flask_dashboard import AudioClip
        
        clip1 = AudioClip.query.get(clip1_id)
        clip2 = AudioClip.query.get(clip2_id)
        
        if not clip1 or not clip2:
            return {"success": False, "error": "Clip not found"}
        
        if clip1.is_locked or clip2.is_locked:
            return {"success": False, "error": "One or both clips are locked"}
        
        # Verify clips are adjacent or overlapping
        if clip2.start_time < clip1.end_time - 0.01:  # Small tolerance
            # Overlapping - apply crossfade to overlap region
            overlap = clip1.end_time - clip2.start_time
            crossfade_duration = min(duration, overlap)
        elif clip2.start_time > clip1.end_time + 0.01:
            return {"success": False, "error": "Clips are not adjacent"}
        else:
            # Adjacent - no overlap, can't crossfade
            return {"success": False, "error": "Clips must overlap for crossfade"}
        
        # Apply fades
        clip1.fade_out_duration = crossfade_duration
        clip1.fade_out_curve = "exponential"
        
        clip2.fade_in_duration = crossfade_duration
        clip2.fade_in_curve = "logarithmic"
        
        self.db.session.commit()
        
        return {
            "success": True,
            "clip1_id": clip1_id,
            "clip2_id": clip2_id,
            "crossfade_duration": crossfade_duration
        }
    
    # ========== CLIP DUPLICATION ==========
    
    def duplicate_clip(
        self,
        clip_id: int,
        offset: float = 0.0
    ) -> Dict[str, Any]:
        """Duplicate a clip on the timeline.
        
        Args:
            clip_id: Clip to duplicate
            offset: Time offset for the duplicate (0 = place immediately after)
        
        Returns:
            Dict with new clip ID
        """
        from flask_dashboard import AudioClip
        
        clip = AudioClip.query.get(clip_id)
        if not clip:
            return {"success": False, "error": "Clip not found"}
        
        # Calculate new position
        if offset == 0.0:
            # Place immediately after original
            new_start = clip.end_time
        else:
            new_start = clip.start_time + offset
        
        # Snap to grid
        if self.snap_enabled:
            new_start = self._snap_to_grid(new_start)
        
        duration = clip.end_time - clip.start_time
        
        # Create duplicate
        new_clip = AudioClip(
            project_id=clip.project_id,
            track_id=clip.track_id,
            asset_id=clip.asset_id,
            start_time=new_start,
            end_time=new_start + duration,
            source_start=clip.source_start,
            source_end=clip.source_end,
            clip_gain=clip.clip_gain,
            pitch_shift=clip.pitch_shift,
            time_stretch=clip.time_stretch,
            fade_in_duration=clip.fade_in_duration,
            fade_out_duration=clip.fade_out_duration,
            fade_in_curve=clip.fade_in_curve,
            fade_out_curve=clip.fade_out_curve,
            clip_effects=clip.clip_effects,
            clip_color=clip.clip_color,
            clip_name=f"{clip.clip_name} (Copy)" if clip.clip_name else None
        )
        
        self.db.session.add(new_clip)
        self.db.session.commit()
        
        return {
            "success": True,
            "original_clip_id": clip_id,
            "new_clip_id": new_clip.id,
            "new_start_time": new_start,
            "new_end_time": new_start + duration
        }
    
    # ========== SNAP TO GRID ==========
    
    def set_snap_grid(self, grid_size: float, enabled: bool = True):
        """Set snap-to-grid settings.
        
        Args:
            grid_size: Grid size in seconds (e.g., 0.1 = 100ms, 1.0 = 1 second)
            enabled: Whether snap is enabled
        """
        self.snap_grid_size = grid_size
        self.snap_enabled = enabled
    
    def _snap_to_grid(self, time: float) -> float:
        """Snap a time value to the nearest grid point.
        
        Args:
            time: Time in seconds
        
        Returns:
            Snapped time
        """
        if not self.snap_enabled or self.snap_grid_size == 0:
            return time
        
        return round(time / self.snap_grid_size) * self.snap_grid_size
    
    # ========== TIMELINE QUERIES ==========
    
    def get_timeline_clips(
        self,
        project_id: int,
        track_id: Optional[int] = None,
        time_range: Optional[Tuple[float, float]] = None
    ) -> List[Dict[str, Any]]:
        """Get all clips on the timeline with optional filtering.
        
        Args:
            project_id: Project ID
            track_id: Optional track filter
            time_range: Optional (start, end) time range filter
        
        Returns:
            List of clip dictionaries
        """
        from flask_dashboard import AudioClip, AudioAsset
        
        query = AudioClip.query.filter_by(project_id=project_id)
        
        if track_id is not None:
            query = query.filter_by(track_id=track_id)
        
        if time_range is not None:
            start, end = time_range
            query = query.filter(
                AudioClip.start_time < end,
                AudioClip.end_time > start
            )
        
        clips = query.order_by(AudioClip.start_time).all()
        
        # Fetch assets for waveform URLs
        asset_ids = list(set(c.asset_id for c in clips))
        assets = AudioAsset.query.filter(AudioAsset.id.in_(asset_ids)).all() if asset_ids else []
        asset_map = {a.id: a for a in assets}
        
        return [{
            "id": c.id,
            "track_id": c.track_id,
            "asset_id": c.asset_id,
            "asset_name": asset_map[c.asset_id].name if c.asset_id in asset_map else None,
            "waveform_url": asset_map[c.asset_id].waveform_url if c.asset_id in asset_map else None,
            "start_time": c.start_time,
            "end_time": c.end_time,
            "source_start": c.source_start,
            "source_end": c.source_end,
            "clip_gain": c.clip_gain,
            "pitch_shift": c.pitch_shift,
            "time_stretch": c.time_stretch,
            "fade_in_duration": c.fade_in_duration,
            "fade_out_duration": c.fade_out_duration,
            "clip_color": c.clip_color,
            "clip_name": c.clip_name,
            "is_locked": c.is_locked
        } for c in clips]
    
    def get_project_duration(self, project_id: int) -> float:
        """Get total duration of project (based on rightmost clip).
        
        Args:
            project_id: Project ID
        
        Returns:
            Duration in seconds
        """
        from flask_dashboard import AudioClip
        from sqlalchemy import func
        
        max_end = self.db.session.query(func.max(AudioClip.end_time)).filter_by(
            project_id=project_id
        ).scalar()
        
        return max_end if max_end else 0.0
