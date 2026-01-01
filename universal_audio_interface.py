# ============================================================================================
# UNIVERSAL AUDIO GENERATION INTERFACE (Audio UGI)
# ============================================================================================
"""
Complete audio generation pipeline orchestrator.

Handles:
1. Engine routing (ElevenLabs, Suno, Stability Audio, AudioCraft)
2. Audio generation
3. Storage (S3/GCS/Azure/Local)
4. Waveform generation
5. Database integration (AudioAsset creation)
6. Lineage tracking

Similar to the Video UGI but optimized for audio workflows.
"""

import os
import time
import requests
from typing import Dict, Any, Optional
from audio_engines import (
    generate_elevenlabs,
    generate_suno,
    generate_stability_audio,
    generate_audiocraft,
    generate_playht,
    generate_azure_voice,  # Fixed: was generate_azure_neural
    generate_udio,
    generate_riffusion,
    generate_foley
)


class UniversalAudioInterface:
    """Universal interface for audio generation across multiple engines."""
    
    def __init__(self, db, storage_config):
        """Initialize with database and storage configuration.
        
        Args:
            db: SQLAlchemy database instance
            storage_config: Storage configuration (S3, GCS, Azure, Local)
        """
        self.db = db
        self.storage = storage_config
        
        # Engine capabilities
        self.engine_specs = {
            'elevenlabs': {
                'type': 'voiceover',
                'max_duration': 300,  # 5 minutes
                'supports_voices': True,
                'supports_style': True,
                'output_format': 'mp3',
                'sample_rate': 44100
            },
            'playht': {
                'type': 'voiceover',
                'max_duration': 600,  # 10 minutes
                'supports_voices': True,
                'supports_voice_cloning': True,
                'output_format': 'mp3',
                'sample_rate': 44100
            },
            'azure': {
                'type': 'voiceover',
                'max_duration': 600,  # 10 minutes
                'supports_voices': True,
                'supports_styles': True,
                'supports_ssml': True,
                'output_format': 'mp3',
                'sample_rate': 44100
            },
            'suno': {
                'type': 'music',
                'max_duration': 300,  # 5 minutes
                'supports_genre': True,
                'supports_mood': True,
                'supports_bpm': True,
                'supports_key': True,
                'supports_instrumental': True,
                'output_format': 'mp3',
                'sample_rate': 44100
            },
            'udio': {
                'type': 'music',
                'max_duration': 300,  # 5 minutes
                'supports_genre': True,
                'supports_mood': True,
                'supports_style': True,
                'output_format': 'mp3',
                'sample_rate': 44100
            },
            'riffusion': {
                'type': 'music',
                'max_duration': 10,  # Short clips
                'supports_negative_prompt': True,
                'supports_seed': True,
                'realtime': True,
                'output_format': 'wav',
                'sample_rate': 44100
            },
            'stability_audio': {
                'type': 'sfx_ambient',
                'max_duration': 47,
                'supports_negative_prompt': True,
                'output_format': 'mp3',
                'sample_rate': 44100
            },
            'audiocraft': {
                'type': 'music',
                'max_duration': 30,
                'supports_model_selection': True,
                'output_format': 'wav',
                'sample_rate': 32000
            },
            'foley': {
                'type': 'sfx',
                'max_duration': 10,
                'supports_action': True,
                'supports_surface': True,
                'supports_intensity': True,
                'procedural': True,
                'output_format': 'wav',
                'sample_rate': 44100
            }
        }
        
        # Phase 8: Initialize waveform extractor and constellation
        self.waveform_extractor = None
        self.constellation = None
        self.evolution_engine = None
        self.enable_phase8_features = True
    
    def generate(
        self,
        prompt: str,
        engine: str,
        project_id: int,
        user_id: int,
        asset_type: str = "music",
        **settings
    ) -> Dict[str, Any]:
        """Complete audio generation pipeline.
        
        Steps:
        1. Validate engine and settings
        2. Generate audio using selected engine
        3. Store audio in cloud storage
        4. Generate waveform data
        5. Create AudioAsset in database
        6. Return complete result
        
        Args:
            prompt: Text prompt or description
            engine: Generation engine (elevenlabs, suno, stability_audio, audiocraft)
            project_id: AudioProject ID
            user_id: User ID
            asset_type: Type of audio (music, voiceover, sfx, ambient)
            **settings: Engine-specific parameters
        
        Returns:
            Dict with asset_id, audio_url, waveform_url, duration, etc.
        """
        try:
            # Step 1: Validate engine
            if engine not in self.engine_specs:
                return {
                    "success": False,
                    "error": f"Unknown engine: {engine}. Available: {list(self.engine_specs.keys())}"
                }
            
            # Step 2: Route to appropriate engine
            if engine == 'elevenlabs':
                result = generate_elevenlabs(prompt, **settings)
            elif engine == 'playht':
                result = generate_playht(prompt, **settings)
            elif engine == 'azure':
                result = generate_azure_voice(prompt, **settings)
            elif engine == 'suno':
                result = generate_suno(prompt, **settings)
            elif engine == 'udio':
                result = generate_udio(prompt, **settings)
            elif engine == 'riffusion':
                result = generate_riffusion(prompt, **settings)
            elif engine == 'stability_audio':
                result = generate_stability_audio(prompt, **settings)
            elif engine == 'audiocraft':
                result = generate_audiocraft(prompt, **settings)
            elif engine == 'foley':
                result = generate_foley(prompt, **settings)
            else:
                return {"success": False, "error": f"Engine {engine} not implemented"}
            
            if not result.get("success"):
                return result
            
            # Step 3: Store audio (would integrate with cloud storage)
            stored_url = self._store_audio(result["audio_url"], engine, user_id)
            
            # PHASE 8: Step 3.5: Auto-extract waveform and metadata
            if self.enable_phase8_features:
                waveform_metadata = self._extract_audio_metadata(stored_url, asset_type)
                waveform_data = waveform_metadata.get('waveform_data')
                waveform_url = waveform_metadata.get('waveform_url')
            else:
                # Step 4: Generate waveform data (legacy method)
                waveform_data = self._generate_waveform(stored_url, result.get("duration", 10))
                waveform_url = self._store_waveform_image(waveform_data, user_id)
            
            # Step 5: Create AudioAsset in database
            from flask_dashboard import AudioAsset, AudioProject
            
            project = AudioProject.query.get(project_id)
            if not project:
                return {"success": False, "error": "Project not found"}
            
            asset = AudioAsset(
                user_id=user_id,
                team_id=project.team_id,
                project_id=project_id,
                name=f"{asset_type.capitalize()} - {int(time.time())}",
                description=f"Generated from: {prompt[:100]}",
                asset_type=asset_type,
                file_url=stored_url,
                waveform_url=waveform_url,
                duration=result.get("duration", 10.0),
                sample_rate=result.get("sample_rate", 44100),
                channels=2,  # Stereo by default
                prompt=prompt,
                generation_engine=engine,
                generation_params=settings,
                voice_id=result.get("voice_id"),
                tags=f"{asset_type},{engine}",
                category=asset_type,
                mood=settings.get("mood"),
                genre=settings.get("genre"),
                key=settings.get("key"),
                bpm=settings.get("bpm"),
                status="ready",
                waveform_data=waveform_data
            )
            
            self.db.session.add(asset)
            self.db.session.commit()
            
            return {
                "success": True,
                "asset_id": asset.id,
                "audio_url": stored_url,
                "waveform_url": waveform_url,
                "duration": asset.duration,
                "sample_rate": asset.sample_rate,
                "engine": engine,
                "prompt": prompt,
                "created_at": asset.timestamp.isoformat()
            }
        
        except Exception as e:
            self.db.session.rollback()
            return {"success": False, "error": str(e)}
    
    def regenerate(self, asset_id: int, **new_settings) -> Dict[str, Any]:
        """Regenerate audio with same prompt but different settings/seed."""
        from flask_dashboard import AudioAsset
        
        original = AudioAsset.query.get(asset_id)
        if not original:
            return {"success": False, "error": "Asset not found"}
        
        # Merge original settings with new settings
        settings = original.generation_params or {}
        settings.update(new_settings)
        
        return self.generate(
            prompt=original.prompt,
            engine=original.generation_engine,
            project_id=original.project_id,
            user_id=original.user_id,
            asset_type=original.asset_type,
            **settings
        )
    
    def evolve(
        self,
        asset_id: int,
        evolution_type: str,
        **params
    ) -> Dict[str, Any]:
        """Evolve audio (change mood, genre, tempo, style).
        
        Evolution types:
        - mood: Change emotional tone
        - genre: Change musical genre
        - tempo: Change BPM
        - style: Change performance style
        - voice: Change voice (for voiceovers)
        """
        from flask_dashboard import AudioAsset
        
        original = AudioAsset.query.get(asset_id)
        if not original:
            return {"success": False, "error": "Asset not found"}
        
        # Build evolved prompt
        evolved_prompt = original.prompt
        
        if evolution_type == "mood":
            new_mood = params.get("mood", "energetic")
            evolved_prompt += f", {new_mood} mood"
        elif evolution_type == "genre":
            new_genre = params.get("genre", "electronic")
            evolved_prompt += f", {new_genre} genre"
        elif evolution_type == "tempo":
            new_bpm = params.get("bpm", 120)
            evolved_prompt += f", {new_bpm} BPM"
        elif evolution_type == "style":
            new_style = params.get("style", "epic")
            evolved_prompt += f", {new_style} style"
        elif evolution_type == "voice":
            params["voice_id"] = params.get("voice_id")
        
        # Generate evolved audio
        result = self.generate(
            prompt=evolved_prompt,
            engine=original.generation_engine,
            project_id=original.project_id,
            user_id=original.user_id,
            asset_type=original.asset_type,
            **params
        )
        
        # Track lineage if successful
        if result.get("success"):
            from flask_dashboard import AudioLineage
            
            lineage = AudioLineage(
                parent_id=asset_id,
                child_id=result["asset_id"],
                evolution_type=evolution_type,
                original_prompt=original.prompt,
                evolved_prompt=evolved_prompt,
                prompt_delta=f"Evolution: {evolution_type}",
                created_by=original.user_id,
                branch_name=f"{evolution_type}_evolution"
            )
            self.db.session.add(lineage)
            self.db.session.commit()
        
        return result
    
    def extend(
        self,
        asset_id: int,
        extension_type: str = "continue"
    ) -> Dict[str, Any]:
        """Extend audio (add more duration, continue melody).
        
        Extension types:
        - continue: Continue the audio naturally
        - loop: Create a seamless loop
        - variation: Create a variation on the theme
        """
        from flask_dashboard import AudioAsset
        
        original = AudioAsset.query.get(asset_id)
        if not original:
            return {"success": False, "error": "Asset not found"}
        
        # Build extension prompt
        if extension_type == "continue":
            extended_prompt = f"Continue this: {original.prompt}"
        elif extension_type == "loop":
            extended_prompt = f"Create a seamless loop of: {original.prompt}"
        elif extension_type == "variation":
            extended_prompt = f"Create a variation on: {original.prompt}"
        else:
            extended_prompt = original.prompt
        
        return self.generate(
            prompt=extended_prompt,
            engine=original.generation_engine,
            project_id=original.project_id,
            user_id=original.user_id,
            asset_type=original.asset_type,
            duration=original.duration * 1.5  # 50% longer
        )
    
    def _store_audio(self, audio_url: str, engine: str, user_id: int) -> str:
        """Store audio in cloud storage.
        
        In production, this would:
        1. Download audio from generation URL
        2. Upload to S3/GCS/Azure
        3. Return permanent storage URL
        """
        # Placeholder - would integrate with cloud storage
        return audio_url
    
    def _generate_waveform(self, audio_url: str, duration: float) -> list:
        """Generate waveform data for visualization.
        
        Returns array of amplitude values (normalized -1.0 to 1.0).
        """
        # Placeholder - would use librosa or similar to extract waveform
        # For now, generate fake waveform data
        import random
        sample_count = int(duration * 100)  # 100 samples per second
        return [random.uniform(-1.0, 1.0) for _ in range(sample_count)]
    
    def _store_waveform_image(self, waveform_data: list, user_id: int) -> str:
        """Generate and store waveform image.
        
        Would use matplotlib or similar to create waveform visualization.
        """
        # Placeholder
        return f"https://storage.example.com/waveforms/user_{user_id}_{int(time.time())}.png"
    
    def get_engine_capabilities(self, engine: str) -> Dict[str, Any]:
        """Get capabilities for a specific engine."""
        return self.engine_specs.get(engine, {})
    
    def list_engines(self) -> Dict[str, Dict[str, Any]]:
        """List all available engines with their capabilities."""
        return self.engine_specs    
    # ========== PHASE 8: AUTO-WAVEFORM EXTRACTION ==========
    
    def _extract_audio_metadata(self, audio_url: str, audio_type: str) -> Dict[str, Any]:
        """Auto-extract waveform and metadata using Phase 8 waveform extractor.
        
        Args:
            audio_url: URL of generated audio
            audio_type: Type of audio (music, voice, sfx, ambient)
        
        Returns:
            Dict with waveform_data, waveform_url, duration, loudness, tags, etc.
        """
        try:
            # Lazy load waveform extractor
            if self.waveform_extractor is None:
                from audio_waveform_extractor import AudioWaveformExtractor
                self.waveform_extractor = AudioWaveformExtractor()
            
            # Extract all metadata
            metadata = self.waveform_extractor.extract_all(
                audio_url=audio_url,
                audio_type=audio_type,
                generate_waveform=True
            )
            
            return metadata
        
        except Exception as e:
            print(f"⚠️ Waveform extraction failed: {e}")
            # Fallback to legacy method
            return {
                'waveform_data': self._generate_waveform(audio_url, 10.0),
                'waveform_url': None,
                'duration': 10.0
            }
    
    # ========== PHASE 8: CONSTELLATION INTEGRATION ==========
    
    def _add_to_constellation(self, asset_id: int) -> bool:
        """Auto-add asset to constellation clusters.
        
        Args:
            asset_id: AudioAsset ID
        
        Returns:
            Success status
        """
        try:
            # Lazy load constellation integration
            if self.constellation is None:
                from audio_constellation_integration import AudioConstellationIntegration
                self.constellation = AudioConstellationIntegration(self.db)
            
            # Auto-assign to clusters
            result = self.constellation.auto_assign_cluster(asset_id)
            
            return result.get('success', False)
        
        except Exception as e:
            print(f"⚠️ Constellation integration failed: {e}")
            return False
    
    # ========== PHASE 8: EVOLUTION INTEGRATION ==========
    
    def evolve_audio(
        self,
        asset_id: int,
        evolution_type: str = "refine",
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Evolve audio using Phase 8 evolution engine.
        
        Args:
            asset_id: Source asset ID
            evolution_type: Evolution type (refine, enhance, cleanup, etc.)
            parameters: Evolution parameters
        
        Returns:
            Dict with evolved asset info
        """
        try:
            # Lazy load evolution engine
            if self.evolution_engine is None:
                from audio_evolution_engine import AudioEvolutionEngine
                self.evolution_engine = AudioEvolutionEngine(self.db)
            
            # Perform evolution
            result = self.evolution_engine.evolve(
                asset_id=asset_id,
                evolution_type=evolution_type,
                parameters=parameters
            )
            
            # If successful, add evolved asset to constellation
            if result.get('success') and result.get('evolved_asset_id'):
                self._add_to_constellation(result['evolved_asset_id'])
            
            return result
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def extend_audio(
        self,
        asset_id: int,
        extension_duration: float = 30.0,
        extension_type: str = "continue",
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Extend audio using Phase 8 evolution engine.
        
        Args:
            asset_id: Source asset ID
            extension_duration: Duration to add (seconds)
            extension_type: Extension type (continue, loop, variation, etc.)
            parameters: Extension parameters
        
        Returns:
            Dict with extended asset info
        """
        try:
            if self.evolution_engine is None:
                from audio_evolution_engine import AudioEvolutionEngine
                self.evolution_engine = AudioEvolutionEngine(self.db)
            
            result = self.evolution_engine.extend(
                asset_id=asset_id,
                extension_duration=extension_duration,
                extension_type=extension_type,
                parameters=parameters
            )
            
            if result.get('success') and result.get('extended_asset_id'):
                self._add_to_constellation(result['extended_asset_id'])
            
            return result
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def regenerate_audio(
        self,
        asset_id: int,
        variation_style: str = "alternate",
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Regenerate audio with alternate take using Phase 8 evolution engine.
        
        Args:
            asset_id: Source asset ID
            variation_style: Variation style (alternate, different, similar, etc.)
            parameters: Regeneration parameters
        
        Returns:
            Dict with alternate asset info
        """
        try:
            if self.evolution_engine is None:
                from audio_evolution_engine import AudioEvolutionEngine
                self.evolution_engine = AudioEvolutionEngine(self.db)
            
            result = self.evolution_engine.regenerate(
                asset_id=asset_id,
                variation_style=variation_style,
                parameters=parameters
            )
            
            if result.get('success') and result.get('alternate_asset_id'):
                self._add_to_constellation(result['alternate_asset_id'])
            
            return result
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def mutate_audio(
        self,
        asset_id: int,
        mutation_type: str = "experimental",
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create experimental mutation using Phase 8 evolution engine.
        
        Args:
            asset_id: Source asset ID
            mutation_type: Mutation type (experimental, genre_shift, style_change, etc.)
            parameters: Mutation parameters
        
        Returns:
            Dict with mutated asset info
        """
        try:
            if self.evolution_engine is None:
                from audio_evolution_engine import AudioEvolutionEngine
                self.evolution_engine = AudioEvolutionEngine(self.db)
            
            result = self.evolution_engine.mutate(
                asset_id=asset_id,
                mutation_type=mutation_type,
                parameters=parameters
            )
            
            if result.get('success') and result.get('mutated_asset_id'):
                self._add_to_constellation(result['mutated_asset_id'])
            
            return result
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ========== PHASE 8: ENHANCED GENERATION WITH AUTO-CONSTELLATION ==========
    
    def generate_audio(
        self,
        prompt: str,
        engine: str = "suno",
        audio_type: str = "music",
        auto_constellation: bool = True,
        **settings
    ) -> Dict[str, Any]:
        """Simplified generation method with Phase 8 auto-constellation.
        
        This is the primary method for API route usage.
        
        Args:
            prompt: Text prompt or description
            engine: Generation engine
            audio_type: Type of audio (music, voiceover, sfx, ambient)
            auto_constellation: Automatically add to constellation (default True)
            **settings: Engine-specific parameters
        
        Returns:
            Dict with audio_url, duration, waveform_url, etc.
        """
        try:
            # Route to appropriate engine
            if engine == 'elevenlabs':
                result = generate_elevenlabs(prompt, **settings)
            elif engine == 'playht':
                result = generate_playht(prompt, **settings)
            elif engine == 'azure':
                result = generate_azure_voice(prompt, **settings)
            elif engine == 'suno':
                result = generate_suno(prompt, **settings)
            elif engine == 'udio':
                result = generate_udio(prompt, **settings)
            elif engine == 'riffusion':
                result = generate_riffusion(prompt, **settings)
            elif engine == 'stability_audio' or engine == 'stability':
                result = generate_stability_audio(prompt, **settings)
            elif engine == 'audiocraft':
                result = generate_audiocraft(prompt, **settings)
            elif engine == 'foley':
                result = generate_foley(prompt, **settings)
            else:
                return {"success": False, "error": f"Unknown engine: {engine}"}
            
            if not result.get("success"):
                return result
            
            # Phase 8: Auto-extract metadata if enabled
            if self.enable_phase8_features:
                metadata = self._extract_audio_metadata(result["audio_url"], audio_type)
                result.update(metadata)
            
            return result
        
        except Exception as e:
            return {"success": False, "error": str(e)}