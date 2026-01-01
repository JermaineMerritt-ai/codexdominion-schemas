"""
🔥 WEBSITE CREATION WORKFLOW - DEMO & TEST SCRIPT 🔥
====================================================
Quick test execution to verify the complete workflow
"""

from website_creation_execution_complete import execute_website_creation_complete
import json

def demo_basic_site():
    """Demo 1: Basic professional website"""
    print("\n" + "="*80)
    print("DEMO 1: Basic Professional Website")
    print("="*80)
    
    result = execute_website_creation_complete(
        site_name="Acme Consulting Group",
        description="Strategic business consulting and advisory services for enterprise clients",
        pages=["home", "about", "services", "contact"],
        brand_colors={
            "primary": "#1a202c",  # Dark blue-gray
            "secondary": "#edf2f7",  # Light gray
            "accent": "#3182ce"  # Blue
        },
        typography={
            "heading": "Montserrat",
            "body": "Open Sans"
        },
        tone="professional",
        platform="nextjs",
        output_dir="./test_output"
    )
    
    print(f"\n✅ Demo 1 Complete!")
    print(f"   Output: {result['output_directory']}")
    print(f"   Duration: {result['duration_seconds']}s")
    return result


def demo_creative_agency():
    """Demo 2: Creative/playful agency site"""
    print("\n" + "="*80)
    print("DEMO 2: Creative Agency Website")
    print("="*80)
    
    result = execute_website_creation_complete(
        site_name="Pixel Perfect Studios",
        description="Bold, beautiful web design that makes your brand unforgettable",
        pages=["home", "about", "services", "portfolio", "contact"],
        brand_colors={
            "primary": "#8b5cf6",  # Purple
            "secondary": "#fbbf24",  # Yellow
            "accent": "#ec4899"  # Pink
        },
        typography={
            "heading": "Poppins",
            "body": "Inter"
        },
        tone="playful",
        platform="nextjs",
        output_dir="./test_output"
    )
    
    print(f"\n✅ Demo 2 Complete!")
    print(f"   Output: {result['output_directory']}")
    print(f"   Duration: {result['duration_seconds']}s")
    return result


def demo_luxury_brand():
    """Demo 3: Luxury/premium brand site"""
    print("\n" + "="*80)
    print("DEMO 3: Luxury Brand Website")
    print("="*80)
    
    result = execute_website_creation_complete(
        site_name="Noir Elegance",
        description="Timeless luxury and sophisticated design for discerning clientele",
        pages=["home", "about", "services", "team", "contact"],
        brand_colors={
            "primary": "#000000",  # Black
            "secondary": "#f5f5f5",  # Off-white
            "accent": "#d4af37"  # Gold
        },
        typography={
            "heading": "Playfair Display",
            "body": "Lato"
        },
        tone="luxury",
        platform="nextjs",
        output_dir="./test_output"
    )
    
    print(f"\n✅ Demo 3 Complete!")
    print(f"   Output: {result['output_directory']}")
    print(f"   Duration: {result['duration_seconds']}s")
    return result


def demo_tech_startup():
    """Demo 4: Tech startup with blog"""
    print("\n" + "="*80)
    print("DEMO 4: Tech Startup Website")
    print("="*80)
    
    result = execute_website_creation_complete(
        site_name="CloudVault AI",
        description="Next-generation cloud security powered by artificial intelligence",
        pages=["home", "about", "services", "pricing", "blog", "contact"],
        brand_colors={
            "primary": "#0f172a",  # Dark slate
            "secondary": "#e0f2fe",  # Light blue
            "accent": "#06b6d4"  # Cyan
        },
        typography={
            "heading": "Inter",
            "body": "Inter"
        },
        tone="professional",
        platform="nextjs",
        output_dir="./test_output"
    )
    
    print(f"\n✅ Demo 4 Complete!")
    print(f"   Output: {result['output_directory']}")
    print(f"   Duration: {result['duration_seconds']}s")
    return result


def verify_output_structure(result):
    """Verify all expected files were created"""
    import os
    from pathlib import Path
    
    print("\n" + "="*80)
    print("VERIFICATION: Checking Output Structure")
    print("="*80)
    
    output_dir = Path(result['output_directory'])
    
    required_files = [
        'site.json',
        'content.json',
        'seo.json',
        'theme.json',
        'theme.css',
        'robots.txt',
        'EXECUTION_SUMMARY.json'
    ]
    
    all_exist = True
    for filename in required_files:
        filepath = output_dir / filename
        exists = filepath.exists()
        status = "✅" if exists else "❌"
        print(f"{status} {filename}")
        if not exists:
            all_exist = False
    
    # Check pages directory
    pages_dir = output_dir / "pages"
    if pages_dir.exists():
        page_files = list(pages_dir.glob("*.json"))
        print(f"✅ pages/ directory ({len(page_files)} pages)")
        for page_file in page_files:
            print(f"   ✓ {page_file.name}")
    else:
        print("❌ pages/ directory")
        all_exist = False
    
    print("\n" + "-"*80)
    if all_exist:
        print("✅ VERIFICATION PASSED - All files generated successfully!")
    else:
        print("❌ VERIFICATION FAILED - Some files are missing!")
    print("="*80)
    
    return all_exist


def inspect_generated_content(result):
    """Inspect and display generated content samples"""
    from pathlib import Path
    
    print("\n" + "="*80)
    print("CONTENT INSPECTION")
    print("="*80)
    
    output_dir = Path(result['output_directory'])
    
    # Load and display content sample
    content_file = output_dir / "content.json"
    if content_file.exists():
        with open(content_file, 'r') as f:
            content = json.load(f)
        
        # Show home page hero content
        if "home" in content["pages"]:
            home = content["pages"]["home"]
            print("\n📝 HOME PAGE HERO:")
            print(f"   Title: {home.get('hero_title', 'N/A')}")
            print(f"   Subtitle: {home.get('hero_subtitle', 'N/A')}")
            print(f"   CTA: {home.get('cta_text', 'N/A')}")
    
    # Load and display theme sample
    theme_file = output_dir / "theme.json"
    if theme_file.exists():
        with open(theme_file, 'r') as f:
            theme = json.load(f)
        
        print("\n🎨 BRAND THEME:")
        colors = theme.get('colors', {}).get('brand', {})
        print(f"   Primary: {colors.get('primary', {}).get('500', 'N/A')}")
        print(f"   Secondary: {colors.get('secondary', {}).get('500', 'N/A')}")
        print(f"   Accent: {colors.get('accent', {}).get('500', 'N/A')}")
        
        fonts = theme.get('typography', {}).get('fonts', {})
        print(f"   Heading Font: {fonts.get('heading', 'N/A')}")
        print(f"   Body Font: {fonts.get('body', 'N/A')}")
    
    # Load and display SEO sample
    seo_file = output_dir / "seo.json"
    if seo_file.exists():
        with open(seo_file, 'r') as f:
            seo = json.load(f)
        
        print("\n🔍 SEO METADATA:")
        global_seo = seo.get('global', {})
        print(f"   Site Name: {global_seo.get('site_name', 'N/A')}")
        print(f"   Description: {global_seo.get('default_description', 'N/A')[:80]}...")
        
        if "pages" in seo and "home" in seo["pages"]:
            home_seo = seo["pages"]["home"]
            print(f"   Home Title: {home_seo.get('title', 'N/A')}")
            print(f"   OG Image: {home_seo.get('og', {}).get('image', 'N/A')}")
    
    print("\n" + "="*80)


def run_all_demos():
    """Run all demonstration workflows"""
    print("\n" + "🔥"*40)
    print(" CODEX DOMINION - WEBSITE CREATION WORKFLOW")
    print(" Complete Execution Demonstration")
    print("🔥"*40)
    
    demos = [
        ("Basic Professional Site", demo_basic_site),
        ("Creative Agency Site", demo_creative_agency),
        ("Luxury Brand Site", demo_luxury_brand),
        ("Tech Startup Site", demo_tech_startup)
    ]
    
    results = []
    for name, demo_func in demos:
        try:
            result = demo_func()
            results.append((name, result, True))
        except Exception as e:
            print(f"\n❌ {name} FAILED: {e}")
            results.append((name, None, False))
    
    # Summary
    print("\n" + "="*80)
    print("EXECUTION SUMMARY")
    print("="*80)
    
    total_duration = 0
    success_count = 0
    
    for name, result, success in results:
        if success and result:
            status = "✅"
            duration = result['duration_seconds']
            total_duration += duration
            success_count += 1
            print(f"{status} {name} - {duration:.2f}s")
        else:
            status = "❌"
            print(f"{status} {name} - FAILED")
    
    print(f"\nTotal: {success_count}/{len(results)} successful")
    print(f"Total Duration: {total_duration:.2f}s")
    print(f"Average: {total_duration/len(results):.2f}s per site")
    print("="*80)
    
    # Verify last result
    if results[-1][2] and results[-1][1]:
        verify_output_structure(results[-1][1])
        inspect_generated_content(results[-1][1])
    
    return results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        demo_name = sys.argv[1].lower()
        
        demos_map = {
            "basic": demo_basic_site,
            "creative": demo_creative_agency,
            "luxury": demo_luxury_brand,
            "tech": demo_tech_startup,
            "all": run_all_demos
        }
        
        if demo_name in demos_map:
            result = demos_map[demo_name]()
            if result and isinstance(result, dict):
                verify_output_structure(result)
                inspect_generated_content(result)
        else:
            print(f"Unknown demo: {demo_name}")
            print(f"Available: {', '.join(demos_map.keys())}")
    else:
        # Run all demos by default
        run_all_demos()
