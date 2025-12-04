# 🔥 IONOS Direct Deployment via GitHub

## Your IONOS Setup
- **Host**: access-5018657992.webspace-host.com
- **Username**: a3404521
- **Port**: 22
- **Domain**: codexdominion.app

## Option 1: Use IONOS Web Terminal (Easiest)

Since SSH from Windows is restricted, use IONOS's web-based terminal:

### Steps:

1. **Log into IONOS Control Panel**: https://www.ionos.com/login

2. **Navigate to Web Terminal**:
   - Go to **Hosting** → Your webspace package
   - Click **Tools** → **Web Terminal** (or **SSH Access**)
   - This opens a browser-based terminal

3. **Clone Repository** (in Web Terminal):
   ```bash
   cd ~
   git clone https://github.com/JermaineMerritt-ai/codexdominion-schemas.git codexdominion.app
   cd codexdominion.app
   ```

4. **Check Your Environment**:
   ```bash
   # Check Python version (need 3.8+)
   python3 --version

   # Check Node.js version (need 18+)
   node --version

   # Check available commands
   which git python3 node npm
   ```

5. **Frontend is Already Built** (uploaded in repo):
   ```bash
   ls frontend/.next/standalone
   # Should see server.js and pages
   ```

6. **Install Python Dependencies**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

7. **Create Environment File**:
   ```bash
   nano .env.production
   ```

   Add:
   ```env
   DATABASE_URL=mysql://a3404521:YOUR_DB_PASSWORD@localhost/a3404521_db
   API_BASE_URL=https://codexdominion.app/api
   FRONTEND_URL=https://codexdominion.app
   NODE_ENV=production
   PYTHON_ENV=production
   JWT_SECRET=$(openssl rand -hex 32)
   SECRET_KEY=$(openssl rand -hex 32)
   ```

8. **Start Backend API**:
   ```bash
   # Create startup script
   cat > ~/start-api.sh << 'EOF'
   #!/bin/bash
   cd ~/codexdominion.app
   source .venv/bin/activate
   uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 &
   echo $! > ~/api.pid
   EOF

   chmod +x ~/start-api.sh
   ~/start-api.sh
   ```

9. **Configure Web Server**:

   IONOS likely uses Apache. Create `.htaccess` in document root:

   ```bash
   # Find your document root (usually ~/public_html or ~/htdocs)
   nano ~/public_html/.htaccess
   ```

   Add:
   ```apache
   # API Proxy
   RewriteEngine On
   RewriteRule ^api/(.*)$ http://127.0.0.1:8000/$1 [P,L]

   # Frontend static files
   RewriteCond %{REQUEST_FILENAME} !-f
   RewriteRule ^(.*)$ /codexdominion.app/frontend/.next/standalone/$1 [L]

   # Default index
   DirectoryIndex index.html
   ```

10. **Test Deployment**:
    ```bash
    # Test API locally
    curl http://127.0.0.1:8000/health

    # Test frontend
    curl http://localhost
    ```

## Option 2: Contact IONOS Support

If SSH/Web Terminal is not available, contact IONOS support:

**Subject**: Enable SSH/Git Access for CodexDominion.app Deployment

**Message**:
```
Hello,

I need to deploy my application (CodexDominion.app) to my IONOS webspace.

Account: a3404521
Domain: codexdominion.app

Could you please:
1. Enable SSH access or Web Terminal for my account
2. Confirm Python 3.8+ and Node.js 18+ are available
3. Provide instructions for running background processes (uvicorn API server)

The application is ready to deploy from GitHub:
https://github.com/JermaineMerritt-ai/codexdominion-schemas

Thank you!
```

## Option 3: Upgrade to IONOS VPS

If shared hosting limitations prevent deployment:

- **IONOS VPS** (Virtual Private Server) gives you:
  - Full root access
  - SSH access
  - Custom port access (8000 for API)
  - Systemd services
  - Better performance

**Pricing**: Starting at ~$4/month for VPS S

Then you can use the full deployment scripts:
```bash
ssh a3404521@your-vps-ip
git clone https://github.com/JermaineMerritt-ai/codexdominion-schemas.git
cd codexdominion-schemas
# Follow IONOS_SETUP_GUIDE.md
```

## What's Already Done ✅

- ✅ Frontend built and ready (frontend/.next/standalone/)
- ✅ All capsule artifacts created (3 complete systems)
- ✅ ESLint optimized for production
- ✅ Deployment scripts created
- ✅ Server configs ready (nginx, systemd)
- ✅ Code pushed to GitHub
- ✅ 0 critical errors

## Next Action

**Immediate**: Try Option 1 (IONOS Web Terminal) first. If that's not available, contact IONOS support (Option 2).

---

## 📞 IONOS Support Contact

- **Phone**: Check your IONOS dashboard for support number
- **Live Chat**: Available in IONOS control panel
- **Email**: support@ionos.com

**Your deployment is ready to go live!** 🔥
