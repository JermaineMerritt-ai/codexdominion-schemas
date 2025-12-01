"""
🔥 Codex Dominion - WooCommerce Integration
Enhanced WooCommerce API integration for The Merritt Method store
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import requests


class CodexWooCommerceSync:
    """Enhanced WooCommerce synchronization for Codex Dominion"""

    def __init__(
        self,
        store_url: str = None,
        consumer_key: str = None,
        consumer_secret: str = None,
    ):
        # Default to The Merritt Method store
        self.store_url = store_url or "https://store.themerrittmethod.com"
        self.api_url = f"{self.store_url}/wp-json/wc/v3"

        # Load credentials from config file or environment
        config = self.load_config()
        self.consumer_key = (
            consumer_key or config.get("consumer_key") or os.getenv("WC_KEY")
        )
        self.consumer_secret = (
            consumer_secret or config.get("consumer_secret") or os.getenv("WC_SECRET")
        )

        # Authentication
        self.auth = (
            (self.consumer_key, self.consumer_secret)
            if self.consumer_key and self.consumer_secret
            else None
        )

        # Session for connection pooling
        self.session = requests.Session()
        if self.auth:
            self.session.auth = self.auth

    def load_config(self) -> Dict:
        """Load WooCommerce configuration from file"""
        try:
            config_path = Path("woocommerce_config.json")
            if config_path.exists():
                with open(config_path, "r") as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Could not load config: {e}")
        return {}

    def save_config(self, config: Dict):
        """Save WooCommerce configuration to file"""
        try:
            with open("woocommerce_config.json", "w") as f:
                json.dump(config, f, indent=2)
            print("✅ Configuration saved")
        except Exception as e:
            print(f"❌ Could not save config: {e}")

    def test_connection(self) -> bool:
        """Test WooCommerce API connection"""
        if not self.auth:
            print("❌ No authentication credentials provided")
            return False

        try:
            response = self.session.get(f"{self.api_url}/system_status")
            if response.status_code == 200:
                print("✅ WooCommerce connection successful")
                return True
            else:
                print(f"❌ Connection failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

    def get_categories(self) -> List[Dict]:
        """Get all product categories"""
        try:
            response = self.session.get(f"{self.api_url}/products/categories")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"⚠️ Failed to get categories: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error getting categories: {e}")
            return []

    def create_product(self, product_data: Dict) -> Optional[Dict]:
        """Create a single product"""
        try:
            # Validate required fields
            required_fields = ["name", "type", "regular_price"]
            for field in required_fields:
                if field not in product_data:
                    print(f"❌ Missing required field: {field}")
                    return None

            response = self.session.post(f"{self.api_url}/products", json=product_data)

            if response.status_code == 201:
                product = response.json()
                print(
                    f"✅ Created product: {product_data['name']} (ID: {product['id']})"
                )
                return product
            else:
                print(
                    f"❌ Failed to create product {product_data['name']}: {response.status_code} - {response.text}"
                )
                return None

        except Exception as e:
            print(
                f"❌ Error creating product {product_data.get('name', 'Unknown')}: {e}"
            )
            return None

    def sync_products(self, products: List[Dict]) -> Dict:
        """Enhanced product synchronization with detailed reporting"""
        if not self.auth:
            print("❌ Cannot sync: No authentication credentials")
            return {"success": 0, "failed": 0, "errors": ["No authentication"]}

        print(
            f"🚀 Starting sync of {len(products)} products to The Merritt Method store..."
        )

        results = {
            "success": 0,
            "failed": 0,
            "errors": [],
            "created_products": [],
            "sync_time": datetime.now().isoformat(),
        }

        for i, product in enumerate(products, 1):
            print(
                f"📦 Syncing product {i}/{len(products)}: {product.get('title', product.get('name', 'Unknown'))}"
            )

            # Transform product data to WooCommerce format
            wc_product = self.transform_product_data(product)

            # Create the product
            created_product = self.create_product(wc_product)

            if created_product:
                results["success"] += 1
                results["created_products"].append(
                    {
                        "id": created_product["id"],
                        "name": created_product["name"],
                        "price": created_product["regular_price"],
                        "url": created_product["permalink"],
                    }
                )
            else:
                results["failed"] += 1
                results["errors"].append(
                    f"Failed to create {product.get('title', product.get('name', 'Unknown'))}"
                )

        # Save sync results
        self.save_sync_results(results)

        print(
            f"📊 Sync complete: {results['success']} successful, {results['failed']} failed"
        )
        return results

    def transform_product_data(self, product: Dict) -> Dict:
        """Transform product data to WooCommerce format"""
        return {
            "name": product.get("title", product.get("name", "")),
            "type": product.get("type", "simple"),
            "regular_price": str(
                product.get("price", product.get("regular_price", "0"))
            ),
            "description": product.get("description", ""),
            "short_description": product.get("short_description", ""),
            "categories": (
                [{"id": product["category_id"]}] if product.get("category_id") else []
            ),
            "images": [{"src": img} for img in product.get("images", [])],
            "sku": product.get("sku", ""),
            "manage_stock": product.get("manage_stock", False),
            "stock_quantity": product.get("stock_quantity"),
            "status": product.get("status", "publish"),
            "featured": product.get("featured", False),
            "virtual": product.get("virtual", False),
            "downloadable": product.get("downloadable", False),
            "weight": product.get("weight", ""),
            "dimensions": {
                "length": product.get("length", ""),
                "width": product.get("width", ""),
                "height": product.get("height", ""),
            },
        }

    def save_sync_results(self, results: Dict):
        """Save synchronization results to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"wc_sync_results_{timestamp}.json"

            with open(filename, "w") as f:
                json.dump(results, f, indent=2)

            print(f"📄 Sync results saved to: {filename}")
        except Exception as e:
            print(f"⚠️ Could not save sync results: {e}")

    def get_existing_products(self) -> List[Dict]:
        """Get all existing products from WooCommerce"""
        try:
            products = []
            page = 1
            per_page = 100

            while True:
                response = self.session.get(
                    f"{self.api_url}/products",
                    params={"page": page, "per_page": per_page},
                )

                if response.status_code == 200:
                    batch = response.json()
                    if not batch:
                        break
                    products.extend(batch)
                    page += 1
                else:
                    print(f"⚠️ Failed to get products: {response.status_code}")
                    break

            print(f"📦 Found {len(products)} existing products")
            return products

        except Exception as e:
            print(f"❌ Error getting products: {e}")
            return []

    def update_product(self, product_id: int, product_data: Dict) -> Optional[Dict]:
        """Update an existing product"""
        try:
            response = self.session.put(
                f"{self.api_url}/products/{product_id}", json=product_data
            )

            if response.status_code == 200:
                product = response.json()
                print(f"✅ Updated product: {product['name']} (ID: {product['id']})")
                return product
            else:
                print(
                    f"❌ Failed to update product {product_id}: {response.status_code}"
                )
                return None

        except Exception as e:
            print(f"❌ Error updating product {product_id}: {e}")
            return None

    def delete_product(self, product_id: int) -> bool:
        """Delete a product"""
        try:
            response = self.session.delete(f"{self.api_url}/products/{product_id}")

            if response.status_code == 200:
                print(f"✅ Deleted product ID: {product_id}")
                return True
            else:
                print(
                    f"❌ Failed to delete product {product_id}: {response.status_code}"
                )
                return False

        except Exception as e:
            print(f"❌ Error deleting product {product_id}: {e}")
            return False


# Convenience functions for quick usage
WC_URL = "https://store.themerrittmethod.com/wp-json/wc/v3/products"
WC_KEY = "YOUR_WC_KEY"  # Replace with actual key
WC_SECRET = "YOUR_WC_SECRET"  # Replace with actual secret


def sync_products(products: List[Dict], wc_key: str = None, wc_secret: str = None):
    """Simple sync function for backward compatibility"""
    sync_client = CodexWooCommerceSync(
        consumer_key=wc_key or WC_KEY, consumer_secret=wc_secret or WC_SECRET
    )

    return sync_client.sync_products(products)


# Example usage and sample products
def create_sample_products():
    """Create sample products for The Merritt Method"""
    return [
        {
            "title": "Digital Sovereignty Mastery Course",
            "price": 297.00,
            "description": "Complete course on achieving digital independence and sovereignty.",
            "short_description": "Master digital sovereignty with this comprehensive course.",
            "category_id": 1,  # Update with actual category ID
            "type": "simple",
            "virtual": True,
            "downloadable": True,
            "featured": True,
        },
        {
            "title": "Codex Dominion Consultation",
            "price": 197.00,
            "description": "One-on-one consultation for implementing your digital sovereignty strategy.",
            "short_description": "Personalized guidance for your digital transformation.",
            "category_id": 2,
            "type": "simple",
            "virtual": True,
        },
        {
            "title": "The Merritt Method Blueprint",
            "price": 97.00,
            "description": "Step-by-step blueprint for digital transformation and sovereignty.",
            "short_description": "Your roadmap to digital independence.",
            "category_id": 1,
            "type": "simple",
            "virtual": True,
            "downloadable": True,
        },
    ]


if __name__ == "__main__":
    # Test the WooCommerce integration
    print("🔥 Codex Dominion WooCommerce Integration Test")

    # Initialize sync client
    sync_client = CodexWooCommerceSync()

    # Test connection
    if sync_client.test_connection():
        # Get categories
        categories = sync_client.get_categories()
        print(f"📁 Available categories: {len(categories)}")

        # Create sample products
        sample_products = create_sample_products()

        # Sync products
        results = sync_client.sync_products(sample_products)
        print(f"📊 Final results: {results}")
    else:
        print("❌ Cannot proceed without valid connection")
        print(
            "💡 Please update WC_KEY and WC_SECRET with your actual WooCommerce API credentials"
        )
