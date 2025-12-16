# 🚀 DOT300 API - Quick Start Guide

**Base URL:** http://localhost:8300

---

## 📍 Available Endpoints

### **1. API Documentation**
```bash
GET http://localhost:8300/
```
Returns list of all available endpoints and industries.

---

### **2. Health Check**
```bash
GET http://localhost:8300/health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "DOT300 Agents"
}
```

---

### **3. System Statistics**
```bash
GET http://localhost:8300/api/stats
```
**Response:**
```json
{
  "total_agents": 301,
  "version": "1.0.0",
  "generated_at": "2025-12-16T02:36:04"
}
```

---

### **4. Get All Agents**
```bash
GET http://localhost:8300/api/agents
```
Returns complete JSON with all 301 agents including:
- Agent ID
- Name
- Industry
- Specialization
- Performance score
- Success rate
- Tasks completed
- Capabilities
- Metadata

---

### **5. Get Specific Agent**
```bash
GET http://localhost:8300/api/agents/agent_0001
```
**Example Response:**
```json
{
  "id": "agent_0001",
  "name": "Primary Care Physician AI",
  "industry": "healthcare",
  "specialization": "General diagnosis and treatment",
  "performance_score": 0.954,
  "success_rate": 0.854,
  "tasks_completed": 965,
  "status": "idle",
  "capabilities": [
    {
      "name": "general_diagnosis_and_treatment",
      "skill_level": 0.864,
      "experience_points": 5051
    },
    {
      "name": "communication",
      "skill_level": 0.816,
      "experience_points": 3305
    }
  ],
  "metadata": {
    "tier": "elite",
    "cost_per_task": 8.24,
    "avg_response_time": 3.17
  }
}
```

---

### **6. Get Agents by Industry**
```bash
GET http://localhost:8300/api/agents/industry/{industry_name}
```

**Available Industries:**
- `healthcare` (43 agents)
- `finance` (43 agents)
- `legal` (43 agents)
- `real_estate` (43 agents)
- `ecommerce` (43 agents)
- `education` (43 agents)
- `entertainment` (43 agents)

**Example:**
```bash
GET http://localhost:8300/api/agents/industry/healthcare
```

**Response:**
```json
{
  "industry": "healthcare",
  "count": 43,
  "agents": [
    {
      "id": "agent_0001",
      "name": "Primary Care Physician AI",
      "specialization": "General diagnosis and treatment",
      ...
    },
    ...
  ]
}
```

---

## 🧪 Testing with PowerShell

### **Quick Health Check:**
```powershell
Invoke-RestMethod http://localhost:8300/health
```

### **Get Statistics:**
```powershell
$stats = Invoke-RestMethod http://localhost:8300/api/stats
Write-Host "Total Agents: $($stats.total_agents)"
```

### **Get Healthcare Agents:**
```powershell
$hc = Invoke-RestMethod http://localhost:8300/api/agents/industry/healthcare
Write-Host "Found $($hc.count) healthcare agents"
$hc.agents | Select-Object name, specialization | Format-Table
```

### **Get Specific Agent:**
```powershell
$agent = Invoke-RestMethod http://localhost:8300/api/agents/agent_0001
Write-Host "$($agent.name) - Score: $($agent.performance_score)"
```

---

## 🧪 Testing with curl

### **Health Check:**
```bash
curl http://localhost:8300/health
```

### **Get All Agents:**
```bash
curl http://localhost:8300/api/agents
```

### **Get Finance Agents:**
```bash
curl http://localhost:8300/api/agents/industry/finance
```

---

## 🎯 Agent Industries & Specializations

### **Healthcare (43 agents)**
- Primary Care, Cardiologist, Oncologist, Pediatrician
- Surgeon, Dermatologist, Psychiatrist, Neurologist
- Orthopedic, Ophthalmologist, Radiologist, etc.

### **Finance (43 agents)**
- Stock Analyst, Algo Trader, Portfolio Manager
- Risk Analyst, Compliance Officer, Tax Consultant
- Crypto Analyst, Forex Trader, Options Trader, etc.

### **Legal (43 agents)**
- Contract Lawyer, IP Attorney, Corporate Lawyer
- Family Lawyer, Immigration Attorney, Tax Lawyer, etc.

### **Real Estate (43 agents)**
- Listing Agent, Buyer's Agent, Property Appraiser
- Home Inspector, Mortgage Broker, Title Agent, etc.

### **E-commerce (43 agents)**
- Product Manager, Inventory Manager, Pricing AI
- SEO Optimizer, Social Media Manager, Email Marketer, etc.

### **Education (43 agents)**
- Math Tutor, Programming Tutor, Career Counselor
- Language Coach, Study Skills Coach, Test Prep, etc.

### **Entertainment (43 agents)**
- Script Writer, Music Composer, Video Editor
- Sound Engineer, Animator, Game Designer, etc.

---

## 🐳 Docker Management

### **Check Status:**
```powershell
docker ps --filter "name=codex-dot300"
```

### **View Logs:**
```powershell
docker logs codex-dot300 -f
```

### **Restart Service:**
```powershell
docker restart codex-dot300
```

### **Stop Service:**
```powershell
docker stop codex-dot300
```

### **Start Service:**
```powershell
docker-compose -f docker-compose.test.yml up -d dot300
```

---

## 📊 Performance Metrics

**Total Agents:** 301
**Industries:** 7
**Average Performance Score:** 0.85+
**Top Performer:** Portfolio Manager AI (0.987)
**API Response Time:** < 100ms
**Container Status:** Healthy ✅

---

## 🔧 Troubleshooting

### **Port Already in Use:**
```powershell
# Find process using port 8300
netstat -ano | findstr :8300

# Kill the process (replace PID)
taskkill /PID <PID> /F

# Restart container
docker restart codex-dot300
```

### **Container Not Starting:**
```powershell
# Check logs for errors
docker logs codex-dot300

# Rebuild image
docker-compose -f docker-compose.test.yml build dot300

# Restart
docker-compose -f docker-compose.test.yml up -d dot300
```

### **API Not Responding:**
```powershell
# Check if agents file is mounted
docker exec codex-dot300 ls -lh dot300_agents.json

# Check Flask is running
docker exec codex-dot300 ps aux | grep python
```

---

## 🚀 Next Steps

1. **Build Frontend UI** - Create web interface to browse agents
2. **Add Search** - Implement agent search and filtering
3. **Task Assignment** - Build system to assign tasks to agents
4. **Analytics** - Track agent performance and usage metrics
5. **Cloud Deploy** - Deploy to Azure/GCP/AWS for production

---

## 📚 Documentation

- [BUILD_PROGRESS_90_PERCENT.md](BUILD_PROGRESS_90_PERCENT.md) - Full agent system docs
- [PRODUCTION_DEPLOYMENT_COMPLETE.md](PRODUCTION_DEPLOYMENT_COMPLETE.md) - Deployment guide
- [DOT300_DEPLOYED.md](DOT300_DEPLOYED.md) - Deployment success summary
- [100_PERCENT_COMPLETE.md](100_PERCENT_COMPLETE.md) - Complete system overview

---

**Status:** ✅ OPERATIONAL
**Endpoint:** http://localhost:8300
**Agents:** 301 Ready to Work! 🤖

🔥 **Your AI Agent Marketplace is LIVE!** 🔥
