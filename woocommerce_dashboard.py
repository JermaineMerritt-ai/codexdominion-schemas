"""
🔥 Codex Dominion - WooCommerce Dashboard Integration
Streamlit component for WooCommerce product synchronization
"""

import streamlit as st
import json
from datetime import datetime
from codex_woocommerce_sync import CodexWooCommerceSync

def render_woocommerce_tab():
    """Render the WooCommerce tab in the Codex Dashboard"""
    
    st.header("🏪 WooCommerce Store Integration")
    st.markdown("**The Merritt Method Store - Product Synchronization & Management**")
    
    # Configuration section
    with st.expander("⚙️ Configuration", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            store_url = st.text_input(
                "Store URL", 
                value="https://store.themerrittmethod.com",
                help="Your WooCommerce store URL"
            )
            
            consumer_key = st.text_input(
                "Consumer Key",
                value="",
                type="password",
                help="WooCommerce API Consumer Key"
            )
        
        with col2:
            consumer_secret = st.text_input(
                "Consumer Secret",
                value="",
                type="password",
                help="WooCommerce API Consumer Secret"
            )
            
            if st.button("💾 Save Configuration"):
                config = {
                    "store_url": store_url,
                    "consumer_key": consumer_key,
                    "consumer_secret": consumer_secret
                }
                try:
                    with open("woocommerce_config.json", "r") as f:
                        existing_config = json.load(f)
                    
                    existing_config.update({
                        "woocommerce": {
                            "base_url": f"{store_url}/wp-json/wc/v3",
                            "consumer_key": consumer_key,
                            "consumer_secret": consumer_secret
                        }
                    })
                    
                    with open("woocommerce_config.json", "w") as f:
                        json.dump(existing_config, f, indent=2)
                    
                    st.success("✅ Configuration saved!")
                except Exception as e:
                    st.error(f"❌ Error saving configuration: {e}")
    
    st.divider()
    
    # Initialize sync client
    if consumer_key and consumer_secret:
        sync_client = CodexWooCommerceSync(
            store_url=store_url,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret
        )
    else:
        sync_client = CodexWooCommerceSync()
    
    # Connection status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Test Connection"):
            with st.spinner("Testing connection..."):
                connection_ok = sync_client.test_connection()
                if connection_ok:
                    st.success("✅ Connection successful!")
                else:
                    st.error("❌ Connection failed!")
    
    with col2:
        if st.button("📁 Get Categories"):
            with st.spinner("Loading categories..."):
                categories = sync_client.get_categories()
                if categories:
                    st.success(f"Found {len(categories)} categories")
                    for cat in categories[:5]:
                        st.write(f"• {cat['name']} (ID: {cat['id']})")
                else:
                    st.warning("No categories found")
    
    with col3:
        if st.button("📦 Count Products"):
            with st.spinner("Counting products..."):
                products = sync_client.get_existing_products()
                st.info(f"📊 {len(products)} products in store")
    
    st.divider()
    
    # Product synchronization section
    st.subheader("🚀 Product Synchronization")
    
    tab1, tab2, tab3 = st.tabs(["📤 Sync Products", "📝 Create Custom", "📊 Sync History"])
    
    with tab1:
        st.markdown("**Sync products from sample data**")
        
        # Load sample products
        try:
            with open('sample_products.json', 'r') as f:
                sample_data = json.load(f)
            
            if isinstance(sample_data, dict) and 'products' in sample_data:
                products = sample_data['products']
            else:
                products = sample_data if isinstance(sample_data, list) else []
            
            st.success(f"✅ Loaded {len(products)} sample products")
            
            # Product selection
            if products:
                selected_indices = st.multiselect(
                    "Select products to sync:",
                    range(len(products)),
                    format_func=lambda x: f"{products[x].get('title', products[x].get('name', 'Unknown'))} - ${products[x].get('price', products[x].get('regular_price', 'N/A'))}"
                )
                
                selected_products = [products[i] for i in selected_indices]
                
                if selected_products:
                    st.write(f"Selected {len(selected_products)} products for sync")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        dry_run = st.checkbox("🧪 Dry Run (test only)", value=True)
                    with col2:
                        auto_update = st.checkbox("🔄 Update existing products", value=False)
                    
                    if st.button("🚀 Sync Products", type="primary"):
                        if dry_run:
                            st.info("🧪 Dry run mode - no products will be created")
                            for i, product in enumerate(selected_products, 1):
                                name = product.get('title', product.get('name', 'Unknown'))
                                price = product.get('price', product.get('regular_price', 'N/A'))
                                st.write(f"{i}. Would create: **{name}** - ${price}")
                        else:
                            with st.spinner("Syncing products..."):
                                results = sync_client.sync_products(selected_products)
                                
                                # Display results
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("✅ Success", results['success'])
                                with col2:
                                    st.metric("❌ Failed", results['failed'])
                                
                                if results['created_products']:
                                    st.success("🎉 Created Products:")
                                    for product in results['created_products']:
                                        st.write(f"• **{product['name']}** (ID: {product['id']}) - ${product['price']}")
                                
                                if results['errors']:
                                    st.error("⚠️ Errors:")
                                    for error in results['errors']:
                                        st.write(f"• {error}")
        
        except FileNotFoundError:
            st.warning("📦 No sample products file found")
            if st.button("🔧 Create Sample Products"):
                # Create basic sample products
                sample_products = {
                    "products": [
                        {
                            "title": "Digital Sovereignty Starter Kit",
                            "price": 97.00,
                            "description": "Essential tools for digital independence",
                            "type": "simple",
                            "virtual": True,
                            "downloadable": True
                        }
                    ]
                }
                
                with open('sample_products.json', 'w') as f:
                    json.dump(sample_products, f, indent=2)
                
                st.success("✅ Sample products created!")
                st.rerun()
    
    with tab2:
        st.markdown("**Create custom product**")
        
        with st.form("create_product"):
            col1, col2 = st.columns(2)
            
            with col1:
                product_name = st.text_input("Product Name*")
                product_price = st.number_input("Price ($)*", min_value=0.01, value=97.00)
                product_type = st.selectbox("Product Type", ["simple", "variable", "grouped"])
                
            with col2:
                product_sku = st.text_input("SKU")
                category_id = st.number_input("Category ID", min_value=1, value=1)
                is_virtual = st.checkbox("Virtual Product", value=True)
                is_downloadable = st.checkbox("Downloadable", value=True)
                is_featured = st.checkbox("Featured Product", value=False)
            
            product_description = st.text_area("Product Description")
            short_description = st.text_input("Short Description")
            
            submitted = st.form_submit_button("🛍️ Create Product", type="primary")
            
            if submitted and product_name and product_price:
                custom_product = {
                    "name": product_name,
                    "type": product_type,
                    "regular_price": str(product_price),
                    "description": product_description,
                    "short_description": short_description,
                    "sku": product_sku,
                    "categories": [{"id": category_id}] if category_id else [],
                    "virtual": is_virtual,
                    "downloadable": is_downloadable,
                    "featured": is_featured,
                    "status": "publish"
                }
                
                with st.spinner("Creating product..."):
                    created_product = sync_client.create_product(custom_product)
                    
                    if created_product:
                        st.success(f"✅ Created product: {created_product['name']}")
                        st.json(created_product)
                    else:
                        st.error("❌ Failed to create product")
    
    with tab3:
        st.markdown("**Synchronization History**")
        
        # Load sync history
        import glob
        
        sync_files = glob.glob("wc_sync_results_*.json")
        
        if sync_files:
            # Sort by date (newest first)
            sync_files.sort(reverse=True)
            
            st.write(f"Found {len(sync_files)} sync history files")
            
            for sync_file in sync_files[:10]:  # Show last 10 syncs
                try:
                    with open(sync_file, 'r') as f:
                        sync_data = json.load(f)
                    
                    sync_time = sync_data.get('sync_time', 'Unknown')
                    success_count = sync_data.get('success', 0)
                    failed_count = sync_data.get('failed', 0)
                    
                    with st.expander(f"📅 {sync_time} - ✅{success_count} ❌{failed_count}"):
                        st.json(sync_data)
                
                except Exception as e:
                    st.error(f"Error reading {sync_file}: {e}")
        else:
            st.info("📝 No sync history found yet")
    
    st.divider()
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 Refresh Store Data"):
            st.rerun()
    
    with col2:
        if st.button("📊 Store Analytics"):
            st.info("🚧 Analytics coming soon!")
    
    with col3:
        if st.button("💾 Export Products"):
            try:
                products = sync_client.get_existing_products()
                if products:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"wc_products_export_{timestamp}.json"
                    
                    with open(filename, 'w') as f:
                        json.dump(products, f, indent=2)
                    
                    st.success(f"📤 Products exported to {filename}")
                else:
                    st.warning("No products to export")
            except Exception as e:
                st.error(f"❌ Export failed: {e}")
    
    with col4:
        if st.button("🛡️ Backup Store"):
            st.info("🚧 Backup feature coming soon!")

# Add this to your main dashboard tabs
def add_woocommerce_to_dashboard():
    """Instructions for adding WooCommerce tab to main dashboard"""
    instructions = """
    To add WooCommerce integration to your main Codex Dashboard:
    
    1. Open codex_dashboard.py
    2. Add this import at the top:
       from woocommerce_dashboard import render_woocommerce_tab
    
    3. Add a new tab in your tab list:
       tabs = st.tabs([..., "🏪 WooCommerce Store", ...])
    
    4. Add the WooCommerce tab content:
       with tabs[X]:  # Replace X with appropriate index
           render_woocommerce_tab()
    """
    return instructions

if __name__ == "__main__":
    # Standalone test
    st.set_page_config(
        page_title="🏪 WooCommerce Integration Test",
        page_icon="🏪",
        layout="wide"
    )
    
    st.title("🔥 Codex Dominion - WooCommerce Integration")
    render_woocommerce_tab()