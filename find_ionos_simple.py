"""
Simple IONOS Resource Finder - Alternative approach using requests
"""
import requests
import json
from requests.auth import HTTPBasicAuth

# Credentials
username = "Jermaine.Bourne36@gmail.com"
password = "Jer48#jer48"
datacenter_id = "7b3fa8e1-d7d7-4646-8005-9f59a8a004fe"

base_url = "https://api.ionos.com/cloudapi/v6"
auth = HTTPBasicAuth(username, password)
headers = {"Content-Type": "application/json"}

print("=" * 70)
print("🔍 Finding IONOS Resources")
print("=" * 70)

# Get servers in datacenter
print(f"\n📡 Fetching servers in datacenter {datacenter_id}...")
servers_url = f"{base_url}/datacenters/{datacenter_id}/servers?depth=2"

try:
    response = requests.get(servers_url, auth=auth, headers=headers)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        servers = data.get('items', [])

        print(f"✅ Found {len(servers)} server(s)\n")

        target_ip = "74.208.123.158"
        found = False

        for server in servers:
            server_id = server['id']
            server_name = server['properties']['name']

            print(f"🖥️  Server: {server_name}")
            print(f"   Server ID: {server_id}")

            # Get NICs for this server
            nics_url = f"{base_url}/datacenters/{datacenter_id}/servers/{server_id}/nics?depth=2"
            nic_response = requests.get(nics_url, auth=auth, headers=headers)

            if nic_response.status_code == 200:
                nic_data = nic_response.json()
                nics = nic_data.get('items', [])

                print(f"   NICs: {len(nics)}")

                for nic in nics:
                    nic_id = nic['id']
                    nic_name = nic['properties']['name']
                    nic_ips = nic['properties'].get('ips', [])

                    print(f"      • {nic_name}")
                    print(f"        NIC ID: {nic_id}")
                    print(f"        IPs: {', '.join(nic_ips) if nic_ips else 'None'}")

                    if target_ip in nic_ips:
                        print(f"\n{'=' * 70}")
                        print(f"🎯 FOUND SERVER WITH IP {target_ip}!")
                        print(f"{'=' * 70}")
                        print(f"\n📋 Copy these commands:\n")
                        print(f'$env:IONOS_USERNAME = "Jermaine.Bourne36@gmail.com"')
                        print(f'$env:IONOS_PASSWORD = "Jer48#jer48"')
                        print(f'$env:IONOS_DATACENTER_ID = "{datacenter_id}"')
                        print(f'$env:IONOS_SERVER_ID = "{server_id}"')
                        print(f'$env:IONOS_NIC_ID = "{nic_id}"')
                        print(f"\nThen run: .\\ionos-firewall-config.ps1")
                        print(f"{'=' * 70}\n")
                        found = True

            print()

        if not found:
            print(f"⚠️  Server with IP {target_ip} not found in this datacenter")

    elif response.status_code == 401:
        print("❌ 401 Unauthorized - Check your credentials")
    elif response.status_code == 404:
        print("❌ 404 Not Found - Datacenter ID may be incorrect")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"❌ Error: {str(e)}")
