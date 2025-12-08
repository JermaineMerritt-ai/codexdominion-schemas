# 👑 Digital Seal Service - Codex Dominion

**Cryptographic Signing Infrastructure for Ceremonial Exports**

---

## Overview

The Digital Seal Service provides enterprise-grade cryptographic sealing for all Codex Dominion exports (PDF ledgers, Markdown scrolls, YAML capsules). Each export is stamped with immutable signatures from the Custodian and optionally from Council members, forming a multi-signature covenant that can be verified centuries later.

## Architecture

### Core Components

1. **DigitalSealService** (`backend/services/digital_seal_service.py`)
   - Custodian master key (RSA-2048)
   - Council member seal registry
   - SHA-256 content hashing
   - RSA-2048 and ECC P-256 signature algorithms
   - Immutable signature ledger

2. **Seal Verification API** (`backend/routes/seal_verification.py`)
   - `/api/seal/ledger` - View complete signature ledger
   - `/api/seal/verify` - Verify seal packages
   - `/api/seal/register-council` - Register council members
   - `/api/seal/multi-signature-covenant` - Create multi-signed exports
   - `/api/seal/verify/{content_hash}` - Lookup by hash

3. **Export Integration** (`backend/routes/annotations_export.py`)
   - Updated to use Digital Seal Service
   - Support for multi-signature covenants via query params
   - Seal metadata embedded in all exports

---

## Cryptographic Specifications

### Custodian Seal
- **Algorithm**: RSA-2048-PSS-SHA256
- **Key Size**: 2048 bits
- **Padding**: PSS (Probabilistic Signature Scheme) with SHA-256
- **Salt Length**: Maximum (randomized for each signature)
- **Key Storage**: In production, use Azure Key Vault or HSM

### Council Seals
- **RSA Option**: RSA-2048-PSS-SHA256 (same as custodian)
- **ECC Option**: ECDSA-P256-SHA256 (Elliptic Curve, faster, smaller)
- **Curve**: SECP256R1 (NIST P-256)
- **Key Format**: PEM-encoded PKCS8

### Content Hashing
- **Algorithm**: SHA-256
- **Input**: Raw export content (before seal footer)
- **Output**: 64-character hex digest
- **Collision Resistance**: ~2^256 (computationally infeasible to forge)

---

## Seal Package Structure

```json
{
  "content_hash": "a3f5d8e7c2b4...",
  "hash_algorithm": "SHA-256",
  "export_format": "markdown",
  "timestamp": "2025-12-07T18:30:00.000000Z",
  "covenant_type": "multi-signature",
  "metadata": {
    "cycle": "seasonal",
    "engine": "Commerce Engine",
    "entry_count": 42
  },
  "signatures": [
    {
      "signer": "custodian",
      "name": "Jermaine Merritt",
      "role": "Sovereign Custodian",
      "signature": "base64_encoded_signature...",
      "algorithm": "RSA-2048-PSS-SHA256",
      "timestamp": "2025-12-07T18:30:00.000000Z"
    },
    {
      "signer": "council",
      "member_id": "council_001",
      "name": "Elena Rodriguez",
      "role": "Senior Council",
      "signature": "base64_encoded_signature...",
      "algorithm": "ECDSA-P256-SHA256",
      "timestamp": "2025-12-07T18:30:15.000000Z"
    }
  ],
  "signature_count": 2,
  "required_signatures": 2
}
```

---

## API Usage

### 1. Register Council Member

```bash
curl -X POST http://localhost:8000/api/seal/register-council \
  -H "Content-Type: application/json" \
  -d '{
    "member_id": "council_001",
    "member_name": "Elena Rodriguez",
    "role": "Senior Council",
    "seal_type": "ECC-P256"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Council seal registered for Elena Rodriguez",
  "seal": {
    "member_id": "council_001",
    "member_name": "Elena Rodriguez",
    "role": "Senior Council",
    "seal_type": "ECC-P256",
    "public_key": "-----BEGIN PUBLIC KEY-----\n...",
    "created_at": "2025-12-07T18:25:00.000000Z"
  }
}
```

### 2. Export with Multi-Signature Covenant

```bash
curl "http://localhost:8000/api/annotations/export?format=markdown&cycle=seasonal&include_council=true&council_members=council_001,council_002"
```

**Result**: Markdown file with custodian + 2 council signatures

### 3. Verify Seal Package

```bash
curl -X POST http://localhost:8000/api/seal/verify \
  -H "Content-Type: application/json" \
  -d '{
    "seal_package": {...},
    "content": "# Ceremonial Annotation Scroll\n...",
    "content_encoding": "utf-8"
  }'
```

**Response:**
```json
{
  "valid": true,
  "verification_results": {
    "Jermaine Merritt": true,
    "Elena Rodriguez": true
  },
  "signature_count": 2,
  "content_hash": "a3f5d8e7c2b4...",
  "timestamp": "2025-12-07T18:30:00.000000Z"
}
```

### 4. View Signature Ledger

```bash
curl http://localhost:8000/api/seal/ledger
```

**Response:**
```json
{
  "ledger": [
    {
      "entry_id": 1,
      "content_hash": "a3f5d8e7c2b4...",
      "export_format": "markdown",
      "timestamp": "2025-12-07T18:30:00.000000Z",
      "signature_count": 2,
      "signers": ["Jermaine Merritt", "Elena Rodriguez"],
      "metadata": {"cycle": "seasonal", "engine": "Commerce Engine"}
    }
  ],
  "total_entries": 1,
  "custodian": "Jermaine Merritt"
}
```

### 5. Lookup by Content Hash

```bash
curl http://localhost:8000/api/seal/verify/a3f5d8e7c2b4...
```

---

## Immutable Ledger

Every seal operation is recorded in the immutable signature ledger:

- **Entry ID**: Sequential, monotonically increasing
- **Content Hash**: SHA-256 of export content
- **Export Format**: pdf/markdown/yaml
- **Timestamp**: UTC ISO-8601
- **Signature Count**: Number of signers
- **Signers**: List of names (custodian + council)
- **Metadata**: Cycle, engine, role filters

The ledger can be exported as JSON for archival:

```bash
curl http://localhost:8000/api/seal/ledger/export -o seal-ledger.json
```

---

## Frontend Integration

### AnnotationExport Component Update

Add multi-signature option:

```typescript
const [includeCouncil, setIncludeCouncil] = useState(false);
const [selectedCouncil, setSelectedCouncil] = useState<string[]>([]);

const exportFile = async (format: 'pdf' | 'markdown' | 'yaml') => {
  const params = new URLSearchParams();
  params.set('format', format);
  if (includeCouncil) {
    params.set('include_council', 'true');
    params.set('council_members', selectedCouncil.join(','));
  }

  window.open(`/api/annotations/export?${params.toString()}`, '_blank');
};
```

### Council Seal Selector

```tsx
<div className="mb-4">
  <label>
    <input
      type="checkbox"
      checked={includeCouncil}
      onChange={(e) => setIncludeCouncil(e.target.checked)}
    />
    Include Council Signatures (Multi-Signature Covenant)
  </label>

  {includeCouncil && (
    <select multiple onChange={(e) => setSelectedCouncil(Array.from(e.target.selectedOptions, o => o.value))}>
      <option value="council_001">Elena Rodriguez (Senior Council)</option>
      <option value="council_002">Marcus Chen (Council Observer)</option>
      <option value="council_003">Aisha Patel (Technical Council)</option>
    </select>
  )}
</div>
```

---

## Security Best Practices

### Production Deployment

1. **Key Storage**
   - Store custodian private key in Azure Key Vault
   - Use Hardware Security Module (HSM) for signing operations
   - Never expose private keys in logs or responses

2. **Council Key Management**
   - Issue keys via secure ceremony (in-person or video-verified)
   - Store private keys client-side (browser crypto.subtle) or in secure enclaves
   - Rotate keys annually or after compromise

3. **Signature Verification**
   - Always verify content hash matches before verifying signatures
   - Check timestamp is reasonable (not future, not ancient)
   - Validate certificate chain for council seals

4. **Ledger Integrity**
   - Back up ledger to immutable storage (Azure Blob with WORM)
   - Compute Merkle tree root of ledger entries
   - Publish root hash to blockchain for public auditability (optional)

### Attack Mitigation

- **Replay Attacks**: Include timestamp in seal, reject old signatures
- **Man-in-the-Middle**: Use HTTPS for all API calls
- **Key Compromise**: Implement key revocation list (CRL)
- **Hash Collisions**: Use SHA-256 (no known collisions)

---

## Example Export with Seal

**Markdown Scroll (excerpt):**

```markdown
# 📜 Ceremonial Annotation Scroll

**Generated:** 2025-12-07 18:30 UTC
**Cycle Binding:** Seasonal
**Total Entries:** 42

---

## Commerce Engine

### 📍 2025-12-07 06:36:00
**Observer:** Council Member (council)
**Capsule:** 12345
**Tags:** revenue-impact, degraded-status

Revenue dip aligned with degraded status.

---

## 👑 Cryptographic Seals

**Content Hash:** `a3f5d8e7c2b4f6a8d5e3c1b9a7f4d2e0c8b6a4f2d0e8c6b4a2f0d8e6c4b2a0f8`
**Hash Algorithm:** SHA-256
**Timestamp:** 2025-12-07T18:30:00.000000Z

### Seal 1: Jermaine Merritt
- **Role:** Sovereign Custodian
- **Signature:** `kQ7mL3pR9wX...` (2048 bits)
- **Algorithm:** RSA-2048-PSS-SHA256
- **Signed:** 2025-12-07T18:30:00.000000Z

### Seal 2: Elena Rodriguez
- **Role:** Senior Council
- **Signature:** `hF4dK8nM2vZ...` (256 bits)
- **Algorithm:** ECDSA-P256-SHA256
- **Signed:** 2025-12-07T18:30:15.000000Z

*This scroll is cryptographically sealed and immutable.*
*Verification URL: https://codexdominion.app/api/seal/verify/a3f5d8e7c2b4...*
```

---

## Verification Workflow

1. **Export is generated** → Content hashed → Custodian signs → Council signs
2. **Seal package stored** → Ledger entry created → Public verification URL generated
3. **User downloads export** → Can verify locally or via API
4. **Verification checks**:
   - Recompute content hash
   - Verify each signature with public key
   - Check timestamp is valid
   - Confirm ledger entry exists

**Result**: Tamper-proof exports that can be verified centuries later, even if original server is gone (as long as public keys are preserved).

---

## CLI Tool for Verification

Create `verify_seal.py`:

```python
import requests
import json
import sys

def verify_export(file_path: str, seal_url: str):
    with open(file_path, 'r') as f:
        content = f.read()

    # Extract seal package from file (embedded as JSON comment or footer)
    # For simplicity, assume seal URL provided

    response = requests.post(f"{seal_url}/api/seal/verify", json={
        "seal_package": {...},  # Extracted from file
        "content": content,
        "content_encoding": "utf-8"
    })

    if response.json()["valid"]:
        print("✅ All signatures valid - Export is authentic")
    else:
        print("❌ Signature verification failed - Export may be tampered")

if __name__ == "__main__":
    verify_export(sys.argv[1], "https://codexdominion.app")
```

Usage:
```bash
python verify_seal.py codex-dominion-scroll-seasonal-20251207.md
```

---

## Future Enhancements

1. **Blockchain Anchoring**
   - Publish ledger root hash to Ethereum or Bitcoin
   - Enables verification even if Codex Dominion servers disappear

2. **Hardware Token Support**
   - Council members use YubiKey or similar for signing
   - Private keys never leave the device

3. **Timestamp Authority**
   - Use RFC 3161 timestamp service for legal non-repudiation
   - Proves signature existed at specific time

4. **Seal Expiration**
   - Set expiration dates on seals (e.g., 10 years)
   - Require re-sealing for long-term archives

5. **Quantum-Resistant Signatures**
   - Migrate to post-quantum algorithms (CRYSTALS-Dilithium)
   - Ensures seals remain valid against future quantum computers

---

## Installation

```bash
cd backend
pip install -r requirements.txt

# Verify cryptography library installed
python -c "from cryptography.hazmat.primitives.asymmetric import rsa; print('✅ Cryptography library ready')"

# Start FastAPI server
uvicorn main:app --reload --port 8000
```

---

## Testing

```python
# Test custodian seal
from services.digital_seal_service import get_seal_service

seal_service = get_seal_service("Jermaine Merritt")
content = "# Test Export\n\nThis is a test."
seal_package = seal_service.sign_export(content, "markdown")

print(f"Content Hash: {seal_package['content_hash']}")
print(f"Signature: {seal_package['signatures'][0]['signature'][:32]}...")

# Verify
is_valid = seal_service.verify_signature(seal_package, content, 0)
print(f"Valid: {is_valid}")  # Should print True
```

---

## Support

For questions about the Digital Seal Service:
- **Documentation**: This file
- **API Reference**: http://localhost:8000/docs (FastAPI auto-generated)
- **Custodian**: Jermaine Merritt
- **Security Issues**: Report privately via encrypted channel

---

**👑 Codex Dominion Digital Seal Service v1.0.0**

*Cryptographic authenticity for ceremonial archives, immutable across centuries.*
