"""
Quick test for Steps 6-10 implementation
"""

from website_creation_steps_6_to_10 import generate_nextjs_project
from website_creation_execution_complete import (
    generate_site_blueprint,
    generate_page_content,
    generate_seo_metadata,
    generate_brand_theme
)
from pathlib import Path

print("\n🔥 Testing Website Creation Steps 6-10 🔥\n")

# Generate JSON artifacts (Steps 1-5)
print("Step 1-5: Generating JSON artifacts...")
blueprint = generate_site_blueprint("Demo Site", "Testing Steps 6-10", ["home", "about"], "nextjs")
content = generate_page_content(blueprint, "Demo Site", "Testing", "professional")
seo = generate_seo_metadata(blueprint, content, "Demo Site", "Testing")
theme = generate_brand_theme(
    {"primary": "#1a1a1a", "secondary": "#f7f1e3", "accent": "#d4af37"},
    {"heading": "Inter", "body": "Open Sans"}
)
print("✅ JSON artifacts generated\n")

# Step 6: Generate Next.js project
print("Step 6: Generating Next.js project...")
result = generate_nextjs_project(
    blueprint, content, theme, seo, "Demo Site",
    Path("./test_nextjs_output")
)
print(f"✅ Next.js project generated at: {result['project_dir']}\n")

# Verify files exist
project_dir = Path(result['project_dir'])
files_to_check = [
    "package.json",
    "tsconfig.json",
    "next.config.js",
    "tailwind.config.js",
    "app/layout.tsx",
    "app/page.tsx",
    "components/Header.tsx",
    "components/Footer.tsx",
    "README.md"
]

print("Verifying generated files:")
all_exist = True
for file_path in files_to_check:
    full_path = project_dir / file_path
    exists = full_path.exists()
    status = "✅" if exists else "❌"
    print(f"  {status} {file_path}")
    if not exists:
        all_exist = False

if all_exist:
    print("\n🎉 All files generated successfully!")
    print(f"\n📁 Project location: {project_dir}")
    print("\n💡 Next steps:")
    print(f"  cd {project_dir}")
    print("  npm install")
    print("  npm run dev")
else:
    print("\n⚠️  Some files missing")
