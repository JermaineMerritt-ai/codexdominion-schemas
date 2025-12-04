# 🔥 IONOS Webspace Deployment Guide for CodexDominion.app

## IONOS Credentials
- **Host**: access-5018657992.webspace-host.com
- **Username**: a3404521
- **Port**: 22 (SSH/SFTP)
- **Domain**: codexdominion.app

## Deployment Method 1: FTP/SFTP Upload (Recommended)

### Using FileZilla (Windows)

1. **Download FileZilla**: https://filezilla-project.org/download.php?type=client

2. **Connect to IONOS**:
   - Host: `sftp://access-5018657992.webspace-host.com`
   - Username: `a3404521`
   - Password: [Your IONOS password]
   - Port: `22`

3. **Upload Deployment Package**:
   - Navigate to local directory: `C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion`
   - Find file: `codexdominion_20251203_021228.zip`
   - Drag and drop to remote `/` directory

4. **Connect via SSH** (using PuTTY or PowerShell):
   ```bash
   ssh a3404521@access-5018657992.webspace-host.com -p 22
   ```

5. **Extract and Setup**:
   ```bash
   # Check available space
   df -h

   # Extract deployment
   unzip codexdominion_20251203_021228.zip -d ~/codexdominion.app
   cd ~/codexdominion.app

   # Setup Python environment
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## Deployment Method 2: Direct Git Clone

### On IONOS Server (via SSH):

```bash
# Connect to IONOS
ssh a3404521@access-5018657992.webspace-host.com -p 22

# Clone repository
cd ~
git clone https://github.com/JermaineMerritt-ai/codexdominion-schemas.git codexdominion.app
cd codexdominion.app

# Build Frontend
cd frontend
npm install
npm run build
cd ..

# Setup Python Backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run setup guide
cat IONOS_SETUP_GUIDE.md
```

## Deployment Method 3: IONOS Web Hosting Panel

### Using IONOS Control Panel:

1. **Log into IONOS**: https://www.ionos.com/login

2. **Navigate to File Manager**:
   - Go to **Hosting** → Your package
   - Click **File Manager** or **Webspace Explorer**

3. **Upload via Web Interface**:
   - Click **Upload** button
   - Select `codexdominion_20251203_021228.zip`
   - Wait for upload (23.54 MB)

4. **Extract via Web Terminal**:
   - Open **Web Terminal** in IONOS panel
   - Run: `unzip codexdominion_20251203_021228.zip -d codexdominion.app`

## IONOS Webspace Configuration

### Directory Structure:
```
/home/a3404521/
├── codexdominion.app/          # Application root
│   ├── frontend/
│   │   ├── .next/
│   │   └── out/                # Static files
│   ├── src/                    # FastAPI backend
│   ├── codexdominion/          # Python package
│   ├── artifacts/              # Capsules
│   └── .venv/                  # Python virtual env
└── logs/                       # Application logs
```

### Environment Configuration:

Create `.env.production`:
```bash
cat > ~/codexdominion.app/.env.production << 'EOF'
# Database (IONOS provides MySQL, adjust as needed)
DATABASE_URL=mysql://a3404521:password@localhost/a3404521_db

# Application
NODE_ENV=production
PYTHON_ENV=production
API_BASE_URL=https://codexdominion.app/api
FRONTEND_URL=https://codexdominion.app

# Security
JWT_SECRET=$(openssl rand -hex 32)
SECRET_KEY=$(openssl rand -hex 32)
ALLOWED_ORIGINS=https://codexdominion.app,https://www.codexdominion.app

# Logging
LOG_LEVEL=INFO
LOG_DIR=/home/a3404521/logs
EOF
```

### Start FastAPI Backend:

```bash
# Create startup script
cat > ~/start-api.sh << 'EOF'
#!/bin/bash
cd ~/codexdominion.app
source .venv/bin/activate
uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 --workers 2 &
echo $! > ~/api.pid
EOF

chmod +x ~/start-api.sh
~/start-api.sh
```

### Configure Web Server (Apache/Nginx):

IONOS typically uses **Apache** with `.htaccess` for shared hosting.

Create `.htaccess` in document root:
```bash
cat > ~/codexdominion.app/.htaccess << 'EOF'
# Enable Rewrite Engine
RewriteEngine On

# API Proxy (to FastAPI on port 8000)
RewriteRule ^api/(.*)$ http://localhost:8000/$1 [P,L]

# Frontend SPA routing
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ /frontend/out/$1 [L]

# Default to index.html for SPA
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ /frontend/out/index.html [L]

# Security Headers
Header set X-Content-Type-Options "nosniff"
Header set X-Frame-Options "SAMEORIGIN"
Header set X-XSS-Protection "1; mode=block"

# CORS for API
<IfModule mod_headers.c>
  Header set Access-Control-Allow-Origin "https://codexdominion.app"
  Header set Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"
  Header set Access-Control-Allow-Headers "Content-Type, Authorization"
</IfModule>

# Compression
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/javascript application/javascript application/json
</IfModule>
EOF
```

## DNS Configuration for CodexDominion.app

In IONOS Domain Control Panel:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | 74.208.123.158 | 3600 |
| A | www | 74.208.123.158 | 3600 |
| CNAME | api | access-5018657992.webspace-host.com | 3600 |

## SSL Certificate Setup

IONOS provides free SSL certificates:

1. **Enable in Control Panel**:
   - Go to **Domains & SSL** → codexdominion.app
   - Click **Manage SSL**
   - Select **Free SSL Certificate (Let's Encrypt)**
   - Click **Activate**

2. **Verify HTTPS**:
   ```bash
   curl -I https://codexdominion.app
   ```

## Testing Deployment

### Test Backend:
```bash
curl http://localhost:8000/health
```

### Test Frontend:
```bash
curl https://codexdominion.app
```

### Check Logs:
```bash
tail -f ~/logs/api.log
tail -f ~/logs/error.log
```

## Troubleshooting IONOS SSH Connection

If SSH is not responding:

### Option A: Use IONOS Web Terminal
1. Log into IONOS Control Panel
2. Navigate to **Hosting** → Your package
3. Click **Web Terminal** or **SSH Access**
4. Execute commands directly in browser

### Option B: Check SSH Access Settings
1. In IONOS panel, go to **SSH Access**
2. Ensure SSH is **enabled** for your package
3. Verify username is `a3404521`
4. Reset password if needed

### Option C: Alternative SSH Command
```powershell
# Try with explicit identity
ssh -v a3404521@access-5018657992.webspace-host.com -p 22

# Or use PuTTY on Windows
# Host: access-5018657992.webspace-host.com
# Port: 22
# Username: a3404521
```

## Quick Start Command Sequence

Once SSH is working:

```bash
# 1. Connect
ssh a3404521@access-5018657992.webspace-host.com -p 22

# 2. Upload via SFTP (in another terminal)
# Use FileZilla or WinSCP to upload codexdominion_20251203_021228.zip

# 3. On server, extract
cd ~
unzip codexdominion_20251203_021228.zip -d codexdominion.app
cd codexdominion.app

# 4. Setup environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 5. Configure environment
cp .env.production.example .env.production
nano .env.production  # Edit with your settings

# 6. Start backend
uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 --workers 2 &

# 7. Configure Apache
nano .htaccess  # Use content from above

# 8. Test
curl http://localhost:8000/health
curl https://codexdominion.app
```

## IONOS Package Limitations

IONOS shared hosting may have restrictions:

- **Python Version**: Check `python3 --version` (may need to request specific version)
- **Node.js Version**: Check `node --version` (may be limited)
- **Background Processes**: May need to use cron jobs instead of systemd
- **Port Access**: Port 8000 may need to be configured via IONOS panel
- **Database**: MySQL provided, PostgreSQL may need upgrade

### Upgrade to VPS if Needed:

If shared hosting limitations are an issue, consider:
- **IONOS VPS**: Full root access, custom services
- **Docker support**: Full container deployment
- **Systemd services**: Proper service management

Contact IONOS support for package capabilities.

---

## 🔥 Next Steps

1. **Upload via FileZilla/SFTP**: Easiest method for 23.54 MB file
2. **Connect via SSH**: Use Web Terminal if SSH hangs
3. **Follow setup commands**: Extract, install, configure
4. **Enable SSL**: Use IONOS free Let's Encrypt certificate
5. **Configure DNS**: Point codexdominion.app to IONOS server
6. **Test deployment**: Verify both frontend and API work

**Need help with FileZilla setup?** Let me know!

✨ **CodexDominion.app is almost live!** ✨
