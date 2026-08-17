from __future__ import annotations

from typing import Protocol

from switchctl.models import SwitchStatus, SwitchTarget


class Backend(Protocol):
    name: str

    def status(self, target: SwitchTarget) -> SwitchStatus: ...

    def set_enabled(self, target: SwitchTarget, enabled: bool) -> SwitchStatus: ...
