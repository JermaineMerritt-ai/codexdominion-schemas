"""
🔑 HEIRS & CROWN KEYS SYSTEM 👑
Generational Inheritance & Access Control
The Merritt Method™ - Eternal Sovereignty Architecture

System Components:
- HEIRS → Designated inheritors with Crown Keys
- CROWN KEYS → Access tokens for Eternal Archives & Assets
- INHERITANCE VAULT → Secure legacy preservation system
- SUCCESSION PROTOCOL → Automated inheritance transfer
"""

import datetime
import json
import secrets
from pathlib import Path
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass, asdict
import hashlib


# ============================================================================
# ENUMS
# ============================================================================

class HeirStatus(Enum):
    """Status of heir in the system"""
    ACTIVE = "active"
    PENDING = "pending"
    SUSPENDED = "suspended"
    INHERITED = "inherited"


class CrownKeyType(Enum):
    """Types of Crown Keys with different access levels"""
    MASTER_KEY = "master_key"           # Full access to everything
    ARCHIVE_KEY = "archive_key"         # Access to Eternal Archives
    CROWN_KEY = "crown_key"             # Access to specific Crowns (products)
    LEDGER_KEY = "ledger_key"           # Access to financial records
    SCROLL_KEY = "scroll_key"           # Access to campaign data
    READ_ONLY = "read_only"             # View-only access


class AccessScope(Enum):
    """Scope of access for Crown Keys"""
    FULL = "full"                       # All resources
    CATEGORY = "category"               # Specific category
    RESOURCE = "resource"               # Specific resource ID
    TIME_LIMITED = "time_limited"       # Time-bound access


class InheritanceTrigger(Enum):
    """Events that trigger inheritance transfer"""
    MANUAL = "manual"                   # Manual activation
    DATE_BASED = "date_based"           # Specific date reached
    AGE_BASED = "age_based"             # Heir reaches age
    EVENT_BASED = "event_based"         # Specific event occurs


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Heir:
    """👨‍👩‍👧‍👦 Heir (Designated Inheritor)"""
    id: str
    name: str
    relationship: str                   # "son", "daughter", "spouse", "trusted_advisor"
    email: str
    birth_date: Optional[datetime.date]
    status: HeirStatus
    crown_keys: List[str]               # List of Crown Key IDs
    inheritance_date: Optional[datetime.date]
    notes: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['status'] = self.status.value
        if self.birth_date:
            data['birth_date'] = self.birth_date.isoformat()
        if self.inheritance_date:
            data['inheritance_date'] = self.inheritance_date.isoformat()
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data


@dataclass
class CrownKey:
    """🔑 Crown Key (Access Token)"""
    id: str
    key_hash: str                       # Hashed key for security
    key_type: CrownKeyType
    access_scope: AccessScope
    heir_id: str
    resource_ids: List[str]             # IDs of accessible resources
    permissions: List[str]              # ["read", "download", "share"]
    expires_at: Optional[datetime.datetime]
    created_at: datetime.datetime
    last_used: Optional[datetime.datetime]
    usage_count: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['key_type'] = self.key_type.value
        data['access_scope'] = self.access_scope.value
        if self.expires_at:
            data['expires_at'] = self.expires_at.isoformat()
        data['created_at'] = self.created_at.isoformat()
        if self.last_used:
            data['last_used'] = self.last_used.isoformat()
        return data


@dataclass
class InheritanceVault:
    """🏛️ Inheritance Vault (Legacy Package)"""
    id: str
    heir_id: str
    vault_name: str
    description: str
    contents: Dict[str, Any]            # All inherited assets
    trigger: InheritanceTrigger
    trigger_date: Optional[datetime.date]
    unlocked: bool
    unlocked_at: Optional[datetime.datetime]
    created_at: datetime.datetime

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['trigger'] = self.trigger.value
        if self.trigger_date:
            data['trigger_date'] = self.trigger_date.isoformat()
        if self.unlocked_at:
            data['unlocked_at'] = self.unlocked_at.isoformat()
        data['created_at'] = self.created_at.isoformat()
        return data


@dataclass
class SuccessionProtocol:
    """📜 Succession Protocol (Inheritance Rules)"""
    id: str
    name: str
    primary_heir_id: str
    backup_heir_ids: List[str]
    conditions: Dict[str, Any]
    asset_distribution: Dict[str, float]  # heir_id: percentage
    instructions: str
    active: bool
    created_at: datetime.datetime

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        return data


# ============================================================================
# HEIRS & CROWN KEYS MANAGER
# ============================================================================

class HeirsCrownKeysManager:
    """
    🔑 Manager for Heirs & Crown Keys System

    Manages:
    - Heirs (Designated inheritors)
    - Crown Keys (Access tokens)
    - Inheritance Vaults (Legacy packages)
    - Succession Protocols (Inheritance rules)
    """

    def __init__(self, base_path: str = "archives/sovereign"):
        """Initialize heirs & crown keys manager"""
        self.base_path = Path(base_path)

        # Create directories
        self.heirs_path = self.base_path / "heirs"
        self.keys_path = self.base_path / "crown_keys"
        self.vaults_path = self.base_path / "inheritance_vaults"
        self.protocols_path = self.base_path / "succession_protocols"

        for path in [self.heirs_path, self.keys_path, self.vaults_path, self.protocols_path]:
            path.mkdir(parents=True, exist_ok=True)

    # ========================================================================
    # HEIRS MANAGEMENT 👨‍👩‍👧‍👦
    # ========================================================================

    def designate_heir(self, name: str, relationship: str, email: str,
                      birth_date: Optional[datetime.date] = None,
                      inheritance_date: Optional[datetime.date] = None,
                      notes: str = "") -> Heir:
        """👑 Designate a new Heir"""
        heir_id = f"heir_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

        heir = Heir(
            id=heir_id,
            name=name,
            relationship=relationship,
            email=email,
            birth_date=birth_date,
            status=HeirStatus.ACTIVE,
            crown_keys=[],
            inheritance_date=inheritance_date,
            notes=notes,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )

        # Save heir
        heir_file = self.heirs_path / f"{heir_id}.json"
        with open(heir_file, 'w') as f:
            json.dump(heir.to_dict(), f, indent=2)

        print(f"👑 Heir designated: {name} ({relationship})")
        return heir

    def list_heirs(self, status: Optional[HeirStatus] = None) -> List[Dict[str, Any]]:
        """📋 List all Heirs"""
        heirs = []
        for heir_file in self.heirs_path.glob("heir_*.json"):
            with open(heir_file, 'r') as f:
                heir_data = json.load(f)
                if not status or heir_data.get('status') == status.value:
                    heirs.append(heir_data)
        return heirs

    def get_heir(self, heir_id: str) -> Optional[Dict[str, Any]]:
        """🔍 Get Heir by ID"""
        heir_file = self.heirs_path / f"{heir_id}.json"
        if heir_file.exists():
            with open(heir_file, 'r') as f:
                return json.load(f)
        return None

    # ========================================================================
    # CROWN KEYS MANAGEMENT 🔑
    # ========================================================================

    def forge_crown_key(self, heir_id: str, key_type: CrownKeyType,
                       access_scope: AccessScope, resource_ids: List[str],
                       permissions: List[str],
                       expires_at: Optional[datetime.datetime] = None) -> tuple[CrownKey, str]:
        """🔑 Forge a new Crown Key"""
        key_id = f"key_{key_type.value}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Generate secure key
        raw_key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

        crown_key = CrownKey(
            id=key_id,
            key_hash=key_hash,
            key_type=key_type,
            access_scope=access_scope,
            heir_id=heir_id,
            resource_ids=resource_ids,
            permissions=permissions,
            expires_at=expires_at,
            created_at=datetime.datetime.now(),
            last_used=None,
            usage_count=0
        )

        # Save key
        key_file = self.keys_path / f"{key_id}.json"
        with open(key_file, 'w') as f:
            json.dump(crown_key.to_dict(), f, indent=2)

        # Update heir's crown_keys list
        heir_data = self.get_heir(heir_id)
        if heir_data:
            heir_data['crown_keys'].append(key_id)
            heir_file = self.heirs_path / f"{heir_id}.json"
            with open(heir_file, 'w') as f:
                json.dump(heir_data, f, indent=2)

        print(f"🔑 Crown Key forged: {key_type.value} for {heir_id}")
        return crown_key, raw_key

    def verify_crown_key(self, raw_key: str) -> Optional[Dict[str, Any]]:
        """✅ Verify Crown Key"""
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

        for key_file in self.keys_path.glob("key_*.json"):
            with open(key_file, 'r') as f:
                key_data = json.load(f)
                if key_data['key_hash'] == key_hash:
                    # Check expiration
                    if key_data.get('expires_at'):
                        expires_at = datetime.datetime.fromisoformat(key_data['expires_at'])
                        if datetime.datetime.now() > expires_at:
                            return None

                    # Update usage
                    key_data['usage_count'] += 1
                    key_data['last_used'] = datetime.datetime.now().isoformat()
                    with open(key_file, 'w') as f:
                        json.dump(key_data, f, indent=2)

                    return key_data

        return None

    def list_crown_keys(self, heir_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """📋 List Crown Keys"""
        keys = []
        for key_file in self.keys_path.glob("key_*.json"):
            with open(key_file, 'r') as f:
                key_data = json.load(f)
                if not heir_id or key_data.get('heir_id') == heir_id:
                    keys.append(key_data)
        return keys

    # ========================================================================
    # INHERITANCE VAULTS 🏛️
    # ========================================================================

    def create_inheritance_vault(self, heir_id: str, vault_name: str,
                                 description: str, contents: Dict[str, Any],
                                 trigger: InheritanceTrigger,
                                 trigger_date: Optional[datetime.date] = None) -> InheritanceVault:
        """🏛️ Create Inheritance Vault"""
        vault_id = f"vault_{heir_id}_{datetime.datetime.now().strftime('%Y%m%d')}"

        vault = InheritanceVault(
            id=vault_id,
            heir_id=heir_id,
            vault_name=vault_name,
            description=description,
            contents=contents,
            trigger=trigger,
            trigger_date=trigger_date,
            unlocked=False,
            unlocked_at=None,
            created_at=datetime.datetime.now()
        )

        # Save vault
        vault_file = self.vaults_path / f"{vault_id}.json"
        with open(vault_file, 'w') as f:
            json.dump(vault.to_dict(), f, indent=2)

        print(f"🏛️ Inheritance Vault created: {vault_name} for {heir_id}")
        return vault

    def unlock_vault(self, vault_id: str, crown_key: str) -> Optional[Dict[str, Any]]:
        """🔓 Unlock Inheritance Vault"""
        # Verify crown key
        key_data = self.verify_crown_key(crown_key)
        if not key_data:
            print("❌ Invalid Crown Key")
            return None

        # Load vault
        vault_file = self.vaults_path / f"{vault_id}.json"
        if not vault_file.exists():
            print("❌ Vault not found")
            return None

        with open(vault_file, 'r') as f:
            vault_data = json.load(f)

        # Check if heir matches
        if vault_data['heir_id'] != key_data['heir_id']:
            print("❌ Vault does not belong to this heir")
            return None

        # Unlock vault
        vault_data['unlocked'] = True
        vault_data['unlocked_at'] = datetime.datetime.now().isoformat()

        with open(vault_file, 'w') as f:
            json.dump(vault_data, f, indent=2)

        print(f"🔓 Vault unlocked: {vault_data['vault_name']}")
        return vault_data['contents']

    def list_vaults(self, heir_id: Optional[str] = None, unlocked_only: bool = False) -> List[Dict[str, Any]]:
        """📋 List Inheritance Vaults"""
        vaults = []
        for vault_file in self.vaults_path.glob("vault_*.json"):
            with open(vault_file, 'r') as f:
                vault_data = json.load(f)
                if heir_id and vault_data.get('heir_id') != heir_id:
                    continue
                if unlocked_only and not vault_data.get('unlocked'):
                    continue
                vaults.append(vault_data)
        return vaults

    # ========================================================================
    # SUCCESSION PROTOCOLS 📜
    # ========================================================================

    def create_succession_protocol(self, name: str, primary_heir_id: str,
                                   backup_heir_ids: List[str],
                                   conditions: Dict[str, Any],
                                   asset_distribution: Dict[str, float],
                                   instructions: str) -> SuccessionProtocol:
        """📜 Create Succession Protocol"""
        protocol_id = f"protocol_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

        protocol = SuccessionProtocol(
            id=protocol_id,
            name=name,
            primary_heir_id=primary_heir_id,
            backup_heir_ids=backup_heir_ids,
            conditions=conditions,
            asset_distribution=asset_distribution,
            instructions=instructions,
            active=True,
            created_at=datetime.datetime.now()
        )

        # Save protocol
        protocol_file = self.protocols_path / f"{protocol_id}.json"
        with open(protocol_file, 'w') as f:
            json.dump(protocol.to_dict(), f, indent=2)

        print(f"📜 Succession Protocol created: {name}")
        return protocol

    def execute_succession(self, protocol_id: str) -> Dict[str, Any]:
        """⚖️ Execute Succession Protocol"""
        protocol_file = self.protocols_path / f"{protocol_id}.json"
        if not protocol_file.exists():
            return {"success": False, "error": "Protocol not found"}

        with open(protocol_file, 'r') as f:
            protocol_data = json.load(f)

        results = {
            "protocol_id": protocol_id,
            "protocol_name": protocol_data['name'],
            "primary_heir": protocol_data['primary_heir_id'],
            "assets_transferred": [],
            "vaults_unlocked": [],
            "keys_activated": []
        }

        # Distribute assets according to protocol
        for heir_id, percentage in protocol_data['asset_distribution'].items():
            results['assets_transferred'].append({
                "heir_id": heir_id,
                "percentage": percentage
            })

        print(f"⚖️ Succession executed: {protocol_data['name']}")
        return results


# ============================================================================
# MAIN EXECUTION & TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🔑 HEIRS & CROWN KEYS SYSTEM 👑")
    print("Generational Inheritance & Access Control")
    print("=" * 70)

    manager = HeirsCrownKeysManager()

    # Test: Designate Heir
    print("\n👑 DESIGNATING HEIRS...")
    heir1 = manager.designate_heir(
        name="Jermaine Jr.",
        relationship="son",
        email="jr@codexdominion.com",
        birth_date=datetime.date(2010, 5, 15),
        inheritance_date=datetime.date(2028, 5, 15),  # When he turns 18
        notes="Primary heir, inherits full business ownership at age 18"
    )

    heir2 = manager.designate_heir(
        name="Sarah Merritt",
        relationship="spouse",
        email="sarah@codexdominion.com",
        notes="Co-founder, full access to all operations"
    )

    # Test: Forge Crown Keys
    print("\n🔑 FORGING CROWN KEYS...")
    master_key, master_key_raw = manager.forge_crown_key(
        heir_id=heir2.id,
        key_type=CrownKeyType.MASTER_KEY,
        access_scope=AccessScope.FULL,
        resource_ids=["*"],
        permissions=["read", "write", "delete", "download", "share"]
    )

    archive_key, archive_key_raw = manager.forge_crown_key(
        heir_id=heir1.id,
        key_type=CrownKeyType.ARCHIVE_KEY,
        access_scope=AccessScope.FULL,
        resource_ids=["*"],
        permissions=["read", "download"],
        expires_at=datetime.datetime(2050, 12, 31)
    )

    print(f"\n🔑 Master Key (SAVE SECURELY): {master_key_raw}")
    print(f"🔑 Archive Key (SAVE SECURELY): {archive_key_raw}")

    # Test: Create Inheritance Vault
    print("\n🏛️ CREATING INHERITANCE VAULT...")
    vault1 = manager.create_inheritance_vault(
        heir_id=heir1.id,
        vault_name="Jermaine Jr.'s Legacy Vault",
        description="Complete business inheritance package for age 18",
        contents={
            "crowns": ["crown_daily_flame", "crown_radiant_faith", "crown_business_blueprint"],
            "eternal_archives": ["all_archives_2020_2028"],
            "financial_records": "complete_ledger_2020_2028",
            "business_documentation": "operations_manual_v2028",
            "personal_message": "Son, this is your inheritance. Build on what I started. - Dad"
        },
        trigger=InheritanceTrigger.DATE_BASED,
        trigger_date=datetime.date(2028, 5, 15)
    )

    # Test: Create Succession Protocol
    print("\n📜 CREATING SUCCESSION PROTOCOL...")
    protocol1 = manager.create_succession_protocol(
        name="Primary Succession Protocol",
        primary_heir_id=heir1.id,
        backup_heir_ids=[heir2.id],
        conditions={
            "age_requirement": 18,
            "education_milestone": "high_school_graduate",
            "business_training_complete": True
        },
        asset_distribution={
            heir1.id: 0.60,  # 60% to son
            heir2.id: 0.40   # 40% to spouse
        },
        instructions="Transfer primary business control to Jermaine Jr. at age 18, with Sarah maintaining operational oversight until age 25."
    )

    # Test: Verify Key
    print("\n✅ VERIFYING CROWN KEY...")
    verified = manager.verify_crown_key(archive_key_raw)
    if verified:
        print(f"✅ Key verified: {verified['key_type']} (used {verified['usage_count']} times)")

    # Test: List all heirs and keys
    print("\n📋 LISTING HEIRS...")
    heirs = manager.list_heirs()
    for heir in heirs:
        print(f"  - {heir['name']} ({heir['relationship']}) - {len(heir['crown_keys'])} keys")

    print("\n📋 LISTING CROWN KEYS...")
    keys = manager.list_crown_keys()
    for key in keys:
        print(f"  - {key['key_type']} for {key['heir_id']} (scope: {key['access_scope']})")

    print("\n" + "=" * 70)
    print("✅ HEIRS & CROWN KEYS SYSTEM TEST COMPLETE")
    print("=" * 70)
    print(f"📂 Archives saved to: {manager.base_path}")
    print("\n👑 THE SUCCESSION IS SECURED 👑")
