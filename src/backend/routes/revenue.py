"""
Revenue API - Multi-Platform Revenue Tracking
Tracks revenue across 8 platforms with real-time sales feed
"""
from datetime import datetime, timedelta
from typing import List, Optional
from enum import Enum

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
import random

router = APIRouter(prefix="/api/revenue", tags=["Revenue"])


class SaleStatus(str, Enum):
    """Sale status enum"""
    COMPLETED = "completed"
    PENDING = "pending"
    REFUNDED = "refunded"
    FAILED = "failed"


class Platform(str, Enum):
    """Revenue platforms"""
    SHOPIFY = "shopify"
    STRIPE = "stripe"
    PAYPAL = "paypal"
    WOOCOMMERCE = "woocommerce"
    AFFILIATE = "affiliate"
    DOWNLOADS = "downloads"
    SUBSCRIPTIONS = "subscriptions"
    CONSULTING = "consulting"


class Sale(BaseModel):
    """Individual sale record"""
    id: str
    platform: Platform
    product: str
    amount: float
    customer: str
    status: SaleStatus
    timestamp: datetime
    transaction_id: str
    fee: float = 0.0
    net_amount: float


class PlatformBalance(BaseModel):
    """Balance for a specific platform"""
    platform: Platform
    balance: float
    pending_balance: float
    total_sales: float
    sales_count: int
    change_24h: float
    last_updated: datetime


class RevenueMetrics(BaseModel):
    """Overall revenue metrics"""
    total_revenue: float
    available_balance: float
    pending_clearance: float
    total_sales: int
    revenue_change_24h: float
    average_sale: float
    top_platform: Platform
    platforms_count: int


class WithdrawalRequest(BaseModel):
    """Withdrawal request"""
    platform: Platform
    amount: float
    payment_method: str
    account_info: str


# Mock data storage (replace with database in production)
_sales_history: List[Sale] = []
_platform_balances = {}


def _initialize_mock_data():
    """Initialize mock data for testing"""
    global _platform_balances

    _platform_balances = {
        Platform.SHOPIFY: {
            "balance": 12450.75,
            "pending": 2340.50,
            "total": 14791.25,
            "count": 87,
            "change": 8.5
        },
        Platform.STRIPE: {
            "balance": 8920.30,
            "pending": 1200.00,
            "total": 10120.30,
            "count": 45,
            "change": 12.3
        },
        Platform.PAYPAL: {
            "balance": 5680.90,
            "pending": 890.25,
            "total": 6571.15,
            "count": 34,
            "change": -2.1
        },
        Platform.WOOCOMMERCE: {
            "balance": 3420.60,
            "pending": 450.00,
            "total": 3870.60,
            "count": 28,
            "change": 5.7
        },
        Platform.AFFILIATE: {
            "balance": 2150.40,
            "pending": 680.75,
            "total": 2831.15,
            "count": 56,
            "change": 15.2
        },
        Platform.DOWNLOADS: {
            "balance": 1890.25,
            "pending": 0.00,
            "total": 1890.25,
            "count": 42,
            "change": 6.8
        },
        Platform.SUBSCRIPTIONS: {
            "balance": 4560.00,
            "pending": 0.00,
            "total": 4560.00,
            "count": 38,
            "change": 3.4
        },
        Platform.CONSULTING: {
            "balance": 7200.00,
            "pending": 3600.00,
            "total": 10800.00,
            "count": 6,
            "change": 20.0
        }
    }

    # Generate mock sales history
    products = [
        "Premium Course Bundle", "Monthly Subscription", "E-book",
        "Physical Product", "Consulting Session", "Software License",
        "Digital Download", "Affiliate Commission"
    ]
    customers = [
        "John Smith", "Sarah Johnson", "Mike Chen", "Emily Davis",
        "Partner #47", "Customer #892", "Jane Doe", "Alex Rivera"
    ]

    for i in range(50):
        platform = random.choice(list(Platform))
        amount = round(random.uniform(25, 500), 2)
        fee = round(amount * 0.029 + 0.30, 2)  # Standard payment processing fee

        _sales_history.append(Sale(
            id=f"sale-{1000 + i}",
            platform=platform,
            product=random.choice(products),
            amount=amount,
            customer=random.choice(customers),
            status=random.choice([SaleStatus.COMPLETED, SaleStatus.PENDING]),
            timestamp=datetime.now() - timedelta(minutes=random.randint(5, 1440)),
            transaction_id=f"txn-{random.randint(100000, 999999)}",
            fee=fee,
            net_amount=amount - fee
        ))


# Initialize mock data on module load
_initialize_mock_data()


@router.get("/platforms", response_model=List[PlatformBalance])
async def get_platform_balances():
    """
    Get balance information for all revenue platforms
    """
    balances = []

    for platform, data in _platform_balances.items():
        balances.append(PlatformBalance(
            platform=platform,
            balance=data["balance"],
            pending_balance=data["pending"],
            total_sales=data["total"],
            sales_count=data["count"],
            change_24h=data["change"],
            last_updated=datetime.now()
        ))

    return balances


@router.get("/platforms/{platform}", response_model=PlatformBalance)
async def get_platform_balance(platform: Platform):
    """
    Get balance for a specific platform
    """
    if platform not in _platform_balances:
        raise HTTPException(status_code=404, detail=f"Platform {platform} not found")

    data = _platform_balances[platform]

    return PlatformBalance(
        platform=platform,
        balance=data["balance"],
        pending_balance=data["pending"],
        total_sales=data["total"],
        sales_count=data["count"],
        change_24h=data["change"],
        last_updated=datetime.now()
    )


@router.get("/sales", response_model=List[Sale])
async def get_sales_history(
    platform: Optional[Platform] = None,
    status: Optional[SaleStatus] = None,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """
    Get sales history with optional filtering
    """
    # Filter sales
    filtered_sales = _sales_history

    if platform:
        filtered_sales = [s for s in filtered_sales if s.platform == platform]

    if status:
        filtered_sales = [s for s in filtered_sales if s.status == status]

    # Sort by timestamp (newest first)
    filtered_sales.sort(key=lambda x: x.timestamp, reverse=True)

    # Apply pagination
    return filtered_sales[offset:offset + limit]


@router.get("/metrics", response_model=RevenueMetrics)
async def get_revenue_metrics():
    """
    Get overall revenue metrics across all platforms
    """
    total_revenue = sum(data["total"] for data in _platform_balances.values())
    available_balance = sum(data["balance"] for data in _platform_balances.values())
    pending_clearance = sum(data["pending"] for data in _platform_balances.values())
    total_sales_count = sum(data["count"] for data in _platform_balances.values())

    # Calculate weighted average change
    total_change = sum(
        data["change"] * data["total"]
        for data in _platform_balances.values()
    )
    avg_change = total_change / total_revenue if total_revenue > 0 else 0

    # Find top platform
    top_platform = max(
        _platform_balances.items(),
        key=lambda x: x[1]["total"]
    )[0]

    return RevenueMetrics(
        total_revenue=round(total_revenue, 2),
        available_balance=round(available_balance, 2),
        pending_clearance=round(pending_clearance, 2),
        total_sales=total_sales_count,
        revenue_change_24h=round(avg_change, 1),
        average_sale=round(total_revenue / total_sales_count, 2) if total_sales_count > 0 else 0,
        top_platform=top_platform,
        platforms_count=len(_platform_balances)
    )


@router.post("/withdraw", response_model=dict)
async def request_withdrawal(request: WithdrawalRequest):
    """
    Request a withdrawal from a platform
    """
    if request.platform not in _platform_balances:
        raise HTTPException(status_code=404, detail=f"Platform {request.platform} not found")

    data = _platform_balances[request.platform]

    if request.amount > data["balance"]:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient balance. Available: ${data['balance']:.2f}, Requested: ${request.amount:.2f}"
        )

    # Process withdrawal (mock)
    data["balance"] -= request.amount

    withdrawal_id = f"wd-{random.randint(100000, 999999)}"

    return {
        "status": "success",
        "withdrawal_id": withdrawal_id,
        "platform": request.platform,
        "amount": request.amount,
        "payment_method": request.payment_method,
        "estimated_arrival": (datetime.now() + timedelta(days=3)).isoformat(),
        "remaining_balance": data["balance"]
    }


@router.post("/sales/add", response_model=Sale)
async def add_sale(
    platform: Platform,
    product: str,
    amount: float,
    customer: str,
    status: SaleStatus = SaleStatus.COMPLETED
):
    """
    Add a new sale (for testing/demo purposes)
    """
    fee = round(amount * 0.029 + 0.30, 2)

    sale = Sale(
        id=f"sale-{len(_sales_history) + 1000}",
        platform=platform,
        product=product,
        amount=amount,
        customer=customer,
        status=status,
        timestamp=datetime.now(),
        transaction_id=f"txn-{random.randint(100000, 999999)}",
        fee=fee,
        net_amount=amount - fee
    )

    _sales_history.append(sale)

    # Update platform balance
    if platform in _platform_balances:
        if status == SaleStatus.COMPLETED:
            _platform_balances[platform]["balance"] += sale.net_amount
        else:
            _platform_balances[platform]["pending"] += sale.net_amount

        _platform_balances[platform]["total"] += sale.net_amount
        _platform_balances[platform]["count"] += 1

    return sale


@router.get("/export", response_model=dict)
async def export_revenue_data(
    format: str = Query("csv", regex="^(csv|json)$"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Export revenue data in CSV or JSON format
    """
    # Filter by date range if provided
    filtered_sales = _sales_history

    if start_date:
        filtered_sales = [s for s in filtered_sales if s.timestamp >= start_date]

    if end_date:
        filtered_sales = [s for s in filtered_sales if s.timestamp <= end_date]

    if format == "csv":
        # Generate CSV
        csv_data = "ID,Platform,Product,Amount,Customer,Status,Timestamp,Transaction ID,Fee,Net Amount\n"
        for sale in filtered_sales:
            csv_data += f"{sale.id},{sale.platform.value},{sale.product},{sale.amount},{sale.customer},{sale.status.value},{sale.timestamp.isoformat()},{sale.transaction_id},{sale.fee},{sale.net_amount}\n"

        return {
            "format": "csv",
            "records": len(filtered_sales),
            "data": csv_data
        }
    else:
        # Return JSON
        return {
            "format": "json",
            "records": len(filtered_sales),
            "data": [sale.dict() for sale in filtered_sales]
        }
