import os
import requests

SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")  # per store, or stored in DB per store
SHOPIFY_API_VERSION = "2024-01"


def _shopify_headers(access_token: str):
    return {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }


def create_product(store_domain: str, access_token: str, product_payload: dict) -> dict:
    """
    Creates a product in Shopify.
    product_payload should match Shopify's product schema:
    https://shopify.dev/docs/api/admin-rest/latest/resources/product
    """
    url = f"https://{store_domain}/admin/api/{SHOPIFY_API_VERSION}/products.json"
    resp = requests.post(url, headers=_shopify_headers(access_token), json={"product": product_payload})
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"Shopify create_product failed: {resp.status_code} {resp.text}")
    return resp.json()["product"]


def update_product(store_domain: str, access_token: str, product_id: int, product_payload: dict) -> dict:
    """
    Updates a product in Shopify.
    """
    url = f"https://{store_domain}/admin/api/{SHOPIFY_API_VERSION}/products/{product_id}.json"
    resp = requests.put(url, headers=_shopify_headers(access_token), json={"product": product_payload})
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"Shopify update_product failed: {resp.status_code} {resp.text}")
    return resp.json()["product"]


def get_store_info(store_domain: str, access_token: str) -> dict:
    """
    Fetch basic store details to verify connection.
    """
    url = f"https://{store_domain}/admin/api/{SHOPIFY_API_VERSION}/shop.json"
    resp = requests.get(url, headers=_shopify_headers(access_token))
    if resp.status_code != 200:
        raise RuntimeError(f"Shopify get_store_info failed: {resp.status_code} {resp.text}")
    return resp.json()["shop"]
