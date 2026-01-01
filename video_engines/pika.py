"""
Pika Labs Video Generation Engine

API Documentation: https://docs.pika.art/
Model: Pika 1.0 (text-to-video, image-to-video)
"""

import os
import requests
import time
from typing import Dict, Any, Optional


class PikaAPIError(Exception):
    """Pika API error"""
    pass


def generate(prompt: str, **kwargs) -> Dict[str, Any]:
    """
    Generate video using Pika Labs API.
    
    Args:
        prompt: Text description of the video
        **kwargs: Optional parameters:
            - duration: Video length (seconds, 3 or 6, default: 3)
            - aspect_ratio: "16:9", "9:16", "1:1" (default: "16:9")
            - motion: Motion intensity 1-4 (default: 2)
            - guidance_scale: Prompt adherence 1-20 (default: 12)
            - seed: Random seed (optional)
            - image_url: Starting image for image-to-video (optional)
    
    Returns:
        dict: {
            "video_url": "https://cdn.pika.art/.../video.mp4",
            "thumbnail_url": "https://cdn.pika.art/.../thumb.jpg",
            "duration": 3.0,
            "status": "complete",
            "engine": "pika",
            "job_id": "xyz789..."
        }
    
    Raises:
        PikaAPIError: If API call fails
    """
    api_key = os.getenv('PIKA_API_KEY')
    if not api_key:
        raise PikaAPIError("PIKA_API_KEY not set in environment")
    
    # Extract parameters with defaults
    duration = kwargs.get('duration', 3)
    aspect_ratio = kwargs.get('aspect_ratio', '16:9')
    motion = kwargs.get('motion', 2)
    guidance_scale = kwargs.get('guidance_scale', 12)
    seed = kwargs.get('seed')
    image_url = kwargs.get('image_url')
    
    # Validate duration (Pika supports 3s or 6s)
    if duration not in [3, 6]:
        duration = 3
    
    # Pika API endpoint
    api_url = "https://api.pika.art/v1/generate"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "duration": duration,
        "aspect_ratio": aspect_ratio,
        "motion": motion,
        "guidance_scale": guidance_scale
    }
    
    if seed is not None:
        payload["seed"] = seed
    
    if image_url:
        payload["image_url"] = image_url
    
    try:
        # Submit generation request
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        job_id = result.get('job_id') or result.get('id')
        
        if not job_id:
            raise PikaAPIError(f"No job ID in response: {result}")
        
        # Poll for completion
        status_url = f"https://api.pika.art/v1/jobs/{job_id}"
        max_attempts = 40  # ~3 minutes max (5s intervals)
        
        for attempt in range(max_attempts):
            status_response = requests.get(status_url, headers=headers, timeout=30)
            status_response.raise_for_status()
            status_data = status_response.json()
            
            status = status_data.get('status')
            
            if status == 'completed':
                video_url = status_data.get('video_url') or status_data.get('result', {}).get('url')
                if not video_url:
                    raise PikaAPIError(f"No video URL in completed job: {status_data}")
                
                thumbnail_url = status_data.get('thumbnail_url') or _generate_thumbnail_url(video_url)
                
                return {
                    "video_url": video_url,
                    "thumbnail_url": thumbnail_url,
                    "duration": duration,
                    "status": "complete",
                    "engine": "pika",
                    "job_id": job_id
                }
            
            elif status == 'failed':
                error_msg = status_data.get('error', 'Unknown error')
                raise PikaAPIError(f"Generation failed: {error_msg}")
            
            # Still processing
            time.sleep(5)
        
        raise PikaAPIError(f"Generation timeout after {max_attempts * 5} seconds")
    
    except requests.RequestException as e:
        raise PikaAPIError(f"API request failed: {str(e)}")


def _generate_thumbnail_url(video_url: str) -> str:
    """Generate thumbnail URL from video URL"""
    return video_url.replace('.mp4', '_thumb.jpg')


# Fallback for development/testing
def generate_placeholder(prompt: str, **kwargs) -> Dict[str, Any]:
    """Placeholder response for testing without API key"""
    return {
        "video_url": "https://example.com/pika_video.mp4",
        "thumbnail_url": "https://example.com/pika_thumb.jpg",
        "duration": kwargs.get('duration', 3.0),
        "status": "complete",
        "engine": "pika",
        "job_id": "placeholder_job",
        "note": "Placeholder - Set PIKA_API_KEY to use real API"
    }
