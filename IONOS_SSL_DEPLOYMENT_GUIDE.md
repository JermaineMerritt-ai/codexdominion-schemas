# IONOS SSL Certificate Deployment Guide
# Commands ready to execute on your IONOS server

## 🚀 Quick Deployment Steps:

### 1. Upload deployment script to IONOS server:
```bash
scp ionos-ssl-deployment.sh user@your-ionos-server.com:/tmp/
```

### 2. Connect to IONOS server and run deployment:
```bash
ssh user@your-ionos-server.com
chmod +x /tmp/ionos-ssl-deployment.sh
sudo /tmp/ionos-ssl-deployment.sh
```

### 3. Verify SSL installation with your requested commands:

```bash
# View certificate details (your exact command)
sudo openssl x509 -in /etc/letsencrypt/live/aistorelab.com/fullchain.pem -text -noout

# Test certificate renewal (your exact command)  
sudo certbot renew --dry-run

# List all certificates (your exact command)
sudo certbot certificates

# Custom monitoring script (bonus command)
cosmic-ssl-status
```

## 🔧 Additional SSL Management Commands:

### Certificate Information:
```bash
# Show certificate expiry date
sudo openssl x509 -in /etc/letsencrypt/live/aistorelab.com/fullchain.pem -noout -enddate

# Show certificate subject and issuer
sudo openssl x509 -in /etc/letsencrypt/live/aistorelab.com/fullchain.pem -noout -subject -issuer

# Verify certificate chain
sudo openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt /etc/letsencrypt/live/aistorelab.com/fullchain.pem
```

### Certificate Renewal Management:
```bash
# Force certificate renewal
sudo certbot renew --force-renewal

# Renew specific certificate
sudo certbot renew --cert-name aistorelab.com

# Show renewal configuration
sudo cat /etc/letsencrypt/renewal/aistorelab.com.conf
```

### Monitoring and Status:
```bash
# Check certbot timer status
sudo systemctl status certbot.timer

# View certbot logs
sudo journalctl -u certbot.timer

# Check nginx SSL configuration
sudo nginx -t && echo "SSL config OK"
```

## 📊 Expected Output After Deployment:

### `sudo openssl x509 -in /etc/letsencrypt/live/aistorelab.com/fullchain.pem -text -noout`
```
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: ...
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = US, O = Let's Encrypt, CN = R3
        Validity
            Not Before: ...
            Not After : ...
        Subject: CN = aistorelab.com
        ...
```

### `sudo certbot renew --dry-run`
```
Saving debug log to /var/log/letsencrypt/letsencrypt.log

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Processing /etc/letsencrypt/renewal/aistorelab.com.conf
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Cert not due for renewal, but simulating renewal for dry run
Simulating renewal of an existing certificate for aistorelab.com and www.aistorelab.com

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Congratulations, all simulated renewals succeeded:
  /etc/letsencrypt/live/aistorelab.com/fullchain.pem (success)
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```

### `sudo certbot certificates`
```
Found the following certs:
  Certificate Name: aistorelab.com
    Domains: aistorelab.com www.aistorelab.com
    Expiry Date: 2026-02-06 12:00:00+00:00 (VALID: 89 days)
    Certificate Path: /etc/letsencrypt/live/aistorelab.com/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/aistorelab.com/privkey.pem
```

### `cosmic-ssl-status`
```
🔒 COSMIC DOMINION SSL STATUS
=============================

📋 Certificate Information:
   Certificate Name: aistorelab.com
   Domains: aistorelab.com www.aistorelab.com
   Expiry Date: 2026-02-06 12:00:00+00:00 (VALID: 89 days)

🔄 Auto-renewal Status:
   ✅ Certbot timer: ACTIVE
   📅 Next check: Sat 2025-11-09 12:00:00 UTC

🌐 Nginx SSL Status:
   ✅ Nginx configuration: VALID
   ✅ Nginx service: RUNNING

🔍 HTTPS Connectivity Test:
   ✅ https://aistorelab.com: ACCESSIBLE
   ✅ https://www.aistorelab.com: ACCESSIBLE

📅 Certificate Expiry Details:
   📆 Expires: Feb  6 12:00:00 2026 GMT
   ⏰ Days remaining: 89
   ✅ Certificate expiry is healthy

🔥 DIGITAL SOVEREIGNTY SSL STATUS COMPLETE! 🔥
```

## 🛡️ Security Features Included:

- ✅ **Let's Encrypt SSL certificates** for aistorelab.com and www.aistorelab.com
- ✅ **Automatic renewal** via systemd timer (every 12 hours)
- ✅ **Nginx reload hooks** after certificate renewal
- ✅ **HTTP to HTTPS redirect** enforced
- ✅ **SSL security headers** configured
- ✅ **Certificate monitoring** with cosmic-ssl-status
- ✅ **Renewal testing** with dry-run capability

## 🔄 Troubleshooting:

### If certificate commands fail:
```bash
# Check if certificates exist
ls -la /etc/letsencrypt/live/aistorelab.com/

# Check nginx configuration
sudo nginx -t

# Check certbot status
sudo systemctl status certbot.timer

# Re-run deployment script
sudo /tmp/ionos-ssl-deployment.sh
```

### Manual certificate installation:
```bash
sudo certbot --nginx -d aistorelab.com -d www.aistorelab.com
```

**All commands are ready to work immediately on your IONOS server!** 🚀🔒