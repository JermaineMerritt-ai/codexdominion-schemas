#!/usr/bin/env python3
"""
EternalWave Module - Cycle Replay and Cross-Crown Propagation System

This module implements scheduled cycle replay and cross-crown artifact
propagation for the Codex Dominion sovereign governance system.

Core Responsibilities:
- Schedule and execute cycle replays at configurable intervals
- Propagate artifacts and events across all Crown modules
- Coordinate cross-crown synchronization
- Maintain replay history and propagation logs
"""

import json
import hashlib
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from threading import Thread, Event
import sched


class ReplayScheduler:
    """Manages scheduled cycle replays."""
    
    def __init__(self, schedule_path: str = "data/replay-schedule.json"):
        self.schedule_path = Path(schedule_path)
        self.schedule_path.parent.mkdir(parents=True, exist_ok=True)
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.scheduled_tasks: Dict[str, Any] = {}
        self.stop_event = Event()
        self._initialize_schedule()
    
    def _initialize_schedule(self) -> None:
        """Initialize replay schedule registry."""
        if not self.schedule_path.exists():
            initial_data = {
                "schedules": [],
                "last_updated": datetime.utcnow().isoformat()
            }
            self._write_schedule(initial_data)
    
    def _read_schedule(self) -> Dict[str, Any]:
        """Read schedule registry."""
        with open(self.schedule_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _write_schedule(self, data: Dict[str, Any]) -> None:
        """Write schedule registry."""
        with open(self.schedule_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def schedule_replay(
        self,
        cycle_id: str,
        interval: int,
        callback: Optional[Callable] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Schedule a cycle replay at specified interval.
        
        Args:
            cycle_id: Identifier of the cycle to replay
            interval: Interval in seconds between replays
            callback: Optional callback function to execute on replay
            metadata: Optional additional metadata
        
        Returns:
            Dict containing schedule record
        """
        schedule_data = self._read_schedule()
        
        schedule_record = {
            "schedule_id": hashlib.sha256(
                f"{cycle_id}_{datetime.utcnow().isoformat()}".encode('utf-8')
            ).hexdigest()[:16],
            "cycle_id": cycle_id,
            "interval_seconds": interval,
            "next_replay": (
                datetime.utcnow() + timedelta(seconds=interval)
            ).isoformat(),
            "created_at": datetime.utcnow().isoformat(),
            "status": "active",
            "replay_count": 0,
            "metadata": metadata or {}
        }
        
        schedule_data["schedules"].append(schedule_record)
        schedule_data["last_updated"] = datetime.utcnow().isoformat()
        self._write_schedule(schedule_data)
        
        # Store callback reference
        if callback:
            self.scheduled_tasks[schedule_record["schedule_id"]] = {
                "callback": callback,
                "interval": interval,
                "cycle_id": cycle_id
            }
        
        return schedule_record
    
    def execute_replay(self, cycle_id: str) -> Dict[str, Any]:
        """
        Execute a cycle replay immediately.
        
        Args:
            cycle_id: Identifier of the cycle to replay
        
        Returns:
            Dict containing replay execution record
        """
        execution_record = {
            "execution_id": hashlib.sha256(
                f"replay_{cycle_id}_{datetime.utcnow().isoformat()}"
                .encode('utf-8')
            ).hexdigest()[:16],
            "cycle_id": cycle_id,
            "executed_at": datetime.utcnow().isoformat(),
            "status": "completed"
        }
        
        # Update schedule replay count
        schedule_data = self._read_schedule()
        for schedule in schedule_data["schedules"]:
            if schedule["cycle_id"] == cycle_id and schedule["status"] == "active":
                schedule["replay_count"] += 1
                schedule["last_replay"] = datetime.utcnow().isoformat()
                schedule["next_replay"] = (
                    datetime.utcnow() + 
                    timedelta(seconds=schedule["interval_seconds"])
                ).isoformat()
        
        schedule_data["last_updated"] = datetime.utcnow().isoformat()
        self._write_schedule(schedule_data)
        
        return execution_record
    
    def cancel_schedule(self, schedule_id: str) -> Dict[str, Any]:
        """
        Cancel a scheduled replay.
        
        Args:
            schedule_id: Identifier of the schedule to cancel
        
        Returns:
            Dict with cancellation status
        """
        schedule_data = self._read_schedule()
        
        for schedule in schedule_data["schedules"]:
            if schedule["schedule_id"] == schedule_id:
                schedule["status"] = "cancelled"
                schedule["cancelled_at"] = datetime.utcnow().isoformat()
                
                # Remove from scheduled tasks
                if schedule_id in self.scheduled_tasks:
                    del self.scheduled_tasks[schedule_id]
                
                schedule_data["last_updated"] = datetime.utcnow().isoformat()
                self._write_schedule(schedule_data)
                
                return {
                    "cancelled": True,
                    "schedule_id": schedule_id,
                    "cycle_id": schedule["cycle_id"]
                }
        
        return {"cancelled": False, "message": "Schedule not found"}
    
    def get_active_schedules(self) -> List[Dict[str, Any]]:
        """Get all active replay schedules."""
        schedule_data = self._read_schedule()
        return [
            s for s in schedule_data["schedules"]
            if s["status"] == "active"
        ]


class CrossCrownPropagator:
    """Propagates artifacts and events across all Crown modules."""
    
    def __init__(self, propagation_path: str = "data/propagation-log.json"):
        self.propagation_path = Path(propagation_path)
        self.propagation_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_log()
        
        # Crown module registry
        self.crowns = {
            "eternal_ledger": {"priority": 1, "status": "active"},
            "efficiency_crown": {"priority": 2, "status": "active"},
            "knowledge_crown": {"priority": 3, "status": "active"},
            "commerce_crown": {"priority": 4, "status": "active"},
            "companion_crown": {"priority": 5, "status": "active"},
            "audit_consent_ring": {"priority": 6, "status": "active"}
        }
    
    def _initialize_log(self) -> None:
        """Initialize propagation log."""
        if not self.propagation_path.exists():
            initial_data = {
                "propagations": [],
                "last_updated": datetime.utcnow().isoformat()
            }
            self._write_log(initial_data)
    
    def _read_log(self) -> Dict[str, Any]:
        """Read propagation log."""
        with open(self.propagation_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _write_log(self, data: Dict[str, Any]) -> None:
        """Write propagation log."""
        with open(self.propagation_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def propagate_across_crowns(
        self,
        cycle_id: str,
        payload: Optional[Dict[str, Any]] = None,
        target_crowns: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Propagate a cycle across all Crown modules.
        
        Args:
            cycle_id: Identifier of the cycle to propagate
            payload: Optional payload data to propagate
            target_crowns: Optional list of specific crowns to target
        
        Returns:
            Dict containing propagation results for each crown
        """
        log_data = self._read_log()
        
        # Determine target crowns
        targets = (
            target_crowns if target_crowns
            else sorted(self.crowns.keys(), key=lambda x: self.crowns[x]["priority"])
        )
        
        # Execute propagation
        propagation_results = {
            "propagation_id": hashlib.sha256(
                f"propagate_{cycle_id}_{datetime.utcnow().isoformat()}"
                .encode('utf-8')
            ).hexdigest()[:16],
            "cycle_id": cycle_id,
            "started_at": datetime.utcnow().isoformat(),
            "payload": payload or {},
            "crown_results": {}
        }
        
        # Propagate to each crown in priority order
        for crown_name in targets:
            if crown_name not in self.crowns:
                propagation_results["crown_results"][crown_name] = {
                    "status": "skipped",
                    "reason": "Crown not registered"
                }
                continue
            
            crown_info = self.crowns[crown_name]
            
            if crown_info["status"] != "active":
                propagation_results["crown_results"][crown_name] = {
                    "status": "skipped",
                    "reason": f"Crown status: {crown_info['status']}"
                }
                continue
            
            # Simulate propagation (in real implementation, would call actual crown methods)
            crown_result = {
                "status": "propagated",
                "priority": crown_info["priority"],
                "timestamp": datetime.utcnow().isoformat(),
                "payload_received": bool(payload)
            }
            
            propagation_results["crown_results"][crown_name] = crown_result
        
        # Record completion
        propagation_results["completed_at"] = datetime.utcnow().isoformat()
        propagation_results["success_count"] = sum(
            1 for r in propagation_results["crown_results"].values()
            if r["status"] == "propagated"
        )
        propagation_results["total_targets"] = len(targets)
        
        # Log propagation
        log_data["propagations"].append(propagation_results)
        log_data["last_updated"] = datetime.utcnow().isoformat()
        self._write_log(log_data)
        
        return propagation_results
    
    def get_propagation_history(
        self,
        cycle_id: Optional[str] = None,
        crown_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get propagation history with optional filtering.
        
        Args:
            cycle_id: Filter by cycle ID
            crown_name: Filter by crown name
        
        Returns:
            List of matching propagation records
        """
        log_data = self._read_log()
        propagations = log_data["propagations"]
        
        # Apply filters
        if cycle_id:
            propagations = [
                p for p in propagations
                if p["cycle_id"] == cycle_id
            ]
        
        if crown_name:
            propagations = [
                p for p in propagations
                if crown_name in p["crown_results"]
            ]
        
        return propagations
    
    def register_crown(
        self,
        crown_name: str,
        priority: int,
        status: str = "active"
    ) -> Dict[str, Any]:
        """
        Register a new crown for propagation.
        
        Args:
            crown_name: Name of the crown module
            priority: Propagation priority (lower = earlier)
            status: Crown status (active/inactive)
        
        Returns:
            Dict with registration status
        """
        self.crowns[crown_name] = {
            "priority": priority,
            "status": status,
            "registered_at": datetime.utcnow().isoformat()
        }
        
        return {
            "registered": True,
            "crown_name": crown_name,
            "priority": priority
        }
    
    def get_crown_status(self) -> Dict[str, Any]:
        """Get status of all registered crowns."""
        return {
            "total_crowns": len(self.crowns),
            "active_crowns": sum(
                1 for c in self.crowns.values()
                if c["status"] == "active"
            ),
            "crowns": self.crowns
        }


class EternalWave:
    """
    Main interface for cycle replay and cross-crown propagation.
    
    Provides unified access to scheduled replay and artifact propagation
    across the entire sovereign governance system.
    """
    
    def __init__(
        self,
        schedule_path: str = "data/replay-schedule.json",
        propagation_path: str = "data/propagation-log.json"
    ):
        self.replay_scheduler = ReplayScheduler(schedule_path)
        self.cross_crown_propagator = CrossCrownPropagator(propagation_path)
    
    def schedule_replay(
        self,
        cycle_id: str,
        interval: int,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Schedule a cycle replay at specified interval.
        
        Args:
            cycle_id: Identifier of the cycle to replay
            interval: Interval in seconds between replays
            **kwargs: Additional parameters (callback, metadata)
        
        Returns:
            Dict containing schedule record with schedule_id and next_replay time
        """
        return self.replay_scheduler.schedule_replay(
            cycle_id,
            interval,
            **kwargs
        )
    
    def propagate_across_crowns(
        self,
        cycle_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Propagate a cycle across all Crown modules.
        
        Args:
            cycle_id: Identifier of the cycle to propagate
            **kwargs: Additional parameters (payload, target_crowns)
        
        Returns:
            Dict containing propagation results for each crown module
        """
        return self.cross_crown_propagator.propagate_across_crowns(
            cycle_id,
            **kwargs
        )
    
    def execute_replay(self, cycle_id: str) -> Dict[str, Any]:
        """Execute a cycle replay immediately."""
        return self.replay_scheduler.execute_replay(cycle_id)
    
    def cancel_schedule(self, schedule_id: str) -> Dict[str, Any]:
        """Cancel a scheduled replay."""
        return self.replay_scheduler.cancel_schedule(schedule_id)
    
    def get_active_schedules(self) -> List[Dict[str, Any]]:
        """Get all active replay schedules."""
        return self.replay_scheduler.get_active_schedules()
    
    def get_propagation_history(self, **filters) -> List[Dict[str, Any]]:
        """Get propagation history with optional filters."""
        return self.cross_crown_propagator.get_propagation_history(**filters)
    
    def register_crown(
        self,
        crown_name: str,
        priority: int,
        status: str = "active"
    ) -> Dict[str, Any]:
        """Register a new crown for propagation."""
        return self.cross_crown_propagator.register_crown(
            crown_name,
            priority,
            status
        )
    
    def get_crown_status(self) -> Dict[str, Any]:
        """Get status of all registered crowns."""
        return self.cross_crown_propagator.get_crown_status()
    
    def replay_and_propagate(
        self,
        cycle_id: str,
        payload: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a replay and immediately propagate across all crowns.
        
        Args:
            cycle_id: Identifier of the cycle
            payload: Optional payload to propagate
        
        Returns:
            Dict containing both replay and propagation results
        """
        # Execute replay
        replay_result = self.execute_replay(cycle_id)
        
        # Propagate across crowns
        propagation_result = self.propagate_across_crowns(
            cycle_id,
            payload=payload
        )
        
        return {
            "cycle_id": cycle_id,
            "replay": replay_result,
            "propagation": propagation_result,
            "completed_at": datetime.utcnow().isoformat()
        }


def main():
    """Demo: EternalWave in action."""
    print("=== EternalWave Demo ===\n")
    
    # Initialize the wave
    wave = EternalWave()
    
    # Schedule a replay
    print("1. Scheduling cycle replay...")
    schedule = wave.schedule_replay(
        "cycle_2024_q4",
        interval=3600,  # Every hour
        metadata={"type": "quarterly_review", "year": 2024}
    )
    print(f"✓ Scheduled: {schedule['schedule_id']}")
    print(f"   Cycle: {schedule['cycle_id']}")
    print(f"   Interval: {schedule['interval_seconds']}s")
    print(f"   Next replay: {schedule['next_replay']}\n")
    
    # Propagate across crowns
    print("2. Propagating cycle across all crowns...")
    propagation = wave.propagate_across_crowns(
        "cycle_2024_q4",
        payload={
            "artifacts": ["eternal-ledger", "commerce-constellation"],
            "event_type": "quarterly_sync"
        }
    )
    print(f"✓ Propagated: {propagation['propagation_id']}")
    print(f"   Success count: {propagation['success_count']}/{propagation['total_targets']}")
    print("   Crown results:")
    for crown, result in propagation["crown_results"].items():
        print(f"      - {crown}: {result['status']}")
    print()
    
    # Execute immediate replay
    print("3. Executing immediate replay...")
    replay = wave.execute_replay("cycle_2024_q4")
    print(f"✓ Replay executed: {replay['execution_id']}")
    print(f"   Status: {replay['status']}\n")
    
    # Combined replay and propagation
    print("4. Combined replay and propagation...")
    combined = wave.replay_and_propagate(
        "cycle_2024_q4",
        payload={"event": "synchronized_replay"}
    )
    print(f"✓ Combined operation complete")
    print(f"   Replay: {combined['replay']['status']}")
    print(f"   Propagation: {combined['propagation']['success_count']} crowns\n")
    
    # Get crown status
    print("5. Crown status...")
    status = wave.get_crown_status()
    print(f"   Total crowns: {status['total_crowns']}")
    print(f"   Active crowns: {status['active_crowns']}")
    print("   Registered crowns:")
    for crown, info in sorted(
        status['crowns'].items(),
        key=lambda x: x[1]['priority']
    ):
        print(f"      {info['priority']}. {crown} ({info['status']})")
    print()
    
    # Get active schedules
    print("6. Active schedules...")
    schedules = wave.get_active_schedules()
    print(f"   Total active: {len(schedules)}")
    for sched in schedules:
        print(f"   - {sched['cycle_id']}: "
              f"{sched['replay_count']} replays, "
              f"next at {sched['next_replay']}")
    print()
    
    print("=== Demo Complete ===")
    print("EternalWave: Perpetual cycles across sovereign crowns.")


if __name__ == "__main__":
    main()
