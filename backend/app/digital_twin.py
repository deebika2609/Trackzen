"""
Digital Twin / Network Impact Simulator.

Models the corridor network as a graph and checks what happens to traffic
that would have used the blocked corridor: does it divert onto a loop line
or alternate route that is already near capacity? This is the check a
single-corridor scheduler skips entirely.
"""
import networkx as nx

EDGE_CAPACITY = 50  # assumed max trains/day an edge can safely absorb


def build_graph(edges: list) -> nx.Graph:
    G = nx.Graph()
    for e in edges:
        G.add_edge(e.u, e.v, corridor=e.corridor, daily_trains=e.daily_trains)
    return G


def simulate_block_impact(edges: list, blocked_corridor: str) -> dict:
    G = build_graph(edges)
    blocked_edge = next((e for e in edges if e.corridor == blocked_corridor), None)
    if blocked_edge is None:
        return {"error": f"corridor {blocked_corridor} not found"}

    u, v, diverted_trains = blocked_edge.u, blocked_edge.v, blocked_edge.daily_trains

    G_reduced = G.copy()
    G_reduced.remove_edge(u, v)

    if not nx.has_path(G_reduced, u, v):
        return {
            "blocked_corridor": blocked_corridor,
            "diverted_trains": diverted_trains,
            "alternate_route": None,
            "affected_edges": [],
            "verdict": "No alternate route exists — this corridor is a single point of failure. "
                       "Block only during a scheduled full traffic suspension.",
            "risk_level": "critical",
        }

    path = nx.shortest_path(G_reduced, u, v, weight=None)
    path_edges = list(zip(path[:-1], path[1:]))

    affected = []
    max_utilisation = 0.0
    for (a, b) in path_edges:
        data = G_reduced.get_edge_data(a, b)
        current = data["daily_trains"]
        new_load = current + diverted_trains
        utilisation = round(new_load / EDGE_CAPACITY * 100, 1)
        max_utilisation = max(max_utilisation, utilisation)
        affected.append({
            "corridor": data["corridor"],
            "current_daily_trains": current,
            "projected_daily_trains": new_load,
            "capacity_utilisation_pct": utilisation,
        })

    if max_utilisation >= 100:
        risk, verdict = "critical", (
            "Diverting traffic pushes an alternate section over capacity — "
            "recommend a different time window or splitting the block."
        )
    elif max_utilisation >= 80:
        risk, verdict = "elevated", (
            "Alternate route absorbs the diverted traffic but runs close to capacity — "
            "acceptable, monitor closely during the block."
        )
    else:
        risk, verdict = "low", (
            "Alternate route comfortably absorbs diverted traffic — safe to proceed."
        )

    return {
        "blocked_corridor": blocked_corridor,
        "diverted_trains": diverted_trains,
        "alternate_route": " -> ".join(path),
        "affected_edges": affected,
        "verdict": verdict,
        "risk_level": risk,
    }
