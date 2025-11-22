"""Ledger System for Codex Dominion"""
from typing import Dict, Any, List
from datetime import datetime
import json

class CodexLedger:
    """Transaction ledger for the Codex system"""
    
    def __init__(self):
        self.transactions = []
        self.balances = {}
    
    def record_transaction(self, transaction: Dict[str, Any]) -> str:
        """Record a new transaction"""
        transaction_id = f"txn_{len(self.transactions) + 1}"
        transaction["id"] = transaction_id
        transaction["timestamp"] = datetime.now().isoformat()
        self.transactions.append(transaction)
        return transaction_id
    
    def get_balance(self, account: str) -> float:
        """Get account balance"""
        return self.balances.get(account, 0.0)
    
    def update_balance(self, account: str, amount: float) -> None:
        """Update account balance"""
        self.balances[account] = self.balances.get(account, 0.0) + amount
    
    def get_transactions(self, limit: int = 100) -> List[Dict]:
        """Get recent transactions"""
        return self.transactions[-limit:]

codex_ledger = CodexLedger()
