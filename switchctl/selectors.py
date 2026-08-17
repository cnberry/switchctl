from __future__ import annotations

from collections.abc import Iterable

from switchctl.errors import SelectionError
from switchctl.models import SwitchTarget


def _normalize(value: str | None) -> str:
    return (value or "").strip().lower().replace("-", " ").replace("_", " ")


def _matches_selector(target: SwitchTarget, selector: str) -> bool:
    normalized = _normalize(selector)
    aliases = {
        _normalize(target.id),
        _normalize(target.name),
        *{_normalize(tag) for tag in target.tags},
    }
    return normalized in aliases


def select_targets(
    targets: Iterable[SwitchTarget],
    selector: str | None = None,
    room: str | None = None,
    role: str | None = None,
    tags: list[str] | None = None,
    all_targets: bool = False,
) -> list[SwitchTarget]:
    selected = list(targets)

    if selector:
        selected = [target for target in selected if _matches_selector(target, selector)]
    if room:
        selected = [target for target in selected if target.room == room]
    if role:
        selected = [target for target in selected if target.role == role]
    if tags:
        required = {_normalize(tag) for tag in tags}
        selected = [
            target
            for target in selected
            if required.issubset({_normalize(tag) for tag in target.tags})
        ]

    if not any([selector, room, role, tags, all_targets]):
        return selected
    if not selected:
        raise SelectionError("no targets matched the requested selector")
    return selected


def require_safe_mutation(selected: list[SwitchTarget], confirmed: bool) -> None:
    if selected and not confirmed:
        raise SelectionError("refusing switch mutation without --yes")
