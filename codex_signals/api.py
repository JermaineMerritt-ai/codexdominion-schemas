"""
🔥 CODEX SIGNALS API SERVICE 📊
FastAPI REST API for Advanced Market Intelligence

The Merritt Method™ - Scalable Financial Intelligence
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from codex_signals.data_feeds import DataFeedManager, MockDataFeed
# Import Codex Signals components
from codex_signals.engine import MarketSnapshot, Pick, Position, SignalsEngine
from codex_signals.integration import CodexSignalsIntegration

# Initialize FastAPI app
app = FastAPI(
    title="🔥 Codex Signals API",
    description="Advanced Market Intelligence & Portfolio Signals Engine",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware for web dashboard integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
engine = SignalsEngine()
data_feed = DataFeedManager()
integration = CodexSignalsIntegration()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Pydantic models for request/response validation
class MarketSnapshotModel(BaseModel):
    symbol: str = Field(..., description="Asset symbol (e.g., 'MSFT', 'BTC-USD')")
    price: float = Field(..., gt=0, description="Current market price")
    vol_30d: float = Field(
        ..., ge=0, le=2, description="30-day realized volatility [0.0-2.0]"
    )
    trend_20d: float = Field(
        ..., ge=-1, le=1, description="20-day trend score [-1.0, 1.0]"
    )
    liquidity_rank: int = Field(..., ge=1, description="Liquidity rank (1=highest)")


class PositionModel(BaseModel):
    symbol: str = Field(..., description="Asset symbol")
    weight: float = Field(
        ..., ge=0, le=1, description="Current portfolio weight [0.0-1.0]"
    )
    allowed_max: float = Field(
        ..., ge=0, le=1, description="Maximum allowed weight [0.0-1.0]"
    )


class EngineConfigModel(BaseModel):
    exposure_cap: float = Field(
        0.10, ge=0.01, le=0.50, description="Maximum weight per position"
    )
    vol_alpha: float = Field(
        0.25, ge=0.10, le=0.60, description="Volatility threshold for Alpha tier"
    )
    trend_alpha: float = Field(
        0.35, ge=0.10, le=0.80, description="Trend threshold for Alpha tier"
    )


class DailySignalsRequest(BaseModel):
    market: List[MarketSnapshotModel] = Field(
        ..., description="List of market snapshots"
    )
    positions: List[PositionModel] = Field(
        default=[], description="Current portfolio positions"
    )
    engine_config: Optional[EngineConfigModel] = Field(
        None, description="Engine configuration override"
    )


class SignalsResponse(BaseModel):
    generated_at: str
    tier_counts: Dict[str, int]
    banner: str
    picks: List[Dict[str, Any]]
    market_summary: Optional[Dict[str, Any]] = None
    execution_time_ms: Optional[float] = None


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers and monitoring"""
    try:
        # Test engine functionality
        test_snapshot = MarketSnapshot(
            symbol="TEST", price=100.0, vol_30d=0.25, trend_20d=0.35, liquidity_rank=50
        )
        test_tier = engine.classify_tier(test_snapshot)

        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "engine_status": "operational",
            "test_classification": test_tier,
            "services": {
                "signals_engine": True,
                "data_feed": True,
                "integration": True,
            },
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


# Main signals generation endpoint (your enhanced version)
@app.post("/signals/daily", response_model=SignalsResponse)
async def daily_signals(request: DailySignalsRequest):
    """
    Generate daily portfolio signals from market data
    Enhanced version of your original endpoint
    """
    try:
        start_time = datetime.utcnow()

        # Convert Pydantic models to dataclasses
        market = [
            MarketSnapshot(
                symbol=m.symbol,
                price=m.price,
                vol_30d=m.vol_30d,
                trend_20d=m.trend_20d,
                liquidity_rank=m.liquidity_rank,
            )
            for m in request.market
        ]

        positions = {
            p.symbol: Position(
                symbol=p.symbol, weight=p.weight, allowed_max=p.allowed_max
            )
            for p in request.positions
        }

        # Configure engine if specified
        if request.engine_config:
            global engine
            engine = SignalsEngine(
                exposure_cap=request.engine_config.exposure_cap,
                vol_alpha=request.engine_config.vol_alpha,
                trend_alpha=request.engine_config.trend_alpha,
            )

        # Generate signals
        snapshot = engine.generate(market, positions)

        # Add execution timing
        end_time = datetime.utcnow()
        execution_time = (end_time - start_time).total_seconds() * 1000

        # Add market summary
        market_summary = {
            "total_symbols": len(market),
            "avg_volatility": (
                sum(m.vol_30d for m in market) / len(market) if market else 0
            ),
            "avg_trend": (
                sum(m.trend_20d for m in market) / len(market) if market else 0
            ),
            "high_liquidity_count": sum(1 for m in market if m.liquidity_rank <= 50),
        }

        # Enhanced response
        response_data = {
            **snapshot,
            "market_summary": market_summary,
            "execution_time_ms": round(execution_time, 2),
        }

        logger.info(
            f"Generated signals for {len(market)} symbols in {execution_time:.2f}ms"
        )
        return SignalsResponse(**response_data)

    except Exception as e:
        logger.error(f"Error generating daily signals: {e}")
        raise HTTPException(
            status_code=500, detail=f"Signal generation failed: {str(e)}"
        )


# Mock data endpoint
@app.get("/signals/mock")
async def mock_signals():
    """Generate signals using mock market data for testing"""
    try:
        market = MockDataFeed.get_mock_snapshots()
        positions = {
            "MSFT": Position(symbol="MSFT", weight=0.04, allowed_max=0.08),
            "AAPL": Position(symbol="AAPL", weight=0.03, allowed_max=0.06),
            "BTC-USD": Position(symbol="BTC-USD", weight=0.02, allowed_max=0.06),
        }

        snapshot = engine.generate(market, positions)

        # Add mock data indicators
        snapshot["data_source"] = "mock"
        snapshot["mock_symbols"] = len(market)

        logger.info("Generated mock signals successfully")
        return snapshot

    except Exception as e:
        logger.error(f"Error generating mock signals: {e}")
        raise HTTPException(status_code=500, detail=f"Mock signals failed: {str(e)}")


# Live data endpoint (requires data feed configuration)
@app.get("/signals/live")
async def live_signals():
    """Generate signals using live market data"""
    try:
        market = data_feed.get_market_snapshots()

        if not market:
            raise HTTPException(
                status_code=503,
                detail="No live market data available. Check data feed configuration.",
            )

        # Load positions from integration
        positions = integration.load_positions_from_ledger()

        snapshot = engine.generate(market, positions)
        snapshot["data_source"] = "live"

        logger.info(f"Generated live signals for {len(market)} symbols")
        return snapshot

    except Exception as e:
        logger.error(f"Error generating live signals: {e}")
        raise HTTPException(status_code=500, detail=f"Live signals failed: {str(e)}")


# Dawn dispatch integration endpoint
@app.get("/signals/dawn")
async def dawn_signals():
    """Get signals summary for dawn dispatch integration"""
    try:
        summary = integration.get_signals_for_dawn_dispatch()

        if "error" in summary:
            raise HTTPException(status_code=500, detail=summary["error"])

        logger.info("Generated dawn dispatch signals summary")
        return summary

    except Exception as e:
        logger.error(f"Error generating dawn signals: {e}")
        raise HTTPException(status_code=500, detail=f"Dawn signals failed: {str(e)}")


# Engine configuration endpoints
@app.get("/engine/config")
async def get_engine_config():
    """Get current engine configuration"""
    return {
        "exposure_cap": engine.exposure_cap,
        "vol_alpha": engine.vol_alpha,
        "trend_alpha": engine.trend_alpha,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/engine/config")
async def update_engine_config(config: EngineConfigModel):
    """Update engine configuration"""
    try:
        global engine
        engine = SignalsEngine(
            exposure_cap=config.exposure_cap,
            vol_alpha=config.vol_alpha,
            trend_alpha=config.trend_alpha,
        )

        logger.info(f"Updated engine configuration: {config}")
        return {
            "message": "Engine configuration updated successfully",
            "config": config.dict(),
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"Error updating engine config: {e}")
        raise HTTPException(status_code=500, detail=f"Config update failed: {str(e)}")


# Tier classification endpoint
@app.post("/classify/tier")
async def classify_tier(snapshot: MarketSnapshotModel):
    """Classify a single market snapshot into risk tier"""
    try:
        market_snapshot = MarketSnapshot(
            symbol=snapshot.symbol,
            price=snapshot.price,
            vol_30d=snapshot.vol_30d,
            trend_20d=snapshot.trend_20d,
            liquidity_rank=snapshot.liquidity_rank,
        )

        tier = engine.classify_tier(market_snapshot)
        rationale = engine.rationale(tier, market_snapshot)
        risk_factors = engine.risk_factors(market_snapshot)

        return {
            "symbol": snapshot.symbol,
            "tier": tier,
            "rationale": rationale,
            "risk_factors": risk_factors,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"Error classifying tier: {e}")
        raise HTTPException(
            status_code=500, detail=f"Tier classification failed: {str(e)}"
        )


# Portfolio analysis endpoint
@app.post("/portfolio/analysis")
async def portfolio_analysis(request: DailySignalsRequest):
    """Comprehensive portfolio analysis with rebalancing recommendations"""
    try:
        # Generate signals first
        signals_response = await daily_signals(request)

        # Get rebalancing recommendations
        market = [
            MarketSnapshot(
                symbol=m.symbol,
                price=m.price,
                vol_30d=m.vol_30d,
                trend_20d=m.trend_20d,
                liquidity_rank=m.liquidity_rank,
            )
            for m in request.market
        ]

        positions = {
            p.symbol: Position(
                symbol=p.symbol, weight=p.weight, allowed_max=p.allowed_max
            )
            for p in request.positions
        }

        snapshot = engine.generate(market, positions)
        rebalance_analysis = integration.update_positions_from_signals(
            snapshot, auto_rebalance=False
        )

        return {
            "signals": signals_response.dict(),
            "rebalancing": rebalance_analysis,
            "analysis_timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"Error in portfolio analysis: {e}")
        raise HTTPException(
            status_code=500, detail=f"Portfolio analysis failed: {str(e)}"
        )


# Background task for automated signals generation
@app.post("/signals/schedule")
async def schedule_signals(background_tasks: BackgroundTasks):
    """Schedule background signals generation and archiving"""

    def generate_and_archive():
        try:
            logger.info("Starting scheduled signals generation")

            # Generate signals report
            report = integration.generate_signals_report(use_live_data=True)

            if "error" not in report:
                # Save to file
                integration.save_signals_snapshot(report)
                logger.info("Scheduled signals generated and archived successfully")
            else:
                logger.error(f"Scheduled signals generation failed: {report['error']}")

        except Exception as e:
            logger.error(f"Background signals generation failed: {e}")

    background_tasks.add_task(generate_and_archive)

    return {
        "message": "Signals generation scheduled",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/bulletin", tags=["Reports"])
async def generate_bulletin(
    format: str = Query("md", description="Output format: 'txt' or 'md'"),
    use_live_data: bool = Query(False, description="Use live market data"),
):
    """
    Generate formatted bulletin for sharing

    - **format**: Output format - 'txt' for plain text or 'md' for Markdown
    - **use_live_data**: Whether to use live market data (if available)

    Returns formatted bulletin content perfect for sharing or publishing
    """
    try:
        # Generate signals snapshot
        if use_live_data:
            snapshots = data_feed.get_market_snapshots()
        else:
            snapshots = MockDataFeed.get_mock_snapshots()

        positions = integration.load_positions_from_ledger()
        signals_snapshot = engine.generate(snapshots, positions)

        if format == "md":
            from .integration import bulletin_md

            bulletin_content = bulletin_md(signals_snapshot)
        else:
            # Text format
            bulletin_content = f"""CODEX SIGNALS DAILY BULLETIN - {signals_snapshot['generated_at']}

{signals_snapshot['banner']}

TIER DISTRIBUTION:
- Alpha Tier: {signals_snapshot['tier_counts']['Alpha']} positions
- Beta Tier: {signals_snapshot['tier_counts']['Beta']} positions
- Gamma Tier: {signals_snapshot['tier_counts']['Gamma']} positions
- Delta Tier: {signals_snapshot['tier_counts']['Delta']} positions

POSITION RECOMMENDATIONS:
"""

            for pick in signals_snapshot["picks"]:
                bulletin_content += f"""
{pick['symbol']} - Tier {pick['tier']}
Target Weight: {pick['target_weight']:.2%}
Rationale: {pick['rationale']}
Risk Factors: {', '.join(pick['risk_factors']) if pick['risk_factors'] else 'None'}
"""

        return {
            "format": format,
            "content": bulletin_content,
            "generated_at": signals_snapshot["generated_at"],
            "tier_counts": signals_snapshot["tier_counts"],
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating bulletin: {str(e)}"
        )


# Statistics and metrics endpoint
@app.get("/metrics")
async def get_metrics():
    """Get API and engine performance metrics"""
    try:
        # Load signals history for metrics
        history_file = "signals_history.json"
        metrics = {
            "total_requests": 0,
            "avg_execution_time": 0,
            "signals_generated_today": 0,
            "uptime_start": datetime.utcnow().isoformat(),
            "engine_config": {
                "exposure_cap": engine.exposure_cap,
                "vol_alpha": engine.vol_alpha,
                "trend_alpha": engine.trend_alpha,
            },
        }

        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                history = json.load(f)

            today = datetime.utcnow().date()
            today_signals = [
                h
                for h in history
                if datetime.fromisoformat(h.get("timestamp", "2000-01-01")).date()
                == today
            ]

            metrics["signals_generated_today"] = len(today_signals)
            metrics["total_historical_signals"] = len(history)

        return metrics

    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(
            status_code=500, detail=f"Metrics retrieval failed: {str(e)}"
        )


# Root endpoint with API information
@app.get("/")
async def root():
    """API root with service information"""
    return {
        "service": "🔥 Codex Signals API 📊",
        "description": "Advanced Market Intelligence & Portfolio Signals Engine",
        "version": "1.0.0",
        "motto": "The Merritt Method™ - Scalable Financial Intelligence",
        "endpoints": {
            "daily_signals": "/signals/daily (POST)",
            "mock_signals": "/signals/mock (GET)",
            "live_signals": "/signals/live (GET)",
            "dawn_signals": "/signals/dawn (GET)",
            "tier_classification": "/classify/tier (POST)",
            "portfolio_analysis": "/portfolio/analysis (POST)",
            "engine_config": "/engine/config (GET/POST)",
            "health_check": "/health (GET)",
            "metrics": "/metrics (GET)",
            "documentation": "/docs (GET)",
        },
        "timestamp": datetime.utcnow().isoformat(),
    }


# Error handler for validation errors
@app.exception_handler(422)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "detail": "Please check your request data format",
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


# Global exception handler
@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


if __name__ == "__main__":
    import uvicorn

    # Development server
    uvicorn.run(
        "codex_signals.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
