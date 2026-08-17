import stat

from switchctl.backends.manual import ManualBackend
from switchctl.backends.tuya_local import TuyaLocalBackend
from switchctl.models import SwitchTarget


def make_target(**overrides):
    data = {
        "id": "example-outlet",
        "name": "Example Outlet",
        "room": "example-zone",
        "role": "light",
        "backend": "manual",
        "backend_id": None,
        "host": None,
        "port": None,
        "device_id": None,
        "local_key": None,
        "local_key_env": None,
        "switch_dp": None,
        "protocol_version": None,
        "notes": [],
    }
    data.update(overrides)
    return SwitchTarget(**data)


def test_manual_backend_uses_backend_id_for_state_key(tmp_path):
    backend = ManualBackend(tmp_path / "manual-state.json")
    target = make_target(backend_id="tuya-device-123")

    backend.set_enabled(target, False)

    state = backend._read()
    assert state == {"tuya-device-123": False}
    assert backend.status(target).enabled is False
    assert stat.S_IMODE((tmp_path / "manual-state.json").stat().st_mode) == 0o600


def test_tuya_local_backend_reports_missing_fields_without_network_call(tmp_path):
    backend = TuyaLocalBackend()
    target = make_target(backend="tuya-local")

    status = backend.status(target)

    assert status.backend == "tuya-local"
    assert status.enabled is False
    assert status.reachable is None
    assert status.missing == ["host", "device_id", "local_key", "switch_dp"]
    assert status.notes[0] == "Missing config: host, device_id, local_key, switch_dp"


def test_tuya_write_reports_post_write_status(monkeypatch):
    calls = []

    class FakeOutlet:
        def __init__(self, device_id, host, local_key):
            calls.append((device_id, host, local_key))

        def set_version(self, version):
            calls.append(("version", version))

        def set_status(self, enabled, switch_dp):
            calls.append(("set", enabled, switch_dp))
            return {"ok": True}

        def status(self):
            calls.append(("status",))
            return {"dps": {"1": True}}

    monkeypatch.setattr("switchctl.backends.tuya_local.tinytuya.OutletDevice", FakeOutlet)
    monkeypatch.setattr(
        "switchctl.backends.tuya_local.reachability",
        lambda host, port: {"ok": True, "host": host, "port": port},
    )
    target = make_target(
        backend="tuya-local",
        host="192.0.2.10",
        port=6668,
        device_id="example-device",
        local_key="example-local-key",
        switch_dp="1",
        protocol_version="3.4",
    )

    status = TuyaLocalBackend().set_enabled(target, True)

    assert status.enabled is True
    assert ("set", True, 1) in calls
    assert calls[-1] == ("status",)
