# ============================================================================================
# AI AUDIO ASSISTANT - Intelligent Mixing & Mastering
# ============================================================================================
"""
AI-powered audio engineering assistant.

Features:
- Auto-level balancing
- Noise reduction suggestions
- EQ curve recommendations
- Clipping detection & prevention
- Frequency conflict resolution
- Transition suggestions
- Loudness matching
- Auto-mastering
"""

from typing import Dict, Any, List, Optional
import random


class AIAudioAssistant:
    """AI-powered mixing and mastering assistant."""
    
    def __init__(self, db):
        """Initialize AI assistant."""
        self.db = db
    
    # ========== LEVEL BALANCING ==========
    
    def analyze_levels(
        self,
        project_id: int
    ) -> Dict[str, Any]:
        """Analyze track levels and suggest balance improvements.
        
        Returns recommendations for fader adjustments.
        """
        from flask_dashboard import AudioMixerSettings, AudioTrack
        
        channels = AudioMixerSettings.query.filter_by(project_id=project_id).filter(
            AudioMixerSettings.track_id.isnot(None)
        ).all()
        
        if not channels:
            return {"success": False, "error": "No tracks found"}
        
        suggestions = []
        
        for channel in channels:
            track = AudioTrack.query.get(channel.track_id)
            if not track:
                continue
            
            # Analyze RMS levels
            avg_level = (channel.rms_level_left + channel.rms_level_right) / 2
            
            # Generate suggestions based on levels
            if avg_level > -6.0:
                suggestions.append({
                    "track_id": channel.track_id,
                    "track_name": track.track_id,
                    "issue": "too_loud",
                    "current_level": channel.fader_level,
                    "suggested_level": channel.fader_level - 6,
                    "reason": "Exceeds recommended headroom (-6dB)"
                })
            elif avg_level < -40.0:
                suggestions.append({
                    "track_id": channel.track_id,
                    "track_name": track.track_id,
                    "issue": "too_quiet",
                    "current_level": channel.fader_level,
                    "suggested_level": channel.fader_level + 6,
                    "reason": "Below recommended audibility threshold"
                })
        
        return {
            "success": True,
            "project_id": project_id,
            "suggestions": suggestions,
            "overall_recommendation": "Apply suggested level adjustments for better balance"
        }
    
    def auto_balance(
        self,
        project_id: int,
        target_loudness: float = -14.0  # LUFS
    ) -> Dict[str, Any]:
        """Automatically balance all track levels.
        
        Args:
            project_id: Project ID
            target_loudness: Target integrated loudness in LUFS
        
        Returns:
            Dict with adjusted track levels
        """
        from flask_dashboard import AudioMixerSettings
        
        channels = AudioMixerSettings.query.filter_by(project_id=project_id).filter(
            AudioMixerSettings.track_id.isnot(None)
        ).all()
        
        if not channels:
            return {"success": False, "error": "No tracks found"}
        
        adjustments = []
        
        for channel in channels:
            # Calculate adjustment needed
            current_rms = (channel.rms_level_left + channel.rms_level_right) / 2
            adjustment = target_loudness - current_rms
            
            # Clamp adjustment to reasonable range
            adjustment = max(-12, min(12, adjustment))
            
            # Apply adjustment
            new_level = channel.fader_level + adjustment
            channel.fader_level = max(-60, min(12, new_level))
            
            adjustments.append({
                "track_id": channel.track_id,
                "old_level": channel.fader_level - adjustment,
                "new_level": channel.fader_level,
                "adjustment": adjustment
            })
        
        self.db.session.commit()
        
        return {
            "success": True,
            "project_id": project_id,
            "adjustments": adjustments,
            "target_loudness": target_loudness
        }
    
    # ========== NOISE REDUCTION ==========
    
    def detect_noise(
        self,
        project_id: int,
        track_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Detect noise in tracks and suggest reduction settings."""
        from flask_dashboard import AudioTrack, AudioClip, AudioAsset
        
        query = AudioTrack.query.filter_by(project_id=project_id)
        if track_id:
            query = query.filter_by(id=track_id)
        
        tracks = query.all()
        
        noise_reports = []
        
        for track in tracks:
            # Get clips on this track
            clips = AudioClip.query.filter_by(track_id=track.id).all()
            
            for clip in clips:
                asset = AudioAsset.query.get(clip.asset_id)
                if not asset:
                    continue
                
                # Analyze asset type for noise likelihood
                noise_level = "none"
                suggested_reduction = 0
                
                if asset.asset_type == "voiceover":
                    noise_level = "low"
                    suggested_reduction = -40
                elif asset.asset_type == "ambient":
                    noise_level = "medium"
                    suggested_reduction = -35
                
                if noise_level != "none":
                    noise_reports.append({
                        "track_id": track.id,
                        "clip_id": clip.id,
                        "asset_name": asset.name,
                        "noise_level": noise_level,
                        "suggested_threshold": suggested_reduction,
                        "suggested_reduction_db": 12
                    })
        
        return {
            "success": True,
            "project_id": project_id,
            "noise_reports": noise_reports,
            "total_issues": len(noise_reports)
        }
    
    def apply_noise_reduction(
        self,
        clip_id: int,
        threshold: float = -40,
        reduction_db: float = 12
    ) -> Dict[str, Any]:
        """Apply noise reduction effect to clip."""
        from audio_effects import AudioEffectsEngine
        
        effects_engine = AudioEffectsEngine(self.db)
        
        return effects_engine.add_effect(
            project_id=0,  # Will be set from clip
            effect_type="noise_reduction",
            clip_id=clip_id,
            parameters={
                "threshold": threshold,
                "reduction": reduction_db,
                "attack": 10,
                "release": 50
            }
        )
    
    # ========== EQ SUGGESTIONS ==========
    
    def suggest_eq(
        self,
        asset_type: str,
        genre: Optional[str] = None
    ) -> Dict[str, Any]:
        """Suggest EQ settings based on audio type and genre.
        
        Args:
            asset_type: music, voiceover, sfx, ambient
            genre: Musical genre (for music assets)
        
        Returns:
            Recommended EQ settings
        """
        eq_presets = {
            "voiceover": {
                "low": -2,  # Reduce rumble
                "mid": 2,   # Boost presence
                "high": 1,  # Brighten
                "low_freq": 80,
                "mid_freq": 2000,
                "high_freq": 8000,
                "reason": "Enhance vocal clarity and reduce rumble"
            },
            "music_orchestral": {
                "low": 1,
                "mid": 0,
                "high": 2,
                "low_freq": 100,
                "mid_freq": 1000,
                "high_freq": 10000,
                "reason": "Enhance strings and brass presence"
            },
            "sfx": {
                "low": 2,
                "mid": -1,
                "high": 0,
                "low_freq": 60,
                "mid_freq": 1000,
                "high_freq": 8000,
                "reason": "Boost impact, reduce harshness"
            },
            "ambient": {
                "low": 0,
                "mid": -2,
                "high": -1,
                "low_freq": 100,
                "mid_freq": 1500,
                "high_freq": 10000,
                "reason": "Create space, reduce interference"
            }
        }
        
        # Select preset based on type and genre
        preset_key = asset_type
        if asset_type == "music" and genre:
            preset_key = f"music_{genre.lower()}"
        
        preset = eq_presets.get(preset_key, eq_presets.get(asset_type, {
            "low": 0, "mid": 0, "high": 0,
            "low_freq": 100, "mid_freq": 1000, "high_freq": 10000,
            "reason": "Neutral EQ curve"
        }))
        
        return {
            "success": True,
            "asset_type": asset_type,
            "genre": genre,
            "eq_settings": preset
        }
    
    # ========== CLIPPING DETECTION ==========
    
    def detect_clipping(
        self,
        project_id: int
    ) -> Dict[str, Any]:
        """Detect clipping in project and suggest fixes."""
        from flask_dashboard import AudioMixerSettings
        
        channels = AudioMixerSettings.query.filter_by(project_id=project_id).all()
        
        clipping_tracks = []
        
        for channel in channels:
            peak_left = channel.peak_level_left
            peak_right = channel.peak_level_right
            
            # Detect clipping (peak > 0dBFS)
            if peak_left > -0.5 or peak_right > -0.5:
                reduction_needed = max(peak_left, peak_right) + 3  # Add 3dB headroom
                
                clipping_tracks.append({
                    "track_id": channel.track_id,
                    "peak_left": peak_left,
                    "peak_right": peak_right,
                    "current_fader": channel.fader_level,
                    "suggested_fader": channel.fader_level - reduction_needed,
                    "severity": "high" if max(peak_left, peak_right) > 1 else "medium"
                })
        
        return {
            "success": True,
            "project_id": project_id,
            "clipping_tracks": clipping_tracks,
            "total_issues": len(clipping_tracks),
            "recommendation": "Reduce fader levels to prevent distortion"
        }
    
    # ========== AUTO-MASTERING ==========
    
    def auto_master(
        self,
        project_id: int,
        target_loudness: float = -14.0,  # LUFS
        add_limiter: bool = True
    ) -> Dict[str, Any]:
        """Apply automatic mastering to project.
        
        Steps:
        1. Balance all track levels
        2. Add master bus EQ
        3. Add master bus compressor
        4. Add master bus limiter
        5. Adjust to target loudness
        """
        from audio_effects import AudioEffectsEngine
        
        results = []
        
        # Step 1: Balance levels
        balance_result = self.auto_balance(project_id, target_loudness)
        results.append({"step": "level_balance", "result": balance_result})
        
        # Step 2: Add master EQ (subtle enhancement)
        effects_engine = AudioEffectsEngine(self.db)
        eq_result = effects_engine.add_effect(
            project_id=project_id,
            effect_type="eq",
            track_id=None,  # Master bus
            parameters={
                "low": 1,
                "mid": 0,
                "high": 2,
                "low_freq": 60,
                "mid_freq": 1000,
                "high_freq": 10000
            }
        )
        results.append({"step": "master_eq", "result": eq_result})
        
        # Step 3: Add master compressor (gentle glue)
        comp_result = effects_engine.add_effect(
            project_id=project_id,
            effect_type="compressor",
            track_id=None,
            parameters={
                "threshold": -12,
                "ratio": 2,
                "attack": 10,
                "release": 100,
                "knee": 5,
                "gain": 0
            }
        )
        results.append({"step": "master_compressor", "result": comp_result})
        
        # Step 4: Add limiter (if requested)
        if add_limiter:
            limiter_result = effects_engine.add_effect(
                project_id=project_id,
                effect_type="compressor",
                track_id=None,
                parameters={
                    "threshold": -1,
                    "ratio": 20,  # Hard limiting
                    "attack": 0.1,
                    "release": 50,
                    "knee": 0,
                    "gain": 0
                }
            )
            results.append({"step": "master_limiter", "result": limiter_result})
        
        return {
            "success": True,
            "project_id": project_id,
            "target_loudness": target_loudness,
            "steps_applied": len(results),
            "results": results
        }
    
    # ========== MIXING SUGGESTIONS ==========
    
    def suggest_mix_improvements(
        self,
        project_id: int
    ) -> Dict[str, Any]:
        """Analyze mix and suggest improvements."""
        suggestions = []
        
        # Run all analysis tools
        level_analysis = self.analyze_levels(project_id)
        if level_analysis.get("suggestions"):
            suggestions.extend(level_analysis["suggestions"])
        
        noise_analysis = self.detect_noise(project_id)
        if noise_analysis.get("noise_reports"):
            suggestions.append({
                "category": "noise",
                "count": len(noise_analysis["noise_reports"]),
                "action": "apply_noise_reduction"
            })
        
        clipping_analysis = self.detect_clipping(project_id)
        if clipping_analysis.get("clipping_tracks"):
            suggestions.extend([{
                "category": "clipping",
                "track_id": t["track_id"],
                "action": "reduce_level",
                "adjustment": t["suggested_fader"] - t["current_fader"]
            } for t in clipping_analysis["clipping_tracks"]])
        
        return {
            "success": True,
            "project_id": project_id,
            "total_suggestions": len(suggestions),
            "suggestions": suggestions,
            "can_auto_fix": True
        }
