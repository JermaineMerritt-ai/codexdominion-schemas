
#!/bin/bash
# Deployment script for jermaineai.com

echo "🚀 Starting deployment for jermaineai.com"

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y nginx mysql-server redis-server python3 python3-pip git certbot python3-certbot-nginx

# Create deployment directory
sudo mkdir -p /opt/jermaineai-com
cd /opt/jermaineai-com

# Clone repository (if applicable)
# git clone https://github.com/your-repo/jermaineai.com.git .

# Install Python dependencies
pip3 install streamlit plotly pandas numpy scikit-learn

# Configure Nginx
sudo cp nginx.conf /etc/nginx/sites-available/jermaineai.com
sudo ln -sf /etc/nginx/sites-available/jermaineai.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Setup SSL
sudo certbot --nginx -d jermaineai.com -d www.jermaineai.com

# Setup database
sudo mysql -e "CREATE DATABASE jermaineai_com_db;"
sudo mysql -e "CREATE USER 'jermaineai_com_user'@'localhost' IDENTIFIED BY 'secure_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON jermaineai_com_db.* TO 'jermaineai_com_user'@'localhost';"

# Setup systemd service
sudo tee /etc/systemd/system/jermaineai-com.service << EOF
[Unit]
Description=jermaineai.com Codex Dominion Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/jermaineai-com
ExecStart=/usr/bin/python3 -m streamlit run main.py --server.port 8500
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable jermaineai-com
sudo systemctl start jermaineai-com

echo "✅ Deployment complete for jermaineai.com"
echo "🌐 Site available at: https://jermaineai.com"
