#!/usr/bin/env python3
"""
IONOS Cloud Firewall Configuration Script
Configures firewall rules for HTTP, HTTPS, SSH, and custom application ports
"""
import os
import sys
import ionoscloud
from ionoscloud.models import FirewallRule, FirewallRuleProperties

def configure_firewall():
    """Configure IONOS firewall rules for web services and application ports"""

    # Get credentials from environment variables
    username = os.getenv("IONOS_USERNAME")
    password = os.getenv("IONOS_PASSWORD")
    datacenter_id = os.getenv("IONOS_DATACENTER_ID")
    server_id = os.getenv("IONOS_SERVER_ID")
    nic_id = os.getenv("IONOS_NIC_ID")

    if not all([username, password, datacenter_id, server_id, nic_id]):
        print("❌ Error: Missing required environment variables:")
        print("   - IONOS_USERNAME")
        print("   - IONOS_PASSWORD")
        print("   - IONOS_DATACENTER_ID")
        print("   - IONOS_SERVER_ID")
        print("   - IONOS_NIC_ID")
        sys.exit(1)

    # Configure API client
    configuration = ionoscloud.Configuration(
        username=username,
        password=password
    )
    client = ionoscloud.ApiClient(configuration)
    firewall_api = ionoscloud.FirewallRulesApi(client)

    # Define comprehensive firewall rules
    rules = [
        # Web Services
        FirewallRule(
            properties=FirewallRuleProperties(
                name="Allow-HTTP",
                protocol="TCP",
                source_ip="0.0.0.0/0",
                port_range_start=80,
                port_range_end=80
            )
        ),
        FirewallRule(
            properties=FirewallRuleProperties(
                name="Allow-HTTPS",
                protocol="TCP",
                source_ip="0.0.0.0/0",
                port_range_start=443,
                port_range_end=443
            )
        ),
        # SSH Access (consider restricting source_ip for production)
        FirewallRule(
            properties=FirewallRuleProperties(
                name="Allow-SSH",
                protocol="TCP",
                source_ip="0.0.0.0/0",
                port_range_start=22,
                port_range_end=22
            )
        ),
        # Next.js Development Server (if needed)
        FirewallRule(
            properties=FirewallRuleProperties(
                name="Allow-Next-Dev",
                protocol="TCP",
                source_ip="0.0.0.0/0",
                port_range_start=3000,
                port_range_end=3000
            )
        ),
        # Backend API Server
        FirewallRule(
            properties=FirewallRuleProperties(
                name="Allow-Backend-API",
                protocol="TCP",
                source_ip="0.0.0.0/0",
                port_range_start=8001,
                port_range_end=8001
            )
        ),
        # Alternative Backend Port
        FirewallRule(
            properties=FirewallRuleProperties(
                name="Allow-Backend-Alt",
                protocol="TCP",
                source_ip="0.0.0.0/0",
                port_range_start=8080,
                port_range_end=8080
            )
        ),
        # Database Access (PostgreSQL - consider restricting)
        FirewallRule(
            properties=FirewallRuleProperties(
                name="Allow-PostgreSQL",
                protocol="TCP",
                source_ip="0.0.0.0/0",
                port_range_start=5432,
                port_range_end=5432
            )
        ),
        # Redis Cache
        FirewallRule(
            properties=FirewallRuleProperties(
                name="Allow-Redis",
                protocol="TCP",
                source_ip="0.0.0.0/0",
                port_range_start=6379,
                port_range_end=6379
            )
        ),
        # ICMP for ping/diagnostics
        FirewallRule(
            properties=FirewallRuleProperties(
                name="Allow-ICMP",
                protocol="ICMP",
                source_ip="0.0.0.0/0",
                icmp_type=8,
                icmp_code=0
            )
        ),
    ]

    print("🔥 Configuring IONOS Cloud Firewall Rules...")
    print(f"   Datacenter: {datacenter_id}")
    print(f"   Server: {server_id}")
    print(f"   NIC: {nic_id}")
    print()

    # Apply rules
    success_count = 0
    error_count = 0

    for rule in rules:
        try:
            firewall_api.datacenters_servers_nics_firewallrules_post(
                datacenter_id=datacenter_id,
                server_id=server_id,
                nic_id=nic_id,
                firewallrule=rule
            )
            print(f"✅ Applied rule: {rule.properties.name}")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed to apply rule {rule.properties.name}: {str(e)}")
            error_count += 1

    print()
    print(f"📊 Summary:")
    print(f"   ✅ Success: {success_count}")
    print(f"   ❌ Errors: {error_count}")
    print()

    if error_count == 0:
        print("🎉 All firewall rules configured successfully!")
        return 0
    else:
        print("⚠️  Some firewall rules failed to apply. Check errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(configure_firewall())
