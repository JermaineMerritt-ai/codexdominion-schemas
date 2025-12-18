"""
🔥 Codex Dominion - Portfolio Risk Management API 👑
FastAPI endpoints for portfolio creation and risk profile management
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
import uvicorn

app = FastAPI(title="Codex Portfolio API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PORTFOLIO_LEDGER = "portfolios.json"

# Helper functions
def load_portfolios():
    """Load portfolio ledger"""
    try:
        with open(PORTFOLIO_LEDGER, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "meta": {
                "version": "1.0.0",
                "last_updated": datetime.utcnow().isoformat() + "Z",
                "custodian_authority": "Jermaine Merritt",
                "ledger_type": "PORTFOLIO_LEDGER"
            },
            "portfolios": [],
            "risk_profiles": {
                "conservative": {
                    "description": "Low risk, stable returns",
                    "max_stock_allocation": 0.4,
                    "min_bond_allocation": 0.5
                },
                "moderate": {
                    "description": "Balanced risk and growth",
                    "max_stock_allocation": 0.7,
                    "min_bond_allocation": 0.2
                },
                "aggressive": {
                    "description": "High risk, maximum growth potential",
                    "max_stock_allocation": 1.0,
                    "min_bond_allocation": 0.0
                }
            }
        }

def save_portfolios(data):
    """Save portfolio ledger with timestamp"""
    data["meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
    with open(PORTFOLIO_LEDGER, "w") as f:
        json.dump(data, f, indent=2)

# Endpoints
@app.get("/")
def root():
    """Health check"""
    return {
        "status": "operational",
        "service": "Codex Portfolio API",
        "version": "1.0.0",
        "flame": "🔥 The Flame Burns Sovereign and Eternal 👑"
    }

@app.get("/health")
def health():
    """Detailed health check"""
    data = load_portfolios()
    return {
        "status": "healthy",
        "portfolios_count": len(data.get("portfolios", [])),
        "last_updated": data["meta"]["last_updated"]
    }

@app.post("/api/auth/register")
def register_user(credentials: dict):
    """Register new user with risk profile"""
    # In production, hash password and store in secure database
    # For now, return mock response
    email = credentials.get("email", "")
    return {
        "token": f"abc123_{email}",
        "user_id": hash(email) % 1000,
        "message": "Account created successfully"
    }

@app.get("/api/portfolios")
def get_portfolios(user_id: Optional[int] = None):
    """Get all portfolios or filter by user_id"""
    data = load_portfolios()
    portfolios = data.get("portfolios", [])

    if user_id:
        portfolios = [p for p in portfolios if p["user_id"] == user_id]

    return portfolios

@app.get("/api/portfolios/{portfolio_id}")
def get_portfolio(portfolio_id: int):
    """Get specific portfolio"""
    data = load_portfolios()
    portfolios = data.get("portfolios", [])

    for portfolio in portfolios:
        if portfolio["id"] == portfolio_id:
            return portfolio

    raise HTTPException(status_code=404, detail="Portfolio not found")

@app.post("/api/portfolios")
def create_portfolio(portfolio: dict):
    """Create new portfolio"""
    data = load_portfolios()

    # Validate risk profile
    risk_profile = portfolio.get("risk_profile")
    if risk_profile not in data["risk_profiles"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid risk profile. Must be one of: {list(data['risk_profiles'].keys())}"
        )

    # Generate new ID
    existing_ids = [p["id"] for p in data.get("portfolios", [])]
    new_id = max(existing_ids) + 1 if existing_ids else 1

    # Create portfolio
    now = datetime.utcnow().isoformat() + "Z"
    new_portfolio = {
        "id": new_id,
        "user_id": portfolio.get("user_id"),
        "name": portfolio.get("name"),
        "risk_profile": risk_profile,
        "holdings": portfolio.get("holdings", []),
        "total_value": 0.0,
        "created_at": now,
        "updated_at": now
    }

    data["portfolios"].append(new_portfolio)
    save_portfolios(data)

    return new_portfolio

@app.put("/api/portfolios/{portfolio_id}")
def update_portfolio(portfolio_id: int, portfolio: dict):
    """Update existing portfolio"""
    data = load_portfolios()

    for i, p in enumerate(data["portfolios"]):
        if p["id"] == portfolio_id:
            # Update fields
            p["name"] = portfolio.get("name", p["name"])
            p["risk_profile"] = portfolio.get("risk_profile", p["risk_profile"])
            p["holdings"] = portfolio.get("holdings", p["holdings"])
            p["updated_at"] = datetime.utcnow().isoformat() + "Z"

            # Recalculate total value
            p["total_value"] = sum(h.get("value", 0) for h in p["holdings"])

            data["portfolios"][i] = p
            save_portfolios(data)
            return p

    raise HTTPException(status_code=404, detail="Portfolio not found")

@app.delete("/api/portfolios/{portfolio_id}")
def delete_portfolio(portfolio_id: int):
    """Delete portfolio"""
    data = load_portfolios()

    initial_count = len(data["portfolios"])
    data["portfolios"] = [p for p in data["portfolios"] if p["id"] != portfolio_id]

    if len(data["portfolios"]) == initial_count:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    save_portfolios(data)
    return {"message": "Portfolio deleted successfully", "id": portfolio_id}

@app.get("/api/risk-profiles")
def get_risk_profiles():
    """Get available risk profiles"""
    data = load_portfolios()
    return data.get("risk_profiles", {})

@app.post("/api/portfolios/{portfolio_id}/holdings")
def add_holding(portfolio_id: int, holding: dict):
    """Add holding to portfolio"""
    data = load_portfolios()

    for i, p in enumerate(data["portfolios"]):
        if p["id"] == portfolio_id:
            # Add holding
            p["holdings"].append(holding)

            # Recalculate totals
            p["total_value"] = sum(h.get("value", 0) for h in p["holdings"])
            p["updated_at"] = datetime.utcnow().isoformat() + "Z"

            # Update sector breakdown
            sector_totals = {}
            for h in p["holdings"]:
                sector = h.get("sector", "Other")
                sector_totals[sector] = sector_totals.get(sector, 0) + h.get("value", 0)

            if p["total_value"] > 0:
                p["sector_breakdown"] = {
                    sector: round((value / p["total_value"]) * 100, 2)
                    for sector, value in sector_totals.items()
                }

            # Calculate performance
            total_gain_loss = sum(h.get("gain_loss", 0) for h in p["holdings"])
            cost_basis = p["total_value"] - total_gain_loss
            p["performance"] = {
                "total_gain_loss": round(total_gain_loss, 2),
                "total_gain_loss_pct": round((total_gain_loss / cost_basis * 100) if cost_basis > 0 else 0, 2),
                "daily_change": sum(h.get("daily_change", 0) for h in p["holdings"]),
                "daily_change_pct": round((sum(h.get("daily_change", 0) for h in p["holdings"]) / p["total_value"] * 100) if p["total_value"] > 0 else 0, 2)
            }

            data["portfolios"][i] = p
            save_portfolios(data)
            return p

    raise HTTPException(status_code=404, detail="Portfolio not found")

@app.get("/api/portfolios/{portfolio_id}/performance")
def get_portfolio_performance(portfolio_id: int):
    """Get portfolio performance metrics"""
    data = load_portfolios()

    for portfolio in data["portfolios"]:
        if portfolio["id"] == portfolio_id:
            return {
                "id": portfolio["id"],
                "name": portfolio["name"],
                "total_value": portfolio.get("total_value", 0),
                "performance": portfolio.get("performance", {}),
                "sector_breakdown": portfolio.get("sector_breakdown", {}),
                "top_holdings": sorted(
                    portfolio.get("holdings", []),
                    key=lambda x: x.get("value", 0),
                    reverse=True
                )[:5]
            }

    raise HTTPException(status_code=404, detail="Portfolio not found")

@app.get("/api/portfolios/{portfolio_id}/holdings")
def get_holdings(portfolio_id: int):
    """Get all holdings in a portfolio"""
    data = load_portfolios()

    for portfolio in data["portfolios"]:
        if portfolio["id"] == portfolio_id:
            return portfolio.get("holdings", [])

    raise HTTPException(status_code=404, detail="Portfolio not found")

if __name__ == "__main__":
    print("🔥 Starting Codex Portfolio API 👑")
    print("📊 Endpoints:")
    print("  - GET    /health")
    print("  - POST   /api/auth/register")
    print("  - GET    /api/portfolios")
    print("  - POST   /api/portfolios")
    print("  - GET    /api/portfolios/{id}")
    print("  - PUT    /api/portfolios/{id}")
    print("  - DELETE /api/portfolios/{id}")
    print("  - GET    /api/portfolios/{id}/holdings")
    print("  - POST   /api/portfolios/{id}/holdings")
    print("  - GET    /api/portfolios/{id}/performance")
    print("  - GET    /api/risk-profiles")
    print("\n👑 Running on http://localhost:8096")
    uvicorn.run(app, host="0.0.0.0", port=8096)
