# Codex Dominion Artifact Syndication - Onboarding Guide

Welcome to the Codex Dominion artifact syndication system! This guide will help you get started as a contributor or distributor.

## Prerequisites

### Required
- Python 3.8 or higher
- Git
- AWS account (for S3 syndication)
- GitHub account

### Optional
- boto3 Python library (`pip install boto3`)
- GitHub CLI (`gh`)

## For Contributors

### 1. Clone the Repository

```bash
git clone https://github.com/JermaineMerritt-ai/codexdominion-schemas.git
cd codexdominion-schemas/codexdominion
```

### 2. Set Up Python Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install boto3
```

### 3. Create Your First Capsule

**Step 1:** Create the capsule directory
```bash
mkdir capsules/my-first-capsule
```

**Step 2:** Place your artifact (PNG, PDF, etc.) in `capsules/my-first-capsule/`
```bash
# Copy your artifact file
cp /path/to/your/diagram.png capsules/my-first-capsule/
```

**Step 3:** Add supporting files
```
capsules/my-first-capsule/
├── diagram.png           # Your main artifact (REQUIRED)
├── notes.md              # Documentation (REQUIRED)
└── artifact.json         # Metadata (REQUIRED)
```

### 4. Create Artifact Metadata

Create `capsules/my-first-capsule/artifact.json`:

```json
{
  "artifactId": "my-first-capsule-001",
  "title": "My First Artifact",
  "version": "1.0.0",
  "crown": ["Knowledge", "Innovation"],
  "cycle": "2025-12-02T14:38:00Z",
  "authors": ["Your Name"],
  "channels": [
    "Planetary Schools",
    "Diaspora Councils"
  ],
  "files": [
    {
      "path": "capsules/my-first-capsule/diagram.png",
      "contentType": "image/png"
    },
    {
      "path": "capsules/my-first-capsule/notes.md",
      "contentType": "text/markdown"
    }
  ],
  "consent": {
    "license": "CodexDominion Sovereign License v1",
    "attribution": "Your Name",
    "revocationPolicy": "Revocable by Sovereign Avatar with ledger entry",
    "distribution": "Consent-first; educational and ceremonial use favored"
  },
  "metadata": {
    "category": "your-category",
    "tags": ["education", "diagram", "tutorial"],
    "visibility": "public",
    "constellation": false
  },
  "syndication": {
    "targets": ["codexdominion.app"],
    "cdn_base_url": "https://cdn.codexdominion.app/artifacts",
    "compression": "gzip",
    "cache_ttl": 3600
  }
}
```

### 5. Calculate Hashes

```bash
python scripts/calculate_hashes.py
```

This will add SHA256 hashes to your artifact metadata.

### 6. Update Main Manifest

Add your capsule to `manifests/artifact.manifest.json`:

```json
{
  "artifacts": [
    {
      "id": "my-first-capsule",
      "name": "My First Capsule",
      "type": "educational-diagram",
      "capsule_path": "capsules/my-first-capsule",
      "assets": [
        {"filename": "diagram.png", "type": "image/png"},
        {"filename": "notes.md", "type": "text/markdown"},
        {"filename": "artifact.json", "type": "application/json"}
      ],
      "syndication_targets": ["s3", "github"]
    }
  ]
}
```

### 7. Test Packaging

```bash
python scripts/package_artifacts.py
```

Check that your capsule is packaged correctly in `dist/`.

### 8. Submit for Review

```bash
git add capsules/my-first-capsule
git add manifests/artifact.manifest.json
git commit -m "Add: My First Capsule artifact"
git push origin main
```

## For Distributors

### 1. Configure AWS Credentials

Set up AWS credentials for S3 syndication:

```bash
# Option 1: Environment variables
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_REGION="us-east-1"
export S3_BUCKET="codex-dominion-artifacts"

# Option 2: AWS CLI
aws configure
```

### 2. Configure GitHub Secrets

Add secrets to GitHub repository:

1. Go to: `https://github.com/JermaineMerritt-ai/codexdominion-schemas/settings/secrets/actions`
2. Add the following secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION`
   - `S3_BUCKET`

### 3. Manual Syndication

To manually syndicate artifacts:

```bash
# Package all capsules
python scripts/package_artifacts.py

# Upload to S3
python scripts/upload_s3.py
```

### 4. Automated Syndication

Push to GitHub to trigger automated workflow:

```bash
git push origin main
```

The GitHub Actions workflow will:
1. Calculate hashes
2. Package artifacts
3. Upload to S3
4. Create GitHub release

## Directory Structure

```
codexdominion/
├─ capsules/          # Artifact capsules
│  ├─ eternal-ledger/
│  │  ├─ eternal-ledger.png
│  │  ├─ notes.md
│  │  └─ artifact.json
│  └─ commerce-crown/
│     ├─ commerce-constellation.png
│     ├─ notes.md
│     └─ artifact.json
├─ manifests/         # Syndication manifests
│  ├─ artifact.manifest.json
│  ├─ index.json
│  └─ revocations.json
├─ scripts/           # Automation scripts
│  ├─ calculate_hashes.py
│  ├─ package_artifacts.py
│  ├─ upload_s3.py
│  └─ revoke_artifact.py
├─ .github/workflows/ # CI/CD automation
│  └─ syndication.yml
├─ docs/              # Documentation
│  ├─ ceremony-notes.md
│  ├─ onboarding-guide.md
│  └─ artifact-standards.md
└─ dist/              # Packaged artifacts (generated)
```

## Verification

Check artifact integrity:

```bash
# View current manifests
cat manifests/artifact.manifest.json
cat manifests/index.json

# Check revocation ledger
cat manifests/revocations.json

# View packaged artifacts
ls -lh dist/
```

## Troubleshooting

### Issue: "Manifest not found"
**Solution:** Run from the `codexdominion/` directory

### Issue: "boto3 not installed"
**Solution:** `pip install boto3`

### Issue: "AWS credentials not configured"
**Solution:** Set environment variables or run `aws configure`

### Issue: "File hash mismatch"
**Solution:** Re-run `python scripts/calculate_hashes.py`

## Support

For questions or issues:
- Open an issue on GitHub
- Contact: Sovereign Avatar
- Documentation: `docs/`

## Next Steps

1. ✅ Read ceremony notes: `docs/ceremony-notes.md`
2. ✅ Review artifact standards: `docs/artifact-standards.md`
3. ✅ Create your first capsule
4. ✅ Test packaging and syndication
5. ✅ Submit for review

Welcome to the Codex Dominion! 🔥

---

*Sovereign artifact distribution with consent-first policies*
