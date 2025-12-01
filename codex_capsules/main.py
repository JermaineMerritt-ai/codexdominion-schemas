# codex_capsules/main.py
from api import app as capsules_app
from fastapi import FastAPI

app = FastAPI(
    title="Codex Capsules Service",
    description="Standalone service for operational sovereignty tracking",
    version="1.0.0",
)

# Mount the capsules API
app.mount("/api", capsules_app)


@app.get("/")
def root():
    return {
        "service": "Codex Capsules",
        "version": "1.0.0",
        "description": "Operational sovereignty tracking for ceremonial and technical operations",
        "api_docs": "/docs",
        "capsules_api": "/api/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
