"""
Intelligence Core - All Access Patterns Test
=============================================
Tests all three requested access patterns for Phase 1
"""

import json

print("\n" + "="*70)
print("  INTELLIGENCE CORE - ACCESS PATTERN VALIDATION")
print("="*70)

# Pattern 1: Industries → Capsules
print("\n📋 PATTERN 1: Industries → Capsules")
print("-" * 70)
industries_data = json.load(open('industries.json'))
industries = {i['id']: i for i in industries_data['industries']}
user_industry = "faith_education"
capsules = industries[user_industry]["primary_capsules"]
print(f"✓ Industry: {industries[user_industry]['name']}")
print(f"  Primary Capsules: {capsules}")
print(f"  → {', '.join(capsules)}")

# Pattern 2: Niches → Blueprint
print("\n📋 PATTERN 2: Niches → Blueprint")
print("-" * 70)
niches_data = json.load(open('niches.json'))
niches = {n['id']: n for n in niches_data['niches']}
blueprint = niches['kids_bible_stories']['blueprint']
print(f"✓ Niche: {niches['kids_bible_stories']['name']}")
print(f"  Blueprint Components:")
print(f"    - Content Pillars: {blueprint['content_pillars'][:2]}")
print(f"    - Product Types: {blueprint['product_types'][:2]}")
print(f"    - Pricing Strategy: {blueprint['pricing_strategy']}")
print(f"    - Distribution: {blueprint['distribution_channels']}")

# Pattern 3: Domain Packs → Templates & Workflows
print("\n📋 PATTERN 3: Domain Packs → Templates & Workflows")
print("-" * 70)
packs_data = json.load(open('domain_packs.json'))
packs = {p['id']: p for p in packs_data['domain_packs']}
pack = packs["faith_education_pack"]
templates = pack["components"]["templates"]
workflows = pack["components"]["workflows"]
print(f"✓ Pack: {pack['name']}")
print(f"  Templates ({len(templates)}):")
for t in templates:
    print(f"    - {t}")
print(f"  Workflows ({len(workflows)}):")
for w in workflows:
    print(f"    - {w}")

# Cross-Pattern Integration Test
print("\n📋 CROSS-PATTERN INTEGRATION")
print("-" * 70)
# From industry → find niches → get their packs
industry_niches = [n for n in niches_data['niches'] if n['industry'] == user_industry]
industry_packs = [p for p in packs_data['domain_packs'] if p['industry'] == user_industry]

print(f"✓ Industry: {industries[user_industry]['name']}")
print(f"  └─ Related Niches: {len(industry_niches)}")
for niche in industry_niches:
    print(f"     - {niche['name']}")
    print(f"       Engines: {', '.join(niche['active_engines'][:2])}...")
print(f"  └─ Related Packs: {len(industry_packs)}")
for pack in industry_packs:
    print(f"     - {pack['name']}")
    print(f"       Components: {len(pack['components']['templates'])} templates, {len(pack['components']['workflows'])} workflows")

# Performance Stats
print("\n📊 SYSTEM STATISTICS")
print("-" * 70)
total_industries = len(industries_data['industries'])
total_niches = len(niches_data['niches'])
total_packs = len(packs_data['domain_packs'])
total_templates = sum(len(p['components']['templates']) for p in packs_data['domain_packs'])
total_workflows = sum(len(p['components']['workflows']) for p in packs_data['domain_packs'])
total_integrations = sum(len(p['components']['integrations']) for p in packs_data['domain_packs'])

print(f"✓ Industries: {total_industries}")
print(f"✓ Niches: {total_niches}")
print(f"✓ Domain Packs: {total_packs}")
print(f"✓ Total Templates: {total_templates}")
print(f"✓ Total Workflows: {total_workflows}")
print(f"✓ Total Integrations: {total_integrations}")

# Verify all requested patterns work
print("\n✅ ALL ACCESS PATTERNS VALIDATED")
print("="*70)
print("\nReady for use:")
print("  1. industries[id]['primary_capsules'] → list of capsules")
print("  2. niches[id]['blueprint'] → complete blueprint dict")
print("  3. packs[id]['components'] → templates, workflows, integrations")
print("\n🔥 Phase 1: Structural Intelligence — OPERATIONAL 👑\n")
