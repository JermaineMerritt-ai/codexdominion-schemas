# ============================================================================================
# AUDIO AUTOMATION - Dynamic Parameter Control
# ============================================================================================
"""
Automation engine for dynamic sound control over time.

Supports:
- Volume automation
- Pan automation
- Effect parameter automation
- Send level automation
- Automation curves (linear, exponential, logarithmic, s-curve)
- Point manipulation (add, move, delete)
"""

from typing import List, Dict, Any, Optional
import math


class AudioAutomationEngine:
    """Complete automation system for dynamic parameter control."""
    
    def __init__(self, db):
        """Initialize automation engine."""
        self.db = db
    
    # ========== AUTOMATION CREATION ==========
    
    def create_automation(
        self,
        project_id: int,
        automation_type: str,
        track_id: Optional[int] = None,
        clip_id: Optional[int] = None,
        initial_points: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Create new automation lane.
        
        Args:
            project_id: Project ID
            automation_type: volume, pan, reverb_send, delay_send, filter_cutoff, eq_band_1, etc.
            track_id: Track ID (for track automation)
            clip_id: Clip ID (for clip automation)
            initial_points: Initial automation points [{time, value, curve}]
        """
        from flask_dashboard import AudioAutomation
        
        if initial_points is None:
            # Default: flat line at default value
            default_values = {
                "volume": 1.0,
                "pan": 0.0,
                "reverb_send": 0.0,
                "delay_send": 0.0
            }
            initial_points = [
                {"time": 0.0, "value": default_values.get(automation_type, 0.5), "curve": "linear"}
            ]
        
        automation = AudioAutomation(
            project_id=project_id,
            track_id=track_id,
            clip_id=clip_id,
            automation_type=automation_type,
            points=initial_points,
            default_curve="linear"
        )
        
        self.db.session.add(automation)
        self.db.session.commit()
        
        return {
            "success": True,
            "automation_id": automation.id,
            "automation_type": automation_type,
            "points": initial_points
        }
    
    # ========== POINT MANIPULATION ==========
    
    def add_point(
        self,
        automation_id: int,
        time: float,
        value: float,
        curve: str = "linear"
    ) -> Dict[str, Any]:
        """Add automation point."""
        from flask_dashboard import AudioAutomation
        
        automation = AudioAutomation.query.get(automation_id)
        if not automation:
            return {"success": False, "error": "Automation not found"}
        
        if automation.is_locked:
            return {"success": False, "error": "Automation is locked"}
        
        points = automation.points if automation.points else []
        
        # Insert point in time-sorted order
        new_point = {"time": time, "value": value, "curve": curve}
        insert_index = 0
        for i, point in enumerate(points):
            if point["time"] > time:
                insert_index = i
                break
            insert_index = i + 1
        
        points.insert(insert_index, new_point)
        automation.points = points
        
        self.db.session.commit()
        
        return {
            "success": True,
            "automation_id": automation_id,
            "point_index": insert_index,
            "point": new_point,
            "total_points": len(points)
        }
    
    def move_point(
        self,
        automation_id: int,
        point_index: int,
        new_time: Optional[float] = None,
        new_value: Optional[float] = None
    ) -> Dict[str, Any]:
        """Move an automation point."""
        from flask_dashboard import AudioAutomation
        
        automation = AudioAutomation.query.get(automation_id)
        if not automation:
            return {"success": False, "error": "Automation not found"}
        
        if automation.is_locked:
            return {"success": False, "error": "Automation is locked"}
        
        points = automation.points if automation.points else []
        
        if point_index < 0 or point_index >= len(points):
            return {"success": False, "error": "Invalid point index"}
        
        if new_time is not None:
            points[point_index]["time"] = new_time
        if new_value is not None:
            points[point_index]["value"] = new_value
        
        # Re-sort points by time
        points.sort(key=lambda p: p["time"])
        automation.points = points
        
        self.db.session.commit()
        
        return {
            "success": True,
            "automation_id": automation_id,
            "point": points[point_index]
        }
    
    def delete_point(
        self,
        automation_id: int,
        point_index: int
    ) -> Dict[str, Any]:
        """Delete automation point."""
        from flask_dashboard import AudioAutomation
        
        automation = AudioAutomation.query.get(automation_id)
        if not automation:
            return {"success": False, "error": "Automation not found"}
        
        if automation.is_locked:
            return {"success": False, "error": "Automation is locked"}
        
        points = automation.points if automation.points else []
        
        if point_index < 0 or point_index >= len(points):
            return {"success": False, "error": "Invalid point index"}
        
        if len(points) == 1:
            return {"success": False, "error": "Cannot delete last point"}
        
        del points[point_index]
        automation.points = points
        
        self.db.session.commit()
        
        return {
            "success": True,
            "automation_id": automation_id,
            "remaining_points": len(points)
        }
    
    # ========== AUTOMATION CURVES ==========
    
    def interpolate_value(
        self,
        time: float,
        point1: Dict,
        point2: Dict,
        curve_type: str = "linear"
    ) -> float:
        """Interpolate value between two points using specified curve.
        
        Args:
            time: Time to interpolate at
            point1: Start point {time, value, curve}
            point2: End point {time, value, curve}
            curve_type: linear, exponential, logarithmic, s-curve, step
        
        Returns:
            Interpolated value
        """
        t1, v1 = point1["time"], point1["value"]
        t2, v2 = point2["time"], point2["value"]
        
        if time <= t1:
            return v1
        if time >= t2:
            return v2
        
        # Normalize time to 0..1
        t = (time - t1) / (t2 - t1)
        
        if curve_type == "linear":
            return v1 + (v2 - v1) * t
        
        elif curve_type == "exponential":
            # Exponential curve (accelerating)
            t_exp = t * t
            return v1 + (v2 - v1) * t_exp
        
        elif curve_type == "logarithmic":
            # Logarithmic curve (decelerating)
            t_log = math.sqrt(t)
            return v1 + (v2 - v1) * t_log
        
        elif curve_type == "s-curve":
            # S-curve (ease in/out)
            t_s = (1 - math.cos(t * math.pi)) / 2
            return v1 + (v2 - v1) * t_s
        
        elif curve_type == "step":
            # Step (instant change at midpoint)
            return v1 if t < 0.5 else v2
        
        else:
            return v1 + (v2 - v1) * t
    
    def get_value_at_time(
        self,
        automation_id: int,
        time: float
    ) -> Optional[float]:
        """Get automation value at specific time."""
        from flask_dashboard import AudioAutomation
        
        automation = AudioAutomation.query.get(automation_id)
        if not automation or not automation.points:
            return None
        
        points = automation.points
        
        # Before first point
        if time <= points[0]["time"]:
            return points[0]["value"]
        
        # After last point
        if time >= points[-1]["time"]:
            return points[-1]["value"]
        
        # Find surrounding points
        for i in range(len(points) - 1):
            if points[i]["time"] <= time <= points[i + 1]["time"]:
                curve = points[i].get("curve", automation.default_curve)
                return self.interpolate_value(time, points[i], points[i + 1], curve)
        
        return points[-1]["value"]
    
    # ========== AUTOMATION QUERIES ==========
    
    def get_automation(
        self,
        project_id: int,
        automation_type: Optional[str] = None,
        track_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get automation lanes for project."""
        from flask_dashboard import AudioAutomation
        
        query = AudioAutomation.query.filter_by(project_id=project_id)
        
        if automation_type:
            query = query.filter_by(automation_type=automation_type)
        if track_id is not None:
            query = query.filter_by(track_id=track_id)
        
        automations = query.all()
        
        return [{
            "id": a.id,
            "automation_type": a.automation_type,
            "track_id": a.track_id,
            "clip_id": a.clip_id,
            "points": a.points,
            "default_curve": a.default_curve,
            "is_locked": a.is_locked,
            "is_visible": a.is_visible
        } for a in automations]
