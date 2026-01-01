import os
import requests
from requests.auth import HTTPBasicAuth

WC_CONSUMER_KEY = os.getenv("WC_CONSUMER_KEY")
WC_CONSUMER_SECRET = os.getenv("WC_CONSUMER_SECRET")
WC_API_VERSION = "wc/v3"


def _wc_auth():
    return HTTPBasicAuth(WC_CONSUMER_KEY, WC_CONSUMER_SECRET)


def create_product(store_domain: str, product_payload: dict) -> dict:
    """
    Creates a product in WooCommerce.
    product_payload: https://woocommerce.github.io/woocommerce-rest-api-docs/#product-properties
    """
    url = f"{store_domain}/wp-json/wc/v3/products"
    resp = requests.post(url, auth=_wc_auth(), json=product_payload)
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"WooCommerce create_product failed: {resp.status_code} {resp.text}")
    return resp.json()


def update_product(store_domain: str, product_id: int, product_payload: dict) -> dict:
    """
    Updates a product in WooCommerce.
    """
    url = f"{store_domain}/wp-json/wc/v3/products/{product_id}"
    resp = requests.put(url, auth=_wc_auth(), json=product_payload)
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"WooCommerce update_product failed: {resp.status_code} {resp.text}")
    return resp.json()


def get_store_info(store_domain: str) -> dict:
    """
    Minimal health check – Woo doesn't have a single 'shop' endpoint like Shopify.
    You can fetch settings or a sample request to verify auth.
    """
    url = f"{store_domain}/wp-json/wc/v3/system_status"
    resp = requests.get(url, auth=_wc_auth())
    if resp.status_code != 200:
        raise RuntimeError(f"WooCommerce get_store_info failed: {resp.status_code} {resp.text}")
    return resp.json()
