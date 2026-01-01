# ============================================================================================
# AUDIO EVOLUTION ENGINE - Evolve, Extend, Regenerate, Mutate
# ============================================================================================
"""
Audio evolution system for iterative refinement and variation.

Operations:
- **Evolve**: Refine/improve the audio (better quality, clarity, mixing)
- **Extend**: Continue the audio (longer duration, seamless continuation)
- **Regenerate**: Create alternate takes (different interpretation, same prompt)
- **Mutate**: Experimental variations (genre shift, style change, remixing)

Features:
- Lineage tracking (parent-child relationships)
- Generation history
- Prompt evolution
- Parameter tracking
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import json


class AudioEvolutionEngine:
    """Manage audio evolution, extension, and variation."""
    
    def __init__(self, db):
        """Initialize evolution engine with database."""
        self.db = db
    
    # ========== EVOLVE (REFINE) ==========
    
    def evolve(
        self,
        asset_id: int,
        evolution_type: str = "refine",  # refine, enhance, cleanup
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Evolve audio to improve quality or characteristics.
        
        Args:
            asset_id: Source audio asset ID
            evolution_type: Type of evolution (refine, enhance, cleanup)
            parameters: Evolution parameters
        
        Returns:
            Dict with new asset info and evolution metadata
        """
        from flask_dashboard import AudioAsset, AudioLineage
        
        try:
            # Get source asset
            source_asset = AudioAsset.query.get(asset_id)
            if not source_asset:
                return {"success": False, "error": "Asset not found"}
            
            # Build evolution prompt
            evolution_prompt = self._build_evolution_prompt(
                source_asset,
                evolution_type,
                parameters
            )
            
            # Generate evolved audio using appropriate engine
            from universal_audio_interface import UniversalAudioInterface
            audio_ugi = UniversalAudioInterface()
            
            result = audio_ugi.generate_audio(
                prompt=evolution_prompt,
                engine=source_asset.engine,
                audio_type=source_asset.asset_type,
                **parameters or {}
            )
            
            if not result.get("success"):
                return result
            
            # Create new asset for evolved audio
            evolved_asset = AudioAsset(
                project_id=source_asset.project_id,
                name=f"{source_asset.name} (Evolved)",
                asset_type=source_asset.asset_type,
                audio_url=result["audio_url"],
                waveform_url=result.get("waveform_url"),
                duration=result.get("duration"),
                sample_rate=result.get("sample_rate"),
                loudness_lufs=result.get("loudness_lufs"),
                engine=source_asset.engine,
                prompt=evolution_prompt,
                generation_params=json.dumps(parameters or {}),
                status="ready"
            )
            
            self.db.session.add(evolved_asset)
            self.db.session.flush()
            
            # Create lineage record
            lineage = AudioLineage(
                parent_asset_id=asset_id,
                child_asset_id=evolved_asset.id,
                relationship_type="evolution",
                evolution_method=evolution_type,
                generation_number=source_asset.generation_number + 1
            )
            
            self.db.session.add(lineage)
            evolved_asset.generation_number = lineage.generation_number
            
            self.db.session.commit()
            
            return {
                "success": True,
                "evolved_asset_id": evolved_asset.id,
                "audio_url": evolved_asset.audio_url,
                "evolution_type": evolution_type,
                "generation_number": evolved_asset.generation_number,
                "lineage_id": lineage.id
            }
        
        except Exception as e:
            self.db.session.rollback()
            return {"success": False, "error": str(e)}
    
    def _build_evolution_prompt(
        self,
        source_asset: Any,
        evolution_type: str,
        parameters: Optional[Dict[str, Any]]
    ) -> str:
        """Build prompt for audio evolution.
        
        Args:
            source_asset: Source AudioAsset object
            evolution_type: Evolution type
            parameters: Evolution parameters
        
        Returns:
            Enhanced prompt string
        """
        base_prompt = source_asset.prompt or "audio"
        
        evolution_instructions = {
            "refine": "Improve the quality and clarity of this audio",
            "enhance": "Enhance the production quality and richness",
            "cleanup": "Remove noise and artifacts, clean up the audio",
            "polish": "Add professional polish and finishing touches",
            "remaster": "Remaster for optimal loudness and balance"
        }
        
        instruction = evolution_instructions.get(evolution_type, "Refine this audio")
        
        # Combine with original prompt
        evolved_prompt = f"{instruction}: {base_prompt}"
        
        # Add parameter-specific instructions
        if parameters:
            if parameters.get("target_loudness"):
                evolved_prompt += f", target loudness: {parameters['target_loudness']} LUFS"
            if parameters.get("enhance_bass"):
                evolved_prompt += ", enhance bass frequencies"
            if parameters.get("brighten"):
                evolved_prompt += ", brighten high frequencies"
        
        return evolved_prompt
    
    # ========== EXTEND (CONTINUE) ==========
    
    def extend(
        self,
        asset_id: int,
        extension_duration: float = 30.0,
        extension_type: str = "continue",  # continue, loop, variation
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Extend audio duration by continuing or looping.
        
        Args:
            asset_id: Source audio asset ID
            extension_duration: Additional duration in seconds
            extension_type: How to extend (continue, loop, variation)
            parameters: Extension parameters
        
        Returns:
            Dict with new extended asset info
        """
        from flask_dashboard import AudioAsset, AudioLineage
        
        try:
            # Get source asset
            source_asset = AudioAsset.query.get(asset_id)
            if not source_asset:
                return {"success": False, "error": "Asset not found"}
            
            # Build extension prompt
            extension_prompt = self._build_extension_prompt(
                source_asset,
                extension_type,
                extension_duration,
                parameters
            )
            
            # Generate extended audio
            from universal_audio_interface import UniversalAudioInterface
            audio_ugi = UniversalAudioInterface()
            
            result = audio_ugi.generate_audio(
                prompt=extension_prompt,
                engine=source_asset.engine,
                audio_type=source_asset.asset_type,
                duration=extension_duration,
                **parameters or {}
            )
            
            if not result.get("success"):
                return result
            
            # Create new asset for extended audio
            extended_asset = AudioAsset(
                project_id=source_asset.project_id,
                name=f"{source_asset.name} (Extended)",
                asset_type=source_asset.asset_type,
                audio_url=result["audio_url"],
                waveform_url=result.get("waveform_url"),
                duration=(source_asset.duration or 0) + extension_duration,
                sample_rate=result.get("sample_rate"),
                loudness_lufs=result.get("loudness_lufs"),
                engine=source_asset.engine,
                prompt=extension_prompt,
                generation_params=json.dumps(parameters or {}),
                status="ready"
            )
            
            self.db.session.add(extended_asset)
            self.db.session.flush()
            
            # Create lineage record
            lineage = AudioLineage(
                parent_asset_id=asset_id,
                child_asset_id=extended_asset.id,
                relationship_type="extension",
                evolution_method=extension_type,
                generation_number=source_asset.generation_number + 1
            )
            
            self.db.session.add(lineage)
            extended_asset.generation_number = lineage.generation_number
            
            self.db.session.commit()
            
            return {
                "success": True,
                "extended_asset_id": extended_asset.id,
                "audio_url": extended_asset.audio_url,
                "extension_type": extension_type,
                "total_duration": extended_asset.duration,
                "lineage_id": lineage.id
            }
        
        except Exception as e:
            self.db.session.rollback()
            return {"success": False, "error": str(e)}
    
    def _build_extension_prompt(
        self,
        source_asset: Any,
        extension_type: str,
        duration: float,
        parameters: Optional[Dict[str, Any]]
    ) -> str:
        """Build prompt for audio extension.
        
        Args:
            source_asset: Source AudioAsset object
            extension_type: Extension type
            duration: Extension duration
            parameters: Extension parameters
        
        Returns:
            Extension prompt string
        """
        base_prompt = source_asset.prompt or "audio"
        
        extension_instructions = {
            "continue": f"Continue this audio seamlessly for {duration} more seconds",
            "loop": f"Create a {duration} second looping variation of this audio",
            "variation": f"Create a {duration} second thematic variation",
            "outro": f"Create a {duration} second outro/ending for this audio",
            "bridge": f"Create a {duration} second bridge section"
        }
        
        instruction = extension_instructions.get(extension_type, f"Extend this audio by {duration} seconds")
        
        extended_prompt = f"{instruction}: {base_prompt}"
        
        # Add parameters
        if parameters:
            if parameters.get("fade_out"):
                extended_prompt += ", fade out at the end"
            if parameters.get("build_intensity"):
                extended_prompt += ", gradually build intensity"
        
        return extended_prompt
    
    # ========== REGENERATE (ALTERNATE TAKES) ==========
    
    def regenerate(
        self,
        asset_id: int,
        variation_style: str = "alternate",  # alternate, different, similar
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Regenerate audio with alternate interpretation.
        
        Args:
            asset_id: Source audio asset ID
            variation_style: How different the alternate should be
            parameters: Regeneration parameters
        
        Returns:
            Dict with new alternate asset info
        """
        from flask_dashboard import AudioAsset, AudioLineage
        
        try:
            # Get source asset
            source_asset = AudioAsset.query.get(asset_id)
            if not source_asset:
                return {"success": False, "error": "Asset not found"}
            
            # Use original prompt with variation
            regenerate_prompt = self._build_regenerate_prompt(
                source_asset,
                variation_style,
                parameters
            )
            
            # Generate alternate version
            from universal_audio_interface import UniversalAudioInterface
            audio_ugi = UniversalAudioInterface()
            
            result = audio_ugi.generate_audio(
                prompt=regenerate_prompt,
                engine=source_asset.engine,
                audio_type=source_asset.asset_type,
                **parameters or {}
            )
            
            if not result.get("success"):
                return result
            
            # Create new asset for alternate
            alternate_asset = AudioAsset(
                project_id=source_asset.project_id,
                name=f"{source_asset.name} (Take {source_asset.generation_number + 1})",
                asset_type=source_asset.asset_type,
                audio_url=result["audio_url"],
                waveform_url=result.get("waveform_url"),
                duration=result.get("duration"),
                sample_rate=result.get("sample_rate"),
                loudness_lufs=result.get("loudness_lufs"),
                engine=source_asset.engine,
                prompt=regenerate_prompt,
                generation_params=json.dumps(parameters or {}),
                status="ready"
            )
            
            self.db.session.add(alternate_asset)
            self.db.session.flush()
            
            # Create lineage record
            lineage = AudioLineage(
                parent_asset_id=asset_id,
                child_asset_id=alternate_asset.id,
                relationship_type="regeneration",
                evolution_method=variation_style,
                generation_number=source_asset.generation_number + 1
            )
            
            self.db.session.add(lineage)
            alternate_asset.generation_number = lineage.generation_number
            
            self.db.session.commit()
            
            return {
                "success": True,
                "alternate_asset_id": alternate_asset.id,
                "audio_url": alternate_asset.audio_url,
                "variation_style": variation_style,
                "take_number": alternate_asset.generation_number,
                "lineage_id": lineage.id
            }
        
        except Exception as e:
            self.db.session.rollback()
            return {"success": False, "error": str(e)}
    
    def _build_regenerate_prompt(
        self,
        source_asset: Any,
        variation_style: str,
        parameters: Optional[Dict[str, Any]]
    ) -> str:
        """Build prompt for regeneration.
        
        Args:
            source_asset: Source AudioAsset object
            variation_style: Variation style
            parameters: Regeneration parameters
        
        Returns:
            Regeneration prompt string
        """
        base_prompt = source_asset.prompt or "audio"
        
        variation_modifiers = {
            "alternate": "Create an alternate version of",
            "different": "Create a different interpretation of",
            "similar": "Create a similar but distinct version of",
            "remix": "Create a remixed version of",
            "reinterpret": "Reinterpret"
        }
        
        modifier = variation_modifiers.get(variation_style, "Regenerate")
        
        regenerate_prompt = f"{modifier}: {base_prompt}"
        
        # Add variation parameters
        if parameters:
            if parameters.get("change_tempo"):
                regenerate_prompt += f", change tempo to {parameters['change_tempo']} BPM"
            if parameters.get("change_key"):
                regenerate_prompt += f", transpose to {parameters['change_key']} key"
            if parameters.get("different_instruments"):
                regenerate_prompt += ", use different instrumentation"
        
        return regenerate_prompt
    
    # ========== MUTATE (EXPERIMENTAL) ==========
    
    def mutate(
        self,
        asset_id: int,
        mutation_type: str = "experimental",  # experimental, genre_shift, style_change
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create experimental mutation of audio.
        
        Args:
            asset_id: Source audio asset ID
            mutation_type: Type of mutation
            parameters: Mutation parameters (genre, style, effects, etc.)
        
        Returns:
            Dict with new mutated asset info
        """
        from flask_dashboard import AudioAsset, AudioLineage
        
        try:
            # Get source asset
            source_asset = AudioAsset.query.get(asset_id)
            if not source_asset:
                return {"success": False, "error": "Asset not found"}
            
            # Build mutation prompt
            mutation_prompt = self._build_mutation_prompt(
                source_asset,
                mutation_type,
                parameters
            )
            
            # Generate mutated audio
            from universal_audio_interface import UniversalAudioInterface
            audio_ugi = UniversalAudioInterface()
            
            result = audio_ugi.generate_audio(
                prompt=mutation_prompt,
                engine=source_asset.engine,
                audio_type=source_asset.asset_type,
                **parameters or {}
            )
            
            if not result.get("success"):
                return result
            
            # Create new asset for mutated audio
            mutated_asset = AudioAsset(
                project_id=source_asset.project_id,
                name=f"{source_asset.name} (Mutated)",
                asset_type=source_asset.asset_type,
                audio_url=result["audio_url"],
                waveform_url=result.get("waveform_url"),
                duration=result.get("duration"),
                sample_rate=result.get("sample_rate"),
                loudness_lufs=result.get("loudness_lufs"),
                engine=source_asset.engine,
                prompt=mutation_prompt,
                generation_params=json.dumps(parameters or {}),
                status="ready"
            )
            
            self.db.session.add(mutated_asset)
            self.db.session.flush()
            
            # Create lineage record
            lineage = AudioLineage(
                parent_asset_id=asset_id,
                child_asset_id=mutated_asset.id,
                relationship_type="mutation",
                evolution_method=mutation_type,
                generation_number=source_asset.generation_number + 1
            )
            
            self.db.session.add(lineage)
            mutated_asset.generation_number = lineage.generation_number
            
            self.db.session.commit()
            
            return {
                "success": True,
                "mutated_asset_id": mutated_asset.id,
                "audio_url": mutated_asset.audio_url,
                "mutation_type": mutation_type,
                "generation_number": mutated_asset.generation_number,
                "lineage_id": lineage.id
            }
        
        except Exception as e:
            self.db.session.rollback()
            return {"success": False, "error": str(e)}
    
    def _build_mutation_prompt(
        self,
        source_asset: Any,
        mutation_type: str,
        parameters: Optional[Dict[str, Any]]
    ) -> str:
        """Build prompt for audio mutation.
        
        Args:
            source_asset: Source AudioAsset object
            mutation_type: Mutation type
            parameters: Mutation parameters
        
        Returns:
            Mutation prompt string
        """
        base_prompt = source_asset.prompt or "audio"
        
        mutation_instructions = {
            "experimental": "Create an experimental variation of",
            "genre_shift": "Transform into a different genre",
            "style_change": "Completely change the style of",
            "deconstruct": "Deconstruct and reimagine",
            "fusion": "Create a fusion/hybrid version of"
        }
        
        instruction = mutation_instructions.get(mutation_type, "Create a mutation of")
        
        mutated_prompt = f"{instruction}: {base_prompt}"
        
        # Add mutation parameters
        if parameters:
            if parameters.get("target_genre"):
                mutated_prompt += f", transform to {parameters['target_genre']} genre"
            if parameters.get("target_style"):
                mutated_prompt += f", apply {parameters['target_style']} style"
            if parameters.get("add_effects"):
                mutated_prompt += f", add {', '.join(parameters['add_effects'])} effects"
            if parameters.get("tempo_multiplier"):
                mutated_prompt += f", multiply tempo by {parameters['tempo_multiplier']}x"
        
        return mutated_prompt
    
    # ========== LINEAGE QUERIES ==========
    
    def get_lineage_tree(self, asset_id: int) -> Dict[str, Any]:
        """Get complete lineage tree for an asset.
        
        Args:
            asset_id: Asset ID to get lineage for
        
        Returns:
            Lineage tree structure
        """
        from flask_dashboard import AudioLineage, AudioAsset
        
        try:
            # Get asset
            asset = AudioAsset.query.get(asset_id)
            if not asset:
                return {"success": False, "error": "Asset not found"}
            
            # Get all ancestors
            ancestors = self._get_ancestors(asset_id)
            
            # Get all descendants
            descendants = self._get_descendants(asset_id)
            
            return {
                "success": True,
                "asset_id": asset_id,
                "asset_name": asset.name,
                "generation_number": asset.generation_number,
                "ancestors": ancestors,
                "descendants": descendants
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _get_ancestors(self, asset_id: int, depth: int = 0) -> List[Dict[str, Any]]:
        """Recursively get all ancestors of an asset."""
        from flask_dashboard import AudioLineage, AudioAsset
        
        if depth > 10:  # Prevent infinite recursion
            return []
        
        lineages = AudioLineage.query.filter_by(child_asset_id=asset_id).all()
        
        ancestors = []
        for lineage in lineages:
            parent = AudioAsset.query.get(lineage.parent_asset_id)
            if parent:
                ancestor_data = {
                    "asset_id": parent.id,
                    "name": parent.name,
                    "relationship": lineage.relationship_type,
                    "method": lineage.evolution_method,
                    "generation": parent.generation_number
                }
                
                # Recursively get parent's ancestors
                ancestor_data["parents"] = self._get_ancestors(parent.id, depth + 1)
                
                ancestors.append(ancestor_data)
        
        return ancestors
    
    def _get_descendants(self, asset_id: int, depth: int = 0) -> List[Dict[str, Any]]:
        """Recursively get all descendants of an asset."""
        from flask_dashboard import AudioLineage, AudioAsset
        
        if depth > 10:  # Prevent infinite recursion
            return []
        
        lineages = AudioLineage.query.filter_by(parent_asset_id=asset_id).all()
        
        descendants = []
        for lineage in lineages:
            child = AudioAsset.query.get(lineage.child_asset_id)
            if child:
                descendant_data = {
                    "asset_id": child.id,
                    "name": child.name,
                    "relationship": lineage.relationship_type,
                    "method": lineage.evolution_method,
                    "generation": child.generation_number
                }
                
                # Recursively get child's descendants
                descendant_data["children"] = self._get_descendants(child.id, depth + 1)
                
                descendants.append(descendant_data)
        
        return descendants
    
    def get_evolution_history(self, asset_id: int) -> List[Dict[str, Any]]:
        """Get evolution history for an asset (linear path from root to this asset).
        
        Args:
            asset_id: Asset ID
        
        Returns:
            List of evolution steps
        """
        from flask_dashboard import AudioLineage, AudioAsset
        
        try:
            history = []
            current_id = asset_id
            
            # Walk back through ancestors
            while current_id:
                lineage = AudioLineage.query.filter_by(child_asset_id=current_id).first()
                
                if not lineage:
                    break
                
                parent = AudioAsset.query.get(lineage.parent_asset_id)
                if parent:
                    history.insert(0, {
                        "asset_id": parent.id,
                        "name": parent.name,
                        "relationship": lineage.relationship_type,
                        "method": lineage.evolution_method,
                        "generation": parent.generation_number
                    })
                
                current_id = lineage.parent_asset_id
            
            return history
        
        except Exception as e:
            print(f"❌ Evolution history error: {e}")
            return []
