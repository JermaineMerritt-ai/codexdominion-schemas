
#!/bin/bash
# Deployment script for themerrittmethod.com

echo "🚀 Starting deployment for themerrittmethod.com"

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y nginx mysql-server redis-server python3 python3-pip git certbot python3-certbot-nginx

# Create deployment directory
sudo mkdir -p /opt/themerrittmethod-com
cd /opt/themerrittmethod-com

# Clone repository (if applicable)
# git clone https://github.com/your-repo/themerrittmethod.com.git .

# Install Python dependencies
pip3 install streamlit plotly pandas numpy scikit-learn

# Configure Nginx
sudo cp nginx.conf /etc/nginx/sites-available/themerrittmethod.com
sudo ln -sf /etc/nginx/sites-available/themerrittmethod.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Setup SSL
sudo certbot --nginx -d themerrittmethod.com -d www.themerrittmethod.com

# Setup database
sudo mysql -e "CREATE DATABASE themerrittmethod_com_db;"
sudo mysql -e "CREATE USER 'themerrittmethod_com_user'@'localhost' IDENTIFIED BY 'secure_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON themerrittmethod_com_db.* TO 'themerrittmethod_com_user'@'localhost';"

# Setup systemd service
sudo tee /etc/systemd/system/themerrittmethod-com.service << EOF
[Unit]
Description=themerrittmethod.com Codex Dominion Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/themerrittmethod-com
ExecStart=/usr/bin/python3 -m streamlit run main.py --server.port 8500
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable themerrittmethod-com
sudo systemctl start themerrittmethod-com

echo "✅ Deployment complete for themerrittmethod.com"
echo "🌐 Site available at: https://themerrittmethod.com"
