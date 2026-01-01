"""
Universal Generation Interface (UGI) - Video Studio Phase 3

The orchestrator that routes video generation requests to the appropriate engine,
handles storage, generates thumbnails, and manages the complete pipeline.

Flow:
1. User enters prompt + settings
2. UGI selects engine connector
3. Engine generates video (with polling)
4. Video saved to storage
5. Thumbnail extracted
6. VideoAsset created in database
7. Clip appears on timeline

This is the creative super-hub.
"""

import os
import io
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime
from PIL import Image
import requests
from flask_sqlalchemy import SQLAlchemy


class UniversalGenerationInterface:
    """
    Universal Video Generation Interface
    
    Routes generation requests to the appropriate engine,
    handles storage, thumbnails, and database integration.
    """
    
    def __init__(self, db: SQLAlchemy, storage_config, video_pipeline):
        """
        Initialize UGI with database and storage.
        
        Args:
            db: SQLAlchemy database instance
            storage_config: VideoStorageConfig instance
            video_pipeline: VideoGenerationPipeline instance
        """
        self.db = db
        self.storage = storage_config
        self.pipeline = video_pipeline
        
        # Engine capabilities
        self.engine_specs = {
            'runway': {
                'max_duration': 10,
                'default_duration': 5,
                'supports_image_to_video': False,
                'aspect_ratios': ['16:9', '9:16', '1:1'],
                'default_aspect': '16:9'
            },
            'pika': {
                'max_duration': 6,
                'default_duration': 3,
                'supports_image_to_video': True,
                'aspect_ratios': ['16:9', '9:16', '1:1'],
                'default_aspect': '16:9'
            },
            'luma': {
                'max_duration': 5,
                'default_duration': 5,
                'supports_image_to_video': True,
                'aspect_ratios': ['16:9', '9:16', '1:1', '21:9'],
                'default_aspect': '16:9'
            },
            'stability': {
                'max_duration': 4,
                'default_duration': 4,
                'supports_image_to_video': True,
                'aspect_ratios': ['16:9', '9:16', '1:1'],
                'default_aspect': '16:9'
            }
        }
    
    def generate(
        self,
        prompt: str,
        engine: str = 'runway',
        project_id: Optional[int] = None,
        user_id: Optional[int] = None,
        **settings
    ) -> Dict[str, Any]:
        """
        Complete generation pipeline: prompt → video → storage → database.
        
        Args:
            prompt: Text description of video
            engine: Engine to use (runway, pika, luma, stability)
            project_id: VideoProject ID to associate with
            user_id: User who created the video
            **settings: Engine-specific settings (duration, aspect_ratio, etc.)
        
        Returns:
            dict: {
                "asset_id": 123,
                "video_url": "https://...",
                "thumbnail_url": "https://...",
                "duration": 5.0,
                "status": "complete",
                "engine": "runway"
            }
        
        Raises:
            Exception: If generation fails
        """
        # Step 1: Validate engine and settings
        engine = self._validate_engine(engine)
        settings = self._validate_settings(engine, settings)
        
        # Step 2: Generate video using selected engine
        print(f"🎬 UGI: Generating with {engine}...")
        result = self.pipeline.generate_video(prompt, engine=engine, **settings)
        
        if result.get('status') != 'complete':
            raise Exception(f"Generation failed: {result}")
        
        # Step 3: Store video in cloud storage
        print(f"☁️ UGI: Storing video...")
        stored_video_url = self._store_video(result['video_url'], engine)
        
        # Step 4: Generate and store thumbnail
        print(f"🖼️ UGI: Generating thumbnail...")
        thumbnail_url = self._generate_and_store_thumbnail(
            result.get('thumbnail_url') or result['video_url'],
            engine
        )
        
        # Step 5: Create VideoAsset in database
        print(f"💾 UGI: Creating asset record...")
        asset = self._create_video_asset(
            prompt=prompt,
            video_url=stored_video_url,
            thumbnail_url=thumbnail_url,
            duration=result.get('duration', settings.get('duration', 5.0)),
            engine=engine,
            project_id=project_id,
            user_id=user_id,
            settings=settings
        )
        
        # Step 6: Return complete result
        print(f"✅ UGI: Generation complete! Asset ID: {asset.id}")
        return {
            "asset_id": asset.id,
            "video_url": stored_video_url,
            "thumbnail_url": thumbnail_url,
            "duration": asset.duration,
            "status": "complete",
            "engine": engine,
            "prompt": prompt,
            "created_at": asset.created_at.isoformat()
        }
    
    def regenerate(self, asset_id: int, **new_settings) -> Dict[str, Any]:
        """
        Regenerate video with same prompt, new variation.
        
        Args:
            asset_id: Original VideoAsset ID
            **new_settings: Override settings (seed, etc.)
        
        Returns:
            New VideoAsset result
        """
        # Import here to avoid circular dependency
        from flask_dashboard import VideoAsset
        
        original = self.db.session.query(VideoAsset).get(asset_id)
        if not original:
            raise ValueError(f"Asset {asset_id} not found")
        
        # Use original prompt but new seed/settings
        settings = original.settings or {}
        settings.update(new_settings)
        
        # Generate new variation
        return self.generate(
            prompt=original.prompt,
            engine=original.engine or 'runway',
            project_id=original.project_id,
            user_id=original.user_id,
            **settings
        )
    
    def evolve(self, asset_id: int, evolution_type: str, **params) -> Dict[str, Any]:
        """
        Evolve video based on style, mood, angle, etc.
        
        Args:
            asset_id: Original VideoAsset ID
            evolution_type: "variation", "mood", "lighting", "angle"
            **params: Evolution parameters (mood="dramatic", etc.)
        
        Returns:
            New evolved VideoAsset result
        """
        from flask_dashboard import VideoAsset
        
        original = self.db.session.query(VideoAsset).get(asset_id)
        if not original:
            raise ValueError(f"Asset {asset_id} not found")
        
        # Build evolved prompt
        evolved_prompt = self._build_evolved_prompt(
            original.prompt,
            evolution_type,
            params
        )
        
        # Generate with evolved prompt
        return self.generate(
            prompt=evolved_prompt,
            engine=original.engine or 'runway',
            project_id=original.project_id,
            user_id=original.user_id,
            **(original.settings or {})
        )
    
    def extend(self, asset_id: int, extension_type: str) -> Dict[str, Any]:
        """
        Extend video to generate next moment/shot/beat.
        
        Args:
            asset_id: Original VideoAsset ID
            extension_type: "next_moment", "next_shot", "next_beat"
        
        Returns:
            New extended VideoAsset result
        """
        from flask_dashboard import VideoAsset
        
        original = self.db.session.query(VideoAsset).get(asset_id)
        if not original:
            raise ValueError(f"Asset {asset_id} not found")
        
        # Build extension prompt
        extended_prompt = self._build_extension_prompt(
            original.prompt,
            extension_type
        )
        
        # Generate continuation
        return self.generate(
            prompt=extended_prompt,
            engine=original.engine or 'runway',
            project_id=original.project_id,
            user_id=original.user_id,
            **(original.settings or {})
        )
    
    def _validate_engine(self, engine: str) -> str:
        """Validate and normalize engine name"""
        engine = engine.lower()
        if engine not in self.engine_specs:
            print(f"⚠️ Unknown engine '{engine}', falling back to runway")
            return 'runway'
        return engine
    
    def _validate_settings(self, engine: str, settings: Dict) -> Dict:
        """Validate settings for selected engine"""
        specs = self.engine_specs[engine]
        validated = {}
        
        # Duration
        duration = settings.get('duration', specs['default_duration'])
        validated['duration'] = min(duration, specs['max_duration'])
        
        # Aspect ratio
        aspect = settings.get('aspect_ratio', specs['default_aspect'])
        if aspect not in specs['aspect_ratios']:
            aspect = specs['default_aspect']
        validated['aspect_ratio'] = aspect
        
        # Pass through other settings
        for key in ['motion_scale', 'motion', 'seed', 'guidance_scale', 'cfg_scale']:
            if key in settings:
                validated[key] = settings[key]
        
        return validated
    
    def _store_video(self, video_url: str, engine: str) -> str:
        """Download and store video in cloud storage"""
        try:
            # Download video
            response = requests.get(video_url, timeout=60)
            response.raise_for_status()
            video_data = response.content
            
            # Generate filename
            filename = f"{engine}_{self._generate_hash(video_data)}.mp4"
            
            # Upload to storage
            stored_url = self.storage.upload_video(io.BytesIO(video_data), filename)
            return stored_url
        
        except Exception as e:
            print(f"⚠️ Storage failed: {e}, using original URL")
            return video_url
    
    def _generate_and_store_thumbnail(self, source_url: str, engine: str) -> str:
        """Generate thumbnail from video/image and store"""
        try:
            # Download source
            response = requests.get(source_url, timeout=30)
            response.raise_for_status()
            
            # If it's an image URL, use directly
            if source_url.endswith(('.jpg', '.jpeg', '.png')):
                image_data = response.content
            else:
                # For video, extract first frame (simplified - use opencv in production)
                image_data = self._extract_first_frame(response.content)
            
            # Generate thumbnail filename
            filename = f"thumb_{engine}_{self._generate_hash(image_data)}.jpg"
            
            # Upload thumbnail
            thumbnail_url = self.storage.upload_video(io.BytesIO(image_data), filename)
            return thumbnail_url
        
        except Exception as e:
            print(f"⚠️ Thumbnail generation failed: {e}")
            return source_url
    
    def _extract_first_frame(self, video_data: bytes) -> bytes:
        """Extract first frame from video (placeholder - use opencv/ffmpeg in production)"""
        # In production, use: cv2.VideoCapture or ffmpeg
        # For now, return placeholder
        return video_data[:1024]  # Simplified
    
    def _generate_hash(self, data: bytes) -> str:
        """Generate hash for unique filenames"""
        return hashlib.md5(data[:10000]).hexdigest()[:12]
    
    def _create_video_asset(
        self,
        prompt: str,
        video_url: str,
        thumbnail_url: str,
        duration: float,
        engine: str,
        project_id: Optional[int],
        user_id: Optional[int],
        settings: Dict
    ):
        """Create VideoAsset database record"""
        from flask_dashboard import VideoAsset
        
        asset = VideoAsset(
            project_id=project_id,
            user_id=user_id,
            prompt=prompt,
            video_url=video_url,
            thumbnail_url=thumbnail_url,
            duration=duration,
            status='complete',
            engine=engine,
            settings=settings,
            file_size=0,  # Update if available
            tags=f"generated,{engine}"
        )
        
        self.db.session.add(asset)
        self.db.session.commit()
        
        return asset
    
    def _build_evolved_prompt(
        self,
        original_prompt: str,
        evolution_type: str,
        params: Dict
    ) -> str:
        """Build evolved prompt based on type"""
        if evolution_type == 'variation':
            return f"{original_prompt}, alternate composition"
        
        elif evolution_type == 'mood':
            mood = params.get('mood', 'dramatic')
            return f"{original_prompt}, {mood} mood"
        
        elif evolution_type == 'lighting':
            lighting = params.get('lighting', 'golden hour')
            return f"{original_prompt}, {lighting} lighting"
        
        elif evolution_type == 'angle':
            angle = params.get('angle', 'aerial view')
            return f"{original_prompt}, {angle}"
        
        else:
            return f"{original_prompt}, variation"
    
    def _build_extension_prompt(
        self,
        original_prompt: str,
        extension_type: str
    ) -> str:
        """Build extension prompt"""
        if extension_type == 'next_moment':
            return f"Continuation of: {original_prompt}, showing what happens next"
        
        elif extension_type == 'next_shot':
            return f"Following shot after: {original_prompt}"
        
        elif extension_type == 'next_beat':
            return f"Next beat in the sequence: {original_prompt}"
        
        else:
            return f"Continuation of: {original_prompt}"
    
    def get_engine_capabilities(self, engine: str) -> Dict[str, Any]:
        """Get capabilities for specific engine"""
        return self.engine_specs.get(engine, {})
    
    def list_available_engines(self) -> List[str]:
        """List all available engines"""
        return list(self.engine_specs.keys())
