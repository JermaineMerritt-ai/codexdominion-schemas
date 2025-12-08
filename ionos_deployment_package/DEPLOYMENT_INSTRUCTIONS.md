# Codex Dominion - IONOS Deployment Instructions

## Server Information
- IP Address: 74.208.123.158
- Domain: CodexDominion.app
- Deployment Directory: /var/www/codexdominion

## Step 1: Upload Files to IONOS Server

### Option A: Using SCP (Recommended)
tar -czf codexdominion-frontend.tar.gz ionos_deployment_package/
scp codexdominion-frontend.tar.gz root@74.208.123.158:/tmp/

### Option B: Using SFTP
sftp root@74.208.123.158
put -r ionos_deployment_package /tmp/
exit

## Step 2: SSH into IONOS Server
ssh root@74.208.123.158

## Step 3: Deploy on Server

### Install Node.js (if not installed)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

### Extract and Setup Application
cd /tmp
tar -xzf codexdominion-frontend.tar.gz
sudo mkdir -p /var/www/codexdominion
sudo cp -r ionos_deployment_package/* /var/www/codexdominion/
sudo chown -R www-data:www-data /var/www/codexdominion
sudo chmod +x /var/www/codexdominion/start.sh

### Setup Systemd Service
sudo cp /var/www/codexdominion/codexdominion.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable codexdominion
sudo systemctl start codexdominion
sudo systemctl status codexdominion

### Setup Nginx
sudo apt-get install -y nginx
sudo cp /var/www/codexdominion/nginx-codexdominion.conf /etc/nginx/sites-available/codexdominion
sudo ln -s /etc/nginx/sites-available/codexdominion /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

## Step 4: Configure DNS
In IONOS DNS Manager:
1. A Record: @ -> 74.208.123.158
2. CNAME: www -> CodexDominion.app

## Step 5: Setup SSL
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d CodexDominion.app -d www.CodexDominion.app

## Verification
curl http://localhost:3000
sudo journalctl -u codexdominion -f
