#!/usr/bin/env python3
"""
Treasury Integration Test - Original Format Compatibility
=========================================================

This script demonstrates how your original PostgreSQL code integrates 
seamlessly with the enhanced Codex Treasury system.
"""

import datetime
import sys
import os

# Add the current directory to Python path to import our modules
sys.path.insert(0, os.getcwd())

# Import the Codex Treasury system
from codex_treasury_database import CodexTreasury

# Your original database configuration (example)
DB_CONFIG = {
    "dbname": "codex",
    "user": "codex_user",
    "password": "codex_pass",
    "host": "localhost",
    "port": 5432
}

# Initialize the Codex Treasury system
treasury = CodexTreasury()

def connect_db():
    """Original function - now uses Codex Treasury connection management."""
    # The treasury handles connection pooling and fallback to JSON
    return treasury._get_connection() if treasury.connection_pool else None

def archive_transaction(stream, amount, currency="USD", source="", status="pending"):
    """
    Your original archive_transaction function, now enhanced with Codex integration.
    
    This maintains 100% compatibility with your original code while adding:
    - Dual storage (PostgreSQL + JSON ledger)
    - Better error handling
    - Integration with Dawn Dispatch system
    - Treasury analytics
    """
    
    print(f"💰 Archiving {stream} transaction: ${amount} {currency}")
    
    # Use the enhanced treasury system
    txn_id = treasury.archive_transaction(
        stream=stream,
        amount=amount,
        currency=currency,
        source=source,
        status=status
    )
    
    print(f"✅ Treasury archived transaction {txn_id} from stream {stream}")
    return txn_id

def ingest_affiliate(order_id, amount, currency="USD"):
    """Original affiliate ingest function - enhanced."""
    return treasury.ingest_affiliate(order_id, amount, currency)

def ingest_stock(symbol, amount, currency="USD"):
    """Original stock ingest function - enhanced.""" 
    return treasury.ingest_stock(symbol, amount, currency)

def ingest_amm(pool_id, amount, currency="USD"):
    """Original AMM ingest function - enhanced."""
    return treasury.ingest_amm(pool_id, amount, currency)

def treasury_report():
    """Generate a comprehensive treasury report."""
    print("\n📊 Codex Treasury Report")
    print("=" * 40)
    
    # Get treasury summary
    summary = treasury.get_treasury_summary(30)
    
    print(f"💰 Total Revenue (30 days): ${summary['total_revenue']:.2f}")
    print(f"📈 Total Transactions: {summary['total_transactions']}")
    print(f"🗄️  Data Source: {summary['source']}")
    
    print(f"\n📊 Revenue Stream Breakdown:")
    for stream, data in summary['revenue_streams'].items():
        print(f"   {stream.title()}: ${data['total_amount']:.2f} ({data['transaction_count']} txns)")
    
    # Show recent transactions from ledger
    ledger = treasury.load_ledger()
    recent_txns = ledger.get("transactions", [])[-5:]  # Last 5 transactions
    
    if recent_txns:
        print(f"\n📋 Recent Transactions:")
        for txn in recent_txns:
            print(f"   {txn['id']}: {txn['stream']} ${txn['amount']:.2f} - {txn['status']}")

def main():
    """
    Your original main function - demonstrating compatibility and enhancements.
    """
    print("🏛️  Codex Treasury Integration Test")
    print("Original code compatibility + Enhanced features")
    print("=" * 50)
    
    # Your original example runs - now enhanced
    print("\n💼 Processing example transactions...")
    
    try:
        # Example 1: Affiliate commission (your original)
        affiliate_id = ingest_affiliate("A123", 49.99)
        print(f"   Affiliate: {affiliate_id}")
        
        # Example 2: Stock trading (your original)
        stock_id = ingest_stock("MSFT", 1000.00)
        print(f"   Stock: {stock_id}")
        
        # Example 3: AMM pool (your original)
        amm_id = ingest_amm("pool-eth-usdc", 500.00)
        print(f"   AMM: {amm_id}")
        
        # Example 4: Direct archive (your original function)
        direct_id = archive_transaction("consulting", 750.00, "USD", "direct:client", "confirmed")
        print(f"   Direct: {direct_id}")
        
        # Enhanced feature: Treasury report
        treasury_report()
        
        # Show integration with Dawn Dispatch
        print(f"\n🌅 Dawn Dispatch Integration:")
        ledger = treasury.load_ledger()
        if "dawn_dispatches" in ledger:
            dawn_count = len(ledger["dawn_dispatches"])
            print(f"   Dawn dispatches logged: {dawn_count}")
            if dawn_count > 0:
                last_dawn = ledger["dawn_dispatches"][-1]
                print(f"   Last dispatch: {last_dawn['date']}")
        
        print(f"\n✅ All transactions processed successfully!")
        print(f"💾 Data stored in: JSON ledger + PostgreSQL (if available)")
        
    except Exception as e:
        print(f"❌ Error processing transactions: {e}")
        print(f"💡 The system continues with JSON-only mode")

if __name__ == "__main__":
    main()