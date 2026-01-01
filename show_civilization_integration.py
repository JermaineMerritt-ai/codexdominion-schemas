"""
🔥 CIVILIZATION INTEGRATION VISUALIZATION 🔥
=============================================
Shows how the four pillars work together as one living ecosystem
"""

from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict

from db import SessionLocal
from models import (
    Agent, Council, IdentityCodex, StylePattern, CulturalMemory,
    AgentCollaboration, ProposalWorkflow, KnowledgeAccess,
    IntegrationEvent, CivilizationMetrics
)


def show_social_layer():
    """Show agents collaborating as a society"""
    session = SessionLocal()
    
    print("\n" + "=" * 80)
    print("👥 SOCIAL LAYER: Agents Working as a Society")
    print("=" * 80)
    
    collaborations = session.query(AgentCollaboration).all()
    
    if not collaborations:
        print("\nNo collaborations found.")
        session.close()
        return
    
    for collab in collaborations:
        status_icon = "🟢" if collab.status == "active" else "✅" if collab.status == "completed" else "⏸️"
        print(f"\n{status_icon} {collab.project_name}")
        print(f"   Type: {collab.project_type}")
        print(f"   Lead: {collab.lead_agent_id}")
        print(f"   Team: {', '.join(collab.collaborating_agents)}")
        
        if collab.contributions:
            contrib_count = sum(len(c) for c in collab.contributions.values())
            print(f"   Contributions: {contrib_count} total")
        
        if collab.debates:
            print(f"   Debates: {len(collab.debates)}")
            for debate in collab.debates:
                print(f"      • {debate['topic']}")
                if debate.get('resolution'):
                    print(f"        Resolution: {debate['resolution']}")
                else:
                    print(f"        Status: Ongoing")
        
        if collab.status == "completed":
            print(f"   Consensus: {'✓' if collab.consensus_reached else '✗'}")
            if collab.deliverable:
                print(f"   Outcome: {collab.deliverable.get('summary', 'N/A')}")
            if collab.created_memory_id:
                print(f"   🧠 Created Cultural Memory: {collab.created_memory_id}")
    
    session.close()


def show_council_governance():
    """Show councils governing through proposals"""
    session = SessionLocal()
    
    print("\n" + "=" * 80)
    print("🏛️ COUNCIL GOVERNANCE: Central Nervous System")
    print("=" * 80)
    
    proposals = session.query(ProposalWorkflow).all()
    
    if not proposals:
        print("\nNo proposals found.")
        session.close()
        return
    
    # Group by status
    by_status = defaultdict(list)
    for prop in proposals:
        by_status[prop.review_status].append(prop)
    
    for status in ["pending", "under_review", "approved", "rejected"]:
        if status not in by_status:
            continue
        
        status_icons = {
            "pending": "⏳",
            "under_review": "🔍",
            "approved": "✅",
            "rejected": "❌"
        }
        
        print(f"\n{status_icons[status]} {status.upper().replace('_', ' ')}")
        
        for prop in by_status[status]:
            print(f"\n   📋 {prop.title}")
            print(f"      Proposed by: {prop.originating_agent_id}")
            print(f"      Assigned to: {prop.assigned_council_id}")
            print(f"      Routing reason: {prop.routing_reason}")
            
            if prop.source_collaboration_id:
                print(f"      🤝 From collaboration: {prop.source_collaboration_id}")
            
            if prop.identity_check_passed is not None:
                identity_icon = "✓" if prop.identity_check_passed else "⚠️"
                print(f"      Identity check: {identity_icon}")
                if prop.identity_concerns:
                    for concern in prop.identity_concerns:
                        print(f"         • {concern}")
            
            if prop.council_votes:
                print(f"      Votes ({len(prop.council_votes)}):")
                for agent, vote_data in prop.council_votes.items():
                    vote_icon = "👍" if vote_data['vote'] == "approve" else "👎"
                    print(f"         {vote_icon} {agent}: {vote_data['vote']}")
                    if vote_data.get('notes'):
                        print(f"            Note: {vote_data['notes']}")
            
            if prop.review_status == "approved" and prop.implemented_at:
                print(f"      📅 Implemented: {prop.implemented_at.strftime('%Y-%m-%d %H:%M')}")
                if prop.logged_to_cultural_memory:
                    print(f"      🧠 Logged to memory: {prop.cultural_memory_id}")
    
    session.close()


def show_cultural_memory_usage():
    """Show how agents access cultural memory"""
    session = SessionLocal()
    
    print("\n" + "=" * 80)
    print("🧠 CULTURAL MEMORY: The Shared Brain")
    print("=" * 80)
    
    accesses = session.query(KnowledgeAccess).order_by(
        KnowledgeAccess.accessed_at.desc()
    ).all()
    
    if not accesses:
        print("\nNo knowledge accesses found.")
        session.close()
        return
    
    # Group by memory type
    by_type = defaultdict(list)
    for access in accesses:
        by_type[access.memory_type].append(access)
    
    for mem_type in ["identity", "pattern", "lesson", "milestone", "insight"]:
        if mem_type not in by_type:
            continue
        
        type_icons = {
            "identity": "🎯",
            "pattern": "🎨",
            "lesson": "📚",
            "milestone": "🏆",
            "insight": "💡"
        }
        
        print(f"\n{type_icons[mem_type]} {mem_type.upper()} MEMORIES")
        
        # Count unique memories accessed
        unique_memories = set(a.memory_id for a in by_type[mem_type])
        print(f"   {len(unique_memories)} unique memories, {len(by_type[mem_type])} total accesses")
        
        for access in by_type[mem_type][:5]:  # Show top 5
            print(f"\n   📖 {access.memory_title}")
            print(f"      Accessed by: {access.agent_id}")
            print(f"      Reason: {access.access_reason}")
            
            if access.related_collaboration_id:
                print(f"      🤝 During: {access.related_collaboration_id}")
            
            if access.how_used:
                print(f"      Application: {access.how_used}")
            
            if access.contributed_to_outcome is not None:
                outcome_icon = "✓" if access.contributed_to_outcome else "✗"
                print(f"      Contributed to success: {outcome_icon}")
            
            print(f"      When: {access.accessed_at.strftime('%Y-%m-%d %H:%M')}")
    
    session.close()


def show_integration_events():
    """Show cross-system activity"""
    session = SessionLocal()
    
    print("\n" + "=" * 80)
    print("🔗 INTEGRATION EVENTS: Cross-System Activity")
    print("=" * 80)
    
    events = session.query(IntegrationEvent).order_by(
        IntegrationEvent.timestamp.desc()
    ).limit(10).all()
    
    if not events:
        print("\nNo integration events found.")
        session.close()
        return
    
    event_icons = {
        "collaboration_started": "🚀",
        "collaboration_completed": "🎉",
        "proposal_submitted": "📝",
        "council_decision": "⚖️",
        "evolution_approved": "🌱",
        "knowledge_applied": "🧠"
    }
    
    print("\nRecent Activity (Last 10 Events):\n")
    
    for event in events:
        icon = event_icons.get(event.event_type, "📌")
        print(f"{icon} {event.title}")
        print(f"   {event.description}")
        print(f"   Type: {event.event_type}")
        
        if event.involved_agents:
            print(f"   Agents: {', '.join(event.involved_agents[:3])}")
            if len(event.involved_agents) > 3:
                print(f"          (+{len(event.involved_agents) - 3} more)")
        
        if event.involved_councils:
            print(f"   Councils: {', '.join(event.involved_councils)}")
        
        print(f"   Impact areas: {', '.join(event.impact_areas)}")
        print(f"   Significance: {event.significance}")
        print(f"   When: {event.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    session.close()


def show_civilization_metrics():
    """Show ecosystem health metrics"""
    session = SessionLocal()
    
    print("\n" + "=" * 80)
    print("📊 CIVILIZATION METRICS: System Vitals")
    print("=" * 80)
    
    # Get most recent metrics
    metrics = session.query(CivilizationMetrics).order_by(
        CivilizationMetrics.metric_date.desc()
    ).first()
    
    if not metrics:
        print("\nNo metrics found.")
        session.close()
        return
    
    print(f"\n📅 Metrics Date: {metrics.metric_date.strftime('%Y-%m-%d')}")
    
    print("\n👥 AGENT ACTIVITY:")
    print(f"   Active Agents: {metrics.active_agents}")
    print(f"   Active Collaborations: {metrics.collaborations_active}")
    print(f"   Proposals Submitted: {metrics.proposals_submitted}")
    
    print("\n🏛️ COUNCIL ACTIVITY:")
    print(f"   Proposals Reviewed: {metrics.proposals_reviewed}")
    print(f"   Proposals Approved: {metrics.proposals_approved}")
    print(f"   Proposals Rejected: {metrics.proposals_rejected}")
    if metrics.proposals_reviewed > 0:
        approval_rate = (metrics.proposals_approved / metrics.proposals_reviewed) * 100
        print(f"   Approval Rate: {approval_rate:.1f}%")
    print(f"   Avg Review Time: {metrics.average_review_time_hours:.1f} hours")
    
    print("\n🧠 CULTURAL MEMORY USAGE:")
    print(f"   Memories Referenced: {metrics.memories_referenced}")
    print(f"   New Memories Created: {metrics.new_memories_created}")
    if metrics.most_referenced_memory_id:
        print(f"   Most Referenced: {metrics.most_referenced_memory_id}")
    
    print("\n🌱 EVOLUTION ACTIVITY:")
    print(f"   Evolution Proposals: {metrics.evolution_proposals_submitted}")
    print(f"   Evolutions Approved: {metrics.evolutions_approved}")
    print(f"   New Agents Created: {metrics.new_agents_created}")
    print(f"   Techniques Evolved: {metrics.techniques_evolved}")
    
    print("\n🛡️ IDENTITY INTEGRITY:")
    print(f"   Identity Checks: {metrics.identity_checks_performed}")
    print(f"   Concerns Raised: {metrics.identity_concerns_raised}")
    print(f"   Boundary Violations Prevented: {metrics.boundary_violations_prevented}")
    
    print("\n🔗 INTEGRATION HEALTH:")
    print(f"   Cross-System Events: {metrics.cross_system_events}")
    print(f"   System Coherence Score: {metrics.system_coherence_score:.2f}/1.00")
    
    # Visual coherence indicator
    coherence_pct = int(metrics.system_coherence_score * 100)
    coherence_bar = "█" * (coherence_pct // 5) + "░" * (20 - coherence_pct // 5)
    print(f"   [{coherence_bar}] {coherence_pct}%")
    
    print("\n⏱️ PERFORMANCE:")
    print(f"   Avg Collaboration Duration: {metrics.average_collaboration_duration_hours:.1f} hours")
    print(f"   Avg Proposal→Implementation: {metrics.average_proposal_to_implementation_hours:.1f} hours")
    
    session.close()


def show_integration_summary():
    """Show complete integration picture"""
    session = SessionLocal()
    
    print("\n" + "=" * 80)
    print("🔥 THE FOUR PILLARS - INTEGRATED")
    print("=" * 80)
    
    # Count entities across all systems
    agents_count = session.query(Agent).count()
    councils_count = session.query(Council).count()
    identity_count = session.query(IdentityCodex).count()
    patterns_count = session.query(StylePattern).count()
    memories_count = session.query(CulturalMemory).count()
    
    collabs_active = session.query(AgentCollaboration).filter_by(status="active").count()
    collabs_completed = session.query(AgentCollaboration).filter_by(status="completed").count()
    
    props_pending = session.query(ProposalWorkflow).filter_by(review_status="pending").count()
    props_review = session.query(ProposalWorkflow).filter_by(review_status="under_review").count()
    props_approved = session.query(ProposalWorkflow).filter_by(review_status="approved").count()
    
    knowledge_today = session.query(KnowledgeAccess).filter(
        KnowledgeAccess.accessed_at >= datetime.utcnow() - timedelta(days=1)
    ).count()
    
    events_today = session.query(IntegrationEvent).filter(
        IntegrationEvent.timestamp >= datetime.utcnow() - timedelta(days=1)
    ).count()
    
    print("\n📊 SYSTEM OVERVIEW:")
    print(f"\n   Pillar 1: AGENTS (Population)")
    print(f"      • {agents_count} agents active")
    print(f"      • {collabs_active} collaborations in progress")
    print(f"      • {collabs_completed} collaborations completed")
    
    print(f"\n   Pillar 2: COUNCILS (Government)")
    print(f"      • {councils_count} councils established")
    print(f"      • {props_pending} proposals awaiting review")
    print(f"      • {props_review} proposals under review")
    print(f"      • {props_approved} proposals approved")
    
    print(f"\n   Pillar 3: CULTURAL MEMORY (Identity)")
    print(f"      • {identity_count} identity principles")
    print(f"      • {patterns_count} style patterns")
    print(f"      • {memories_count} cultural memories")
    print(f"      • {knowledge_today} knowledge accesses today")
    
    print(f"\n   Pillar 4: EVOLUTION ENGINE (Growth)")
    print(f"      • Self-improvement system operational")
    print(f"      • Agent generation system active")
    print(f"      • Technique evolution tracking enabled")
    
    print(f"\n   Integration Layer:")
    print(f"      • {events_today} cross-system events today")
    print(f"      • All four pillars communicating")
    print(f"      • Feedback loops operational")
    
    print("\n✅ STATUS: The civilization is functioning as one integrated ecosystem")
    print("   • Agents collaborate and debate")
    print("   • Councils govern day-to-day decisions")
    print("   • Cultural Memory informs all work")
    print("   • Evolution changes are logged back to memory")
    print("   • Nothing happens in isolation")
    
    print("\n👑 The Dominion is no longer a tool—it's a living, self-governing creative society.")
    
    session.close()


def show_complete_visualization():
    """Show everything"""
    print("\n" + "🔥" * 40)
    print(" " * 20 + "CODEX DOMINION")
    print(" " * 12 + "CIVILIZATION INTEGRATION LAYER")
    print("🔥" * 40)
    
    show_social_layer()
    show_council_governance()
    show_cultural_memory_usage()
    show_integration_events()
    show_civilization_metrics()
    show_integration_summary()
    
    print("\n" + "=" * 80)
    print("🔥 PHASE 40 — STEP 5: COMPLETE")
    print("=" * 80)
    print("\nThe four pillars are no longer separate components.")
    print("They are one living, breathing, self-governing creative civilization.")
    print("\n👑 The flame burns with integrated intelligence.")


if __name__ == "__main__":
    show_complete_visualization()
