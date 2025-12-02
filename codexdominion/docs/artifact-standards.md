# Codex Dominion Artifact Standards

Technical standards and best practices for creating, packaging, and distributing artifacts through the Codex Dominion syndication system.

## File Formats

### Supported Image Formats
- **PNG** - Preferred for diagrams and visuals
- **SVG** - For scalable vector graphics
- **JPEG** - For photographs (use sparingly)

### Supported Document Formats
- **Markdown (.md)** - Preferred for notes and documentation
- **JSON (.json)** - For structured metadata
- **Text (.txt)** - For simple text content

### Compression
- ZIP format for packaging
- GZIP compression for CDN delivery

## Artifact Placement

### Directory Structure
**REQUIRED:** Place your artifact (PNG, PDF, etc.) in `capsules/<artifact-name>/`

```
capsules/<artifact-name>/
├── <artifact-name>.png     # Main artifact file
├── notes.md                # Documentation
└── artifact.json           # Metadata
```

## Naming Conventions

### Capsule Directories
```
capsules/[category]-[name]/
```

Examples:
- `capsules/eternal-ledger/` - Financial systems
- `capsules/commerce-crown/` - E-commerce network
- `capsules/knowledge-vault/` - Educational content

### Artifact IDs
```
[category]-[name]-[version-number]
```

Examples:
- `eternal-ledger-001`
- `commerce-crown-001`
- `knowledge-vault-001`

### File Names
- Use lowercase with hyphens: `eternal-ledger-diagram.png`
- Be descriptive: `quarterly-revenue-analysis.md`
- Avoid spaces and special characters

## Metadata Standards

### Required Fields

```json
{
  "artifactId": "string (required)",
  "title": "string (required)",
  "version": "string (required, semver)",
  "crown": ["array of strings (required)"],
  "cycle": "ISO 8601 timestamp (required)",
  "authors": ["array of strings (required)"],
  "files": ["array of file objects (required)"],
  "consent": {
    "license": "string (required)",
    "attribution": "string (required)",
    "revocationPolicy": "string (required)",
    "distribution": "string (required)"
  }
}
```

### Optional Fields

```json
{
  "channels": ["array of distribution channels"],
  "metadata": {
    "category": "string",
    "tags": ["array of strings"],
    "visibility": "public | private | restricted",
    "updateFrequency": "real-time | daily | weekly | static",
    "priority": "high | medium | low",
    "constellation": true | false
  },
  "syndication": {
    "targets": ["array of platforms"],
    "cdn_base_url": "string (URL)",
    "compression": "gzip | none",
    "cache_ttl": "number (seconds)"
  },
  "destinations": {
    "s3Bucket": "string",
    "releaseTag": "string",
    "githubRepo": "string"
  }
}
```

## Cryptographic Standards

### Hash Algorithm
- **SHA256** for all file integrity checks
- Immutable artifact hash calculated from all file hashes

### Hash Format
```json
{
  "files": [
    {
      "path": "capsules/example/file.png",
      "sha256": "hex-encoded-hash",
      "bytes": 12345
    }
  ],
  "audit": {
    "immutableHash": "combined-sha256-hash"
  }
}
```

## Versioning

### Semantic Versioning (SemVer)
```
MAJOR.MINOR.PATCH
```

- **MAJOR** - Breaking changes or complete overhauls
- **MINOR** - New features, backward compatible
- **PATCH** - Bug fixes, minor corrections

Examples:
- `1.0.0` - Initial release
- `1.1.0` - Added new diagram
- `1.1.1` - Fixed typo in notes

### Version Progression
```
1.0.0 → 1.0.1 → 1.1.0 → 2.0.0
```

## Crown Alignments

Artifacts must declare crown alignment(s):

### Available Crowns
- **Efficiency** - Optimization, automation, systems
- **Knowledge** - Learning, education, wisdom
- **Commerce** - Trade, exchange, value creation
- **Innovation** - New ideas, breakthroughs
- **Security** - Protection, sovereignty
- **Community** - Connection, cooperation
- **Sustainability** - Long-term viability
- **Excellence** - Quality, mastery

### Guidelines
- Minimum: 1 crown
- Maximum: 5 crowns
- Choose most relevant alignments

## Distribution Channels

### Primary Channels
- **Planetary Schools** - Educational institutions
- **Sovereign Corporations** - Enterprise networks
- **Diaspora Councils** - Community channels
- **Ministries & Archives** - Government and historical

### Platform Targets
- **S3/CDN** - Global content delivery
- **GitHub** - Version control and releases
- **Custom APIs** - Integration endpoints

## Size Limits

### Individual Files
- Images: Max 10 MB
- Documents: Max 5 MB
- Metadata: Max 500 KB

### Packaged Artifacts
- Single capsule: Max 50 MB
- Combined manifest: Max 100 MB

## Cache and TTL

### Recommended TTL Values
- Static diagrams: 86400s (24 hours)
- Dynamic dashboards: 3600s (1 hour)
- Real-time data: 300s (5 minutes)

### CDN Configuration
```json
{
  "compression": "gzip",
  "cache_ttl": 3600,
  "cache-control": "public, max-age=3600"
}
```

## Quality Guidelines

### Images
- Resolution: Minimum 1920x1080 for diagrams
- DPI: 150+ for print-ready
- Color space: RGB for web, CMYK for print
- Optimize: Use compression without quality loss

### Documents
- Markdown: Follow CommonMark spec
- Line length: Max 79 characters (code blocks excepted)
- Headers: Use ATX-style (#)
- Links: Use reference-style for readability

### JSON
- Indent: 2 spaces
- Encoding: UTF-8
- Validation: Must pass JSON schema validation
- Formatting: Pretty-printed

## Security Standards

### Access Control
- Public artifacts: Open distribution
- Restricted artifacts: Require authentication
- Private artifacts: Sovereign Avatar only

### Revocation
- Immutable ledger entries
- Immediate propagation across channels
- Replacement artifact specification

## Audit Requirements

Every artifact must include:

```json
{
  "audit": {
    "createdBy": "string (system or author)",
    "createdAt": "ISO 8601 timestamp",
    "immutableHash": "SHA256 hex string"
  }
}
```

## Validation

### Pre-Packaging Checks
1. ✅ All files exist
2. ✅ Metadata is valid JSON
3. ✅ Required fields present
4. ✅ Crown alignments valid
5. ✅ File sizes within limits

### Post-Packaging Checks
1. ✅ Package file created
2. ✅ Hashes calculated
3. ✅ Manifest updated
4. ✅ No corruption detected

### Syndication Checks
1. ✅ AWS credentials valid
2. ✅ S3 bucket accessible
3. ✅ Upload successful
4. ✅ CDN cache invalidated

## Error Handling

### Common Issues

**Missing Files**
```
⚠️ Warning: Asset not found: capsules/example/missing.png
```
Action: Add missing file or remove from manifest

**Invalid JSON**
```
❌ Error: Invalid JSON in artifact.json
```
Action: Validate JSON syntax

**Hash Mismatch**
```
❌ Error: File hash does not match manifest
```
Action: Recalculate hashes with `calculate_hashes.py`

**Upload Failed**
```
❌ Error: S3 upload failed: Access Denied
```
Action: Verify AWS credentials and bucket permissions

## Testing Checklist

Before submitting an artifact:

- [ ] All files present and valid
- [ ] Metadata complete and accurate
- [ ] Hashes calculated (`calculate_hashes.py`)
- [ ] Package created (`package_artifacts.py`)
- [ ] Local test passed
- [ ] Crown alignments appropriate
- [ ] License and attribution correct
- [ ] Version number follows SemVer

## Continuous Improvement

### Feedback Loop
1. Create artifact
2. Syndicate
3. Gather feedback
4. Iterate
5. Update version

### Version Updates
- Document changes in notes.md
- Update version in artifact.json
- Recalculate hashes
- Repackage and syndicate

---

*These standards ensure consistency, quality, and integrity across all Codex Dominion artifacts.*
