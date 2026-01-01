"""
Council Engine - Governance and oversight management for Codex Dominion
Implements Council Seal architecture for policy enforcement and agent coordination.
"""

import json
import uuid
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path


@dataclass
class CouncilOversight:
    """Oversight configuration for a council."""
    review_actions: bool
    review_threshold_weekly_savings: float
    blocked_action_types: List[str] = field(default_factory=list)


@dataclass
class Council:
    """Represents a governance council in the Codex Dominion system."""
    id: str
    name: str
    purpose: str
    primary_engines: List[str]
    agents: List[str]
    domains: List[str]
    oversight: CouncilOversight
    status: str = "active"
    created_at: str = ""
    updated_at: str = ""
    
    def __post_init__(self):
        """Initialize timestamps if not provided."""
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat() + "Z"
        if not self.updated_at:
            self.updated_at = datetime.utcnow().isoformat() + "Z"


class CouncilEngine:
    """
    Manages councils, their oversight, and policy enforcement.
    Integrates with workflow engine and agent systems.
    """
    
    def __init__(self, councils_file: str = "councils.json"):
        """Initialize council engine with JSON storage."""
        self.councils_file = Path(councils_file)
        self.councils: Dict[str, Council] = {}
        self._load_councils()
    
    def _load_councils(self):
        """Load councils from JSON file."""
        if not self.councils_file.exists():
            self._initialize_councils_file()
            return
        
        try:
            with open(self.councils_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for council_data in data.get("councils", []):
                oversight_data = council_data.get("oversight", {})
                oversight = CouncilOversight(
                    review_actions=oversight_data.get("review_actions", True),
                    review_threshold_weekly_savings=oversight_data.get("review_threshold_weekly_savings", 5000),
                    blocked_action_types=oversight_data.get("blocked_action_types", [])
                )
                
                council = Council(
                    id=council_data["id"],
                    name=council_data["name"],
                    purpose=council_data["purpose"],
                    primary_engines=council_data.get("primary_engines", []),
                    agents=council_data.get("agents", []),
                    domains=council_data.get("domains", []),
                    oversight=oversight,
                    status=council_data.get("status", "active"),
                    created_at=council_data.get("created_at", ""),
                    updated_at=council_data.get("updated_at", "")
                )
                self.councils[council.id] = council
                
        except Exception as e:
            print(f"Error loading councils: {e}")
            self._initialize_councils_file()
    
    def _initialize_councils_file(self):
        """Create initial councils file with default structure."""
        data = {
            "councils": [],
            "meta": {
                "version": "1.0.0",
                "last_updated": datetime.utcnow().isoformat() + "Z",
                "total_councils": 0
            }
        }
        self._save_councils_data(data)
    
    def _save_councils_data(self, data: Dict[str, Any]):
        """Save councils data to JSON file."""
        with open(self.councils_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _save_councils(self):
        """Save all councils to JSON file."""
        councils_list = []
        for council in self.councils.values():
            council_dict = {
                "id": council.id,
                "name": council.name,
                "purpose": council.purpose,
                "primary_engines": council.primary_engines,
                "agents": council.agents,
                "domains": council.domains,
                "oversight": {
                    "review_actions": council.oversight.review_actions,
                    "review_threshold_weekly_savings": council.oversight.review_threshold_weekly_savings,
                    "blocked_action_types": council.oversight.blocked_action_types
                },
                "status": council.status,
                "created_at": council.created_at,
                "updated_at": council.updated_at
            }
            councils_list.append(council_dict)
        
        data = {
            "councils": councils_list,
            "meta": {
                "version": "1.0.0",
                "last_updated": datetime.utcnow().isoformat() + "Z",
                "total_councils": len(councils_list)
            }
        }
        self._save_councils_data(data)
    
    def create_council(
        self,
        name: str,
        purpose: str,
        primary_engines: List[str],
        agents: List[str],
        domains: List[str],
        oversight: CouncilOversight,
        council_id: Optional[str] = None
    ) -> Council:
        """Create a new council."""
        if council_id is None:
            council_id = f"council_{name.lower().replace(' ', '_')}"
        
        if council_id in self.councils:
            raise ValueError(f"Council with ID {council_id} already exists")
        
        council = Council(
            id=council_id,
            name=name,
            purpose=purpose,
            primary_engines=primary_engines,
            agents=agents,
            domains=domains,
            oversight=oversight,
            status="active"
        )
        
        self.councils[council_id] = council
        self._save_councils()
        return council
    
    def get_council(self, council_id: str) -> Optional[Council]:
        """Get a council by ID."""
        return self.councils.get(council_id)
    
    def list_councils(self, status: Optional[str] = None) -> List[Council]:
        """List all councils, optionally filtered by status."""
        councils = list(self.councils.values())
        if status:
            councils = [c for c in councils if c.status == status]
        return councils
    
    def update_council(self, council_id: str, **updates) -> Optional[Council]:
        """Update council properties."""
        council = self.councils.get(council_id)
        if not council:
            return None
        
        for key, value in updates.items():
            if hasattr(council, key):
                setattr(council, key, value)
        
        council.updated_at = datetime.utcnow().isoformat() + "Z"
        self._save_councils()
        return council
    
    def delete_council(self, council_id: str) -> bool:
        """Delete a council."""
        if council_id in self.councils:
            del self.councils[council_id]
            self._save_councils()
            return True
        return False
    
    def check_action_allowed(self, action_type: str, council_id: str) -> bool:
        """Check if an action type is allowed by a council's oversight."""
        council = self.councils.get(council_id)
        if not council:
            return True  # Default to allow if council not found
        
        return action_type not in council.oversight.blocked_action_types
    
    def requires_review(self, weekly_savings: float, council_id: str) -> bool:
        """Check if an action requires council review based on savings threshold."""
        council = self.councils.get(council_id)
        if not council or not council.oversight.review_actions:
            return False
        
        return weekly_savings >= council.oversight.review_threshold_weekly_savings
    
    def get_councils_by_agent(self, agent_id: str) -> List[Council]:
        """Get all councils that include a specific agent."""
        return [c for c in self.councils.values() if agent_id in c.agents]
    
    def get_councils_by_domain(self, domain: str) -> List[Council]:
        """Get all councils that oversee a specific domain."""
        return [c for c in self.councils.values() if domain in c.domains]
    
    def get_council_by_domain(self, domain: str) -> Optional[Council]:
        """Get the first council that oversees a specific domain."""
        for council in self.councils.values():
            if domain in council.domains:
                return council
        return None
    
    def council_allows_action(
        self, 
        council_id: str, 
        action_type: str, 
        savings: Optional[Dict[str, float]] = None
    ) -> bool:
        """
        Combined check: action allowed AND doesn't require review.
        Returns False if action is blocked OR requires manual review.
        
        Args:
            council_id: Council ID to check
            action_type: Type of action to validate
            savings: Optional dict with savings metrics (weekly_savings, total_weekly_savings)
        
        Returns:
            True if action is allowed and doesn't require review, False otherwise
        """
        council = self.councils.get(council_id)
        if not council:
            return True  # Default to allow if council not found
        
        # Check if action type is blocked
        if action_type in council.oversight.blocked_action_types:
            return False
        
        # Check if requires review based on savings threshold
        if savings and council.oversight.review_actions:
            weekly = savings.get("weekly_savings") or savings.get("total_weekly_savings") or 0
            if weekly >= council.oversight.review_threshold_weekly_savings:
                # Requires manual review - return False
                return False
        
        return True
    
    def add_agent_to_council(self, council_id: str, agent_id: str) -> bool:
        """Add an agent to a council."""
        council = self.councils.get(council_id)
        if not council:
            return False
        
        if agent_id not in council.agents:
            council.agents.append(agent_id)
            council.updated_at = datetime.utcnow().isoformat() + "Z"
            self._save_councils()
        return True
    
    def remove_agent_from_council(self, council_id: str, agent_id: str) -> bool:
        """Remove an agent from a council."""
        council = self.councils.get(council_id)
        if not council:
            return False
        
        if agent_id in council.agents:
            council.agents.remove(agent_id)
            council.updated_at = datetime.utcnow().isoformat() + "Z"
            self._save_councils()
        return True


# Global singleton instance
council_engine = CouncilEngine()


# ==================== UTILITY FUNCTIONS ====================

def get_council_by_domain(domain: str) -> Optional[Dict[str, Any]]:
    """
    Utility function: Get first council by domain (returns dict, not Council object).
    Useful for quick JSON-based lookups without full engine initialization.
    """
    councils_file = Path("councils.json")
    if not councils_file.exists():
        return None
    
    try:
        with open(councils_file, 'r', encoding='utf-8') as f:
            councils_json = json.load(f)
        
        for council in councils_json.get("councils", []):
            if domain in council.get("domains", []):
                return council
    except Exception:
        pass
    
    return None


def council_allows_action(council: Dict[str, Any], action_type: str, savings: Optional[Dict[str, float]] = None) -> bool:
    """
    Utility function: Check if council allows an action (combined blocked + review check).
    Returns False if action is blocked OR requires manual review.
    
    Args:
        council: Council dict (from JSON)
        action_type: Type of action to validate
        savings: Optional dict with savings metrics (weekly_savings, total_weekly_savings)
    
    Returns:
        True if action is allowed and doesn't require review, False otherwise
    """
    if not council:
        return True
    
    oversight = council.get("oversight", {})
    
    # Check if action type is blocked
    blocked = oversight.get("blocked_action_types", [])
    if action_type in blocked:
        return False
    
    # Check if requires review based on savings threshold
    threshold = oversight.get("review_threshold_weekly_savings")
    if threshold is not None and savings:
        weekly = savings.get("weekly_savings") or savings.get("total_weekly_savings") or 0
        if weekly >= threshold:
            # Requires manual review - return False
            return False
    
    return True
