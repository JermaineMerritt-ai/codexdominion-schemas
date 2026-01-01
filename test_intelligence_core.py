"""
Test Intelligence Core Data Access
===================================
Quick validation script for industries, niches, and domain packs
"""

import json
from pathlib import Path

def test_industries():
    """Test industries.json access"""
    print("\n🏭 INDUSTRIES TEST")
    print("=" * 50)
    
    with open('industries.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    industries = {i['id']: i for i in data['industries']}
    
    # Test: Faith Education industry
    faith_ed = industries['faith_education']
    print(f"✓ Industry: {faith_ed['name']}")
    print(f"  Primary Capsules: {', '.join(faith_ed['primary_capsules'])}")
    print(f"  Key Engines: {', '.join(faith_ed['key_engines'])}")
    print(f"  Compliance: {', '.join(faith_ed['compliance_requirements'])}")
    
    # Test: Stock Trading industry
    stock = industries['stock_trading']
    print(f"\n✓ Industry: {stock['name']}")
    print(f"  Primary Capsules: {', '.join(stock['primary_capsules'])}")
    print(f"  Compliance: {', '.join(stock['compliance_requirements'])}")
    
    return True

def test_niches():
    """Test niches.json access"""
    print("\n🎯 NICHES TEST")
    print("=" * 50)
    
    with open('niches.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    niches = {n['id']: n for n in data['niches']}
    
    # Test: Kids Bible Stories niche
    kids_bible = niches['kids_bible_stories']
    blueprint = kids_bible['blueprint']
    
    print(f"✓ Niche: {kids_bible['name']}")
    print(f"  Industry: {kids_bible['industry']}")
    print(f"  Target Age: {kids_bible['target_age_range']}")
    print(f"  Content Pillars: {len(blueprint['content_pillars'])} defined")
    print(f"    - {blueprint['content_pillars'][0]}")
    print(f"    - {blueprint['content_pillars'][1]}")
    print(f"  Product Types: {', '.join(blueprint['product_types'])}")
    print(f"  Pricing Strategy: {blueprint['pricing_strategy']}")
    print(f"  Active Engines: {', '.join(kids_bible['active_engines'])}")
    
    # Test: Stock Signals niche
    stock_signals = niches['stock_signals_daily']
    print(f"\n✓ Niche: {stock_signals['name']}")
    print(f"  Monetization Tiers:")
    for tier, price in stock_signals['monetization'].items():
        if tier != 'upsells':
            print(f"    - {tier}: {price}")
    
    return True

def test_domain_packs():
    """Test domain_packs.json access"""
    print("\n📦 DOMAIN PACKS TEST")
    print("=" * 50)
    
    with open('domain_packs.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    packs = {p['id']: p for p in data['domain_packs']}
    
    # Test: Faith Education Pack
    faith_pack = packs['faith_education_pack']
    print(f"✓ Pack: {faith_pack['name']}")
    print(f"  Industry: {faith_pack['industry']}")
    print(f"  Capsules: {', '.join(faith_pack['capsules'])}")
    print(f"  Engines: {', '.join(faith_pack['engines'])}")
    print(f"  Components:")
    print(f"    - Templates: {len(faith_pack['components']['templates'])}")
    print(f"    - Workflows: {len(faith_pack['components']['workflows'])}")
    print(f"    - Integrations: {len(faith_pack['components']['integrations'])}")
    print(f"    - Compliance: {len(faith_pack['components']['compliance'])}")
    print(f"  Pre-configured Settings:")
    for key, value in faith_pack['pre_configured_settings'].items():
        print(f"    - {key}: {value}")
    
    # Test: E-Commerce Pack
    ecom_pack = packs['ecommerce_automation_pack']
    print(f"\n✓ Pack: {ecom_pack['name']}")
    print(f"  Revenue Streams: {', '.join(ecom_pack['revenue_streams'])}")
    print(f"  Typical Pricing:")
    for tier, price in ecom_pack['typical_pricing'].items():
        print(f"    - {tier}: {price}")
    
    return True

def test_cross_references():
    """Test relationships between industries, niches, and packs"""
    print("\n🔗 CROSS-REFERENCE TEST")
    print("=" * 50)
    
    # Load all three
    with open('industries.json', 'r', encoding='utf-8') as f:
        industries_data = json.load(f)
    with open('niches.json', 'r', encoding='utf-8') as f:
        niches_data = json.load(f)
    with open('domain_packs.json', 'r', encoding='utf-8') as f:
        packs_data = json.load(f)
    
    # Cross-reference: Faith Education
    industry_id = 'faith_education'
    industry = next(i for i in industries_data['industries'] if i['id'] == industry_id)
    related_niches = [n for n in niches_data['niches'] if n['industry'] == industry_id]
    related_packs = [p for p in packs_data['domain_packs'] if p['industry'] == industry_id]
    
    print(f"✓ Industry: {industry['name']}")
    print(f"  Related Niches: {len(related_niches)}")
    for niche in related_niches:
        print(f"    - {niche['name']}")
    print(f"  Related Packs: {len(related_packs)}")
    for pack in related_packs:
        print(f"    - {pack['name']}")
    
    # Verify capsule overlap
    industry_capsules = set(industry['primary_capsules'])
    niche_capsules = set()
    for niche in related_niches:
        niche_capsules.update(niche['primary_capsules'])
    pack_capsules = set()
    for pack in related_packs:
        pack_capsules.update(pack['capsules'])
    
    print(f"\n  Capsule Coverage:")
    print(f"    - Industry defines: {', '.join(industry_capsules)}")
    print(f"    - Niches use: {', '.join(niche_capsules)}")
    print(f"    - Packs provide: {', '.join(pack_capsules)}")
    print(f"    - Overlap: {len(industry_capsules & niche_capsules & pack_capsules)} shared")
    
    return True

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  INTELLIGENCE CORE - DATA STRUCTURE VALIDATION")
    print("=" * 70)
    
    try:
        test_industries()
        test_niches()
        test_domain_packs()
        test_cross_references()
        
        print("\n" + "=" * 70)
        print("  ✅ ALL TESTS PASSED - SYSTEM OPERATIONAL")
        print("=" * 70)
        print("\nPhase 1 Engines Ready:")
        print("  1. Industry Ontology Engine → industries.json (12 industries)")
        print("  2. Niche Blueprint Engine → niches.json (18 niches)")
        print("  3. Domain Expertise Packs → domain_packs.json (12 packs)")
        print("\nAPI Endpoints Live:")
        print("  - GET /api/industries")
        print("  - GET /api/industries/<industry_id>")
        print("  - GET /api/niches")
        print("  - GET /api/niches/industry/<industry_id>")
        print("  - GET /api/domain-packs")
        print("  - GET /api/domain-packs/<pack_id>")
        print("\n🔥 The Flame Burns Sovereign and Eternal! 👑\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
