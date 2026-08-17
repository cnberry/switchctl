from __future__ import annotations

from pathlib import Path

from switchctl.backends.manual import ManualBackend
from switchctl.backends.tuya_local import TuyaLocalBackend
from switchctl.config import DEFAULT_MANUAL_STATE_PATH, load_targets
from switchctl.errors import ConfigError, SelectionError
from switchctl.models import SwitchStatus, SwitchTarget
from switchctl.selectors import require_safe_mutation, select_targets


class SwitchService:
    def __init__(self, config_path: Path | None = None):
        self.raw_config, self.targets = load_targets(config_path)
        manual_state_path = Path(
            self.raw_config.get("manual_state_path", DEFAULT_MANUAL_STATE_PATH)
        ).expanduser()
        self.backends = {
            "manual": ManualBackend(manual_state_path),
            "tuya-local": TuyaLocalBackend(),
        }

    def _backend_for(self, target: SwitchTarget):
        if target.backend not in self.backends:
            raise ConfigError(f"unsupported backend: {target.backend}")
        return self.backends[target.backend]

    def list_targets(
        self,
        selector: str | None = None,
        room: str | None = None,
        role: str | None = None,
        tags: list[str] | None = None,
        all_targets: bool = False,
    ) -> list[SwitchTarget]:
        return select_targets(
            self.targets,
            selector=selector,
            room=room,
            role=role,
            tags=tags,
            all_targets=all_targets,
        )

    def status(
        self,
        selector: str | None = None,
        room: str | None = None,
        role: str | None = None,
        tags: list[str] | None = None,
        all_targets: bool = False,
    ) -> list[SwitchStatus]:
        selected = self.list_targets(
            selector=selector, room=room, role=role, tags=tags, all_targets=all_targets
        )
        return [self._backend_for(target).status(target) for target in selected]

    def set_enabled(
        self,
        enabled: bool,
        selector: str | None = None,
        room: str | None = None,
        role: str | None = None,
        tags: list[str] | None = None,
        all_targets: bool = False,
        yes: bool = False,
    ) -> list[SwitchStatus]:
        if not any([selector, room, role, tags, all_targets]):
            raise SelectionError("refusing switch mutation without an explicit selector or --all")
        selected = self.list_targets(
            selector=selector, room=room, role=role, tags=tags, all_targets=all_targets
        )
        require_safe_mutation(selected, confirmed=yes)
        return [self._backend_for(target).set_enabled(target, enabled) for target in selected]

    def doctor(
        self,
        selector: str | None = None,
        room: str | None = None,
        role: str | None = None,
        tags: list[str] | None = None,
        all_targets: bool = False,
    ) -> list[SwitchStatus]:
        return self.status(
            selector=selector, room=room, role=role, tags=tags, all_targets=all_targets
        )
