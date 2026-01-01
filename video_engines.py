"""
Video Engines - Multi-AI Video Generation System (Phase 8)

This module provides unified access to multiple video generation AI engines:
- Runway Gen-2: High-quality, cinematic video generation
- Pika Labs: Creative video generation with motion control
- Luma AI: Text-to-video and image-to-video generation
- Stability Video: Stable Video Diffusion for video generation

Architecture mirrors Graphics Phase 8 (graphics_engines.py) for consistency.

Author: Codex Dominion Video Studio
Created: December 22, 2025
Version: 8.0.0
"""

import os
import time
import json
import base64
import asyncio
from enum import Enum
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import requests
from datetime import datetime


# =============================================================================
# VIDEO ENGINE SPECIFICATIONS
# =============================================================================

@dataclass
class VideoEngineSpec:
    """Specifications for a video generation engine"""
    name: str
    provider: str
    max_duration: int  # seconds
    max_resolution: Tuple[int, int]  # (width, height)
    supported_fps: List[int]
    supports_image_to_video: bool
    supports_video_to_video: bool
    supports_camera_motion: bool
    supports_subject_motion: bool
    typical_generation_time: int  # seconds
    cost_per_second: float  # estimated USD


VIDEO_ENGINE_SPECS = {
    "runway-gen2": VideoEngineSpec(
        name="Runway Gen-2",
        provider="Runway ML",
        max_duration=18,
        max_resolution=(1408, 768),
        supported_fps=[24, 30],
        supports_image_to_video=True,
        supports_video_to_video=True,
        supports_camera_motion=True,
        supports_subject_motion=True,
        typical_generation_time=120,
        cost_per_second=0.05
    ),
    "pika": VideoEngineSpec(
        name="Pika Labs",
        provider="Pika",
        max_duration=3,
        max_resolution=(1280, 720),
        supported_fps=[24, 30],
        supports_image_to_video=True,
        supports_video_to_video=False,
        supports_camera_motion=True,
        supports_subject_motion=True,
        typical_generation_time=60,
        cost_per_second=0.03
    ),
    "luma": VideoEngineSpec(
        name="Luma AI Dream Machine",
        provider="Luma Labs",
        max_duration=5,
        max_resolution=(1280, 720),
        supported_fps=[24, 30],
        supports_image_to_video=True,
        supports_video_to_video=False,
        supports_camera_motion=True,
        supports_subject_motion=True,
        typical_generation_time=90,
        cost_per_second=0.04
    ),
    "stability-video": VideoEngineSpec(
        name="Stable Video Diffusion",
        provider="Stability AI",
        max_duration=4,
        max_resolution=(1024, 576),
        supported_fps=[24],
        supports_image_to_video=True,
        supports_video_to_video=False,
        supports_camera_motion=False,
        supports_subject_motion=True,
        typical_generation_time=30,
        cost_per_second=0.02
    )
}


# =============================================================================
# CAMERA MOTION TYPES
# =============================================================================

class CameraMotion(str, Enum):
    """Camera movement types"""
    STATIC = "static"
    PAN_LEFT = "pan_left"
    PAN_RIGHT = "pan_right"
    TILT_UP = "tilt_up"
    TILT_DOWN = "tilt_down"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    DOLLY_IN = "dolly_in"
    DOLLY_OUT = "dolly_out"
    ORBIT_LEFT = "orbit_left"
    ORBIT_RIGHT = "orbit_right"
    CRANE_UP = "crane_up"
    CRANE_DOWN = "crane_down"


class SubjectMotion(str, Enum):
    """Subject movement types"""
    NONE = "none"
    SLOW = "slow"
    MEDIUM = "medium"
    FAST = "fast"
    WALK = "walk"
    RUN = "run"
    FLY = "fly"
    SPIN = "spin"
    GROW = "grow"
    SHRINK = "shrink"


# =============================================================================
# RUNWAY GEN-2 ENGINE
# =============================================================================

class RunwayEngine:
    """
    Runway Gen-2 video generation engine
    
    Capabilities:
    - Text-to-video generation
    - Image-to-video generation
    - Video-to-video transformation
    - Camera motion control
    - Subject motion control
    - Up to 18 seconds duration
    - 1408x768 resolution
    
    API Documentation: https://docs.runwayml.com/
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Runway Gen-2 engine
        
        Args:
            api_key: Runway API key (or set RUNWAY_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('RUNWAY_API_KEY')
        if not self.api_key:
            print("⚠️ No Runway API key - set RUNWAY_API_KEY environment variable")
        
        self.api_base = "https://api.runwayml.com/v1"
        self.spec = VIDEO_ENGINE_SPECS["runway-gen2"]
    
    async def generate_text_to_video(
        self,
        prompt: str,
        duration: int = 4,
        resolution: str = "1408x768",
        fps: int = 24,
        camera_motion: Optional[CameraMotion] = None,
        subject_motion: Optional[SubjectMotion] = None,
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate video from text prompt
        
        Args:
            prompt: Text description of the video
            duration: Duration in seconds (max 18)
            resolution: Video resolution (e.g., "1408x768", "1280x720")
            fps: Frames per second (24 or 30)
            camera_motion: Camera movement type
            subject_motion: Subject movement speed
            seed: Random seed for reproducibility
        
        Returns:
            {
                'video_url': str,
                'preview_url': str,
                'duration': int,
                'resolution': tuple,
                'fps': int,
                'job_id': str,
                'status': 'generating' | 'complete' | 'failed',
                'estimated_time': int,
                'metadata': dict
            }
        """
        if not self.api_key:
            raise ValueError("Runway API key required")
        
        # Build prompt with motion controls
        enhanced_prompt = prompt
        if camera_motion:
            enhanced_prompt += f" Camera motion: {camera_motion.value}"
        if subject_motion:
            enhanced_prompt += f" Subject motion: {subject_motion.value}"
        
        # Prepare request payload
        payload = {
            "promptText": enhanced_prompt,
            "duration": min(duration, self.spec.max_duration),
            "resolution": resolution,
            "fps": fps if fps in self.spec.supported_fps else 24,
            "seed": seed or int(time.time())
        }
        
        # Make API request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/gen2/text-to-video",
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'video_url': data.get('url'),
                'preview_url': data.get('preview_url'),
                'duration': duration,
                'resolution': tuple(map(int, resolution.split('x'))),
                'fps': fps,
                'job_id': data.get('id'),
                'status': 'generating',
                'estimated_time': self.spec.typical_generation_time,
                'metadata': {
                    'engine': 'runway-gen2',
                    'prompt': prompt,
                    'camera_motion': camera_motion.value if camera_motion else None,
                    'subject_motion': subject_motion.value if subject_motion else None,
                    'seed': payload['seed']
                }
            }
            
        except requests.RequestException as e:
            print(f"❌ Runway Gen-2 API error: {e}")
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    async def generate_image_to_video(
        self,
        image_url: str,
        prompt: str,
        duration: int = 4,
        camera_motion: Optional[CameraMotion] = None,
        subject_motion: Optional[SubjectMotion] = None
    ) -> Dict[str, Any]:
        """
        Generate video from static image
        
        Args:
            image_url: URL or base64 of source image
            prompt: Text description of desired motion/scene
            duration: Duration in seconds (max 18)
            camera_motion: Camera movement type
            subject_motion: Subject movement speed
        
        Returns:
            Same format as generate_text_to_video
        """
        if not self.api_key:
            raise ValueError("Runway API key required")
        
        enhanced_prompt = prompt
        if camera_motion:
            enhanced_prompt += f" Camera motion: {camera_motion.value}"
        if subject_motion:
            enhanced_prompt += f" Subject motion: {subject_motion.value}"
        
        payload = {
            "promptImage": image_url,
            "promptText": enhanced_prompt,
            "duration": min(duration, self.spec.max_duration)
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/gen2/image-to-video",
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'video_url': data.get('url'),
                'preview_url': data.get('preview_url'),
                'duration': duration,
                'job_id': data.get('id'),
                'status': 'generating',
                'estimated_time': self.spec.typical_generation_time,
                'metadata': {
                    'engine': 'runway-gen2',
                    'source_image': image_url,
                    'prompt': prompt,
                    'camera_motion': camera_motion.value if camera_motion else None,
                    'subject_motion': subject_motion.value if subject_motion else None
                }
            }
            
        except requests.RequestException as e:
            print(f"❌ Runway Gen-2 API error: {e}")
            return {'error': str(e), 'status': 'failed'}
    
    async def check_status(self, job_id: str) -> Dict[str, Any]:
        """
        Check generation status
        
        Args:
            job_id: Job ID from generate_* call
        
        Returns:
            {
                'status': 'generating' | 'complete' | 'failed',
                'progress': float,  # 0.0 to 1.0
                'video_url': str (if complete),
                'error': str (if failed)
            }
        """
        if not self.api_key:
            raise ValueError("Runway API key required")
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            response = requests.get(
                f"{self.api_base}/tasks/{job_id}",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'status': data.get('status', 'unknown'),
                'progress': data.get('progress', 0.0),
                'video_url': data.get('output', [{}])[0].get('url') if data.get('status') == 'SUCCEEDED' else None,
                'error': data.get('error') if data.get('status') == 'FAILED' else None
            }
            
        except requests.RequestException as e:
            print(f"❌ Runway status check error: {e}")
            return {'status': 'unknown', 'error': str(e)}


# =============================================================================
# PIKA LABS ENGINE
# =============================================================================

class PikaEngine:
    """
    Pika Labs video generation engine
    
    Capabilities:
    - Text-to-video generation
    - Image-to-video generation
    - Camera motion control
    - Subject motion control
    - Up to 3 seconds duration
    - 1280x720 resolution
    
    API Documentation: https://docs.pika.art/
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Pika Labs engine
        
        Args:
            api_key: Pika API key (or set PIKA_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('PIKA_API_KEY')
        if not self.api_key:
            print("⚠️ No Pika API key - set PIKA_API_KEY environment variable")
        
        self.api_base = "https://api.pika.art/v1"
        self.spec = VIDEO_ENGINE_SPECS["pika"]
    
    async def generate(
        self,
        prompt: str,
        image_url: Optional[str] = None,
        duration: int = 3,
        fps: int = 24,
        camera_motion: Optional[CameraMotion] = None,
        motion_strength: float = 1.0
    ) -> Dict[str, Any]:
        """
        Generate video from text or image
        
        Args:
            prompt: Text description
            image_url: Optional source image URL
            duration: Duration in seconds (max 3)
            fps: Frames per second (24 or 30)
            camera_motion: Camera movement type
            motion_strength: Motion intensity (0.1 to 2.0)
        
        Returns:
            Same format as RunwayEngine.generate_text_to_video
        """
        if not self.api_key:
            raise ValueError("Pika API key required")
        
        payload = {
            "prompt": prompt,
            "duration": min(duration, self.spec.max_duration),
            "fps": fps if fps in self.spec.supported_fps else 24,
            "motion": motion_strength
        }
        
        if image_url:
            payload["image"] = image_url
        
        if camera_motion:
            payload["camera_motion"] = camera_motion.value
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/generate",
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'video_url': data.get('video_url'),
                'preview_url': data.get('preview_url'),
                'duration': duration,
                'resolution': (1280, 720),
                'fps': fps,
                'job_id': data.get('id'),
                'status': 'generating',
                'estimated_time': self.spec.typical_generation_time,
                'metadata': {
                    'engine': 'pika',
                    'prompt': prompt,
                    'source_image': image_url,
                    'camera_motion': camera_motion.value if camera_motion else None,
                    'motion_strength': motion_strength
                }
            }
            
        except requests.RequestException as e:
            print(f"❌ Pika API error: {e}")
            return {'error': str(e), 'status': 'failed'}


# =============================================================================
# LUMA AI ENGINE
# =============================================================================

class LumaEngine:
    """
    Luma AI Dream Machine video generation engine
    
    Capabilities:
    - Text-to-video generation
    - Image-to-video generation
    - Camera motion control
    - Up to 5 seconds duration
    - 1280x720 resolution
    
    API Documentation: https://docs.lumalabs.ai/
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Luma AI engine
        
        Args:
            api_key: Luma API key (or set LUMA_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('LUMA_API_KEY')
        if not self.api_key:
            print("⚠️ No Luma API key - set LUMA_API_KEY environment variable")
        
        self.api_base = "https://api.lumalabs.ai/v1"
        self.spec = VIDEO_ENGINE_SPECS["luma"]
    
    async def generate(
        self,
        prompt: str,
        image_url: Optional[str] = None,
        duration: int = 5,
        aspect_ratio: str = "16:9",
        loop: bool = False
    ) -> Dict[str, Any]:
        """
        Generate video from text or image
        
        Args:
            prompt: Text description
            image_url: Optional source image URL
            duration: Duration in seconds (max 5)
            aspect_ratio: Aspect ratio ("16:9", "9:16", "1:1", "4:3")
            loop: Create seamless loop
        
        Returns:
            Same format as RunwayEngine.generate_text_to_video
        """
        if not self.api_key:
            raise ValueError("Luma API key required")
        
        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "loop": loop
        }
        
        if image_url:
            payload["keyframes"] = {"frame0": {"type": "image", "url": image_url}}
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/generations",
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'video_url': data.get('video', {}).get('url'),
                'preview_url': data.get('video', {}).get('thumbnail_url'),
                'duration': duration,
                'resolution': (1280, 720) if aspect_ratio == "16:9" else (720, 1280),
                'fps': 24,
                'job_id': data.get('id'),
                'status': data.get('state', 'generating'),
                'estimated_time': self.spec.typical_generation_time,
                'metadata': {
                    'engine': 'luma',
                    'prompt': prompt,
                    'source_image': image_url,
                    'aspect_ratio': aspect_ratio,
                    'loop': loop
                }
            }
            
        except requests.RequestException as e:
            print(f"❌ Luma API error: {e}")
            return {'error': str(e), 'status': 'failed'}


# =============================================================================
# STABILITY VIDEO ENGINE
# =============================================================================

class StabilityVideoEngine:
    """
    Stable Video Diffusion engine
    
    Capabilities:
    - Image-to-video generation
    - Up to 4 seconds duration
    - 1024x576 resolution
    - Fast generation
    - Cost-effective
    
    API Documentation: https://platform.stability.ai/docs/api-reference#tag/v2alpha/operation/videoStableDiffusion
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Stability Video engine
        
        Args:
            api_key: Stability API key (or set STABILITY_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('STABILITY_API_KEY')
        if not self.api_key:
            print("⚠️ No Stability API key - set STABILITY_API_KEY environment variable")
        
        self.api_base = "https://api.stability.ai/v2alpha"
        self.spec = VIDEO_ENGINE_SPECS["stability-video"]
    
    async def generate_from_image(
        self,
        image_path: str,
        motion_bucket_id: int = 127,
        cfg_scale: float = 2.5,
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate video from static image
        
        Args:
            image_path: Path to source image or URL
            motion_bucket_id: Motion intensity (40-255, default 127)
            cfg_scale: How closely to follow prompt (0-10, default 2.5)
            seed: Random seed for reproducibility
        
        Returns:
            Same format as RunwayEngine.generate_text_to_video
        """
        if not self.api_key:
            raise ValueError("Stability API key required")
        
        # Prepare multipart form data
        files = {}
        if image_path.startswith('http'):
            # Download image
            img_response = requests.get(image_path)
            files['image'] = ('image.png', img_response.content, 'image/png')
        else:
            files['image'] = open(image_path, 'rb')
        
        data = {
            'seed': seed or int(time.time()),
            'cfg_scale': cfg_scale,
            'motion_bucket_id': motion_bucket_id
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/image-to-video",
                headers=headers,
                files=files,
                data=data,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            
            return {
                'video_url': result.get('video'),
                'preview_url': result.get('preview'),
                'duration': 4,
                'resolution': (1024, 576),
                'fps': 24,
                'job_id': result.get('id'),
                'status': 'generating',
                'estimated_time': self.spec.typical_generation_time,
                'metadata': {
                    'engine': 'stability-video',
                    'source_image': image_path,
                    'motion_bucket_id': motion_bucket_id,
                    'cfg_scale': cfg_scale,
                    'seed': data['seed']
                }
            }
            
        except requests.RequestException as e:
            print(f"❌ Stability Video API error: {e}")
            return {'error': str(e), 'status': 'failed'}


# =============================================================================
# UNIVERSAL VIDEO INTERFACE
# =============================================================================

class UniversalVideoInterface:
    """
    Universal video generation interface - auto-routes to best engine
    
    Similar to UniversalGraphicsInterface in graphics_engines.py
    Provides single entry point for all video generation operations
    """
    
    def __init__(self):
        """Initialize all video engines"""
        self.runway = RunwayEngine()
        self.pika = PikaEngine()
        self.luma = LumaEngine()
        self.stability = StabilityVideoEngine()
        
        self.engines = {
            'runway': self.runway,
            'pika': self.pika,
            'luma': self.luma,
            'stability': self.stability
        }
    
    def get_available_engines(self) -> List[str]:
        """Get list of available engines"""
        available = []
        for name, engine in self.engines.items():
            if engine.api_key:
                available.append(name)
        return available
    
    def select_best_engine(
        self,
        duration: int,
        has_source_image: bool,
        requires_camera_motion: bool,
        budget: str = "medium"
    ) -> str:
        """
        Auto-select best engine based on requirements
        
        Args:
            duration: Desired video duration in seconds
            has_source_image: Whether starting from image
            requires_camera_motion: Whether camera motion needed
            budget: Budget constraint ("low", "medium", "high")
        
        Returns:
            Engine name ("runway", "pika", "luma", "stability")
        """
        available = self.get_available_engines()
        
        if not available:
            raise ValueError("No video engines available - set API keys")
        
        # Duration-based selection
        if duration > 5:
            if 'runway' in available:
                return 'runway'  # Can handle up to 18 seconds
        
        # Budget-based selection
        if budget == "low":
            if 'stability' in available and has_source_image:
                return 'stability'  # Cheapest option
            if 'pika' in available:
                return 'pika'  # Second cheapest
        
        # Camera motion required
        if requires_camera_motion:
            if 'runway' in available:
                return 'runway'  # Best camera controls
            if 'pika' in available:
                return 'pika'
            if 'luma' in available:
                return 'luma'
        
        # Default to first available
        return available[0]
    
    async def generate(
        self,
        prompt: str,
        engine: str = "auto",
        duration: int = 4,
        image_url: Optional[str] = None,
        camera_motion: Optional[CameraMotion] = None,
        subject_motion: Optional[SubjectMotion] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate video using specified or auto-selected engine
        
        Args:
            prompt: Text description of video
            engine: Engine to use ("auto", "runway", "pika", "luma", "stability")
            duration: Duration in seconds
            image_url: Optional source image
            camera_motion: Camera movement type
            subject_motion: Subject movement speed
            **kwargs: Engine-specific parameters
        
        Returns:
            {
                'video_url': str,
                'preview_url': str,
                'duration': int,
                'resolution': tuple,
                'fps': int,
                'engine': str,
                'job_id': str,
                'status': str,
                'estimated_time': int,
                'metadata': dict
            }
        """
        # Auto-select engine if needed
        if engine == "auto":
            engine = self.select_best_engine(
                duration=duration,
                has_source_image=image_url is not None,
                requires_camera_motion=camera_motion is not None,
                budget=kwargs.get('budget', 'medium')
            )
        
        if engine not in self.engines:
            raise ValueError(f"Unknown engine: {engine}. Available: {list(self.engines.keys())}")
        
        engine_obj = self.engines[engine]
        
        # Route to appropriate engine
        if engine == 'runway':
            if image_url:
                result = await engine_obj.generate_image_to_video(
                    image_url=image_url,
                    prompt=prompt,
                    duration=duration,
                    camera_motion=camera_motion,
                    subject_motion=subject_motion
                )
            else:
                result = await engine_obj.generate_text_to_video(
                    prompt=prompt,
                    duration=duration,
                    camera_motion=camera_motion,
                    subject_motion=subject_motion,
                    **kwargs
                )
        
        elif engine == 'pika':
            result = await engine_obj.generate(
                prompt=prompt,
                image_url=image_url,
                duration=duration,
                camera_motion=camera_motion,
                **kwargs
            )
        
        elif engine == 'luma':
            result = await engine_obj.generate(
                prompt=prompt,
                image_url=image_url,
                duration=duration,
                **kwargs
            )
        
        elif engine == 'stability':
            if not image_url:
                raise ValueError("Stability Video requires source image")
            result = await engine_obj.generate_from_image(
                image_path=image_url,
                **kwargs
            )
        
        # Add engine info to result
        result['engine'] = engine
        
        return result


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def get_engine_specs() -> Dict[str, VideoEngineSpec]:
    """Get specifications for all video engines"""
    return VIDEO_ENGINE_SPECS


def estimate_cost(engine: str, duration: int) -> float:
    """
    Estimate cost for video generation
    
    Args:
        engine: Engine name
        duration: Video duration in seconds
    
    Returns:
        Estimated cost in USD
    """
    if engine not in VIDEO_ENGINE_SPECS:
        return 0.0
    
    spec = VIDEO_ENGINE_SPECS[engine]
    return spec.cost_per_second * min(duration, spec.max_duration)


def compare_engines() -> str:
    """
    Generate comparison table of video engines
    
    Returns:
        Formatted table string
    """
    table = "VIDEO ENGINE COMPARISON\n"
    table += "=" * 80 + "\n"
    table += f"{'Engine':<20} {'Duration':<12} {'Resolution':<15} {'Camera':<10} {'Cost/sec':<10}\n"
    table += "-" * 80 + "\n"
    
    for key, spec in VIDEO_ENGINE_SPECS.items():
        table += f"{spec.name:<20} {spec.max_duration:<12}s {spec.max_resolution[0]}x{spec.max_resolution[1]:<15} "
        table += f"{'Yes' if spec.supports_camera_motion else 'No':<10} ${spec.cost_per_second:<10.2f}\n"
    
    return table


# =============================================================================
# MAIN - DEMO/TEST
# =============================================================================

if __name__ == "__main__":
    print("🎬 Video Engines Module - Phase 8")
    print("=" * 80)
    print(compare_engines())
    print("\n✅ Video engines initialized!")
    print(f"Available specs: {list(VIDEO_ENGINE_SPECS.keys())}")
    
    # Test cost estimation
    print(f"\nCost for 10-second Runway video: ${estimate_cost('runway-gen2', 10):.2f}")
    print(f"Cost for 3-second Pika video: ${estimate_cost('pika', 3):.2f}")
    print(f"Cost for 4-second Stability video: ${estimate_cost('stability-video', 4):.2f}")
