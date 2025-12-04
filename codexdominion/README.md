# 🔥 Codex Dominion Artifact Syndication

**Version:** 2.0.0
**Status:** Active
**Last Updated:** December 2, 2025

## Overview

The Codex Dominion Artifact Syndication system enables global distribution of constellation capsules, visual assets, and sovereign data across multiple platforms and CDN networks.

## Structure

```
codexdominion/
├─ capsules/              # Constellation capsules
│  ├─ eternal-ledger/     # Financial sovereignty dashboard
│  │  ├─ eternal-ledger.png
│  │  └─ notes.md
│  ├─ commerce-crown/     # E-commerce & affiliate network
│  │  ├─ commerce-constellation.png
│  │  └─ notes.md
├─ manifests/             # Syndication manifests
│  ├─ artifact.manifest.json  # Main artifact manifest
│  └─ index.json          # Capsule index
├─ scripts/               # Automation scripts
│  ├─ package_artifacts.py    # Package capsules
│  └─ upload_s3.py        # Upload to S3/CDN
├─ .github/
│  └─ workflows/
│     └─ syndication.yml  # Automated syndication
└─ README.md
```

## Capsules

### 🏦 Eternal Ledger
**Type:** Financial Sovereignty Dashboard
**Purpose:** Immutable record of all treasury operations, transactions, and revenue streams

- Real-time treasury tracking
- Multi-source revenue aggregation
- Blockchain-integrated ledger
- Audit trail and compliance

### 👑 Commerce Crown
**Type:** E-Commerce & Affiliate Network
**Purpose:** Sovereign marketplace infrastructure and affiliate integrations

- Multi-platform affiliate tracking
- E-commerce integration
- Revenue optimization
- Customer analytics

## Quick Start

1. **Create capsule directory:** `mkdir capsules/<artifact-name>`
2. **Place your artifact:** Copy your PNG, PDF, etc. to `capsules/<artifact-name>/`
3. **Add documentation:** Create `notes.md` in the capsule directory
4. **Create metadata:** Add `artifact.json` with sovereign consent model
5. **Calculate hashes:** Run `python scripts/calculate_hashes.py`
6. **Package artifacts:** Run `python scripts/package_artifacts.py`
7. **Syndicate:** Run `python scripts/upload_s3.py` (or push to trigger GitHub Actions)

### Example Capsule Structure
```
capsules/eternal-ledger/
├── eternal-ledger.png      # Your artifact (REQUIRED)
├── notes.md                # Documentation (REQUIRED)
└── artifact.json           # Metadata (REQUIRED)
```

## Usage

### Package Artifacts

```bash
cd codexdominion
python scripts/package_artifacts.py
```

This will:
1. Validate all capsules against manifest
2. Package each capsule as `.zip` archive
3. Generate syndication metadata
4. Output to `dist/` directory

### Upload to CDN

```bash
cd codexdominion
python scripts/upload_s3.py
```

Prerequisites:
- AWS credentials configured (environment variables or `~/.aws/credentials`)
- S3 bucket created or script will create it
- boto3 installed: `pip install boto3`

This will:
1. Load syndication metadata
2. Create/verify S3 bucket
3. Upload all packaged artifacts
4. Set proper cache headers and ACLs
5. Generate CDN URLs

### Automated Syndication

The GitHub Actions workflow `.github/workflows/syndication.yml` automatically:

- **Triggers:**
  - Push to main branch (capsule/manifest changes)
  - Daily at 3 AM UTC
  - Manual workflow dispatch

- **Jobs:**
  1. Validate: Check manifests and capsule integrity
  2. Package: Create distribution archives
  3. Syndicate: Upload to S3/CDN
  4. Notify: Send completion notifications

## Manifest Schema

### artifact.manifest.json

```json
{
  "manifest_version": "1.0.0",
  "codex_version": "2.0.0",
  "syndication_id": "unique-id",
  "artifacts": [
    {
      "id": "capsule-id",
      "name": "Capsule Name",
      "type": "capsule-type",
      "capsule_path": "capsules/path",
      "assets": [
        {
          "filename": "asset.png",
          "type": "image/png",
          "purpose": "constellation-visual"
        }
      ],
      "metadata": {
        "category": "finance",
        "tags": ["tag1", "tag2"],
        "visibility": "public"
      },
      "syndication_targets": [
        "platform1",
        "platform2"
      ]
    }
  ],
  "syndication_config": {
    "s3_bucket": "bucket-name",
    "cdn_base_url": "https://cdn.example.com",
    "compression": "gzip",
    "cache_ttl": 3600
  }
}
```

## CDN Configuration

### S3 Bucket Structure

```
codex-dominion-artifacts/
├─ capsules/
│  ├─ eternal-ledger/
│  │  └─ codex-eternal-ledger-YYYYMMDD_HHMMSS.zip
│  └─ commerce-crown/
│     └─ codex-commerce-crown-YYYYMMDD_HHMMSS.zip
└─ syndication.json
```

### Cache Settings

- **TTL:** 1 hour (3600 seconds)
- **Compression:** gzip enabled
- **Access:** Public read
- **Content-Type:** Set per file type

## Integration

### Accessing Syndicated Artifacts

```javascript
// Fetch syndication metadata
const response = await fetch('https://cdn.codexdominion.app/artifacts/syndication.json');
const metadata = await response.json();

// Download specific capsule
const capsule = metadata.capsules.find(c => c.id === 'eternal-ledger');
const packageUrl = `${metadata.cdn_base_url}/${capsule.package_file}`;
```

### API Endpoints

- **Syndication metadata:** `GET /syndication.json`
- **Capsule package:** `GET /capsules/{id}/{package_file}`
- **Manifest:** `GET /manifests/artifact.manifest.json`

## Development

### Adding New Capsules

1. **Create capsule directory:** `mkdir capsules/<artifact-name>/`
2. **Place your artifact (PNG, PDF, etc.)** in `capsules/<artifact-name>/`
3. **Add documentation:** Create `notes.md` with artifact description
4. **Create metadata:** Add `artifact.json` with sovereign consent
5. **Update manifests:** Edit `manifests/artifact.manifest.json` and `index.json`
6. **Calculate hashes:** Run `python scripts/calculate_hashes.py`
7. **Test packaging:** Run `python scripts/package_artifacts.py`
8. **Commit and push:** Triggers auto-syndication via GitHub Actions

### Local Testing

```bash
# Validate manifests
cd codexdominion
python -m json.tool manifests/artifact.manifest.json

# Test packaging
python scripts/package_artifacts.py

# Check dist output
ls -la dist/
```

## Security

- **Assets:** Public read access on CDN
- **Credentials:** AWS secrets stored in GitHub Actions secrets
- **Validation:** Manifest validation before syndication
- **Integrity:** SHA256 checksums for all packages

## Monitoring

- **GitHub Actions:** Monitor workflow runs
- **S3 Metrics:** CloudWatch for bucket metrics
- **CDN Stats:** CloudFront analytics (if configured)
- **Logs:** GitHub Actions logs for debugging

## Troubleshooting

### Common Issues

**Package validation fails:**
- Check all asset files exist
- Validate manifest JSON syntax
- Ensure capsule directories present

**S3 upload fails:**
- Verify AWS credentials set
- Check bucket permissions
- Confirm region configuration

**CDN cache not updating:**
- Invalidate CloudFront cache
- Check cache TTL settings
- Verify S3 object metadata

## Support

- **Documentation:** This README
- **Issues:** GitHub repository issues
- **Workflows:** `.github/workflows/syndication.yml`
- **Scripts:** `scripts/` directory

---

_Artifacts eternal. Distribution sovereign. The constellation syndicated across the digital cosmos._ 🔥🌐

**The Codex Dominion syndication system: Where artifacts become immortal.**
