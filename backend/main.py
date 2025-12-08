"""
Codex Dominion Backend API
FastAPI server with Digital Seal Service integration
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.annotations_export import router as export_router
from routes.seal_verification import router as seal_router

app = FastAPI(
    title="Codex Dominion API",
    description="Cryptographic sealing infrastructure for ceremonial exports",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Get CORS origins from environment or use defaults
cors_origins_str = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:3001')
cors_origins = [origin.strip() for origin in cors_origins_str.split(',')]

# Add Azure and IONOS production domains if not already included
production_origins = [
    "https://codexdominion.app",
    "https://www.codexdominion.app",
    "https://api.codexdominion.app",
    "https://codexdominion.azurewebsites.net",
    "https://codexdominion-api.azurewebsites.net"
]

for origin in production_origins:
    if origin not in cors_origins:
        cors_origins.append(origin)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(export_router)
app.include_router(seal_router)


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "👑 Codex Dominion API",
        "version": "1.0.0",
        "seal_service": "active",
        "documentation": "/docs",
        "endpoints": {
            "seal_ledger": "/api/seal/ledger",
            "council_seals": "/api/seal/council-seals",
            "export": "/api/annotations/export",
            "verify": "/api/seal/verify"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "codex-dominion-api",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
