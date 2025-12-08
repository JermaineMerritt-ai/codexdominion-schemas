#!/bin/bash
# WooCommerce Product Taxonomy Setup
# Run inside WordPress container: docker exec -it <container> bash
# Then: wp --allow-root < setup-woocommerce-taxonomy.sh

echo "=========================================="
echo "Setting up WooCommerce Product Categories"
echo "=========================================="

# Product Categories
wp term create product_cat "Kids Bible Stories" --description="Animated Bible stories for children" --allow-root
wp term create product_cat "Coloring Books" --description="Printable coloring activities" --allow-root
wp term create product_cat "Activity Packs" --description="Educational activity bundles" --allow-root
wp term create product_cat "Homeschool" --description="Homeschooling resources" --allow-root
wp term create product_cat "Seasonal" --description="Holiday and seasonal content" --allow-root
wp term create product_cat "Memory Verses" --description="Scripture memorization tools" --allow-root
wp term create product_cat "Parents" --description="Resources for parents" --allow-root
wp term create product_cat "Churches" --description="Church ministry materials" --allow-root
wp term create product_cat "Bundles" --description="Product bundle deals" --allow-root
wp term create product_cat "Multi-Language" --description="Multilingual products" --allow-root
wp term create product_cat "Wedding" --description="Wedding and marriage resources" --allow-root
wp term create product_cat "Eco-Friendly" --description="Sustainable and eco-conscious products" --allow-root
wp term create product_cat "Animals" --description="Animal-themed content" --allow-root
wp term create product_cat "Home Decor" --description="Decorative items and prints" --allow-root
wp term create product_cat "Digital Downloads" --description="Instant digital products" --allow-root

echo ""
echo "=========================================="
echo "Setting up WooCommerce Product Tags"
echo "=========================================="

# Product Tags - Episodes
wp term create product_tag "episode-christmas" --description="Christmas story episode" --allow-root
wp term create product_tag "episode-noah" --description="Noah's Ark episode" --allow-root

# Product Tags - Content Types
wp term create product_tag "coloring" --description="Coloring activities" --allow-root
wp term create product_tag "activity" --description="Interactive activities" --allow-root
wp term create product_tag "homeschool" --description="Homeschool curriculum" --allow-root
wp term create product_tag "memory-verse" --description="Bible verse memorization" --allow-root

# Product Tags - Special Features
wp term create product_tag "eco-friendly" --description="Environmentally friendly" --allow-root
wp term create product_tag "animals" --description="Animal content" --allow-root
wp term create product_tag "home-decor" --description="Home decoration" --allow-root
wp term create product_tag "digital" --description="Digital download" --allow-root

# Product Tags - Languages
wp term create product_tag "spanish" --description="Spanish language" --allow-root
wp term create product_tag "french" --description="French language" --allow-root
wp term create product_tag "haitian-creole" --description="Haitian Creole language" --allow-root

# Product Tags - Special Occasions
wp term create product_tag "wedding" --description="Wedding related" --allow-root

echo ""
echo "=========================================="
echo "Taxonomy Setup Complete!"
echo "=========================================="
echo ""
echo "Categories created: 15"
echo "Tags created: 14"
echo ""
echo "Verify with:"
echo "  wp term list product_cat --allow-root"
echo "  wp term list product_tag --allow-root"
