"""
Codex Dominion Database Integration Module
Advanced PostgreSQL integration for trading and portfolio management
"""

import os
import uuid
import asyncio
import psycopg2
import psycopg2.extras
import json
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass
from contextlib import asynccontextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Configuration
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'codex_dominion'),
    'user': os.getenv('DB_USER', 'codex_admin'),
    'password': os.getenv('DB_PASSWORD', 'your_secure_password'),
    'min_connections': 5,
    'max_connections': 20
}

# Data Models
@dataclass
class Portfolio:
    id: str
    owner_id: str
    risk_tier: str  # conservative, moderate, aggressive
    created_at: datetime
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            owner_id=data['owner_id'],
            risk_tier=data['risk_tier'],
            created_at=data['created_at']
        )

@dataclass
class Position:
    id: str
    portfolio_id: str
    symbol: str
    quantity: Decimal
    avg_cost: Decimal
    last_price: Optional[Decimal]
    updated_at: datetime
    
    @property
    def market_value(self) -> Decimal:
        return self.quantity * (self.last_price or self.avg_cost)
    
    @property
    def unrealized_pnl(self) -> Decimal:
        if not self.last_price:
            return Decimal('0')
        return (self.last_price - self.avg_cost) * self.quantity
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            portfolio_id=data['portfolio_id'],
            symbol=data['symbol'],
            quantity=Decimal(str(data['quantity'])),
            avg_cost=Decimal(str(data['avg_cost'])),
            last_price=Decimal(str(data['last_price'])) if data['last_price'] else None,
            updated_at=data['updated_at']
        )

@dataclass
class DailyPick:
    id: str
    user_id: str
    trade_date: date
    symbols: List[str]
    scores: Dict[str, Any]
    performance: Dict[str, Any]
    created_at: datetime
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            trade_date=data['trade_date'],
            symbols=data['symbols'],
            scores=data['scores'] or {},
            performance=data['performance'] or {},
            created_at=data['created_at']
        )

@dataclass
class AffiliateMetrics:
    id: str
    program: str
    clicks: int
    conversions: int
    commission: Decimal
    captured_at: datetime
    
    @property
    def conversion_rate(self) -> float:
        return (self.conversions / self.clicks * 100) if self.clicks > 0 else 0.0
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            program=data['program'],
            clicks=data['clicks'],
            conversions=data['conversions'],
            commission=Decimal(str(data['commission'])),
            captured_at=data['captured_at']
        )

@dataclass
class AmmPool:
    id: str
    pool_symbol: str
    tvl_usd: Decimal
    apr: Decimal
    risk_tier: Optional[str]
    updated_at: datetime
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            pool_symbol=data['pool_symbol'],
            tvl_usd=Decimal(str(data['tvl_usd'])),
            apr=Decimal(str(data['apr'])),
            risk_tier=data['risk_tier'],
            updated_at=data['updated_at']
        )

@dataclass
class AmmEvent:
    id: str
    pool_id: str
    event_type: str  # stake, unstake, swap, harvest
    payload: Dict[str, Any]
    tx_hash: Optional[str]
    created_at: datetime
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            pool_id=data['pool_id'],
            event_type=data['event_type'],
            payload=data['payload'] or {},
            tx_hash=data['tx_hash'],
            created_at=data['created_at']
        )

class CodexDatabase:
    """Main database connection and operations manager"""
    
    def __init__(self):
        self.pool = None
        self.connected = False
    
    async def connect(self):
        """Initialize database connection pool"""
        try:
            # Using psycopg2 connection instead of asyncpg pool
            self.connection = psycopg2.connect(**DATABASE_CONFIG)
            self.connected = True
            logger.info("✅ Database connection pool established")
            return True
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            self.connected = False
            return False
    
    async def disconnect(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            self.connected = False
            logger.info("🔌 Database connection pool closed")
    
    @asynccontextmanager
    async def get_connection(self):
        """Get database connection from pool"""
        if not self.connected:
            await self.connect()
        
        async with self.pool.acquire() as conn:
            yield conn
    
    # Portfolio Operations
    async def create_portfolio(self, owner_id: str, risk_tier: str) -> Portfolio:
        """Create new portfolio"""
        portfolio_id = str(uuid.uuid4())
        
        async with self.get_connection() as conn:
            await conn.execute("""
                INSERT INTO portfolios (id, owner_id, risk_tier, created_at)
                VALUES ($1, $2, $3, $4)
            """, portfolio_id, owner_id, risk_tier, datetime.now())
            
            row = await conn.fetchrow("""
                SELECT * FROM portfolios WHERE id = $1
            """, portfolio_id)
            
            return Portfolio.from_dict(dict(row))
    
    async def get_portfolio(self, portfolio_id: str) -> Optional[Portfolio]:
        """Get portfolio by ID"""
        async with self.get_connection() as conn:
            row = await conn.fetchrow("""
                SELECT * FROM portfolios WHERE id = $1
            """, portfolio_id)
            
            return Portfolio.from_dict(dict(row)) if row else None
    
    async def get_user_portfolios(self, owner_id: str) -> List[Portfolio]:
        """Get all portfolios for a user"""
        async with self.get_connection() as conn:
            rows = await conn.fetch("""
                SELECT * FROM portfolios WHERE owner_id = $1
                ORDER BY created_at DESC
            """, owner_id)
            
            return [Portfolio.from_dict(dict(row)) for row in rows]
    
    # Position Operations
    async def add_position(self, portfolio_id: str, symbol: str, 
                          quantity: Decimal, avg_cost: Decimal) -> Position:
        """Add new position to portfolio"""
        position_id = str(uuid.uuid4())
        
        async with self.get_connection() as conn:
            await conn.execute("""
                INSERT INTO positions (id, portfolio_id, symbol, quantity, avg_cost, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6)
            """, position_id, portfolio_id, symbol, quantity, avg_cost, datetime.now())
            
            row = await conn.fetchrow("""
                SELECT * FROM positions WHERE id = $1
            """, position_id)
            
            return Position.from_dict(dict(row))
    
    async def update_position_price(self, position_id: str, last_price: Decimal):
        """Update position last price"""
        async with self.get_connection() as conn:
            await conn.execute("""
                UPDATE positions SET last_price = $1, updated_at = $2
                WHERE id = $3
            """, last_price, datetime.now(), position_id)
    
    async def get_portfolio_positions(self, portfolio_id: str) -> List[Position]:
        """Get all positions for a portfolio"""
        async with self.get_connection() as conn:
            rows = await conn.fetch("""
                SELECT * FROM positions WHERE portfolio_id = $1
                ORDER BY symbol
            """, portfolio_id)
            
            return [Position.from_dict(dict(row)) for row in rows]
    
    async def get_portfolio_performance(self, portfolio_id: str) -> Dict[str, Any]:
        """Calculate comprehensive portfolio performance metrics"""
        positions = await self.get_portfolio_positions(portfolio_id)
        
        total_cost = sum(pos.quantity * pos.avg_cost for pos in positions)
        total_market_value = sum(pos.market_value for pos in positions)
        total_unrealized_pnl = sum(pos.unrealized_pnl for pos in positions)
        
        return {
            'total_positions': len(positions),
            'total_cost_basis': float(total_cost),
            'total_market_value': float(total_market_value),
            'unrealized_pnl': float(total_unrealized_pnl),
            'return_percentage': float((total_unrealized_pnl / total_cost * 100)) if total_cost > 0 else 0.0,
            'positions': [
                {
                    'symbol': pos.symbol,
                    'quantity': float(pos.quantity),
                    'avg_cost': float(pos.avg_cost),
                    'last_price': float(pos.last_price) if pos.last_price else None,
                    'market_value': float(pos.market_value),
                    'unrealized_pnl': float(pos.unrealized_pnl),
                    'weight': float(pos.market_value / total_market_value * 100) if total_market_value > 0 else 0.0
                }
                for pos in positions
            ]
        }
    
    # Daily Picks Operations
    async def create_daily_pick(self, user_id: str, trade_date: date, 
                               symbols: List[str], scores: Dict[str, Any],
                               performance: Dict[str, Any]) -> DailyPick:
        """Create daily trading pick"""
        pick_id = str(uuid.uuid4())
        
        async with self.get_connection() as conn:
            await conn.execute("""
                INSERT INTO daily_picks (id, user_id, trade_date, symbols, scores, performance, created_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            """, pick_id, user_id, trade_date, symbols, json.dumps(scores), 
                json.dumps(performance), datetime.now())
            
            row = await conn.fetchrow("""
                SELECT * FROM daily_picks WHERE id = $1
            """, pick_id)
            
            return DailyPick.from_dict(dict(row))
    
    async def get_recent_picks(self, user_id: str, days: int = 30) -> List[DailyPick]:
        """Get recent daily picks for user"""
        async with self.get_connection() as conn:
            rows = await conn.fetch("""
                SELECT * FROM daily_picks 
                WHERE user_id = $1 AND trade_date >= CURRENT_DATE - INTERVAL '%s days'
                ORDER BY trade_date DESC
            """, user_id, days)
            
            return [DailyPick.from_dict(dict(row)) for row in rows]
    
    # Affiliate Metrics Operations
    async def record_affiliate_metrics(self, program: str, clicks: int, 
                                     conversions: int, commission: Decimal) -> AffiliateMetrics:
        """Record affiliate marketing metrics"""
        metrics_id = str(uuid.uuid4())
        
        async with self.get_connection() as conn:
            await conn.execute("""
                INSERT INTO affiliate_metrics (id, program, clicks, conversions, commission, captured_at)
                VALUES ($1, $2, $3, $4, $5, $6)
            """, metrics_id, program, clicks, conversions, commission, datetime.now())
            
            row = await conn.fetchrow("""
                SELECT * FROM affiliate_metrics WHERE id = $1
            """, metrics_id)
            
            return AffiliateMetrics.from_dict(dict(row))
    
    async def get_affiliate_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get affiliate performance summary"""
        async with self.get_connection() as conn:
            rows = await conn.fetch("""
                SELECT program, 
                       SUM(clicks) as total_clicks,
                       SUM(conversions) as total_conversions,
                       SUM(commission) as total_commission
                FROM affiliate_metrics 
                WHERE captured_at >= CURRENT_TIMESTAMP - INTERVAL '%s days'
                GROUP BY program
                ORDER BY total_commission DESC
            """, days)
            
            total_commission = sum(row['total_commission'] for row in rows)
            total_clicks = sum(row['total_clicks'] for row in rows)
            total_conversions = sum(row['total_conversions'] for row in rows)
            
            return {
                'total_commission': float(total_commission),
                'total_clicks': total_clicks,
                'total_conversions': total_conversions,
                'overall_conversion_rate': (total_conversions / total_clicks * 100) if total_clicks > 0 else 0.0,
                'programs': [
                    {
                        'program': row['program'],
                        'clicks': row['total_clicks'],
                        'conversions': row['total_conversions'],
                        'commission': float(row['total_commission']),
                        'conversion_rate': (row['total_conversions'] / row['total_clicks'] * 100) if row['total_clicks'] > 0 else 0.0
                    }
                    for row in rows
                ]
            }
    
    # AMM Pool Operations
    async def create_amm_pool(self, pool_symbol: str, tvl_usd: Decimal, 
                             apr: Decimal, risk_tier: Optional[str] = None) -> AmmPool:
        """Create AMM pool record"""
        pool_id = str(uuid.uuid4())
        
        async with self.get_connection() as conn:
            await conn.execute("""
                INSERT INTO amm_pools (id, pool_symbol, tvl_usd, apr, risk_tier, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6)
            """, pool_id, pool_symbol, tvl_usd, apr, risk_tier, datetime.now())
            
            row = await conn.fetchrow("""
                SELECT * FROM amm_pools WHERE id = $1
            """, pool_id)
            
            return AmmPool.from_dict(dict(row))
    
    async def record_amm_event(self, pool_id: str, event_type: str, 
                              payload: Dict[str, Any], tx_hash: Optional[str] = None) -> AmmEvent:
        """Record AMM event"""
        event_id = str(uuid.uuid4())
        
        async with self.get_connection() as conn:
            await conn.execute("""
                INSERT INTO amm_events (id, pool_id, event_type, payload, tx_hash, created_at)
                VALUES ($1, $2, $3, $4, $5, $6)
            """, event_id, pool_id, event_type, json.dumps(payload), tx_hash, datetime.now())
            
            row = await conn.fetchrow("""
                SELECT * FROM amm_events WHERE id = $1
            """, event_id)
            
            return AmmEvent.from_dict(dict(row))
    
    async def get_top_amm_pools(self, limit: int = 10) -> List[AmmPool]:
        """Get top AMM pools by TVL"""
        async with self.get_connection() as conn:
            rows = await conn.fetch("""
                SELECT * FROM amm_pools 
                ORDER BY tvl_usd DESC 
                LIMIT $1
            """, limit)
            
            return [AmmPool.from_dict(dict(row)) for row in rows]

# Global database instance
db = CodexDatabase()

# Utility functions for sync operations
def sync_db_operation(coro):
    """Run async database operation in sync context"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)

# Quick access functions for common operations
def get_portfolio_summary(portfolio_id: str) -> Dict[str, Any]:
    """Sync wrapper for portfolio performance"""
    return sync_db_operation(db.get_portfolio_performance(portfolio_id))

def get_affiliate_performance(days: int = 30) -> Dict[str, Any]:
    """Sync wrapper for affiliate summary"""
    return sync_db_operation(db.get_affiliate_summary(days))

def get_top_pools(limit: int = 10) -> List[Dict[str, Any]]:
    """Sync wrapper for top AMM pools"""
    pools = sync_db_operation(db.get_top_amm_pools(limit))
    return [
        {
            'pool_symbol': pool.pool_symbol,
            'tvl_usd': float(pool.tvl_usd),
            'apr': float(pool.apr),
            'risk_tier': pool.risk_tier
        }
        for pool in pools
    ]

if __name__ == "__main__":
    # Test database connection
    async def test_connection():
        await db.connect()
        if db.connected:
            print("✅ Database connection successful!")
        else:
            print("❌ Database connection failed!")
        await db.disconnect()
    
    sync_db_operation(test_connection())