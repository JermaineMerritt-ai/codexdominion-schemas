"""
WooCommerce Product Uploader for Faith-Empire Digital Products
Uploads generated Advent devotional to WooCommerce store
"""

import json
import os
from pathlib import Path
from typing import Dict, Any
from woocommerce import API
from dotenv import load_dotenv

load_dotenv()


class WooCommerceUploader:
    """Upload digital products to WooCommerce"""

    def __init__(self):
        self.wcapi = API(
            url=os.getenv("WC_API_URL", "https://codexdominion.app"),
            consumer_key=os.getenv("WC_CONSUMER_KEY"),
            consumer_secret=os.getenv("WC_CONSUMER_SECRET"),
            version="wc/v3",
            timeout=30
        )

    def upload_advent_devotional(self, product_json_path: str) -> Dict[str, Any]:
        """Upload Advent devotional as WooCommerce product"""

        # Load product data
        with open(product_json_path, "r") as f:
            product = json.load(f)

        # Prepare WooCommerce product data
        wc_product = {
            "name": product["title"],
            "type": "simple",
            "regular_price": str(product["pricing"]["base_price"]),
            "description": self._generate_description(product),
            "short_description": product["subtitle"],
            "virtual": True,
            "downloadable": True,
            "download_limit": -1,  # Unlimited downloads
            "download_expiry": -1,  # Never expires
            "categories": [
                {"name": "Digital Downloads"},
                {"name": "Faith & Devotional"},
                {"name": "Advent"}
            ],
            "tags": [{"name": tag} for tag in product["distribution"]["product_tags"]],
            "images": [
                {
                    "src": "https://codexdominion.app/images/advent-devotional-cover.jpg",
                    "alt": product["title"]
                }
            ],
            "meta_data": [
                {"key": "_product_id", "value": product["product_id"]},
                {"key": "_realm", "value": product["realm"]},
                {"key": "_engines", "value": ",".join(product["bound_engines"])},
                {"key": "_word_count", "value": str(product["metadata"]["word_count"])},
                {"key": "_reading_time", "value": product["metadata"]["reading_time_per_day"]},
            ]
        }

        # Create product
        try:
            response = self.wcapi.post("products", wc_product)

            if response.status_code == 201:
                wc_product_id = response.json()["id"]
                print(f"✅ Product uploaded successfully!")
                print(f"   WooCommerce ID: {wc_product_id}")
                print(f"   View at: {os.getenv('WC_API_URL')}/product/{response.json()['slug']}")
                return response.json()
            else:
                print(f"❌ Upload failed: {response.status_code}")
                print(f"   {response.json()}")
                return None

        except Exception as e:
            print(f"❌ Error uploading to WooCommerce: {e}")
            return None

    def _generate_description(self, product: Dict[str, Any]) -> str:
        """Generate rich product description HTML"""

        html = f"""
        <div class="advent-devotional-description">
            <h2>Journey Through Advent with Purpose</h2>
            <p>Experience the true meaning of Christmas with this comprehensive 25-day devotional guide.
            Each day brings fresh insights into the themes of <strong>Hope, Peace, Joy, and Love</strong>
            that define the Advent season.</p>

            <h3>What's Included:</h3>
            <ul>
        """

        for feature in product["metadata"]["includes"]:
            html += f"        <li>{feature}</li>\n"

        html += f"""
            </ul>

            <h3>Perfect For:</h3>
            <ul>
                <li>Personal daily devotions</li>
                <li>Family worship and discussion</li>
                <li>Small group studies</li>
                <li>Gift-giving to friends and loved ones</li>
            </ul>

            <h3>Product Details:</h3>
            <ul>
                <li><strong>Total Days:</strong> {product["metadata"]["total_days"]}</li>
                <li><strong>Reading Time:</strong> {product["metadata"]["reading_time_per_day"]} per day</li>
                <li><strong>Word Count:</strong> {product["metadata"]["word_count"]:,} words</li>
                <li><strong>Format:</strong> PDF, EPUB, MOBI (all included)</li>
                <li><strong>Delivery:</strong> Instant download after purchase</li>
            </ul>

            <h3>Features:</h3>
            <ul>
                <li>✓ Printable for journaling</li>
                <li>✓ Mobile-friendly reading</li>
                <li>✓ Share with family members</li>
                <li>✓ Perfect for Advent study groups</li>
            </ul>

            <div class="purchase-now-cta">
                <p><strong>Start your Advent journey today!</strong> Download instantly and begin reading within minutes.</p>
            </div>
        </div>
        """

        return html


def main():
    """Upload generated Advent devotional to WooCommerce"""

    print("\n" + "="*60)
    print("🛒 WOOCOMMERCE PRODUCT UPLOADER")
    print("="*60 + "\n")

    # Find latest Advent product JSON
    content_dir = Path("content/faith-empire/advent-devotional")
    product_files = list(content_dir.glob("advent-*-product.json"))

    if not product_files:
        print("❌ No Advent product files found!")
        print(f"   Expected location: {content_dir}")
        return

    latest_product = sorted(product_files)[-1]
    print(f"📦 Found product: {latest_product.name}\n")

    # Upload to WooCommerce
    uploader = WooCommerceUploader()
    result = uploader.upload_advent_devotional(str(latest_product))

    if result:
        print("\n✅ Upload complete!")
        print("\n💡 Next Steps:")
        print("   1. Review product page in WooCommerce admin")
        print("   2. Add product images and cover art")
        print("   3. Configure digital file downloads")
        print("   4. Set up email notifications for purchasers")
        print("   5. Create marketing campaigns")
    else:
        print("\n❌ Upload failed. Check WooCommerce credentials and try again.")


if __name__ == "__main__":
    main()
