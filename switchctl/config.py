from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any

from switchctl.errors import ConfigError
from switchctl.models import SwitchTarget

ENV_CONFIG_PATH = "SWITCHCTL_CONFIG"
DEFAULT_CONFIG_PATH = Path.home() / ".config" / "switchctl" / "config.json"
DEFAULT_MANUAL_STATE_PATH = Path.home() / ".local" / "state" / "switchctl" / "manual-state.json"
ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_CONFIG_PATH = ROOT / "config" / "switches.example.json"


def default_config() -> dict[str, Any]:
    return {
        "manual_state_path": str(DEFAULT_MANUAL_STATE_PATH),
        "targets": [
            {
                "id": "example-media-power",
                "name": "Example Media Power",
                "room": "example-room",
                "role": "tv",
                "backend": "manual",
                "backend_id": "example-media-power",
                "notes": ["Replace this example with private site configuration."],
            },
        ],
    }


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.parent.chmod(0o700)


def resolve_config_path(explicit_path: Path | None = None) -> Path:
    if explicit_path is not None:
        return explicit_path
    override = os.environ.get(ENV_CONFIG_PATH)
    if override:
        return Path(override).expanduser()
    if DEFAULT_CONFIG_PATH.exists():
        return DEFAULT_CONFIG_PATH
    return DEFAULT_CONFIG_PATH


def write_default_config(path: Path = DEFAULT_CONFIG_PATH) -> Path:
    ensure_parent(path)
    if not path.exists():
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as config_file:
            json.dump(default_config(), config_file, indent=2)
            config_file.write("\n")
    path.chmod(0o600)
    return path


def redacted_config(data: dict[str, Any]) -> dict[str, Any]:
    safe = deepcopy(data)
    if safe.get("manual_state_path"):
        safe["manual_state_path"] = "<redacted>"
    for target in safe.get("targets", []):
        if not isinstance(target, dict):
            continue
        for field in ("backend_id", "host", "device_id", "local_key"):
            if target.get(field):
                target[field] = "<redacted>"
    return safe


def load_raw_config(path: Path | None = None) -> dict[str, Any]:
    resolved = resolve_config_path(path)
    if not resolved.exists():
        write_default_config(resolved)
    return json.loads(resolved.read_text(encoding="utf-8"))


def load_targets(path: Path | None = None) -> tuple[dict[str, Any], list[SwitchTarget]]:
    data = load_raw_config(path)
    if "targets" not in data or not isinstance(data["targets"], list):
        raise ConfigError("config must contain a 'targets' list")
    try:
        targets = [SwitchTarget.from_dict(item) for item in data["targets"]]
    except KeyError as exc:
        raise ConfigError(f"missing required target field: {exc}") from exc
    return data, targets
