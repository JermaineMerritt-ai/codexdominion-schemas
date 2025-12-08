#!/usr/bin/env python3
"""
IONOS Cloud Resource ID Discovery Script
This script helps you find the datacenter_id, server_id, and nic_id needed for firewall configuration.
"""

import ionoscloud
from ionoscloud.rest import ApiException

def get_ionos_resources():
    """Retrieve and display IONOS Cloud resource IDs."""

    print("=" * 80)
    print("IONOS Cloud Resource ID Discovery")
    print("=" * 80)
    print("\nYou need to provide your IONOS API credentials.")
    print("You can create API credentials at: https://dcd.ionos.com/")
    print("Navigate to: Menu > API > Create API Token\n")

    # Get credentials from user
    username = input("Enter IONOS API Username (email or token): ").strip()
    password = input("Enter IONOS API Password (or token secret): ").strip()

    # Configure API client
    configuration = ionoscloud.Configuration(
        username=username,
        password=password
    )

    try:
        # Initialize API clients
        dc_api = ionoscloud.DataCentersApi(ionoscloud.ApiClient(configuration))
        server_api = ionoscloud.ServersApi(ionoscloud.ApiClient(configuration))
        nic_api = ionoscloud.NetworkInterfacesApi(ionoscloud.ApiClient(configuration))

        print("\n" + "=" * 80)
        print("Retrieving Resources...")
        print("=" * 80)

        # Get all datacenters
        datacenters = dc_api.datacenters_get(depth=1)

        if not datacenters.items:
            print("\n⚠️  No datacenters found. Please check your API credentials.")
            return

        print(f"\n✅ Found {len(datacenters.items)} datacenter(s)\n")

        target_ip = "74.208.123.158"
        found_match = False

        for dc in datacenters.items:
            print(f"\n📦 Datacenter: {dc.properties.name}")
            print(f"   ID: {dc.id}")
            print(f"   Location: {dc.properties.location}")

            # Get servers in this datacenter
            try:
                servers = server_api.datacenters_servers_get(datacenter_id=dc.id, depth=2)

                for server in servers.items:
                    print(f"\n   🖥️  Server: {server.properties.name}")
                    print(f"      ID: {server.id}")

                    # Get NICs for this server
                    try:
                        nics = nic_api.datacenters_servers_nics_get(
                            datacenter_id=dc.id,
                            server_id=server.id,
                            depth=2
                        )

                        for nic in nics.items:
                            ips = nic.properties.ips if nic.properties.ips else []
                            print(f"\n      🔌 NIC: {nic.properties.name}")
                            print(f"         ID: {nic.id}")
                            print(f"         IPs: {', '.join(ips) if ips else 'None'}")

                            # Check if this NIC has our target IP
                            if target_ip in ips:
                                found_match = True
                                print(f"\n      🎯 MATCH FOUND! This is your server!")
                                print(f"\n      " + "=" * 60)
                                print(f"      Use these values in ionos-firewall-config.py:")
                                print(f"      " + "=" * 60)
                                print(f"      datacenter_id = '{dc.id}'")
                                print(f"      server_id     = '{server.id}'")
                                print(f"      nic_id        = '{nic.id}'")
                                print(f"      " + "=" * 60)

                            # Show existing firewall rules
                            if hasattr(nic.properties, 'firewall_active') and nic.properties.firewall_active:
                                print(f"         Firewall: Active")
                                if hasattr(nic.entities, 'firewallrules') and nic.entities.firewallrules:
                                    print(f"         Existing Rules:")
                                    for rule in nic.entities.firewallrules.items:
                                        props = rule.properties
                                        port_info = ""
                                        if hasattr(props, 'port_range_start') and props.port_range_start:
                                            if props.port_range_start == props.port_range_end:
                                                port_info = f":{props.port_range_start}"
                                            else:
                                                port_info = f":{props.port_range_start}-{props.port_range_end}"
                                        print(f"           - {props.name}: {props.protocol}{port_info} from {props.source_ip or 'any'}")
                            else:
                                print(f"         Firewall: Inactive or not configured")

                    except ApiException as e:
                        print(f"      ⚠️  Could not retrieve NICs: {e}")

            except ApiException as e:
                print(f"   ⚠️  Could not retrieve servers: {e}")

        if not found_match:
            print(f"\n⚠️  No server found with IP {target_ip}")
            print(f"   The IP might be assigned differently or NAT is in use.")
            print(f"   Check the IONOS control panel to identify your server manually.")

        print("\n" + "=" * 80)
        print("Discovery Complete")
        print("=" * 80 + "\n")

    except ApiException as e:
        print(f"\n❌ API Error: {e}")
        print(f"   Status Code: {e.status}")
        print(f"   Reason: {e.reason}")
        print(f"\n   Please verify your API credentials and try again.")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")

if __name__ == "__main__":
    get_ionos_resources()
