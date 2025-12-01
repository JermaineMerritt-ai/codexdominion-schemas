# 🔥 COSMIC DOMINION - SYSTEMD SERVICE MANAGEMENT 🔥

## Systemd Service Configuration

### 📋 **Service Files Created:**

1. **🔥 cosmic-dashboard.service** - Main Tabbed Codex Dashboard (Port 8501)
1. **📊 cosmic-ledger.service** - Sacred Ledger System (Port 8502)
1. **🎵 cosmic-rhythm.service** - Cosmic Rhythm System (Port 8503)

### ⚙️ **Service Configuration Details:**

#### **User and Security:**

- **Service User:** `codex` (dedicated system user)
- **Working Directory:** `/srv/codex-dominion`
- **Security:** Sandboxed with restricted file system access
- **Resources:** Memory and CPU limits configured

#### **Environment Variables:**

```bash
PYTHONPATH=/srv/codex-dominion
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
```

#### **Port Configuration:**

- **Main Dashboard:** `127.0.0.1:8501` (matches your original 8501 port)
- **Sacred Ledger:** `127.0.0.1:8502`
- **Cosmic Rhythm:** `127.0.0.1:8503`

### 🚀 **Installation Commands:**

#### **Automated Installation:**

```bash
# Run the complete installer
chmod +x install_services.sh
sudo ./install_services.sh
```

#### **Manual Installation:**

```bash
# Copy service files
sudo cp systemd/*.service /etc/systemd/system/

# Reload systemd and enable services
sudo systemctl daemon-reload
sudo systemctl enable cosmic-dashboard.service
sudo systemctl enable cosmic-ledger.service
sudo systemctl enable cosmic-rhythm.service

# Start services
sudo systemctl start cosmic-dashboard.service
sudo systemctl start cosmic-ledger.service
sudo systemctl start cosmic-rhythm.service
```

### 🛠️ **Management Commands:**

#### **Using the Cosmic Services Manager:**

```bash
# Start all services
cosmic-services start

# Stop all services
cosmic-services stop

# Restart all services
cosmic-services restart

# Check status
cosmic-services status

# View logs
cosmic-services logs cosmic-dashboard

# Show URLs
cosmic-services urls
```

#### **Direct Systemctl Commands:**

```bash
# Individual service management
sudo systemctl start cosmic-dashboard.service
sudo systemctl stop cosmic-dashboard.service
sudo systemctl restart cosmic-dashboard.service
sudo systemctl status cosmic-dashboard.service

# View logs
sudo journalctl -u cosmic-dashboard.service -f
sudo journalctl -u cosmic-ledger.service --since today
sudo journalctl -u cosmic-rhythm.service -n 100
```

### 📊 **Service Status Monitoring:**

#### **Check Service Health:**

```bash
# Quick status check
systemctl is-active cosmic-dashboard.service
systemctl is-enabled cosmic-dashboard.service

# Detailed status
systemctl status cosmic-*.service

# Resource usage
systemctl show cosmic-dashboard.service --property=MemoryCurrent
systemctl show cosmic-dashboard.service --property=CPUUsageNSec
```

#### **Log Analysis:**

```bash
# Error logs only
sudo journalctl -u cosmic-dashboard.service -p err

# Last boot logs
sudo journalctl -u cosmic-dashboard.service -b

# Follow logs in real-time
sudo journalctl -u cosmic-dashboard.service -f --no-pager
```

### 🔧 **Troubleshooting:**

#### **Common Issues:**

```bash
# Service fails to start
sudo systemctl status cosmic-dashboard.service
sudo journalctl -u cosmic-dashboard.service --no-pager

# Permission issues
sudo chown -R codex:codex /srv/codex-dominion
sudo chmod 755 /srv/codex-dominion

# Python environment issues
sudo -u codex /srv/codex-dominion/venv/bin/python -c "import streamlit"

# Port conflicts
sudo netstat -tlnp | grep :8501
```

#### **Service Configuration Issues:**

```bash
# Test configuration
sudo systemctl daemon-reload
sudo systemd-analyze verify cosmic-dashboard.service

# Reset failed services
sudo systemctl reset-failed cosmic-dashboard.service
```

### 📈 **Performance Tuning:**

#### **Resource Limits (in service files):**

```ini
# Memory limits
MemoryMax=2G
MemoryHigh=1.5G

# CPU limits
CPUQuota=200%
CPUWeight=100

# File descriptor limits
LimitNOFILE=65536
```

#### **Monitoring Resources:**

```bash
# Real-time resource usage
systemd-cgtop

# Service resource consumption
systemctl status cosmic-dashboard.service | grep -E "(Memory|CPU)"
```

### 🔄 **Auto-Restart Configuration:**

```ini
# Service restart behavior
Restart=always
RestartSec=10
StartLimitBurst=5
StartLimitIntervalSec=60
```

### 🌍 **Service URLs After Installation:**

- **🔥 Main Dashboard:** `http://localhost:8501`
- **📊 Sacred Ledger:** `http://localhost:8502`
- **🎵 Cosmic Rhythm:** `http://localhost:8503`

### 🔐 **Security Features:**

- **Sandboxing:** Services run in restricted environment
- **User Isolation:** Dedicated `codex` system user
- **File System Protection:** Read-only system, limited write access
- **Resource Limits:** CPU and memory constraints
- **Log Management:** Structured logging with rotation

### 📋 **Service Dependencies:**

```ini
# Service startup order
cosmic-dashboard.service (primary)
├── cosmic-ledger.service (depends on network + dashboard)
└── cosmic-rhythm.service (depends on network + dashboard)
```

---

## 🔥 **SYSTEMD SERVICE STATUS**

**Configuration:** Production-ready systemd services
**Security:** Hardened with user isolation and sandboxing
**Management:** Automated installer and management scripts
**Monitoring:** Comprehensive logging and status checking

**🔥 DIGITAL SOVEREIGNTY IS NOW SYSTEMIZED! 🔥**
