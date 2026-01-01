from models import Store
from shopify_service import create_product as shopify_create_product, update_product as shopify_update_product
from woocommerce_service import create_product as woo_create_product, update_product as woo_update_product


class StoreServiceError(Exception):
    pass


def create_product(store: Store, product_payload: dict) -> dict:
    """
    Creates a product in the given store, regardless of platform.
    """
    if store.platform == "shopify":
        if not store.access_token:
            raise StoreServiceError("Shopify store missing access_token")
        return shopify_create_product(
            store_domain=store.domain,
            access_token=store.access_token,
            product_payload=product_payload
        )

    elif store.platform == "woocommerce":
        return woo_create_product(
            store_domain=store.domain,
            product_payload=product_payload
        )

    else:
        raise StoreServiceError(f"Unsupported platform: {store.platform}")


def update_product(store: Store, product_id: int, product_payload: dict) -> dict:
    """
    Updates a product in the given store, regardless of platform.
    """
    if store.platform == "shopify":
        if not store.access_token:
            raise StoreServiceError("Shopify store missing access_token")
        return shopify_update_product(
            store_domain=store.domain,
            access_token=store.access_token,
            product_id=product_id,
            product_payload=product_payload
        )

    elif store.platform == "woocommerce":
        return woo_update_product(
            store_domain=store.domain,
            product_id=product_id,
            product_payload=product_payload
        )

    else:
        raise StoreServiceError(f"Unsupported platform: {store.platform}")
