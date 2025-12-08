# 🚀 Deploy Codex Dominion to IONOS Hosting

## ✅ Build Status
**Production build completed successfully!**
- 61 pages generated
- All 16 engines operational
- All 6 AI tools ready
- Main dashboard optimized (10.3 kB)

## 📦 Files Ready for Upload

### What to Upload to IONOS:
```
frontend/.next/          (entire folder - 97.1 kB shared + page bundles)
frontend/public/         (static assets)
frontend/package.json
frontend/node_modules/   (or install on server)
```

## 🔧 IONOS Deployment Steps

### Method 1: FTP Upload (Easiest)

1. **Connect via FTP:**
   - Host: `ftp.aistorelab.com` (or your IONOS FTP host)
   - Username: Your IONOS username
   - Password: Your IONOS password
   - Port: 21 (or 22 for SFTP)

2. **Upload Files:**
   ```
   /public_html/
   ├── .next/              (upload entire folder)
   ├── public/             (upload entire folder)
   ├── package.json
   ├── node_modules/       (or install remotely)
   └── server.js           (Node.js server file)
   ```

3. **Set Permissions:**
   - Files: 644
   - Folders: 755
   - Make sure .next folder is readable

### Method 2: SSH Deployment (Recommended)

```bash
# 1. Connect to your IONOS server via SSH
ssh your-username@aistorelab.com

# 2. Navigate to web directory
cd /var/www/vhosts/aistorelab.com/httpdocs/

# 3. Upload your built frontend
# (Use SCP or rsync from local machine)

# From your local machine:
scp -r frontend/.next your-username@aistorelab.com:/var/www/vhosts/aistorelab.com/httpdocs/
scp -r frontend/public your-username@aistorelab.com:/var/www/vhosts/aistorelab.com/httpdocs/
scp frontend/package.json your-username@aistorelab.com:/var/www/vhosts/aistorelab.com/httpdocs/

# 4. On server, install dependencies
npm install --production

# 5. Start the application
npm start
```

### Method 3: Git Deploy

```bash
# 1. On IONOS server
cd /var/www/vhosts/aistorelab.com/httpdocs/
git clone https://github.com/JermaineMerritt-ai/codex-dominion.git
cd codex-dominion/frontend

# 2. Install and build
npm install
npm run build

# 3. Start production server
npm start
```

## ⚙️ IONOS Server Configuration

### 1. Node.js Setup
Ensure IONOS has Node.js installed (v18+):
```bash
node --version  # Should be >= 18.0.0
```

### 2. Process Manager (PM2)
Install PM2 to keep the app running:
```bash
npm install -g pm2
pm2 start npm --name "codex-dominion" -- start
pm2 save
pm2 startup
```

### 3. Nginx Configuration
Create/update nginx config at `/etc/nginx/sites-available/aistorelab.com`:

```nginx
server {
    listen 80;
    server_name aistorelab.com www.aistorelab.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name aistorelab.com www.aistorelab.com;

    ssl_certificate /path/to/ssl/cert.pem;
    ssl_certificate_key /path/to/ssl/key.pem;

    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
ln -s /etc/nginx/sites-available/aistorelab.com /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

### 4. SSL Certificate (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d aistorelab.com -d www.aistorelab.com
```

## 🔐 Environment Variables

Create `.env.production` on server:
```env
NODE_ENV=production
PORT=3001
NEXT_PUBLIC_API_URL=https://api.aistorelab.com
NEXT_PUBLIC_SITE_URL=https://aistorelab.com
```

## 🌐 DNS Configuration

Update DNS records to point to IONOS server:
```
A Record:  aistorelab.com  →  Your-IONOS-Server-IP
A Record:  www.aistorelab.com  →  Your-IONOS-Server-IP
```

## 📊 Verify Deployment

After deployment, test these URLs:
- https://aistorelab.com
- https://aistorelab.com/main-dashboard
- https://aistorelab.com/ai-video-studio
- https://aistorelab.com/automation-studio
- https://aistorelab.com/research-studio
- https://aistorelab.com/creative-studio
- https://aistorelab.com/website-builder
- https://aistorelab.com/ebook-manager

## 🔄 Future Updates

To update the live site:
```bash
# On server
cd /var/www/vhosts/aistorelab.com/httpdocs/codex-dominion/frontend
git pull
npm install
npm run build
pm2 restart codex-dominion
```

## 📱 Mobile Optimization
All pages are responsive and tested for:
- ✅ Desktop (1920px+)
- ✅ Tablet (768px-1024px)
- ✅ Mobile (320px-767px)

## 🎯 Performance Optimizations Applied
- ✅ Static generation for 61 pages
- ✅ Code splitting (97.1 kB base + page bundles)
- ✅ Image optimization
- ✅ CSS minification
- ✅ JavaScript tree-shaking
- ✅ Gzip compression

## 🚨 Troubleshooting

**Port 3001 already in use:**
```bash
lsof -ti:3001 | xargs kill -9
```

**Permission denied:**
```bash
sudo chown -R $USER:$USER /var/www/vhosts/aistorelab.com/
```

**Module not found:**
```bash
rm -rf node_modules package-lock.json
npm install
```

---

## 🎉 Your Sovereign Dashboard is Ready for Production!

**What's Live:**
- 👑 Sovereign Dashboard with 16 Engines
- 👥 Avatar Council (28 AI agents including Claude & Copilot)
- 💰 Commerce Constellation with revenue tracking
- 🎬 AI Video Studio
- ⚡ Automation Studio (500+ integrations)
- 🔬 Research Studio
- 🎨 Creative Studio
- 🚀 Website Builder
- 📚 eBook Manager
- 📊 50+ Additional Dashboards

**Total Build Size:** 97.1 kB shared + optimized page bundles
**Pages Generated:** 61 static pages
**Performance:** Production-optimized

🔥 **Ready to rule the digital realm!** 👑
