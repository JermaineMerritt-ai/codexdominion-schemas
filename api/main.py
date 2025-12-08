from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Codex Dominion API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Codex Dominion API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/products")
async def get_products():
    return {"products": []}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 4000))
    uvicorn.run(app, host="0.0.0.0", port=port)
