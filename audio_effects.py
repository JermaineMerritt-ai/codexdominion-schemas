# ============================================================================================
# AUDIO EFFECTS - Built-in Effects Processing
# ============================================================================================
"""
Built-in audio effects with effect chain management.

Effects:
- EQ (3-band parametric)
- Compressor (dynamics control)
- Reverb (room simulation)
- Delay (echo/delay)
- Chorus (modulation)
- Distortion (saturation)
- Filter (low-pass, high-pass, band-pass)
- Noise Reduction (denoising)
"""

from typing import Dict, Any, List, Optional


class AudioEffectsEngine:
    """Complete audio effects processing system."""
    
    def __init__(self, db):
        """Initialize effects engine."""
        self.db = db
        
        # Effect templates with default parameters
        self.effect_templates = {
            "eq": {
                "low": 0, "mid": 0, "high": 0,
                "low_freq": 100, "mid_freq": 1000, "high_freq": 10000
            },
            "compressor": {
                "threshold": -20, "ratio": 4, "attack": 5, "release": 100, "knee": 3, "gain": 0
            },
            "reverb": {
                "wet": 0.3, "dry": 0.7, "room_size": 0.5, "decay": 2.0, "pre_delay": 10, "damping": 0.5
            },
            "delay": {
                "time": 0.5, "feedback": 0.3, "wet": 0.25, "dry": 0.75, "sync": True, "ping_pong": False
            },
            "chorus": {
                "rate": 0.5, "depth": 0.3, "mix": 0.5, "voices": 2
            },
            "distortion": {
                "drive": 0.5, "tone": 0.5, "mix": 0.5, "type": "soft"
            },
            "filter": {
                "type": "lowpass", "cutoff": 1000, "resonance": 0.5, "slope": "12db"
            },
            "noise_reduction": {
                "threshold": -40, "reduction": 12, "attack": 10, "release": 50
            }
        }
    
    # ========== EFFECT MANAGEMENT ==========
    
    def add_effect(
        self,
        project_id: int,
        effect_type: str,
        track_id: Optional[int] = None,
        clip_id: Optional[int] = None,
        parameters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Add effect to track or clip.
        
        Args:
            project_id: Project ID
            effect_type: eq, compressor, reverb, delay, etc.
            track_id: Track ID (for track effect)
            clip_id: Clip ID (for clip effect)
            parameters: Effect parameters (uses defaults if not provided)
        """
        from flask_dashboard import AudioEffect
        from sqlalchemy import func
        
        if effect_type not in self.effect_templates:
            return {"success": False, "error": f"Unknown effect type: {effect_type}"}
        
        # Get default parameters and merge with provided ones
        default_params = self.effect_templates[effect_type].copy()
        if parameters:
            default_params.update(parameters)
        
        # Get next order index
        query = AudioEffect.query.filter_by(project_id=project_id)
        if track_id:
            query = query.filter_by(track_id=track_id)
        if clip_id:
            query = query.filter_by(clip_id=clip_id)
        
        max_order = self.db.session.query(func.max(AudioEffect.order_index)).filter(
            AudioEffect.project_id == project_id
        ).scalar() or 0
        
        effect = AudioEffect(
            project_id=project_id,
            track_id=track_id,
            clip_id=clip_id,
            effect_type=effect_type,
            parameters=default_params,
            order_index=max_order + 1,
            is_enabled=True
        )
        
        self.db.session.add(effect)
        self.db.session.commit()
        
        return {
            "success": True,
            "effect_id": effect.id,
            "effect_type": effect_type,
            "parameters": default_params,
            "order_index": effect.order_index
        }
    
    def update_effect(
        self,
        effect_id: int,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update effect parameters."""
        from flask_dashboard import AudioEffect
        
        effect = AudioEffect.query.get(effect_id)
        if not effect:
            return {"success": False, "error": "Effect not found"}
        
        current_params = effect.parameters or {}
        current_params.update(parameters)
        effect.parameters = current_params
        
        self.db.session.commit()
        
        return {
            "success": True,
            "effect_id": effect_id,
            "parameters": current_params
        }
    
    def remove_effect(self, effect_id: int) -> Dict[str, Any]:
        """Remove effect from chain."""
        from flask_dashboard import AudioEffect
        
        effect = AudioEffect.query.get(effect_id)
        if not effect:
            return {"success": False, "error": "Effect not found"}
        
        self.db.session.delete(effect)
        self.db.session.commit()
        
        return {"success": True, "message": "Effect removed"}
    
    def toggle_effect(self, effect_id: int) -> Dict[str, Any]:
        """Enable/disable effect."""
        from flask_dashboard import AudioEffect
        
        effect = AudioEffect.query.get(effect_id)
        if not effect:
            return {"success": False, "error": "Effect not found"}
        
        effect.is_enabled = not effect.is_enabled
        self.db.session.commit()
        
        return {"success": True, "effect_id": effect_id, "is_enabled": effect.is_enabled}
    
    def bypass_effect(self, effect_id: int) -> Dict[str, Any]:
        """Toggle bypass state."""
        from flask_dashboard import AudioEffect
        
        effect = AudioEffect.query.get(effect_id)
        if not effect:
            return {"success": False, "error": "Effect not found"}
        
        effect.is_bypassed = not effect.is_bypassed
        self.db.session.commit()
        
        return {"success": True, "effect_id": effect_id, "is_bypassed": effect.is_bypassed}
    
    # ========== EFFECT CHAIN ==========
    
    def reorder_effects(
        self,
        project_id: int,
        effect_order: List[int],
        track_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Reorder effects in chain."""
        from flask_dashboard import AudioEffect
        
        for i, effect_id in enumerate(effect_order):
            effect = AudioEffect.query.get(effect_id)
            if effect and effect.project_id == project_id:
                if track_id is None or effect.track_id == track_id:
                    effect.order_index = i
        
        self.db.session.commit()
        
        return {"success": True, "new_order": effect_order}
    
    def get_effect_chain(
        self,
        project_id: int,
        track_id: Optional[int] = None,
        clip_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get effect chain for track or clip."""
        from flask_dashboard import AudioEffect
        
        query = AudioEffect.query.filter_by(project_id=project_id)
        
        if track_id is not None:
            query = query.filter_by(track_id=track_id)
        if clip_id is not None:
            query = query.filter_by(clip_id=clip_id)
        
        effects = query.order_by(AudioEffect.order_index).all()
        
        return [{
            "id": e.id,
            "effect_type": e.effect_type,
            "parameters": e.parameters,
            "order_index": e.order_index,
            "is_enabled": e.is_enabled,
            "is_bypassed": e.is_bypassed,
            "preset_name": e.preset_name
        } for e in effects]
    
    # ========== PRESETS ==========
    
    def save_preset(
        self,
        user_id: int,
        effect_type: str,
        name: str,
        parameters: Dict[str, Any],
        category: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Save effect preset."""
        from flask_dashboard import AudioEffectPreset
        
        preset = AudioEffectPreset(
            user_id=user_id,
            effect_type=effect_type,
            name=name,
            description=description,
            category=category,
            parameters=parameters,
            is_public=False
        )
        
        self.db.session.add(preset)
        self.db.session.commit()
        
        return {
            "success": True,
            "preset_id": preset.id,
            "name": name
        }
    
    def load_preset(
        self,
        effect_id: int,
        preset_id: int
    ) -> Dict[str, Any]:
        """Load preset into effect."""
        from flask_dashboard import AudioEffect, AudioEffectPreset
        
        effect = AudioEffect.query.get(effect_id)
        preset = AudioEffectPreset.query.get(preset_id)
        
        if not effect or not preset:
            return {"success": False, "error": "Effect or preset not found"}
        
        if effect.effect_type != preset.effect_type:
            return {"success": False, "error": "Effect type mismatch"}
        
        effect.parameters = preset.parameters.copy()
        effect.preset_name = preset.name
        effect.preset_id = preset_id
        
        preset.use_count += 1
        
        self.db.session.commit()
        
        return {
            "success": True,
            "effect_id": effect_id,
            "preset_name": preset.name,
            "parameters": effect.parameters
        }
    
    def list_presets(
        self,
        effect_type: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List available presets."""
        from flask_dashboard import AudioEffectPreset
        
        query = AudioEffectPreset.query
        
        if effect_type:
            query = query.filter_by(effect_type=effect_type)
        if category:
            query = query.filter_by(category=category)
        
        presets = query.order_by(AudioEffectPreset.use_count.desc()).all()
        
        return [{
            "id": p.id,
            "name": p.name,
            "effect_type": p.effect_type,
            "category": p.category,
            "description": p.description,
            "is_factory": p.is_factory,
            "use_count": p.use_count
        } for p in presets]
