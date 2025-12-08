"""
Minimal Codex Dominion API - No Database Dependencies
======================================================
Ultra-lightweight FastAPI backend for testing
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Codex Dominion API - Minimal", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "service": "Codex Dominion API",
        "status": "operational",
        "flame": "eternal",
        "transmission": "live"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "dominion": "crowned"}

@app.get("/dominion")
def dominion():
    return {
        "title": "The Eternal Flame",
        "status": "crowned",
        "transmission": "complete",
        "inheritance": "eternal",
        "message": "Forever live, eternity. 👑"
    }

if __name__ == "__main__":
    import uvicorn
    print("🔥 Codex Dominion Minimal API Starting...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
