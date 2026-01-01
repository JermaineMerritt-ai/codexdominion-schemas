"""
🎨 Graphics Evolution Engine - Image Refinement & Variation System
===================================================================

Advanced evolution system for AI-generated images:
- Evolve: Refine and enhance existing images
- Transform: Apply style transfer and transformations
- Remix: Blend multiple prompts and styles
- Mutate: Experimental variations and modifications

Similar to Audio Studio Phase 8's evolution system but for images.

Usage:
------
from graphics_evolution_engine import GraphicsEvolutionEngine
from db import SessionLocal

engine = GraphicsEvolutionEngine()

# Evolve an image (refinement)
evolved = engine.evolve(
    asset_id="img_123",
    evolution_type="enhance",
    parameters={"quality_boost": 0.8, "detail_level": "high"}
)

# Transform with style transfer
transformed = engine.transform(
    asset_id="img_123",
    target_style="impressionist",
    intensity=0.7
)

# Remix multiple prompts
remix = engine.remix(
    asset_ids=["img_123", "img_456"],
    blend_mode="interpolate",
    weights=[0.6, 0.4]
)

# Get complete lineage tree
lineage = engine.get_lineage_tree("img_123")
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from db import SessionLocal
from models import GraphicsProject, PromptHistory


class GraphicsEvolutionEngine:
    """
    Image evolution system with lineage tracking
    
    Mirrors Audio Studio Phase 8's evolution capabilities:
    - Multiple evolution operations (evolve, transform, remix, mutate)
    - Complete lineage tracking (ancestors + descendants)
    - Automatic prompt enhancement
    - Style transfer and blending
    """
    
    def __init__(self, session=None):
        self.session = session or SessionLocal()
        
        # Evolution operation types
        self.evolution_types = {
            "refine": "Improve overall quality and clarity",
            "enhance": "Enhance details and sharpness",
            "upscale": "Increase resolution while maintaining quality",
            "cleanup": "Remove artifacts and improve smoothness",
            "polish": "Final professional touches",
            "remaster": "Complete quality overhaul"
        }
        
        # Transform types (style transfer)
        self.transform_types = {
            "impressionist": "Van Gogh-style impressionist painting",
            "photorealistic": "Convert to photorealistic style",
            "anime": "Transform to anime/manga aesthetic",
            "oil_painting": "Oil painting on canvas texture",
            "watercolor": "Soft watercolor painting",
            "sketch": "Pencil sketch or line art",
            "cyberpunk": "Futuristic cyberpunk aesthetic",
            "fantasy": "Epic fantasy art style",
            "minimalist": "Clean minimalist design",
            "vintage": "Retro vintage photograph"
        }
    
    def evolve(
        self,
        asset_id: str,
        evolution_type: str = "enhance",
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Evolve image to improve quality/clarity
        
        Evolution types:
        - refine: General quality improvement
        - enhance: Sharpen details
        - upscale: Increase resolution
        - cleanup: Remove artifacts
        - polish: Professional finishing
        - remaster: Complete remake
        
        Args:
            asset_id: ID of image to evolve
            evolution_type: Type of evolution (see evolution_types dict)
            parameters: Additional parameters:
                - quality_boost: 0.0-1.0 (how much to improve)
                - detail_level: "low", "medium", "high"
                - preserve_style: True/False (maintain original style)
        
        Returns:
            {
                "evolved_asset_id": "img_789",
                "original_asset_id": "img_123",
                "evolution_type": "enhance",
                "generation": 2,
                "lineage_id": "lineage_xyz",
                "image_url": "https://...",
                "prompt": "Enhanced prompt"
            }
        """
        # Get original asset
        original_project = self.session.query(GraphicsProject).filter_by(id=asset_id).first()
        
        if not original_project:
            raise ValueError(f"Asset {asset_id} not found")
        
        # Build evolved prompt
        params = parameters or {}
        quality_boost = params.get("quality_boost", 0.7)
        detail_level = params.get("detail_level", "high")
        preserve_style = params.get("preserve_style", True)
        
        evolution_desc = self.evolution_types.get(evolution_type, "Improve the image")
        
        evolved_prompt = f"{evolution_desc}: {original_project.prompt}"
        
        if quality_boost > 0.5:
            evolved_prompt += f", {detail_level} detail level"
        
        if preserve_style:
            if original_project.mood:
                evolved_prompt += f", maintain {original_project.mood} mood"
            if original_project.color_palette:
                evolved_prompt += f", preserve {original_project.color_palette} color palette"
        
        # Generate evolved image (placeholder - would call graphics_engines.py)
        # In production, this would use the same engine as original
        from graphics_engines import UniversalGraphicsInterface
        graphics = UniversalGraphicsInterface()
        
        # Determine which engine to use
        engine_hint = "auto"
        if original_project.prompt_source == "midjourney":
            engine_hint = "midjourney"
        elif original_project.prompt_source == "dall-e":
            engine_hint = "dall-e"
        elif original_project.prompt_source == "stable-diffusion":
            engine_hint = "stable-diffusion"
        
        try:
            result = graphics.generate(evolved_prompt, engine=engine_hint)
            image_url = result.get("image_url")
        except:
            # Fallback placeholder
            image_url = "https://via.placeholder.com/1024x1024/4F46E5/FFFFFF?text=Evolved+Image"
        
        # Create new GraphicsProject for evolved image
        evolved_project = GraphicsProject(
            prompt=evolved_prompt,
            aspect_ratio=original_project.aspect_ratio,
            color_palette=original_project.color_palette,
            mood=original_project.mood,
            lighting=original_project.lighting,
            camera_angle=original_project.camera_angle,
            thumbnail_url=image_url,
            tags=original_project.tags,
            category=original_project.category,
            user_id=original_project.user_id,
            team_id=original_project.team_id,
            original_prompt=original_project.original_prompt or original_project.prompt,
            prompt_version=(original_project.prompt_version or 1) + 1,
            parent_project_id=original_project.id,
            prompt_source="evolved"
        )
        
        self.session.add(evolved_project)
        self.session.commit()
        
        # Update PromptHistory if exists
        if original_project.parent_prompt_id:
            parent_prompt = self.session.query(PromptHistory).get(original_project.parent_prompt_id)
            if parent_prompt:
                # Create evolved prompt history entry
                evolved_prompt_history = PromptHistory(
                    prompt_text=evolved_prompt,
                    team_id=original_project.team_id,
                    created_by=original_project.user_id,
                    parent_id=parent_prompt.id,
                    generation=parent_prompt.generation + 1,
                    evolution_reason=evolution_type,
                    mood=evolved_project.mood,
                    color_palette=evolved_project.color_palette,
                    tags=evolved_project.tags,
                    category=evolved_project.category,
                    is_evolved=True
                )
                self.session.add(evolved_prompt_history)
                self.session.commit()
                
                evolved_project.parent_prompt_id = evolved_prompt_history.id
                self.session.commit()
        
        return {
            "evolved_asset_id": str(evolved_project.id),
            "original_asset_id": asset_id,
            "evolution_type": evolution_type,
            "generation": evolved_project.prompt_version,
            "lineage_id": str(evolved_project.parent_prompt_id) if evolved_project.parent_prompt_id else None,
            "image_url": image_url,
            "prompt": evolved_prompt,
            "created_at": evolved_project.timestamp.isoformat() + "Z"
        }
    
    def transform(
        self,
        asset_id: str,
        target_style: str,
        intensity: float = 0.7,
        preserve_content: bool = True
    ) -> Dict[str, Any]:
        """
        Transform image to different style (style transfer)
        
        Transform types:
        - impressionist, photorealistic, anime, oil_painting, watercolor
        - sketch, cyberpunk, fantasy, minimalist, vintage
        
        Args:
            asset_id: ID of image to transform
            target_style: Target style (see transform_types dict)
            intensity: Transformation intensity (0.0-1.0)
            preserve_content: Keep original content/composition
        
        Returns:
            Transformed image data (same format as evolve())
        """
        # Get original asset
        original_project = self.session.query(GraphicsProject).filter_by(id=asset_id).first()
        
        if not original_project:
            raise ValueError(f"Asset {asset_id} not found")
        
        # Build transformation prompt
        style_desc = self.transform_types.get(target_style, target_style)
        
        if preserve_content:
            transform_prompt = f"Transform this image to {style_desc} style: {original_project.prompt}"
        else:
            transform_prompt = f"Reimagine in {style_desc} style: {original_project.prompt}"
        
        if intensity > 0.8:
            transform_prompt += ", dramatic transformation"
        elif intensity < 0.3:
            transform_prompt += ", subtle style hints"
        
        # Generate transformed image
        from graphics_engines import UniversalGraphicsInterface
        graphics = UniversalGraphicsInterface()
        
        try:
            # Use Stable Diffusion img2img for style transfer if available
            result = graphics.generate(transform_prompt, engine="stable-diffusion")
            image_url = result.get("image_url")
        except:
            image_url = "https://via.placeholder.com/1024x1024/8B5CF6/FFFFFF?text=Transformed+Image"
        
        # Create transformed project
        transformed_project = GraphicsProject(
            prompt=transform_prompt,
            aspect_ratio=original_project.aspect_ratio,
            color_palette=target_style if target_style in ["vintage", "cyberpunk", "fantasy"] else original_project.color_palette,
            mood=original_project.mood,
            lighting=original_project.lighting,
            camera_angle=original_project.camera_angle,
            thumbnail_url=image_url,
            tags=f"{original_project.tags},{target_style}" if original_project.tags else target_style,
            category=original_project.category,
            user_id=original_project.user_id,
            team_id=original_project.team_id,
            original_prompt=original_project.original_prompt or original_project.prompt,
            prompt_version=(original_project.prompt_version or 1) + 1,
            parent_project_id=original_project.id,
            prompt_source="transformed"
        )
        
        self.session.add(transformed_project)
        self.session.commit()
        
        return {
            "transformed_asset_id": str(transformed_project.id),
            "original_asset_id": asset_id,
            "target_style": target_style,
            "intensity": intensity,
            "generation": transformed_project.prompt_version,
            "image_url": image_url,
            "prompt": transform_prompt,
            "created_at": transformed_project.timestamp.isoformat() + "Z"
        }
    
    def remix(
        self,
        asset_ids: List[str],
        blend_mode: str = "interpolate",
        weights: Optional[List[float]] = None,
        style: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Remix multiple images into one (multi-prompt blending)
        
        Blend modes:
        - interpolate: Smooth blend between images
        - combine: Merge distinct elements
        - hybrid: Fusion of concepts
        - collage: Artistic combination
        
        Args:
            asset_ids: List of 2-4 image IDs to remix
            blend_mode: How to blend (see above)
            weights: Blend weights (must sum to 1.0)
            style: Optional style to apply to remix
        
        Returns:
            Remixed image data (same format as evolve())
        """
        if len(asset_ids) < 2:
            raise ValueError("Need at least 2 assets to remix")
        
        if len(asset_ids) > 4:
            raise ValueError("Maximum 4 assets for remix")
        
        # Get all source assets
        source_projects = []
        for asset_id in asset_ids:
            project = self.session.query(GraphicsProject).filter_by(id=asset_id).first()
            if project:
                source_projects.append(project)
        
        if not source_projects:
            raise ValueError("No valid source assets found")
        
        # Build remix prompt
        prompts = [p.prompt for p in source_projects]
        
        if blend_mode == "interpolate":
            remix_prompt = f"Seamless blend of: {' AND '.join(prompts)}"
        elif blend_mode == "combine":
            remix_prompt = f"Combine elements from: {' + '.join(prompts)}"
        elif blend_mode == "hybrid":
            remix_prompt = f"Hybrid fusion of: {' merged with '.join(prompts)}"
        elif blend_mode == "collage":
            remix_prompt = f"Artistic collage inspired by: {', '.join(prompts)}"
        else:
            remix_prompt = f"Creative mix of: {' and '.join(prompts)}"
        
        if style:
            remix_prompt += f", {style} style"
        
        # Apply weights if provided
        if weights and len(weights) == len(source_projects):
            remix_prompt += f" (blend weights: {', '.join([f'{w:.1f}' for w in weights])})"
        
        # Generate remix image
        from graphics_engines import UniversalGraphicsInterface
        graphics = UniversalGraphicsInterface()
        
        try:
            result = graphics.generate(remix_prompt, engine="midjourney")  # Midjourney excels at blending
            image_url = result.get("image_url")
        except:
            image_url = "https://via.placeholder.com/1024x1024/F59E0B/FFFFFF?text=Remixed+Image"
        
        # Use first project as base for attributes
        base_project = source_projects[0]
        
        # Merge tags from all sources
        all_tags = set()
        for p in source_projects:
            if p.tags:
                all_tags.update(p.tags.split(','))
        merged_tags = ','.join(all_tags)
        
        # Create remix project
        remix_project = GraphicsProject(
            prompt=remix_prompt,
            aspect_ratio=base_project.aspect_ratio,
            color_palette=base_project.color_palette,
            mood=base_project.mood,
            lighting=base_project.lighting,
            camera_angle=base_project.camera_angle,
            thumbnail_url=image_url,
            tags=merged_tags,
            category=base_project.category,
            user_id=base_project.user_id,
            team_id=base_project.team_id,
            original_prompt=remix_prompt,
            prompt_version=1,  # First version of remix
            parent_project_id=base_project.id,  # Link to primary source
            prompt_source="remixed"
        )
        
        self.session.add(remix_project)
        self.session.commit()
        
        return {
            "remixed_asset_id": str(remix_project.id),
            "source_asset_ids": asset_ids,
            "blend_mode": blend_mode,
            "weights": weights,
            "image_url": image_url,
            "prompt": remix_prompt,
            "created_at": remix_project.timestamp.isoformat() + "Z"
        }
    
    def mutate(
        self,
        asset_id: str,
        mutation_type: str = "experimental",
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create experimental mutations (wild variations)
        
        Mutation types:
        - experimental: Random creative variations
        - genre_shift: Change artistic genre
        - mood_shift: Alter emotional tone
        - color_shift: Change color palette dramatically
        - composition_shift: Alter layout/composition
        
        Args:
            asset_id: ID of image to mutate
            mutation_type: Type of mutation
            parameters: Mutation settings:
                - chaos_level: 0.0-1.0 (how wild)
                - target_genre: New artistic genre
                - target_mood: New emotional tone
                - target_palette: New color scheme
        
        Returns:
            Mutated image data (same format as evolve())
        """
        # Get original asset
        original_project = self.session.query(GraphicsProject).filter_by(id=asset_id).first()
        
        if not original_project:
            raise ValueError(f"Asset {asset_id} not found")
        
        # Build mutation prompt
        params = parameters or {}
        chaos_level = params.get("chaos_level", 0.7)
        
        base_prompt = original_project.prompt
        
        if mutation_type == "experimental":
            mutation_prompt = f"Experimental wild variation of: {base_prompt}, chaos level {int(chaos_level * 100)}"
        
        elif mutation_type == "genre_shift":
            target_genre = params.get("target_genre", "surrealist")
            mutation_prompt = f"Transform to {target_genre} genre: {base_prompt}"
        
        elif mutation_type == "mood_shift":
            target_mood = params.get("target_mood", "mysterious")
            mutation_prompt = f"{base_prompt}, but with {target_mood} mood"
        
        elif mutation_type == "color_shift":
            target_palette = params.get("target_palette", "neon")
            mutation_prompt = f"{base_prompt}, reimagined with {target_palette} color palette"
        
        elif mutation_type == "composition_shift":
            mutation_prompt = f"Recompose with different layout: {base_prompt}"
        
        else:
            mutation_prompt = f"Creative mutation of: {base_prompt}"
        
        # Add chaos modifiers
        if chaos_level > 0.8:
            mutation_prompt += ", extremely abstract and unconventional"
        elif chaos_level > 0.5:
            mutation_prompt += ", bold creative liberties"
        
        # Generate mutated image
        from graphics_engines import UniversalGraphicsInterface
        graphics = UniversalGraphicsInterface()
        
        try:
            # Use engine that handles chaos well
            result = graphics.generate(mutation_prompt, engine="midjourney", chaos=int(chaos_level * 100))
            image_url = result.get("image_url")
        except:
            image_url = "https://via.placeholder.com/1024x1024/DC2626/FFFFFF?text=Mutated+Image"
        
        # Create mutated project
        mutated_project = GraphicsProject(
            prompt=mutation_prompt,
            aspect_ratio=original_project.aspect_ratio,
            color_palette=params.get("target_palette", original_project.color_palette),
            mood=params.get("target_mood", original_project.mood),
            lighting=original_project.lighting,
            camera_angle=original_project.camera_angle,
            thumbnail_url=image_url,
            tags=f"{original_project.tags},{mutation_type}" if original_project.tags else mutation_type,
            category=original_project.category,
            user_id=original_project.user_id,
            team_id=original_project.team_id,
            original_prompt=original_project.original_prompt or original_project.prompt,
            prompt_version=(original_project.prompt_version or 1) + 1,
            parent_project_id=original_project.id,
            prompt_source="mutated"
        )
        
        self.session.add(mutated_project)
        self.session.commit()
        
        return {
            "mutated_asset_id": str(mutated_project.id),
            "original_asset_id": asset_id,
            "mutation_type": mutation_type,
            "chaos_level": chaos_level,
            "generation": mutated_project.prompt_version,
            "image_url": image_url,
            "prompt": mutation_prompt,
            "created_at": mutated_project.timestamp.isoformat() + "Z"
        }
    
    def get_lineage_tree(
        self,
        asset_id: str,
        max_depth: int = 10
    ) -> Dict[str, Any]:
        """
        Get complete evolutionary lineage (ancestors + descendants)
        
        Args:
            asset_id: ID of asset to get lineage for
            max_depth: Maximum tree depth to prevent infinite recursion
        
        Returns:
            {
                "asset_id": "img_123",
                "ancestors": [...],  # Parent → grandparent → etc.
                "descendants": [...],  # Children → grandchildren → etc.
                "total_generations": 5
            }
        """
        project = self.session.query(GraphicsProject).filter_by(id=asset_id).first()
        
        if not project:
            return {"error": "Asset not found"}
        
        # Get ancestors (walk up the tree)
        ancestors = self._get_ancestors(project, depth=0, max_depth=max_depth)
        
        # Get descendants (walk down the tree)
        descendants = self._get_descendants(project, depth=0, max_depth=max_depth)
        
        return {
            "asset_id": asset_id,
            "prompt": project.prompt,
            "generation": project.prompt_version or 1,
            "ancestors": ancestors,
            "descendants": descendants,
            "total_generations": len(ancestors) + len(descendants) + 1
        }
    
    def _get_ancestors(
        self,
        project: GraphicsProject,
        depth: int,
        max_depth: int
    ) -> List[Dict[str, Any]]:
        """Recursively get parent lineage"""
        if depth >= max_depth:
            return []
        
        if not project.parent_project_id:
            return []
        
        parent = self.session.query(GraphicsProject).get(project.parent_project_id)
        
        if not parent:
            return []
        
        ancestor_data = {
            "asset_id": str(parent.id),
            "prompt": parent.prompt,
            "generation": parent.prompt_version or 1,
            "relationship": "parent",
            "source": parent.prompt_source,
            "depth": depth + 1
        }
        
        # Recursively get grandparents
        grandparents = self._get_ancestors(parent, depth + 1, max_depth)
        
        return [ancestor_data] + grandparents
    
    def _get_descendants(
        self,
        project: GraphicsProject,
        depth: int,
        max_depth: int
    ) -> List[Dict[str, Any]]:
        """Recursively get children lineage"""
        if depth >= max_depth:
            return []
        
        # Find all children (projects with this as parent)
        children = self.session.query(GraphicsProject).filter_by(parent_project_id=project.id).all()
        
        if not children:
            return []
        
        descendants = []
        
        for child in children:
            child_data = {
                "asset_id": str(child.id),
                "prompt": child.prompt,
                "generation": child.prompt_version or 1,
                "relationship": "child",
                "source": child.prompt_source,
                "depth": depth + 1
            }
            
            # Recursively get grandchildren
            grandchildren = self._get_descendants(child, depth + 1, max_depth)
            
            child_data["children"] = grandchildren
            descendants.append(child_data)
        
        return descendants


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    engine = GraphicsEvolutionEngine()
    
    # Example: Evolve an image
    print("🎨 Testing Graphics Evolution Engine\n")
    
    # This would require an actual asset_id from database
    # evolved = engine.evolve(
    #     asset_id="1",
    #     evolution_type="enhance",
    #     parameters={"quality_boost": 0.8, "detail_level": "high"}
    # )
    # print("✅ Evolved image:", evolved)
    
    print("Available evolution types:", list(engine.evolution_types.keys()))
    print("Available transform types:", list(engine.transform_types.keys()))
