#!/usr/bin/env python3
"""
🔥 Codex Dominion - WooCommerce Test Script
Test the enhanced WooCommerce integration
"""

import json

from codex_woocommerce_sync import CodexWooCommerceSync, sync_products


def test_woocommerce_integration():
    """Test WooCommerce integration with sample data"""
    print("🔥 === CODEX DOMINION WOOCOMMERCE TEST ===")
    print("")

    # Initialize the sync client
    print("🔧 Initializing WooCommerce sync client...")
    sync_client = CodexWooCommerceSync()

    # Load sample products
    print("📦 Loading sample products...")
    try:
        with open("sample_products.json", "r") as f:
            sample_data = json.load(f)

        # Handle both array and object formats
        if isinstance(sample_data, dict) and "products" in sample_data:
            products = sample_data["products"][:3]  # Test with first 3 products
        else:
            products = sample_data[:3] if isinstance(sample_data, list) else []

        print(f"✅ Loaded {len(products)} sample products for testing")

    except FileNotFoundError:
        print("⚠️ Sample products file not found, creating test products...")
        products = [
            {
                "title": "Test Product - Digital Sovereignty Guide",
                "name": "Digital Sovereignty Guide",
                "price": 97.00,
                "regular_price": "97.00",
                "description": "A comprehensive guide to achieving digital sovereignty.",
                "short_description": "Your path to digital independence.",
                "type": "simple",
                "virtual": True,
                "downloadable": True,
                "sku": "TEST-DSG-001",
            }
        ]

    # Display configuration status
    print("")
    print("⚙️ Configuration Status:")
    if sync_client.consumer_key and sync_client.consumer_key != "YOUR_WC_KEY":
        print("✅ Consumer Key: Configured")
    else:
        print("❌ Consumer Key: Not configured (using placeholder)")

    if sync_client.consumer_secret and sync_client.consumer_secret != "YOUR_WC_SECRET":
        print("✅ Consumer Secret: Configured")
    else:
        print("❌ Consumer Secret: Not configured (using placeholder)")

    print(f"🏪 Store URL: {sync_client.store_url}")

    # Test connection
    print("")
    print("🔍 Testing WooCommerce connection...")
    connection_ok = sync_client.test_connection()

    if connection_ok:
        print("✅ Connection successful!")

        # Get categories
        print("")
        print("📁 Getting product categories...")
        categories = sync_client.get_categories()
        for i, cat in enumerate(categories[:5]):  # Show first 5 categories
            print(f"   {cat['id']}: {cat['name']}")
        if len(categories) > 5:
            print(f"   ... and {len(categories) - 5} more categories")

        # Get existing products count
        print("")
        print("📊 Getting existing products...")
        existing_products = sync_client.get_existing_products()
        print(f"📦 Found {len(existing_products)} existing products in store")

        # Test sync (dry run mode)
        print("")
        print("🧪 Testing product sync (DRY RUN)...")
        print("Products that would be created:")
        for i, product in enumerate(products, 1):
            name = product.get("title", product.get("name", "Unknown"))
            price = product.get("price", product.get("regular_price", "N/A"))
            print(f"   {i}. {name} - ${price}")

        # Ask if user wants to perform actual sync
        print("")
        perform_sync = input("🔥 Perform actual product sync? (y/n): ").lower().strip()

        if perform_sync == "y":
            print("")
            print("🚀 Starting actual product sync...")
            results = sync_client.sync_products(products)

            print("")
            print("📊 Sync Results:")
            print(f"✅ Successfully created: {results['success']} products")
            print(f"❌ Failed: {results['failed']} products")

            if results["created_products"]:
                print("")
                print("🎉 Created Products:")
                for product in results["created_products"]:
                    print(
                        f"   • {product['name']} (ID: {product['id']}) - ${product['price']}"
                    )
                    print(f"     URL: {product['url']}")

            if results["errors"]:
                print("")
                print("⚠️ Errors:")
                for error in results["errors"]:
                    print(f"   • {error}")
        else:
            print("ℹ️ Sync cancelled by user")

    else:
        print("")
        print("❌ Cannot proceed with sync due to connection issues")
        print("")
        print("💡 To fix this:")
        print("1. Update woocommerce_config.json with your actual API credentials")
        print("2. Or set environment variables WC_KEY and WC_SECRET")
        print("3. Ensure your WooCommerce store has REST API enabled")
        print("4. Check that your API keys have read/write permissions")

    print("")
    print("🔥 Test complete! Sacred flames burn eternal! ✨")


def show_configuration_help():
    """Show how to configure WooCommerce credentials"""
    print("🔧 === WOOCOMMERCE CONFIGURATION GUIDE ===")
    print("")
    print("To use the WooCommerce integration, you need API credentials:")
    print("")
    print("1. 🏪 Log into your WooCommerce admin dashboard")
    print("2. 🔧 Go to WooCommerce → Settings → Advanced → REST API")
    print("3. 🔑 Click 'Add Key' to create new API credentials")
    print("4. 📝 Set permissions to 'Read/Write'")
    print("5. 💾 Copy the Consumer Key and Consumer Secret")
    print("")
    print("Then update your credentials in one of these ways:")
    print("")
    print("Option 1: Update woocommerce_config.json")
    print('   "consumer_key": "ck_your_actual_key_here"')
    print('   "consumer_secret": "cs_your_actual_secret_here"')
    print("")
    print("Option 2: Set environment variables")
    print('   $env:WC_KEY = "ck_your_actual_key_here"')
    print('   $env:WC_SECRET = "cs_your_actual_secret_here"')
    print("")
    print("🔥 Once configured, run this test again!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        show_configuration_help()
    else:
        test_woocommerce_integration()
