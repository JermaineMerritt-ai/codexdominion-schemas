"""
Scene Flow Engine - Phase 4

Analyzes narrative continuity, pacing, shot progression, and emotional arcs.
Provides intelligent suggestions for scene ordering and transitions.

This is the AI director inside the Dominion.
"""

from typing import List, Dict, Any, Optional
from enum import Enum


class SceneType(Enum):
    """Scene shot types for cinematic structure"""
    WIDE = "wide"                    # Establishing shot
    MEDIUM = "medium"                # Standard conversation
    CLOSE_UP = "close_up"           # Emotional intensity
    EXTREME_CLOSE_UP = "extreme_close_up"  # Detail/tension
    OVER_SHOULDER = "over_shoulder" # Dialogue
    TRACKING = "tracking"           # Motion/follow
    STATIC = "static"               # Fixed camera
    AERIAL = "aerial"               # Drone/overhead
    POV = "pov"                     # Point of view


class Mood(Enum):
    """Emotional tone of scenes"""
    INTENSE = "intense"
    CALM = "calm"
    DRAMATIC = "dramatic"
    MYSTERIOUS = "mysterious"
    JOYFUL = "joyful"
    MELANCHOLY = "melancholy"
    TENSE = "tense"
    PEACEFUL = "peaceful"


class SceneFlowEngine:
    """
    Analyzes scene sequences for narrative continuity and pacing.
    
    Detects issues:
    - Repetitive shots
    - Abrupt transitions
    - Poor pacing
    - Lack of emotional variety
    
    Suggests improvements:
    - Insert transition shots
    - Add establishing shots
    - Vary camera angles
    - Balance emotional rhythm
    """
    
    def __init__(self):
        # Shot progression rules
        self.good_progressions = [
            ['wide', 'medium', 'close_up'],      # Classic progression
            ['wide', 'tracking', 'medium'],      # Movement to interaction
            ['close_up', 'medium', 'wide'],      # Emotional to context
            ['aerial', 'wide', 'medium'],        # Perspective shift
        ]
        
        # Transition compatibility
        self.smooth_transitions = {
            'wide': ['medium', 'tracking', 'aerial'],
            'medium': ['close_up', 'over_shoulder', 'wide'],
            'close_up': ['extreme_close_up', 'medium', 'over_shoulder'],
            'tracking': ['medium', 'wide', 'pov'],
            'static': ['tracking', 'medium'],
            'aerial': ['wide', 'tracking']
        }
    
    def analyze_sequence(self, scenes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze a sequence of scenes for narrative quality.
        
        Args:
            scenes: List of scene dicts with: scene_type, mood, duration, tags, prompt
        
        Returns:
            {
                "quality_score": 0-100,
                "issues": [...],
                "suggestions": [...],
                "continuity_report": {...}
            }
        """
        if len(scenes) < 2:
            return {
                "quality_score": 100,
                "issues": [],
                "suggestions": ["Add more scenes to analyze flow"],
                "continuity_report": {}
            }
        
        issues = []
        suggestions = []
        
        # 1. Check shot variety
        shot_types = [s.get('scene_type', 'medium') for s in scenes]
        if len(set(shot_types)) == 1:
            issues.append({
                "type": "repetitive_shots",
                "severity": "high",
                "message": f"All scenes use {shot_types[0]} shots - lacks visual variety"
            })
            suggestions.append({
                "type": "add_variety",
                "action": "insert_scene",
                "position": len(scenes) // 2,
                "scene_type": self._suggest_contrasting_shot(shot_types[0]),
                "reason": "Break repetition with different camera angle"
            })
        
        # 2. Check transition smoothness
        for i in range(len(scenes) - 1):
            current_type = scenes[i].get('scene_type', 'medium')
            next_type = scenes[i + 1].get('scene_type', 'medium')
            
            if not self._is_smooth_transition(current_type, next_type):
                issues.append({
                    "type": "abrupt_transition",
                    "severity": "medium",
                    "position": i,
                    "message": f"Abrupt transition from {current_type} to {next_type}"
                })
                suggestions.append({
                    "type": "add_bridge",
                    "action": "insert_scene",
                    "position": i + 1,
                    "scene_type": self._suggest_bridge_shot(current_type, next_type),
                    "reason": f"Smooth transition from {current_type} to {next_type}"
                })
        
        # 3. Check emotional pacing
        moods = [s.get('mood', 'calm') for s in scenes]
        mood_issues = self._analyze_emotional_pacing(moods)
        issues.extend(mood_issues['issues'])
        suggestions.extend(mood_issues['suggestions'])
        
        # 4. Check duration pacing
        durations = [s.get('duration', 5) for s in scenes]
        pacing_issues = self._analyze_temporal_pacing(durations)
        issues.extend(pacing_issues['issues'])
        suggestions.extend(pacing_issues['suggestions'])
        
        # 5. Check thematic continuity
        tags_issues = self._analyze_thematic_continuity(scenes)
        issues.extend(tags_issues['issues'])
        suggestions.extend(tags_issues['suggestions'])
        
        # Calculate quality score
        quality_score = 100 - (len(issues) * 10)
        quality_score = max(0, min(100, quality_score))
        
        return {
            "quality_score": quality_score,
            "issues": issues,
            "suggestions": suggestions[:10],  # Top 10 suggestions
            "continuity_report": {
                "shot_variety": len(set(shot_types)) / len(shot_types),
                "mood_variety": len(set(moods)) / len(moods),
                "total_duration": sum(durations),
                "average_shot_length": sum(durations) / len(durations),
                "scene_count": len(scenes)
            }
        }
    
    def suggest_next_scene(self, previous_scenes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Suggest what type of scene should come next for optimal flow.
        
        Args:
            previous_scenes: Recent scenes in sequence
        
        Returns:
            Suggestion dict with scene_type, mood, duration, reasoning
        """
        if not previous_scenes:
            return {
                "scene_type": "wide",
                "mood": "calm",
                "duration": 5,
                "reasoning": "Start with establishing wide shot"
            }
        
        last_scene = previous_scenes[-1]
        last_type = last_scene.get('scene_type', 'medium')
        last_mood = last_scene.get('mood', 'calm')
        
        # Get recent shot types
        recent_types = [s.get('scene_type', 'medium') for s in previous_scenes[-3:]]
        
        # Avoid repetition
        suggested_type = self._suggest_next_shot_type(recent_types, last_type)
        
        # Balance mood
        recent_moods = [s.get('mood', 'calm') for s in previous_scenes[-3:]]
        suggested_mood = self._suggest_balancing_mood(recent_moods)
        
        # Suggest duration based on pacing
        durations = [s.get('duration', 5) for s in previous_scenes[-3:]]
        avg_duration = sum(durations) / len(durations)
        suggested_duration = 5 if avg_duration > 6 else 7  # Balance long/short
        
        return {
            "scene_type": suggested_type,
            "mood": suggested_mood,
            "duration": suggested_duration,
            "reasoning": self._explain_suggestion(suggested_type, suggested_mood, last_scene)
        }
    
    def _is_smooth_transition(self, from_type: str, to_type: str) -> bool:
        """Check if transition between shot types is smooth"""
        smooth_next = self.smooth_transitions.get(from_type, [])
        return to_type in smooth_next
    
    def _suggest_bridge_shot(self, from_type: str, to_type: str) -> str:
        """Suggest a shot type to bridge two incompatible shots"""
        # Use medium as universal bridge
        if from_type == 'wide' and to_type == 'close_up':
            return 'medium'
        if from_type == 'close_up' and to_type == 'aerial':
            return 'wide'
        return 'medium'
    
    def _suggest_contrasting_shot(self, current_type: str) -> str:
        """Suggest opposite shot type for variety"""
        contrasts = {
            'wide': 'close_up',
            'close_up': 'wide',
            'medium': 'extreme_close_up',
            'static': 'tracking',
            'aerial': 'close_up'
        }
        return contrasts.get(current_type, 'medium')
    
    def _analyze_emotional_pacing(self, moods: List[str]) -> Dict[str, List]:
        """Analyze if emotional rhythm is balanced"""
        issues = []
        suggestions = []
        
        # Check for too many high-intensity moods in a row
        intense_moods = ['intense', 'dramatic', 'tense']
        consecutive_intense = 0
        
        for i, mood in enumerate(moods):
            if mood in intense_moods:
                consecutive_intense += 1
                if consecutive_intense >= 3:
                    issues.append({
                        "type": "exhausting_pacing",
                        "severity": "medium",
                        "position": i,
                        "message": f"Three consecutive high-intensity scenes - audience may feel exhausted"
                    })
                    suggestions.append({
                        "type": "reset_rhythm",
                        "action": "insert_scene",
                        "position": i + 1,
                        "mood": "calm",
                        "reason": "Add a quieter moment to reset emotional intensity"
                    })
                    break
            else:
                consecutive_intense = 0
        
        return {"issues": issues, "suggestions": suggestions}
    
    def _analyze_temporal_pacing(self, durations: List[float]) -> Dict[str, List]:
        """Analyze if scene durations create good pacing"""
        issues = []
        suggestions = []
        
        avg_duration = sum(durations) / len(durations)
        
        # Check if all scenes are same length (monotonous)
        if all(abs(d - avg_duration) < 1 for d in durations):
            issues.append({
                "type": "monotonous_pacing",
                "severity": "low",
                "message": "All scenes have similar duration - pacing feels flat"
            })
            suggestions.append({
                "type": "vary_duration",
                "action": "adjust_scene",
                "position": len(durations) // 2,
                "duration": max(3, avg_duration - 2),
                "reason": "Vary duration for dynamic pacing"
            })
        
        return {"issues": issues, "suggestions": suggestions}
    
    def _analyze_thematic_continuity(self, scenes: List[Dict[str, Any]]) -> Dict[str, List]:
        """Analyze thematic coherence via tags"""
        issues = []
        suggestions = []
        
        # Collect all tags
        all_tags = []
        for scene in scenes:
            tags_str = scene.get('tags', '')
            if tags_str:
                all_tags.extend(tags_str.split(','))
        
        # Check for thematic coherence
        unique_tags = set(all_tags)
        if len(unique_tags) > len(scenes) * 2:
            issues.append({
                "type": "thematic_scatter",
                "severity": "low",
                "message": "Many different themes - consider focusing the narrative"
            })
        
        return {"issues": issues, "suggestions": suggestions}
    
    def _suggest_next_shot_type(self, recent_types: List[str], last_type: str) -> str:
        """Suggest next shot type based on recent progression"""
        # Avoid repetition
        if len(set(recent_types)) == 1:
            return self._suggest_contrasting_shot(last_type)
        
        # Use smooth transition rules
        smooth_next = self.smooth_transitions.get(last_type, ['medium'])
        return smooth_next[0]
    
    def _suggest_balancing_mood(self, recent_moods: List[str]) -> str:
        """Suggest mood that balances recent emotional tone"""
        intense_moods = ['intense', 'dramatic', 'tense']
        calm_moods = ['calm', 'peaceful', 'joyful']
        
        recent_intense = sum(1 for m in recent_moods if m in intense_moods)
        
        if recent_intense >= 2:
            return 'calm'
        else:
            return 'dramatic'
    
    def _explain_suggestion(self, suggested_type: str, suggested_mood: str, last_scene: Dict) -> str:
        """Generate human-readable explanation for suggestion"""
        last_type = last_scene.get('scene_type', 'medium')
        
        explanations = {
            'wide': "Establish context and spatial relationships",
            'close_up': "Increase emotional intensity and focus",
            'medium': "Balance between detail and context",
            'tracking': "Add dynamic movement and energy"
        }
        
        base = explanations.get(suggested_type, "Continue the narrative flow")
        return f"{base}. Follows {last_type} shot for smooth progression."
