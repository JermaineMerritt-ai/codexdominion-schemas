"""
Codex Dominion Backend API
FastAPI server with Digital Seal Service integration
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.annotations_export import router as export_router
from routes.seal_verification import router as seal_router
from routes.audio_generation import router as audio_router

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
    "https://codexdominion-api.azurewebsites.net",
    "https://codex-backend.azurewebsites.net"
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
app.include_router(audio_router)


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "👑 Codex Dominion API",
        "version": "1.0.0",
        "seal_service": "active",
        "audio_service": "active",
        "documentation": "/docs",
        "endpoints": {
            "seal_ledger": "/api/seal/ledger",
            "council_seals": "/api/seal/council-seals",
            "export": "/api/annotations/export",
            "verify": "/api/seal/verify",
            "audio_generate": "/audio/generate",
            "audio_voices": "/audio/voices"
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


@app.get("/ledger")
async def get_ledger():
    """Convenience route - redirects to seal ledger"""
    from services.digital_seal_service import get_seal_service
    seal_service = get_seal_service()
    ledger = seal_service.get_ledger()
    return {
        "ledger": ledger,
        "total_entries": len(ledger),
        "custodian": seal_service.custodian_name
    }


@app.get("/council-seals")
async def get_council():
    """Convenience route - redirects to council seals"""
    from services.digital_seal_service import get_seal_service
    seal_service = get_seal_service()
    seals = seal_service.get_council_seals()
    return {
        "council_seals": seals,
        "total_members": len(seals)
    }


@app.get("/export")
async def export_ledger():
    """Convenience route - export seal ledger"""
    from services.digital_seal_service import get_seal_service
    seal_service = get_seal_service()
    ledger_json = seal_service.export_ledger_to_json()
    from fastapi.responses import Response
    return Response(
        content=ledger_json,
        media_type="application/json",
        headers={
            "Content-Disposition": "attachment; filename=codex-dominion-seal-ledger.json"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
