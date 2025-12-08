<?php
/**
 * Plugin Name: CodexDominion Auto Bundles
 * Plugin URI: https://codexdominion.app
 * Description: Automatically adds products to WooCommerce bundles based on tags
 * Version: 1.0.0
 * Author: CodexDominion
 * Author URI: https://codexdominion.app
 * Text Domain: codex-auto-bundles
 * Domain Path: /languages
 * Requires at least: 5.8
 * Requires PHP: 7.4
 * WC requires at least: 5.0
 * WC tested up to: 8.0
 *
 * @package CodexDominion\AutoBundles
 */

defined('ABSPATH') || exit;

/**
 * Main hook: When a product is saved, check tags and add to appropriate bundles
 */
add_action('save_post_product', 'codex_auto_assign_to_bundles', 10, 1);

function codex_auto_assign_to_bundles($post_id) {
    // Avoid infinite loops and revisions
    if (wp_is_post_revision($post_id) || wp_is_post_autosave($post_id)) {
        return;
    }

    // Get product tags
    $tags = wp_get_post_terms($post_id, 'product_tag', ['fields' => 'slugs']);

    if (is_wp_error($tags) || empty($tags)) {
        return;
    }

    // Seasonal Christmas Bundle
    if (in_array('seasonal-christmas', $tags) || in_array('episode-christmas', $tags)) {
        codex_add_to_bundle('Christmas Mega Bundle', $post_id);
    }

    // Homeschool Bundles
    if (in_array('homeschool', $tags)) {
        codex_add_to_bundle('Homeschool Starter Pack', $post_id);
        codex_add_to_bundle('Homeschool Master Pack', $post_id);
    }

    // Wedding Bundle
    if (in_array('wedding', $tags)) {
        codex_add_to_bundle('Wedding Printables Mega Bundle', $post_id);
    }

    // Activity Pack Bundle
    if (in_array('activity', $tags)) {
        codex_add_to_bundle('Activity Mega Pack', $post_id);
    }

    // Coloring Bundle
    if (in_array('coloring', $tags)) {
        codex_add_to_bundle('Coloring Collection Bundle', $post_id);
    }

    // Multi-Language Bundle
    if (in_array('spanish', $tags) || in_array('french', $tags) || in_array('haitian-creole', $tags)) {
        codex_add_to_bundle('Multi-Language Bundle', $post_id);
    }

    // Digital Downloads Bundle
    if (in_array('digital', $tags)) {
        codex_add_to_bundle('Digital Downloads Complete Pack', $post_id);
    }

    // Memory Verse Bundle
    if (in_array('memory-verse', $tags)) {
        codex_add_to_bundle('Memory Verse Collection', $post_id);
    }

    // Eco-Friendly Bundle
    if (in_array('eco-friendly', $tags)) {
        codex_add_to_bundle('Eco-Friendly Bundle', $post_id);
    }
}

/**
 * Add a product to a specific bundle
 *
 * @param string $bundle_name Name of the bundle product
 * @param int $product_id ID of the product to add
 * @return bool Success status
 */
function codex_add_to_bundle($bundle_name, $product_id) {
    $bundle = codex_find_bundle_by_name($bundle_name);

    if (!$bundle) {
        error_log("CodexDominion Auto Bundles: Bundle '{$bundle_name}' not found");
        return false;
    }

    // Get existing bundle items
    $items = get_post_meta($bundle->ID, '_bundle_items', true);

    if (!is_array($items)) {
        $items = [];
    }

    // Check if product is already in bundle
    if (in_array($product_id, $items)) {
        return true; // Already exists
    }

    // Add product to bundle
    $items[] = $product_id;
    $updated = update_post_meta($bundle->ID, '_bundle_items', $items);

    if ($updated) {
        error_log("CodexDominion Auto Bundles: Added product {$product_id} to bundle '{$bundle_name}'");

        // Update bundle modified date to trigger recalculation
        wp_update_post([
            'ID' => $bundle->ID,
            'post_modified' => current_time('mysql'),
            'post_modified_gmt' => current_time('mysql', 1)
        ]);

        return true;
    }

    return false;
}

/**
 * Find a bundle product by name
 *
 * @param string $name Bundle name to search for
 * @return WP_Post|null Bundle post object or null if not found
 */
function codex_find_bundle_by_name($name) {
    // Use transient caching to reduce queries
    $cache_key = 'codex_bundle_' . sanitize_title($name);
    $cached = get_transient($cache_key);

    if ($cached !== false) {
        return get_post($cached);
    }

    $query = new WP_Query([
        'post_type' => 'product',
        's' => $name,
        'exact' => true,
        'posts_per_page' => 1,
        'post_status' => 'publish',
        'meta_query' => [
            'relation' => 'OR',
            [
                'key' => '_is_bundle',
                'value' => 'yes',
                'compare' => '='
            ],
            [
                'key' => '_product_type',
                'value' => 'bundle',
                'compare' => '='
            ]
        ]
    ]);

    if ($query->have_posts()) {
        $bundle = $query->posts[0];
        // Cache for 12 hours
        set_transient($cache_key, $bundle->ID, 12 * HOUR_IN_SECONDS);
        return $bundle;
    }

    return null;
}

/**
 * Remove product from bundle when tags are removed
 */
add_action('set_object_terms', 'codex_maybe_remove_from_bundles', 10, 6);

function codex_maybe_remove_from_bundles($object_id, $terms, $tt_ids, $taxonomy, $append, $old_tt_ids) {
    if ($taxonomy !== 'product_tag' || get_post_type($object_id) !== 'product') {
        return;
    }

    // Check if tags were removed
    if (!empty($old_tt_ids) && !$append) {
        $removed_terms = array_diff($old_tt_ids, $tt_ids);

        if (!empty($removed_terms)) {
            // Trigger re-evaluation of bundle membership
            codex_auto_assign_to_bundles($object_id);
        }
    }
}

/**
 * Admin notice for missing bundles
 */
add_action('admin_notices', 'codex_bundle_admin_notices');

function codex_bundle_admin_notices() {
    $screen = get_current_screen();

    if ($screen && $screen->id === 'edit-product') {
        $expected_bundles = [
            'Christmas Mega Bundle',
            'Homeschool Starter Pack',
            'Homeschool Master Pack',
            'Wedding Printables Mega Bundle',
            'Activity Mega Pack',
            'Coloring Collection Bundle',
            'Multi-Language Bundle',
            'Digital Downloads Complete Pack',
            'Memory Verse Collection',
            'Eco-Friendly Bundle'
        ];

        $missing = [];
        foreach ($expected_bundles as $bundle_name) {
            if (!codex_find_bundle_by_name($bundle_name)) {
                $missing[] = $bundle_name;
            }
        }

        if (!empty($missing)) {
            echo '<div class="notice notice-warning"><p>';
            echo '<strong>CodexDominion Auto Bundles:</strong> The following bundles are not found: ';
            echo implode(', ', $missing);
            echo '</p></div>';
        }
    }
}

/**
 * Clear bundle cache when bundle is updated
 */
add_action('save_post_product', 'codex_clear_bundle_cache', 10, 1);

function codex_clear_bundle_cache($post_id) {
    $is_bundle = get_post_meta($post_id, '_is_bundle', true) === 'yes';

    if ($is_bundle) {
        $title = get_the_title($post_id);
        $cache_key = 'codex_bundle_' . sanitize_title($title);
        delete_transient($cache_key);
    }
}
