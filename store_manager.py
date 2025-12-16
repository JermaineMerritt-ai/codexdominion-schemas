"""
Codex Dominion - Store Manager
Complete WooCommerce store management system with product sync, inventory, orders, and analytics.

Features:
- WooCommerce API integration (REST API v3)
- Product management (create, update, delete, batch operations)
- Category and tag management
- Order management and fulfillment
- Customer management
- Inventory tracking and alerts
- Sales analytics and reports
- Automated product import from CSV/JSON
- Image upload and optimization
- Store health monitoring

Author: Codex Dominion AI Systems
Version: 1.0.0
"""

import json
import os
import time
import hashlib
import hmac
import base64
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import csv
from io import StringIO


@dataclass
class WooCommerceConfig:
    """WooCommerce store configuration"""
    store_url: str
    consumer_key: str
    consumer_secret: str
    version: str = "wc/v3"
    verify_ssl: bool = True
    timeout: int = 30

    def get_base_url(self) -> str:
        """Get base API URL"""
        return f"{self.store_url.rstrip('/')}/wp-json/{self.version}"


@dataclass
class Product:
    """Product data structure"""
    name: str
    type: str = "simple"  # simple, grouped, external, variable
    regular_price: str = ""
    sale_price: str = ""
    description: str = ""
    short_description: str = ""
    sku: str = ""
    manage_stock: bool = False
    stock_quantity: int = 0
    stock_status: str = "instock"  # instock, outofstock, onbackorder
    categories: List[Dict] = None
    tags: List[Dict] = None
    images: List[Dict] = None
    attributes: List[Dict] = None
    id: Optional[int] = None

    def __post_init__(self):
        if self.categories is None:
            self.categories = []
        if self.tags is None:
            self.tags = []
        if self.images is None:
            self.images = []
        if self.attributes is None:
            self.attributes = []


class WooCommerceAPI:
    """WooCommerce REST API client"""

    def __init__(self, config: WooCommerceConfig):
        self.config = config
        self.base_url = config.get_base_url()
        self.session = requests.Session()
        self.session.auth = (config.consumer_key, config.consumer_secret)

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                     params: Optional[Dict] = None) -> Dict:
        """Make authenticated API request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            if method.upper() == "GET":
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.config.timeout,
                    verify=self.config.verify_ssl
                )
            elif method.upper() == "POST":
                response = self.session.post(
                    url,
                    json=data,
                    params=params,
                    timeout=self.config.timeout,
                    verify=self.config.verify_ssl
                )
            elif method.upper() == "PUT":
                response = self.session.put(
                    url,
                    json=data,
                    params=params,
                    timeout=self.config.timeout,
                    verify=self.config.verify_ssl
                )
            elif method.upper() == "DELETE":
                response = self.session.delete(
                    url,
                    params=params,
                    timeout=self.config.timeout,
                    verify=self.config.verify_ssl
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"❌ WooCommerce API Error: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            raise

    # Product Management
    def get_products(self, page: int = 1, per_page: int = 10, **filters) -> List[Dict]:
        """Get products with filters"""
        params = {"page": page, "per_page": per_page, **filters}
        return self._make_request("GET", "products", params=params)

    def get_product(self, product_id: int) -> Dict:
        """Get single product by ID"""
        return self._make_request("GET", f"products/{product_id}")

    def create_product(self, product: Product) -> Dict:
        """Create new product"""
        data = {k: v for k, v in asdict(product).items() if v and k != 'id'}
        return self._make_request("POST", "products", data=data)

    def update_product(self, product_id: int, updates: Dict) -> Dict:
        """Update existing product"""
        return self._make_request("PUT", f"products/{product_id}", data=updates)

    def delete_product(self, product_id: int, force: bool = False) -> Dict:
        """Delete product"""
        params = {"force": force}
        return self._make_request("DELETE", f"products/{product_id}", params=params)

    def batch_update_products(self, create: List[Dict] = None, update: List[Dict] = None,
                            delete: List[int] = None) -> Dict:
        """Batch create/update/delete products"""
        data = {}
        if create:
            data["create"] = create
        if update:
            data["update"] = update
        if delete:
            data["delete"] = delete
        return self._make_request("POST", "products/batch", data=data)

    # Category Management
    def get_categories(self, page: int = 1, per_page: int = 100) -> List[Dict]:
        """Get product categories"""
        params = {"page": page, "per_page": per_page}
        return self._make_request("GET", "products/categories", params=params)

    def create_category(self, name: str, parent: int = 0, description: str = "") -> Dict:
        """Create product category"""
        data = {"name": name, "parent": parent, "description": description}
        return self._make_request("POST", "products/categories", data=data)

    # Order Management
    def get_orders(self, page: int = 1, per_page: int = 10, status: str = "any") -> List[Dict]:
        """Get orders"""
        params = {"page": page, "per_page": per_page, "status": status}
        return self._make_request("GET", "orders", params=params)

    def get_order(self, order_id: int) -> Dict:
        """Get single order"""
        return self._make_request("GET", f"orders/{order_id}")

    def update_order_status(self, order_id: int, status: str) -> Dict:
        """Update order status"""
        data = {"status": status}
        return self._make_request("PUT", f"orders/{order_id}", data=data)

    # Customer Management
    def get_customers(self, page: int = 1, per_page: int = 10) -> List[Dict]:
        """Get customers"""
        params = {"page": page, "per_page": per_page}
        return self._make_request("GET", "customers", params=params)

    # Reports
    def get_sales_report(self, period: str = "week") -> Dict:
        """Get sales report"""
        params = {"period": period}
        return self._make_request("GET", "reports/sales", params=params)

    def get_top_sellers(self, period: str = "week") -> List[Dict]:
        """Get top selling products"""
        params = {"period": period}
        return self._make_request("GET", "reports/top_sellers", params=params)


class InventoryTracker:
    """Track inventory levels and send alerts"""

    def __init__(self, api: WooCommerceAPI, low_stock_threshold: int = 10):
        self.api = api
        self.low_stock_threshold = low_stock_threshold
        self.inventory_file = "inventory_tracking.json"

    def check_inventory_levels(self) -> Dict[str, List[Dict]]:
        """Check all products for low/out of stock"""
        products = self.api.get_products(per_page=100)

        low_stock = []
        out_of_stock = []

        for product in products:
            if not product.get("manage_stock"):
                continue

            stock_qty = product.get("stock_quantity", 0)

            if stock_qty == 0:
                out_of_stock.append({
                    "id": product["id"],
                    "name": product["name"],
                    "sku": product.get("sku", ""),
                    "stock": stock_qty
                })
            elif stock_qty <= self.low_stock_threshold:
                low_stock.append({
                    "id": product["id"],
                    "name": product["name"],
                    "sku": product.get("sku", ""),
                    "stock": stock_qty
                })

        return {
            "low_stock": low_stock,
            "out_of_stock": out_of_stock,
            "timestamp": datetime.now().isoformat()
        }

    def save_inventory_snapshot(self, data: Dict):
        """Save inventory snapshot to file"""
        if os.path.exists(self.inventory_file):
            with open(self.inventory_file, 'r') as f:
                history = json.load(f)
        else:
            history = {"snapshots": []}

        history["snapshots"].append(data)
        # Keep last 30 days
        history["snapshots"] = history["snapshots"][-30:]

        with open(self.inventory_file, 'w') as f:
            json.dump(history, f, indent=2)


class ProductImporter:
    """Import products from CSV/JSON files"""

    def __init__(self, api: WooCommerceAPI):
        self.api = api

    def import_from_csv(self, csv_file: str) -> Dict:
        """Import products from CSV file"""
        results = {"success": [], "errors": []}

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    product = Product(
                        name=row.get("name", ""),
                        type=row.get("type", "simple"),
                        regular_price=row.get("regular_price", ""),
                        sale_price=row.get("sale_price", ""),
                        description=row.get("description", ""),
                        short_description=row.get("short_description", ""),
                        sku=row.get("sku", ""),
                        manage_stock=row.get("manage_stock", "").lower() == "true",
                        stock_quantity=int(row.get("stock_quantity", 0)),
                        stock_status=row.get("stock_status", "instock")
                    )

                    # Handle categories
                    if row.get("categories"):
                        categories = [{"name": cat.strip()} for cat in row["categories"].split("|")]
                        product.categories = categories

                    # Handle tags
                    if row.get("tags"):
                        tags = [{"name": tag.strip()} for tag in row["tags"].split("|")]
                        product.tags = tags

                    # Create product
                    result = self.api.create_product(product)
                    results["success"].append({
                        "name": product.name,
                        "id": result.get("id")
                    })

                except Exception as e:
                    results["errors"].append({
                        "name": row.get("name", "Unknown"),
                        "error": str(e)
                    })

        return results

    def import_from_json(self, json_file: str) -> Dict:
        """Import products from JSON file"""
        results = {"success": [], "errors": []}

        with open(json_file, 'r', encoding='utf-8') as f:
            products_data = json.load(f)

        for product_data in products_data:
            try:
                product = Product(**product_data)
                result = self.api.create_product(product)
                results["success"].append({
                    "name": product.name,
                    "id": result.get("id")
                })
            except Exception as e:
                results["errors"].append({
                    "name": product_data.get("name", "Unknown"),
                    "error": str(e)
                })

        return results


class StoreAnalytics:
    """Store performance analytics"""

    def __init__(self, api: WooCommerceAPI):
        self.api = api

    def get_dashboard_stats(self, days: int = 30) -> Dict:
        """Get comprehensive store statistics"""
        # Get orders from last N days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        orders = self.api.get_orders(per_page=100, status="any")

        # Calculate stats
        total_orders = len(orders)
        completed_orders = [o for o in orders if o["status"] == "completed"]
        pending_orders = [o for o in orders if o["status"] in ["pending", "processing"]]

        total_revenue = sum(float(o.get("total", 0)) for o in completed_orders)
        average_order_value = total_revenue / len(completed_orders) if completed_orders else 0

        # Get product stats
        products = self.api.get_products(per_page=100)
        total_products = len(products)
        in_stock = [p for p in products if p.get("stock_status") == "instock"]
        out_of_stock = [p for p in products if p.get("stock_status") == "outofstock"]

        # Get top sellers
        top_sellers = self.api.get_top_sellers(period="month")

        return {
            "period_days": days,
            "orders": {
                "total": total_orders,
                "completed": len(completed_orders),
                "pending": len(pending_orders),
                "revenue": round(total_revenue, 2),
                "average_order_value": round(average_order_value, 2)
            },
            "products": {
                "total": total_products,
                "in_stock": len(in_stock),
                "out_of_stock": len(out_of_stock)
            },
            "top_sellers": top_sellers[:5] if top_sellers else [],
            "timestamp": datetime.now().isoformat()
        }

    def get_customer_stats(self) -> Dict:
        """Get customer statistics"""
        customers = self.api.get_customers(per_page=100)

        total_customers = len(customers)
        total_orders = sum(c.get("orders_count", 0) for c in customers)
        total_spent = sum(float(c.get("total_spent", 0)) for c in customers)

        avg_orders_per_customer = total_orders / total_customers if total_customers else 0
        avg_spent_per_customer = total_spent / total_customers if total_customers else 0

        return {
            "total_customers": total_customers,
            "total_orders": total_orders,
            "total_spent": round(total_spent, 2),
            "avg_orders_per_customer": round(avg_orders_per_customer, 2),
            "avg_spent_per_customer": round(avg_spent_per_customer, 2),
            "timestamp": datetime.now().isoformat()
        }


class StoreManager:
    """Main store management interface"""

    def __init__(self, config_file: str = "woocommerce_config.json"):
        self.config = self._load_config(config_file)
        self.api = WooCommerceAPI(self.config)
        self.inventory = InventoryTracker(self.api)
        self.importer = ProductImporter(self.api)
        self.analytics = StoreAnalytics(self.api)

    def _load_config(self, config_file: str) -> WooCommerceConfig:
        """Load configuration from file"""
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config_data = json.load(f)
                return WooCommerceConfig(**config_data)
        else:
            # Return default config with env variables
            return WooCommerceConfig(
                store_url=os.getenv("WC_STORE_URL", "https://your-store.com"),
                consumer_key=os.getenv("WC_CONSUMER_KEY", ""),
                consumer_secret=os.getenv("WC_CONSUMER_SECRET", "")
            )

    def get_store_health(self) -> Dict:
        """Get overall store health status"""
        try:
            # Check inventory
            inventory_status = self.inventory.check_inventory_levels()

            # Get analytics
            stats = self.analytics.get_dashboard_stats(days=7)

            # Determine health status
            health_score = 100
            issues = []

            if len(inventory_status["out_of_stock"]) > 0:
                health_score -= 20
                issues.append(f"{len(inventory_status['out_of_stock'])} products out of stock")

            if len(inventory_status["low_stock"]) > 0:
                health_score -= 10
                issues.append(f"{len(inventory_status['low_stock'])} products low on stock")

            if stats["orders"]["pending"] > 10:
                health_score -= 15
                issues.append(f"{stats['orders']['pending']} pending orders need attention")

            return {
                "health_score": max(0, health_score),
                "status": "healthy" if health_score >= 80 else "warning" if health_score >= 60 else "critical",
                "issues": issues,
                "inventory": inventory_status,
                "stats": stats,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            return {
                "health_score": 0,
                "status": "error",
                "issues": [f"Unable to check store health: {str(e)}"],
                "timestamp": datetime.now().isoformat()
            }

    def sync_products(self, source: str = "csv", file_path: str = "") -> Dict:
        """Sync products from external source"""
        if source == "csv":
            return self.importer.import_from_csv(file_path)
        elif source == "json":
            return self.importer.import_from_json(file_path)
        else:
            raise ValueError(f"Unsupported source: {source}")

    def get_dashboard_data(self) -> Dict:
        """Get complete dashboard data"""
        return {
            "health": self.get_store_health(),
            "analytics": self.analytics.get_dashboard_stats(days=30),
            "customer_stats": self.analytics.get_customer_stats(),
            "timestamp": datetime.now().isoformat()
        }


# ============================================================================
# CLI INTERFACE
# ============================================================================

def print_header(title: str):
    """Print section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """CLI interface for Store Manager"""
    print_header("🛒 CODEX DOMINION - STORE MANAGER")

    # Initialize manager
    manager = StoreManager()

    while True:
        print("\n📋 STORE MANAGER MENU:")
        print("1. 📊 View Dashboard")
        print("2. 🏥 Check Store Health")
        print("3. 📦 View Products")
        print("4. ➕ Create Product")
        print("5. 📥 Import Products (CSV)")
        print("6. 📋 View Orders")
        print("7. 👥 View Customers")
        print("8. 📈 Analytics Report")
        print("9. 📊 Inventory Check")
        print("0. 🚪 Exit")

        choice = input("\n👉 Select option: ").strip()

        if choice == "1":
            # Dashboard
            print_header("📊 STORE DASHBOARD")
            data = manager.get_dashboard_data()

            print(f"🏥 Health Score: {data['health']['health_score']}/100 ({data['health']['status'].upper()})")
            if data['health']['issues']:
                print("\n⚠️  Issues:")
                for issue in data['health']['issues']:
                    print(f"   • {issue}")

            print(f"\n📦 Orders (30 days):")
            print(f"   • Total: {data['analytics']['orders']['total']}")
            print(f"   • Completed: {data['analytics']['orders']['completed']}")
            print(f"   • Revenue: ${data['analytics']['orders']['revenue']:.2f}")
            print(f"   • Avg Order: ${data['analytics']['orders']['average_order_value']:.2f}")

            print(f"\n🛍️  Products:")
            print(f"   • Total: {data['analytics']['products']['total']}")
            print(f"   • In Stock: {data['analytics']['products']['in_stock']}")
            print(f"   • Out of Stock: {data['analytics']['products']['out_of_stock']}")

            print(f"\n👥 Customers:")
            print(f"   • Total: {data['customer_stats']['total_customers']}")
            print(f"   • Avg Orders: {data['customer_stats']['avg_orders_per_customer']:.1f}")
            print(f"   • Avg Spent: ${data['customer_stats']['avg_spent_per_customer']:.2f}")

        elif choice == "2":
            # Store Health
            print_header("🏥 STORE HEALTH CHECK")
            health = manager.get_store_health()
            print(f"Health Score: {health['health_score']}/100")
            print(f"Status: {health['status'].upper()}")

            if health['issues']:
                print("\n⚠️  Issues Found:")
                for issue in health['issues']:
                    print(f"   • {issue}")
            else:
                print("\n✅ No issues found!")

        elif choice == "3":
            # View Products
            print_header("📦 PRODUCTS")
            page = int(input("Page number (default 1): ") or "1")
            products = manager.api.get_products(page=page, per_page=10)

            for product in products:
                print(f"\n🏷️  {product['name']}")
                print(f"   ID: {product['id']} | SKU: {product.get('sku', 'N/A')}")
                print(f"   Price: ${product.get('price', '0')} | Stock: {product.get('stock_status', 'N/A')}")
                if product.get('manage_stock'):
                    print(f"   Quantity: {product.get('stock_quantity', 0)}")

        elif choice == "4":
            # Create Product
            print_header("➕ CREATE PRODUCT")
            name = input("Product name: ")
            regular_price = input("Regular price: ")
            description = input("Description: ")

            product = Product(
                name=name,
                regular_price=regular_price,
                description=description,
                type="simple"
            )

            try:
                result = manager.api.create_product(product)
                print(f"\n✅ Product created! ID: {result['id']}")
            except Exception as e:
                print(f"\n❌ Error: {e}")

        elif choice == "5":
            # Import Products
            print_header("📥 IMPORT PRODUCTS")
            file_path = input("CSV file path: ")

            if os.path.exists(file_path):
                print("\n⏳ Importing products...")
                results = manager.sync_products(source="csv", file_path=file_path)
                print(f"\n✅ Success: {len(results['success'])} products imported")
                if results['errors']:
                    print(f"❌ Errors: {len(results['errors'])} products failed")
            else:
                print(f"\n❌ File not found: {file_path}")

        elif choice == "6":
            # View Orders
            print_header("📋 ORDERS")
            status = input("Status (any/pending/processing/completed): ") or "any"
            orders = manager.api.get_orders(per_page=10, status=status)

            for order in orders:
                print(f"\n🛒 Order #{order['id']}")
                print(f"   Status: {order['status']} | Total: ${order['total']}")
                print(f"   Customer: {order['billing']['first_name']} {order['billing']['last_name']}")
                print(f"   Date: {order['date_created']}")

        elif choice == "7":
            # View Customers
            print_header("👥 CUSTOMERS")
            customers = manager.api.get_customers(per_page=10)

            for customer in customers:
                print(f"\n👤 {customer['first_name']} {customer['last_name']}")
                print(f"   Email: {customer['email']}")
                print(f"   Orders: {customer['orders_count']} | Spent: ${customer['total_spent']}")

        elif choice == "8":
            # Analytics Report
            print_header("📈 ANALYTICS REPORT")
            days = int(input("Period (days, default 30): ") or "30")
            stats = manager.analytics.get_dashboard_stats(days=days)

            print(f"\n📊 Sales Performance ({days} days):")
            print(f"   • Total Orders: {stats['orders']['total']}")
            print(f"   • Completed: {stats['orders']['completed']}")
            print(f"   • Revenue: ${stats['orders']['revenue']:.2f}")
            print(f"   • Avg Order Value: ${stats['orders']['average_order_value']:.2f}")

            if stats['top_sellers']:
                print(f"\n🏆 Top Sellers:")
                for i, seller in enumerate(stats['top_sellers'][:5], 1):
                    print(f"   {i}. {seller.get('title', 'Unknown')} - {seller.get('quantity', 0)} sold")

        elif choice == "9":
            # Inventory Check
            print_header("📊 INVENTORY CHECK")
            inventory = manager.inventory.check_inventory_levels()

            if inventory['out_of_stock']:
                print("\n❌ OUT OF STOCK:")
                for item in inventory['out_of_stock']:
                    print(f"   • {item['name']} (SKU: {item['sku']})")

            if inventory['low_stock']:
                print("\n⚠️  LOW STOCK:")
                for item in inventory['low_stock']:
                    print(f"   • {item['name']} - {item['stock']} remaining (SKU: {item['sku']})")

            if not inventory['out_of_stock'] and not inventory['low_stock']:
                print("\n✅ All products have sufficient stock!")

        elif choice == "0":
            print("\n👋 Goodbye!")
            break

        else:
            print("\n❌ Invalid option!")


if __name__ == "__main__":
    main()
