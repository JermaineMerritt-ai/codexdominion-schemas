#!/usr/bin/env python3
"""
🛒 WooCommerce Product Sync for The Merritt Method
Synchronizes products with store.themerrittmethod.com via WooCommerce API
"""

import requests
import json
import datetime
import time
from typing import Dict, List, Optional

# WooCommerce API Configuration
WC_BASE_URL = "https://store.themerrittmethod.com/wp-json/wc/v3"
WC_KEY = ""  # Set your WooCommerce Consumer Key
WC_SECRET = ""  # Set your WooCommerce Consumer Secret

class WooCommerceSync:
    def __init__(self, consumer_key: str = None, consumer_secret: str = None):
        """Initialize WooCommerce API client"""
        self.consumer_key = consumer_key or WC_KEY
        self.consumer_secret = consumer_secret or WC_SECRET
        self.base_url = WC_BASE_URL
        
        if not self.consumer_key or not self.consumer_secret:
            raise ValueError("WooCommerce API credentials not provided")
    
    def wc_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
        """Make authenticated request to WooCommerce API"""
        url = f"{self.base_url}/{endpoint}"
        auth = (self.consumer_key, self.consumer_secret)
        
        try:
            response = requests.request(
                method=method,
                url=url,
                auth=auth,
                json=data,
                timeout=30,
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'MerrittMethod-Sync/1.0'
                }
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            raise Exception(f"Request timeout for {endpoint}")
        except requests.exceptions.ConnectionError:
            raise Exception(f"Connection error for {endpoint}")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
    
    def get_products(self, per_page: int = 100, page: int = 1) -> List[Dict]:
        """Retrieve products from WooCommerce store"""
        endpoint = f"products?per_page={per_page}&page={page}"
        return self.wc_request(endpoint)
    
    def get_product(self, product_id: int) -> Dict:
        """Get specific product by ID"""
        return self.wc_request(f"products/{product_id}")
    
    def create_product(self, product_data: Dict) -> Dict:
        """Create new product"""
        return self.wc_request("products", method="POST", data=product_data)
    
    def update_product(self, product_id: int, product_data: Dict) -> Dict:
        """Update existing product"""
        return self.wc_request(f"products/{product_id}", method="PUT", data=product_data)
    
    def delete_product(self, product_id: int, force: bool = True) -> Dict:
        """Delete product"""
        endpoint = f"products/{product_id}?force={'true' if force else 'false'}"
        return self.wc_request(endpoint, method="DELETE")
    
    def sync_products(self, products_json: List[Dict], batch_size: int = 10) -> Dict:
        """
        Sync multiple products with rate limiting and error handling
        
        Args:
            products_json: List of product dictionaries
            batch_size: Number of products to process in each batch
            
        Returns:
            Dict with sync results
        """
        results = {
            "success": [],
            "errors": [],
            "skipped": [],
            "total_processed": 0,
            "start_time": datetime.datetime.now().isoformat()
        }
        
        print(f"🛒 Starting WooCommerce sync for {len(products_json)} products")
        
        for i, product in enumerate(products_json):
            try:
                # Rate limiting - pause between requests
                if i > 0 and i % batch_size == 0:
                    print(f"📦 Processed {i} products, pausing for rate limit...")
                    time.sleep(2)
                
                # Validate required fields
                if not product.get('name'):
                    results["errors"].append({
                        "index": i,
                        "error": "Product name is required",
                        "product": product
                    })
                    continue
                
                # Check if product exists (by SKU if provided)
                existing_product = None
                if product.get('sku'):
                    try:
                        existing_products = self.wc_request(f"products?sku={product['sku']}")
                        if existing_products:
                            existing_product = existing_products[0]
                    except Exception as e:
                        print(f"⚠️  Could not check for existing product: {str(e)}")
                
                # Create or update product
                if existing_product:
                    print(f"🔄 Updating existing product: {product['name']}")
                    result = self.update_product(existing_product['id'], product)
                    results["success"].append({
                        "action": "updated",
                        "product_id": existing_product['id'],
                        "name": product['name'],
                        "result": result
                    })
                else:
                    print(f"➕ Creating new product: {product['name']}")
                    result = self.create_product(product)
                    results["success"].append({
                        "action": "created",
                        "product_id": result['id'],
                        "name": product['name'],
                        "result": result
                    })
                
                results["total_processed"] += 1
                
            except Exception as e:
                error_info = {
                    "index": i,
                    "error": str(e),
                    "product_name": product.get('name', 'Unknown'),
                    "product": product
                }
                results["errors"].append(error_info)
                print(f"❌ Error syncing product {product.get('name', 'Unknown')}: {str(e)}")
        
        results["end_time"] = datetime.datetime.now().isoformat()
        results["duration_seconds"] = (
            datetime.datetime.fromisoformat(results["end_time"]) - 
            datetime.datetime.fromisoformat(results["start_time"])
        ).total_seconds()
        
        return results
    
    def validate_product_data(self, product: Dict) -> Dict:
        """Validate and clean product data before sync"""
        validated = product.copy()
        
        # Required fields validation
        if not validated.get('name'):
            raise ValueError("Product name is required")
        
        # Set default values
        validated.setdefault('type', 'simple')
        validated.setdefault('status', 'publish')
        validated.setdefault('catalog_visibility', 'visible')
        
        # Price validation
        if 'regular_price' in validated:
            validated['regular_price'] = str(validated['regular_price'])
        if 'sale_price' in validated:
            validated['sale_price'] = str(validated['sale_price'])
        
        # Categories format
        if 'categories' in validated and isinstance(validated['categories'], list):
            validated['categories'] = [
                {'id': cat} if isinstance(cat, int) else cat 
                for cat in validated['categories']
            ]
        
        return validated

def load_products_from_file(filepath: str) -> List[Dict]:
    """Load products from JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise Exception(f"Products file not found: {filepath}")
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON in products file: {str(e)}")

def save_sync_results(results: Dict, filepath: str = None):
    """Save sync results to file"""
    if not filepath:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"woocommerce_sync_results_{timestamp}.json"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Sync results saved to: {filepath}")

def main():
    """Main sync function"""
    # Example usage
    try:
        # Initialize WooCommerce client
        wc = WooCommerceSync()
        
        # Example product data
        sample_products = [
            {
                "name": "The Merritt Method Course",
                "type": "simple",
                "regular_price": "297.00",
                "description": "Complete digital transformation course",
                "short_description": "Master the Merritt Method",
                "categories": [{"id": 15}],
                "images": [
                    {
                        "src": "https://store.themerrittmethod.com/wp-content/uploads/course-image.jpg"
                    }
                ],
                "sku": "MERRITT-001",
                "manage_stock": True,
                "stock_quantity": 100,
                "status": "publish"
            }
        ]
        
        # Load products from file (if exists)
        try:
            products = load_products_from_file("products.json")
            print(f"📦 Loaded {len(products)} products from file")
        except Exception:
            products = sample_products
            print("📦 Using sample products")
        
        # Validate products
        validated_products = []
        for product in products:
            try:
                validated = wc.validate_product_data(product)
                validated_products.append(validated)
            except Exception as e:
                print(f"⚠️  Skipping invalid product: {str(e)}")
        
        # Sync products
        if validated_products:
            results = wc.sync_products(validated_products)
            
            # Print summary
            print(f"\n🏁 Sync Complete!")
            print(f"✅ Success: {len(results['success'])}")
            print(f"❌ Errors: {len(results['errors'])}")
            print(f"⏱️  Duration: {results['duration_seconds']:.2f} seconds")
            
            # Save results
            save_sync_results(results)
        else:
            print("❌ No valid products to sync")
    
    except Exception as e:
        print(f"❌ Sync failed: {str(e)}")

if __name__ == "__main__":
    main()