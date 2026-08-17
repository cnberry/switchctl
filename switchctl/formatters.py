from __future__ import annotations

from switchctl.models import SwitchStatus, SwitchTarget


def render_list(rows: list[SwitchTarget]) -> str:
    if not rows:
        return ""
    id_w = max(len(row.id) for row in rows)
    role_w = max(len(row.role) for row in rows)
    room_w = max(len(row.room or "-") for row in rows)
    return "\n".join(
        f"{row.id.ljust(id_w)}  {row.role.ljust(role_w)}  {(row.room or '-').ljust(room_w)}  {row.name}  backend={row.backend}"
        for row in rows
    )


def render_status(rows: list[SwitchStatus]) -> str:
    if not rows:
        return ""
    id_w = max(len(row.id) for row in rows)
    role_w = max(len(row.role) for row in rows)
    state_w = max(len("enabled" if row.enabled else "disabled") for row in rows)
    lines = []
    for row in rows:
        state = "enabled" if row.enabled else "disabled"
        extra = []
        if row.reachable is not None:
            extra.append(f"reachable={'yes' if row.reachable else 'no'}")
        if row.missing:
            extra.append(f"missing={','.join(row.missing)}")
        extra.append(f"backend={row.backend}")
        lines.append(
            f"{row.id.ljust(id_w)}  {row.role.ljust(role_w)}  {state.ljust(state_w)}  {' '.join(extra)}"
        )
    return "\n".join(lines)
