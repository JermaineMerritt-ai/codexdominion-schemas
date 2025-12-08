<?php
/**
 * Plugin Name: CodexDominion Schema Markup
 * Plugin URI: https://codexdominion.app
 * Description: Adds Schema.org structured data (JSON-LD) to WooCommerce products for better SEO
 * Version: 1.0.0
 * Author: CodexDominion
 * Author URI: https://codexdominion.app
 * Text Domain: codex-schema-markup
 * Requires at least: 5.8
 * Requires PHP: 7.4
 * WC requires at least: 5.0
 * WC tested up to: 8.0
 *
 * @package CodexDominion\SchemaMarkup
 */

defined('ABSPATH') || exit;

/**
 * Add Product Schema to single product pages
 */
add_action('wp_head', 'codex_add_product_schema', 5);

function codex_add_product_schema() {
    if (!is_product()) {
        return;
    }

    global $product;

    if (!$product || !is_a($product, 'WC_Product')) {
        return;
    }

    $schema = codex_generate_product_schema($product);

    if ($schema) {
        echo '<script type="application/ld+json">' . "\n";
        echo wp_json_encode($schema, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n";
        echo '</script>' . "\n";
    }
}

/**
 * Generate Product Schema data
 *
 * @param WC_Product $product
 * @return array|null
 */
function codex_generate_product_schema($product) {
    if (!$product) {
        return null;
    }

    $schema = [
        '@context' => 'https://schema.org',
        '@type' => 'Product',
        'name' => $product->get_name(),
        'description' => wp_strip_all_tags($product->get_short_description() ?: $product->get_description()),
    ];

    // SKU
    if ($product->get_sku()) {
        $schema['sku'] = $product->get_sku();
    }

    // Brand
    $schema['brand'] = [
        '@type' => 'Brand',
        'name' => 'CodexDominion'
    ];

    // Image
    $image_id = $product->get_image_id();
    if ($image_id) {
        $image_url = wp_get_attachment_image_url($image_id, 'full');
        if ($image_url) {
            $schema['image'] = $image_url;
        }
    }

    // Offers
    $schema['offers'] = codex_generate_offer_schema($product);

    // Aggregated Rating (if reviews exist)
    if ($product->get_review_count() > 0) {
        $schema['aggregateRating'] = [
            '@type' => 'AggregateRating',
            'ratingValue' => $product->get_average_rating(),
            'reviewCount' => $product->get_review_count(),
            'bestRating' => '5',
            'worstRating' => '1'
        ];
    }

    // Additional properties for digital products
    if ($product->is_virtual() || $product->is_downloadable()) {
        $schema['additionalType'] = 'https://schema.org/DigitalDocument';
    }

    // Categories
    $categories = wp_get_post_terms($product->get_id(), 'product_cat', ['fields' => 'names']);
    if (!empty($categories) && !is_wp_error($categories)) {
        $schema['category'] = implode(', ', $categories);
    }

    return $schema;
}

/**
 * Generate Offer Schema
 *
 * @param WC_Product $product
 * @return array
 */
function codex_generate_offer_schema($product) {
    $offer = [
        '@type' => 'Offer',
        'price' => $product->get_price(),
        'priceCurrency' => get_woocommerce_currency(),
        'url' => get_permalink($product->get_id())
    ];

    // Availability
    if ($product->is_in_stock()) {
        $offer['availability'] = 'https://schema.org/InStock';
    } elseif ($product->is_on_backorder()) {
        $offer['availability'] = 'https://schema.org/BackOrder';
    } else {
        $offer['availability'] = 'https://schema.org/OutOfStock';
    }

    // Price valid until (30 days from now)
    $offer['priceValidUntil'] = date('Y-m-d', strtotime('+30 days'));

    // Sale price
    if ($product->is_on_sale() && $product->get_sale_price()) {
        $offer['price'] = $product->get_sale_price();

        // Add regular price as additional offer
        $offer['priceSpecification'] = [
            '@type' => 'PriceSpecification',
            'price' => $product->get_regular_price(),
            'priceCurrency' => get_woocommerce_currency()
        ];
    }

    // Seller
    $offer['seller'] = [
        '@type' => 'Organization',
        'name' => get_bloginfo('name'),
        'url' => home_url()
    ];

    return $offer;
}

/**
 * Add Organization Schema to homepage
 */
add_action('wp_head', 'codex_add_organization_schema', 5);

function codex_add_organization_schema() {
    if (!is_front_page()) {
        return;
    }

    $schema = [
        '@context' => 'https://schema.org',
        '@type' => 'Organization',
        'name' => 'CodexDominion',
        'url' => home_url(),
        'logo' => get_site_icon_url(),
        'description' => get_bloginfo('description'),
        'sameAs' => []
    ];

    // Add social media profiles if available
    $social_profiles = [
        'facebook' => get_option('codex_facebook_url'),
        'twitter' => get_option('codex_twitter_url'),
        'instagram' => get_option('codex_instagram_url'),
        'youtube' => get_option('codex_youtube_url'),
        'pinterest' => get_option('codex_pinterest_url')
    ];

    foreach ($social_profiles as $profile_url) {
        if ($profile_url) {
            $schema['sameAs'][] = $profile_url;
        }
    }

    if (empty($schema['sameAs'])) {
        unset($schema['sameAs']);
    }

    echo '<script type="application/ld+json">' . "\n";
    echo wp_json_encode($schema, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n";
    echo '</script>' . "\n";
}

/**
 * Add BreadcrumbList Schema
 */
add_action('wp_head', 'codex_add_breadcrumb_schema', 5);

function codex_add_breadcrumb_schema() {
    if (is_front_page() || !is_singular()) {
        return;
    }

    $items = [
        [
            '@type' => 'ListItem',
            'position' => 1,
            'name' => 'Home',
            'item' => home_url()
        ]
    ];

    $position = 2;

    // Add product category breadcrumb
    if (is_product()) {
        global $product;

        if ($product) {
            $categories = wp_get_post_terms($product->get_id(), 'product_cat');

            if (!empty($categories) && !is_wp_error($categories)) {
                $category = $categories[0];
                $items[] = [
                    '@type' => 'ListItem',
                    'position' => $position++,
                    'name' => $category->name,
                    'item' => get_term_link($category)
                ];
            }

            // Current product
            $items[] = [
                '@type' => 'ListItem',
                'position' => $position,
                'name' => $product->get_name(),
                'item' => get_permalink($product->get_id())
            ];
        }
    }

    if (count($items) > 1) {
        $schema = [
            '@context' => 'https://schema.org',
            '@type' => 'BreadcrumbList',
            'itemListElement' => $items
        ];

        echo '<script type="application/ld+json">' . "\n";
        echo wp_json_encode($schema, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n";
        echo '</script>' . "\n";
    }
}

/**
 * Settings page for social media URLs
 */
add_action('admin_menu', 'codex_schema_settings_menu');

function codex_schema_settings_menu() {
    add_submenu_page(
        'woocommerce',
        'Schema Markup Settings',
        'Schema Markup',
        'manage_woocommerce',
        'codex-schema-markup',
        'codex_schema_settings_page'
    );
}

function codex_schema_settings_page() {
    if (isset($_POST['codex_save_schema_settings']) && check_admin_referer('codex_schema_settings')) {
        update_option('codex_facebook_url', sanitize_url($_POST['facebook_url'] ?? ''));
        update_option('codex_twitter_url', sanitize_url($_POST['twitter_url'] ?? ''));
        update_option('codex_instagram_url', sanitize_url($_POST['instagram_url'] ?? ''));
        update_option('codex_youtube_url', sanitize_url($_POST['youtube_url'] ?? ''));
        update_option('codex_pinterest_url', sanitize_url($_POST['pinterest_url'] ?? ''));

        echo '<div class="notice notice-success"><p>Settings saved successfully!</p></div>';
    }

    ?>
    <div class="wrap">
        <h1>CodexDominion Schema Markup Settings</h1>

        <div class="card">
            <h2>What This Plugin Does</h2>
            <p>Automatically adds Schema.org structured data (JSON-LD) to your site:</p>
            <ul>
                <li><strong>Product Schema:</strong> Added to all WooCommerce product pages (name, price, availability, ratings)</li>
                <li><strong>Organization Schema:</strong> Added to homepage with social media links</li>
                <li><strong>Breadcrumb Schema:</strong> Added to product pages for better search navigation</li>
            </ul>
            <p>This helps search engines understand your content better, leading to rich snippets in search results!</p>
        </div>

        <div class="card">
            <h2>Social Media Profiles</h2>
            <p>Add your social media URLs to include them in Organization Schema:</p>

            <form method="post">
                <?php wp_nonce_field('codex_schema_settings'); ?>

                <table class="form-table">
                    <tr>
                        <th><label for="facebook_url">Facebook URL</label></th>
                        <td>
                            <input type="url" id="facebook_url" name="facebook_url"
                                   value="<?php echo esc_attr(get_option('codex_facebook_url')); ?>"
                                   class="regular-text" placeholder="https://facebook.com/codexdominion">
                        </td>
                    </tr>
                    <tr>
                        <th><label for="twitter_url">Twitter/X URL</label></th>
                        <td>
                            <input type="url" id="twitter_url" name="twitter_url"
                                   value="<?php echo esc_attr(get_option('codex_twitter_url')); ?>"
                                   class="regular-text" placeholder="https://twitter.com/codexdominion">
                        </td>
                    </tr>
                    <tr>
                        <th><label for="instagram_url">Instagram URL</label></th>
                        <td>
                            <input type="url" id="instagram_url" name="instagram_url"
                                   value="<?php echo esc_attr(get_option('codex_instagram_url')); ?>"
                                   class="regular-text" placeholder="https://instagram.com/codexdominion">
                        </td>
                    </tr>
                    <tr>
                        <th><label for="youtube_url">YouTube URL</label></th>
                        <td>
                            <input type="url" id="youtube_url" name="youtube_url"
                                   value="<?php echo esc_attr(get_option('codex_youtube_url')); ?>"
                                   class="regular-text" placeholder="https://youtube.com/@codexdominion">
                        </td>
                    </tr>
                    <tr>
                        <th><label for="pinterest_url">Pinterest URL</label></th>
                        <td>
                            <input type="url" id="pinterest_url" name="pinterest_url"
                                   value="<?php echo esc_attr(get_option('codex_pinterest_url')); ?>"
                                   class="regular-text" placeholder="https://pinterest.com/codexdominion">
                        </td>
                    </tr>
                </table>

                <p class="submit">
                    <button type="submit" name="codex_save_schema_settings" class="button button-primary">
                        Save Settings
                    </button>
                </p>
            </form>
        </div>

        <div class="card">
            <h2>Testing Your Schema</h2>
            <p>Verify your structured data is working correctly:</p>
            <ul>
                <li><a href="https://search.google.com/test/rich-results" target="_blank">Google Rich Results Test</a></li>
                <li><a href="https://validator.schema.org/" target="_blank">Schema.org Validator</a></li>
            </ul>
        </div>
    </div>
    <?php
}
