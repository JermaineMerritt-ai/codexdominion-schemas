# DNS Configuration Quick Reference
# CodexDominion.app

## Current Status
❌ **No A records configured** - Domain exists but not pointing to any server

## Required DNS Records

### A Records (all point to your IONOS server IP)
```
Type    Name            Value                   TTL
A       @               YOUR_IONOS_SERVER_IP    3600
A       www             YOUR_IONOS_SERVER_IP    3600
A       api             YOUR_IONOS_SERVER_IP    3600
A       monitoring      YOUR_IONOS_SERVER_IP    3600
A       dashboard       YOUR_IONOS_SERVER_IP    3600
```

### CNAME Records
```
Type    Name    Value               TTL
CNAME   *       codexdominion.app   3600
```

## How to Get Your IONOS Server IP

### Method 1: IONOS Dashboard
1. Log in to https://my.ionos.com
2. Go to **Hosting** or **Server & Cloud**
3. Find your server details
4. Copy the public IP address

### Method 2: SSH into Server
```bash
ssh root@YOUR_SERVER_IP
curl ifconfig.me
# or
hostname -I
```

## DNS Configuration Steps

### Option 1: Google Domains
1. Go to https://domains.google.com
2. Click on **codexdominion.app**
3. Click **DNS** in the left menu
4. Click **Manage custom records**
5. Add each A record:
   - Click **Create new record**
   - Host name: `@` (for root), `www`, `api`, `monitoring`, `dashboard`
   - Type: `A`
   - TTL: `3600`
   - Data: `YOUR_IONOS_SERVER_IP`
6. Add CNAME record:
   - Host name: `*`
   - Type: `CNAME`
   - TTL: `3600`
   - Data: `codexdominion.app`
7. Click **Save**

### Option 2: Cloudflare (if using Cloudflare)
1. Go to https://dash.cloudflare.com
2. Select **codexdominion.app**
3. Go to **DNS** → **Records**
4. Click **Add record** for each A record
5. Add the CNAME record for wildcard subdomain

### Option 3: Terraform (Automated - Cloudflare only)
```powershell
cd c:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion-terraform\

# Edit main.tf and update the IP address on line 28
# Then run:
terraform init
terraform plan
terraform apply
```

## Verify DNS Configuration

### Check DNS Resolution
```powershell
# Check root domain
Resolve-DnsName codexdominion.app -Type A -Server 8.8.8.8

# Check www subdomain
Resolve-DnsName www.codexdominion.app -Type A -Server 8.8.8.8

# Check api subdomain
Resolve-DnsName api.codexdominion.app -Type A -Server 8.8.8.8

# Check monitoring subdomain
Resolve-DnsName monitoring.codexdominion.app -Type A -Server 8.8.8.8
```

### Expected Result (after propagation)
```
Name                        Type   TTL   Section    IPAddress
----                        ----   ---   -------    ---------
codexdominion.app           A      3600  Answer     YOUR_IONOS_SERVER_IP
```

## DNS Propagation Time
- **Typical**: 5-30 minutes
- **Maximum**: Up to 48 hours (rare)
- **Check Status**: https://www.whatsmydns.net/#A/codexdominion.app

## Troubleshooting

### Issue: SOA record only, no A records
**Cause**: DNS records not configured yet
**Solution**: Add A records as described above

### Issue: DNS not resolving after 1 hour
**Check**:
1. Verify records are saved in DNS provider
2. Check for typos in IP address
3. Ensure TTL is not too high (use 3600 or lower)
4. Try flushing local DNS cache: `ipconfig /flushdns`

### Issue: Some subdomains work, others don't
**Check**:
1. Verify all A records are added
2. Check wildcard CNAME is configured
3. Ensure no conflicting records exist

## After DNS is Working

### 1. Test HTTP Access
```powershell
curl http://codexdominion.app
curl http://api.codexdominion.app/health
```

### 2. Set Up SSL Certificates
```bash
# SSH into IONOS server
ssh root@YOUR_SERVER_IP

# Install Certbot (if not installed)
apt-get install -y certbot python3-certbot-nginx

# Obtain SSL certificates
certbot certonly --nginx \
    -d codexdominion.app \
    -d www.codexdominion.app \
    -d api.codexdominion.app \
    -d monitoring.codexdominion.app \
    -d dashboard.codexdominion.app \
    --email jermaine@codexdominion.app \
    --agree-tos \
    --non-interactive

# Auto-renewal (already set up by certbot)
certbot renew --dry-run
```

### 3. Verify SSL
```powershell
curl https://codexdominion.app
curl https://api.codexdominion.app/health
```

## Quick Setup Script
Run the interactive setup script:
```powershell
.\setup-dns.ps1
```

## Support Resources
- **IONOS Support**: https://www.ionos.com/help/
- **Google Domains**: https://support.google.com/domains
- **Cloudflare Docs**: https://developers.cloudflare.com/dns/
- **DNS Checker**: https://dnschecker.org/

---

**Last Updated**: December 5, 2025
**Status**: ❌ DNS not configured - needs A records
**Next Action**: Add A records pointing to IONOS server IP
