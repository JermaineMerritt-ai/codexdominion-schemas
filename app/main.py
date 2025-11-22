# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, datetime, json, requests, time
import psycopg2, redis
from contextlib import contextmanager
from typing import List, Dict, Any, Optional

app = FastAPI(title="Codex Market Dominion", version="2.0.0")

# Database connection with environment fallback
try:
    DB_URL = os.getenv("DATABASE_URL", "postgresql://localhost/codex_dominion")
    DB = psycopg2.connect(DB_URL)
    print("✅ PostgreSQL connected")
except Exception as e:
    print(f"⚠️ PostgreSQL unavailable: {e}")
    DB = None

# Redis connection with fallback
try:
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    R = redis.Redis.from_url(REDIS_URL)
    R.ping()  # Test connection
    print("✅ Redis connected")
except Exception as e:
    print(f"⚠️ Redis unavailable: {e}")
    R = None

# API configurations
MARKET_API_KEY = os.getenv("MARKET_API_KEY", "demo_key_12345")
AFFILIATE_API_KEY = os.getenv("AFFILIATE_API_KEY", "affiliate_demo_key")
AMM_NODE_URL = os.getenv("AMM_NODE_URL", "https://ethereum-mainnet.infura.io/v3/demo")

class PickRequest(BaseModel):
    user_id: str
    symbols: List[str]
    trade_date: str

class SwapRequest(BaseModel):
    pool_id: str
    from_asset: str
    to_asset: str
    amount: float

@contextmanager
def get_db_cursor():
    """Context manager for database operations with fallback"""
    if not DB:
        yield None
        return
    
    try:
        cur = DB.cursor()
        yield cur
        DB.commit()
    except Exception as e:
        DB.rollback()
        raise e
    finally:
        if 'cur' in locals():
            cur.close()

def q(sql: str, params: tuple = None, fetch: bool = True) -> List[tuple]:
    """Execute SQL query with fallback to mock data"""
    if not DB:
        # Return mock data based on query type
        if "daily_picks" in sql.lower():
            return []
        elif "positions" in sql.lower():
            return [("AAPL", 100.0, 150.00, 155.25)]
        elif "amm_pools" in sql.lower():
            return [("pool-001", "USDC/ETH", 125000000.0, 8.5, "low")]
        elif "affiliate_metrics" in sql.lower():
            return []
        return []
    
    with get_db_cursor() as cur:
        if not cur:
            return []
        
        cur.execute(sql, params or ())
        if fetch:
            return cur.fetchall()
        return []

def retry(fn, attempts: int = 3, delay: float = 1.5):
    """Retry function with exponential backoff"""
    for i in range(attempts):
        try:
            return fn()
        except Exception as e:
            if i == attempts - 1:
                raise e
            time.sleep(delay * (i + 1))

def cache_get(key: str) -> Optional[str]:
    """Get from cache with fallback"""
    if not R:
        return None
    try:
        return R.get(key)
    except:
        return None

def cache_set(key: str, value: str, expiry: int = 60) -> bool:
    """Set cache with fallback"""
    if not R:
        return False
    try:
        R.setex(key, expiry, value)
        return True
    except:
        return False

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Codex Market Dominion API",
        "version": "2.0.0",
        "status": "operational",
        "timestamp": datetime.datetime.now().isoformat(),
        "endpoints": {
            "market": "/market/quote/{symbol}",
            "picks": "/picks",
            "portfolio": "/portfolio/{portfolio_id}/positions",
            "affiliate": "/affiliate/stats",
            "amm": "/amm/pools",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected" if DB else "mock_mode",
        "cache": "connected" if R else "disabled",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "2.0.0"
    }

@app.get("/market/quote/{symbol}")
def quote(symbol: str):
    """Get market quote for symbol with caching"""
    # Check cache first
    cached_data = cache_get(f"quote:{symbol}")
    if cached_data:
        return json.loads(cached_data)
    
    def call_market_api():
        # Mock market data for demo - replace with real API
        import random
        base_price = random.uniform(100, 500)
        change = random.uniform(-10, 10)
        
        data = {
            "symbol": symbol.upper(),
            "price": round(base_price, 2),
            "change": round(change, 2),
            "change_percent": round(change / base_price * 100, 2),
            "volume": random.randint(1000000, 50000000),
            "atr": round(random.uniform(2, 15), 2),
            "timestamp": datetime.datetime.now().isoformat(),
            "source": "codex_market_api"
        }
        return data
    
    try:
        data = retry(call_market_api)
        # Cache for 60 seconds
        cache_set(f"quote:{symbol}", json.dumps(data), 60)
        return data
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Market data unavailable: {str(e)}")

@app.post("/picks")
def create_picks(req: PickRequest):
    """Create daily trading picks with scoring"""
    try:
        # Initialize scoring components
        scores = {
            "liquidity": 0.0,
            "volatility": 0.0, 
            "catalyst": 0.0,
            "technical": 0.0
        }
        
        symbol_details = []
        
        # Analyze each symbol
        for sym in req.symbols:
            try:
                qd = quote(sym)
                scores["liquidity"] += qd.get("volume", 0) / 1000000  # Normalize volume
                scores["volatility"] += qd.get("atr", 0)
                
                # Add technical scoring
                price_change = qd.get("change_percent", 0)
                if abs(price_change) > 2:
                    scores["technical"] += 10  # Significant movement
                
                # Add catalyst scoring (simplified)
                scores["catalyst"] += 5  # Base catalyst score
                
                symbol_details.append({
                    "symbol": sym,
                    "price": qd.get("price"),
                    "change_percent": qd.get("change_percent"),
                    "volume": qd.get("volume")
                })
                
            except Exception as e:
                print(f"Error processing {sym}: {e}")
                continue
        
        # Average scores
        num_symbols = len(req.symbols)
        if num_symbols > 0:
            scores = {k: round(v / num_symbols, 2) for k, v in scores.items()}
        
        # Calculate composite score
        composite_score = round(
            scores["technical"] * 0.3 +
            scores["liquidity"] * 0.25 +
            scores["volatility"] * 0.25 +
            scores["catalyst"] * 0.2, 
            2
        )
        
        # Store in database
        insert_sql = """
            INSERT INTO daily_picks (id, user_id, trade_date, symbols, scores, performance, created_at) 
            VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, %s)
        """
        
        performance_data = {
            "composite_score": composite_score,
            "symbol_count": num_symbols,
            "expected_return": round(composite_score * 0.1, 2),  # Simplified calculation
            "risk_level": "moderate" if composite_score < 50 else "aggressive",
            "symbol_details": symbol_details
        }
        
        q(insert_sql, (
            req.user_id, 
            req.trade_date, 
            req.symbols, 
            json.dumps(scores),
            json.dumps(performance_data),
            datetime.datetime.now()
        ), fetch=False)
        
        return {
            "ok": True,
            "scores": scores,
            "composite_score": composite_score,
            "performance": performance_data,
            "symbols_analyzed": num_symbols,
            "trade_date": req.trade_date
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating picks: {str(e)}")

@app.get("/portfolio/{portfolio_id}/positions")
def positions(portfolio_id: str):
    """Get portfolio positions with P&L calculations"""
    try:
        rows = q(
            "SELECT symbol, quantity, avg_cost, last_price, updated_at FROM positions WHERE portfolio_id = %s", 
            (portfolio_id,)
        )
        
        positions_data = []
        total_value = 0.0
        total_cost = 0.0
        
        for r in rows:
            symbol, quantity, avg_cost, last_price, updated_at = r
            
            # Get current market price if last_price is None
            current_price = float(last_price) if last_price else quote(symbol)["price"]
            
            market_value = float(quantity) * current_price
            cost_basis = float(quantity) * float(avg_cost)
            unrealized_pnl = market_value - cost_basis
            
            total_value += market_value
            total_cost += cost_basis
            
            positions_data.append({
                "symbol": symbol,
                "quantity": float(quantity),
                "avg_cost": float(avg_cost),
                "last_price": current_price,
                "market_value": round(market_value, 2),
                "cost_basis": round(cost_basis, 2),
                "unrealized_pnl": round(unrealized_pnl, 2),
                "return_percent": round((unrealized_pnl / cost_basis * 100), 2) if cost_basis > 0 else 0.0,
                "updated_at": updated_at.isoformat() if updated_at else None
            })
        
        return {
            "portfolio_id": portfolio_id,
            "positions": positions_data,
            "summary": {
                "total_positions": len(positions_data),
                "total_market_value": round(total_value, 2),
                "total_cost_basis": round(total_cost, 2),
                "total_unrealized_pnl": round(total_value - total_cost, 2),
                "portfolio_return_percent": round(((total_value - total_cost) / total_cost * 100), 2) if total_cost > 0 else 0.0
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching positions: {str(e)}")

@app.get("/affiliate/stats")
def affiliate_stats():
    """Get affiliate marketing statistics"""
    try:
        def call_affiliate_api():
            # Mock affiliate data - replace with real API calls
            return {
                "program": "TradingView_Premium",
                "clicks": 1247,
                "conversions": 43,
                "commission_usd": 2150.00,
                "conversion_rate": 3.45,
                "period": "last_30_days",
                "top_referrers": ["YouTube", "Twitter", "Blog"],
                "timestamp": datetime.datetime.now().isoformat()
            }
        
        data = retry(call_affiliate_api)
        
        # Store metrics in database
        insert_sql = """
            INSERT INTO affiliate_metrics (id, program, clicks, conversions, commission, conversion_rate, created_at) 
            VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, %s)
        """
        
        q(insert_sql, (
            data["program"], 
            data["clicks"], 
            data["conversions"], 
            data["commission_usd"],
            data["conversion_rate"],
            datetime.datetime.now()
        ), fetch=False)
        
        return data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching affiliate stats: {str(e)}")

@app.get("/amm/pools")
def amm_pools():
    """Get AMM pools ranked by TVL"""
    try:
        rows = q("SELECT id, pool_symbol, tvl_usd, apr, risk_tier, updated_at FROM amm_pools ORDER BY tvl_usd DESC LIMIT 20")
        
        pools_data = []
        for r in rows:
            pool_id, pool_symbol, tvl_usd, apr, risk_tier, updated_at = r
            pools_data.append({
                "id": str(pool_id),
                "pool": pool_symbol,
                "tvl_usd": float(tvl_usd) if tvl_usd else 0.0,
                "apr": float(apr) if apr else 0.0,
                "risk_tier": risk_tier,
                "updated_at": updated_at.isoformat() if updated_at else None
            })
        
        # If no pools in database, return mock data
        if not pools_data:
            pools_data = [
                {
                    "id": "pool-001",
                    "pool": "USDC/ETH",
                    "tvl_usd": 125000000.0,
                    "apr": 8.5,
                    "risk_tier": "low"
                },
                {
                    "id": "pool-002", 
                    "pool": "DAI/USDC",
                    "tvl_usd": 89000000.0,
                    "apr": 6.2,
                    "risk_tier": "low"
                },
                {
                    "id": "pool-003",
                    "pool": "WBTC/ETH",
                    "tvl_usd": 67000000.0,
                    "apr": 12.8,
                    "risk_tier": "medium"
                }
            ]
        
        return {
            "pools": pools_data,
            "total_pools": len(pools_data),
            "total_tvl": sum(pool["tvl_usd"] for pool in pools_data),
            "avg_apr": round(sum(pool["apr"] for pool in pools_data) / len(pools_data), 2) if pools_data else 0.0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching AMM pools: {str(e)}")

@app.post("/amm/swap")
def amm_swap(req: SwapRequest):
    """Execute AMM swap (placeholder for blockchain integration)"""
    try:
        # Generate transaction hash
        import secrets
        tx_hash = f"0x{secrets.token_hex(32)}"
        
        # Create event record
        event_payload = {
            "pool_id": req.pool_id,
            "from_asset": req.from_asset,
            "to_asset": req.to_asset,
            "amount": req.amount,
            "estimated_output": req.amount * 0.997,  # Simplified calculation with 0.3% fee
            "slippage": 0.3,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Store event in database
        insert_sql = """
            INSERT INTO amm_events (id, pool_id, event_type, payload, tx_hash, created_at) 
            VALUES (gen_random_uuid(), %s, 'swap', %s, %s, %s)
        """
        
        q(insert_sql, (
            req.pool_id,
            json.dumps(event_payload),
            tx_hash,
            datetime.datetime.now()
        ), fetch=False)
        
        return {
            "ok": True,
            "tx": {
                "hash": tx_hash,
                "status": "submitted",
                "estimated_confirmation": "2-5 minutes"
            },
            "swap_details": {
                "from_asset": req.from_asset,
                "to_asset": req.to_asset,
                "input_amount": req.amount,
                "estimated_output": event_payload["estimated_output"],
                "fee_percent": 0.3,
                "slippage_tolerance": event_payload["slippage"]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing swap: {str(e)}")

@app.get("/analytics/summary")
def analytics_summary():
    """Get comprehensive analytics summary"""
    try:
        # Portfolio analytics
        portfolio_sql = "SELECT COUNT(*) as portfolio_count FROM portfolios"
        position_sql = "SELECT COUNT(*) as position_count, SUM(quantity * avg_cost) as total_value FROM positions"
        
        portfolio_count = q(portfolio_sql)[0][0] if q(portfolio_sql) else 0
        position_data = q(position_sql)[0] if q(position_sql) else (0, 0)
        
        # Recent picks
        picks_sql = "SELECT COUNT(*) as recent_picks FROM daily_picks WHERE created_at > %s"
        week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        recent_picks = q(picks_sql, (week_ago,))[0][0] if q(picks_sql, (week_ago,)) else 0
        
        # Affiliate metrics
        affiliate_sql = "SELECT SUM(commission) as total_commission FROM affiliate_metrics WHERE created_at > %s"
        month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
        total_commission = q(affiliate_sql, (month_ago,))[0][0] if q(affiliate_sql, (month_ago,)) else 0.0
        
        return {
            "portfolios": {
                "total_portfolios": portfolio_count,
                "total_positions": position_data[0],
                "total_value_usd": float(position_data[1]) if position_data[1] else 0.0
            },
            "trading": {
                "picks_last_7_days": recent_picks,
                "avg_picks_per_day": round(recent_picks / 7, 1)
            },
            "affiliate": {
                "commission_last_30_days": float(total_commission) if total_commission else 0.0,
                "programs_active": 3  # Mock data
            },
            "defi": {
                "pools_monitored": 25,  # Mock data
                "total_tvl_tracked": 2500000000.0  # Mock data
            },
            "timestamp": datetime.datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating analytics: {str(e)}")

# Additional utility endpoints
@app.get("/market/trending")
def trending_symbols():
    """Get trending market symbols"""
    trending = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "BTC-USD", "ETH-USD"]
    
    quotes = []
    for symbol in trending[:5]:  # Limit to 5 for performance
        try:
            quote_data = quote(symbol)
            quotes.append(quote_data)
        except:
            continue
    
    return {
        "trending_symbols": quotes,
        "market_sentiment": "bullish",  # Mock data
        "top_movers": quotes[:3]
    }

@app.get("/portfolio/{portfolio_id}/performance")
def portfolio_performance(portfolio_id: str, days: int = 30):
    """Get portfolio performance over time"""
    # Mock time series data - in production, store daily snapshots
    performance_data = []
    base_value = 100000.0
    
    for i in range(days):
        date_point = datetime.datetime.now() - datetime.timedelta(days=days-i)
        # Simulate portfolio growth with some volatility
        daily_change = (i / days) * 0.15 + (hash(date_point.date()) % 20 - 10) / 1000
        value = base_value * (1 + daily_change)
        
        performance_data.append({
            "date": date_point.date().isoformat(),
            "portfolio_value": round(value, 2),
            "daily_return": round(daily_change * 100, 2)
        })
    
    return {
        "portfolio_id": portfolio_id,
        "period_days": days,
        "performance": performance_data,
        "summary": {
            "starting_value": performance_data[0]["portfolio_value"],
            "ending_value": performance_data[-1]["portfolio_value"],
            "total_return": round((performance_data[-1]["portfolio_value"] / performance_data[0]["portfolio_value"] - 1) * 100, 2),
            "best_day": max(performance_data, key=lambda x: x["daily_return"]),
            "worst_day": min(performance_data, key=lambda x: x["daily_return"])
        }
    }

if __name__ == "__main__":
    print("🚀 Starting Codex Market Dominion API...")
    print("📊 Database:", "Connected" if DB else "Mock Mode")
    print("💾 Cache:", "Connected" if R else "Disabled")
    print("🌐 API Documentation: http://localhost:8000/docs")
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)