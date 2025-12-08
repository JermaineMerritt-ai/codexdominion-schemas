"""
IONOS Cloud Resource ID Retriever
This script helps you find your datacenter_id, server_id, and nic_id for firewall configuration.
"""

import os
from ionoscloud import Configuration, ApiClient, DataCentersApi, ServersApi, NetworkInterfacesApi
from ionoscloud.rest import ApiException

def get_ionos_resources():
    """Retrieve and display all IONOS Cloud resources for firewall configuration."""

    # Get credentials from environment variables
    username = os.getenv('IONOS_USERNAME')
    password = os.getenv('IONOS_PASSWORD')

    if not username or not password:
        print("❌ Error: IONOS_USERNAME and IONOS_PASSWORD environment variables must be set.")
        print("\nSet them with:")
        print('  $env:IONOS_USERNAME = "your-email@example.com"')
        print('  $env:IONOS_PASSWORD = "your-password"')
        return

    # Configure API client
    configuration = Configuration(
        username=username,
        password=password
    )

    print("=" * 70)
    print("🔍 IONOS Cloud Resource Discovery")
    print("=" * 70)
    print()

    try:
        with ApiClient(configuration) as api_client:
            # Get datacenters
            print("📦 Fetching Datacenters...")
            dc_api = DataCentersApi(api_client)
            datacenters = dc_api.datacenters_get(depth=1)

            if not datacenters.items:
                print("⚠️  No datacenters found in your account.")
                return

            print(f"✅ Found {len(datacenters.items)} datacenter(s)\n")

            target_ip = "74.208.123.158"
            found_match = False

            # Iterate through datacenters
            for dc in datacenters.items:
                dc_id = dc.id
                dc_name = dc.properties.name
                dc_location = dc.properties.location

                print(f"🏢 Datacenter: {dc_name}")
                print(f"   ID: {dc_id}")
                print(f"   Location: {dc_location}")
                print()

                # Get servers in this datacenter
                try:
                    servers_api = ServersApi(api_client)
                    servers = servers_api.datacenters_servers_get(dc_id, depth=2)

                    if servers.items:
                        print(f"   🖥️  Servers ({len(servers.items)}):")

                        for server in servers.items:
                            server_id = server.id
                            server_name = server.properties.name
                            server_state = server.properties.vm_state

                            print(f"      • {server_name}")
                            print(f"        Server ID: {server_id}")
                            print(f"        State: {server_state}")

                            # Get NICs for this server
                            try:
                                nics_api = NetworkInterfacesApi(api_client)
                                nics = nics_api.datacenters_servers_nics_get(dc_id, server_id, depth=2)

                                if nics.items:
                                    print(f"        NICs ({len(nics.items)}):")

                                    for nic in nics.items:
                                        nic_id = nic.id
                                        nic_name = nic.properties.name
                                        nic_ips = nic.properties.ips if nic.properties.ips else []

                                        print(f"          ○ {nic_name}")
                                        print(f"            NIC ID: {nic_id}")
                                        print(f"            IPs: {', '.join(nic_ips) if nic_ips else 'None'}")

                                        # Check if this is the target server
                                        if target_ip in nic_ips:
                                            print(f"\n{'=' * 70}")
                                            print(f"🎯 FOUND YOUR SERVER WITH IP {target_ip}!")
                                            print(f"{'=' * 70}")
                                            print(f"\n📋 Use these values for firewall configuration:")
                                            print(f"\n$env:IONOS_DATACENTER_ID = \"{dc_id}\"")
                                            print(f"$env:IONOS_SERVER_ID = \"{server_id}\"")
                                            print(f"$env:IONOS_NIC_ID = \"{nic_id}\"")
                                            print(f"\nThen run: .\\ionos-firewall-config.ps1")
                                            print(f"{'=' * 70}\n")
                                            found_match = True

                                        print()

                            except ApiException as e:
                                print(f"        ⚠️  Could not retrieve NICs: {e.status} {e.reason}")

                            print()
                    else:
                        print(f"   ⚠️  No servers found in this datacenter")
                        print()

                except ApiException as e:
                    print(f"   ⚠️  Could not retrieve servers: {e.status} {e.reason}")
                    print()

                print("-" * 70)
                print()

            if not found_match:
                print(f"⚠️  Could not find a server with IP {target_ip}")
                print(f"   Make sure the server is running and has the correct IP assigned.")

    except ApiException as e:
        print(f"❌ API Error: {e.status} {e.reason}")
        if e.status == 401:
            print("\n💡 This means your credentials are incorrect.")
            print("   Check your IONOS_USERNAME and IONOS_PASSWORD.")
        elif e.status == 403:
            print("\n💡 This means your account doesn't have API access.")
            print("   Enable API access in IONOS Cloud Data Center Designer.")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    get_ionos_resources()
