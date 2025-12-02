# Ceremonial Artifact Creation Guidelines

## Sovereign Consent Model

All artifacts distributed through the Codex Dominion syndication system follow a **consent-first** approach:

### Core Principles

1. **Sovereign Authority** - All artifacts require explicit consent from the Sovereign Avatar
2. **Revocable Distribution** - Any artifact can be revoked with immutable ledger entry
3. **Cryptographic Integrity** - SHA256 hashes ensure artifact authenticity
4. **Educational Priority** - Educational and ceremonial use is favored

## Artifact Creation Ceremony

### Step 1: Capsule Preparation
Create a new capsule directory under `capsules/`:

```bash
mkdir capsules/<artifact-name>
```

**Important:** Place your artifact (PNG, PDF, etc.) in `capsules/<artifact-name>/`

### Step 2: Artifact Assets
Add your artifact files to the capsule directory:
- **Diagrams** - PNG, SVG (primary artifacts)
- **Documents** - PDF, Markdown
- **Notes** - Markdown documentation
- **Metadata** - artifact.json

Example structure:
```
capsules/eternal-ledger/
├── eternal-ledger.png      # Main artifact
├── notes.md                # Documentation
└── artifact.json           # Metadata
```

### Step 3: Metadata Declaration
Create `artifact.json` with sovereign consent:

```json
{
  "artifactId": "capsule-name-001",
  "title": "Artifact Title",
  "version": "1.0.0",
  "crown": ["Efficiency", "Knowledge", "Commerce"],
  "cycle": "2025-12-02T14:38:00Z",
  "authors": ["Jermaine Merritt"],
  "consent": {
    "license": "CodexDominion Sovereign License v1",
    "attribution": "Jermaine Merritt",
    "revocationPolicy": "Revocable by Sovereign Avatar with ledger entry",
    "distribution": "Consent-first; educational and ceremonial use favored"
  }
}
```

### Step 4: Hash Calculation
Run integrity verification:

```bash
python scripts/calculate_hashes.py
```

This generates SHA256 hashes for all files and creates an immutable artifact hash.

### Step 5: Packaging
Package the capsule:

```bash
python scripts/package_artifacts.py
```

Creates compressed archives in `dist/` directory.

### Step 6: Syndication
Upload to distribution channels:

```bash
python scripts/upload_s3.py
```

Or push to GitHub to trigger automated syndication workflow.

## Revocation Ceremony

To revoke an artifact:

```bash
python scripts/revoke_artifact.py
```

This will:
1. Create immutable revocation ledger entry
2. Update artifact metadata with revocation status
3. Mark artifact as revoked across all channels

## Crown Alignments

Each artifact aligns with one or more crowns:

- **Efficiency** - Optimization, automation, systems
- **Knowledge** - Learning, education, wisdom
- **Commerce** - Trade, exchange, value creation
- **Innovation** - New ideas, breakthroughs, advancement
- **Security** - Protection, safety, sovereignty
- **Community** - Connection, cooperation, collective power

## Syndication Targets

Artifacts can be distributed to:
- **S3/CDN** - Global content delivery
- **GitHub Releases** - Version-controlled distribution
- **Diaspora Councils** - Community channels
- **Planetary Schools** - Educational institutions
- **Sovereign Corporations** - Enterprise networks

## Audit Trail

Every artifact maintains:
- Creation timestamp
- Author attribution
- Immutable hash (SHA256)
- File-level hashes
- Syndication history
- Revocation status (if applicable)

---

*These ceremonies ensure sovereign control and consent-first distribution across all platforms.*
