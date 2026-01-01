"""
AUTOMATIC COUNCIL ROUTING DEMONSTRATION
=========================================
Shows how the domain field drives intelligent workflow routing
"""

from workflow_types.website_creation import WORKFLOW_TYPE_WEBSITE_CREATION
from workflow_types.ecommerce_website_creation import WORKFLOW_TYPE_ECOMMERCE_WEBSITE

print('=' * 70)
print('AUTOMATIC COUNCIL ROUTING COMPARISON')
print('=' * 70)
print()

# Basic website
print('1️⃣  BASIC WEBSITE')
print('   ' + '-' * 60)
print(f'   ID: {WORKFLOW_TYPE_WEBSITE_CREATION["id"]}')
print(f'   Domain: {WORKFLOW_TYPE_WEBSITE_CREATION["domain"]}')
print(f'   Routes to: MEDIA COUNCIL 📰')
print(f'   Risk flags: {len(WORKFLOW_TYPE_WEBSITE_CREATION["governance"]["risk_flags"])} items')
print(f'   Review criteria: {len(WORKFLOW_TYPE_WEBSITE_CREATION["governance"]["review_criteria"])} items')
print(f'   Annual savings: ${WORKFLOW_TYPE_WEBSITE_CREATION["calculated_savings"]["annual_savings"]:,.2f}')
print()

# E-commerce website
print('2️⃣  E-COMMERCE WEBSITE')
print('   ' + '-' * 60)
print(f'   ID: {WORKFLOW_TYPE_ECOMMERCE_WEBSITE["id"]}')
print(f'   Domain: {WORKFLOW_TYPE_ECOMMERCE_WEBSITE["domain"]}')
print(f'   Routes to: COMMERCE COUNCIL 💰')
print(f'   Risk flags: {len(WORKFLOW_TYPE_ECOMMERCE_WEBSITE["governance"]["risk_flags"])} items')
print(f'   Review criteria: {len(WORKFLOW_TYPE_ECOMMERCE_WEBSITE["governance"]["review_criteria"])} items')
print(f'   Annual savings: ${WORKFLOW_TYPE_ECOMMERCE_WEBSITE["calculated_savings"]["annual_savings"]:,.2f}')
print()

print('=' * 70)
print('KEY DIFFERENCES')
print('=' * 70)
print()
print('🎯 Routing:')
print('   Basic site → domain: "media" → Media Council')
print('   E-commerce → domain: "commerce" → Commerce Council')
print()
print('⚠️  Risk Flags:')
print('   Basic: public_facing, brand_sensitive, youth_sensitive')
print('   E-commerce: handles_payments, stores_customer_data, high_value_transactions')
print()
print('✅ Review Criteria:')
print('   Basic: Brand, SEO, Accessibility, Content, Navigation')
print('   E-commerce: PCI compliance, GDPR, Transaction accuracy, Refunds, Cart optimization')
print()
print('💰 Value:')
print('   Basic: $11,700/year (3 hours/week saved)')
print('   E-commerce: $58,500/year (15 hours/week saved)')
print()
print('🔥 The domain field = automatic intelligent routing!')
print()

# Show how routing engine works
print('=' * 70)
print('HOW ROUTING ENGINE WORKS')
print('=' * 70)
print()

from council_routing_engine import determine_required_councils

# Example 1: Basic site with blog
basic_inputs = {
    "site_name": "Tech Blog",
    "description": "Latest tech news and articles",
    "pages": ["home", "blog", "about"]
}
councils = determine_required_councils("website.create_basic_site", basic_inputs)
print(f'Example 1: Tech Blog')
print(f'   Inputs: blog, articles, news')
print(f'   Routes to: {[c.value for c in councils]}')
print()

# Example 2: E-commerce store
ecom_inputs = {
    "site_name": "Premium Store",
    "description": "Buy premium templates and products",
    "pages": ["shop", "cart", "checkout"],
    "payment_methods": ["stripe", "paypal"]
}
councils = determine_required_councils("website.create_ecommerce_site", ecom_inputs)
print(f'Example 2: E-commerce Store')
print(f'   Inputs: shop, buy, cart, checkout, payment')
print(f'   Routes to: {[c.value for c in councils]}')
print()

# Example 3: Youth education site
youth_inputs = {
    "site_name": "Kids Learning Portal",
    "description": "Educational content for children and students",
    "target_audience": "youth",
    "pages": ["home", "lessons", "games"]
}
councils = determine_required_councils("website.create_basic_site", youth_inputs)
print(f'Example 3: Youth Education Site')
print(f'   Inputs: kids, children, students, education')
print(f'   Routes to: {[c.value for c in councils]}')
print()

print('✅ Content analysis + keyword detection = smart routing!')
