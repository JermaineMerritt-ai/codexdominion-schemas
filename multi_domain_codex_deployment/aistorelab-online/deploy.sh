
#!/bin/bash
# Deployment script for aistorelab.online

echo "🚀 Starting deployment for aistorelab.online"

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y nginx mysql-server redis-server python3 python3-pip git certbot python3-certbot-nginx

# Create deployment directory
sudo mkdir -p /opt/aistorelab-online
cd /opt/aistorelab-online

# Clone repository (if applicable)
# git clone https://github.com/your-repo/aistorelab.online.git .

# Install Python dependencies
pip3 install streamlit plotly pandas numpy scikit-learn

# Configure Nginx
sudo cp nginx.conf /etc/nginx/sites-available/aistorelab.online
sudo ln -sf /etc/nginx/sites-available/aistorelab.online /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Setup SSL
sudo certbot --nginx -d aistorelab.online -d www.aistorelab.online

# Setup database
sudo mysql -e "CREATE DATABASE aistorelab_online_db;"
sudo mysql -e "CREATE USER 'aistorelab_online_user'@'localhost' IDENTIFIED BY 'secure_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON aistorelab_online_db.* TO 'aistorelab_online_user'@'localhost';"

# Setup systemd service
sudo tee /etc/systemd/system/aistorelab-online.service << EOF
[Unit]
Description=aistorelab.online Codex Dominion Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/aistorelab-online
ExecStart=/usr/bin/python3 -m streamlit run main.py --server.port 8500
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable aistorelab-online
sudo systemctl start aistorelab-online

echo "✅ Deployment complete for aistorelab.online"
echo "🌐 Site available at: https://aistorelab.online"
