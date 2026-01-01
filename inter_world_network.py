"""
🔥 PHASE 60 — STEP 2: INTER-WORLD NETWORK ARCHITECTURE
The communication, collaboration, and coordination layer of the Dominion Cosmos.

This module implements the 4-layer Inter-World Network (IWN):
1. Inter-World Communication Protocol (IWCP) - Messaging system
2. Resource Exchange Grid (REG) - Resource sharing
3. Inter-World Project Router (IWPR) - Intelligent project routing
4. Cosmic Memory Synchronizer (CMS) - Unified memory across worlds

The IWN turns isolated worlds into a connected creative universe.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum
import uuid
import json

from db import SessionLocal
from models import Agent, Workflow
from multiworld_schema import (
    World, WorldAgent, InterWorldConnection, 
    AgentMigration, CrossWorldProject, InterWorldMessage
)


# ============================================================================
# LAYER 1 — INTER-WORLD COMMUNICATION PROTOCOL (IWCP)
# ============================================================================

class MessageType(Enum):
    """Types of messages worlds can send to each other."""
    REQUEST_SUPPORT = "request_support"           # World needs help
    SHARE_RESOURCE = "share_resource"             # World offering resource
    ESCALATE_DECISION = "escalate_decision"       # Decision needs higher authority
    SYNC_MEMORY = "sync_memory"                   # Share cultural memory update
    PROPOSE_COLLABORATION = "propose_collaboration"  # Start cross-world project
    AGENT_MIGRATION_REQUEST = "agent_migration_request"  # Request agent transfer
    WORKFLOW_HANDOFF = "workflow_handoff"         # Pass workflow to another world
    INNOVATION_BROADCAST = "innovation_broadcast"  # Share breakthrough
    RESOURCE_AVAILABILITY = "resource_availability"  # Announce available resources
    EMERGENCY_ALERT = "emergency_alert"           # Critical issue


class MessagePriority(Enum):
    """Message priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class InterWorldCommunicationProtocol:
    """
    LAYER 1: The basic language worlds use to communicate.
    
    Handles:
    - Message sending and receiving
    - Protocol formatting
    - Message routing
    - Priority handling
    - Response tracking
    """
    
    def __init__(self):
        self.session = SessionLocal()
    
    def send_message(
        self,
        from_world_id: str,
        to_world_id: str,
        message_type: MessageType,
        subject: str,
        content: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL,
        related_project_id: Optional[str] = None
    ) -> InterWorldMessage:
        """
        Send a message from one world to another.
        
        This is the fundamental communication primitive of the IWN.
        """
        message = InterWorldMessage(
            id=f"iwm_{uuid.uuid4().hex[:12]}",
            from_world_id=from_world_id,
            to_world_id=to_world_id,
            message_type=message_type.value,
            subject=subject,
            content=json.dumps(content),  # Convert dict to JSON string
            priority=priority.value,
            related_project_id=related_project_id,
            status="sent",
            sent_date=datetime.utcnow()
        )
        
        self.session.add(message)
        
        # Update connection activity
        connection = self.session.query(InterWorldConnection).filter_by(
            source_world_id=from_world_id,
            target_world_id=to_world_id
        ).first()
        
        if connection:
            connection.total_exchanges += 1
            connection.last_interaction = datetime.utcnow()
        
        self.session.commit()
        
        return message
    
    def broadcast_message(
        self,
        from_world_id: str,
        message_type: MessageType,
        subject: str,
        content: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL
    ) -> List[InterWorldMessage]:
        """
        Broadcast a message to all connected worlds.
        
        Used for:
        - Innovation announcements
        - Resource availability
        - Emergency alerts
        """
        messages = []
        
        # Get all outgoing connections from this world
        connections = self.session.query(InterWorldConnection).filter_by(
            source_world_id=from_world_id,
            status="active"
        ).all()
        
        for connection in connections:
            message = self.send_message(
                from_world_id=from_world_id,
                to_world_id=connection.target_world_id,
                message_type=message_type,
                subject=subject,
                content=content,
                priority=priority
            )
            messages.append(message)
        
        return messages
    
    def request_support(
        self,
        requesting_world_id: str,
        target_world_id: str,
        support_type: str,
        details: Dict[str, Any]
    ) -> InterWorldMessage:
        """
        Request support from another world.
        
        Support types:
        - agent_expertise
        - creative_asset
        - workflow_template
        - technical_capability
        """
        return self.send_message(
            from_world_id=requesting_world_id,
            to_world_id=target_world_id,
            message_type=MessageType.REQUEST_SUPPORT,
            subject=f"Support Request: {support_type}",
            content={
                "support_type": support_type,
                "details": details,
                "urgency": details.get("urgency", "normal"),
                "duration_needed": details.get("duration_needed", "unknown")
            },
            priority=MessagePriority.HIGH if details.get("urgent") else MessagePriority.NORMAL
        )
    
    def get_pending_messages(self, world_id: str) -> List[InterWorldMessage]:
        """Get all pending messages for a world."""
        return self.session.query(InterWorldMessage).filter_by(
            to_world_id=world_id,
            status="sent"
        ).order_by(InterWorldMessage.sent_date.desc()).all()
    
    def mark_message_read(self, message_id: str):
        """Mark a message as read."""
        message = self.session.query(InterWorldMessage).filter_by(id=message_id).first()
        if message:
            message.status = "read"
            message.read_date = datetime.utcnow()
            self.session.commit()
    
    def close(self):
        """Close database session."""
        self.session.close()


# ============================================================================
# LAYER 2 — RESOURCE EXCHANGE GRID (REG)
# ============================================================================

class ResourceType(Enum):
    """Types of resources that can be exchanged."""
    AGENT = "agent"
    CREATIVE_ASSET = "creative_asset"
    TEMPLATE = "template"
    WORKFLOW = "workflow"
    STYLE_GUIDE = "style_guide"
    MEMORY_FRAGMENT = "memory_fragment"
    EVOLUTION_PROPOSAL = "evolution_proposal"
    CAPABILITY = "capability"


class ResourceExchangeGrid:
    """
    LAYER 2: How worlds share resources.
    
    Ensures:
    - No world becomes isolated
    - No world becomes overloaded
    - No world hoards resources
    - Every world can request help
    - Every world can contribute
    
    This is the economic bloodstream of the cosmos.
    """
    
    def __init__(self):
        self.session = SessionLocal()
        self.iwcp = InterWorldCommunicationProtocol()
    
    def offer_resource(
        self,
        offering_world_id: str,
        resource_type: ResourceType,
        resource_id: str,
        resource_data: Dict[str, Any],
        availability: str = "available"
    ) -> List[InterWorldMessage]:
        """
        Offer a resource to other worlds.
        
        Broadcasts availability to all connected worlds.
        """
        content = {
            "resource_type": resource_type.value,
            "resource_id": resource_id,
            "resource_data": resource_data,
            "availability": availability,
            "offered_at": datetime.utcnow().isoformat()
        }
        
        return self.iwcp.broadcast_message(
            from_world_id=offering_world_id,
            message_type=MessageType.RESOURCE_AVAILABILITY,
            subject=f"Resource Available: {resource_type.value}",
            content=content,
            priority=MessagePriority.NORMAL
        )
    
    def request_agent_migration(
        self,
        from_world_id: str,
        to_world_id: str,
        agent_id: str,
        migration_type: str,
        reason: str,
        duration_days: Optional[int] = None
    ) -> AgentMigration:
        """
        Request an agent to migrate from one world to another.
        
        Migration types:
        - temporary: Agent returns after duration
        - permanent: Agent stays in new world
        - exploratory: Short-term learning visit
        - assignment: Specific project assignment
        """
        # Send message to coordinate migration
        self.iwcp.send_message(
            from_world_id=to_world_id,
            to_world_id=from_world_id,
            message_type=MessageType.AGENT_MIGRATION_REQUEST,
            subject=f"Agent Migration Request: {agent_id}",
            content={
                "agent_id": agent_id,
                "migration_type": migration_type,
                "reason": reason,
                "duration_days": duration_days
            },
            priority=MessagePriority.HIGH
        )
        
        # Create migration record
        migration = AgentMigration(
            id=f"migration_{uuid.uuid4().hex[:12]}",
            agent_id=agent_id,
            from_world_id=from_world_id,
            to_world_id=to_world_id,
            migration_type=migration_type,
            reason=reason,
            duration_expected_days=duration_days,
            status="requested",
            initiated_date=datetime.utcnow()
        )
        
        self.session.add(migration)
        self.session.commit()
        
        return migration
    
    def approve_agent_migration(self, migration_id: str) -> WorldAgent:
        """
        Approve an agent migration and create WorldAgent entry.
        """
        migration = self.session.query(AgentMigration).filter_by(id=migration_id).first()
        if not migration:
            raise ValueError(f"Migration {migration_id} not found")
        
        # Update migration status
        migration.status = "active"
        
        # Create WorldAgent entry in destination world
        world_agent = WorldAgent(
            id=f"wa_{uuid.uuid4().hex[:12]}",
            agent_id=migration.agent_id,
            world_id=migration.to_world_id,
            role="migrant",
            citizenship_status="visitor" if migration.migration_type == "temporary" else "immigrant",
            origin_world_id=migration.from_world_id,
            is_temporary=(migration.migration_type == "temporary"),
            world_reputation=50.0  # Starting reputation in new world
        )
        
        self.session.add(world_agent)
        
        # Update world populations
        from_world = self.session.query(World).filter_by(id=migration.from_world_id).first()
        to_world = self.session.query(World).filter_by(id=migration.to_world_id).first()
        
        if from_world and migration.migration_type == "permanent":
            from_world.population -= 1
        if to_world:
            to_world.population += 1
        
        self.session.commit()
        
        return world_agent
    
    def share_creative_asset(
        self,
        from_world_id: str,
        to_world_id: str,
        asset_type: str,
        asset_data: Dict[str, Any]
    ) -> InterWorldMessage:
        """
        Share a creative asset with another world.
        
        Asset types:
        - template: Reusable content template
        - style_guide: Visual/narrative guidelines
        - workflow: Process definition
        - pattern: Cultural memory pattern
        """
        return self.iwcp.send_message(
            from_world_id=from_world_id,
            to_world_id=to_world_id,
            message_type=MessageType.SHARE_RESOURCE,
            subject=f"Creative Asset: {asset_type}",
            content={
                "asset_type": asset_type,
                "asset_data": asset_data,
                "usage_rights": "unrestricted",
                "attribution_required": True
            },
            priority=MessagePriority.NORMAL
        )
    
    def close(self):
        """Close database sessions."""
        self.session.close()
        self.iwcp.close()


# ============================================================================
# LAYER 3 — INTER-WORLD PROJECT ROUTER (IWPR)
# ============================================================================

class InterWorldProjectRouter:
    """
    LAYER 3: Intelligent project routing across worlds.
    
    Decides:
    - Which world should handle which project
    - Which worlds should collaborate
    - Which agents should migrate temporarily
    - How tasks should be distributed
    
    This ensures every project flows to the best world for the job.
    """
    
    def __init__(self):
        self.session = SessionLocal()
        self.iwcp = InterWorldCommunicationProtocol()
        self.reg = ResourceExchangeGrid()
    
    def route_project(
        self,
        project_type: str,
        requirements: Dict[str, Any],
        preferred_world_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Route a project to the most suitable world(s).
        
        Routing logic considers:
        - World specialization
        - Current workload
        - Agent capabilities
        - Success history
        - Connection strength
        """
        # Get all active worlds
        worlds = self.session.query(World).filter_by(status="active").all()
        
        # Score each world for suitability
        world_scores = []
        for world in worlds:
            score = self._calculate_world_suitability(world, project_type, requirements)
            world_scores.append({
                "world": world,
                "score": score,
                "reasoning": self._get_routing_reasoning(world, project_type, requirements)
            })
        
        # Sort by score
        world_scores.sort(key=lambda x: x["score"], reverse=True)
        
        # Determine if collaboration is needed
        top_world = world_scores[0]
        collaboration_needed = requirements.get("complexity", "simple") in ["complex", "multi-domain"]
        
        routing_decision = {
            "primary_world": top_world["world"].id,
            "primary_world_name": top_world["world"].name,
            "confidence_score": top_world["score"],
            "reasoning": top_world["reasoning"],
            "collaboration_recommended": collaboration_needed,
            "supporting_worlds": []
        }
        
        # If collaboration needed, suggest supporting worlds
        if collaboration_needed and len(world_scores) > 1:
            for candidate in world_scores[1:4]:  # Top 3 supporting worlds
                if candidate["score"] > 0.5:
                    routing_decision["supporting_worlds"].append({
                        "world_id": candidate["world"].id,
                        "world_name": candidate["world"].name,
                        "role": self._suggest_collaboration_role(candidate["world"], requirements)
                    })
        
        return routing_decision
    
    def create_cross_world_project(
        self,
        project_name: str,
        project_type: str,
        lead_world_id: str,
        participating_world_ids: List[str],
        objectives: List[str],
        requirements: Dict[str, Any]
    ) -> CrossWorldProject:
        """
        Create a project spanning multiple worlds.
        """
        project = CrossWorldProject(
            id=f"cwp_{uuid.uuid4().hex[:12]}",
            name=project_name,
            project_type=project_type,
            lead_world_id=lead_world_id,
            description=requirements.get("description", ""),
            objectives=objectives,
            requirements=requirements,
            status="active",
            progress_percentage=0.0,
            target_completion_date=datetime.utcnow() + timedelta(days=requirements.get("duration_days", 30))
        )
        
        self.session.add(project)
        
        # Add participating worlds
        for world_id in participating_world_ids:
            world = self.session.query(World).filter_by(id=world_id).first()
            if world:
                project.participating_worlds.append(world)
        
        # Send collaboration proposals to all participating worlds
        for world_id in participating_world_ids:
            if world_id != lead_world_id:
                self.iwcp.send_message(
                    from_world_id=lead_world_id,
                    to_world_id=world_id,
                    message_type=MessageType.PROPOSE_COLLABORATION,
                    subject=f"Cross-World Project: {project_name}",
                    content={
                        "project_id": project.id,
                        "project_name": project_name,
                        "objectives": objectives,
                        "your_role": requirements.get(f"role_{world_id}", "supporting"),
                        "duration_days": requirements.get("duration_days", 30)
                    },
                    related_project_id=project.id,
                    priority=MessagePriority.HIGH
                )
        
        self.session.commit()
        
        return project
    
    def handoff_workflow(
        self,
        workflow_id: str,
        from_world_id: str,
        to_world_id: str,
        handoff_reason: str
    ) -> InterWorldMessage:
        """
        Hand off a workflow from one world to another.
        
        Used when:
        - Project enters new phase requiring different expertise
        - Original world becomes overloaded
        - Better-suited world becomes available
        """
        workflow = self.session.query(Workflow).filter_by(id=workflow_id).first()
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        return self.iwcp.send_message(
            from_world_id=from_world_id,
            to_world_id=to_world_id,
            message_type=MessageType.WORKFLOW_HANDOFF,
            subject=f"Workflow Handoff: {workflow.workflow_type_id}",
            content={
                "workflow_id": workflow_id,
                "workflow_type": workflow.workflow_type_id,
                "current_status": workflow.status,
                "handoff_reason": handoff_reason,
                "context": workflow.inputs or {},
                "progress_so_far": workflow.execution_metadata or {}
            },
            priority=MessagePriority.HIGH
        )
    
    def _calculate_world_suitability(
        self,
        world: World,
        project_type: str,
        requirements: Dict[str, Any]
    ) -> float:
        """Calculate how suitable a world is for a project (0.0-1.0)."""
        score = 0.0
        
        # Domain match (40% of score)
        if world.primary_domain in requirements.get("required_domains", []):
            score += 0.4
        elif world.specialization and any(
            spec in world.specialization.lower() 
            for spec in requirements.get("keywords", [])
        ):
            score += 0.2
        
        # World type match (20% of score)
        expected_type = requirements.get("world_type")
        if expected_type and world.world_type.value == expected_type:
            score += 0.2
        
        # Performance metrics (20% of score)
        score += (world.creative_output_quality / 100) * 0.1
        score += (world.collaboration_index / 100) * 0.1
        
        # Workload consideration (10% of score)
        if world.population > 0:
            active_projects = self.session.query(CrossWorldProject).filter(
                CrossWorldProject.participating_worlds.any(id=world.id),
                CrossWorldProject.status == "active"
            ).count()
            workload_factor = max(0, 1 - (active_projects / 5))  # Penalize if more than 5 projects
            score += workload_factor * 0.1
        
        # Maturity level (10% of score)
        maturity_scores = {"emerging": 0.05, "established": 0.07, "mature": 0.1, "legendary": 0.1}
        score += maturity_scores.get(world.maturity_level, 0.05)
        
        return min(score, 1.0)
    
    def _get_routing_reasoning(
        self,
        world: World,
        project_type: str,
        requirements: Dict[str, Any]
    ) -> str:
        """Generate human-readable reasoning for routing decision."""
        reasons = []
        
        if world.primary_domain in requirements.get("required_domains", []):
            reasons.append(f"Primary domain match ({world.primary_domain})")
        
        if world.creative_output_quality >= 80:
            reasons.append(f"High quality score ({world.creative_output_quality:.0f}/100)")
        
        if world.collaboration_index >= 80:
            reasons.append(f"Strong collaboration capability")
        
        if world.maturity_level in ["mature", "legendary"]:
            reasons.append(f"{world.maturity_level.capitalize()} world with proven track record")
        
        return "; ".join(reasons) if reasons else "General capability match"
    
    def _suggest_collaboration_role(self, world: World, requirements: Dict[str, Any]) -> str:
        """Suggest a role for a supporting world in collaboration."""
        if "video" in world.primary_domain.lower():
            return "Video production and post-processing"
        elif "story" in world.primary_domain.lower():
            return "Narrative structure and content creation"
        elif "design" in world.primary_domain.lower():
            return "Visual design and asset creation"
        elif "innovation" in world.world_type.value:
            return "Experimental techniques and innovation"
        elif "production" in world.world_type.value:
            return "High-volume execution and optimization"
        else:
            return "Supporting expertise and quality assurance"
    
    def close(self):
        """Close database sessions."""
        self.session.close()
        self.iwcp.close()
        self.reg.close()


# ============================================================================
# LAYER 4 — COSMIC MEMORY SYNCHRONIZER (CMS)
# ============================================================================

class CosmicMemorySynchronizer:
    """
    LAYER 4: Shared memory across all worlds.
    
    Ensures:
    - Identity synchronization across worlds
    - Prevention of drift
    - Breakthrough sharing
    - Lineage distribution
    - Core value alignment
    
    This is how the constellation stays unified while diversifying.
    """
    
    def __init__(self):
        self.session = SessionLocal()
        self.iwcp = InterWorldCommunicationProtocol()
    
    def sync_innovation(
        self,
        originating_world_id: str,
        innovation_type: str,
        innovation_data: Dict[str, Any]
    ) -> List[InterWorldMessage]:
        """
        Broadcast an innovation to all connected worlds.
        
        Innovation types:
        - technique: New creative technique
        - workflow: Improved process
        - pattern: Cultural memory pattern
        - capability: New agent capability
        """
        return self.iwcp.broadcast_message(
            from_world_id=originating_world_id,
            message_type=MessageType.INNOVATION_BROADCAST,
            subject=f"Innovation: {innovation_type}",
            content={
                "innovation_type": innovation_type,
                "innovation_data": innovation_data,
                "originating_world": originating_world_id,
                "adoption_recommended": innovation_data.get("success_rate", 0) > 0.7,
                "discovered_at": datetime.utcnow().isoformat()
            },
            priority=MessagePriority.HIGH
        )
    
    def sync_core_values(
        self,
        sovereign_world_id: str = "dominion_prime",
        updated_values: Dict[str, Any] = None
    ) -> List[InterWorldMessage]:
        """
        Synchronize core values from sovereign world to all worlds.
        
        Ensures all worlds stay aligned with Dominion's identity.
        """
        sovereign = self.session.query(World).filter_by(id=sovereign_world_id).first()
        if not sovereign:
            raise ValueError(f"Sovereign world {sovereign_world_id} not found")
        
        return self.iwcp.broadcast_message(
            from_world_id=sovereign_world_id,
            message_type=MessageType.SYNC_MEMORY,
            subject="Core Values Synchronization",
            content={
                "sync_type": "core_values",
                "values": updated_values or sovereign.culture.get("core_values", []),
                "identity": sovereign.culture.get("motto", ""),
                "mandatory_compliance": True,
                "effective_date": datetime.utcnow().isoformat()
            },
            priority=MessagePriority.CRITICAL
        )
    
    def escalate_decision(
        self,
        requesting_world_id: str,
        decision_type: str,
        decision_context: Dict[str, Any],
        escalation_reason: str
    ) -> InterWorldMessage:
        """
        Escalate a decision to the sovereign world (Dominion Prime).
        
        Used when:
        - Decision affects multiple worlds
        - Decision violates world constraints
        - Decision requires sovereign authority
        - Decision has cross-cosmos implications
        """
        return self.iwcp.send_message(
            from_world_id=requesting_world_id,
            to_world_id="dominion_prime",
            message_type=MessageType.ESCALATE_DECISION,
            subject=f"Decision Escalation: {decision_type}",
            content={
                "decision_type": decision_type,
                "context": decision_context,
                "escalation_reason": escalation_reason,
                "requesting_world": requesting_world_id,
                "urgency": decision_context.get("urgency", "normal")
            },
            priority=MessagePriority.URGENT
        )
    
    def get_cosmic_memory_snapshot(self) -> Dict[str, Any]:
        """
        Get a snapshot of the entire cosmos's shared memory.
        
        Includes:
        - All worlds and their status
        - Active connections
        - Recent innovations
        - Core values
        - Active projects
        """
        worlds = self.session.query(World).all()
        connections = self.session.query(InterWorldConnection).filter_by(status="active").all()
        projects = self.session.query(CrossWorldProject).filter_by(status="active").all()
        migrations = self.session.query(AgentMigration).filter_by(status="active").all()
        
        return {
            "snapshot_time": datetime.utcnow().isoformat(),
            "total_worlds": len(worlds),
            "active_connections": len(connections),
            "active_projects": len(projects),
            "active_migrations": len(migrations),
            "worlds": [
                {
                    "id": w.id,
                    "name": w.name,
                    "type": w.world_type.value,
                    "domain": w.primary_domain,
                    "population": w.population,
                    "maturity": w.maturity_level,
                    "quality": w.creative_output_quality
                }
                for w in worlds
            ],
            "network_health": self._calculate_network_health(worlds, connections)
        }
    
    def _calculate_network_health(
        self,
        worlds: List[World],
        connections: List[InterWorldConnection]
    ) -> Dict[str, Any]:
        """Calculate overall health metrics of the Inter-World Network."""
        if not worlds:
            return {"status": "no_worlds", "score": 0.0}
        
        total_possible_connections = len(worlds) * (len(worlds) - 1)
        connection_density = len(connections) / total_possible_connections if total_possible_connections > 0 else 0
        
        avg_quality = sum(w.creative_output_quality for w in worlds) / len(worlds)
        avg_collaboration = sum(w.collaboration_index for w in worlds) / len(worlds)
        
        health_score = (connection_density * 0.3 + (avg_quality / 100) * 0.4 + (avg_collaboration / 100) * 0.3)
        
        if health_score >= 0.8:
            status = "excellent"
        elif health_score >= 0.6:
            status = "good"
        elif health_score >= 0.4:
            status = "fair"
        else:
            status = "needs_attention"
        
        return {
            "status": status,
            "score": round(health_score, 3),
            "connection_density": round(connection_density, 3),
            "avg_quality": round(avg_quality, 1),
            "avg_collaboration": round(avg_collaboration, 1),
            "recommendations": self._get_health_recommendations(health_score, connection_density, avg_quality)
        }
    
    def _get_health_recommendations(
        self,
        health_score: float,
        connection_density: float,
        avg_quality: float
    ) -> List[str]:
        """Generate recommendations for improving network health."""
        recommendations = []
        
        if connection_density < 0.3:
            recommendations.append("Increase inter-world connections to improve collaboration")
        
        if avg_quality < 70:
            recommendations.append("Focus on quality improvement across worlds")
        
        if health_score < 0.5:
            recommendations.append("Consider world consolidation or specialization refinement")
        
        if not recommendations:
            recommendations.append("Network is healthy - continue current operations")
        
        return recommendations
    
    def close(self):
        """Close database sessions."""
        self.session.close()
        self.iwcp.close()


# ============================================================================
# UNIFIED IWN INTERFACE
# ============================================================================

class InterWorldNetwork:
    """
    Unified interface to the complete Inter-World Network.
    
    Provides access to all 4 layers:
    - IWCP: Communication Protocol
    - REG: Resource Exchange Grid
    - IWPR: Project Router
    - CMS: Cosmic Memory Synchronizer
    """
    
    def __init__(self):
        self.iwcp = InterWorldCommunicationProtocol()
        self.reg = ResourceExchangeGrid()
        self.iwpr = InterWorldProjectRouter()
        self.cms = CosmicMemorySynchronizer()
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the Inter-World Network."""
        memory_snapshot = self.cms.get_cosmic_memory_snapshot()
        
        return {
            "network_name": "Inter-World Network (IWN)",
            "status": "operational",
            "layers": {
                "iwcp": "Inter-World Communication Protocol - ACTIVE",
                "reg": "Resource Exchange Grid - ACTIVE",
                "iwpr": "Inter-World Project Router - ACTIVE",
                "cms": "Cosmic Memory Synchronizer - ACTIVE"
            },
            "cosmos_snapshot": memory_snapshot,
            "capabilities": [
                "Cross-world messaging",
                "Agent migration",
                "Resource sharing",
                "Intelligent project routing",
                "Innovation broadcasting",
                "Memory synchronization",
                "Decision escalation",
                "Workflow handoff"
            ]
        }
    
    def close(self):
        """Close all database sessions."""
        self.iwcp.close()
        self.reg.close()
        self.iwpr.close()
        self.cms.close()
