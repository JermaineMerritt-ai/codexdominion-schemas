# Google Domains DNS Configuration for CodexDominion.app

**Domain:** CodexDominion.app
**Registrar:** Google Domains
**Multi-Cloud Strategy:** IONOS Primary + Azure Secondary with Geographic Load Balancing

## 🌐 DNS Records Configuration

### Primary Records (Root Domain)

```dns
# A Records - Root Domain
@               A       1h      74.208.123.158      # IONOS Primary Server
@               A       1h      135.237.24.198      # Azure LoadBalancer (Failover)

# AAAA Records (IPv6 - if available)
@               AAAA    1h      [IONOS_IPv6]        # Add when IONOS provides IPv6
@               AAAA    1h      [AZURE_IPv6]        # Add when Azure provides IPv6

# MX Records (Email - Optional)
@               MX      1h      10 mail.codexdominion.app.
```

### WWW Subdomain

```dns
www             CNAME   1h      codexdominion.app.
```

### AI Systems Subdomains (Azure AKS)

```dns
# AI Trinity System - All point to Azure LoadBalancer
jermaine-ai     A       1h      135.237.24.198
dot300-ai       A       1h      135.237.24.198
avatar          A       1h      135.237.24.198

# Alternative CNAME approach
jermaine-ai     CNAME   1h      codexdominion-azure.eastus.cloudapp.azure.com.
dot300-ai       CNAME   1h      codexdominion-azure.eastus.cloudapp.azure.com.
avatar          CNAME   1h      codexdominion-azure.eastus.cloudapp.azure.com.
```

### Dashboard & Admin Subdomains

```dns
# Main Dashboard (IONOS)
dashboard       A       1h      74.208.123.158
admin           A       1h      74.208.123.158
portal          A       1h      74.208.123.158

# API Gateway (Multi-Cloud)
api             A       1h      74.208.123.158      # IONOS Primary
api             A       1h      135.237.24.198      # Azure Secondary
```

### Application Subdomains (IONOS)

```dns
# Analytics Platforms
stockanalytics  A       1h      74.208.123.158
analytics       A       1h      74.208.123.158
data            A       1h      74.208.123.158

# Business Applications
crm             A       1h      74.208.123.158
erp             A       1h      74.208.123.158
store           A       1h      74.208.123.158
```

### Development & Staging

```dns
# Staging Environments
staging         A       1h      74.208.123.158
dev             A       1h      74.208.123.158
test            A       1h      135.237.24.198      # Azure for testing

# CI/CD Webhooks
cicd            A       1h      135.237.24.198
deploy          A       1h      135.237.24.198
```

### Infrastructure Subdomains

```dns
# Monitoring & Observability
grafana         A       1h      135.237.24.198
prometheus      A       1h      135.237.24.198
status          A       1h      74.208.123.158

# Kubernetes Engine Subdomains
engine01        A       1h      135.237.24.198
engine02        A       1h      135.237.24.198
# ... (engine03-engine16 all point to Azure LoadBalancer)
```

### TXT Records (Verification & Security)

```dns
# Domain Verification
@               TXT     1h      "google-site-verification=YOUR_VERIFICATION_CODE"
@               TXT     1h      "v=spf1 include:_spf.google.com ~all"

# DKIM (if using email)
default._domainkey  TXT 1h      "v=DKIM1; k=rsa; p=YOUR_PUBLIC_KEY"

# DMARC Policy
_dmarc          TXT     1h      "v=DMARC1; p=quarantine; rua=mailto:admin@codexdominion.app"

# CAA Records (Certificate Authority Authorization)
@               CAA     1h      0 issue "letsencrypt.org"
@               CAA     1h      0 issuewild "letsencrypt.org"
```

### SRV Records (Optional Services)

```dns
# Kubernetes API (if exposing externally)
_kubernetes._tcp    SRV 1h  10 5 6443 codexdominion-azure.eastus.cloudapp.azure.com.

# Monitoring Services
_prometheus._tcp    SRV 1h  10 5 9090 prometheus.codexdominion.app.
```

## 🔧 Google Domains Configuration Steps

### Step 1: Access DNS Settings

1. Go to **domains.google.com**
2. Click on **CodexDominion.app**
3. Navigate to **DNS** section
4. Select **Custom records**

### Step 2: Add Root Domain Records

```plaintext
Type    Host    Data                    TTL
A       @       74.208.123.158         1h
A       @       135.237.24.198         1h
```

### Step 3: Add Subdomain Records

```plaintext
Type    Host            Data                    TTL
A       jermaine-ai     135.237.24.198         1h
A       dot300-ai       135.237.24.198         1h
A       avatar          135.237.24.198         1h
A       dashboard       74.208.123.158         1h
A       api             74.208.123.158         1h
A       api             135.237.24.198         1h
CNAME   www             codexdominion.app.     1h
```

### Step 4: Add Security Records

```plaintext
Type    Host            Data                                        TTL
CAA     @               0 issue "letsencrypt.org"                  1h
TXT     @               "v=spf1 include:_spf.google.com ~all"      1h
TXT     _dmarc          "v=DMARC1; p=quarantine; rua=mailto:admin@codexdominion.app" 1h
```

## 🌍 Geographic Routing Strategy

### Option 1: Round-Robin DNS (Simple)

- Multiple A records with same hostname
- DNS automatically rotates between IPs
- Client gets different IP on each query
- **Pros:** Simple, no extra services needed
- **Cons:** No health checks, no geographic preference

### Option 2: Google Cloud DNS (Advanced)

1. **Export from Google Domains to Cloud DNS:**
   ```bash
   # Enable Cloud DNS API
   gcloud services enable dns.googleapis.com

   # Create DNS zone
   gcloud dns managed-zones create codexdominion-app \
       --dns-name="codexdominion.app." \
       --description="CodexDominion Multi-Cloud DNS"

   # Update nameservers in Google Domains
   gcloud dns managed-zones describe codexdominion-app
   ```

2. **Configure Routing Policies:**
   ```bash
   # Geographic routing (US traffic to Azure, EU to IONOS)
   gcloud dns record-sets create codexdominion.app. \
       --type=A \
       --ttl=300 \
       --routing-policy-type=GEO \
       --routing-policy-data="us-east1=135.237.24.198;europe-west1=74.208.123.158"
   ```

### Option 3: Cloudflare (Recommended for Production)

1. **Transfer DNS to Cloudflare:**
   - Point CodexDominion.app nameservers to Cloudflare
   - Get free DDoS protection + CDN
   - Use Cloudflare Load Balancer for health checks

2. **Cloudflare Load Balancer Setup:**
   ```yaml
   pools:
     - name: "ionos-primary"
       origins:
         - address: "74.208.123.158"
           weight: 1
     - name: "azure-secondary"
       origins:
         - address: "135.237.24.198"
           weight: 1

   load_balancer:
     default_pools: ["ionos-primary", "azure-secondary"]
     fallback_pool: "azure-secondary"
     region_pools:
       WNAM: ["azure-secondary"]  # North America -> Azure
       EU: ["ionos-primary"]      # Europe -> IONOS
   ```

## 🔐 SSL Certificate Strategy

### Let's Encrypt (Free, Automated)

**IONOS Server:**
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificates for all domains
sudo certbot --nginx -d codexdominion.app \
    -d www.codexdominion.app \
    -d dashboard.codexdominion.app \
    -d api.codexdominion.app \
    -d stockanalytics.codexdominion.app \
    -d analytics.codexdominion.app

# Auto-renewal (already configured)
sudo certbot renew --dry-run
```

**Azure AKS:**
```bash
# Already configured with cert-manager
# Certificates auto-provisioned for:
# - jermaine-ai.codexdominion.app
# - dot300-ai.codexdominion.app
# - avatar.codexdominion.app
```

### Wildcard Certificate (Alternative)

```bash
# Single wildcard cert for all subdomains
sudo certbot certonly --manual \
    --preferred-challenges=dns \
    -d codexdominion.app \
    -d *.codexdominion.app

# Add TXT record when prompted:
# _acme-challenge.codexdominion.app  TXT  "VALIDATION_STRING"
```

## 📊 DNS Propagation & Testing

### Check DNS Propagation

```powershell
# Test from multiple locations
nslookup codexdominion.app 8.8.8.8          # Google DNS
nslookup codexdominion.app 1.1.1.1          # Cloudflare DNS

# Detailed DNS query
Resolve-DnsName codexdominion.app -Type A
Resolve-DnsName jermaine-ai.codexdominion.app -Type A

# Test from external service
# Visit: https://www.whatsmydns.net/#A/codexdominion.app
```

### Verify SSL Certificates

```powershell
# Check SSL for each subdomain
curl -I https://codexdominion.app
curl -I https://jermaine-ai.codexdominion.app
curl -I https://dashboard.codexdominion.app

# Detailed SSL check
openssl s_client -connect codexdominion.app:443 -servername codexdominion.app
```

## 🚀 Quick Setup Commands

### Complete DNS Setup Script

```powershell
# Save as: setup-dns.ps1

$domains = @{
    "@" = @("74.208.123.158", "135.237.24.198")
    "www" = "CNAME:codexdominion.app"
    "jermaine-ai" = "135.237.24.198"
    "dot300-ai" = "135.237.24.198"
    "avatar" = "135.237.24.198"
    "dashboard" = "74.208.123.158"
    "api" = @("74.208.123.158", "135.237.24.198")
    "stockanalytics" = "74.208.123.158"
    "analytics" = "74.208.123.158"
}

Write-Host "🌐 DNS Configuration for CodexDominion.app" -ForegroundColor Cyan
Write-Host "=" * 60
foreach ($host in $domains.Keys) {
    $target = $domains[$host]
    Write-Host "✓ $host -> $target" -ForegroundColor Green
}

Write-Host "`n📋 Manual Steps Required:" -ForegroundColor Yellow
Write-Host "1. Go to domains.google.com"
Write-Host "2. Select CodexDominion.app > DNS"
Write-Host "3. Add above records to Custom records section"
Write-Host "4. Wait 1-48 hours for propagation"
```

## 📈 Monitoring & Maintenance

### Health Check Endpoints

```yaml
# Configure in Google Domains or Cloudflare
health_checks:
  - url: "https://codexdominion.app/health"
    interval: 60s
    timeout: 10s

  - url: "https://jermaine-ai.codexdominion.app/health"
    interval: 60s
    timeout: 10s

  - url: "http://74.208.123.158/health"  # IONOS direct
    interval: 30s

  - url: "http://135.237.24.198/health"  # Azure direct
    interval: 30s
```

### DNS Change Log

| Date | Change | Reason |
|------|--------|--------|
| 2025-12-01 | Initial setup | Multi-cloud deployment |
| TBD | Add IPv6 | Future enhancement |
| TBD | Migrate to Cloudflare | Enhanced load balancing |

---

**Configuration Status:** Ready for implementation
**Estimated Propagation Time:** 1-48 hours
**TTL:** 1 hour (3600 seconds)
**DNSSEC:** Optional (can enable in Google Domains)
