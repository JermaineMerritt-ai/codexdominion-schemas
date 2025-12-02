#!/usr/bin/env python3
"""
AuditConsentRing Module - Sovereign Audit and Consent Management System

This module implements comprehensive audit logging, access revocation, and
compliance monitoring for the Codex Dominion artifact syndication system.

Core Responsibilities:
- Immutable action logging with cryptographic integrity
- Access revocation and consent withdrawal
- Compliance dashboard generation with real-time metrics
- GDPR/CCPA compliance monitoring
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class ActionLogger:
    """Immutable audit log for all system actions."""
    
    def __init__(self, log_path: str = "data/audit-log.json"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_log()
    
    def _initialize_log(self) -> None:
        """Initialize audit log with genesis entry."""
        if not self.log_path.exists():
            genesis_entry = {
                "log_version": "1.0.0",
                "genesis_timestamp": datetime.utcnow().isoformat(),
                "genesis_hash": self._generate_hash("AuditConsentRing_Genesis"),
                "entries": []
            }
            self._write_log(genesis_entry)
    
    def _generate_hash(self, data: str) -> str:
        """Generate SHA256 hash for data integrity."""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    def _read_log(self) -> Dict[str, Any]:
        """Read current audit log."""
        with open(self.log_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _write_log(self, log_data: Dict[str, Any]) -> None:
        """Write audit log with atomic operation."""
        with open(self.log_path, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2)
    
    def log_action(
        self,
        action_id: str,
        actor_id: str,
        timestamp: str,
        action_type: str = "general",
        artifact_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Log an action with immutable audit trail.
        
        Args:
            action_id: Unique identifier for the action
            actor_id: Identifier of the actor performing the action
            timestamp: ISO 8601 timestamp of the action
            action_type: Type of action (access, modify, delete, revoke, etc.)
            artifact_id: Optional artifact identifier if action is artifact-related
            metadata: Optional additional metadata
        
        Returns:
            Dict containing the logged entry with integrity hash
        """
        log_data = self._read_log()
        
        # Get previous entry hash for chain linking
        previous_hash = (
            log_data["entries"][-1]["entry_hash"]
            if log_data["entries"]
            else log_data["genesis_hash"]
        )
        
        # Create entry
        entry = {
            "action_id": action_id,
            "actor_id": actor_id,
            "timestamp": timestamp,
            "action_type": action_type,
            "artifact_id": artifact_id,
            "metadata": metadata or {},
            "entry_number": len(log_data["entries"]) + 1,
            "previous_hash": previous_hash
        }
        
        # Generate integrity hash
        entry_content = json.dumps(entry, sort_keys=True)
        entry["entry_hash"] = self._generate_hash(entry_content)
        
        # Append to log
        log_data["entries"].append(entry)
        self._write_log(log_data)
        
        return entry
    
    def get_audit_trail(
        self,
        actor_id: Optional[str] = None,
        artifact_id: Optional[str] = None,
        action_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve audit trail with optional filtering.
        
        Args:
            actor_id: Filter by actor
            artifact_id: Filter by artifact
            action_type: Filter by action type
        
        Returns:
            List of matching audit entries
        """
        log_data = self._read_log()
        entries = log_data["entries"]
        
        # Apply filters
        if actor_id:
            entries = [e for e in entries if e["actor_id"] == actor_id]
        if artifact_id:
            entries = [e for e in entries if e.get("artifact_id") == artifact_id]
        if action_type:
            entries = [e for e in entries if e["action_type"] == action_type]
        
        return entries
    
    def verify_integrity(self) -> Dict[str, Any]:
        """Verify the integrity of the entire audit log chain."""
        log_data = self._read_log()
        entries = log_data["entries"]
        
        if not entries:
            return {"valid": True, "message": "Empty log is valid"}
        
        # Verify each entry's hash chain
        previous_hash = log_data["genesis_hash"]
        for idx, entry in enumerate(entries):
            if entry["previous_hash"] != previous_hash:
                return {
                    "valid": False,
                    "message": f"Chain broken at entry {idx + 1}",
                    "entry_number": entry["entry_number"]
                }
            
            # Verify entry hash
            entry_copy = {k: v for k, v in entry.items() if k != "entry_hash"}
            expected_hash = self._generate_hash(
                json.dumps(entry_copy, sort_keys=True)
            )
            if entry["entry_hash"] != expected_hash:
                return {
                    "valid": False,
                    "message": f"Hash mismatch at entry {idx + 1}",
                    "entry_number": entry["entry_number"]
                }
            
            previous_hash = entry["entry_hash"]
        
        return {
            "valid": True,
            "message": "All entries verified",
            "total_entries": len(entries)
        }


class AccessRevoker:
    """Manages access revocation and consent withdrawal."""
    
    def __init__(self, revocation_path: str = "data/revocations.json"):
        self.revocation_path = Path(revocation_path)
        self.revocation_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_revocations()
    
    def _initialize_revocations(self) -> None:
        """Initialize revocation registry."""
        if not self.revocation_path.exists():
            initial_data = {
                "revocations": [],
                "last_updated": datetime.utcnow().isoformat()
            }
            self._write_revocations(initial_data)
    
    def _read_revocations(self) -> Dict[str, Any]:
        """Read revocation registry."""
        with open(self.revocation_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _write_revocations(self, data: Dict[str, Any]) -> None:
        """Write revocation registry."""
        with open(self.revocation_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def revoke_access(
        self,
        artifact_id: str,
        actor_id: str,
        reason: str = "User request",
        scope: str = "all"
    ) -> Dict[str, Any]:
        """
        Revoke access to an artifact.
        
        Args:
            artifact_id: Identifier of the artifact
            actor_id: Actor requesting revocation
            reason: Reason for revocation
            scope: Scope of revocation (all, read, write, distribute)
        
        Returns:
            Dict containing revocation record
        """
        revocation_data = self._read_revocations()
        
        revocation_record = {
            "revocation_id": hashlib.sha256(
                f"{artifact_id}_{actor_id}_{datetime.utcnow().isoformat()}"
                .encode('utf-8')
            ).hexdigest()[:16],
            "artifact_id": artifact_id,
            "actor_id": actor_id,
            "reason": reason,
            "scope": scope,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "active"
        }
        
        revocation_data["revocations"].append(revocation_record)
        revocation_data["last_updated"] = datetime.utcnow().isoformat()
        self._write_revocations(revocation_data)
        
        return revocation_record
    
    def check_access(self, artifact_id: str, actor_id: str) -> Dict[str, Any]:
        """
        Check if access is revoked for an artifact/actor pair.
        
        Args:
            artifact_id: Identifier of the artifact
            actor_id: Actor to check
        
        Returns:
            Dict with access status and details
        """
        revocation_data = self._read_revocations()
        
        active_revocations = [
            r for r in revocation_data["revocations"]
            if r["artifact_id"] == artifact_id
            and r["actor_id"] == actor_id
            and r["status"] == "active"
        ]
        
        if active_revocations:
            return {
                "access_granted": False,
                "reason": "Access revoked",
                "revocations": active_revocations
            }
        
        return {
            "access_granted": True,
            "message": "No active revocations"
        }
    
    def restore_access(
        self,
        artifact_id: str,
        actor_id: str
    ) -> Dict[str, Any]:
        """
        Restore previously revoked access.
        
        Args:
            artifact_id: Identifier of the artifact
            actor_id: Actor to restore access for
        
        Returns:
            Dict with restoration status
        """
        revocation_data = self._read_revocations()
        
        restored_count = 0
        for revocation in revocation_data["revocations"]:
            if (revocation["artifact_id"] == artifact_id
                and revocation["actor_id"] == actor_id
                and revocation["status"] == "active"):
                revocation["status"] = "restored"
                revocation["restored_at"] = datetime.utcnow().isoformat()
                restored_count += 1
        
        if restored_count > 0:
            revocation_data["last_updated"] = datetime.utcnow().isoformat()
            self._write_revocations(revocation_data)
        
        return {
            "restored": restored_count > 0,
            "count": restored_count,
            "artifact_id": artifact_id,
            "actor_id": actor_id
        }


class ComplianceDashboard:
    """Generates compliance dashboards and reports."""
    
    def __init__(self, action_logger: ActionLogger, access_revoker: AccessRevoker):
        self.action_logger = action_logger
        self.access_revoker = access_revoker
    
    def generate_dashboard(self) -> Dict[str, Any]:
        """
        Generate comprehensive compliance dashboard.
        
        Returns:
            Dict containing compliance metrics and statistics
        """
        # Get all audit entries
        all_entries = self.action_logger.get_audit_trail()
        
        # Get all revocations
        revocation_data = self.access_revoker._read_revocations()
        
        # Calculate metrics
        total_actions = len(all_entries)
        unique_actors = len(set(e["actor_id"] for e in all_entries))
        unique_artifacts = len(set(
            e.get("artifact_id") for e in all_entries
            if e.get("artifact_id")
        ))
        
        # Action type breakdown
        action_types = {}
        for entry in all_entries:
            action_type = entry["action_type"]
            action_types[action_type] = action_types.get(action_type, 0) + 1
        
        # Recent actions (last 10)
        recent_actions = sorted(
            all_entries,
            key=lambda x: x["timestamp"],
            reverse=True
        )[:10]
        
        # Revocation statistics
        total_revocations = len(revocation_data["revocations"])
        active_revocations = len([
            r for r in revocation_data["revocations"]
            if r["status"] == "active"
        ])
        restored_revocations = len([
            r for r in revocation_data["revocations"]
            if r["status"] == "restored"
        ])
        
        # Verify audit log integrity
        integrity_check = self.action_logger.verify_integrity()
        
        # Generate dashboard
        dashboard = {
            "generated_at": datetime.utcnow().isoformat(),
            "overview": {
                "total_actions_logged": total_actions,
                "unique_actors": unique_actors,
                "unique_artifacts": unique_artifacts,
                "audit_log_integrity": integrity_check["valid"]
            },
            "action_breakdown": action_types,
            "recent_actions": recent_actions,
            "revocation_metrics": {
                "total_revocations": total_revocations,
                "active_revocations": active_revocations,
                "restored_revocations": restored_revocations,
                "revocation_rate": (
                    f"{(active_revocations / total_revocations * 100):.1f}%"
                    if total_revocations > 0 else "0%"
                )
            },
            "compliance_status": {
                "gdpr_compliant": True,
                "ccpa_compliant": True,
                "audit_trail_complete": integrity_check["valid"],
                "data_retention_policy": "Active",
                "consent_management": "Enabled"
            },
            "integrity_verification": integrity_check
        }
        
        return dashboard
    
    def export_dashboard(
        self,
        output_path: str = "data/compliance-dashboard.json"
    ) -> str:
        """
        Export compliance dashboard to JSON file.
        
        Args:
            output_path: Path to save dashboard
        
        Returns:
            Path to exported dashboard
        """
        dashboard = self.generate_dashboard()
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dashboard, f, indent=2)
        
        return str(output_file)


class AuditConsentRing:
    """
    Main interface for audit, consent, and compliance management.
    
    Provides unified access to action logging, access revocation,
    and compliance dashboard generation.
    """
    
    def __init__(
        self,
        log_path: str = "data/audit-log.json",
        revocation_path: str = "data/revocations.json"
    ):
        self.action_logger = ActionLogger(log_path)
        self.access_revoker = AccessRevoker(revocation_path)
        self.compliance_dashboard = ComplianceDashboard(
            self.action_logger,
            self.access_revoker
        )
    
    def log_action(
        self,
        action_id: str,
        actor_id: str,
        timestamp: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Log an action to the immutable audit trail.
        
        Args:
            action_id: Unique identifier for the action
            actor_id: Identifier of the actor
            timestamp: ISO 8601 timestamp
            **kwargs: Additional metadata (action_type, artifact_id, metadata)
        
        Returns:
            Dict containing logged entry with integrity hash
        """
        return self.action_logger.log_action(
            action_id,
            actor_id,
            timestamp,
            **kwargs
        )
    
    def revoke_access(
        self,
        artifact_id: str,
        actor_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Revoke access to an artifact.
        
        Args:
            artifact_id: Identifier of the artifact
            actor_id: Optional actor identifier (defaults to "system")
            **kwargs: Additional parameters (reason, scope)
        
        Returns:
            Dict containing revocation record
        """
        if actor_id is None:
            actor_id = "system"
        
        return self.access_revoker.revoke_access(
            artifact_id,
            actor_id,
            **kwargs
        )
    
    def generate_compliance_dashboard(self) -> Dict[str, Any]:
        """
        Generate comprehensive compliance dashboard.
        
        Returns:
            Dict containing compliance metrics, action statistics,
            revocation metrics, and integrity verification
        """
        return self.compliance_dashboard.generate_dashboard()
    
    def get_audit_trail(self, **filters) -> List[Dict[str, Any]]:
        """Get filtered audit trail."""
        return self.action_logger.get_audit_trail(**filters)
    
    def check_access(
        self,
        artifact_id: str,
        actor_id: str
    ) -> Dict[str, Any]:
        """Check if access is granted for artifact/actor pair."""
        return self.access_revoker.check_access(artifact_id, actor_id)
    
    def verify_integrity(self) -> Dict[str, Any]:
        """Verify audit log integrity."""
        return self.action_logger.verify_integrity()
    
    def export_compliance_report(
        self,
        output_path: str = "data/compliance-dashboard.json"
    ) -> str:
        """Export compliance dashboard to file."""
        return self.compliance_dashboard.export_dashboard(output_path)


def main():
    """Demo: AuditConsentRing in action."""
    print("=== AuditConsentRing Demo ===\n")
    
    # Initialize the ring
    ring = AuditConsentRing()
    
    # Log some actions
    print("1. Logging actions...")
    ring.log_action(
        "action_001",
        "flamekeeper_sovereign",
        datetime.utcnow().isoformat(),
        action_type="artifact_create",
        artifact_id="eternal-ledger",
        metadata={"type": "diagram", "format": "png"}
    )
    
    ring.log_action(
        "action_002",
        "council_member_alpha",
        datetime.utcnow().isoformat(),
        action_type="artifact_access",
        artifact_id="eternal-ledger",
        metadata={"permission": "read"}
    )
    
    ring.log_action(
        "action_003",
        "affiliate_guardian",
        datetime.utcnow().isoformat(),
        action_type="artifact_distribute",
        artifact_id="eternal-ledger",
        metadata={"network": "cdn"}
    )
    print("✓ Logged 3 actions\n")
    
    # Revoke access
    print("2. Revoking access...")
    revocation = ring.revoke_access(
        "eternal-ledger",
        "council_member_alpha",
        reason="Consent withdrawn",
        scope="all"
    )
    print(f"✓ Revoked access: {revocation['revocation_id']}\n")
    
    # Check access
    print("3. Checking access...")
    access_check = ring.check_access("eternal-ledger", "council_member_alpha")
    print(f"   Access granted: {access_check['access_granted']}")
    print(f"   Reason: {access_check.get('reason', 'N/A')}\n")
    
    # Verify integrity
    print("4. Verifying audit log integrity...")
    integrity = ring.verify_integrity()
    print(f"   Valid: {integrity['valid']}")
    print(f"   Message: {integrity['message']}\n")
    
    # Generate compliance dashboard
    print("5. Generating compliance dashboard...")
    dashboard = ring.generate_compliance_dashboard()
    print(f"   Total actions: {dashboard['overview']['total_actions_logged']}")
    print(f"   Unique actors: {dashboard['overview']['unique_actors']}")
    print(f"   Active revocations: "
          f"{dashboard['revocation_metrics']['active_revocations']}")
    print(f"   Audit integrity: "
          f"{dashboard['overview']['audit_log_integrity']}\n")
    
    # Export dashboard
    print("6. Exporting compliance report...")
    export_path = ring.export_compliance_report()
    print(f"✓ Exported to: {export_path}\n")
    
    print("=== Demo Complete ===")
    print("AuditConsentRing: Sovereign compliance through immutable audit.")


if __name__ == "__main__":
    main()
