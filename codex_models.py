#!/usr/bin/env python3
"""
🔥 CODEX DOMINION DATA MODELS 🔥
===============================
Pydantic models for sophisticated revenue tracking and constellation management
"""

import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Stream(str, Enum):
    """Revenue stream sources"""

    store = "store"
    social = "social"
    website = "website"


class Status(str, Enum):
    """Transaction status levels"""

    pending = "pending"
    witnessed = "witnessed"
    crowned = "crowned"


class Transaction(BaseModel):
    """Individual transaction record"""

    model_config = ConfigDict(use_enum_values=True)

    source: Stream
    item: str
    amount: float = Field(..., gt=0)
    timestamp: datetime


class Approval(BaseModel):
    """Approval tracking for transactions"""

    model_config = ConfigDict(use_enum_values=True)

    cycle: str
    source: Stream
    vault: float
    status: Status
    witness: Optional[str] = None
    crowned: Optional[str] = None


class Proclamation(BaseModel):
    """Sacred proclamation records"""

    timestamp: datetime
    cycle: Optional[str] = None
    text: Optional[str] = None
    ritual_type: Optional[str] = None
    council_role: Optional[str] = None
    power_level: Optional[int] = None


class LedgerEntry(BaseModel):
    """Ledger entry for revenue tracking"""

    model_config = ConfigDict(use_enum_values=True)

    timestamp: datetime
    source: Stream
    cycle: str
    amount: float
    transaction_id: Optional[str] = None


class Cycle(BaseModel):
    """Revenue cycle structure"""

    morning: Optional[float] = None
    twilight: Optional[float] = None
    seasonal: Optional[float] = None
    great_year: Optional[float] = None
    total: float


class ConstellationStar(BaseModel):
    """Individual star in a constellation"""

    name: str
    total: float
    cycles: Optional[Cycle] = None
    transactions: Optional[List[Transaction]] = None


class Constellation(BaseModel):
    """Revenue constellation structure"""

    name: str
    stars: List[ConstellationStar]
    total_revenue: float
    created_at: datetime
    last_updated: datetime


class CodexDataManager:
    """Enhanced data manager using Pydantic models"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def save_transaction(self, transaction: Transaction) -> bool:
        """Save a new transaction"""
        try:
            # Load existing transactions
            transactions = self.load_transactions()

            # Add new transaction
            transactions.append(transaction.model_dump())

            # Save back to file
            transactions_file = self.data_dir / "transactions.json"
            with open(transactions_file, "w", encoding="utf-8") as f:
                json.dump(transactions, f, indent=2, default=str)

            return True
        except Exception as e:
            print(f"Error saving transaction: {e}")
            return False

    def load_transactions(self) -> List[Dict]:
        """Load all transactions"""
        try:
            transactions_file = self.data_dir / "transactions.json"
            if transactions_file.exists():
                with open(transactions_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading transactions: {e}")
            return []

    def save_constellation(self, constellation: Constellation) -> bool:
        """Save constellation data"""
        try:
            # Load existing constellations
            constellations_data = self.load_constellations_data()

            # Update or add constellation
            constellation_dict = constellation.model_dump()

            # Find and update existing or add new
            updated = False
            for i, existing in enumerate(constellations_data.get("constellations", [])):
                if existing.get("name") == constellation.name:
                    constellations_data["constellations"][i] = constellation_dict
                    updated = True
                    break

            if not updated:
                constellations_data.setdefault("constellations", []).append(
                    constellation_dict
                )

            # Save back to file
            constellations_file = self.data_dir / "constellations.json"
            with open(constellations_file, "w", encoding="utf-8") as f:
                json.dump(constellations_data, f, indent=2, default=str)

            return True
        except Exception as e:
            print(f"Error saving constellation: {e}")
            return False

    def load_constellations_data(self) -> Dict:
        """Load constellation data"""
        try:
            constellations_file = self.data_dir / "constellations.json"
            if constellations_file.exists():
                with open(constellations_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {"constellations": []}
        except Exception as e:
            print(f"Error loading constellations: {e}")
            return {"constellations": []}

    def save_proclamation(self, proclamation: Proclamation) -> bool:
        """Save a new proclamation"""
        try:
            # Load existing proclamations
            proclamations_data = self.load_proclamations_data()

            # Add new proclamation
            proclamation_dict = proclamation.model_dump()
            proclamations_data.setdefault("proclamations", []).append(proclamation_dict)

            # Save back to file
            proclamations_file = self.data_dir / "proclamations.json"
            with open(proclamations_file, "w", encoding="utf-8") as f:
                json.dump(proclamations_data, f, indent=2, default=str)

            return True
        except Exception as e:
            print(f"Error saving proclamation: {e}")
            return False

    def load_proclamations_data(self) -> Dict:
        """Load proclamation data"""
        try:
            proclamations_file = self.data_dir / "proclamations.json"
            if proclamations_file.exists():
                with open(proclamations_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {"proclamations": []}
        except Exception as e:
            print(f"Error loading proclamations: {e}")
            return {"proclamations": []}

    def create_ledger_entry(
        self, source: Stream, cycle: str, amount: float
    ) -> LedgerEntry:
        """Create a new ledger entry"""
        return LedgerEntry(
            timestamp=datetime.now(), source=source, cycle=cycle, amount=amount
        )

    def create_constellation_from_revenue(
        self, name: str, revenue_data: Dict
    ) -> Constellation:
        """Create constellation from revenue data"""
        stars = []
        total_revenue = 0

        for stream_name, amount in revenue_data.items():
            if isinstance(amount, (int, float)) and amount > 0:
                star = ConstellationStar(
                    name=f"{stream_name.title()} Star",
                    total=float(amount),
                    cycles=Cycle(total=float(amount)),
                )
                stars.append(star)
                total_revenue += amount

        return Constellation(
            name=name,
            stars=stars,
            total_revenue=total_revenue,
            created_at=datetime.now(),
            last_updated=datetime.now(),
        )

    def get_revenue_summary(self) -> Dict[str, Any]:
        """Get comprehensive revenue summary"""
        try:
            transactions = self.load_transactions()
            constellations_data = self.load_constellations_data()

            # Calculate totals by stream
            stream_totals = {stream.value: 0 for stream in Stream}

            for transaction in transactions:
                if "source" in transaction and "amount" in transaction:
                    source = transaction["source"]
                    if source in stream_totals:
                        stream_totals[source] += transaction["amount"]

            # Add constellation totals
            constellation_total = 0
            for constellation in constellations_data.get("constellations", []):
                constellation_total += constellation.get("total_revenue", 0)

            return {
                "stream_totals": stream_totals,
                "total_transactions": len(transactions),
                "constellation_total": constellation_total,
                "grand_total": sum(stream_totals.values()) + constellation_total,
                "last_updated": datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"Error getting revenue summary: {e}")
            return {}


# Example usage and data creation
def initialize_codex_data():
    """Initialize Codex Dominion with sample data using Pydantic models"""

    manager = CodexDataManager()

    # Create sample transactions
    sample_transactions = [
        Transaction(
            source=Stream.store,
            item="Digital Sovereignty Course",
            amount=300.0,
            timestamp=datetime.now(),
        ),
        Transaction(
            source=Stream.social,
            item="Consultation Session",
            amount=150.0,
            timestamp=datetime.now(),
        ),
        Transaction(
            source=Stream.website,
            item="Premium Membership",
            amount=200.0,
            timestamp=datetime.now(),
        ),
    ]

    # Save transactions
    for transaction in sample_transactions:
        manager.save_transaction(transaction)

    # Create sample constellation
    revenue_data = {"store": 300, "social": 150, "website": 200}

    constellation = manager.create_constellation_from_revenue(
        "Revenue Crown Constellation", revenue_data
    )

    manager.save_constellation(constellation)

    # Create sample proclamation
    proclamation = Proclamation(
        timestamp=datetime.now(),
        cycle="Eternal Flame Cycle",
        text="By flame and silence, the Codex Dominion achieves total digital sovereignty!",
        ritual_type="Sacred Proclamation",
        council_role="High Council",
        power_level=10,
    )

    manager.save_proclamation(proclamation)

    print("✅ Codex Dominion data initialized with Pydantic models!")
    return manager


if __name__ == "__main__":
    initialize_codex_data()
