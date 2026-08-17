from __future__ import annotations

from typing import Any

import tinytuya

from switchctl.errors import BackendError, NotConfiguredError
from switchctl.models import SwitchStatus, SwitchTarget
from switchctl.network import reachability


class TuyaLocalBackend:
    name = "tuya-local"

    def _missing_fields(self, target: SwitchTarget) -> list[str]:
        missing = []
        if not target.host:
            missing.append("host")
        if not target.device_id:
            missing.append("device_id")
        if not target.local_key:
            missing.append("local_key")
        if not target.switch_dp:
            missing.append("switch_dp")
        return missing

    def _tuya_rpc(
        self, target: SwitchTarget, action: str, power: bool | None = None
    ) -> dict[str, Any]:
        try:
            outlet = tinytuya.OutletDevice(target.device_id, target.host, target.local_key)
            outlet.set_version(float(target.protocol_version or "3.3"))
            if action == "status":
                return outlet.status()
            if action == "set":
                response = outlet.set_status(bool(power), int(str(target.switch_dp)))
                return {"response": response, "status": outlet.status()}
            raise BackendError(f"unsupported Tuya action: {action}")
        except BackendError:
            raise
        except Exception as exc:
            raise BackendError("Tuya local request failed") from exc

    def _extract_state(self, raw: dict[str, Any], switch_dp: str | int | None) -> bool:
        if switch_dp is None:
            raise NotConfiguredError("switch_dp is required")
        dps = raw.get("dps", {})
        return bool(dps.get(str(switch_dp)))

    def status(self, target: SwitchTarget) -> SwitchStatus:
        missing = self._missing_fields(target)
        notes = list(target.notes)
        if missing:
            notes = [f"Missing config: {', '.join(missing)}"] + notes
            return SwitchStatus(
                id=target.id,
                name=target.name,
                room=target.room,
                role=target.role,
                enabled=False,
                backend=self.name,
                reachable=None,
                missing=missing,
                notes=notes,
            )

        network = reachability(target.host or "", int(target.port or 6668))
        reachable = bool(network.get("ok"))
        if not reachable:
            notes = ["Network reachability failed"] + notes
            return SwitchStatus(
                id=target.id,
                name=target.name,
                room=target.room,
                role=target.role,
                enabled=False,
                backend=self.name,
                reachable=False,
                missing=[],
                notes=notes,
                raw={"network_error": True},
            )

        raw = self._tuya_rpc(target, "status")
        enabled = self._extract_state(raw, target.switch_dp)
        return SwitchStatus(
            id=target.id,
            name=target.name,
            room=target.room,
            role=target.role,
            enabled=enabled,
            backend=self.name,
            reachable=True,
            missing=[],
            notes=notes,
            raw=raw,
        )

    def set_enabled(self, target: SwitchTarget, enabled: bool) -> SwitchStatus:
        missing = self._missing_fields(target)
        if missing:
            raise NotConfiguredError(
                f"target '{target.id}' missing required fields: {', '.join(missing)}"
            )
        network = reachability(target.host or "", int(target.port or 6668))
        if not network.get("ok"):
            raise BackendError(f"target '{target.id}' is not reachable")
        rpc = self._tuya_rpc(target, "set", power=enabled)
        raw_status = rpc["status"]
        return SwitchStatus(
            id=target.id,
            name=target.name,
            room=target.room,
            role=target.role,
            enabled=self._extract_state(raw_status, target.switch_dp),
            backend=self.name,
            reachable=True,
            missing=[],
            notes=list(target.notes),
            raw=raw_status,
        )
