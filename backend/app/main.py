import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from . import synthetic_data as sd
from .priority import PriorityEngine
from .scheduler import solve_schedule
from .digital_twin import simulate_block_impact
from .auction import negotiate

app = FastAPI(
    title="TrackZen API — Intelligent Block Planning (RailSync SIH 2026)",
    description="Smart railway block scheduling, priority scoring, multi-department auction & digital twin simulator.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

priority_engine = PriorityEngine()
NETWORK_EDGES = sd.generate_network()


class PlanRequest(BaseModel):
    num_tasks: int = 12
    month: Optional[int] = None


@app.get("/api")
def api_root():
    return {
        "name": "TrackZen API — RailSync Intelligent Block Planning",
        "competition": "Smart India Hackathon (SIH) 2026",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "endpoints": {
            "health": "/api/health",
            "network": "/api/network",
            "full_plan": "/api/plan/full (POST)",
            "weekly_plan": "/api/plan/weekly (GET)"
        }
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "trackzen-railsync-api",
        "time": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/api/network")
def get_network():
    return {"edges": [e.__dict__ for e in NETWORK_EDGES]}


@app.post("/api/plan/full")
def full_plan(req: PlanRequest):
    """Runs the entire pipeline end-to-end: generate -> prioritize ->
    negotiate -> schedule -> simulate impact -> return one block plan."""
    month = req.month or datetime.utcnow().month
    tasks = sd.tasks_as_dicts(sd.generate_tasks(req.num_tasks))

    scored = priority_engine.score_all(tasks, month)
    priority_map = {s["task_id"]: s["urgency_score"] for s in scored}

    groups = negotiate(tasks, priority_map)

    schedule = solve_schedule(tasks, priority_map)

    impacted_corridors = list({t["corridor"] for t in tasks})
    impact_reports = [simulate_block_impact(NETWORK_EDGES, c) for c in impacted_corridors]

    tasks_by_id = {t["id"]: t for t in tasks}
    enriched_schedule = []
    for a in schedule["assignments"]:
        t = tasks_by_id[a["task_id"]]
        enriched_schedule.append({
            **a,
            "task": t["task"],
            "urgency_score": priority_map[a["task_id"]],
        })

    return {
        "month": month,
        "tasks": tasks,
        "priority_scores": scored,
        "auction_groups": groups,
        "schedule": {"status": schedule["status"], "assignments": enriched_schedule},
        "network_impact": impact_reports,
    }


@app.get("/api/plan/weekly")
def weekly_plan():
    """Aggregates 7 independent daily runs into a weekly view — same
    pipeline, longer horizon, as described in the proposal."""
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    week = []
    for i, day in enumerate(days):
        tasks = sd.tasks_as_dicts(sd.generate_tasks(4))
        month = datetime.utcnow().month
        scored = priority_engine.score_all(tasks, month)
        priority_map = {s["task_id"]: s["urgency_score"] for s in scored}
        schedule = solve_schedule(tasks, priority_map)
        tasks_by_id = {t["id"]: t for t in tasks}
        blocks = []
        for a in schedule["assignments"]:
            t = tasks_by_id[a["task_id"]]
            blocks.append({**a, "task": t["task"]})
        week.append({"day": day, "blocks": blocks})
    return {"week": week}


# Mount Frontend Distribution for Unified Deployment
FRONTEND_DIST = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")
)

if os.path.exists(FRONTEND_DIST):
    assets_dir = os.path.join(FRONTEND_DIST, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/")
    async def serve_dashboard():
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))

    @app.get("/{full_path:path}")
    async def serve_spa_catchall(full_path: str):
        if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("openapi.json") or full_path.startswith("redoc"):
            return None
        file_path = os.path.join(FRONTEND_DIST, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))

