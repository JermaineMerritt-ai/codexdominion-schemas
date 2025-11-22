
#!/bin/bash
# Deployment script for jermaineai.online

echo "🚀 Starting deployment for jermaineai.online"

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y nginx mysql-server redis-server python3 python3-pip git certbot python3-certbot-nginx

# Create deployment directory
sudo mkdir -p /opt/jermaineai-online
cd /opt/jermaineai-online

# Clone repository (if applicable)
# git clone https://github.com/your-repo/jermaineai.online.git .

# Install Python dependencies
pip3 install streamlit plotly pandas numpy scikit-learn

# Configure Nginx
sudo cp nginx.conf /etc/nginx/sites-available/jermaineai.online
sudo ln -sf /etc/nginx/sites-available/jermaineai.online /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Setup SSL
sudo certbot --nginx -d jermaineai.online -d www.jermaineai.online

# Setup database
sudo mysql -e "CREATE DATABASE jermaineai_online_db;"
sudo mysql -e "CREATE USER 'jermaineai_online_user'@'localhost' IDENTIFIED BY 'secure_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON jermaineai_online_db.* TO 'jermaineai_online_user'@'localhost';"

# Setup systemd service
sudo tee /etc/systemd/system/jermaineai-online.service << EOF
[Unit]
Description=jermaineai.online Codex Dominion Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/jermaineai-online
ExecStart=/usr/bin/python3 -m streamlit run main.py --server.port 8500
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable jermaineai-online
sudo systemctl start jermaineai-online

echo "✅ Deployment complete for jermaineai.online"
echo "🌐 Site available at: https://jermaineai.online"
