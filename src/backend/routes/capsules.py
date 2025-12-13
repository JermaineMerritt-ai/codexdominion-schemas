"""
Capsule API - BIIE Constellation Management
Manages 30 industry intelligence capsules with avatars and metrics
"""
from datetime import datetime
from typing import List, Optional
from enum import Enum

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/capsules", tags=["BIIE Capsules"])


class CapsuleTier(int, Enum):
    """Capsule tier classification"""
    FOUNDATION = 1
    PROFESSIONAL = 2
    SPECIALIZED = 3


class CapsuleStatus(str, Enum):
    """Capsule operational status"""
    ACTIVE = "active"
    LAUNCHING = "launching"
    PLANNING = "planning"
    IDLE = "idle"
    MAINTENANCE = "maintenance"


class CapsuleInfo(BaseModel):
    """Complete capsule information"""
    id: int
    name: str
    avatar: str
    industry: str
    tier: CapsuleTier
    status: CapsuleStatus
    customers: int
    problems_solved: int
    revenue: float
    success_rate: float
    uptime: float
    satisfaction: float
    created_at: datetime
    last_updated: datetime


class CapsuleMetrics(BaseModel):
    """Aggregated capsule metrics"""
    total_capsules: int
    active_capsules: int
    total_customers: int
    total_problems_solved: int
    total_revenue: float
    avg_success_rate: float
    avg_uptime: float
    avg_satisfaction: float


class CustomerSystem(BaseModel):
    """Customer system managed by capsule"""
    id: str
    customer_name: str
    capsule_id: int
    system_type: str
    health_score: int
    issues_found: int
    last_maintenance: datetime
    auto_repair: bool


# Mock capsule data (matches frontend)
CAPSULES_DATA = [
    # TIER 1: FOUNDATION
    {"id": 1, "name": "BuildMaster AI", "avatar": "🏗️", "industry": "Construction", "tier": 1, "status": "active", "customers": 234, "problems": 4520, "revenue": 521000, "success": 96.9, "uptime": 99.8, "satisfaction": 4.6},
    {"id": 2, "name": "FactoryMind AI", "avatar": "🏭", "industry": "Manufacturing", "tier": 1, "status": "active", "customers": 189, "problems": 5890, "revenue": 612000, "success": 97.8, "uptime": 99.9, "satisfaction": 4.8},
    {"id": 3, "name": "RouteGenius AI", "avatar": "🚚", "industry": "Logistics", "tier": 1, "status": "active", "customers": 276, "problems": 6234, "revenue": 548000, "success": 97.1, "uptime": 99.7, "satisfaction": 4.7},
    {"id": 4, "name": "ShopSense AI", "avatar": "🛒", "industry": "Retail", "tier": 1, "status": "active", "customers": 198, "problems": 3421, "revenue": 425000, "success": 95.8, "uptime": 99.6, "satisfaction": 4.5},
    {"id": 5, "name": "MedFlow AI", "avatar": "🏥", "industry": "Healthcare", "tier": 1, "status": "active", "customers": 342, "problems": 7854, "revenue": 685000, "success": 98.2, "uptime": 99.9, "satisfaction": 4.9},
    {"id": 6, "name": "FarmWise AI", "avatar": "🌾", "industry": "Agriculture", "tier": 1, "status": "active", "customers": 167, "problems": 2987, "revenue": 398000, "success": 94.5, "uptime": 99.5, "satisfaction": 4.4},
    {"id": 7, "name": "PowerGrid AI", "avatar": "⚡", "industry": "Energy", "tier": 1, "status": "active", "customers": 156, "problems": 4231, "revenue": 489000, "success": 96.5, "uptime": 99.8, "satisfaction": 4.7},
    {"id": 8, "name": "PropertyPro AI", "avatar": "🏘️", "industry": "Real Estate", "tier": 1, "status": "active", "customers": 223, "problems": 3876, "revenue": 467000, "success": 95.2, "uptime": 99.4, "satisfaction": 4.5},
    {"id": 9, "name": "HotelHub AI", "avatar": "🏨", "industry": "Hospitality", "tier": 1, "status": "launching", "customers": 145, "problems": 2654, "revenue": 356000, "success": 93.8, "uptime": 99.3, "satisfaction": 4.3},
    {"id": 10, "name": "MenuMaster AI", "avatar": "🍽️", "industry": "Food Service", "tier": 1, "status": "active", "customers": 201, "problems": 3542, "revenue": 412000, "success": 94.9, "uptime": 99.5, "satisfaction": 4.4},

    # TIER 2: PROFESSIONAL
    {"id": 11, "name": "LawLogic AI", "avatar": "⚖️", "industry": "Legal", "tier": 2, "status": "active", "customers": 89, "problems": 1876, "revenue": 289000, "success": 97.3, "uptime": 99.7, "satisfaction": 4.8},
    {"id": 12, "name": "LedgerAI", "avatar": "📊", "industry": "Accounting", "tier": 2, "status": "active", "customers": 134, "problems": 2987, "revenue": 345000, "success": 96.8, "uptime": 99.6, "satisfaction": 4.7},
    {"id": 13, "name": "RiskGuard AI", "avatar": "🛡️", "industry": "Insurance", "tier": 2, "status": "active", "customers": 98, "problems": 2154, "revenue": 312000, "success": 96.2, "uptime": 99.5, "satisfaction": 4.6},
    {"id": 14, "name": "EduFlow AI", "avatar": "📚", "industry": "Education", "tier": 2, "status": "launching", "customers": 76, "problems": 1654, "revenue": 234000, "success": 94.5, "uptime": 99.4, "satisfaction": 4.5},
    {"id": 15, "name": "CampaignIQ AI", "avatar": "📢", "industry": "Marketing", "tier": 2, "status": "active", "customers": 112, "problems": 2345, "revenue": 278000, "success": 95.7, "uptime": 99.6, "satisfaction": 4.6},
    {"id": 16, "name": "TalentFlow AI", "avatar": "👥", "industry": "HR", "tier": 2, "status": "active", "customers": 87, "problems": 1987, "revenue": 245000, "success": 95.2, "uptime": 99.5, "satisfaction": 4.5},
    {"id": 17, "name": "StrategyPro AI", "avatar": "💼", "industry": "Consulting", "tier": 2, "status": "launching", "customers": 54, "problems": 987, "revenue": 198000, "success": 96.5, "uptime": 99.3, "satisfaction": 4.7},
    {"id": 18, "name": "DesignGenius AI", "avatar": "📐", "industry": "Architecture", "tier": 2, "status": "planning", "customers": 42, "problems": 876, "revenue": 167000, "success": 94.8, "uptime": 99.2, "satisfaction": 4.4},
    {"id": 19, "name": "CalcMaster AI", "avatar": "⚙️", "industry": "Engineering", "tier": 2, "status": "planning", "customers": 38, "problems": 765, "revenue": 154000, "success": 95.3, "uptime": 99.4, "satisfaction": 4.5},
    {"id": 20, "name": "ContentKing AI", "avatar": "🎬", "industry": "Media", "tier": 2, "status": "planning", "customers": 67, "problems": 1234, "revenue": 189000, "success": 93.7, "uptime": 99.1, "satisfaction": 4.3},

    # TIER 3: SPECIALIZED
    {"id": 21, "name": "AutoTech AI", "avatar": "🚗", "industry": "Automotive", "tier": 3, "status": "planning", "customers": 29, "problems": 543, "revenue": 123000, "success": 94.2, "uptime": 99.0, "satisfaction": 4.4},
    {"id": 22, "name": "SkyOps AI", "avatar": "✈️", "industry": "Aviation", "tier": 3, "status": "planning", "customers": 18, "problems": 456, "revenue": 289000, "success": 96.8, "uptime": 99.5, "satisfaction": 4.8},
    {"id": 23, "name": "SeaRoute AI", "avatar": "⚓", "industry": "Maritime", "tier": 3, "status": "planning", "customers": 15, "problems": 387, "revenue": 234000, "success": 95.5, "uptime": 99.3, "satisfaction": 4.6},
    {"id": 24, "name": "NetFlow AI", "avatar": "📡", "industry": "Telecom", "tier": 3, "status": "planning", "customers": 34, "problems": 876, "revenue": 298000, "success": 95.9, "uptime": 99.7, "satisfaction": 4.7},
    {"id": 25, "name": "PharmaFlow AI", "avatar": "💊", "industry": "Pharmaceutical", "tier": 3, "status": "planning", "customers": 22, "problems": 654, "revenue": 267000, "success": 97.1, "uptime": 99.6, "satisfaction": 4.8},
    {"id": 26, "name": "ChemSafe AI", "avatar": "🧪", "industry": "Chemical", "tier": 3, "status": "planning", "customers": 12, "problems": 432, "revenue": 198000, "success": 96.3, "uptime": 99.4, "satisfaction": 4.7},
    {"id": 27, "name": "EarthCore AI", "avatar": "⛏️", "industry": "Mining", "tier": 3, "status": "planning", "customers": 9, "problems": 321, "revenue": 245000, "success": 95.7, "uptime": 99.2, "satisfaction": 4.6},
    {"id": 28, "name": "RecycleFlow AI", "avatar": "♻️", "industry": "Waste Management", "tier": 3, "status": "planning", "customers": 31, "problems": 765, "revenue": 156000, "success": 94.4, "uptime": 99.3, "satisfaction": 4.5},
    {"id": 29, "name": "GuardNet AI", "avatar": "🔒", "industry": "Security", "tier": 3, "status": "planning", "customers": 27, "problems": 687, "revenue": 178000, "success": 95.1, "uptime": 99.5, "satisfaction": 4.6},
    {"id": 30, "name": "EcoWatch AI", "avatar": "🌍", "industry": "Environmental", "tier": 3, "status": "planning", "customers": 19, "problems": 543, "revenue": 189000, "success": 96.2, "uptime": 99.4, "satisfaction": 4.7},
]


@router.get("/", response_model=List[CapsuleInfo])
async def get_all_capsules(
    tier: Optional[CapsuleTier] = None,
    status: Optional[CapsuleStatus] = None
):
    """
    Get all capsules with optional filtering by tier and status
    """
    capsules = []

    for data in CAPSULES_DATA:
        # Apply filters
        if tier and data["tier"] != tier:
            continue
        if status and data["status"] != status:
            continue

        capsules.append(CapsuleInfo(
            id=data["id"],
            name=data["name"],
            avatar=data["avatar"],
            industry=data["industry"],
            tier=CapsuleTier(data["tier"]),
            status=CapsuleStatus(data["status"]),
            customers=data["customers"],
            problems_solved=data["problems"],
            revenue=data["revenue"],
            success_rate=data["success"],
            uptime=data["uptime"],
            satisfaction=data["satisfaction"],
            created_at=datetime.now(),
            last_updated=datetime.now()
        ))

    return capsules


@router.get("/{capsule_id}", response_model=CapsuleInfo)
async def get_capsule(capsule_id: int):
    """
    Get detailed information about a specific capsule
    """
    # Find capsule
    capsule_data = next((c for c in CAPSULES_DATA if c["id"] == capsule_id), None)

    if not capsule_data:
        raise HTTPException(status_code=404, detail=f"Capsule {capsule_id} not found")

    return CapsuleInfo(
        id=capsule_data["id"],
        name=capsule_data["name"],
        avatar=capsule_data["avatar"],
        industry=capsule_data["industry"],
        tier=CapsuleTier(capsule_data["tier"]),
        status=CapsuleStatus(capsule_data["status"]),
        customers=capsule_data["customers"],
        problems_solved=capsule_data["problems"],
        revenue=capsule_data["revenue"],
        success_rate=capsule_data["success"],
        uptime=capsule_data["uptime"],
        satisfaction=capsule_data["satisfaction"],
        created_at=datetime.now(),
        last_updated=datetime.now()
    )


@router.get("/metrics/summary", response_model=CapsuleMetrics)
async def get_capsule_metrics():
    """
    Get aggregated metrics across all capsules
    """
    active_count = sum(1 for c in CAPSULES_DATA if c["status"] == "active")
    total_customers = sum(c["customers"] for c in CAPSULES_DATA)
    total_problems = sum(c["problems"] for c in CAPSULES_DATA)
    total_revenue = sum(c["revenue"] for c in CAPSULES_DATA)
    avg_success = sum(c["success"] for c in CAPSULES_DATA) / len(CAPSULES_DATA)
    avg_uptime = sum(c["uptime"] for c in CAPSULES_DATA) / len(CAPSULES_DATA)
    avg_satisfaction = sum(c["satisfaction"] for c in CAPSULES_DATA) / len(CAPSULES_DATA)

    return CapsuleMetrics(
        total_capsules=len(CAPSULES_DATA),
        active_capsules=active_count,
        total_customers=total_customers,
        total_problems_solved=total_problems,
        total_revenue=total_revenue,
        avg_success_rate=round(avg_success, 1),
        avg_uptime=round(avg_uptime, 1),
        avg_satisfaction=round(avg_satisfaction, 1)
    )


@router.post("/{capsule_id}/activate", response_model=dict)
async def activate_capsule(capsule_id: int):
    """
    Activate a capsule (change status from planning/launching to active)
    """
    capsule_data = next((c for c in CAPSULES_DATA if c["id"] == capsule_id), None)

    if not capsule_data:
        raise HTTPException(status_code=404, detail=f"Capsule {capsule_id} not found")

    if capsule_data["status"] == "active":
        return {
            "status": "already_active",
            "message": f"{capsule_data['name']} is already active"
        }

    # Update status
    capsule_data["status"] = "active"

    return {
        "status": "activated",
        "capsule_id": capsule_id,
        "name": capsule_data["name"],
        "message": f"{capsule_data['name']} activated successfully"
    }


@router.post("/{capsule_id}/deactivate", response_model=dict)
async def deactivate_capsule(capsule_id: int):
    """
    Deactivate a capsule (change status to idle)
    """
    capsule_data = next((c for c in CAPSULES_DATA if c["id"] == capsule_id), None)

    if not capsule_data:
        raise HTTPException(status_code=404, detail=f"Capsule {capsule_id} not found")

    capsule_data["status"] = "idle"

    return {
        "status": "deactivated",
        "capsule_id": capsule_id,
        "name": capsule_data["name"],
        "message": f"{capsule_data['name']} deactivated"
    }


@router.get("/{capsule_id}/customers", response_model=List[CustomerSystem])
async def get_capsule_customers(capsule_id: int):
    """
    Get customer systems managed by a specific capsule
    """
    capsule_data = next((c for c in CAPSULES_DATA if c["id"] == capsule_id), None)

    if not capsule_data:
        raise HTTPException(status_code=404, detail=f"Capsule {capsule_id} not found")

    # Mock customer systems
    customers = []
    for i in range(min(5, capsule_data["customers"])):
        customers.append(CustomerSystem(
            id=f"cust-{capsule_id}-{i+1}",
            customer_name=f"Customer {i+1}",
            capsule_id=capsule_id,
            system_type=capsule_data["industry"],
            health_score=95 + (i % 5),
            issues_found=i % 3,
            last_maintenance=datetime.now(),
            auto_repair=True
        ))

    return customers
