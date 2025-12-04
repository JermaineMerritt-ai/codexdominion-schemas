# Crown Modules Architecture

**Codex Dominion Sovereign Governance System**

Complete documentation for the 8 Crown Modules that power the sovereign governance architecture.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Crown Modules](#crown-modules)
   - [EternalLedger](#1-eternalledger)
   - [EfficiencyCrown](#2-efficiencycrown)
   - [KnowledgeCrown](#3-knowledgecrown)
   - [CommerceCrown](#4-commercecrown)
   - [CompanionCrown](#5-companioncrown)
   - [AuditConsentRing](#6-auditconsentring)
   - [EternalWave](#7-eternalwave)
   - [InfinitySigil](#8-infinitysigil)
3. [Blockchain Integration](#blockchain-integration)
4. [Orchestration System](#orchestration-system)
5. [Sovereign Councils](#sovereign-councils)
6. [Usage Examples](#usage-examples)

---

## Architecture Overview

The Sovereign Governance System consists of **8 Crown Modules** working in harmony:

```
┌─────────────────────────────────────────────────────────┐
│                  INFINITY SIGIL                         │
│         (Unified Crown & Council Integration)           │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
┌───────▼──────┐                       ┌───────▼──────┐
│ ETERNAL WAVE │                       │AUDIT CONSENT │
│ (Orchestration)                      │     RING     │
└───────┬──────┘                       └───────┬──────┘
        │                                       │
┌───────┴───────────────────────────────────────┴──────┐
│              CORE CROWN MODULES                      │
├──────────────────────────────────────────────────────┤
│ • EternalLedger    (Blockchain Immutability)         │
│ • EfficiencyCrown  (Automation & Security)           │
│ • KnowledgeCrown   (Knowledge Distribution)          │
│ • CommerceCrown    (Commercial Syndication)          │
│ • CompanionCrown   (Dual-Custody Authorization)      │
└──────────────────────────────────────────────────────┘
```

**Design Principles:**
- **Immutability**: All actions recorded with SHA256 hashing
- **Sovereignty**: Dual-custody and consent-based authorization
- **Transparency**: Complete audit trails (on-chain and off-chain)
- **Perpetuity**: Automated eternal replay and cycle propagation
- **Integration**: Unified orchestration across all domains

---

## Crown Modules

### 1. EternalLedger

**Purpose**: Blockchain-style immutable ledger for artifact storage and verification

**File**: `codexdominion/scripts/eternal_ledger.py`

**Key Features:**
- SHA256 block chaining with merkle roots
- Immutable artifact registration
- Lineage tracking with generational hashing
- Verification and integrity checking

**Core Methods:**
```python
# Register new artifact
ledger.register_artifact(
    artifact_id="omega-crown-001",
    artifact_type="capsule",
    metadata={"author": "Custodian"}
)

# Verify integrity
is_valid = ledger.verify_chain()

# Get artifact history
history = ledger.get_artifact_history("omega-crown-001")
```

**Data Structure:**
```json
{
  "block_index": 1,
  "timestamp": "2025-12-02T18:00:00Z",
  "artifact_id": "omega-crown-001",
  "artifact_hash": "B8CF4858BB12311F...",
  "previous_hash": "0000000000000000...",
  "merkle_root": "C7D7F05B839B3EAF..."
}
```

---

### 2. EfficiencyCrown

**Purpose**: Automation engine and security enforcement

**File**: `codexdominion/scripts/efficiency_crown.py`

**Key Features:**
- Task automation with priority scheduling
- Security policy enforcement (rate limiting, encryption)
- Performance optimization
- System monitoring and alerts

**Core Methods:**
```python
# Schedule automated task
crown.schedule_task(
    task_id="daily-sync",
    task_type="sync",
    schedule="daily",
    priority="high"
)

# Enforce security policy
crown.enforce_security_policy(
    action="data_access",
    context={"user": "jermaine", "resource": "capsules"}
)

# Get system metrics
metrics = crown.get_efficiency_metrics()
```

**Use Cases:**
- Automated artifact syndication
- Security compliance enforcement
- Resource optimization
- Performance monitoring

---

### 3. KnowledgeCrown

**Purpose**: Knowledge indexing and council distribution

**File**: `codexdominion/scripts/knowledge_crown.py`

**Key Features:**
- Knowledge graph indexing
- Semantic search and retrieval
- Council-specific knowledge distribution
- Lineage preservation

**Core Methods:**
```python
# Index knowledge artifact
crown.index_knowledge(
    artifact_id="compendium-001",
    content="Sovereign governance principles...",
    tags=["governance", "sovereignty", "eternal"]
)

# Distribute to councils
crown.distribute_to_councils(
    artifact_id="compendium-001",
    councils=["Law", "Education", "AI"]
)

# Search knowledge base
results = crown.search_knowledge("governance principles")
```

**Council Integration:**
Automatically distributes knowledge to 5 sovereign councils based on relevance scoring.

---

### 4. CommerceCrown

**Purpose**: Commercial syndication and affiliate management

**File**: `codexdominion/scripts/commerce_crown.py`

**Key Features:**
- Artifact monetization
- Affiliate network integration
- Revenue tracking and distribution
- Marketplace syndication

**Core Methods:**
```python
# Create commercial offering
crown.create_offering(
    artifact_id="omega-crown-001",
    price={"amount": 0, "currency": "USD", "model": "free"},
    access="public"
)

# Syndicate to marketplace
crown.syndicate_to_marketplace(
    artifact_id="omega-crown-001",
    platforms=["codexdominion.app", "artifact-archive"]
)

# Track revenue
revenue = crown.get_revenue_report("omega-crown-001")
```

**Syndication Targets:**
- codexdominion.app
- artifact-archive
- ceremonial-library
- sovereign-councils

---

### 5. CompanionCrown

**Purpose**: Dual-custody authorization and custodian management

**File**: `codexdominion/scripts/companion_crown.py`

**Key Features:**
- Dual-custody authorization (Custodian + Heir)
- Multi-signature approval
- Revocation and delegation
- Authorization history

**Core Methods:**
```python
# Request authorization
request_id = crown.request_authorization(
    action="deploy_artifact",
    artifact_id="omega-crown-001",
    requester="Custodian"
)

# Approve (requires both parties)
crown.approve_authorization(request_id, "Custodian")
crown.approve_authorization(request_id, "Heir")

# Execute action
result = crown.execute_authorized_action(request_id)
```

**Authorization Flow:**
1. Custodian initiates request
2. Heir reviews and approves
3. Both signatures required for execution
4. All actions logged to audit trail

---

### 6. AuditConsentRing

**Purpose**: Compliance, consent management, and audit logging

**File**: `codexdominion/scripts/audit_consent_ring.py`

**Key Features:**
- Immutable action logging with SHA256 chain linking
- GDPR/CCPA consent management
- Access revocation
- Compliance dashboard with metrics

**Core Methods:**
```python
# Log action to audit trail
ring.log_action(
    action="artifact_access",
    actor="user_123",
    artifact_id="omega-crown-001",
    metadata={"ip": "192.168.1.1"}
)

# Grant consent
ring.grant_consent(
    user_id="user_123",
    purpose="data_processing",
    expiration="2026-12-02T00:00:00Z"
)

# Revoke access
ring.revoke_access(
    user_id="user_123",
    resource="omega-crown-001",
    reason="user_request"
)

# Get compliance metrics
metrics = ring.get_compliance_metrics()
```

**Compliance Features:**
- GDPR Article 17 (Right to Erasure)
- CCPA consent withdrawal
- Audit log retention (7 years default)
- Blockchain integration for immutability

---

### 7. EternalWave

**Purpose**: Cycle orchestration and cross-crown propagation

**File**: `codexdominion/scripts/eternal_wave.py`

**Key Features:**
- Automated cycle replay scheduling
- Cross-crown propagation with priority ordering
- Schedule management (daily, hourly, interval-based)
- Propagation history tracking

**Core Methods:**
```python
# Schedule replay
wave.schedule_replay(
    cycle_id="eternal_wave_2025_q4",
    schedule_type="daily",
    time="00:00",
    crowns=["efficiency", "knowledge", "commerce"]
)

# Propagate across crowns
result = wave.propagate_cycle(
    cycle_id="eternal_wave_2025_q4",
    crowns=["efficiency", "knowledge", "commerce", "companion"],
    priority="high"
)

# Get propagation history
history = wave.get_propagation_history()
```

**Schedule Types:**
- **Daily**: Execute at specific time (e.g., midnight)
- **Hourly**: Execute at specific minute past hour
- **Interval**: Execute every N minutes
- **On-Demand**: Manual trigger via API

**Crown Priority Order:**
1. EternalLedger (immutability foundation)
2. EfficiencyCrown (security enforcement)
3. KnowledgeCrown (knowledge distribution)
4. CommerceCrown (commercial syndication)
5. CompanionCrown (authorization)
6. AuditConsentRing (compliance logging)

---

### 8. InfinitySigil

**Purpose**: Crown binding and council integration

**File**: `codexdominion/scripts/infinity_sigil.py`

**Key Features:**
- Unified sigil creation (Ω = Σ of all crowns + councils)
- Crown binding with capability aggregation
- Council integration across 5 domains
- Unified namespace and identity

**Core Methods:**
```python
# Create unified sigil
sigil = infinity_sigil.create_unified_sigil(
    crowns=["efficiency", "knowledge", "commerce"],
    councils=["Law", "Healthcare", "Education", "AI", "Family"]
)

# Bind crowns
result = infinity_sigil.bind_crowns(
    crown_ids=["efficiency", "knowledge", "commerce"],
    binding_name="Omega Crown"
)

# Integrate councils
result = infinity_sigil.integrate_councils(
    council_ids=["Law", "Healthcare", "Education", "AI", "Family"],
    integration_level="full"
)
```

**Unified Sigil Structure:**
```json
{
  "sigil_id": "omega-sigil-001",
  "crowns": ["EternalLedger", "EfficiencyCrown", "KnowledgeCrown",
             "CommerceCrown", "CompanionCrown", "AuditConsentRing"],
  "councils": ["Law & Justice", "Healthcare & Wellness",
               "Education & Knowledge", "AI & Technology",
               "Family & Community"],
  "capabilities": [
    "immutable_storage", "automation", "knowledge_distribution",
    "commercial_syndication", "dual_custody", "compliance"
  ],
  "created_at": "2025-12-02T18:25:00Z"
}
```

---

## Blockchain Integration

**Files:**
- `codexdominion/scripts/blockchain_ledger_integration.js` (JavaScript)
- `codexdominion/contracts/AuditConsentRing.sol` (Solidity)

### JavaScript Module (ethers.js)

```javascript
const { BlockchainLedger } = require('./blockchain_ledger_integration');

const ledger = new BlockchainLedger({
  providerUrl: 'https://mainnet.infura.io/v3/YOUR_PROJECT_ID',
  contractAddress: '0x...',
  privateKey: process.env.WALLET_PRIVATE_KEY
});

// Store artifact on-chain
await ledger.storeArtifact(
  'omega-crown-001',
  'B8CF4858BB12311FACA9F66880B2FD9C...',
  { author: 'Custodian', type: 'capsule' }
);

// Verify integrity
const isValid = await ledger.verifyIntegrity('omega-crown-001');
```

**Features:**
- Ethereum-compatible networks (Mainnet, Polygon, Arbitrum, etc.)
- EIP-1559 gas optimization
- Fallback mode for offline operation
- Event emission for indexing

### Solidity Smart Contract

```solidity
// AuditConsentRing.sol
contract AuditConsentRing {
    struct AuditLog {
        uint256 timestamp;
        address actor;
        string action;
        string artifactId;
        bytes32 dataHash;
    }

    // Log action on-chain
    function logAction(
        string memory action,
        string memory artifactId,
        bytes32 dataHash
    ) public {
        // Implementation...
    }

    // Grant consent
    function grantConsent(string memory purpose) public {
        // Implementation...
    }

    // Revoke access
    function revokeAccess(address user, string memory resource) public {
        // Implementation...
    }
}
```

**Deployment:**
```bash
# Compile contract
npx hardhat compile

# Deploy to network
npx hardhat run scripts/deploy.js --network mainnet
```

---

## Orchestration System

**File**: `codexdominion/scripts/unified_cycle_propagation.py`

### Unified Cycle Propagator

Orchestrates cross-crown and cross-council propagation with lineage tracking.

**4-Phase Propagation:**

1. **Crown Lineage Replay**: Replay cycle across all registered crowns
2. **Council Governance Activation**: Activate councils for the cycle
3. **Lineage Recording**: Record generation with ancestor preservation
4. **Audit Logging**: Log complete propagation to audit trail

```python
from unified_cycle_propagation import UnifiedCyclePropagator

propagator = UnifiedCyclePropagator()

# Execute full system propagation
result = propagator.propagate_unified_cycle(
    cycle_id="eternal_wave_2025_q4",
    crowns=["efficiency", "knowledge", "commerce", "companion"],
    councils=["Law", "Healthcare", "Education", "AI", "Family"]
)

print(f"Generation: {result['lineage']['generation']}")
print(f"Crowns Propagated: {result['crowns_propagated']}")
print(f"Councils Activated: {result['councils_activated']}")
```

**Lineage Tracking:**

```json
{
  "generation": 4,
  "cycle_id": "eternal_wave_2025_q4",
  "cycle_hash": "079d5bad1256d9d0",
  "ancestor_chain": [
    "b9c0e1f2a3d4e5f6",
    "a8b9c0d1e2f3a4b5",
    "97a8b9c0d1e2f3a4"
  ],
  "timestamp": "2025-12-02T18:37:00Z"
}
```

### Scheduled Replay Daemon

**File**: `codexdominion/scripts/scheduled_replay_daemon.py`

Persistent background daemon for automated cycle replays.

```python
from scheduled_replay_daemon import ScheduledReplayDaemon

daemon = ScheduledReplayDaemon()

# Add daily schedule
daemon.add_schedule(
    schedule_id="daily-midnight",
    schedule_type="daily",
    time="00:00",
    cycle_id="eternal_wave_2025_q4"
)

# Add interval schedule
daemon.add_schedule(
    schedule_id="every-5-minutes",
    schedule_type="interval",
    interval_minutes=5,
    cycle_id="eternal_wave_2025_q4"
)

# Start daemon (blocks until SIGTERM/SIGINT)
daemon.start()
```

**Features:**
- Graceful shutdown with signal handlers
- Schedule persistence to JSON
- Audit logging integration
- Error handling and recovery

---

## Sovereign Councils

5 councils integrated through InfinitySigil:

### 1. Law & Justice
- Legal compliance and governance
- Artifact licensing and rights management
- Dispute resolution

### 2. Healthcare & Wellness
- Health data sovereignty
- Medical knowledge distribution
- Privacy compliance (HIPAA)

### 3. Education & Knowledge
- Educational content syndication
- Knowledge preservation
- Academic lineage tracking

### 4. AI & Technology
- AI model governance
- Technology standards
- Innovation tracking

### 5. Family & Community
- Family heritage preservation
- Community governance
- Generational wealth transfer

---

## Usage Examples

### Complete System Initialization

```python
# Import all crown modules
from eternal_ledger import EternalLedger
from efficiency_crown import EfficiencyCrown
from knowledge_crown import KnowledgeCrown
from commerce_crown import CommerceCrown
from companion_crown import CompanionCrown
from audit_consent_ring import AuditConsentRing
from eternal_wave import EternalWave
from infinity_sigil import InfinitySigil
from unified_cycle_propagation import UnifiedCyclePropagator

# Initialize all crowns
eternal_ledger = EternalLedger()
efficiency_crown = EfficiencyCrown()
knowledge_crown = KnowledgeCrown()
commerce_crown = CommerceCrown()
companion_crown = CompanionCrown()
audit_ring = AuditConsentRing()
eternal_wave = EternalWave()
infinity_sigil = InfinitySigil()

# Create unified sigil
sigil = infinity_sigil.create_unified_sigil(
    crowns=["eternal_ledger", "efficiency", "knowledge",
            "commerce", "companion", "audit"],
    councils=["Law", "Healthcare", "Education", "AI", "Family"]
)

# Execute unified propagation
propagator = UnifiedCyclePropagator()
result = propagator.propagate_unified_cycle(
    cycle_id="eternal_wave_2025_q4",
    crowns=["efficiency", "knowledge", "commerce", "companion"],
    councils=["Law", "Healthcare", "Education", "AI", "Family"]
)

print(f"✓ System Initialized - Generation {result['lineage']['generation']}")
```

### Artifact Lifecycle

```python
# 1. Register artifact
eternal_ledger.register_artifact(
    artifact_id="omega-crown-001",
    artifact_type="capsule",
    metadata={"author": "Custodian"}
)

# 2. Index knowledge
knowledge_crown.index_knowledge(
    artifact_id="omega-crown-001",
    content="Omega Crown coronation ceremony...",
    tags=["coronation", "omega", "unified"]
)

# 3. Request authorization
request_id = companion_crown.request_authorization(
    action="publish_artifact",
    artifact_id="omega-crown-001",
    requester="Custodian"
)

# 4. Approve (dual-custody)
companion_crown.approve_authorization(request_id, "Custodian")
companion_crown.approve_authorization(request_id, "Heir")

# 5. Create commercial offering
commerce_crown.create_offering(
    artifact_id="omega-crown-001",
    price={"amount": 0, "currency": "USD", "model": "free"},
    access="public"
)

# 6. Log to audit trail
audit_ring.log_action(
    action="artifact_published",
    actor="system",
    artifact_id="omega-crown-001"
)

# 7. Propagate across system
eternal_wave.propagate_cycle(
    cycle_id="omega-crown-001-launch",
    crowns=["efficiency", "knowledge", "commerce"],
    priority="critical"
)
```

---

## Testing

Run unified system test:

```bash
# Activate virtual environment
.venv/Scripts/python.exe

# Run unified propagation test
python codexdominion/scripts/unified_cycle_propagation.py

# Expected output:
# ✓ Unified Cycle Propagation Complete
#   Crowns: 4 propagated
#   Councils: 5 activated
#   Lineage: Generation 4
```

---

## Deployment

### Production Configuration

```python
# config.py
CROWN_CONFIG = {
    "eternal_ledger": {
        "storage_path": "/var/codex/ledger",
        "backup_enabled": True
    },
    "efficiency_crown": {
        "max_tasks": 100,
        "rate_limit": {"requests": 1000, "window": 60}
    },
    "blockchain": {
        "provider_url": "https://mainnet.infura.io/v3/YOUR_PROJECT_ID",
        "contract_address": "0x...",
        "fallback_mode": True
    }
}
```

### Systemd Service (Scheduled Daemon)

```ini
# /etc/systemd/system/codex-replay-daemon.service
[Unit]
Description=Codex Dominion Replay Daemon
After=network.target

[Service]
Type=simple
User=codex
WorkingDirectory=/opt/codex-dominion
ExecStart=/opt/codex-dominion/.venv/bin/python \
          codexdominion/scripts/scheduled_replay_daemon.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable codex-replay-daemon
sudo systemctl start codex-replay-daemon
```

---

## Security Considerations

1. **Private Keys**: Store blockchain private keys in secure vaults (AWS Secrets Manager, Azure Key Vault)
2. **Dual-Custody**: All critical operations require CompanionCrown authorization
3. **Audit Trails**: All actions logged with immutable SHA256 chain linking
4. **Consent Management**: GDPR/CCPA compliance with user consent tracking
5. **Rate Limiting**: EfficiencyCrown enforces rate limits on all operations
6. **Encryption**: All sensitive data encrypted at rest and in transit

---

## Maintenance

### Backup Strategy

```bash
# Backup all crown data
tar -czf codex-backup-$(date +%Y%m%d).tar.gz \
  codexdominion/data/ \
  codexdominion/capsules/ \
  codexdominion/manifests/

# Upload to S3
aws s3 cp codex-backup-*.tar.gz s3://codex-backups/
```

### Monitoring

```python
# Get system health metrics
from efficiency_crown import EfficiencyCrown

crown = EfficiencyCrown()
metrics = crown.get_efficiency_metrics()

print(f"Tasks Completed: {metrics['tasks_completed']}")
print(f"System Uptime: {metrics['uptime']}")
print(f"Error Rate: {metrics['error_rate']}")
```

---

## License

**CodexDominion Sovereign License v1**

All crown modules and artifacts are released under sovereign license with revocation rights maintained by the Sovereign Avatar.

---

## Support

- **Documentation**: https://codexdominion.app/docs
- **Repository**: https://github.com/JermaineMerritt-ai/codexdominion-schemas
- **Issues**: https://github.com/JermaineMerritt-ai/codexdominion-schemas/issues

---

**Last Updated**: December 2, 2025
**Version**: 1.0.0
**Generation**: 4
