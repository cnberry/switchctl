from switchctl.backends.tuya_local import TuyaLocalBackend
from switchctl.models import SwitchTarget


def test_missing_fields_show_in_status_notes(tmp_path):
    backend = TuyaLocalBackend()
    target = SwitchTarget(
        id="example-outlet",
        name="Example Outlet",
        room="example-zone",
        role="light",
        backend="tuya-local",
        host="192.0.2.10",
    )

    status = backend.status(target)

    assert status.missing
    assert any("Missing config" in note for note in status.notes)
