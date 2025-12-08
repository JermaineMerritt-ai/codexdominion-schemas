#!/usr/bin/env python3
"""
IONOS Cloud Firewall Configuration Script
Adds HTTP (80) and HTTPS (443) firewall rules to allow external access.
"""

import ionoscloud
from ionoscloud.models import FirewallRule, FirewallRuleProperties
from ionoscloud.rest import ApiException

def configure_firewall():
    """Configure IONOS firewall to allow HTTP and HTTPS traffic."""

    print("=" * 80)
    print("IONOS Cloud Firewall Configuration")
    print("=" * 80)
    print("\n⚠️  Run ionos-get-ids.py first to get your resource IDs!\n")

    # Get API credentials
    username = input("Enter IONOS API Username (email or token): ").strip()
    password = input("Enter IONOS API Password (or token secret): ").strip()

    # Get resource IDs
    print("\nEnter the resource IDs from ionos-get-ids.py output:")
    datacenter_id = input("datacenter_id: ").strip()
    server_id = input("server_id: ").strip()
    nic_id = input("nic_id: ").strip()

    if not all([datacenter_id, server_id, nic_id]):
        print("\n❌ Error: All resource IDs are required!")
        return

    # Configure API client
    configuration = ionoscloud.Configuration(
        username=username,
        password=password
    )
    client = ionoscloud.ApiClient(configuration)
    firewall_api = ionoscloud.FirewallRulesApi(client)

    # Define firewall rules
    rules = [
        {
            "name": "Allow-HTTP",
            "protocol": "TCP",
            "port": 80,
            "description": "Allow incoming HTTP traffic"
        },
        {
            "name": "Allow-HTTPS",
            "protocol": "TCP",
            "port": 443,
            "description": "Allow incoming HTTPS traffic"
        }
    ]

    print("\n" + "=" * 80)
    print("Creating Firewall Rules...")
    print("=" * 80)

    created_rules = []

    for rule_def in rules:
        try:
            print(f"\n📝 Creating rule: {rule_def['name']}")
            print(f"   Protocol: {rule_def['protocol']}")
            print(f"   Port: {rule_def['port']}")
            print(f"   Source: 0.0.0.0/0 (any)")

            firewall_rule = FirewallRule(
                properties=FirewallRuleProperties(
                    name=rule_def['name'],
                    protocol=rule_def['protocol'],
                    source_ip="0.0.0.0/0",
                    port_range_start=rule_def['port'],
                    port_range_end=rule_def['port']
                )
            )

            result = firewall_api.datacenters_servers_nics_firewallrules_post(
                datacenter_id=datacenter_id,
                server_id=server_id,
                nic_id=nic_id,
                firewallrule=firewall_rule
            )

            print(f"   ✅ Rule created successfully!")
            print(f"   Rule ID: {result.id}")
            created_rules.append(rule_def['name'])

        except ApiException as e:
            print(f"   ❌ Failed to create rule: {e}")
            if e.status == 422:
                print(f"   (Rule might already exist)")
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")

    print("\n" + "=" * 80)
    print("Configuration Summary")
    print("=" * 80)

    if created_rules:
        print(f"\n✅ Successfully created {len(created_rules)} firewall rule(s):")
        for rule_name in created_rules:
            print(f"   - {rule_name}")

        print("\n⏳ Firewall rules may take 1-5 minutes to propagate.")
        print("\n📋 Next Steps:")
        print("   1. Wait a few minutes for the rules to become active")
        print("   2. Test: http://74.208.123.158")
        print("   3. Test: http://74.208.123.158/api/health")
        print("   4. Test: http://74.208.123.158/docs")
        print("\n🎉 If successful, your application will be publicly accessible!")
    else:
        print("\n⚠️  No rules were created.")
        print("   - Rules may already exist")
        print("   - Check the IONOS Control Panel manually")
        print("   - Verify your API credentials and resource IDs")

    print("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    try:
        configure_firewall()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user.\n")
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}\n")
