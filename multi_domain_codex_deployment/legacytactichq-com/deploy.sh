
#!/bin/bash
# Deployment script for legacytactichq.com

echo "🚀 Starting deployment for legacytactichq.com"

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y nginx mysql-server redis-server python3 python3-pip git certbot python3-certbot-nginx

# Create deployment directory
sudo mkdir -p /opt/legacytactichq-com
cd /opt/legacytactichq-com

# Clone repository (if applicable)
# git clone https://github.com/your-repo/legacytactichq.com.git .

# Install Python dependencies
pip3 install streamlit plotly pandas numpy scikit-learn

# Configure Nginx
sudo cp nginx.conf /etc/nginx/sites-available/legacytactichq.com
sudo ln -sf /etc/nginx/sites-available/legacytactichq.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Setup SSL
sudo certbot --nginx -d legacytactichq.com -d www.legacytactichq.com

# Setup database
sudo mysql -e "CREATE DATABASE legacytactichq_com_db;"
sudo mysql -e "CREATE USER 'legacytactichq_com_user'@'localhost' IDENTIFIED BY 'secure_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON legacytactichq_com_db.* TO 'legacytactichq_com_user'@'localhost';"

# Setup systemd service
sudo tee /etc/systemd/system/legacytactichq-com.service << EOF
[Unit]
Description=legacytactichq.com Codex Dominion Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/legacytactichq-com
ExecStart=/usr/bin/python3 -m streamlit run main.py --server.port 8500
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable legacytactichq-com
sudo systemctl start legacytactichq-com

echo "✅ Deployment complete for legacytactichq.com"
echo "🌐 Site available at: https://legacytactichq.com"
