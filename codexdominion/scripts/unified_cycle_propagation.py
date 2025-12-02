#!/usr/bin/env python3
"""
Unified Cycle Propagation - Cross-Crown and Cross-Council Orchestration

This module implements comprehensive cycle propagation across both Crown
modules and Sovereign Councils, providing unified orchestration for the
entire governance system.

Core Responsibilities:
- Propagate cycle replays across all Crown modules
- Activate council governance for each cycle
- Coordinate cross-domain synchronization
- Track propagation lineage and heritage
- Generate propagation reports and analytics
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib

# Import Crown and Council modules
try:
    from eternal_wave import EternalWave
    from infinity_sigil import InfinitySigil
    from audit_consent_ring import AuditConsentRing
    MODULES_AVAILABLE = True
except ImportError:
    MODULES_AVAILABLE = False
    print("⚠ Modules not found, running in simulation mode")


class LineageTracker:
    """Tracks lineage and heritage of cycle propagations."""
    
    def __init__(self, lineage_path: str = "data/propagation-lineage.json"):
        self.lineage_path = Path(lineage_path)
        self.lineage_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_lineage()
    
    def _initialize_lineage(self) -> None:
        """Initialize lineage tracking."""
        if not self.lineage_path.exists():
            initial_data = {
                "lineages": [],
                "genesis_timestamp": datetime.utcnow().isoformat()
            }
            self._write_lineage(initial_data)
    
    def _read_lineage(self) -> Dict[str, Any]:
        """Read lineage data."""
        with open(self.lineage_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _write_lineage(self, data: Dict[str, Any]) -> None:
        """Write lineage data."""
        with open(self.lineage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def record_lineage(
        self,
        cycle_id: str,
        crowns: List[str],
        councils: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Record lineage for a cycle propagation.
        
        Args:
            cycle_id: Identifier of the cycle
            crowns: List of Crown modules propagated
            councils: List of councils activated
            metadata: Optional additional metadata
        
        Returns:
            Dict containing lineage record
        """
        lineage_data = self._read_lineage()
        
        lineage_id = hashlib.sha256(
            f"{cycle_id}_{datetime.utcnow().isoformat()}".encode('utf-8')
        ).hexdigest()[:16]
        
        lineage_record = {
            "lineage_id": lineage_id,
            "cycle_id": cycle_id,
            "timestamp": datetime.utcnow().isoformat(),
            "crown_lineage": {
                "crowns": crowns,
                "count": len(crowns)
            },
            "council_lineage": {
                "councils": councils,
                "count": len(councils)
            },
            "heritage": {
                "generation": len(lineage_data["lineages"]) + 1,
                "ancestors": [
                    l["lineage_id"] for l in lineage_data["lineages"][-3:]
                ] if lineage_data["lineages"] else []
            },
            "metadata": metadata or {}
        }
        
        lineage_data["lineages"].append(lineage_record)
        self._write_lineage(lineage_data)
        
        return lineage_record
    
    def get_lineage_history(
        self,
        cycle_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get lineage history with optional filtering.
        
        Args:
            cycle_id: Optional cycle filter
            limit: Maximum number of records to return
        
        Returns:
            List of lineage records
        """
        lineage_data = self._read_lineage()
        lineages = lineage_data["lineages"]
        
        if cycle_id:
            lineages = [l for l in lineages if l["cycle_id"] == cycle_id]
        
        return lineages[-limit:]


class UnifiedCyclePropagator:
    """
    Unified propagation engine for cycles across crowns and councils.
    
    Orchestrates comprehensive cycle propagation with lineage tracking,
    council activation, and cross-domain synchronization.
    """
    
    def __init__(
        self,
        propagation_log_path: str = "data/unified-propagation.json"
    ):
        self.propagation_log_path = Path(propagation_log_path)
        self.propagation_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize modules if available
        if MODULES_AVAILABLE:
            self.eternal_wave = EternalWave()
            self.infinity_sigil = InfinitySigil()
            self.audit_ring = AuditConsentRing()
        else:
            self.eternal_wave = None
            self.infinity_sigil = None
            self.audit_ring = None
        
        # Initialize lineage tracker
        self.lineage_tracker = LineageTracker()
        
        # Initialize log
        self._initialize_log()
    
    def _initialize_log(self) -> None:
        """Initialize propagation log."""
        if not self.propagation_log_path.exists():
            initial_data = {
                "propagations": [],
                "last_updated": datetime.utcnow().isoformat()
            }
            self._write_log(initial_data)
    
    def _read_log(self) -> Dict[str, Any]:
        """Read propagation log."""
        with open(self.propagation_log_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _write_log(self, data: Dict[str, Any]) -> None:
        """Write propagation log."""
        with open(self.propagation_log_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def propagate_replay(
        self,
        cycle_id: str,
        crowns: List[str],
        councils: List[str],
        payload: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Propagate cycle replay across crowns and activate council governance.
        
        Args:
            cycle_id: Identifier of the cycle to propagate
            crowns: List of Crown module names to propagate through
            councils: List of council names to activate
            payload: Optional payload data
        
        Returns:
            Dict containing propagation results with lineage
        """
        print(f"\n🔥 Unified Cycle Propagation: {cycle_id}")
        print("=" * 60)
        
        propagation_result = {
            "propagation_id": hashlib.sha256(
                f"unified_{cycle_id}_{datetime.utcnow().isoformat()}"
                .encode('utf-8')
            ).hexdigest()[:16],
            "cycle_id": cycle_id,
            "started_at": datetime.utcnow().isoformat(),
            "crown_results": {},
            "council_results": {},
            "success": False
        }
        
        # Phase 1: Replay lineage from each Crown
        print(f"\n📜 Phase 1: Crown Lineage Replay ({len(crowns)} crowns)")
        print("-" * 60)
        
        for crown in crowns:
            print(f"  🔄 Replaying lineage from {crown} into cycle {cycle_id}")
            
            if MODULES_AVAILABLE and self.eternal_wave:
                try:
                    # Execute through EternalWave
                    result = self.eternal_wave.propagate_across_crowns(
                        cycle_id,
                        payload=payload,
                        target_crowns=[crown]
                    )
                    propagation_result["crown_results"][crown] = {
                        "status": "propagated",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    print(f"     ✓ Success")
                except Exception as e:
                    propagation_result["crown_results"][crown] = {
                        "status": "failed",
                        "error": str(e)
                    }
                    print(f"     ✗ Failed: {e}")
            else:
                # Simulation mode
                propagation_result["crown_results"][crown] = {
                    "status": "simulated",
                    "timestamp": datetime.utcnow().isoformat()
                }
                print(f"     ✓ [SIMULATION]")
        
        # Phase 2: Activate council governance
        print(f"\n⚖️  Phase 2: Council Governance Activation ({len(councils)} councils)")
        print("-" * 60)
        
        for council in councils:
            print(f"  🏛️  Activating council governance: {council} for cycle {cycle_id}")
            
            if MODULES_AVAILABLE and self.infinity_sigil:
                try:
                    # Check council availability
                    available_councils = self.infinity_sigil.get_available_councils()
                    council_lower = council.lower()
                    
                    if council_lower in available_councils:
                        propagation_result["council_results"][council] = {
                            "status": "activated",
                            "council_info": available_councils[council_lower],
                            "timestamp": datetime.utcnow().isoformat()
                        }
                        print(f"     ✓ Activated: {available_councils[council_lower]['full_name']}")
                    else:
                        propagation_result["council_results"][council] = {
                            "status": "unavailable",
                            "message": "Council not registered"
                        }
                        print(f"     ⚠ Council not found")
                except Exception as e:
                    propagation_result["council_results"][council] = {
                        "status": "failed",
                        "error": str(e)
                    }
                    print(f"     ✗ Failed: {e}")
            else:
                # Simulation mode
                propagation_result["council_results"][council] = {
                    "status": "simulated",
                    "timestamp": datetime.utcnow().isoformat()
                }
                print(f"     ✓ [SIMULATION]")
        
        # Phase 3: Record lineage
        print(f"\n📖 Phase 3: Recording Lineage")
        print("-" * 60)
        
        lineage_record = self.lineage_tracker.record_lineage(
            cycle_id,
            crowns,
            councils,
            metadata={
                "propagation_id": propagation_result["propagation_id"],
                "payload": payload
            }
        )
        propagation_result["lineage"] = lineage_record
        print(f"  ✓ Lineage recorded: {lineage_record['lineage_id']}")
        print(f"    Generation: {lineage_record['heritage']['generation']}")
        
        # Phase 4: Audit logging
        if MODULES_AVAILABLE and self.audit_ring:
            print(f"\n📋 Phase 4: Audit Logging")
            print("-" * 60)
            
            self.audit_ring.log_action(
                action_id=propagation_result["propagation_id"],
                actor_id="unified_propagator",
                timestamp=datetime.utcnow().isoformat(),
                action_type="unified_propagation",
                artifact_id=cycle_id,
                metadata={
                    "crowns": crowns,
                    "councils": councils,
                    "lineage_id": lineage_record["lineage_id"]
                }
            )
            print(f"  ✓ Action logged to audit trail")
        
        # Finalize
        propagation_result["completed_at"] = datetime.utcnow().isoformat()
        propagation_result["success"] = True
        
        # Log propagation
        log_data = self._read_log()
        log_data["propagations"].append(propagation_result)
        log_data["last_updated"] = datetime.utcnow().isoformat()
        self._write_log(log_data)
        
        print("\n" + "=" * 60)
        print("✓ Unified Cycle Propagation Complete")
        print(f"  Crowns: {len(crowns)} propagated")
        print(f"  Councils: {len(councils)} activated")
        print(f"  Lineage: Generation {lineage_record['heritage']['generation']}")
        print("=" * 60 + "\n")
        
        return propagation_result
    
    def get_propagation_history(
        self,
        cycle_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get propagation history with optional filtering.
        
        Args:
            cycle_id: Optional cycle filter
            limit: Maximum number of records
        
        Returns:
            List of propagation records
        """
        log_data = self._read_log()
        propagations = log_data["propagations"]
        
        if cycle_id:
            propagations = [
                p for p in propagations
                if p["cycle_id"] == cycle_id
            ]
        
        return propagations[-limit:]
    
    def generate_propagation_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive propagation report.
        
        Returns:
            Dict with statistics and analytics
        """
        log_data = self._read_log()
        lineage_data = self.lineage_tracker._read_lineage()
        
        propagations = log_data["propagations"]
        lineages = lineage_data["lineages"]
        
        # Calculate statistics
        total_propagations = len(propagations)
        unique_cycles = len(set(p["cycle_id"] for p in propagations))
        
        all_crowns = []
        all_councils = []
        for p in propagations:
            all_crowns.extend(p["crown_results"].keys())
            all_councils.extend(p["council_results"].keys())
        
        crown_frequency = {}
        for crown in all_crowns:
            crown_frequency[crown] = crown_frequency.get(crown, 0) + 1
        
        council_frequency = {}
        for council in all_councils:
            council_frequency[council] = council_frequency.get(council, 0) + 1
        
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "overview": {
                "total_propagations": total_propagations,
                "unique_cycles": unique_cycles,
                "total_lineages": len(lineages),
                "current_generation": lineages[-1]["heritage"]["generation"] if lineages else 0
            },
            "crown_statistics": {
                "total_propagations": len(all_crowns),
                "unique_crowns": len(set(all_crowns)),
                "frequency": crown_frequency
            },
            "council_statistics": {
                "total_activations": len(all_councils),
                "unique_councils": len(set(all_councils)),
                "frequency": council_frequency
            },
            "recent_propagations": propagations[-5:],
            "recent_lineages": lineages[-5:]
        }
        
        return report


def main():
    """Demo: Unified Cycle Propagation."""
    print("=== Unified Cycle Propagation Demo ===\n")
    
    # Initialize propagator
    propagator = UnifiedCyclePropagator()
    
    # Example 1: Full system propagation
    print("Example 1: Full System Propagation\n")
    
    result1 = propagator.propagate_replay(
        cycle_id="eternal_wave_2025_q4",
        crowns=[
            "efficiency_crown",
            "knowledge_crown",
            "commerce_crown",
            "companion_crown"
        ],
        councils=[
            "Law",
            "Healthcare",
            "Education",
            "AI",
            "Family"
        ],
        payload={
            "event_type": "quarterly_sync",
            "priority": "high"
        }
    )
    
    # Example 2: Targeted propagation
    print("\nExample 2: Targeted Propagation\n")
    
    result2 = propagator.propagate_replay(
        cycle_id="knowledge_distribution_cycle",
        crowns=["knowledge_crown", "eternal_ledger"],
        councils=["Education", "AI"],
        payload={
            "event_type": "knowledge_sync",
            "distribution_type": "academic"
        }
    )
    
    # Generate report
    print("\n=== Propagation Report ===\n")
    report = propagator.generate_propagation_report()
    
    print(f"Total Propagations: {report['overview']['total_propagations']}")
    print(f"Unique Cycles: {report['overview']['unique_cycles']}")
    print(f"Current Generation: {report['overview']['current_generation']}")
    print(f"\nCrown Statistics:")
    print(f"  Total: {report['crown_statistics']['total_propagations']}")
    print(f"  Unique: {report['crown_statistics']['unique_crowns']}")
    print(f"\nCouncil Statistics:")
    print(f"  Total: {report['council_statistics']['total_activations']}")
    print(f"  Unique: {report['council_statistics']['unique_councils']}")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
