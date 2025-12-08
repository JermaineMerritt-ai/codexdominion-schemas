<?php
/**
 * Plugin Name: CodexDominion Subscription Seeder
 * Plugin URI: https://codexdominion.app
 * Description: Creates WooCommerce subscription products on activation
 * Version: 1.0.0
 * Author: CodexDominion
 * Author URI: https://codexdominion.app
 * Text Domain: codex-subscription-seeder
 * Requires at least: 5.8
 * Requires PHP: 7.4
 * WC requires at least: 5.0
 * WC tested up to: 8.0
 *
 * @package CodexDominion\SubscriptionSeeder
 */

defined('ABSPATH') || exit;

/**
 * Create a subscription product
 *
 * @param string $name Product name
 * @param string $price Regular price
 * @param string $interval Subscription period (day, week, month, year)
 * @param int $length Subscription length (0 = indefinite)
 * @return int|WP_Error Product ID or error
 */
function codex_create_subscription($name, $price, $interval = 'month', $length = 0) {
    // Check if WooCommerce is active
    if (!class_exists('WooCommerce')) {
        return new WP_Error('woocommerce_missing', 'WooCommerce is not active');
    }

    // Check if product already exists
    $existing = codex_find_subscription_by_name($name);
    if ($existing) {
        return $existing;
    }

    try {
        // Try to use WC_Product_Subscription if WooCommerce Subscriptions is active
        if (class_exists('WC_Product_Subscription')) {
            $product = new WC_Product_Subscription();
        } else {
            // Fallback to simple product with subscription metadata
            $product = new WC_Product_Simple();
        }

        // Set basic product data
        $product->set_name($name);
        $product->set_regular_price($price);
        $product->set_status('publish');
        $product->set_catalog_visibility('visible');
        $product->set_virtual(true); // Digital products
        $product->set_downloadable(false);

        // Set subscription-specific metadata
        $product->update_meta_data('_subscription_period', $interval);
        $product->update_meta_data('_subscription_length', $length);
        $product->update_meta_data('_subscription_period_interval', 1);
        $product->update_meta_data('_subscription_trial_length', 0);
        $product->update_meta_data('_subscription_sign_up_fee', 0);
        $product->update_meta_data('_subscription_limit', 'no');

        // Add category
        $term = term_exists('Subscriptions', 'product_cat');
        if (!$term) {
            $term = wp_insert_term('Subscriptions', 'product_cat', [
                'description' => 'Recurring subscription products',
                'slug' => 'subscriptions'
            ]);
        }

        if (!is_wp_error($term)) {
            $product->set_category_ids([$term['term_id']]);
        }

        // Save the product
        $product_id = $product->save();

        if ($product_id) {
            error_log("CodexDominion Subscriptions: Created subscription '{$name}' (ID: {$product_id})");
            return $product_id;
        }

        return new WP_Error('creation_failed', 'Failed to create subscription product');

    } catch (Exception $e) {
        error_log("CodexDominion Subscriptions Error: " . $e->getMessage());
        return new WP_Error('exception', $e->getMessage());
    }
}

/**
 * Find subscription by name
 *
 * @param string $name Product name
 * @return int|false Product ID or false
 */
function codex_find_subscription_by_name($name) {
    $query = new WP_Query([
        'post_type' => 'product',
        'title' => $name,
        'posts_per_page' => 1,
        'post_status' => 'any',
        'fields' => 'ids'
    ]);

    return $query->have_posts() ? $query->posts[0] : false;
}

/**
 * Seed subscription products on init
 */
add_action('init', 'codex_seed_subscriptions', 20);

function codex_seed_subscriptions() {
    // Only run once
    if (get_option('codex_subs_seeded')) {
        return;
    }

    // Check if WooCommerce is active
    if (!class_exists('WooCommerce')) {
        return;
    }

    // Create subscription products
    $subscriptions = [
        [
            'name' => 'Kids Bible Monthly',
            'price' => '9.99',
            'interval' => 'month',
            'length' => 0
        ],
        [
            'name' => 'Homeschool Monthly',
            'price' => '19.99',
            'interval' => 'month',
            'length' => 0
        ],
        [
            'name' => 'Wedding Planning Monthly',
            'price' => '14.99',
            'interval' => 'month',
            'length' => 0
        ],
        [
            'name' => 'Premium Coloring Club',
            'price' => '7.99',
            'interval' => 'month',
            'length' => 0
        ],
        [
            'name' => 'Activity Pack Subscription',
            'price' => '12.99',
            'interval' => 'month',
            'length' => 0
        ]
    ];

    $created = [];
    $errors = [];

    foreach ($subscriptions as $sub) {
        $result = codex_create_subscription(
            $sub['name'],
            $sub['price'],
            $sub['interval'],
            $sub['length']
        );

        if (is_wp_error($result)) {
            $errors[] = $sub['name'] . ': ' . $result->get_error_message();
        } else {
            $created[] = $sub['name'];
        }
    }

    // Mark as seeded
    update_option('codex_subs_seeded', 1);
    update_option('codex_subs_created', $created);

    if (!empty($errors)) {
        update_option('codex_subs_errors', $errors);
    }

    // Log results
    if (!empty($created)) {
        error_log("CodexDominion Subscriptions: Created " . count($created) . " subscription products");
    }
    if (!empty($errors)) {
        error_log("CodexDominion Subscriptions Errors: " . implode(', ', $errors));
    }
}

/**
 * Admin notice for subscription creation status
 */
add_action('admin_notices', 'codex_subscription_admin_notices');

function codex_subscription_admin_notices() {
    $screen = get_current_screen();

    if ($screen && ($screen->id === 'plugins' || $screen->id === 'edit-product')) {
        if (get_option('codex_subs_seeded')) {
            $created = get_option('codex_subs_created', []);
            $errors = get_option('codex_subs_errors', []);

            if (!empty($created) && !get_option('codex_subs_notice_dismissed')) {
                echo '<div class="notice notice-success is-dismissible">';
                echo '<p><strong>CodexDominion Subscriptions:</strong> Created ' . count($created) . ' subscription products: ';
                echo implode(', ', $created);
                echo '</p></div>';
            }

            if (!empty($errors)) {
                echo '<div class="notice notice-error is-dismissible">';
                echo '<p><strong>CodexDominion Subscriptions Errors:</strong> ';
                echo implode(' | ', $errors);
                echo '</p></div>';
            }
        }

        // Check if WooCommerce Subscriptions is active
        if (!class_exists('WC_Product_Subscription') && get_option('codex_subs_seeded')) {
            echo '<div class="notice notice-warning">';
            echo '<p><strong>CodexDominion Subscriptions:</strong> WooCommerce Subscriptions plugin not detected. ';
            echo 'Subscription products created as simple products with subscription metadata. ';
            echo 'Install <a href="https://woocommerce.com/products/woocommerce-subscriptions/" target="_blank">WooCommerce Subscriptions</a> for full functionality.</p>';
            echo '</div>';
        }
    }
}

/**
 * Reset seeding (for development/testing)
 */
function codex_reset_subscription_seeding() {
    delete_option('codex_subs_seeded');
    delete_option('codex_subs_created');
    delete_option('codex_subs_errors');
    delete_option('codex_subs_notice_dismissed');
}

// Uncomment to reset on plugin activation (development only)
// register_activation_hook(__FILE__, 'codex_reset_subscription_seeding');

/**
 * Add settings page for manual re-seeding
 */
add_action('admin_menu', 'codex_subscription_menu');

function codex_subscription_menu() {
    add_submenu_page(
        'woocommerce',
        'Subscription Seeder',
        'Subscription Seeder',
        'manage_woocommerce',
        'codex-subscription-seeder',
        'codex_subscription_settings_page'
    );
}

function codex_subscription_settings_page() {
    if (isset($_POST['codex_reseed_subscriptions']) && check_admin_referer('codex_reseed')) {
        codex_reset_subscription_seeding();
        codex_seed_subscriptions();
        echo '<div class="notice notice-success"><p>Subscriptions re-seeded successfully!</p></div>';
    }

    ?>
    <div class="wrap">
        <h1>CodexDominion Subscription Seeder</h1>

        <?php if (get_option('codex_subs_seeded')): ?>
            <div class="card">
                <h2>Status: Seeded ✓</h2>
                <p>Subscription products have been created.</p>

                <?php
                $created = get_option('codex_subs_created', []);
                if (!empty($created)):
                ?>
                    <h3>Created Products:</h3>
                    <ul>
                        <?php foreach ($created as $name): ?>
                            <li><?php echo esc_html($name); ?></li>
                        <?php endforeach; ?>
                    </ul>
                <?php endif; ?>
            </div>
        <?php else: ?>
            <div class="card">
                <h2>Status: Not Seeded</h2>
                <p>Subscription products will be created automatically on next page load.</p>
            </div>
        <?php endif; ?>

        <div class="card">
            <h2>Re-seed Subscriptions</h2>
            <p>Reset and re-create all subscription products. Existing products with the same names will be preserved.</p>

            <form method="post">
                <?php wp_nonce_field('codex_reseed'); ?>
                <button type="submit" name="codex_reseed_subscriptions" class="button button-primary">
                    Re-seed Subscriptions
                </button>
            </form>
        </div>
    </div>
    <?php
}
