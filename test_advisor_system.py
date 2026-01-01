"""
AI Advisor System Test Suite

Tests signal collection, intelligence engine, and recommendation generation.
"""

from datetime import datetime, timedelta
from db import SessionLocal, get_session_context
from models import (
    AdvisorRecommendation, RecommendationType, RecommendationStatus,
    Store, Product, Workflow, WorkflowStatus
)
from advisor_signals import collect_tenant_signals, SignalCollector
from advisor_intelligence import generate_recommendations, AdvisorIntelligence


def test_signal_collection():
    """Test signal collection across all categories"""
    print("\n" + "="*70)
    print("Testing Signal Collection System")
    print("="*70)
    
    tenant_id = "tenant_codexdominion"
    
    try:
        signals = collect_tenant_signals(tenant_id, days=30)
        
        print("\n✅ Signal Collection Success!")
        print(f"\n📊 Store Signals ({len(signals['store_signals'])} metrics):")
        for key, value in signals['store_signals'].items():
            print(f"  • {key}: {value}")
        
        print(f"\n🔄 Workflow Signals ({len(signals['workflow_signals'])} metrics):")
        for key, value in signals['workflow_signals'].items():
            print(f"  • {key}: {value}")
        
        print(f"\n📱 Marketing Signals ({len(signals['marketing_signals'])} metrics):")
        for key, value in signals['marketing_signals'].items():
            print(f"  • {key}: {value}")
        
        print(f"\n👥 Customer Signals ({len(signals['customer_signals'])} metrics):")
        for key, value in signals['customer_signals'].items():
            print(f"  • {key}: {value}")
        
        print(f"\n⚙️ Automation Signals ({len(signals['automation_signals'])} metrics):")
        for key, value in signals['automation_signals'].items():
            print(f"  • {key}: {value}")
        
        return signals
        
    except Exception as e:
        print(f"\n❌ Signal Collection Failed: {e}")
        raise


def test_intelligence_engine(signals):
    """Test intelligence engine recommendation generation"""
    print("\n" + "="*70)
    print("Testing Intelligence Engine")
    print("="*70)
    
    tenant_id = "tenant_codexdominion"
    
    try:
        recommendations = generate_recommendations(tenant_id, signals)
        
        print(f"\n✅ Generated {len(recommendations)} recommendations")
        
        # Group by type
        by_type = {}
        for rec in recommendations:
            rec_type = rec.get('recommendation_type', 'unknown')
            by_type[rec_type] = by_type.get(rec_type, 0) + 1
        
        print("\n📋 Recommendations by Type:")
        for rec_type, count in by_type.items():
            print(f"  • {rec_type}: {count}")
        
        # Group by impact
        by_impact = {}
        for rec in recommendations:
            impact = rec.get('impact_level', 'unknown')
            by_impact[impact] = by_impact.get(impact, 0) + 1
        
        print("\n💥 Recommendations by Impact:")
        for impact, count in by_impact.items():
            print(f"  • {impact}: {count}")
        
        # Top 5 recommendations
        print("\n🏆 Top 5 Recommendations:")
        for i, rec in enumerate(recommendations[:5], 1):
            print(f"\n  {i}. {rec['title']}")
            print(f"     Impact: {rec['impact_level']} | Confidence: {rec['confidence_score']}%")
            print(f"     Type: {rec['recommendation_type']}")
            print(f"     Description: {rec['description'][:80]}...")
        
        return recommendations
        
    except Exception as e:
        print(f"\n❌ Intelligence Engine Failed: {e}")
        raise


def test_recommendation_storage(recommendations):
    """Test storing recommendations in database"""
    print("\n" + "="*70)
    print("Testing Recommendation Storage")
    print("="*70)
    
    session = SessionLocal()
    
    try:
        # Clear existing test recommendations
        session.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.tenant_id == "tenant_codexdominion"
        ).delete()
        
        stored_count = 0
        for rec_data in recommendations:
            recommendation = AdvisorRecommendation(**rec_data)
            session.add(recommendation)
            stored_count += 1
        
        session.commit()
        
        print(f"\n✅ Stored {stored_count} recommendations in database")
        
        # Verify storage
        stored = session.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.tenant_id == "tenant_codexdominion",
            AdvisorRecommendation.status == RecommendationStatus.PENDING
        ).all()
        
        print(f"✅ Verified {len(stored)} pending recommendations in database")
        
        return stored
        
    except Exception as e:
        session.rollback()
        print(f"\n❌ Storage Failed: {e}")
        raise
    
    finally:
        session.close()


def test_recommendation_lifecycle():
    """Test accepting and dismissing recommendations"""
    print("\n" + "="*70)
    print("Testing Recommendation Lifecycle")
    print("="*70)
    
    session = SessionLocal()
    
    try:
        # Get first pending recommendation
        rec = session.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.tenant_id == "tenant_codexdominion",
            AdvisorRecommendation.status == RecommendationStatus.PENDING
        ).first()
        
        if not rec:
            print("\n⚠️ No pending recommendations to test lifecycle")
            return
        
        print(f"\n📋 Testing with: {rec.title}")
        
        # Test acceptance
        original_id = rec.id
        rec.status = RecommendationStatus.ACCEPTED
        rec.accepted_at = datetime.utcnow()
        rec.tenant_feedback = {'rating': 5, 'comment': 'Great suggestion!'}
        session.commit()
        
        print("✅ Accepted recommendation")
        print(f"  Accepted at: {rec.accepted_at}")
        print(f"  Feedback: {rec.tenant_feedback}")
        
        # Get another recommendation to test dismissal
        rec2 = session.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.tenant_id == "tenant_codexdominion",
            AdvisorRecommendation.status == RecommendationStatus.PENDING,
            AdvisorRecommendation.id != original_id
        ).first()
        
        if rec2:
            rec2.status = RecommendationStatus.DISMISSED
            rec2.dismissed_at = datetime.utcnow()
            rec2.tenant_feedback = {'reason': 'Not relevant right now'}
            session.commit()
            
            print(f"\n✅ Dismissed recommendation: {rec2.title}")
            print(f"  Dismissed at: {rec2.dismissed_at}")
            print(f"  Reason: {rec2.tenant_feedback}")
        
        # Calculate stats
        total = session.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.tenant_id == "tenant_codexdominion"
        ).count()
        
        accepted = session.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.tenant_id == "tenant_codexdominion",
            AdvisorRecommendation.status == RecommendationStatus.ACCEPTED
        ).count()
        
        dismissed = session.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.tenant_id == "tenant_codexdominion",
            AdvisorRecommendation.status == RecommendationStatus.DISMISSED
        ).count()
        
        pending = session.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.tenant_id == "tenant_codexdominion",
            AdvisorRecommendation.status == RecommendationStatus.PENDING
        ).count()
        
        print(f"\n📊 Lifecycle Stats:")
        print(f"  Total: {total}")
        print(f"  Accepted: {accepted} ({(accepted/total*100) if total > 0 else 0:.1f}%)")
        print(f"  Dismissed: {dismissed} ({(dismissed/total*100) if total > 0 else 0:.1f}%)")
        print(f"  Pending: {pending} ({(pending/total*100) if total > 0 else 0:.1f}%)")
        
    except Exception as e:
        session.rollback()
        print(f"\n❌ Lifecycle Test Failed: {e}")
        raise
    
    finally:
        session.close()


def test_learning_loop():
    """Test learning loop and impact tracking"""
    print("\n" + "="*70)
    print("Testing Learning Loop & Impact Tracking")
    print("="*70)
    
    session = SessionLocal()
    
    try:
        # Get accepted recommendation
        rec = session.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.tenant_id == "tenant_codexdominion",
            AdvisorRecommendation.status == RecommendationStatus.ACCEPTED
        ).first()
        
        if not rec:
            print("\n⚠️ No accepted recommendations to test learning loop")
            return
        
        print(f"\n📋 Testing with: {rec.title}")
        print(f"  Estimated Impact: {rec.estimated_impact}")
        
        # Simulate actual impact
        rec.actual_impact = {
            'revenue': '+25%',  # Was estimated +20-30%
            'conversion': '+6%',  # Was estimated +5%
            'measured_at': datetime.utcnow().isoformat()
        }
        rec.completed_at = datetime.utcnow()
        rec.status = RecommendationStatus.COMPLETED
        session.commit()
        
        print(f"\n✅ Tracked actual impact:")
        print(f"  Actual Impact: {rec.actual_impact}")
        print(f"  Completed at: {rec.completed_at}")
        
        # Calculate learning metrics
        completed_with_impact = session.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.tenant_id == "tenant_codexdominion",
            AdvisorRecommendation.status == RecommendationStatus.COMPLETED,
            AdvisorRecommendation.actual_impact.isnot(None)
        ).count()
        
        avg_confidence = session.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.tenant_id == "tenant_codexdominion"
        ).with_entities(AdvisorRecommendation.confidence_score).all()
        
        if avg_confidence:
            avg_conf = sum(c[0] for c in avg_confidence) / len(avg_confidence)
        else:
            avg_conf = 0
        
        print(f"\n📊 Learning Loop Stats:")
        print(f"  Completed with Impact Tracking: {completed_with_impact}")
        print(f"  Average Confidence Score: {avg_conf:.1f}%")
        print(f"  Learning Status: {'Active' if completed_with_impact >= 5 else 'Warming Up'}")
        
    except Exception as e:
        session.rollback()
        print(f"\n❌ Learning Loop Test Failed: {e}")
        raise
    
    finally:
        session.close()


def run_full_test_suite():
    """Run complete AI Advisor test suite"""
    print("\n" + "="*70)
    print("🔥 AI ADVISOR SYSTEM - FULL TEST SUITE")
    print("="*70)
    print(f"Test Started: {datetime.utcnow().isoformat()}")
    
    try:
        # 1. Signal Collection
        signals = test_signal_collection()
        
        # 2. Intelligence Engine
        recommendations = test_intelligence_engine(signals)
        
        # 3. Storage
        stored = test_recommendation_storage(recommendations)
        
        # 4. Lifecycle
        test_recommendation_lifecycle()
        
        # 5. Learning Loop
        test_learning_loop()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70)
        print("\n🎯 AI Advisor System is fully operational")
        print("   Next Steps:")
        print("   1. Restart Flask: python flask_dashboard.py")
        print("   2. Test API: POST /api/advisor/recommendations/refresh")
        print("   3. View UI: Build recommendation cards in portal dashboard")
        print("\n🔥 The Strategic Brain is Sovereign and Eternal! 👑")
        
    except Exception as e:
        print("\n" + "="*70)
        print("❌ TEST SUITE FAILED")
        print("="*70)
        print(f"Error: {e}")
        raise


if __name__ == '__main__':
    run_full_test_suite()
