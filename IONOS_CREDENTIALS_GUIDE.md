# IONOS Cloud Credentials & Resource IDs Guide

## Where to Find Your IONOS Credentials

### 1. **Username & Password**
- Go to: https://dcd.ionos.com/
- Your username is typically your IONOS account email
- Password is your IONOS Cloud account password
- **OR** create an API token at: Account > API Management

### 2. **Datacenter ID**
- Login to IONOS Data Center Designer: https://dcd.ionos.com/
- Navigate to: **Virtual Data Center** (left sidebar)
- Click on your datacenter
- Copy the **UUID** from the URL or datacenter details
- Example: `e1c4c9b0-5c8e-4a9e-9f3e-8d7c6b5a4f3e`

### 3. **Server ID**
- In the same datacenter view
- Click on your server (74.208.123.158)
- Copy the **Server UUID** from the details panel
- Example: `a2b3c4d5-6e7f-8a9b-0c1d-2e3f4a5b6c7d`

### 4. **NIC ID (Network Interface Card)**
- Click on your server
- Go to the **Network** tab
- Find the NIC connected to IP 74.208.123.158
- Copy the **NIC UUID**
- Example: `b3c4d5e6-7f8a-9b0c-1d2e-3f4a5b6c7d8e`

## Quick Commands to Find IDs via IONOS CLI (Alternative)

If you have `ionosctl` CLI installed:

```bash
# List datacenters
ionosctl datacenter list

# List servers in a datacenter
ionosctl server list --datacenter-id <DATACENTER_ID>

# List NICs for a server
ionosctl nic list --datacenter-id <DATACENTER_ID> --server-id <SERVER_ID>
```

## Example Configuration

```powershell
# Replace with YOUR actual values:
$env:IONOS_USERNAME = "your-email@example.com"
$env:IONOS_PASSWORD = "YourActualPassword123!"
$env:IONOS_DATACENTER_ID = "e1c4c9b0-5c8e-4a9e-9f3e-8d7c6b5a4f3e"
$env:IONOS_SERVER_ID = "a2b3c4d5-6e7f-8a9b-0c1d-2e3f4a5b6c7d"
$env:IONOS_NIC_ID = "b3c4d5e6-7f8a-9b0c-1d2e-3f4a5b6c7d8e"

# Run the script
.\ionos-firewall-config.ps1
```

## Security Best Practice

Instead of using your main password, create a dedicated API token:
1. Go to: https://dcd.ionos.com/ → Account → API Management
2. Click **Create Token**
3. Set permissions: **Read & Write**
4. Copy the token and use it as `IONOS_PASSWORD`

## Troubleshooting

- **401 Unauthorized**: Wrong username/password or credentials not set
- **404 Not Found**: Wrong datacenter_id, server_id, or nic_id
- **403 Forbidden**: Insufficient API permissions (need firewall management access)

## Alternative: Use IONOS Web UI

If you prefer not to use the API, you can configure firewall rules manually:
1. Login to: https://dcd.ionos.com/
2. Navigate to your Virtual Data Center
3. Click on your server
4. Go to: **Network** tab → Select NIC → **Firewall Rules**
5. Add rules for ports: 80, 443, 22, 3000, 8001, 8080, 5432, 6379
