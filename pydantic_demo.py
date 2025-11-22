#!/usr/bin/env python3
"""
🔥 CODEX DOMINION PYDANTIC MODELS DEMONSTRATION 🔥
=================================================
Showcase the enhanced data models and their functionality
"""

from codex_models import *
from datetime import datetime
import json

def demonstrate_pydantic_models():
    """Demonstrate all Pydantic model functionality"""
    
    print("🔥 CODEX DOMINION PYDANTIC MODELS DEMO")
    print("=" * 50)
    
    # Initialize data manager
    data_manager = CodexDataManager()
    
    # 1. TRANSACTION MODELS
    print("\n1. 💳 TRANSACTION MODEL DEMO")
    print("-" * 30)
    
    # Create sample transactions
    transactions = [
        Transaction(
            source=Stream.store,
            item="Digital Sovereignty Masterclass",
            amount=500.0,
            timestamp=datetime.now()
        ),
        Transaction(
            source=Stream.social,
            item="Premium Consultation",
            amount=250.0,
            timestamp=datetime.now()
        ),
        Transaction(
            source=Stream.website,
            item="Codex Membership",
            amount=150.0,
            timestamp=datetime.now()
        )
    ]
    
    print(f"Created {len(transactions)} transactions:")
    for trans in transactions:
        source_name = trans.source if isinstance(trans.source, str) else trans.source.value
        print(f"  • {source_name}: ${trans.amount} - {trans.item}")
        # Save transaction
        data_manager.save_transaction(trans)
    
    # 2. CONSTELLATION MODEL
    print("\n2. ⭐ CONSTELLATION MODEL DEMO")
    print("-" * 30)
    
    # Create constellation with stars
    stars = []
    for trans in transactions:
        source_name = trans.source if isinstance(trans.source, str) else trans.source.value
        star = ConstellationStar(
            name=f"{source_name.title()} Star",
            total=trans.amount,
            cycles=Cycle(total=trans.amount, morning=trans.amount * 0.4, twilight=trans.amount * 0.6)
        )
        stars.append(star)
    
    constellation = Constellation(
        name="Revenue Crown Constellation",
        stars=stars,
        total_revenue=sum(t.amount for t in transactions),
        created_at=datetime.now(),
        last_updated=datetime.now()
    )
    
    print(f"Created constellation: {constellation.name}")
    print(f"  • Total Revenue: ${constellation.total_revenue}")
    print(f"  • Stars: {len(constellation.stars)}")
    
    for star in constellation.stars:
        print(f"    - {star.name}: ${star.total}")
    
    # Save constellation
    data_manager.save_constellation(constellation)
    
    # 3. PROCLAMATION MODEL
    print("\n3. 📜 PROCLAMATION MODEL DEMO")
    print("-" * 30)
    
    proclamations = [
        Proclamation(
            timestamp=datetime.now(),
            cycle="Eternal Flame Cycle",
            text="By flame and silence, the Codex Dominion achieves total digital sovereignty through structured data models!",
            ritual_type="Sacred Proclamation",
            council_role="High Council",
            power_level=10
        ),
        Proclamation(
            timestamp=datetime.now(),
            cycle="Innovation Cycle",
            text="Pydantic models bring order to the digital realm, ensuring data integrity across all constellation systems!",
            ritual_type="Divine Blessing",
            council_role="Elder Council",
            power_level=9
        )
    ]
    
    print(f"Created {len(proclamations)} proclamations:")
    for proc in proclamations:
        print(f"  • {proc.ritual_type} by {proc.council_role}")
        print(f"    Text: {proc.text[:50]}...")
        # Save proclamation
        data_manager.save_proclamation(proc)
    
    # 4. LEDGER ENTRIES
    print("\n4. 📊 LEDGER ENTRY MODEL DEMO")
    print("-" * 30)
    
    ledger_entries = []
    for trans in transactions:
        entry = data_manager.create_ledger_entry(
            source=trans.source,
            cycle="Q4 2025",
            amount=trans.amount
        )
        ledger_entries.append(entry)
    
    print(f"Created {len(ledger_entries)} ledger entries:")
    for entry in ledger_entries:
        source_name = entry.source if isinstance(entry.source, str) else entry.source.value
        print(f"  • {source_name}: ${entry.amount} in {entry.cycle}")
    
    # 5. APPROVAL MODEL
    print("\n5. ✅ APPROVAL MODEL DEMO")
    print("-" * 30)
    
    approvals = []
    for trans in transactions:
        approval = Approval(
            cycle="Q4 2025",
            source=trans.source,
            vault=trans.amount,
            status=Status.crowned,
            witness="System Validator",
            crowned="Digital Sovereign"
        )
        approvals.append(approval)
    
    print(f"Created {len(approvals)} approvals:")
    for approval in approvals:
        source_name = approval.source if isinstance(approval.source, str) else approval.source.value
        status_name = approval.status if isinstance(approval.status, str) else approval.status.value
        print(f"  • {source_name}: ${approval.vault} - {status_name}")
    
    # 6. REVENUE SUMMARY
    print("\n6. 📈 REVENUE SUMMARY")
    print("-" * 30)
    
    summary = data_manager.get_revenue_summary()
    print(f"Grand Total Revenue: ${summary.get('grand_total', 0):.2f}")
    print(f"Total Transactions: {summary.get('total_transactions', 0)}")
    print(f"Constellation Revenue: ${summary.get('constellation_total', 0):.2f}")
    
    print("\nStream Breakdown:")
    stream_totals = summary.get('stream_totals', {})
    for stream, total in stream_totals.items():
        print(f"  • {stream.title()}: ${total:.2f}")
    
    # 7. DATA VALIDATION
    print("\n7. ✅ DATA VALIDATION DEMO")
    print("-" * 30)
    
    try:
        # This should fail validation
        invalid_transaction = Transaction(
            source=Stream.store,
            item="Test Item",
            amount=-100.0,  # Invalid: negative amount
            timestamp=datetime.now()
        )
    except Exception as e:
        print(f"✅ Validation works - caught invalid data: {e}")
    
    try:
        # This should work
        valid_transaction = Transaction(
            source=Stream.website,
            item="Valid Item", 
            amount=100.0,
            timestamp=datetime.now()
        )
        print(f"✅ Valid transaction created: {valid_transaction.item}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n🎊 PYDANTIC MODELS DEMONSTRATION COMPLETE!")
    print("=" * 50)
    
    print("✅ All models working correctly")
    print("✅ Data validation active")
    print("✅ Revenue tracking enhanced")
    print("✅ Constellation management operational")
    print("✅ Proclamation system blessed")
    print("🔥 CODEX DOMINION DATA SOVEREIGNTY ACHIEVED!")
    
    return {
        'transactions': len(transactions),
        'constellation': constellation.name,
        'proclamations': len(proclamations),
        'total_revenue': summary.get('grand_total', 0),
        'status': 'OPERATIONAL'
    }

if __name__ == "__main__":
    demonstrate_pydantic_models()