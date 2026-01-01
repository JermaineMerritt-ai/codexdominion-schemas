# ============================================================================================
# AUDIO MIXER - Professional Mixing Console
# ============================================================================================
"""
Complete mixing console with:
- Channel strips (fader, pan, mute, solo)
- Master bus processing
- Send/return management
- Metering and level monitoring
- Track routing

This is the heart of sound control in the Audio Studio.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class ChannelStrip:
    """Represents a mixer channel strip."""
    track_id: int
    fader_level: float  # dB
    pan_position: float  # -1.0 to 1.0
    is_muted: bool
    is_solo: bool
    reverb_send: float
    delay_send: float
    track_color: str


class AudioMixer:
    """Professional audio mixing console."""
    
    def __init__(self, db):
        """Initialize mixer with database connection."""
        self.db = db
    
    # ========== CHANNEL STRIP MANAGEMENT ==========
    
    def init_channel_strip(
        self,
        project_id: int,
        track_id: int,
        **initial_settings
    ) -> Dict[str, Any]:
        """Initialize mixer settings for a track.
        
        Args:
            project_id: Project ID
            track_id: Track ID
            **initial_settings: Initial mixer settings
        
        Returns:
            Dict with success status and settings
        """
        from flask_dashboard import AudioMixerSettings
        
        # Check if settings already exist
        existing = AudioMixerSettings.query.filter_by(
            project_id=project_id,
            track_id=track_id
        ).first()
        
        if existing:
            return {"success": False, "error": "Channel strip already exists"}
        
        # Create channel strip
        channel = AudioMixerSettings(
            project_id=project_id,
            track_id=track_id,
            fader_level=initial_settings.get('fader_level', 0.0),
            pan_position=initial_settings.get('pan_position', 0.0),
            is_muted=initial_settings.get('is_muted', False),
            is_solo=initial_settings.get('is_solo', False),
            reverb_send=initial_settings.get('reverb_send', 0.0),
            delay_send=initial_settings.get('delay_send', 0.0),
            track_color=initial_settings.get('track_color', '#00D9FF')
        )
        
        self.db.session.add(channel)
        self.db.session.commit()
        
        return {
            "success": True,
            "channel_id": channel.id,
            "track_id": track_id
        }
    
    def update_fader(
        self,
        project_id: int,
        track_id: int,
        level_db: float
    ) -> Dict[str, Any]:
        """Update track fader level.
        
        Args:
            project_id: Project ID
            track_id: Track ID
            level_db: Level in dB (-60 to +12)
        
        Returns:
            Dict with success status
        """
        from flask_dashboard import AudioMixerSettings
        
        # Clamp level
        level_db = max(-60.0, min(12.0, level_db))
        
        channel = AudioMixerSettings.query.filter_by(
            project_id=project_id,
            track_id=track_id
        ).first()
        
        if not channel:
            # Auto-create if doesn't exist
            result = self.init_channel_strip(project_id, track_id, fader_level=level_db)
            return result
        
        channel.fader_level = level_db
        self.db.session.commit()
        
        return {
            "success": True,
            "track_id": track_id,
            "fader_level": level_db
        }
    
    def update_pan(
        self,
        project_id: int,
        track_id: int,
        pan_position: float
    ) -> Dict[str, Any]:
        """Update track pan position.
        
        Args:
            project_id: Project ID
            track_id: Track ID
            pan_position: Pan position (-1.0 left to 1.0 right)
        
        Returns:
            Dict with success status
        """
        from flask_dashboard import AudioMixerSettings
        
        # Clamp pan
        pan_position = max(-1.0, min(1.0, pan_position))
        
        channel = AudioMixerSettings.query.filter_by(
            project_id=project_id,
            track_id=track_id
        ).first()
        
        if not channel:
            result = self.init_channel_strip(project_id, track_id, pan_position=pan_position)
            return result
        
        channel.pan_position = pan_position
        self.db.session.commit()
        
        return {
            "success": True,
            "track_id": track_id,
            "pan_position": pan_position
        }
    
    def toggle_mute(
        self,
        project_id: int,
        track_id: int
    ) -> Dict[str, Any]:
        """Toggle mute state for a track.
        
        Args:
            project_id: Project ID
            track_id: Track ID
        
        Returns:
            Dict with success status and new mute state
        """
        from flask_dashboard import AudioMixerSettings
        
        channel = AudioMixerSettings.query.filter_by(
            project_id=project_id,
            track_id=track_id
        ).first()
        
        if not channel:
            result = self.init_channel_strip(project_id, track_id, is_muted=True)
            return {**result, "is_muted": True}
        
        channel.is_muted = not channel.is_muted
        self.db.session.commit()
        
        return {
            "success": True,
            "track_id": track_id,
            "is_muted": channel.is_muted
        }
    
    def toggle_solo(
        self,
        project_id: int,
        track_id: int
    ) -> Dict[str, Any]:
        """Toggle solo state for a track.
        
        When soloed, only soloed tracks play.
        
        Args:
            project_id: Project ID
            track_id: Track ID
        
        Returns:
            Dict with success status and new solo state
        """
        from flask_dashboard import AudioMixerSettings
        
        channel = AudioMixerSettings.query.filter_by(
            project_id=project_id,
            track_id=track_id
        ).first()
        
        if not channel:
            result = self.init_channel_strip(project_id, track_id, is_solo=True)
            return {**result, "is_solo": True}
        
        channel.is_solo = not channel.is_solo
        self.db.session.commit()
        
        return {
            "success": True,
            "track_id": track_id,
            "is_solo": channel.is_solo
        }
    
    # ========== SEND/RETURN MANAGEMENT ==========
    
    def update_send_level(
        self,
        project_id: int,
        track_id: int,
        send_type: str,
        level_db: float
    ) -> Dict[str, Any]:
        """Update send level for reverb, delay, or aux buses.
        
        Args:
            project_id: Project ID
            track_id: Track ID
            send_type: reverb, delay, aux_1, aux_2
            level_db: Send level in dB (-60 to +12)
        
        Returns:
            Dict with success status
        """
        from flask_dashboard import AudioMixerSettings
        
        # Clamp level
        level_db = max(-60.0, min(12.0, level_db))
        
        channel = AudioMixerSettings.query.filter_by(
            project_id=project_id,
            track_id=track_id
        ).first()
        
        if not channel:
            initial = {f"{send_type}_send": level_db}
            return self.init_channel_strip(project_id, track_id, **initial)
        
        # Update appropriate send
        if send_type == "reverb":
            channel.reverb_send = level_db
        elif send_type == "delay":
            channel.delay_send = level_db
        elif send_type == "aux_1":
            channel.aux_1_send = level_db
        elif send_type == "aux_2":
            channel.aux_2_send = level_db
        else:
            return {"success": False, "error": f"Unknown send type: {send_type}"}
        
        self.db.session.commit()
        
        return {
            "success": True,
            "track_id": track_id,
            "send_type": send_type,
            "level_db": level_db
        }
    
    # ========== MASTER BUS ==========
    
    def init_master_bus(
        self,
        project_id: int
    ) -> Dict[str, Any]:
        """Initialize master bus settings.
        
        Args:
            project_id: Project ID
        
        Returns:
            Dict with success status
        """
        from flask_dashboard import AudioMixerSettings
        
        # Check if master bus exists (track_id = NULL)
        existing = AudioMixerSettings.query.filter_by(
            project_id=project_id,
            track_id=None
        ).first()
        
        if existing:
            return {"success": False, "error": "Master bus already exists"}
        
        master = AudioMixerSettings(
            project_id=project_id,
            track_id=None,
            fader_level=0.0,
            pan_position=0.0,
            track_color="#FFD700"  # Gold for master
        )
        
        self.db.session.add(master)
        self.db.session.commit()
        
        return {
            "success": True,
            "master_bus_id": master.id
        }
    
    def update_master_fader(
        self,
        project_id: int,
        level_db: float
    ) -> Dict[str, Any]:
        """Update master bus fader level.
        
        Args:
            project_id: Project ID
            level_db: Master level in dB (-60 to +12)
        
        Returns:
            Dict with success status
        """
        from flask_dashboard import AudioMixerSettings
        
        level_db = max(-60.0, min(12.0, level_db))
        
        master = AudioMixerSettings.query.filter_by(
            project_id=project_id,
            track_id=None
        ).first()
        
        if not master:
            self.init_master_bus(project_id)
            master = AudioMixerSettings.query.filter_by(
                project_id=project_id,
                track_id=None
            ).first()
        
        master.fader_level = level_db
        self.db.session.commit()
        
        return {
            "success": True,
            "master_level": level_db
        }
    
    # ========== METERING ==========
    
    def update_metering(
        self,
        project_id: int,
        track_id: Optional[int],
        peak_left: float,
        peak_right: float,
        rms_left: float,
        rms_right: float
    ) -> Dict[str, Any]:
        """Update metering levels for a track or master bus.
        
        Args:
            project_id: Project ID
            track_id: Track ID (None for master bus)
            peak_left/right: Peak levels in dBFS
            rms_left/right: RMS levels in dBFS
        
        Returns:
            Dict with success status
        """
        from flask_dashboard import AudioMixerSettings
        
        channel = AudioMixerSettings.query.filter_by(
            project_id=project_id,
            track_id=track_id
        ).first()
        
        if not channel:
            return {"success": False, "error": "Channel not found"}
        
        channel.peak_level_left = peak_left
        channel.peak_level_right = peak_right
        channel.rms_level_left = rms_left
        channel.rms_level_right = rms_right
        
        self.db.session.commit()
        
        return {
            "success": True,
            "track_id": track_id,
            "peak_levels": [peak_left, peak_right],
            "rms_levels": [rms_left, rms_right]
        }
    
    # ========== MIXER STATE ==========
    
    def get_mixer_state(
        self,
        project_id: int
    ) -> Dict[str, Any]:
        """Get complete mixer state for a project.
        
        Args:
            project_id: Project ID
        
        Returns:
            Dict with all channel strips and master bus settings
        """
        from flask_dashboard import AudioMixerSettings, AudioTrack
        
        # Get all channel strips
        channels = AudioMixerSettings.query.filter_by(project_id=project_id).all()
        
        # Separate master bus from track channels
        master = None
        track_channels = []
        
        for channel in channels:
            if channel.track_id is None:
                master = {
                    "fader_level": channel.fader_level,
                    "pan_position": channel.pan_position,
                    "peak_levels": [channel.peak_level_left, channel.peak_level_right],
                    "rms_levels": [channel.rms_level_left, channel.rms_level_right]
                }
            else:
                # Get track info
                track = AudioTrack.query.get(channel.track_id)
                track_channels.append({
                    "track_id": channel.track_id,
                    "track_name": track.track_id if track else f"Track {channel.track_id}",
                    "fader_level": channel.fader_level,
                    "pan_position": channel.pan_position,
                    "is_muted": channel.is_muted,
                    "is_solo": channel.is_solo,
                    "is_armed": channel.is_armed,
                    "reverb_send": channel.reverb_send,
                    "delay_send": channel.delay_send,
                    "aux_1_send": channel.aux_1_send,
                    "aux_2_send": channel.aux_2_send,
                    "track_color": channel.track_color,
                    "peak_levels": [channel.peak_level_left, channel.peak_level_right],
                    "rms_levels": [channel.rms_level_left, channel.rms_level_right]
                })
        
        return {
            "success": True,
            "project_id": project_id,
            "master_bus": master,
            "tracks": track_channels,
            "track_count": len(track_channels)
        }
    
    def reset_mixer(
        self,
        project_id: int
    ) -> Dict[str, Any]:
        """Reset all mixer settings to defaults.
        
        Args:
            project_id: Project ID
        
        Returns:
            Dict with success status
        """
        from flask_dashboard import AudioMixerSettings
        
        channels = AudioMixerSettings.query.filter_by(project_id=project_id).all()
        
        for channel in channels:
            channel.fader_level = 0.0
            channel.pan_position = 0.0
            channel.is_muted = False
            channel.is_solo = False
            channel.reverb_send = 0.0
            channel.delay_send = 0.0
            channel.aux_1_send = 0.0
            channel.aux_2_send = 0.0
        
        self.db.session.commit()
        
        return {
            "success": True,
            "message": f"Reset {len(channels)} channel strips"
        }
    
    # ========== UTILITY FUNCTIONS ==========
    
    def db_to_linear(self, db: float) -> float:
        """Convert dB to linear amplitude.
        
        Args:
            db: Level in dB
        
        Returns:
            Linear amplitude (0.0 to 1.0+)
        """
        import math
        return 10 ** (db / 20.0)
    
    def linear_to_db(self, linear: float) -> float:
        """Convert linear amplitude to dB.
        
        Args:
            linear: Linear amplitude
        
        Returns:
            Level in dB
        """
        import math
        if linear <= 0:
            return -60.0  # Minimum
        return 20 * math.log10(linear)
    
    def calculate_pan_law(
        self,
        pan_position: float,
        pan_law: str = "constant_power"
    ) -> tuple[float, float]:
        """Calculate left/right gains for pan position.
        
        Args:
            pan_position: Pan position (-1.0 to 1.0)
            pan_law: constant_power, constant_gain, or linear
        
        Returns:
            Tuple of (left_gain, right_gain)
        """
        import math
        
        # Normalize pan from -1..1 to 0..1
        pan_normalized = (pan_position + 1.0) / 2.0
        
        if pan_law == "constant_power":
            # -3dB pan law (most common)
            left_gain = math.cos(pan_normalized * math.pi / 2)
            right_gain = math.sin(pan_normalized * math.pi / 2)
        elif pan_law == "constant_gain":
            # -6dB pan law
            left_gain = 1.0 - pan_normalized
            right_gain = pan_normalized
        else:  # linear
            left_gain = 1.0 - pan_normalized
            right_gain = pan_normalized
        
        return (left_gain, right_gain)
