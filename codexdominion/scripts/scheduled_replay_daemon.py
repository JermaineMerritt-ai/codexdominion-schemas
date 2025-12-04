#!/usr/bin/env python3
"""
Scheduled Cycle Replay Daemon - Automated Eternal Wave Orchestration

This module implements a persistent daemon that schedules and executes
cycle replays across all Crown modules at configurable intervals.

Core Responsibilities:
- Schedule periodic cycle replays (daily, hourly, custom intervals)
- Execute cross-crown propagation on schedule
- Maintain daemon process with graceful shutdown
- Log all scheduled executions
- Support multiple concurrent schedules
"""

import schedule
import time
import signal
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
import logging

# Import Crown modules for integration
try:
    from eternal_wave import EternalWave
    from eternal_ledger import EternalLedger
    from efficiency_crown import EfficiencyCrown
    from knowledge_crown import KnowledgeCrown
    from commerce_crown import CommerceCrown
    from companion_crown import CompanionCrown
    from audit_consent_ring import AuditConsentRing
    CROWN_MODULES_AVAILABLE = True
except ImportError:
    CROWN_MODULES_AVAILABLE = False
    print("⚠ Crown modules not found, running in simulation mode")


class ScheduledReplayDaemon:
    """
    Daemon process for scheduled cycle replays.

    Manages multiple concurrent schedules and executes cycle replays
    across all Crown modules at specified intervals.
    """

    def __init__(
        self,
        log_path: str = "data/replay-daemon.log",
        schedule_config_path: str = "data/daemon-schedules.json"
    ):
        self.log_path = Path(log_path)
        self.schedule_config_path = Path(schedule_config_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.schedule_config_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize logging
        self._setup_logging()

        # Initialize Crown modules if available
        if CROWN_MODULES_AVAILABLE:
            self.eternal_wave = EternalWave()
            self.eternal_ledger = EternalLedger()
            self.audit_ring = AuditConsentRing()
            self.logger.info("✓ Crown modules initialized")
        else:
            self.eternal_wave = None
            self.eternal_ledger = None
            self.audit_ring = None
            self.logger.warning("⚠ Running without Crown modules (simulation mode)")

        # Daemon state
        self.running = False
        self.schedules: Dict[str, Dict[str, Any]] = {}

        # Load existing schedules
        self._load_schedules()

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _setup_logging(self) -> None:
        """Configure logging for the daemon."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(self.log_path),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _load_schedules(self) -> None:
        """Load saved schedules from configuration file."""
        if self.schedule_config_path.exists():
            with open(self.schedule_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.schedules = config.get("schedules", {})
                self.logger.info(f"Loaded {len(self.schedules)} saved schedules")
        else:
            self._save_schedules()

    def _save_schedules(self) -> None:
        """Save current schedules to configuration file."""
        config = {
            "schedules": self.schedules,
            "last_updated": datetime.utcnow().isoformat()
        }
        with open(self.schedule_config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

    def _signal_handler(self, signum, frame) -> None:
        """Handle shutdown signals gracefully."""
        signal_name = signal.Signals(signum).name
        self.logger.info(f"Received {signal_name}, shutting down gracefully...")
        self.stop()

    def replay_cycle(
        self,
        cycle_id: str,
        propagate: bool = True,
        log_action: bool = True
    ) -> Dict[str, Any]:
        """
        Execute a cycle replay across all Crown modules.

        Args:
            cycle_id: Identifier of the cycle to replay
            propagate: Whether to propagate across crowns
            log_action: Whether to log to audit trail

        Returns:
            Dict containing execution results
        """
        self.logger.info(f"Starting cycle replay: {cycle_id}")

        result = {
            "cycle_id": cycle_id,
            "started_at": datetime.utcnow().isoformat(),
            "success": False
        }

        try:
            if CROWN_MODULES_AVAILABLE and self.eternal_wave:
                # Execute replay
                replay_result = self.eternal_wave.execute_replay(cycle_id)
                result["replay"] = replay_result

                # Propagate across crowns if requested
                if propagate:
                    propagation_result = self.eternal_wave.propagate_across_crowns(
                        cycle_id,
                        payload={
                            "scheduled": True,
                            "timestamp": datetime.utcnow().isoformat()
                        }
                    )
                    result["propagation"] = propagation_result
                    self.logger.info(
                        f"  Propagated to {propagation_result['success_count']} crowns"
                    )

                # Log to audit trail if requested
                if log_action and self.audit_ring:
                    self.audit_ring.log_action(
                        action_id=f"replay_{cycle_id}_{int(time.time())}",
                        actor_id="replay_daemon",
                        timestamp=datetime.utcnow().isoformat(),
                        action_type="scheduled_replay",
                        artifact_id=cycle_id,
                        metadata={"propagated": propagate}
                    )

                result["success"] = True
                self.logger.info(f"✓ Cycle replay completed: {cycle_id}")
            else:
                # Simulation mode
                self.logger.info(f"  [SIMULATION] Replaying cycle {cycle_id} across crowns...")
                result["success"] = True
                result["mode"] = "simulation"

        except Exception as e:
            self.logger.error(f"✗ Cycle replay failed: {e}")
            result["error"] = str(e)

        result["completed_at"] = datetime.utcnow().isoformat()
        return result

    def add_daily_schedule(
        self,
        cycle_id: str,
        time_str: str = "00:00",
        propagate: bool = True
    ) -> Dict[str, Any]:
        """
        Add a daily schedule for cycle replay.

        Args:
            cycle_id: Cycle identifier to replay
            time_str: Time of day in HH:MM format (24-hour)
            propagate: Whether to propagate across crowns

        Returns:
            Dict with schedule details
        """
        schedule_id = f"daily_{cycle_id}_{time_str.replace(':', '')}"

        # Create the scheduled job
        job = schedule.every().day.at(time_str).do(
            self.replay_cycle,
            cycle_id=cycle_id,
            propagate=propagate
        )

        # Store schedule metadata
        self.schedules[schedule_id] = {
            "cycle_id": cycle_id,
            "type": "daily",
            "time": time_str,
            "propagate": propagate,
            "created_at": datetime.utcnow().isoformat(),
            "status": "active"
        }

        self._save_schedules()
        self.logger.info(f"Added daily schedule: {cycle_id} at {time_str}")

        return {
            "scheduled": True,
            "schedule_id": schedule_id,
            "cycle_id": cycle_id,
            "frequency": "daily",
            "time": time_str
        }

    def add_hourly_schedule(
        self,
        cycle_id: str,
        minute: int = 0,
        propagate: bool = True
    ) -> Dict[str, Any]:
        """
        Add an hourly schedule for cycle replay.

        Args:
            cycle_id: Cycle identifier to replay
            minute: Minute of the hour (0-59)
            propagate: Whether to propagate across crowns

        Returns:
            Dict with schedule details
        """
        schedule_id = f"hourly_{cycle_id}_{minute}"

        # Create the scheduled job
        job = schedule.every().hour.at(f":{minute:02d}").do(
            self.replay_cycle,
            cycle_id=cycle_id,
            propagate=propagate
        )

        # Store schedule metadata
        self.schedules[schedule_id] = {
            "cycle_id": cycle_id,
            "type": "hourly",
            "minute": minute,
            "propagate": propagate,
            "created_at": datetime.utcnow().isoformat(),
            "status": "active"
        }

        self._save_schedules()
        self.logger.info(f"Added hourly schedule: {cycle_id} at minute {minute}")

        return {
            "scheduled": True,
            "schedule_id": schedule_id,
            "cycle_id": cycle_id,
            "frequency": "hourly",
            "minute": minute
        }

    def add_interval_schedule(
        self,
        cycle_id: str,
        interval_seconds: int,
        propagate: bool = True
    ) -> Dict[str, Any]:
        """
        Add an interval-based schedule for cycle replay.

        Args:
            cycle_id: Cycle identifier to replay
            interval_seconds: Interval in seconds
            propagate: Whether to propagate across crowns

        Returns:
            Dict with schedule details
        """
        schedule_id = f"interval_{cycle_id}_{interval_seconds}"

        # Create the scheduled job
        job = schedule.every(interval_seconds).seconds.do(
            self.replay_cycle,
            cycle_id=cycle_id,
            propagate=propagate
        )

        # Store schedule metadata
        self.schedules[schedule_id] = {
            "cycle_id": cycle_id,
            "type": "interval",
            "interval_seconds": interval_seconds,
            "propagate": propagate,
            "created_at": datetime.utcnow().isoformat(),
            "status": "active"
        }

        self._save_schedules()
        self.logger.info(f"Added interval schedule: {cycle_id} every {interval_seconds}s")

        return {
            "scheduled": True,
            "schedule_id": schedule_id,
            "cycle_id": cycle_id,
            "frequency": "interval",
            "interval_seconds": interval_seconds
        }

    def remove_schedule(self, schedule_id: str) -> Dict[str, Any]:
        """
        Remove a scheduled replay.

        Args:
            schedule_id: Identifier of the schedule to remove

        Returns:
            Dict with removal status
        """
        if schedule_id in self.schedules:
            self.schedules[schedule_id]["status"] = "removed"
            self.schedules[schedule_id]["removed_at"] = datetime.utcnow().isoformat()
            self._save_schedules()

            # Clear from schedule library
            schedule.clear(schedule_id)

            self.logger.info(f"Removed schedule: {schedule_id}")
            return {"removed": True, "schedule_id": schedule_id}

        return {"removed": False, "error": "Schedule not found"}

    def list_schedules(self) -> List[Dict[str, Any]]:
        """List all active schedules."""
        return [
            {
                "schedule_id": sid,
                **details
            }
            for sid, details in self.schedules.items()
            if details.get("status") == "active"
        ]

    def start(self) -> None:
        """Start the daemon process."""
        self.running = True
        self.logger.info("=== Scheduled Replay Daemon Started ===")
        self.logger.info(f"Active schedules: {len(self.list_schedules())}")

        for sched in self.list_schedules():
            self.logger.info(f"  - {sched['schedule_id']}: {sched['type']} ({sched['cycle_id']})")

        self.logger.info("Daemon is running. Press Ctrl+C to stop.\n")

        try:
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt received")
        finally:
            self.stop()

    def stop(self) -> None:
        """Stop the daemon process."""
        self.running = False
        self.logger.info("=== Scheduled Replay Daemon Stopped ===")
        sys.exit(0)


def main():
    """Main entry point for the daemon."""
    print("=== Scheduled Cycle Replay Daemon ===\n")

    # Initialize daemon
    daemon = ScheduledReplayDaemon()

    # Add example schedules
    print("Setting up schedules...\n")

    # Daily replay at midnight
    daemon.add_daily_schedule(
        cycle_id="eternal_wave",
        time_str="00:00",
        propagate=True
    )

    # Hourly replay at minute 0
    daemon.add_hourly_schedule(
        cycle_id="commerce_sync",
        minute=0,
        propagate=True
    )

    # Every 5 minutes for testing
    daemon.add_interval_schedule(
        cycle_id="knowledge_index",
        interval_seconds=300,
        propagate=True
    )

    # List active schedules
    print("\nActive schedules:")
    for sched in daemon.list_schedules():
        print(f"  - {sched['schedule_id']}")
        print(f"    Cycle: {sched['cycle_id']}")
        print(f"    Type: {sched['type']}")
        if sched['type'] == 'daily':
            print(f"    Time: {sched['time']}")
        elif sched['type'] == 'hourly':
            print(f"    Minute: {sched['minute']}")
        elif sched['type'] == 'interval':
            print(f"    Interval: {sched['interval_seconds']}s")
        print()

    # Start the daemon
    print("Starting daemon...\n")
    daemon.start()


if __name__ == "__main__":
    main()
