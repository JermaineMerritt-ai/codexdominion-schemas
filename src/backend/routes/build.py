"""
Build Queue API - Action AI Council Integration
Manages 300 AI agents, build queue, and project coordination
"""
from datetime import datetime
from typing import List, Optional
from enum import Enum

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field
import asyncio
import json

router = APIRouter(prefix="/api/build", tags=["Build Queue"])

# Import the auto build engine
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from auto_build_engine import AutoBuildEngine, BuildType, Priority

# Global build engine instance
build_engine = None
active_websockets: List[WebSocket] = []


class BuildStatus(str, Enum):
    """Build status enum"""
    QUEUED = "queued"
    BUILDING = "building"
    TESTING = "testing"
    DEPLOYING = "deploying"
    COMPLETE = "complete"
    ERROR = "error"


class BuildProjectRequest(BaseModel):
    """Request to add a new build project"""
    name: str = Field(..., description="Project name")
    build_type: str = Field(..., description="Type of build (website, app, store, etc)")
    priority: str = Field(default="medium", description="Priority level")
    description: str = Field(..., description="Project description")
    assigned_ai: Optional[str] = Field(None, description="Specific AI agent to assign")


class BuildProjectResponse(BaseModel):
    """Build project response"""
    id: str
    name: str
    build_type: str
    priority: str
    description: str
    assigned_ai: str
    status: str
    progress: int
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]


class BuildQueueStatus(BaseModel):
    """Overall build queue status"""
    is_live: bool
    total_agents: int
    agents_available: int
    agents_working: int
    queue_length: int
    active_builds: int
    completed_today: int
    total_capacity: int
    utilization_percent: float


class AgentStatus(BaseModel):
    """Individual AI agent status"""
    id: str
    name: str
    capabilities: List[str]
    max_concurrent: int
    current_load: int
    utilization_percent: float
    status: str


def get_build_engine():
    """Get or create build engine instance"""
    global build_engine
    if build_engine is None:
        build_engine = AutoBuildEngine()
    return build_engine


@router.post("/launch", response_model=dict)
async def launch_auto_build():
    """
    Launch the auto-build engine and start building all queued projects
    """
    engine = get_build_engine()

    if engine.is_live:
        return {
            "status": "already_running",
            "message": "Auto-build engine is already running",
            "active_builds": len(engine.active_builds),
            "queue_length": len(engine.build_queue)
        }

    # Start the build engine in background
    asyncio.create_task(engine.go_live())

    # Broadcast to all connected websockets
    await broadcast_status_update()

    return {
        "status": "launched",
        "message": "Auto-build engine launched successfully",
        "launch_projects": len(engine.launch_projects),
        "total_agents": 6,
        "total_capacity": 300
    }


@router.post("/stop", response_model=dict)
async def stop_auto_build():
    """
    Stop the auto-build engine
    """
    engine = get_build_engine()
    engine.is_live = False

    await broadcast_status_update()

    return {
        "status": "stopped",
        "message": "Auto-build engine stopped",
        "active_builds": len(engine.active_builds),
        "completed": len(engine.completed_builds)
    }


@router.get("/status", response_model=BuildQueueStatus)
async def get_build_status():
    """
    Get current build queue status and agent utilization
    """
    engine = get_build_engine()
    status = engine.get_status()

    # Calculate utilization
    total_capacity = sum(agent["max_concurrent"] for agent in engine.ai_agents.values())
    total_load = sum(agent["current_load"] for agent in engine.ai_agents.values())
    utilization = (total_load / total_capacity * 100) if total_capacity > 0 else 0

    # Count available agents
    agents_available = sum(
        1 for agent in engine.ai_agents.values()
        if agent["current_load"] < agent["max_concurrent"]
    )
    agents_working = len(engine.ai_agents) - agents_available

    return BuildQueueStatus(
        is_live=engine.is_live,
        total_agents=len(engine.ai_agents),
        agents_available=agents_available,
        agents_working=agents_working,
        queue_length=status["queue"],
        active_builds=status["active"],
        completed_today=status["completed"],
        total_capacity=total_capacity,
        utilization_percent=round(utilization, 1)
    )


@router.get("/agents", response_model=List[AgentStatus])
async def get_agent_status():
    """
    Get status of all AI agents
    """
    engine = get_build_engine()

    agents = []
    for agent_id, agent_data in engine.ai_agents.items():
        utilization = (agent_data["current_load"] / agent_data["max_concurrent"] * 100) if agent_data["max_concurrent"] > 0 else 0

        # Determine status
        if agent_data["current_load"] == 0:
            status = "idle"
        elif agent_data["current_load"] < agent_data["max_concurrent"]:
            status = "building"
        else:
            status = "at_capacity"

        agents.append(AgentStatus(
            id=agent_id,
            name=agent_data["name"],
            capabilities=agent_data["capabilities"],
            max_concurrent=agent_data["max_concurrent"],
            current_load=agent_data["current_load"],
            utilization_percent=round(utilization, 1),
            status=status
        ))

    return agents


@router.get("/queue", response_model=List[BuildProjectResponse])
async def get_build_queue():
    """
    Get all projects in the build queue
    """
    engine = get_build_engine()

    projects = []
    for project in engine.build_queue:
        projects.append(BuildProjectResponse(
            id=project.id,
            name=project.name,
            build_type=project.build_type.value,
            priority=project.priority.value,
            description=project.description,
            assigned_ai=project.assigned_ai,
            status=project.status,
            progress=project.progress,
            created_at=project.created_at,
            started_at=project.started_at,
            completed_at=project.completed_at
        ))

    return projects


@router.get("/active", response_model=List[BuildProjectResponse])
async def get_active_builds():
    """
    Get all currently building projects
    """
    engine = get_build_engine()

    projects = []
    for project in engine.active_builds:
        projects.append(BuildProjectResponse(
            id=project.id,
            name=project.name,
            build_type=project.build_type.value,
            priority=project.priority.value,
            description=project.description,
            assigned_ai=project.assigned_ai,
            status=project.status,
            progress=project.progress,
            created_at=project.created_at,
            started_at=project.started_at,
            completed_at=project.completed_at
        ))

    return projects


@router.get("/completed", response_model=List[BuildProjectResponse])
async def get_completed_builds():
    """
    Get all completed projects
    """
    engine = get_build_engine()

    projects = []
    for project in engine.completed_builds:
        projects.append(BuildProjectResponse(
            id=project.id,
            name=project.name,
            build_type=project.build_type.value,
            priority=project.priority.value,
            description=project.description,
            assigned_ai=project.assigned_ai,
            status=project.status,
            progress=project.progress,
            created_at=project.created_at,
            started_at=project.started_at,
            completed_at=project.completed_at
        ))

    return projects


@router.post("/add", response_model=BuildProjectResponse)
async def add_build_project(request: BuildProjectRequest):
    """
    Add a new project to the build queue
    """
    engine = get_build_engine()

    # Convert string enums to actual enums
    try:
        build_type = BuildType(request.build_type.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid build_type: {request.build_type}")

    try:
        priority = Priority(request.priority.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid priority: {request.priority}")

    # Add project to engine
    project = engine.add_project(
        name=request.name,
        build_type=build_type,
        priority=priority,
        description=request.description,
        assigned_ai=request.assigned_ai or "jermaine"
    )

    # Broadcast update
    await broadcast_status_update()

    return BuildProjectResponse(
        id=project.id,
        name=project.name,
        build_type=project.build_type.value,
        priority=project.priority.value,
        description=project.description,
        assigned_ai=project.assigned_ai,
        status=project.status,
        progress=project.progress,
        created_at=project.created_at,
        started_at=project.started_at,
        completed_at=project.completed_at
    )


@router.post("/customer-repair", response_model=BuildProjectResponse)
async def add_customer_repair(
    customer_name: str,
    system_type: str,
    issues: str,
    priority: str = "high"
):
    """
    Add a customer system repair project
    """
    engine = get_build_engine()

    try:
        priority_enum = Priority(priority.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid priority: {priority}")

    project = engine.add_customer_repair(
        customer_name=customer_name,
        system_type=system_type,
        issues=issues,
        priority=priority_enum
    )

    await broadcast_status_update()

    return BuildProjectResponse(
        id=project.id,
        name=project.name,
        build_type=project.build_type.value,
        priority=project.priority.value,
        description=project.description,
        assigned_ai=project.assigned_ai,
        status=project.status,
        progress=project.progress,
        created_at=project.created_at,
        started_at=project.started_at,
        completed_at=project.completed_at
    )


@router.websocket("/stream")
async def websocket_build_stream(websocket: WebSocket):
    """
    WebSocket endpoint for real-time build progress updates
    """
    await websocket.accept()
    active_websockets.append(websocket)

    try:
        # Send initial status
        engine = get_build_engine()
        status = engine.get_status()
        await websocket.send_json({
            "type": "status",
            "data": status
        })

        # Keep connection alive and listen for messages
        while True:
            try:
                data = await websocket.receive_text()
                # Echo back for ping/pong
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                })
            except WebSocketDisconnect:
                break

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if websocket in active_websockets:
            active_websockets.remove(websocket)


async def broadcast_status_update():
    """
    Broadcast status update to all connected websockets
    """
    if not active_websockets:
        return

    engine = get_build_engine()
    status = engine.get_status()

    message = {
        "type": "status_update",
        "data": status,
        "timestamp": datetime.now().isoformat()
    }

    # Send to all connected clients
    disconnected = []
    for websocket in active_websockets:
        try:
            await websocket.send_json(message)
        except:
            disconnected.append(websocket)

    # Remove disconnected websockets
    for ws in disconnected:
        active_websockets.remove(ws)
