"""
Runway Gen-3 Video Generation Engine

API Documentation: https://docs.runwayml.com/
Model: Gen-3 Alpha (text-to-video)
"""

import os
import requests
import time
from typing import Dict, Any, Optional


class RunwayAPIError(Exception):
    """Runway API error"""
    pass


def generate(prompt: str, **kwargs) -> Dict[str, Any]:
    """
    Generate video using Runway Gen-3 API.
    
    Args:
        prompt: Text description of the video
        **kwargs: Optional parameters:
            - duration: Video length (seconds, default: 5)
            - resolution: Video resolution (default: "1280x768")
            - motion_scale: Camera motion intensity 0-10 (default: 5)
            - seed: Random seed for reproducibility (optional)
            - model: Model version (default: "gen3a_turbo")
    
    Returns:
        dict: {
            "video_url": "https://storage.googleapis.com/.../video.mp4",
            "thumbnail_url": "https://storage.googleapis.com/.../thumb.jpg",
            "duration": 5.0,
            "status": "complete",
            "engine": "runway",
            "task_id": "abc123..."
        }
    
    Raises:
        RunwayAPIError: If API call fails
    """
    api_key = os.getenv('RUNWAY_API_KEY')
    if not api_key:
        raise RunwayAPIError("RUNWAY_API_KEY not set in environment")
    
    # Extract parameters with defaults
    duration = kwargs.get('duration', 5)
    resolution = kwargs.get('resolution', '1280x768')
    motion_scale = kwargs.get('motion_scale', 5)
    seed = kwargs.get('seed')
    model = kwargs.get('model', 'gen3a_turbo')
    
    # Runway API endpoint
    api_url = "https://api.runwayml.com/v1/generate"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "prompt": prompt,
        "duration": duration,
        "resolution": resolution,
        "motion_scale": motion_scale
    }
    
    if seed is not None:
        payload["seed"] = seed
    
    try:
        # Submit generation request
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        task_id = result.get('id') or result.get('task_id')
        
        if not task_id:
            raise RunwayAPIError(f"No task ID in response: {result}")
        
        # Poll for completion (Runway is async)
        status_url = f"https://api.runwayml.com/v1/tasks/{task_id}"
        max_attempts = 60  # 5 minutes max (5s intervals)
        
        for attempt in range(max_attempts):
            status_response = requests.get(status_url, headers=headers, timeout=30)
            status_response.raise_for_status()
            status_data = status_response.json()
            
            status = status_data.get('status')
            
            if status == 'SUCCEEDED':
                video_url = status_data.get('output', {}).get('url')
                if not video_url:
                    raise RunwayAPIError(f"No video URL in completed task: {status_data}")
                
                return {
                    "video_url": video_url,
                    "thumbnail_url": _generate_thumbnail_url(video_url),
                    "duration": duration,
                    "status": "complete",
                    "engine": "runway",
                    "task_id": task_id
                }
            
            elif status == 'FAILED':
                error_msg = status_data.get('error', 'Unknown error')
                raise RunwayAPIError(f"Generation failed: {error_msg}")
            
            # Still processing - wait and retry
            time.sleep(5)
        
        raise RunwayAPIError(f"Generation timeout after {max_attempts * 5} seconds")
    
    except requests.RequestException as e:
        raise RunwayAPIError(f"API request failed: {str(e)}")


def _generate_thumbnail_url(video_url: str) -> str:
    """Generate thumbnail URL from video URL (Runway usually provides both)"""
    # Runway often provides thumbnail alongside video
    # If not available, you can use a frame extraction service
    return video_url.replace('.mp4', '_thumb.jpg')


# Fallback for development/testing
def generate_placeholder(prompt: str, **kwargs) -> Dict[str, Any]:
    """Placeholder response for testing without API key"""
    return {
        "video_url": "https://example.com/runway_video.mp4",
        "thumbnail_url": "https://example.com/runway_thumb.jpg",
        "duration": kwargs.get('duration', 5.0),
        "status": "complete",
        "engine": "runway",
        "task_id": "placeholder_task",
        "note": "Placeholder - Set RUNWAY_API_KEY to use real API"
    }
