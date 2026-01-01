"""
Luma AI Dream Machine Video Generation Engine

API Documentation: https://docs.lumalabs.ai/
Model: Dream Machine (text-to-video, image-to-video)
"""

import os
import requests
import time
from typing import Dict, Any, Optional


class LumaAPIError(Exception):
    """Luma API error"""
    pass


def generate(prompt: str, **kwargs) -> Dict[str, Any]:
    """
    Generate video using Luma AI Dream Machine.
    
    Args:
        prompt: Text description of the video
        **kwargs: Optional parameters:
            - duration: Video length (seconds, default: 5)
            - keyframes: List of image URLs for keyframe guidance (optional)
            - loop: Enable seamless looping (default: False)
            - aspect_ratio: "16:9", "9:16", "1:1", "21:9" (default: "16:9")
            - extend_prompt: Auto-enhance prompt (default: True)
    
    Returns:
        dict: {
            "video_url": "https://storage.lumalabs.ai/.../video.mp4",
            "thumbnail_url": "https://storage.lumalabs.ai/.../thumb.jpg",
            "duration": 5.0,
            "status": "complete",
            "engine": "luma",
            "generation_id": "gen_abc123..."
        }
    
    Raises:
        LumaAPIError: If API call fails
    """
    api_key = os.getenv('LUMA_API_KEY')
    if not api_key:
        raise LumaAPIError("LUMA_API_KEY not set in environment")
    
    # Extract parameters with defaults
    duration = kwargs.get('duration', 5)
    keyframes = kwargs.get('keyframes', [])
    loop = kwargs.get('loop', False)
    aspect_ratio = kwargs.get('aspect_ratio', '16:9')
    extend_prompt = kwargs.get('extend_prompt', True)
    
    # Luma API endpoint
    api_url = "https://api.lumalabs.ai/dream-machine/v1/generations"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "loop": loop,
        "extend_prompt": extend_prompt
    }
    
    if keyframes:
        payload["keyframes"] = {
            "frame0": {"type": "image", "url": keyframes[0]} if keyframes else None
        }
    
    try:
        # Submit generation request
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        generation_id = result.get('id')
        
        if not generation_id:
            raise LumaAPIError(f"No generation ID in response: {result}")
        
        # Poll for completion
        status_url = f"https://api.lumalabs.ai/dream-machine/v1/generations/{generation_id}"
        max_attempts = 60  # ~5 minutes max (5s intervals)
        
        for attempt in range(max_attempts):
            status_response = requests.get(status_url, headers=headers, timeout=30)
            status_response.raise_for_status()
            status_data = status_response.json()
            
            state = status_data.get('state')
            
            if state == 'completed':
                video_obj = status_data.get('assets', {}).get('video')
                if not video_obj:
                    raise LumaAPIError(f"No video in completed generation: {status_data}")
                
                video_url = video_obj.get('url')
                thumbnail_url = status_data.get('assets', {}).get('thumbnail', {}).get('url')
                
                if not video_url:
                    raise LumaAPIError(f"No video URL in assets: {status_data}")
                
                return {
                    "video_url": video_url,
                    "thumbnail_url": thumbnail_url or _generate_thumbnail_url(video_url),
                    "duration": duration,
                    "status": "complete",
                    "engine": "luma",
                    "generation_id": generation_id
                }
            
            elif state == 'failed':
                failure_reason = status_data.get('failure_reason', 'Unknown error')
                raise LumaAPIError(f"Generation failed: {failure_reason}")
            
            # Still processing (queued or processing state)
            time.sleep(5)
        
        raise LumaAPIError(f"Generation timeout after {max_attempts * 5} seconds")
    
    except requests.RequestException as e:
        raise LumaAPIError(f"API request failed: {str(e)}")


def _generate_thumbnail_url(video_url: str) -> str:
    """Generate thumbnail URL from video URL"""
    return video_url.replace('.mp4', '_thumb.jpg')


# Fallback for development/testing
def generate_placeholder(prompt: str, **kwargs) -> Dict[str, Any]:
    """Placeholder response for testing without API key"""
    return {
        "video_url": "https://example.com/luma_video.mp4",
        "thumbnail_url": "https://example.com/luma_thumb.jpg",
        "duration": kwargs.get('duration', 5.0),
        "status": "complete",
        "engine": "luma",
        "generation_id": "placeholder_gen",
        "note": "Placeholder - Set LUMA_API_KEY to use real API"
    }
