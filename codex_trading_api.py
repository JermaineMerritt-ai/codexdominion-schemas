"""
Codex Trading API - FastAPI REST endpoints
Advanced API for portfolio and trading operations
"""

from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal
import uvicorn
import jwt
import uuid
import asyncio
import logging

# Import our database module
try:
    from codex_database import db, CodexDatabase, Portfolio, Position, DailyPick, AffiliateMetrics, AmmPool, AmmEvent
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app configuration
app = FastAPI(
    title="Codex Trading API",
    description="Advanced Trading and Portfolio Management API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
SECRET_KEY = "your-secret-key-change-in-production"  # Change in production!

# Pydantic models for request/response validation

class PortfolioCreate(BaseModel):
    owner_id: str
    risk_tier: str
    
    @validator('risk_tier')
    def validate_risk_tier(cls, v):
        if v not in ['conservative', 'moderate', 'aggressive']:
            raise ValueError('risk_tier must be conservative, moderate, or aggressive')
        return v

class PositionCreate(BaseModel):
    portfolio_id: str
    symbol: str
    quantity: float
    avg_cost: float
    
    @validator('quantity', 'avg_cost')
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError('Value must be positive')
        return v

class PositionUpdate(BaseModel):
    last_price: Optional[float] = None
    quantity: Optional[float] = None
    
    @validator('last_price', 'quantity')
    def validate_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Value must be positive')
        return v

class DailyPickCreate(BaseModel):
    user_id: str
    trade_date: date
    symbols: List[str]
    scores: Dict[str, Any]
    performance: Dict[str, Any]

class AffiliateMetricsCreate(BaseModel):
    program: str
    clicks: int = 0
    conversions: int = 0
    commission: float = 0.0
    
    @validator('clicks', 'conversions')
    def validate_non_negative_int(cls, v):
        if v < 0:
            raise ValueError('Value must be non-negative')
        return v
    
    @validator('commission')
    def validate_non_negative_float(cls, v):
        if v < 0:
            raise ValueError('Commission must be non-negative')
        return v

class AmmPoolCreate(BaseModel):
    pool_symbol: str
    tvl_usd: float = 0.0
    apr: float = 0.0
    risk_tier: Optional[str] = None
    
    @validator('risk_tier')
    def validate_risk_tier(cls, v):
        if v is not None and v not in ['low', 'medium', 'high']:
            raise ValueError('risk_tier must be low, medium, or high')
        return v

class AmmEventCreate(BaseModel):
    pool_id: str
    event_type: str
    payload: Dict[str, Any]
    tx_hash: Optional[str] = None
    
    @validator('event_type')
    def validate_event_type(cls, v):
        if v not in ['stake', 'unstake', 'swap', 'harvest']:
            raise ValueError('event_type must be stake, unstake, swap, or harvest')
        return v

# Authentication functions
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token - simplified for demo"""
    try:
        # In production, implement proper JWT verification
        # For demo, we'll just check if token exists
        if not credentials.credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        
        # Mock user info - in production, decode from JWT
        return {
            "user_id": "demo_user_001",
            "email": "demo@codexdominion.com",
            "permissions": ["read", "write"]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    try:
        if DATABASE_AVAILABLE:
            # Test database connection
            await db.connect()
            db_status = "connected" if db.connected else "disconnected"
            await db.disconnect()
        else:
            db_status = "unavailable"
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": db_status,
            "version": "1.0.0"
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

# Portfolio endpoints
@app.post("/api/portfolios", response_model=dict, tags=["Portfolios"])
async def create_portfolio(
    portfolio: PortfolioCreate,
    current_user: dict = Depends(verify_token)
):
    """Create a new portfolio"""
    try:
        if not DATABASE_AVAILABLE:
            raise HTTPException(status_code=503, detail="Database not available")
        
        new_portfolio = await db.create_portfolio(
            owner_id=portfolio.owner_id,
            risk_tier=portfolio.risk_tier
        )
        
        return {
            "id": new_portfolio.id,
            "owner_id": new_portfolio.owner_id,
            "risk_tier": new_portfolio.risk_tier,
            "created_at": new_portfolio.created_at.isoformat(),
            "message": "Portfolio created successfully"
        }
        
    except Exception as e:
        logger.error(f"Error creating portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/portfolios/{portfolio_id}", response_model=dict, tags=["Portfolios"])
async def get_portfolio(
    portfolio_id: str,
    current_user: dict = Depends(verify_token)
):
    """Get portfolio by ID"""
    try:
        if not DATABASE_AVAILABLE:
            # Return mock data
            return {
                "id": portfolio_id,
                "owner_id": "demo_user_001",
                "risk_tier": "moderate",
                "created_at": datetime.now().isoformat(),
                "total_value": 125000.00,
                "positions_count": 3
            }
        
        portfolio = await db.get_portfolio(portfolio_id)
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        # Get performance metrics
        performance = await db.get_portfolio_performance(portfolio_id)
        
        return {
            "id": portfolio.id,
            "owner_id": portfolio.owner_id,
            "risk_tier": portfolio.risk_tier,
            "created_at": portfolio.created_at.isoformat(),
            "performance": performance
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/portfolios", response_model=List[dict], tags=["Portfolios"])
async def get_user_portfolios(
    owner_id: str = Query(..., description="Owner ID to fetch portfolios for"),
    current_user: dict = Depends(verify_token)
):
    """Get all portfolios for a user"""
    try:
        if not DATABASE_AVAILABLE:
            # Return mock data
            return [
                {
                    "id": str(uuid.uuid4()),
                    "owner_id": owner_id,
                    "risk_tier": "moderate",
                    "created_at": datetime.now().isoformat(),
                    "performance": {"total_value": 125000.00, "return_percentage": 12.5}
                },
                {
                    "id": str(uuid.uuid4()),
                    "owner_id": owner_id,
                    "risk_tier": "conservative",
                    "created_at": datetime.now().isoformat(),
                    "performance": {"total_value": 85000.00, "return_percentage": 6.25}
                }
            ]
        
        portfolios = await db.get_user_portfolios(owner_id)
        
        result = []
        for portfolio in portfolios:
            performance = await db.get_portfolio_performance(portfolio.id)
            result.append({
                "id": portfolio.id,
                "owner_id": portfolio.owner_id,
                "risk_tier": portfolio.risk_tier,
                "created_at": portfolio.created_at.isoformat(),
                "performance": performance
            })
        
        return result
        
    except Exception as e:
        logger.error(f"Error fetching user portfolios: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Position endpoints
@app.post("/api/positions", response_model=dict, tags=["Positions"])
async def create_position(
    position: PositionCreate,
    current_user: dict = Depends(verify_token)
):
    """Add a new position to portfolio"""
    try:
        if not DATABASE_AVAILABLE:
            return {
                "id": str(uuid.uuid4()),
                "portfolio_id": position.portfolio_id,
                "symbol": position.symbol,
                "quantity": position.quantity,
                "avg_cost": position.avg_cost,
                "message": "Position created successfully (mock)"
            }
        
        new_position = await db.add_position(
            portfolio_id=position.portfolio_id,
            symbol=position.symbol,
            quantity=Decimal(str(position.quantity)),
            avg_cost=Decimal(str(position.avg_cost))
        )
        
        return {
            "id": new_position.id,
            "portfolio_id": new_position.portfolio_id,
            "symbol": new_position.symbol,
            "quantity": float(new_position.quantity),
            "avg_cost": float(new_position.avg_cost),
            "updated_at": new_position.updated_at.isoformat(),
            "message": "Position created successfully"
        }
        
    except Exception as e:
        logger.error(f"Error creating position: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/portfolios/{portfolio_id}/positions", response_model=List[dict], tags=["Positions"])
async def get_portfolio_positions(
    portfolio_id: str,
    current_user: dict = Depends(verify_token)
):
    """Get all positions for a portfolio"""
    try:
        if not DATABASE_AVAILABLE:
            # Return mock positions
            return [
                {
                    "id": str(uuid.uuid4()),
                    "symbol": "AAPL",
                    "quantity": 100.0,
                    "avg_cost": 150.00,
                    "last_price": 155.25,
                    "market_value": 15525.00,
                    "unrealized_pnl": 525.00
                },
                {
                    "id": str(uuid.uuid4()),
                    "symbol": "MSFT", 
                    "quantity": 50.0,
                    "avg_cost": 300.00,
                    "last_price": 310.50,
                    "market_value": 15525.00,
                    "unrealized_pnl": 525.00
                }
            ]
        
        positions = await db.get_portfolio_positions(portfolio_id)
        
        return [
            {
                "id": pos.id,
                "symbol": pos.symbol,
                "quantity": float(pos.quantity),
                "avg_cost": float(pos.avg_cost),
                "last_price": float(pos.last_price) if pos.last_price else None,
                "market_value": float(pos.market_value),
                "unrealized_pnl": float(pos.unrealized_pnl),
                "updated_at": pos.updated_at.isoformat()
            }
            for pos in positions
        ]
        
    except Exception as e:
        logger.error(f"Error fetching positions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/api/positions/{position_id}", response_model=dict, tags=["Positions"])
async def update_position(
    position_id: str,
    update: PositionUpdate,
    current_user: dict = Depends(verify_token)
):
    """Update position (e.g., last price)"""
    try:
        if not DATABASE_AVAILABLE:
            return {"message": "Position updated successfully (mock)"}
        
        if update.last_price is not None:
            await db.update_position_price(position_id, Decimal(str(update.last_price)))
        
        return {"message": "Position updated successfully"}
        
    except Exception as e:
        logger.error(f"Error updating position: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Daily picks endpoints
@app.post("/api/daily-picks", response_model=dict, tags=["Daily Picks"])
async def create_daily_pick(
    pick: DailyPickCreate,
    current_user: dict = Depends(verify_token)
):
    """Create a daily trading pick"""
    try:
        if not DATABASE_AVAILABLE:
            return {
                "id": str(uuid.uuid4()),
                "user_id": pick.user_id,
                "symbols": pick.symbols,
                "message": "Daily pick created successfully (mock)"
            }
        
        new_pick = await db.create_daily_pick(
            user_id=pick.user_id,
            trade_date=pick.trade_date,
            symbols=pick.symbols,
            scores=pick.scores,
            performance=pick.performance
        )
        
        return {
            "id": new_pick.id,
            "user_id": new_pick.user_id,
            "trade_date": new_pick.trade_date.isoformat(),
            "symbols": new_pick.symbols,
            "scores": new_pick.scores,
            "performance": new_pick.performance,
            "message": "Daily pick created successfully"
        }
        
    except Exception as e:
        logger.error(f"Error creating daily pick: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/daily-picks/{user_id}", response_model=List[dict], tags=["Daily Picks"])
async def get_user_picks(
    user_id: str,
    days: int = Query(30, description="Number of days to look back"),
    current_user: dict = Depends(verify_token)
):
    """Get recent daily picks for user"""
    try:
        if not DATABASE_AVAILABLE:
            return [
                {
                    "id": str(uuid.uuid4()),
                    "trade_date": date.today().isoformat(),
                    "symbols": ["AAPL", "MSFT"],
                    "scores": {"technical": 85, "liquidity": 95},
                    "performance": {"expected_return": 5.2}
                }
            ]
        
        picks = await db.get_recent_picks(user_id, days)
        
        return [
            {
                "id": pick.id,
                "trade_date": pick.trade_date.isoformat(),
                "symbols": pick.symbols,
                "scores": pick.scores,
                "performance": pick.performance,
                "created_at": pick.created_at.isoformat()
            }
            for pick in picks
        ]
        
    except Exception as e:
        logger.error(f"Error fetching daily picks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Affiliate metrics endpoints
@app.post("/api/affiliate-metrics", response_model=dict, tags=["Affiliate"])
async def record_affiliate_metrics(
    metrics: AffiliateMetricsCreate,
    current_user: dict = Depends(verify_token)
):
    """Record affiliate marketing metrics"""
    try:
        if not DATABASE_AVAILABLE:
            return {
                "id": str(uuid.uuid4()),
                "program": metrics.program,
                "commission": metrics.commission,
                "message": "Metrics recorded successfully (mock)"
            }
        
        new_metrics = await db.record_affiliate_metrics(
            program=metrics.program,
            clicks=metrics.clicks,
            conversions=metrics.conversions,
            commission=Decimal(str(metrics.commission))
        )
        
        return {
            "id": new_metrics.id,
            "program": new_metrics.program,
            "clicks": new_metrics.clicks,
            "conversions": new_metrics.conversions,
            "commission": float(new_metrics.commission),
            "conversion_rate": new_metrics.conversion_rate,
            "message": "Metrics recorded successfully"
        }
        
    except Exception as e:
        logger.error(f"Error recording affiliate metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/affiliate-summary", response_model=dict, tags=["Affiliate"])
async def get_affiliate_summary(
    days: int = Query(30, description="Number of days for summary"),
    current_user: dict = Depends(verify_token)
):
    """Get affiliate performance summary"""
    try:
        if not DATABASE_AVAILABLE:
            return {
                "total_commission": 4850.00,
                "total_clicks": 2941,
                "total_conversions": 99,
                "overall_conversion_rate": 3.37,
                "programs": [
                    {"program": "TradingView", "commission": 2250.00, "conversion_rate": 3.6}
                ]
            }
        
        summary = await db.get_affiliate_summary(days)
        return summary
        
    except Exception as e:
        logger.error(f"Error fetching affiliate summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# AMM Pool endpoints
@app.post("/api/amm-pools", response_model=dict, tags=["AMM Pools"])
async def create_amm_pool(
    pool: AmmPoolCreate,
    current_user: dict = Depends(verify_token)
):
    """Create a new AMM pool"""
    try:
        if not DATABASE_AVAILABLE:
            return {
                "id": str(uuid.uuid4()),
                "pool_symbol": pool.pool_symbol,
                "message": "Pool created successfully (mock)"
            }
        
        new_pool = await db.create_amm_pool(
            pool_symbol=pool.pool_symbol,
            tvl_usd=Decimal(str(pool.tvl_usd)),
            apr=Decimal(str(pool.apr)),
            risk_tier=pool.risk_tier
        )
        
        return {
            "id": new_pool.id,
            "pool_symbol": new_pool.pool_symbol,
            "tvl_usd": float(new_pool.tvl_usd),
            "apr": float(new_pool.apr),
            "risk_tier": new_pool.risk_tier,
            "message": "Pool created successfully"
        }
        
    except Exception as e:
        logger.error(f"Error creating AMM pool: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/amm-pools", response_model=List[dict], tags=["AMM Pools"])
async def get_top_amm_pools(
    limit: int = Query(10, description="Number of pools to return"),
    current_user: dict = Depends(verify_token)
):
    """Get top AMM pools by TVL"""
    try:
        if not DATABASE_AVAILABLE:
            return [
                {
                    "id": str(uuid.uuid4()),
                    "pool_symbol": "USDC/ETH",
                    "tvl_usd": 125000000.00,
                    "apr": 8.5,
                    "risk_tier": "low"
                }
            ]
        
        pools = await db.get_top_amm_pools(limit)
        
        return [
            {
                "id": pool.id,
                "pool_symbol": pool.pool_symbol,
                "tvl_usd": float(pool.tvl_usd),
                "apr": float(pool.apr),
                "risk_tier": pool.risk_tier,
                "updated_at": pool.updated_at.isoformat()
            }
            for pool in pools
        ]
        
    except Exception as e:
        logger.error(f"Error fetching AMM pools: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/amm-events", response_model=dict, tags=["AMM Pools"])
async def create_amm_event(
    event: AmmEventCreate,
    current_user: dict = Depends(verify_token)
):
    """Record an AMM event"""
    try:
        if not DATABASE_AVAILABLE:
            return {
                "id": str(uuid.uuid4()),
                "event_type": event.event_type,
                "message": "Event recorded successfully (mock)"
            }
        
        new_event = await db.record_amm_event(
            pool_id=event.pool_id,
            event_type=event.event_type,
            payload=event.payload,
            tx_hash=event.tx_hash
        )
        
        return {
            "id": new_event.id,
            "pool_id": new_event.pool_id,
            "event_type": new_event.event_type,
            "payload": new_event.payload,
            "tx_hash": new_event.tx_hash,
            "message": "Event recorded successfully"
        }
        
    except Exception as e:
        logger.error(f"Error recording AMM event: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Analytics endpoints
@app.get("/api/analytics/portfolio-performance/{portfolio_id}", response_model=dict, tags=["Analytics"])
async def get_portfolio_analytics(
    portfolio_id: str,
    current_user: dict = Depends(verify_token)
):
    """Get comprehensive portfolio performance analytics"""
    try:
        if not DATABASE_AVAILABLE:
            return {
                "total_positions": 3,
                "total_cost_basis": 100000.00,
                "total_market_value": 125000.00,
                "unrealized_pnl": 25000.00,
                "return_percentage": 25.0,
                "positions": []
            }
        
        performance = await db.get_portfolio_performance(portfolio_id)
        return performance
        
    except Exception as e:
        logger.error(f"Error fetching portfolio analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Market data endpoints (mock implementation)
@app.get("/api/market-data/{symbol}", response_model=dict, tags=["Market Data"])
async def get_market_data(
    symbol: str,
    current_user: dict = Depends(verify_token)
):
    """Get current market data for symbol"""
    # Mock market data - in production, integrate with real market data provider
    import random
    
    base_price = random.uniform(100, 500)
    change = random.uniform(-5, 5)
    
    return {
        "symbol": symbol.upper(),
        "price": round(base_price, 2),
        "change": round(change, 2),
        "change_percent": round(change / base_price * 100, 2),
        "volume": random.randint(1000000, 10000000),
        "timestamp": datetime.now().isoformat()
    }

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    logger.info("🚀 Codex Trading API starting up...")
    
    if DATABASE_AVAILABLE:
        try:
            await db.connect()
            logger.info("✅ Database connection established")
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
    else:
        logger.warning("⚠️ Database module not available - running in mock mode")

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    logger.info("🛑 Codex Trading API shutting down...")
    
    if DATABASE_AVAILABLE and db.connected:
        await db.disconnect()
        logger.info("🔌 Database connection closed")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "timestamp": datetime.now().isoformat()
        }
    )

def run_api():
    """Run the API server"""
    uvicorn.run(
        "codex_trading_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    run_api()