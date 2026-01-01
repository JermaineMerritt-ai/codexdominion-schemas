# Intelligence Core API Reference

## Quick Start

**Start Flask Server:**
```bash
python flask_dashboard.py
```

**Test All Endpoints:**
```bash
python test_api_endpoints.py
```

## API Endpoints

### 1. Industries

**Get All Industries**
```bash
curl http://localhost:5000/api/industries
```
Returns: 12 industries with capsule mappings, compliance requirements, revenue streams

**Get Specific Industry**
```bash
curl http://localhost:5000/api/industries/faith_education
curl http://localhost:5000/api/industries/stock_trading
curl http://localhost:5000/api/industries/ecommerce
```
Returns: Single industry with all details

### 2. Niches

**Get All Niches**
```bash
curl http://localhost:5000/api/niches
```
Returns: 18 niches with complete blueprints

**Get Niches by Industry**
```bash
curl http://localhost:5000/api/niches/industry/faith_education
curl http://localhost:5000/api/niches/industry/stock_trading
curl http://localhost:5000/api/niches/industry/content_creation
```
Returns: Filtered niches with industry cross-reference

### 3. Domain Packs

**Get All Domain Packs**
```bash
curl http://localhost:5000/api/domain-packs
```
Returns: 12 domain packs with templates, workflows, integrations

**Get Specific Domain Pack**
```bash
curl http://localhost:5000/api/domain-packs/faith_education_pack
curl http://localhost:5000/api/domain-packs/ecommerce_automation_pack
curl http://localhost:5000/api/domain-packs/stock_trading_pack
```
Returns: Single pack with complete components

### 4. System Status

**Get Phase 1 Status**
```bash
curl http://localhost:5000/api/phase-1-status
```
Returns: Activation status of 3 Phase 1 engines with counts and operational status

### 5. Cross-Reference

**Get Complete Industry Mapping**
```bash
curl http://localhost:5000/api/cross-reference/faith_education
curl http://localhost:5000/api/cross-reference/stock_trading
```
Returns: Industry + related niches + related packs + statistics

## Response Examples

### Industry Response
```json
{
  "id": "faith_education",
  "name": "Faith & Education",
  "description": "Christian education, Bible study, devotionals...",
  "primary_capsules": ["youth", "knowledge", "story", "culture"],
  "secondary_capsules": ["creator", "media"],
  "target_audiences": ["families", "children", "educators", "churches"],
  "compliance_requirements": ["coppa", "youth_protection", "content_safety"]
}
```

### Niche Response
```json
{
  "id": "kids_bible_stories",
  "name": "Kids Bible Stories",
  "industry": "faith_education",
  "blueprint": {
    "content_pillars": ["Old Testament stories", "New Testament stories", ...],
    "product_types": ["coloring_books", "activity_books", ...],
    "pricing_strategy": "freemium_to_subscription"
  },
  "active_engines": ["niche_blueprints", "cultural_intelligence"]
}
```

### Domain Pack Response
```json
{
  "id": "faith_education_pack",
  "name": "Faith & Education Domain Pack",
  "industry": "faith_education",
  "components": {
    "templates": ["devotional_template", "bible_story_outline", ...],
    "workflows": ["content_creation_workflow", "age_appropriateness_review", ...],
    "integrations": ["woocommerce_digital_products", "mailchimp_devotional_series", ...]
  },
  "pre_configured_settings": {
    "youth_protection": "strict",
    "content_moderation": "enabled"
  }
}
```

### Phase 1 Status Response
```json
{
  "phase": 1,
  "name": "Structural Intelligence",
  "status": "operational",
  "engines": [
    {
      "name": "Industry Ontology Engine",
      "file": "industries.json",
      "count": 12,
      "operational": true
    },
    {
      "name": "Niche Blueprint Engine",
      "file": "niches.json",
      "count": 18,
      "operational": true
    },
    {
      "name": "Domain Expertise Packs",
      "file": "domain_packs.json",
      "count": 12,
      "operational": true
    }
  ]
}
```

### Cross-Reference Response
```json
{
  "industry": { /* full industry object */ },
  "niches": [ /* array of related niches */ ],
  "packs": [ /* array of related packs */ ],
  "stats": {
    "niche_count": 2,
    "pack_count": 1,
    "total_engines": 3
  }
}
```

## Available Industry IDs
- `faith_education`
- `homeschool`
- `wedding_planning`
- `digital_art`
- `stock_trading`
- `content_creation`
- `ecommerce`
- `affiliate_marketing`
- `healthcare_wellness`
- `legal_compliance`
- `community_engagement`
- `ai_automation`

## Available Niche IDs
- `kids_bible_stories`
- `homeschool_curriculum`
- `wedding_printables`
- `christian_coloring`
- `stock_signals_daily`
- `youtube_automation`
- `digital_product_store`
- `affiliate_tracking`

## Available Pack IDs
- `faith_education_pack`
- `homeschool_pack`
- `wedding_commerce_pack`
- `digital_art_pack`
- `stock_trading_pack`
- `content_automation_pack`
- `ecommerce_automation_pack`
- `affiliate_optimization_pack`
- `healthcare_compliance_pack`
- `legal_automation_pack`
- `community_engagement_pack`
- `ai_development_pack`

## Testing with PowerShell

```powershell
# Test single endpoint
Invoke-RestMethod -Uri "http://localhost:5000/api/phase-1-status" | ConvertTo-Json -Depth 10

# Save response to file
Invoke-RestMethod -Uri "http://localhost:5000/api/industries/faith_education" | ConvertTo-Json -Depth 10 | Out-File response.json

# Test all endpoints
python test_api_endpoints.py
```

## Helper Functions Available in Flask

```python
from flask_dashboard import (
    get_industry,
    get_niche,
    get_domain_pack,
    get_niches_by_industry,
    get_blueprint_for_niche,
    get_pack_components,
    cross_reference_industry,
    get_phase_1_status
)
```

## Notes

- All endpoints return JSON
- 404 error if ID not found
- Cached after first load for performance
- UTF-8 encoding for full emoji/unicode support
- CORS enabled for Next.js integration

🔥 **Phase 1: Structural Intelligence — OPERATIONAL** 👑
