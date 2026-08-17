from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class SwitchTarget:
    id: str
    name: str
    role: str
    backend: str
    room: str | None = None
    tags: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    backend_id: str | None = None
    host: str | None = None
    port: int | None = None
    device_id: str | None = None
    local_key: str | None = None
    local_key_env: str | None = None
    switch_dp: str | int | None = None
    protocol_version: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SwitchTarget":
        local_key_env = data.get("local_key_env")
        local_key = data.get("local_key")
        if not local_key and local_key_env:
            local_key = os.environ.get(local_key_env)
        return cls(
            id=data["id"],
            name=data.get("name", data["id"]),
            role=data.get("role", "switch"),
            backend=data.get("backend", "manual"),
            room=data.get("room"),
            tags=list(data.get("tags", [])),
            notes=list(data.get("notes", [])),
            backend_id=data.get("backend_id"),
            host=data.get("host"),
            port=data.get("port"),
            device_id=data.get("device_id"),
            local_key=local_key,
            local_key_env=local_key_env,
            switch_dp=data.get("switch_dp"),
            protocol_version=data.get("protocol_version"),
        )

    def to_safe_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "backend": self.backend,
            "room": self.room,
            "tags": list(self.tags),
            "notes": list(self.notes),
            "configured": {
                "host": bool(self.host),
                "device_id": bool(self.device_id),
                "local_key": bool(self.local_key),
                "switch_dp": bool(self.switch_dp),
                "protocol_version": bool(self.protocol_version),
            },
        }


@dataclass(frozen=True)
class SwitchStatus:
    id: str
    name: str
    role: str
    backend: str
    enabled: bool
    room: str | None = None
    reachable: bool | None = None
    missing: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    raw: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        raw = data.pop("raw")
        data["raw_available"] = raw is not None
        return data
