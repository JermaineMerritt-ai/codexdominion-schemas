
#!/bin/bash
# Deployment script for jermaineai.store

echo "🚀 Starting deployment for jermaineai.store"

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y nginx mysql-server redis-server python3 python3-pip git certbot python3-certbot-nginx

# Create deployment directory
sudo mkdir -p /opt/jermaineai-store
cd /opt/jermaineai-store

# Clone repository (if applicable)
# git clone https://github.com/your-repo/jermaineai.store.git .

# Install Python dependencies
pip3 install streamlit plotly pandas numpy scikit-learn

# Configure Nginx
sudo cp nginx.conf /etc/nginx/sites-available/jermaineai.store
sudo ln -sf /etc/nginx/sites-available/jermaineai.store /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Setup SSL
sudo certbot --nginx -d jermaineai.store -d www.jermaineai.store

# Setup database
sudo mysql -e "CREATE DATABASE jermaineai_store_db;"
sudo mysql -e "CREATE USER 'jermaineai_store_user'@'localhost' IDENTIFIED BY 'secure_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON jermaineai_store_db.* TO 'jermaineai_store_user'@'localhost';"

# Setup systemd service
sudo tee /etc/systemd/system/jermaineai-store.service << EOF
[Unit]
Description=jermaineai.store Codex Dominion Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/jermaineai-store
ExecStart=/usr/bin/python3 -m streamlit run main.py --server.port 8500
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable jermaineai-store
sudo systemctl start jermaineai-store

echo "✅ Deployment complete for jermaineai.store"
echo "🌐 Site available at: https://jermaineai.store"
