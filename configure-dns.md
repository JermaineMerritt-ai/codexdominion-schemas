# DNS Configuration Guide for Codex Dominion

## 📋 Required DNS Records

### 1. Root Domain (codexdominion.app)
```
Type: CNAME or ALIAS
Name: @ (or leave blank, depending on provider)
Value: mango-wave-0fcc4e40f.3.azurestaticapps.net
TTL: 3600 (1 hour)
```

**Note:** Some DNS providers don't allow CNAME on root domains. In that case:
- Use ALIAS record (if supported by provider like Cloudflare, DNSimple)
- Or use ANAME/CNAME flattening feature
- Or configure www as primary and redirect root

### 2. API Subdomain (api.codexdominion.app)
```
Type: CNAME
Name: api
Value: codex-backend-api.eastus2.azurecontainer.io
TTL: 3600 (1 hour)
```

---

## 🌐 Configuration by Provider

### **Cloudflare:**
1. Log in to Cloudflare dashboard
2. Select domain: codexdominion.app
3. Go to DNS → Records
4. Add Record 1:
   - Type: CNAME
   - Name: @ (or codexdominion.app)
   - Target: mango-wave-0fcc4e40f.3.azurestaticapps.net
   - Proxy status: DNS only (gray cloud)
   - TTL: Auto
5. Add Record 2:
   - Type: CNAME
   - Name: api
   - Target: codex-backend-api.eastus2.azurecontainer.io
   - Proxy status: DNS only (gray cloud)
   - TTL: Auto
6. Save

### **Google Domains:**
1. Go to dns.google.com
2. Select: codexdominion.app
3. DNS → Manage Custom Records
4. Add Record 1:
   - Host name: @ (or leave blank)
   - Type: CNAME
   - TTL: 3600
   - Data: mango-wave-0fcc4e40f.3.azurestaticapps.net
5. Add Record 2:
   - Host name: api
   - Type: CNAME
   - TTL: 3600
   - Data: codex-backend-api.eastus2.azurecontainer.io

### **Namecheap:**
1. Log in to Namecheap
2. Domain List → Manage (codexdominion.app)
3. Advanced DNS
4. Add New Record:
   - Type: CNAME Record
   - Host: @
   - Value: mango-wave-0fcc4e40f.3.azurestaticapps.net
   - TTL: Automatic
5. Add New Record:
   - Type: CNAME Record
   - Host: api
   - Value: codex-backend-api.eastus2.azurecontainer.io
   - TTL: Automatic

### **GoDaddy:**
1. My Products → DNS
2. Select: codexdominion.app
3. Add (CNAME):
   - Name: @
   - Value: mango-wave-0fcc4e40f.3.azurestaticapps.net
   - TTL: 1 Hour
4. Add (CNAME):
   - Name: api
   - Value: codex-backend-api.eastus2.azurecontainer.io
   - TTL: 1 Hour

---

## ✅ Verification Steps

### 1. Check DNS Propagation (5-30 minutes)
```powershell
# Check root domain
nslookup codexdominion.app 8.8.8.8

# Check API subdomain
nslookup api.codexdominion.app 8.8.8.8

# Expected output should show the CNAME targets
```

### 2. Use Online Tools
- https://dnschecker.org/#CNAME/codexdominion.app
- https://dnschecker.org/#CNAME/api.codexdominion.app

### 3. Test with dig (if available)
```bash
dig codexdominion.app CNAME
dig api.codexdominion.app CNAME
```

---

## 🔐 After DNS Propagates

### 1. Bind Custom Domain to Azure Static Web App
```powershell
# Root domain
az staticwebapp hostname set `
  --name "codex-sovereign-bridge" `
  --resource-group "codex-dominion-rg" `
  --hostname "codexdominion.app"

# If DNS validation fails, try without www first
```

### 2. Verify SSL Certificate
SSL certificates auto-generate via Let's Encrypt (5-10 minutes after binding).

Check status:
```powershell
az staticwebapp hostname show `
  --name "codex-sovereign-bridge" `
  --resource-group "codex-dominion-rg" `
  --hostname "codexdominion.app"
```

### 3. Test HTTPS Access
```powershell
# Test root domain
Invoke-RestMethod -Uri "https://codexdominion.app"

# Test API endpoint
Invoke-RestMethod -Uri "https://api.codexdominion.app/health"
```

---

## 🚨 Common Issues

### Issue: "CNAME not allowed on apex domain"
**Solution:** Use ALIAS record or contact DNS provider support

### Issue: DNS not propagating
**Solution:**
- Wait 30-60 minutes
- Clear local DNS cache: `ipconfig /flushdns`
- Check with multiple DNS servers: `nslookup codexdominion.app 1.1.1.1`

### Issue: SSL certificate not generating
**Solution:**
- Verify DNS is fully propagated
- Remove and re-add custom domain in Azure
- Check Azure portal for certificate status

---

## 📞 Need Help?

Run verification script: `.\verify-dns-setup.ps1`

Check deployment status: `.\check-deployment-status.ps1`

View Azure portal: [Resource Group](https://portal.azure.com/#@/resource/subscriptions/054bb0e0-6e79-403f-b3fc-39a28d61e9c9/resourceGroups/codex-dominion-rg/overview)
