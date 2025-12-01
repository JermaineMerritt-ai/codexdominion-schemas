#!/usr/bin/env python3
"""
🔥 IONOS Multi-Domain Flame Diagnostics
Checks all domains: themerrittmethod.com and aistorelab.com (production + staging)
"""

import datetime

import requests


def check_domain_status():
    """Check status of all domains and services"""
    print("🔥 === IONOS MULTI-DOMAIN FLAME DIAGNOSTICS ===")
    print(f"🕐 Ceremony Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    domains = [
        {
            "name": "The Merritt Method",
            "url": "https://themerrittmethod.com",
            "expected_port": 9000,
            "type": "WordPress/PHP",
        },
        {
            "name": "Codex Dominion Production",
            "url": "https://aistorelab.com",
            "expected_port": 8501,
            "type": "Streamlit Dashboard",
        },
        {
            "name": "Codex Dominion Staging",
            "url": "https://staging.aistorelab.com",
            "expected_port": 8502,
            "type": "Streamlit Dashboard",
        },
    ]

    for domain in domains:
        print(f"🌐 Checking {domain['name']}...")
        print(f"   URL: {domain['url']}")
        print(
            f"   Expected Backend: {domain['type']} on port {domain['expected_port']}"
        )

        try:
            response = requests.get(domain["url"], timeout=10)
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                print(f"   ✅ {domain['name']} is ONLINE")
            elif response.status_code == 502:
                print(
                    f"   ⚠️  502 Bad Gateway - Backend not responding on port {domain['expected_port']}"
                )
            elif response.status_code == 503:
                print(
                    f"   ⚠️  503 Service Unavailable - Server overloaded or maintenance"
                )
            elif response.status_code == 404:
                print(f"   ⚠️  404 Not Found - Check nginx configuration")
            else:
                print(f"   ⚡ Unexpected status: {response.status_code}")

        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout - Server may be down or slow")
        except requests.exceptions.ConnectionError:
            print(f"   🔌 Connection Error - DNS issue or server down")
        except requests.exceptions.SSLError:
            print(f"   🔒 SSL Error - Certificate issue")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

        print()


def generate_multi_domain_fix():
    """Generate fix commands for all services"""
    print("🛠️  === MULTI-DOMAIN FIX COMMANDS ===")
    print("Run these commands on your IONOS server:")
    print()

    print("# 1. Check all service statuses")
    print("sudo systemctl status nginx")
    print("sudo systemctl status codex-dashboard")
    print("sudo systemctl status codex-staging")
    print("# Check what's running on your WordPress port:")
    print("sudo netstat -tlnp | grep :9000")
    print()

    print("# 2. Check all port usage")
    print("sudo netstat -tlnp | grep -E '(:80|:443|:8501|:8502|:9000)'")
    print()

    print("# 3. Test local backend connections")
    print("curl -I http://127.0.0.1:9000   # WordPress/PHP")
    print("curl -I http://127.0.0.1:8501   # Codex Production")
    print("curl -I http://127.0.0.1:8502   # Codex Staging")
    print()

    print("# 4. Check nginx configuration")
    print("sudo nginx -t")
    print("sudo nginx -T | grep -A5 -B5 'server_name'")
    print()

    print("# 5. Fix Codex Dominion services (if needed)")
    print("sudo systemctl stop codex-dashboard codex-staging")
    print("sudo pkill -f streamlit")
    print("cd /var/www/codex && sudo git pull origin main")
    print("cd /var/www/codex-staging && sudo git pull origin staging")
    print("sudo systemctl start codex-dashboard")
    print("sleep 5")
    print("sudo systemctl start codex-staging")
    print()

    print("# 6. Restart nginx")
    print("sudo systemctl reload nginx")
    print()


def show_expected_ports():
    """Show what should be running on each port"""
    print("📊 === EXPECTED PORT CONFIGURATION ===")
    print()
    print("Port 80:   HTTP (redirects to HTTPS)")
    print("Port 443:  HTTPS nginx (reverse proxy)")
    print("Port 9000: The Merritt Method (WordPress/PHP)")
    print("Port 8501: Codex Dominion Production (Streamlit)")
    print("Port 8502: Codex Dominion Staging (Streamlit)")
    print()
    print("🔥 All domains should show 200 OK status when working properly!")
    print()


if __name__ == "__main__":
    check_domain_status()
    show_expected_ports()
    generate_multi_domain_fix()

    print("🏁 === MULTI-DOMAIN DIAGNOSTICS COMPLETE ===")
    print("If any domains show 502 errors:")
    print("1. Check that the backend service is running on the expected port")
    print("2. Verify nginx configuration matches the backend ports")
    print("3. Check firewall settings: sudo ufw status")
    print("4. Review nginx error logs: sudo tail /var/log/nginx/error.log")
    print("🔥 May all your flames burn eternal across all domains! ✨")
