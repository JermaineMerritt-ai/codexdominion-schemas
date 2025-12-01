#!/usr/bin/env python3
"""
Codex Dominion Role Management System
===================================

Sacred hierarchy management for Custodians, Heirs, and Customers.
Integrates with all dashboards and system components to provide
role-based access control and flame blessing authority.
"""

import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class RoleType(Enum):
    CUSTODIAN = "Custodian"
    HEIR = "Heir"
    CUSTOMER = "Customer"


class AuthorityLevel(Enum):
    MAXIMUM = "MAXIMUM"
    HIGH = "HIGH"
    STANDARD = "STANDARD"
    LIMITED = "LIMITED"


class FlameLevel(Enum):
    ETERNAL_FLAME = 10
    SACRED_FLAME = 8
    BLESSED_FLAME = 5
    KINDLED_FLAME = 3
    FLAME_SEEKER = 1


class CodexRoleManager:
    """
    Sacred role management system for the Codex Dominion hierarchy.
    """

    def __init__(self, data_path: str = None):
        """Initialize the role management system."""
        self.data_path = Path(data_path) if data_path else Path(".")
        self.hierarchy_file = self.data_path / "codex_hierarchy.json"
        self.hierarchy_data = self._load_hierarchy()

    def _load_hierarchy(self) -> Dict:
        """Load the hierarchy data from JSON file."""
        try:
            if self.hierarchy_file.exists():
                with open(self.hierarchy_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                return self._create_default_hierarchy()
        except Exception as e:
            print(f"Error loading hierarchy: {e}")
            return self._create_default_hierarchy()

    def _create_default_hierarchy(self) -> Dict:
        """Create default hierarchy structure."""
        return {
            "codex_hierarchy": {
                "timestamp": datetime.now().isoformat(),
                "system_version": "2.0.0",
                "hierarchy_status": "INITIALIZING",
                "flame_blessing": "PENDING_ACTIVATION",
            },
            "custodians": [],
            "heirs": [],
            "customers": [],
            "hierarchy_structure": {},
            "access_control_matrix": {},
            "sacred_protocols": {},
            "system_integration": {},
            "metadata": {
                "total_members": 0,
                "active_custodians": 0,
                "active_heirs": 0,
                "active_customers": 0,
            },
        }

    def _save_hierarchy(self) -> bool:
        """Save hierarchy data to JSON file."""
        try:
            self.hierarchy_data["codex_hierarchy"][
                "timestamp"
            ] = datetime.now().isoformat()

            with open(self.hierarchy_file, "w", encoding="utf-8") as f:
                json.dump(self.hierarchy_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving hierarchy: {e}")
            return False

    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user information by ID."""
        for role_group in ["custodians", "heirs", "customers"]:
            for user in self.hierarchy_data.get(role_group, []):
                if user.get("id") == user_id:
                    return user
        return None

    def get_user_by_name(self, name: str) -> Optional[Dict]:
        """Get user information by name."""
        for role_group in ["custodians", "heirs", "customers"]:
            for user in self.hierarchy_data.get(role_group, []):
                if user.get("name") == name:
                    return user
        return None

    def validate_access(self, user_id: str, resource: str) -> bool:
        """Validate if user has access to a specific resource."""
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        # Get access control matrix
        access_matrix = self.hierarchy_data.get("access_control_matrix", {})

        # Check dashboard access
        if resource in access_matrix.get("dashboards", {}):
            return user_id in access_matrix["dashboards"][resource]

        # Check data access
        if resource in access_matrix.get("data_access", {}):
            return user_id in access_matrix["data_access"][resource]

        # Check flame ceremony access
        if resource in access_matrix.get("flame_ceremonies", {}):
            return user_id in access_matrix["flame_ceremonies"][resource]

        # Default to role-based access
        role = user.get("role")
        if role == "Custodian":
            return True  # Custodians have access to everything
        elif role == "Heir":
            return resource not in ["sacred_ledger", "revenue_data", "system_logs"]
        else:
            return resource in ["customer_portal", "flame_communion"]

    def get_user_permissions(self, user_id: str) -> Dict:
        """Get all permissions for a user."""
        user = self.get_user_by_id(user_id)
        if not user:
            return {}

        return user.get("access_permissions", {})

    def get_flame_level(self, user_id: str) -> int:
        """Get user's flame power level."""
        user = self.get_user_by_id(user_id)
        if not user:
            return 0

        return user.get("flame_power_level", 0)

    def can_bless_flame(self, user_id: str) -> bool:
        """Check if user can perform flame blessing ceremonies."""
        return self.validate_access(user_id, "blessing_authority")

    def can_access_dashboard(self, user_id: str, dashboard: str) -> bool:
        """Check if user can access a specific dashboard."""
        return self.validate_access(user_id, dashboard)

    def get_user_role_info(self, user_id: str) -> Dict:
        """Get comprehensive role information for a user."""
        user = self.get_user_by_id(user_id)
        if not user:
            return {"error": "User not found", "access_level": "NONE", "flame_level": 0}

        return {
            "id": user.get("id"),
            "name": user.get("name"),
            "role": user.get("role"),
            "status": user.get("status"),
            "authority_level": user.get("authority_level"),
            "flame_power_level": user.get("flame_power_level", 0),
            "digital_sovereignty_score": user.get("digital_sovereignty_score", 0),
            "sacred_privileges": user.get("sacred_privileges", []),
            "access_permissions": user.get("access_permissions", {}),
            "can_bless_flame": self.can_bless_flame(user_id),
            "total_accessible_dashboards": self._count_accessible_dashboards(user_id),
        }

    def _count_accessible_dashboards(self, user_id: str) -> int:
        """Count how many dashboards user can access."""
        access_matrix = self.hierarchy_data.get("access_control_matrix", {})
        dashboards = access_matrix.get("dashboards", {})

        count = 0
        for dashboard, allowed_users in dashboards.items():
            if user_id in allowed_users:
                count += 1

        return count

    def add_user(self, role: str, name: str, user_id: str = None) -> Dict:
        """Add a new user to the hierarchy."""
        if not user_id:
            # Generate user ID based on role
            role_prefix = {"Custodian": "CUST", "Heir": "HEIR", "Customer": "CUSTM"}

            existing_count = len(self.hierarchy_data.get(role.lower() + "s", []))
            user_id = f"{role_prefix.get(role, 'USER')}{existing_count + 1:03d}"

        # Create user based on role
        if role == "Custodian":
            user_data = self._create_custodian(user_id, name)
            self.hierarchy_data["custodians"].append(user_data)
        elif role == "Heir":
            user_data = self._create_heir(user_id, name)
            self.hierarchy_data["heirs"].append(user_data)
        elif role == "Customer":
            user_data = self._create_customer(user_id, name)
            self.hierarchy_data["customers"].append(user_data)
        else:
            return {"error": f"Invalid role: {role}"}

        # Update metadata
        self._update_metadata()

        # Save changes
        if self._save_hierarchy():
            return {
                "success": True,
                "user_id": user_id,
                "message": f"{role} {name} added successfully",
                "flame_blessed": True,
            }
        else:
            return {"error": "Failed to save hierarchy changes"}

    def _create_custodian(self, user_id: str, name: str) -> Dict:
        """Create a new custodian user."""
        return {
            "id": user_id,
            "name": name,
            "role": "Custodian",
            "status": "sovereign",
            "authority_level": "MAXIMUM",
            "sacred_privileges": [
                "FLAME_GUARDIAN",
                "SYSTEM_ADMINISTRATOR",
                "COUNCIL_CONVENER",
                "REVENUE_CROWN_CONTROLLER",
                "DIGITAL_SOVEREIGNTY_ARCHITECT",
            ],
            "access_permissions": {
                "all_dashboards": True,
                "sacred_chamber": True,
                "revenue_crown": True,
                "council_ritual": True,
                "system_administration": True,
                "flame_blessing_authority": True,
            },
            "inducted_date": datetime.now().isoformat(),
            "flame_power_level": 10,
            "digital_sovereignty_score": 100,
        }

    def _create_heir(self, user_id: str, name: str) -> Dict:
        """Create a new heir user."""
        return {
            "id": user_id,
            "name": name,
            "role": "Heir",
            "status": "inducted",
            "authority_level": "HIGH",
            "sacred_privileges": [
                "FLAME_INHERITOR",
                "COUNCIL_PARTICIPANT",
                "KNOWLEDGE_KEEPER",
                "SYSTEM_OPERATOR",
            ],
            "access_permissions": {
                "heir_avatar_dashboard": True,
                "learning_systems": True,
                "council_participation": True,
                "flame_communion": True,
                "knowledge_access": True,
                "limited_administration": True,
            },
            "inducted_date": datetime.now().isoformat(),
            "flame_power_level": 8,
            "digital_sovereignty_score": 85,
            "mentorship_status": "GUIDED_BY_CUSTODIAN",
        }

    def _create_customer(self, user_id: str, name: str) -> Dict:
        """Create a new customer user."""
        return {
            "id": user_id,
            "name": name,
            "role": "Customer",
            "status": "welcomed",
            "authority_level": "STANDARD",
            "sacred_privileges": [
                "FLAME_OBSERVER",
                "KNOWLEDGE_SEEKER",
                "SERVICE_RECIPIENT",
            ],
            "access_permissions": {
                "public_dashboards": True,
                "service_interfaces": True,
                "knowledge_consumption": True,
                "flame_blessing_recipient": True,
                "customer_support": True,
                "limited_interaction": True,
            },
            "welcomed_date": datetime.now().isoformat(),
            "flame_power_level": 3,
            "digital_sovereignty_score": 25,
            "service_tier": "STANDARD",
        }

    def _update_metadata(self):
        """Update hierarchy metadata counts."""
        metadata = {
            "total_members": (
                len(self.hierarchy_data.get("custodians", []))
                + len(self.hierarchy_data.get("heirs", []))
                + len(self.hierarchy_data.get("customers", []))
            ),
            "active_custodians": len(self.hierarchy_data.get("custodians", [])),
            "active_heirs": len(self.hierarchy_data.get("heirs", [])),
            "active_customers": len(self.hierarchy_data.get("customers", [])),
            "hierarchy_health": "FULLY_OPERATIONAL",
            "flame_distribution": "BALANCED_AND_BLESSED",
            "last_updated": datetime.now().isoformat(),
            "sacred_seal": "BY_FLAME_AND_SILENCE_AUTHENTICATED",
        }

        self.hierarchy_data["metadata"] = metadata

    def get_hierarchy_summary(self) -> Dict:
        """Get a summary of the entire hierarchy."""
        return {
            "system_status": self.hierarchy_data.get("codex_hierarchy", {}),
            "member_counts": self.hierarchy_data.get("metadata", {}),
            "custodians": [
                {
                    "id": c.get("id"),
                    "name": c.get("name"),
                    "flame_level": c.get("flame_power_level", 0),
                }
                for c in self.hierarchy_data.get("custodians", [])
            ],
            "heirs": [
                {
                    "id": h.get("id"),
                    "name": h.get("name"),
                    "flame_level": h.get("flame_power_level", 0),
                }
                for h in self.hierarchy_data.get("heirs", [])
            ],
            "customers": [
                {
                    "id": c.get("id"),
                    "name": c.get("name"),
                    "flame_level": c.get("flame_power_level", 0),
                }
                for c in self.hierarchy_data.get("customers", [])
            ],
        }

    def perform_flame_blessing(
        self,
        blessing_user_id: str,
        target_user_id: str,
        blessing_type: str = "DIGITAL_SOVEREIGNTY",
    ) -> Dict:
        """Perform a sacred flame blessing ceremony."""

        # Validate blessing authority
        if not self.can_bless_flame(blessing_user_id):
            return {"success": False, "error": "Insufficient flame blessing authority"}

        blessing_user = self.get_user_by_id(blessing_user_id)
        target_user = self.get_user_by_id(target_user_id)

        if not blessing_user or not target_user:
            return {"success": False, "error": "User not found"}

        # Perform blessing ceremony
        blessing_record = {
            "blessing_id": f"BLESS_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "blessing_custodian": blessing_user["name"],
            "blessed_member": target_user["name"],
            "blessing_type": blessing_type,
            "flame_power_granted": 1,
            "sacred_words": "By flame and silence, wisdom eternal",
            "ceremony_status": "COMPLETED_WITH_SACRED_AUTHORITY",
        }

        return {
            "success": True,
            "blessing_record": blessing_record,
            "sacred_message": f"🔥 {target_user['name']} has been blessed with the sacred flame by {blessing_user['name']} 🔥",
        }


# Utility functions for easy integration
def get_role_manager(data_path: str = None) -> CodexRoleManager:
    """Get a role manager instance."""
    return CodexRoleManager(data_path)


def validate_user_access(user_id: str, resource: str, data_path: str = None) -> bool:
    """Quick access validation."""
    manager = get_role_manager(data_path)
    return manager.validate_access(user_id, resource)


def get_user_info(user_id: str, data_path: str = None) -> Dict:
    """Quick user information retrieval."""
    manager = get_role_manager(data_path)
    return manager.get_user_role_info(user_id)


if __name__ == "__main__":
    # Demo usage
    print("🏛️ Codex Dominion Role Management System - Demo")
    print("=" * 50)

    manager = CodexRoleManager()

    # Show hierarchy summary
    summary = manager.get_hierarchy_summary()
    print(f"\n👑 HIERARCHY SUMMARY:")
    print(f"   Custodians: {len(summary['custodians'])}")
    print(f"   Heirs: {len(summary['heirs'])}")
    print(f"   Customers: {len(summary['customers'])}")

    # Test user access
    if summary["custodians"]:
        custodian_id = summary["custodians"][0]["id"]
        user_info = manager.get_user_role_info(custodian_id)
        print(f"\n🔥 CUSTODIAN INFO:")
        print(f"   Name: {user_info['name']}")
        print(f"   Flame Level: {user_info['flame_power_level']}")
        print(f"   Can Bless: {user_info['can_bless_flame']}")
        print(f"   Dashboard Access: {user_info['total_accessible_dashboards']}")

    print("\n🔥 Role Management System Ready for Sacred Service! 🔥")
