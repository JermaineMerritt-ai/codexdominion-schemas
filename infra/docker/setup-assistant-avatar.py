#!/usr/bin/env python3
"""
Codex Dominion Setup Assistant Avatar
Interactive AI-powered setup wizard for WordPress, WooCommerce, and system configuration
"""

import os
import sys
import json
import subprocess
import requests
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

class SetupAssistantAvatar:
    """AI-powered setup assistant for Codex Dominion e-commerce platform"""

    def __init__(self):
        self.config = {}
        self.setup_progress = {
            "wordpress_installed": False,
            "woocommerce_installed": False,
            "plugins_activated": False,
            "api_keys_generated": False,
            "webhooks_configured": False,
            "products_seeded": False,
            "bundles_created": False
        }
        self.log_file = "setup-assistant.log"
        # Get repository root (2 levels up from infra/docker)
        self.repo_root = Path(__file__).parent.parent.parent
        self.docker_dir = self.repo_root / "infra" / "docker"

    def log(self, message: str, level: str = "INFO"):
        """Log setup progress"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        with open(self.log_file, "a") as f:
            f.write(log_entry + "\n")

    def greet_user(self):
        """Welcome message from Avatar"""
        print("""
================================================================
    CODEX DOMINION SETUP ASSISTANT AVATAR
================================================================

I'm your AI-powered setup guide. I'll help you:
  * Install & configure WordPress + WooCommerce
  * Activate custom plugins
  * Generate API keys
  * Configure webhooks
  * Seed products & subscriptions
  * Test the complete system

Let's get your e-commerce empire running!
================================================================
        """)

    def check_prerequisites(self) -> bool:
        """Check if Docker and required tools are available"""
        self.log("Checking prerequisites...")

        checks = {
            "docker": "docker --version",
            "docker-compose": "docker-compose --version",
            "curl": "curl --version"
        }

        all_ok = True
        for tool, command in checks.items():
            try:
                result = subprocess.run(
                    command.split(),
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    print(f"[OK] {tool} is installed")
                else:
                    print(f"[X] {tool} not found")
                    all_ok = False
            except Exception as e:
                print(f"[X] {tool} check failed: {e}")
                all_ok = False

        return all_ok

    def check_docker_containers(self) -> Dict[str, bool]:
        """Check which Docker containers are running"""
        self.log("Checking Docker containers status...")

        try:
            result = subprocess.run(
                ["docker-compose", "ps", "--services", "--filter", "status=running"],
                capture_output=True,
                text=True,
                cwd=str(self.docker_dir)
            )
            running_services = result.stdout.strip().split('\n')

            required_services = ["wordpress", "db", "redis", "web", "api", "nginx"]
            status = {}

            for service in required_services:
                status[service] = service in running_services
                symbol = "[OK]" if status[service] else "[X]"
                print(f"{symbol} {service}: {'Running' if status[service] else 'Not running'}")

            return status
        except Exception as e:
            self.log(f"Error checking containers: {e}", "ERROR")
            return {}

    def start_containers(self):
        """Start Docker containers"""
        self.log("Starting Docker containers...")
        print("\n>> Starting infrastructure...")

        try:
            subprocess.run(
                ["docker-compose", "up", "-d", "wordpress", "db", "redis", "nginx"],
                cwd=str(self.docker_dir),
                check=True
            )
            print("[OK] Containers started successfully")
            self.log("Containers started")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"Failed to start containers: {e}", "ERROR")
            return False

    def wait_for_wordpress(self, max_attempts: int = 30) -> bool:
        """Wait for WordPress to be accessible"""
        self.log("Waiting for WordPress to be ready...")
        print("\n>> Waiting for WordPress to start...")

        url = "http://localhost:8080"
        for attempt in range(max_attempts):
            try:
                response = requests.get(url, timeout=3)
                if response.status_code in [200, 302]:
                    print("[OK] WordPress is accessible!")
                    self.log("WordPress is ready")
                    return True
            except requests.exceptions.RequestException:
                pass

            print(f"  Attempt {attempt + 1}/{max_attempts}...", end='\r')
            import time
            time.sleep(2)

        print("\n[X] WordPress did not become accessible")
        return False

    def check_wordpress_installed(self) -> bool:
        """Check if WordPress installation is complete"""
        self.log("Checking WordPress installation status...")

        try:
            # Check if wp-config.php exists
            result = subprocess.run(
                ["docker", "exec", "codex-wordpress", "test", "-f", "/var/www/html/wp-config.php"],
                capture_output=True
            )

            installed = result.returncode == 0
            self.setup_progress["wordpress_installed"] = installed

            if installed:
                print("[OK] WordPress is installed")
            else:
                print("[!] WordPress needs initial setup")
                print("  Visit http://localhost:8080 to complete installation")

            return installed
        except Exception as e:
            self.log(f"Error checking WordPress: {e}", "ERROR")
            return False

    def guide_wordpress_setup(self):
        """Guide user through WordPress installation"""
        print("""
================================================================
         WORDPRESS INSTALLATION GUIDE
================================================================

  1. Open http://localhost:8080 in your browser
  2. Select language: English
  3. Click "Let's go!"
  4. Enter database details:
     Database Name:     codex_db
     Username:          codex_user
     Password:          codex_pass
     Database Host:     db
     Table Prefix:      wp_
  5. Click "Submit" then "Run the installation"
  6. Fill in site information:
     Site Title:        Codex Dominion
     Username:          admin
     Password:          (strong password)
     Email:             your-email@example.com
  7. Click "Install WordPress"

  Press ENTER when installation is complete...
================================================================
        """)
        input()

    def install_woocommerce(self) -> bool:
        """Install WooCommerce plugin via WP-CLI"""
        self.log("Installing WooCommerce...")
        print("\n>> Installing WooCommerce...")

        try:
            # Install WooCommerce
            subprocess.run(
                ["docker", "exec", "codex-wordpress", "wp", "plugin", "install", "woocommerce", "--activate", "--allow-root"],
                check=True
            )

            print("[OK] WooCommerce installed and activated")
            self.setup_progress["woocommerce_installed"] = True
            self.log("WooCommerce installed")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"Failed to install WooCommerce: {e}", "ERROR")
            print("[X] WooCommerce installation failed")
            print("  You can install manually from wp-admin/plugins")
            return False

    def activate_custom_plugins(self) -> bool:
        """Copy and activate custom plugins"""
        self.log("Activating custom plugins...")
        print("\n>> Activating custom plugins...")

        plugins = [
            ("auto-bundles", "codex-auto-bundles"),
            ("subscription-seeder", "codex-subscription-seeder"),
            ("schema-markup", "codex-schema-markup")
        ]

        success = True
        for folder_name, plugin_slug in plugins:
            try:
                # Copy plugin to WordPress container
                source = str(self.repo_root / "wordpress-plugin" / folder_name)
                dest = f"codex-wordpress:/var/www/html/wp-content/plugins/{plugin_slug}"

                subprocess.run(
                    ["docker", "cp", source, dest],
                    check=True
                )

                # Activate plugin
                subprocess.run(
                    ["docker", "exec", "codex-wordpress", "wp", "plugin", "activate", plugin_slug, "--allow-root"],
                    check=True
                )

                print(f"[OK] {plugin_slug} activated")
            except subprocess.CalledProcessError as e:
                self.log(f"Failed to activate {plugin_slug}: {e}", "ERROR")
                print(f"[X] {plugin_slug} activation failed")
                success = False

        self.setup_progress["plugins_activated"] = success
        return success

    def generate_woocommerce_keys(self) -> Optional[Dict[str, str]]:
        """Guide user to generate WooCommerce API keys"""
        print("""
================================================================
         WOOCOMMERCE API KEY GENERATION
================================================================

  1. Log in to WordPress admin (http://localhost:8080)
  2. Go to: WooCommerce -> Settings -> Advanced -> REST API
  3. Click "Add key"
  4. Description: "Codex Dominion API"
  5. User: Select your admin user
  6. Permissions: Read/Write
  7. Click "Generate API key"
  8. Copy the Consumer key and Consumer secret

================================================================
        """)

        print("\nEnter your WooCommerce API credentials:")
        consumer_key = input("Consumer Key: ").strip()
        consumer_secret = input("Consumer Secret: ").strip()

        if consumer_key and consumer_secret:
            # Save to .env file
            env_content = f"""
WC_CONSUMER_KEY={consumer_key}
WC_CONSUMER_SECRET={consumer_secret}
WC_API_URL=http://localhost:8080/wp-json/wc/v3
NEXT_PUBLIC_SITE_URL=http://localhost:3000
"""

            env_file = self.repo_root / "web" / ".env.local"
            env_file.parent.mkdir(parents=True, exist_ok=True)
            with open(env_file, "w") as f:
                f.write(env_content)

            print("[OK] API keys saved to web/.env.local")
            self.setup_progress["api_keys_generated"] = True
            self.log("WooCommerce API keys configured")
            return {"key": consumer_key, "secret": consumer_secret}

        return None

    def configure_webhooks(self) -> bool:
        """Guide user through webhook configuration"""
        print("""
================================================================
         WEBHOOK CONFIGURATION
================================================================

  Follow these steps for EACH webhook:

  1. Go to: WooCommerce -> Settings -> Advanced -> Webhooks
  2. Click "Add webhook"
  3. Configure as follows:

  Webhook 1: Subscription Created
    - Name: Subscription Created
    - Status: Active
    - Topic: Subscription created
    - Delivery URL: http://api:4000/webhooks/wc/subscription
    - Secret: your_secret_here

  Webhook 2: Subscription Renewed
    - Name: Subscription Renewed
    - Topic: Subscription renewed
    - (same URL and secret)

  Repeat for:
    - Subscription cancelled
    - Subscription expired
    - Subscription updated
    - Order completed (URL: /webhooks/wc/order)
    - Order refunded (URL: /webhooks/wc/order)

  See api/docs/webhooks-setup.md for details

  Press ENTER when webhooks are configured...
================================================================
        """)
        input()

        self.setup_progress["webhooks_configured"] = True
        self.log("Webhooks configured")
        return True

    def seed_products(self) -> bool:
        """Trigger subscription seeder plugin"""
        self.log("Seeding subscription products...")
        print("\n>> Creating subscription products...")

        print("""
To seed subscription products:
1. Log in to WordPress admin
2. Go to: Settings -> Codex Subscription Seeder
3. Click "Re-Seed All Subscriptions"
4. This creates 5 subscription plans automatically

Press ENTER when seeding is complete...
        """)
        input()

        self.setup_progress["products_seeded"] = True
        self.log("Products seeded")
        return True

    def run_tests(self) -> bool:
        """Run basic system tests"""
        self.log("Running system tests...")
        print("\n>> Testing system...")

        tests = [
            ("WordPress", "http://localhost:8080"),
            ("API Health", "http://localhost:4000/health"),
            ("Web Frontend", "http://localhost:3000"),
        ]

        all_passed = True
        for name, url in tests:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code in [200, 302]:
                    print(f"[OK] {name} is accessible")
                else:
                    print(f"[!] {name} returned status {response.status_code}")
                    all_passed = False
            except requests.exceptions.RequestException as e:
                print(f"[X] {name} is not accessible: {e}")
                all_passed = False

        return all_passed

    def show_summary(self):
        """Show setup completion summary"""
        print("""
================================================================
              SETUP COMPLETE!
================================================================
        """)

        print("\nSetup Progress:")
        for step, completed in self.setup_progress.items():
            symbol = "[OK]" if completed else "[X]"
            print(f"  {symbol} {step.replace('_', ' ').title()}")

        print("""
>> Access Your System:
  WordPress:  http://localhost:8080/wp-admin
  Website:    http://localhost:3000
  API:        http://localhost:4000
  Grafana:    http://localhost:3001 (admin/admin)

>> Next Steps:
  1. Review playbooks/rollouts/go-live-checklist.md
  2. Test checkout flow
  3. Upload product images
  4. Configure payment gateway (Stripe/PayPal)
  5. Deploy to production when ready

>> Need Help?
  - Documentation: README.md
  - Deployment: playbooks/runbooks/deployment.md
  - Support: support@codexdominion.app
        """)

    def run(self):
        """Run the complete setup wizard"""
        self.greet_user()

        # Prerequisites
        if not self.check_prerequisites():
            print("\n[!] Please install missing prerequisites and try again")
            return

        # Docker containers
        container_status = self.check_docker_containers()
        if not all(container_status.values()):
            response = input("\nStart missing containers? (y/n): ").lower()
            if response == 'y':
                if not self.start_containers():
                    print("Failed to start containers. Please check Docker.")
                    return

        # Wait for WordPress
        if not self.wait_for_wordpress():
            print("WordPress is not accessible. Check Docker logs.")
            return

        # WordPress installation
        if not self.check_wordpress_installed():
            self.guide_wordpress_setup()

            if not self.check_wordpress_installed():
                print("WordPress installation not detected. Please complete it manually.")
                return

        # WooCommerce
        response = input("\nInstall WooCommerce? (y/n): ").lower()
        if response == 'y':
            self.install_woocommerce()

        # Custom plugins
        response = input("\nActivate custom plugins? (y/n): ").lower()
        if response == 'y':
            self.activate_custom_plugins()

        # API keys
        response = input("\nGenerate WooCommerce API keys? (y/n): ").lower()
        if response == 'y':
            self.generate_woocommerce_keys()

        # Webhooks
        response = input("\nConfigure webhooks? (y/n): ").lower()
        if response == 'y':
            self.configure_webhooks()

        # Seed products
        response = input("\nSeed subscription products? (y/n): ").lower()
        if response == 'y':
            self.seed_products()

        # Tests
        print("\n" + "="*60)
        self.run_tests()

        # Summary
        self.show_summary()


if __name__ == "__main__":
    assistant = SetupAssistantAvatar()
    try:
        assistant.run()
    except KeyboardInterrupt:
        print("\n\n[!] Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[X] Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
