#!/usr/bin/env python3
"""
Efficiency Crown - Sovereign Automation & Security Engine

Monitors system flows, triggers automated actions, and enforces
security policies across the Codex Dominion infrastructure.
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


class FlowMonitor:
    """Monitor and track system flows"""

    def __init__(self):
        self.flows: List[Dict[str, Any]] = []
        self.thresholds: Dict[str, float] = {}

    def register_flow(
        self, flow_id: str, source: str, destination: str, metrics: Dict
    ) -> Dict[str, Any]:
        """Register a new flow in the monitoring system"""
        flow = {
            "flow_id": flow_id,
            "source": source,
            "destination": destination,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat(),
            "status": "active"
        }
        self.flows.append(flow)
        return flow

    def get_flow_status(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """Get the current status of a flow"""
        return next(
            (f for f in self.flows if f["flow_id"] == flow_id), None
        )

    def set_threshold(self, metric_name: str, threshold: float) -> None:
        """Set threshold for flow monitoring"""
        self.thresholds[metric_name] = threshold

    def check_thresholds(self, flow_id: str) -> List[str]:
        """Check if flow metrics exceed thresholds"""
        flow = self.get_flow_status(flow_id)
        if not flow:
            return []

        violations = []
        for metric, value in flow["metrics"].items():
            if metric in self.thresholds:
                if value > self.thresholds[metric]:
                    violations.append(
                        f"{metric}: {value} > {self.thresholds[metric]}"
                    )

        return violations


class AutomationEngine:
    """Trigger and manage automated actions"""

    def __init__(self):
        self.triggers: Dict[str, List[Callable]] = {}
        self.event_log: List[Dict[str, Any]] = []

    def register_trigger(
        self, event_type: str, handler: Callable
    ) -> None:
        """Register an automation trigger for an event type"""
        if event_type not in self.triggers:
            self.triggers[event_type] = []
        self.triggers[event_type].append(handler)

    def fire_event(
        self, event_type: str, event_data: Dict[str, Any]
    ) -> List[Any]:
        """Fire an event and execute all registered triggers"""
        event = {
            "event_type": event_type,
            "event_data": event_data,
            "timestamp": datetime.now().isoformat(),
            "handlers_executed": 0
        }

        results = []
        if event_type in self.triggers:
            for handler in self.triggers[event_type]:
                try:
                    result = handler(event_data)
                    results.append(result)
                    event["handlers_executed"] += 1
                except Exception as e:
                    results.append({"error": str(e)})

        self.event_log.append(event)
        return results

    def get_event_history(
        self, event_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get event execution history"""
        if event_type:
            return [
                e for e in self.event_log if e["event_type"] == event_type
            ]
        return self.event_log


class SecurityEnforcer:
    """Enforce security policies across the system"""

    def __init__(self, policy_path: str = "manifests/security_policy.json"):
        self.policy_path = Path(policy_path)
        self.policies: Dict[str, Dict[str, Any]] = {}
        self.violations: List[Dict[str, Any]] = []
        self._load_policies()

    def _load_policies(self) -> None:
        """Load security policies from disk"""
        if self.policy_path.exists():
            with open(self.policy_path, "r", encoding="utf-8") as f:
                self.policies = json.load(f)
        else:
            self._initialize_default_policies()

    def _initialize_default_policies(self) -> None:
        """Initialize default security policies"""
        self.policies = {
            "access_control": {
                "enabled": True,
                "require_authentication": True,
                "allowed_roles": ["sovereign", "council", "contributor"]
            },
            "data_integrity": {
                "enabled": True,
                "require_hash_verification": True,
                "hash_algorithm": "SHA256"
            },
            "rate_limiting": {
                "enabled": True,
                "max_requests_per_minute": 60,
                "max_uploads_per_hour": 10
            },
            "encryption": {
                "enabled": True,
                "require_tls": True,
                "min_tls_version": "1.2"
            }
        }
        self._save_policies()

    def _save_policies(self) -> None:
        """Save policies to disk"""
        self.policy_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.policy_path, "w", encoding="utf-8") as f:
            json.dump(self.policies, f, indent=2)

    def enforce_policy(
        self, policy_name: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Enforce a specific security policy

        Returns dict with:
        - allowed: bool
        - policy: str
        - reason: str (if denied)
        """
        if policy_name not in self.policies:
            return {
                "allowed": False,
                "policy": policy_name,
                "reason": f"Policy not found: {policy_name}"
            }

        policy = self.policies[policy_name]

        if not policy.get("enabled", False):
            return {
                "allowed": True,
                "policy": policy_name,
                "reason": "Policy disabled"
            }

        # Access control enforcement
        if policy_name == "access_control":
            user_role = context.get("role")
            if not user_role:
                return self._log_violation(
                    policy_name, "No role provided", context
                )

            if user_role not in policy["allowed_roles"]:
                return self._log_violation(
                    policy_name, f"Role not allowed: {user_role}", context
                )

        # Data integrity enforcement
        elif policy_name == "data_integrity":
            if policy["require_hash_verification"]:
                if "content_hash" not in context:
                    return self._log_violation(
                        policy_name, "Missing content hash", context
                    )

        # Rate limiting enforcement
        elif policy_name == "rate_limiting":
            request_count = context.get("request_count", 0)
            max_requests = policy["max_requests_per_minute"]
            if request_count > max_requests:
                return self._log_violation(
                    policy_name,
                    f"Rate limit exceeded: {request_count}/{max_requests}",
                    context
                )

        # Encryption enforcement
        elif policy_name == "encryption":
            if policy["require_tls"]:
                tls_version = context.get("tls_version")
                if not tls_version:
                    return self._log_violation(
                        policy_name, "No TLS connection", context
                    )

        return {
            "allowed": True,
            "policy": policy_name,
            "reason": "Policy satisfied"
        }

    def _log_violation(
        self, policy_name: str, reason: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Log a security policy violation"""
        violation = {
            "policy": policy_name,
            "reason": reason,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        self.violations.append(violation)

        return {
            "allowed": False,
            "policy": policy_name,
            "reason": reason
        }

    def get_violations(
        self, policy_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get security violations"""
        if policy_name:
            return [
                v for v in self.violations if v["policy"] == policy_name
            ]
        return self.violations


class EfficiencyCrown:
    """
    Efficiency Crown - Sovereign Automation & Security Engine

    Core capabilities:
    - monitorFlows(): Track and analyze system flows
    - triggerAutomation(event): Fire automated actions based on events
    - enforceSecurity(policy): Enforce security policies
    """

    def __init__(self):
        self.flow_monitor = FlowMonitor()
        self.automation_engine = AutomationEngine()
        self.security_enforcer = SecurityEnforcer()
        print("👑 Efficiency Crown initialized")

    def monitor_flows(
        self, flow_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Monitor system flows and return status

        Args:
            flow_id: Specific flow to monitor (None for all flows)

        Returns:
            Dictionary with flow status and metrics
        """
        print("📊 MONITORING FLOWS")
        print("=" * 60)

        if flow_id:
            flow = self.flow_monitor.get_flow_status(flow_id)
            if not flow:
                print(f"⚠️  Flow not found: {flow_id}")
                return {"status": "not_found", "flow_id": flow_id}

            # Check thresholds
            violations = self.flow_monitor.check_thresholds(flow_id)

            print(f"🔹 Flow: {flow_id}")
            print(f"   Source: {flow['source']}")
            print(f"   Destination: {flow['destination']}")
            print(f"   Status: {flow['status']}")
            print(f"   Metrics: {flow['metrics']}")

            if violations:
                print(f"   ⚠️  Threshold violations: {len(violations)}")
                for violation in violations:
                    print(f"      - {violation}")
            else:
                print("   ✅ All thresholds satisfied")

            return {
                "status": "monitored",
                "flow": flow,
                "violations": violations
            }
        else:
            # Monitor all flows
            total_flows = len(self.flow_monitor.flows)
            active_flows = sum(
                1 for f in self.flow_monitor.flows
                if f["status"] == "active"
            )

            print(f"📋 Total Flows: {total_flows}")
            print(f"✅ Active Flows: {active_flows}")
            print()

            return {
                "status": "monitored",
                "total_flows": total_flows,
                "active_flows": active_flows,
                "flows": self.flow_monitor.flows
            }

    def trigger_automation(
        self, event_type: str, event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Trigger automation based on an event

        Args:
            event_type: Type of event to trigger
            event_data: Data associated with the event

        Returns:
            Dictionary with automation results
        """
        print(f"⚡ TRIGGERING AUTOMATION: {event_type}")
        print("=" * 60)

        # Fire the event
        results = self.automation_engine.fire_event(event_type, event_data)

        print(f"✅ Automation triggered")
        print(f"   Event: {event_type}")
        print(f"   Handlers executed: {len(results)}")
        print(f"   Timestamp: {datetime.now().isoformat()}")
        print()

        return {
            "status": "triggered",
            "event_type": event_type,
            "handlers_executed": len(results),
            "results": results
        }

    def enforce_security(
        self, policy_name: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Enforce a security policy

        Args:
            policy_name: Name of the policy to enforce
            context: Context data for policy evaluation

        Returns:
            Dictionary with enforcement result
        """
        print(f"🔒 ENFORCING SECURITY: {policy_name}")
        print("=" * 60)

        result = self.security_enforcer.enforce_policy(
            policy_name, context
        )

        if result["allowed"]:
            print(f"✅ Security policy satisfied")
            print(f"   Policy: {policy_name}")
            print(f"   Reason: {result['reason']}")
        else:
            print(f"❌ Security policy violation")
            print(f"   Policy: {policy_name}")
            print(f"   Reason: {result['reason']}")

        print()
        return result


def main() -> None:
    """Main execution for testing"""
    print("👑 EFFICIENCY CROWN - SOVEREIGN AUTOMATION ENGINE")
    print("=" * 60)
    print()

    crown = EfficiencyCrown()

    # Example: Register a flow
    print("📝 Registering artifact syndication flow...")
    crown.flow_monitor.register_flow(
        flow_id="artifact-syndication-001",
        source="capsules",
        destination="s3-cdn",
        metrics={"artifacts": 2, "size_mb": 5.2, "latency_ms": 150}
    )

    # Example: Set threshold
    crown.flow_monitor.set_threshold("latency_ms", 200)

    # Monitor flows
    crown.monitor_flows("artifact-syndication-001")

    # Example: Register automation trigger
    def on_artifact_uploaded(data: Dict[str, Any]) -> Dict[str, Any]:
        print(f"   🎯 Handler: Artifact uploaded - {data['artifact_id']}")
        return {"status": "processed", "artifact_id": data["artifact_id"]}

    crown.automation_engine.register_trigger(
        "artifact_uploaded", on_artifact_uploaded
    )

    # Trigger automation
    crown.trigger_automation(
        "artifact_uploaded",
        {"artifact_id": "eternal-ledger-001", "size_mb": 2.5}
    )

    # Enforce security
    crown.enforce_security(
        "access_control",
        {"role": "sovereign", "user": "Jermaine Merritt"}
    )

    # Show violations
    violations = crown.security_enforcer.get_violations()
    print(f"🔒 Total security violations: {len(violations)}")
    print()


if __name__ == "__main__":
    main()
