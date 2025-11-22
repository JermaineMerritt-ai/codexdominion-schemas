# 🏛️ NGINX DEPLOYMENT GUIDE FOR AISTORELAB.COM

## 🚀 **Deployment Options for Operational Sovereignty**

### **Option 1: WSL Ubuntu Deployment (Local Development)**

```bash
# 1. Install Nginx (if not already installed)
wsl sudo apt update
wsl sudo apt install nginx -y

# 2. Copy configuration file
wsl sudo cp /mnt/c/Users/JMerr/OneDrive/Documents/.vscode/codex-dominion/nginx-aistorelab.conf /etc/nginx/sites-available/aistorelab.com

# 3. Enable the site
wsl sudo ln -s /etc/nginx/sites-available/aistorelab.com /etc/nginx/sites-enabled/

# 4. Test configuration
wsl sudo nginx -t

# 5. Start and reload Nginx
wsl sudo systemctl start nginx
wsl sudo systemctl reload nginx

# 6. Enable Nginx to start on boot
wsl sudo systemctl enable nginx
```

### **Option 2: Linux Server Deployment (Production)**

```bash
# SSH into your server, then run:

# 1. Install Nginx (Ubuntu/Debian)
sudo apt update
sudo apt install nginx -y

# 2. Upload and copy configuration
sudo cp nginx-aistorelab.conf /etc/nginx/sites-available/aistorelab.com

# 3. Enable the site
sudo ln -s /etc/nginx/sites-available/aistorelab.com /etc/nginx/sites-enabled/

# 4. Test configuration
sudo nginx -t

# 5. Reload Nginx
sudo systemctl reload nginx
```

### **Option 3: Google Cloud Run + Load Balancer (Cloud-Native)**

Since you already have Cloud Run deployed, you can use Google Cloud Load Balancer:

```bash
# 1. Create SSL certificate
gcloud compute ssl-certificates create aistorelab-ssl \
    --domains=aistorelab.com,www.aistorelab.com

# 2. Create backend service pointing to Cloud Run
gcloud compute backend-services create aistorelab-backend \
    --global

# 3. Add Cloud Run as backend
gcloud compute backend-services add-backend aistorelab-backend \
    --global \
    --network-endpoint-group=your-cloud-run-neg \
    --network-endpoint-group-region=us-central1

# 4. Create URL map
gcloud compute url-maps create aistorelab-url-map \
    --default-service=aistorelab-backend

# 5. Create HTTPS proxy
gcloud compute target-https-proxies create aistorelab-https-proxy \
    --url-map=aistorelab-url-map \
    --ssl-certificates=aistorelab-ssl

# 6. Create forwarding rule
gcloud compute forwarding-rules create aistorelab-forwarding-rule \
    --global \
    --target-https-proxy=aistorelab-https-proxy \
    --ports=443
```

## 🔧 **Configuration Files Available**

### **Simple Configuration** (`nginx-aistorelab-simple.conf`)
- Basic HTTP/HTTPS proxy to port 8501
- Minimal headers and SSL setup
- Perfect for development/testing

### **Enhanced Configuration** (`nginx-aistorelab.conf`)  
- Comprehensive security headers
- WebSocket support for Streamlit
- Multiple service routing
- Production-ready optimizations

## 🎯 **Service Requirements**

**Before deploying, ensure you have:**
1. **Streamlit App**: Running on port 8501
2. **SSL Certificates**: Let's Encrypt or custom certificates  
3. **Domain DNS**: aistorelab.com pointing to your server
4. **Firewall Rules**: Ports 80, 443 open

## 🔐 **SSL Certificate Setup**

### **Let's Encrypt (Free SSL)**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificates
sudo certbot --nginx -d aistorelab.com -d www.aistorelab.com

# Auto-renewal (add to crontab)
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### **Custom SSL Certificates**
Update paths in nginx configuration:
```nginx
ssl_certificate /path/to/your/certificate.pem;
ssl_certificate_key /path/to/your/private-key.pem;
```

## 🧪 **Testing Your Deployment**

```bash
# Test Nginx configuration
sudo nginx -t

# Check Nginx status
sudo systemctl status nginx

# View Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Test SSL configuration
curl -I https://aistorelab.com

# Test HTTP redirect
curl -I http://aistorelab.com
```

## 🎯 **Integration with Operational Sovereignty Platform**

Your aistorelab.com domain can serve:
- **Main Interface**: Streamlit dashboard on port 8501
- **API Endpoints**: FastAPI service on port 8080 (via /api/ path)
- **Health Monitoring**: /health endpoint for uptime checks
- **Security**: HTTPS-only with modern TLS protocols

## 🏆 **Recommended Deployment Strategy**

1. **Development**: Use WSL Ubuntu with simple configuration
2. **Staging**: Linux server with enhanced configuration  
3. **Production**: Google Cloud Load Balancer + Cloud Run
4. **Monitoring**: Add CloudFlare for additional security and CDN

**🏛️ STATUS: NGINX CONFIGURATION READY FOR AISTORELAB.COM DEPLOYMENT**

Choose your deployment method based on your infrastructure requirements. All configurations support your operational sovereignty platform with proper SSL and security headers.