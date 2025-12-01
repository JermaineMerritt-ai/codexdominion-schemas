#!/usr/bin/env python3
"""
🛒 Simple WooCommerce Product Sync Example
Basic usage of the WooCommerce sync functionality
"""

import json

from woocommerce_sync import WooCommerceSync


def simple_sync_example():
    """Simple example matching your original code structure"""

    # Your WooCommerce API credentials
    WC_KEY = "ck_your_consumer_key_here"  # Replace with your actual key
    WC_SECRET = "cs_your_consumer_secret_here"  # Replace with your actual secret

    # Initialize the WooCommerce client
    try:
        wc = WooCommerceSync(consumer_key=WC_KEY, consumer_secret=WC_SECRET)
        print("✅ WooCommerce client initialized")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please set your WC_KEY and WC_SECRET in this script")
        return

    # Example product data (matching your structure)
    products_json = [
        {
            "name": "Test Product 1",
            "regular_price": "29.99",
            "description": "This is a test product",
            "sku": "TEST-001",
        },
        {
            "name": "Test Product 2",
            "regular_price": "49.99",
            "description": "This is another test product",
            "sku": "TEST-002",
        },
    ]

    # Original function structure (enhanced)
    def wc_request(endpoint, method="GET", data=None):
        """Your original function with better error handling"""
        return wc.wc_request(endpoint, method, data)

    def sync_products(products_json):
        """Your original function with enhanced functionality"""
        print(f"🛒 Syncing {len(products_json)} products...")

        for i, product in enumerate(products_json):
            try:
                print(f"📦 Creating product {i+1}: {product['name']}")
                result = wc_request("products", method="POST", data=product)
                print(f"✅ Created product ID: {result['id']}")

            except Exception as e:
                print(f"❌ Failed to create {product['name']}: {str(e)}")

    # Test individual API calls
    print("\n🧪 Testing API Connection...")
    try:
        # Test getting existing products
        products = wc_request("products?per_page=5")
        print(f"✅ Successfully retrieved {len(products)} products")

        # Test creating products
        print("\n📦 Creating test products...")
        sync_products(products_json)

    except Exception as e:
        print(f"❌ API test failed: {str(e)}")


def load_and_sync_from_file():
    """Load products from file and sync"""

    WC_KEY = "ck_your_consumer_key_here"  # Replace with your actual key
    WC_SECRET = "cs_your_consumer_secret_here"  # Replace with your actual secret

    try:
        wc = WooCommerceSync(consumer_key=WC_KEY, consumer_secret=WC_SECRET)

        # Load products from JSON file
        with open("sample_products.json", "r", encoding="utf-8") as f:
            products_json = json.load(f)

        print(f"📁 Loaded {len(products_json)} products from file")

        # Sync products with advanced features
        results = wc.sync_products(products_json)

        print("\n📊 Sync Results:")
        print(f"✅ Successful: {len(results['success'])}")
        print(f"❌ Errors: {len(results['errors'])}")
        print(f"⏱️  Duration: {results['duration_seconds']:.2f} seconds")

        # Show any errors
        if results["errors"]:
            print("\n❌ Errors encountered:")
            for error in results["errors"][:3]:  # Show first 3 errors
                print(f"   • {error['product_name']}: {error['error']}")

    except Exception as e:
        print(f"❌ File sync failed: {str(e)}")


if __name__ == "__main__":
    print("🛒 WooCommerce Sync Examples")
    print("=" * 40)

    print("\n1. Simple sync example:")
    simple_sync_example()

    print("\n" + "=" * 40)
    print("2. File-based sync example:")
    load_and_sync_from_file()

    print("\n🏁 Examples complete!")
    print("\nTo use this script:")
    print(
        "1. Replace WC_KEY and WC_SECRET with your actual WooCommerce API credentials"
    )
    print("2. Modify the products_json data as needed")
    print("3. Run the script to sync your products")
