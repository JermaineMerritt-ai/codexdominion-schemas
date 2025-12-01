#!/usr/bin/env python3
"""
Test Ledger Functionality
"""

import sys
from pathlib import Path

# Add codex-suite to path
sys.path.insert(0, str(Path(__file__).parent / "codex-suite"))

from core.ledger import codex_ledger


def test_ledger():
    print("🧪 Testing Streamlined Ledger")

    # Test add transaction
    tx_id = codex_ledger.add_transaction(
        type="test_transaction",
        data={"test": "Integration test transaction"},
        metadata={"source": "test"},
    )

    print(f"✅ Transaction ID: {tx_id}")

    # Test get transaction
    transaction = codex_ledger.get_transaction(tx_id)

    if transaction:
        print(f"✅ Retrieved transaction type: {transaction.get('type')}")
        print(f"✅ Transaction data: {transaction.get('data')}")
        return True
    else:
        print("❌ Failed to retrieve transaction")
        return False


if __name__ == "__main__":
    success = test_ledger()
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}")
