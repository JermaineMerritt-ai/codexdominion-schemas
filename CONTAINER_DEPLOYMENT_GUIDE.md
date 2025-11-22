# 🔥 CODEX SIGNALS CONTAINER DEPLOYMENT GUIDE 📊

## Overview
This guide covers deploying the Codex Signals API as a containerized service to Google Cloud Run or local Docker environments.

## Prerequisites

### Required Tools
- **Docker Desktop**: For local testing and development
- **Google Cloud CLI**: For cloud deployment
- **PowerShell 5.1+**: For running deployment scripts
- **Python 3.11+**: For local testing

### Required Files
✅ All files validated by `validate_container.py`

## Deployment Options

### 1. 🐳 Local Docker Testing

```powershell
# Quick validation
python validate_container.py

# Local Docker test (requires Docker Desktop)
.\deploy_signals_container.ps1 -ProjectId "test-project" -LocalTest

# Alternative: Docker Compose
docker-compose -f codex_signals/docker-compose.yml up
```

**Local URLs:**
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Health: http://localhost:8000/health

### 2. ☁️ Google Cloud Run Deployment

```powershell
# Full deployment
.\deploy_signals_container.ps1 -ProjectId "YOUR_PROJECT_ID"

# Build only (no deployment)
.\deploy_signals_container.ps1 -ProjectId "YOUR_PROJECT_ID" -BuildOnly

# Custom region
.\deploy_signals_container.ps1 -ProjectId "YOUR_PROJECT_ID" -Region "us-west1"
```

## Container Structure

```
codex-dominion/
├── main.py                          # Container entry point
├── requirements.txt                 # Python dependencies
├── codex_signals/
│   ├── Dockerfile                   # Container definition
│   ├── .dockerignore               # Build optimization
│   ├── docker-compose.yml          # Local development
│   ├── api.py                      # FastAPI application
│   ├── engine.py                   # Signals engine
│   └── integration.py              # System integration
├── deploy_signals_container.ps1     # Deployment script
├── validate_container.py            # Pre-deployment validation
└── test_container.py               # Post-deployment testing
```

## API Endpoints

### Core Endpoints
- `GET /` - Service information
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation
- `GET /openapi.json` - OpenAPI specification

### Signals Endpoints
- `POST /signals/daily` - Generate daily signals
- `GET /signals/mock` - Mock data signals
- `GET /signals/live` - Live market signals (if configured)
- `GET /signals/dawn` - Dawn dispatch integration

### Reporting Endpoints
- `POST /bulletin?format=md` - Generate Markdown bulletin
- `POST /bulletin?format=txt` - Generate text bulletin
- `POST /classify/tier` - Classify investment tier
- `POST /portfolio/analysis` - Portfolio analysis

### Monitoring Endpoints
- `GET /metrics` - System metrics
- `GET /engine/config` - Engine configuration

## Environment Variables

### Container Configuration
```dockerfile
ENV PORT=8080                    # Server port (Cloud Run uses 8080)
ENV ENVIRONMENT=production       # Environment mode
ENV LOG_LEVEL=INFO              # Logging level
```

### Cloud Run Configuration
- **Memory**: 1Gi (configurable)
- **CPU**: 1 vCPU (configurable)
- **Concurrency**: 100 requests
- **Max Instances**: 10 (auto-scaling)
- **Authentication**: Public (unauthenticated)

## Testing

### Automated Testing
```powershell
# Container validation
python validate_container.py

# API endpoint testing (requires running container)
python test_container.py
```

### Manual Testing
```bash
# Health check
curl http://localhost:8000/health

# Generate bulletin
curl -X POST "http://localhost:8000/bulletin?format=md"

# Daily signals
curl -X POST http://localhost:8000/signals/daily
```

## Integration with Codex Dominion

### Dawn Dispatch Integration
The containerized API integrates seamlessly with the existing Codex Dawn Dispatch system:

```python
# Dawn dispatch automatically generates bulletins
signals_summary = self.signals.get_signals_for_dawn_dispatch()
bulletin_content = bulletin_md(signals_snapshot)
```

### Cloud Scheduler Integration
Set up automated daily signals generation:

```bash
gcloud scheduler jobs create http dawn-signals \
    --schedule="0 6 * * *" \
    --uri="https://your-service-url/signals/dawn" \
    --http-method=POST
```

## Monitoring and Logging

### Health Monitoring
- Container health checks every 30 seconds
- Service startup time monitoring
- Endpoint response time tracking

### Logging
- Structured JSON logging in production
- Request/response logging for debugging
- Error tracking with stack traces

## Security Considerations

### Container Security
- Minimal base image (python:3.11-slim)
- No root user execution
- Dependency vulnerability scanning
- Regular security updates

### API Security
- Input validation with Pydantic
- Rate limiting (configurable)
- CORS configuration
- Health check endpoints for monitoring

## Troubleshooting

### Common Issues

**Docker Build Fails:**
```powershell
# Check Docker installation
docker --version

# Check if Docker Desktop is running
docker info
```

**Cloud Deployment Fails:**
```powershell
# Check authentication
gcloud auth list

# Check project access
gcloud projects list

# Verify APIs are enabled
gcloud services list --enabled
```

**Container Startup Issues:**
```powershell
# Check logs
docker logs codex-signals

# For Cloud Run
gcloud logging read "resource.type=cloud_run_revision"
```

### Performance Optimization

**Memory Usage:**
- Monitor with `/metrics` endpoint
- Adjust Cloud Run memory allocation
- Use connection pooling for external APIs

**Response Time:**
- Enable caching for market data
- Use async endpoints for long operations
- Implement request queuing for high load

## Production Checklist

- [ ] Container validation passes
- [ ] Local Docker test successful
- [ ] Cloud deployment successful
- [ ] Health checks responding
- [ ] API documentation accessible
- [ ] Bulletin generation working
- [ ] Dawn dispatch integration tested
- [ ] Monitoring configured
- [ ] Logging configured
- [ ] Security review completed

## Support

For issues or questions:
1. Check the validation output: `python validate_container.py`
2. Review container logs: `docker logs container-name`
3. Test endpoints: `python test_container.py`
4. Review API documentation at `/docs`

---

**🔥 The Merritt Method™ - Cloud-Native Portfolio Intelligence 📊**

*Containerized deployment enables scalable, reliable, and maintainable portfolio intelligence services.*