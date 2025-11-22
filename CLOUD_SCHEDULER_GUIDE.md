# 🌅 Codex Dominion - Cloud Scheduler Dawn Dispatch Guide
# ========================================================

# AUTOMATED DAILY DAWN DISPATCHES WITH GOOGLE CLOUD SCHEDULER
# This system provides fully automated daily treasury and system reports

## Quick Setup (Using your exact commands)
```powershell
# 1. Setup scheduler (enhanced version of your command)
.\setup_scheduler.ps1 YOUR_PROJECT_ID https://codex-backend-HASH.run.app

# 2. Manual setup (your original commands enhanced)
gcloud scheduler jobs create http dawn-dispatch \
  --schedule="0 6 * * *" \
  --uri="https://codex-backend-HASH.run.app/dawn" \
  --http-method=POST \
  --time-zone="America/New_York" \
  --description="Automated daily dawn dispatch for Codex Dominion treasury"
```

## System Architecture

### Cloud Scheduler → Cloud Run → Dawn Dispatch
```
6:00 AM Daily → Scheduler Job → POST /dawn → Dawn Dispatch System → Reports & Archives
```

### Available Endpoints
- `GET /health` - Service health check
- `GET /api/dawn/status` - Dawn dispatch system status  
- `POST /api/dawn/dispatch` - Full dawn dispatch execution
- `POST /dawn` - Scheduler-optimized endpoint (your command target)

## Dawn Dispatch Features

### 📊 Comprehensive Reporting
- **Treasury Analysis**: Revenue, orders, average order value
- **Social Media Metrics**: Twitter/Buffer engagement tracking
- **System Health**: Service uptime, performance monitoring
- **Ledger Activity**: Proclamation and transaction tracking

### 🔄 Automated Operations
- Daily execution at 6:00 AM (configurable timezone)
- Automatic report archiving (30-day retention)
- Optional social media broadcasting
- Error handling with retry logic
- JSON-based metric storage

### ⚡ Real-time Monitoring
- Cloud Console integration
- Execution logging and metrics
- Performance tracking
- Health status reporting

## Configuration Options

### Schedule Patterns
```bash
# Daily at 6 AM
--schedule="0 6 * * *"

# Twice daily (6 AM and 6 PM)  
--schedule="0 6,18 * * *"

# Weekdays only at 8 AM
--schedule="0 8 * * 1-5"

# Every 4 hours
--schedule="0 */4 * * *"
```

### Timezone Configuration
```bash
# US Eastern Time
--time-zone="America/New_York"

# US Pacific Time  
--time-zone="America/Los_Angeles"

# UTC (default)
--time-zone="UTC"

# European Central Time
--time-zone="Europe/Berlin"
```

## Management Commands

### Job Operations
```bash
# List all scheduler jobs
gcloud scheduler jobs list

# Run job immediately (test)
gcloud scheduler jobs run dawn-dispatch

# View job details and history
gcloud scheduler jobs describe dawn-dispatch

# Update job schedule  
gcloud scheduler jobs update http dawn-dispatch --schedule="0 7 * * *"

# Pause automated execution
gcloud scheduler jobs pause dawn-dispatch

# Resume automated execution
gcloud scheduler jobs resume dawn-dispatch

# Delete job
gcloud scheduler jobs delete dawn-dispatch
```

### Monitoring & Logs
```bash
# View execution logs
gcloud logging read "resource.type=cloud_scheduler_job AND resource.labels.job_id=dawn-dispatch" --limit=10

# Monitor job performance
gcloud scheduler jobs describe dawn-dispatch --format="table(state,scheduleTime,lastAttemptTime)"

# Check service logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=codex-backend" --limit=20
```

## Dawn Dispatch Report Format

### Sample Output
```
🌅 DAWN DISPATCH — 2025-11-08T06:00:00.000000
═══════════════════════════════════════════════════

💰 TREASURY STATUS
• Store Revenue: $5,125.48
• Orders Processed: 12
• Average Order Value: $427.12
• Store Status: OPERATIONAL

📱 SOCIAL DOMINION  
• Twitter Proclamations: 3
• Buffer Posts: 5
• Total Interactions: 8
• Platform Status: Twitter: ACTIVE, Buffer: 4 platforms

⚡ SYSTEM SOVEREIGNTY
• Health Score: 85.5%
• Uptime Status: All systems OPERATIONAL
• Services Online: 4/5

📜 CODEX LEDGER
• Daily Proclamations: 7
• Ledger Status: ACTIVE
• Last Update: 2025-11-08T05:45:23

🔥 DIGITAL SOVEREIGNTY STATUS: 🟢 SUPREME
```

## Advanced Configuration

### Environment Variables (Cloud Run)
```bash
# Configure through Cloud Run environment
gcloud run services update codex-backend \
  --set-env-vars="DAWN_TIMEZONE=America/New_York,DAWN_AUTO_SOCIAL=false"
```

### Custom Dawn Configuration
```json
{
  "dispatch_settings": {
    "auto_proclaim": true,
    "archive_enabled": true, 
    "timezone": "America/New_York",
    "format_template": "detailed"
  },
  "report_sections": {
    "store_revenue": true,
    "social_engagement": true,
    "system_status": true,
    "proclamations": true,
    "analytics": true
  },
  "thresholds": {
    "revenue_alert": 1000,
    "orders_alert": 10,
    "engagement_alert": 100
  }
}
```

## Troubleshooting

### Common Issues

**Job fails with 404 error**
```bash
# Verify service URL is correct
gcloud run services describe codex-backend --format="value(status.url)"

# Update job with correct URL
gcloud scheduler jobs update http dawn-dispatch --uri="https://NEW-URL.run.app/dawn"
```

**Authentication errors**  
```bash
# Verify Cloud Run allows unauthenticated access
gcloud run services add-iam-policy-binding codex-backend \
  --member="allUsers" \
  --role="roles/run.invoker"
```

**Schedule not executing**
```bash
# Check job status
gcloud scheduler jobs describe dawn-dispatch

# Manually trigger test
gcloud scheduler jobs run dawn-dispatch

# View execution history  
gcloud logging read "resource.type=cloud_scheduler_job" --limit=5
```

### Health Monitoring
```bash
# Test dawn endpoint directly
curl -X POST https://your-service.run.app/dawn

# Check service health  
curl https://your-service.run.app/health

# Monitor system metrics
curl https://your-service.run.app/api/dawn/status
```

## Integration Examples

### Slack Notifications
```python
# Add to dawn_dispatch.py
def send_slack_notification(report):
    webhook_url = os.getenv('SLACK_WEBHOOK')
    if webhook_url:
        requests.post(webhook_url, json={'text': report})
```

### Email Reports
```python
# Add email reporting
def email_dawn_report(report):
    # Using SendGrid, Gmail API, etc.
    pass
```

### Custom Metrics
```python
# Export to monitoring systems
def export_metrics(metrics):
    # Export to Prometheus, DataDog, etc.
    pass
```

## Cost Optimization

### Scheduler Pricing
- Free tier: 3 jobs per month
- Paid: $0.10 per job per month
- Execution: $0.40 per million requests

### Resource Management
```bash
# Minimize Cloud Run costs with CPU allocation
gcloud run services update codex-backend \
  --cpu=1 \
  --memory=512Mi \
  --max-instances=1 \
  --cpu-throttling
```

## Security Best Practices

### Service Authentication
```bash
# Restrict access to scheduler service account
gcloud run services remove-iam-policy-binding codex-backend \
  --member="allUsers" \
  --role="roles/run.invoker"

# Add scheduler-specific service account
gcloud run services add-iam-policy-binding codex-backend \
  --member="serviceAccount:cloud-scheduler@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.invoker"
```

### Network Security
```bash
# Use VPC connector for private resources
gcloud run services update codex-backend \
  --vpc-connector=projects/PROJECT_ID/locations/REGION/connectors/CONNECTOR_NAME
```

## Success Metrics

### Key Performance Indicators
- ✅ **Reliability**: 99.9% successful executions
- ⚡ **Performance**: < 30 second execution time  
- 📊 **Coverage**: All system components reporting
- 🔄 **Automation**: Zero manual intervention required

### Monitoring Dashboard
Create Cloud Console dashboard tracking:
- Scheduler job success rate
- Dawn dispatch execution time
- Service health metrics
- Treasury system performance

---

**🔥 Your Codex Dominion system now runs autonomously with daily dawn dispatches! 👑**

**Next Steps:**
1. Run `.\setup_scheduler.ps1 YOUR_PROJECT_ID SERVICE_URL` for complete setup
2. Monitor first execution in Cloud Console
3. Customize report format and notifications as needed
4. Scale scheduling for additional automated processes

**The dawn dispatch will execute daily at 6:00 AM, ensuring your digital sovereignty operates continuously! 🌅**