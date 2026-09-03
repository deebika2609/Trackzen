"""
Safety & Conflict Solver.

Uses Google OR-Tools CP-SAT to place every task on a 24-hour timeline
(30-minute slots) subject to hard constraints that must NEVER be violated:

  1. A department cannot run two tasks at the same time (one crew).
  2. Every task fits within the horizon.
  3. High-urgency tasks are pushed earlier (soft objective, not a hard rule).
  4. Tasks that share a corridor are rewarded for overlapping in time —
     this is what actually produces a single combined block instead of
     three separate ones, while tasks in *different* corridors are free
     to be scheduled independently.

This does not decide *fairness* between departments (that's the auction
engine's job) — it only guarantees that whatever the auction proposes is
actually safe and schedulable.
"""
from ortools.sat.python import cp_model

SLOTS_PER_DAY = 48   # 30-minute resolution over 24h
SLOT_MINUTES = 30


def _to_slots(hours: float) -> int:
    return max(1, round(hours * 60 / SLOT_MINUTES))


def solve_schedule(tasks: list, priorities: dict):
    """
    tasks: list of dicts with id, department, corridor, duration_hours
    priorities: {task_id: urgency_score}
    returns: list of {task_id, start_slot, end_slot, start_time, end_time}
    """
    model = cp_model.CpModel()
    n = len(tasks)
    starts, ends, intervals = {}, {}, {}

    for t in tasks:
        dur = _to_slots(t["duration_hours"])
        s = model.NewIntVar(0, SLOTS_PER_DAY - dur, f's_{t["id"]}')
        e = model.NewIntVar(dur, SLOTS_PER_DAY, f'e_{t["id"]}')
        iv = model.NewIntervalVar(s, dur, e, f'iv_{t["id"]}')
        starts[t["id"]], ends[t["id"]], intervals[t["id"]] = s, e, iv

    # Hard constraint: one department = one crew = no double-booking
    for dept in set(t["department"] for t in tasks):
        dept_intervals = [intervals[t["id"]] for t in tasks if t["department"] == dept]
        if len(dept_intervals) > 1:
            model.AddNoOverlap(dept_intervals)

    # Soft objective: urgent tasks earlier + corridor tasks pulled together
    urgency_term = sum(
        int(priorities.get(t["id"], 50)) * starts[t["id"]] for t in tasks
    )

    spread_terms = []
    for corridor in set(t["corridor"] for t in tasks):
        corridor_tasks = [t for t in tasks if t["corridor"] == corridor]
        if len(corridor_tasks) > 1:
            c_starts = [starts[t["id"]] for t in corridor_tasks]
            c_ends = [ends[t["id"]] for t in corridor_tasks]
            min_s = model.NewIntVar(0, SLOTS_PER_DAY, f'min_s_{corridor}')
            max_e = model.NewIntVar(0, SLOTS_PER_DAY, f'max_e_{corridor}')
            model.AddMinEquality(min_s, c_starts)
            model.AddMaxEquality(max_e, c_ends)
            spread = model.NewIntVar(0, SLOTS_PER_DAY, f'spread_{corridor}')
            model.Add(spread == max_e - min_s)
            spread_terms.append(spread)

    spread_penalty = sum(spread_terms) * 40  # weight: prefer combined, compact blocks
    model.Minimize(urgency_term + spread_penalty)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 5.0
    status = solver.Solve(model)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return {"status": "INFEASIBLE", "assignments": []}

    def slot_to_time(slot):
        h, m = divmod(slot * SLOT_MINUTES, 60)
        return f"{h:02d}:{m:02d}"

    assignments = []
    for t in tasks:
        s_val = solver.Value(starts[t["id"]])
        e_val = solver.Value(ends[t["id"]])
        assignments.append({
            "task_id": t["id"],
            "department": t["department"],
            "corridor": t["corridor"],
            "start_slot": s_val,
            "end_slot": e_val,
            "start_time": slot_to_time(s_val),
            "end_time": slot_to_time(e_val),
        })
    assignments.sort(key=lambda a: a["start_slot"])
    return {
        "status": "OPTIMAL" if status == cp_model.OPTIMAL else "FEASIBLE",
        "assignments": assignments,
    }
