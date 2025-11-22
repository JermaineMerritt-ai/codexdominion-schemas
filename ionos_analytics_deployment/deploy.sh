#!/bin/bash
# IONOS Stock Analytics & Data Platform Deployment Script

set -e

echo "Starting IONOS Analytics Platform Deployment..."

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    nginx \
    mysql-server \
    redis-server \
    git \
    curl \
    certbot \
    python3-certbot-nginx

# Create application directory
sudo mkdir -p /opt/analytics-platform
sudo chown ubuntu:ubuntu /opt/analytics-platform

# Create Python virtual environment
cd /opt/analytics-platform
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install \
    streamlit \
    plotly \
    pandas \
    numpy \
    scikit-learn \
    tensorflow \
    yfinance \
    alpha_vantage \
    mysql-connector-python \
    redis \
    fastapi \
    uvicorn \
    celery

# Copy application files
cp /path/to/ai_action_stock_analytics.py .
cp /path/to/advanced_data_analytics_dashboard.py .

# Setup MySQL database
sudo mysql -e "CREATE DATABASE analytics_platform;"
sudo mysql -e "CREATE USER 'analytics'@'localhost' IDENTIFIED BY 'secure_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON analytics_platform.* TO 'analytics'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Import database schema
sudo mysql analytics_platform < init.sql

# Configure Nginx
sudo cp nginx.conf /etc/nginx/sites-available/analytics-platform
sudo ln -sf /etc/nginx/sites-available/analytics-platform /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Setup SSL certificates
sudo certbot --nginx -d stockanalytics.aistorelab.com -d analytics.aistorelab.com

# Install systemd services
sudo cp stock_analytics.service /etc/systemd/system/
sudo cp data_analytics.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable stock_analytics data_analytics
sudo systemctl start stock_analytics data_analytics

# Setup log rotation
sudo tee /etc/logrotate.d/analytics-platform << EOF
/opt/analytics-platform/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    create 644 ubuntu ubuntu
}
EOF

# Setup monitoring with basic health checks
sudo tee /opt/analytics-platform/health_check.sh << EOF
#!/bin/bash
curl -f http://localhost:8515/_stcore/health || systemctl restart stock_analytics
curl -f http://localhost:8516/_stcore/health || systemctl restart data_analytics
EOF

sudo chmod +x /opt/analytics-platform/health_check.sh

# Add to crontab for health monitoring
echo "*/5 * * * * /opt/analytics-platform/health_check.sh" | sudo tee -a /etc/crontab

echo "IONOS Analytics Platform Deployment Complete!"
echo "Stock Analytics: https://stockanalytics.aistorelab.com"
echo "Data Analytics: https://analytics.aistorelab.com"
