"""
ARC Sovereign API Router
FastAPI router exposing ARC arena telemetry and control endpoints.
"""

from fastapi import APIRouter
from arc_sovereign_arena.coordinator import SovereignArcCoordinator

arc_router = APIRouter(prefix="/api/arc", tags=["ARC-Sovereign-Arena"])

@arc_router.get("/status")
def get_arc_status():
    """Returns real-time discovery telemetry across AGI 1, 2, and 3."""
    coordinator = SovereignArcCoordinator()
    return coordinator.get_telemetry()

@arc_router.get("/laws")
def get_arc_laws():
    """Returns the full catalog of synthesized ARC laws."""
    coordinator = SovereignArcCoordinator()
    return {
        "count": len(coordinator.discoveries),
        "laws": coordinator.discoveries
    }

@arc_router.post("/start")
def start_arc_loop():
    """Starts the background discovery loop."""
    coordinator = SovereignArcCoordinator()
    coordinator.start_background_loop()
    return {"status": "started", "message": "ARC Sovereign Discovery Arena running"}
