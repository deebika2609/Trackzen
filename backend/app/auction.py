"""
Auction Negotiation Engine.

Groups tasks that share a corridor and proposes combining them into a
single block, with the highest-urgency task in the group acting as the
"anchor" that sets timing priority. This is what turns three separate
department disruptions into one coordinated block, and — critically —
produces a plain-language reason so the allocation is defensible to a
Divisional Engineer, not a black box.

This module decides WHO gets combined and WHY; the CP-SAT scheduler
(scheduler.py) decides the exact safe timing.
"""


def negotiate(tasks: list, priority_scores: dict) -> list:
    by_corridor = {}
    for t in tasks:
        by_corridor.setdefault(t["corridor"], []).append(t)

    groups = []
    for corridor, group_tasks in by_corridor.items():
        ranked = sorted(group_tasks, key=lambda t: -priority_scores.get(t["id"], 0))
        anchor = ranked[0]
        joiners = ranked[1:]

        blocks_saved = len(joiners)  # each joiner is one fewer separate disruption
        departments = sorted(set(t["department"] for t in ranked))

        if joiners:
            joiner_str = ", ".join(f'{j["department"]} ({j["task"]})' for j in joiners)
            plural_verb = 'joins' if len(joiners) == 1 else 'join'
            plural_s = 's' if blocks_saved > 1 else ''
            urgency_val = priority_scores.get(anchor["id"], 0)
            reason = (
                f'{anchor["department"]}\'s "{anchor["task"]}" (urgency '
                f'{urgency_val:.0f}) anchors this block. '
                f'{joiner_str} '
                f'{plural_verb} the same window since they '
                f'share corridor {corridor} — avoiding {blocks_saved} separate disruption'
                f'{plural_s}.'
            )
        else:
            reason = f"No other department needs corridor {corridor} in this cycle — scheduled standalone."

        groups.append({
            "corridor": corridor,
            "anchor_task": anchor["id"],
            "member_task_ids": [t["id"] for t in ranked],
            "departments_combined": departments,
            "blocks_saved": blocks_saved,
            "reason": reason,
        })

    groups.sort(key=lambda g: -g["blocks_saved"])
    return groups
