"""
Synthetic data generator standing in for real TMS / SMMS / TDMS / COA feeds.

Indian Railways does not expose these systems publicly, so for the prototype
we generate realistic-looking maintenance requests and a small corridor
network graph that the rest of the pipeline (priority engine, scheduler,
digital twin, auction) can operate on exactly as it would on live data.
"""
import random
from dataclasses import dataclass, field, asdict
from typing import List

random.seed(42)

DEPARTMENTS = ["Engineering", "S&T", "TRD"]
CORRIDORS = ["A-B", "B-C", "C-D", "D-E", "E-F"]

TASK_TEMPLATES = {
    "Engineering": ["Rail crack repair", "Track geometry correction", "Ballast renewal", "Points & crossing overhaul"],
    "S&T": ["Signal relay maintenance", "Interlocking check", "Point machine defect", "Communication cable fault"],
    "TRD": ["OHE wire inspection", "Traction transformer check", "Insulator replacement", "Feeder cable maintenance"],
}


@dataclass
class MaintenanceTask:
    id: str
    department: str
    corridor: str
    task: str
    criticality: int      # 1-10
    historical_defects: int
    asset_age_years: int
    traffic_load: int     # trains/day on this corridor
    duration_hours: float
    due_in_days: int


@dataclass
class CorridorEdge:
    u: str
    v: str
    corridor: str
    daily_trains: int


def generate_network() -> List[CorridorEdge]:
    """A small linear-ish rail network with one loop line, so blocking the
    direct corridor forces traffic onto an alternate path — this is what the
    digital twin module checks."""
    stations = ["A", "B", "C", "D", "E", "F"]
    edges = [
        CorridorEdge("A", "B", "A-B", daily_trains=42),
        CorridorEdge("B", "C", "B-C", daily_trains=38),
        CorridorEdge("C", "D", "C-D", daily_trains=35),
        CorridorEdge("D", "E", "D-E", daily_trains=30),
        CorridorEdge("E", "F", "E-F", daily_trains=25),
        # loop / alternate route around B-C-D so blocks there have a real diversion
        CorridorEdge("B", "G", "B-G", daily_trains=18),
        CorridorEdge("G", "D", "G-D", daily_trains=18),
    ]
    return edges


def generate_tasks(n: int = 12) -> List[MaintenanceTask]:
    tasks = []
    for i in range(n):
        dept = random.choice(DEPARTMENTS)
        corridor = random.choice(CORRIDORS)
        task_name = random.choice(TASK_TEMPLATES[dept])
        tasks.append(MaintenanceTask(
            id=f"T{i+1:03d}",
            department=dept,
            corridor=corridor,
            task=task_name,
            criticality=random.randint(3, 10),
            historical_defects=random.randint(0, 15),
            asset_age_years=random.randint(1, 30),
            traffic_load=random.randint(15, 45),
            duration_hours=round(random.choice([0.75, 1.0, 1.5, 2.0, 2.5, 3.0]), 2),
            due_in_days=random.randint(1, 30),
        ))
    return tasks


def tasks_as_dicts(tasks: List[MaintenanceTask]):
    return [asdict(t) for t in tasks]
