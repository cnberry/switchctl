from __future__ import annotations

import json
import os
from pathlib import Path

from switchctl.models import SwitchStatus, SwitchTarget


class ManualBackend:
    name = "manual"

    def __init__(self, state_path: Path):
        self.state_path = state_path
        self.state_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.state_path.parent.chmod(0o700)
        if not self.state_path.exists():
            self._write({})

    def _read(self) -> dict[str, bool]:
        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def _write(self, data: dict[str, bool]) -> None:
        descriptor = os.open(self.state_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as state_file:
            json.dump(data, state_file, indent=2, sort_keys=True)
            state_file.write("\n")
        self.state_path.chmod(0o600)

    def _key(self, target: SwitchTarget) -> str:
        return target.backend_id or target.id

    def status(self, target: SwitchTarget) -> SwitchStatus:
        enabled = self._read().get(self._key(target), True)
        return SwitchStatus(
            id=target.id,
            name=target.name,
            room=target.room,
            role=target.role,
            enabled=enabled,
            backend=self.name,
            notes=list(target.notes),
        )

    def set_enabled(self, target: SwitchTarget, enabled: bool) -> SwitchStatus:
        data = self._read()
        data[self._key(target)] = enabled
        self._write(data)
        return self.status(target)
