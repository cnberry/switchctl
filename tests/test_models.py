from switchctl.models import SwitchStatus, SwitchTarget


def test_target_json_reports_private_configuration_without_values():
    target = SwitchTarget(
        id="example-outlet",
        name="Example Outlet",
        role="outlet",
        backend="tuya-local",
        host="192.0.2.10",
        device_id="private-device-id",
        local_key="private-local-key",
        switch_dp="1",
        protocol_version="3.4",
    )

    safe = target.to_safe_dict()

    assert safe["configured"] == {
        "host": True,
        "device_id": True,
        "local_key": True,
        "switch_dp": True,
        "protocol_version": True,
    }
    assert "private-device-id" not in str(safe)
    assert "private-local-key" not in str(safe)


def test_status_json_omits_raw_backend_response():
    status = SwitchStatus(
        id="example-outlet",
        name="Example Outlet",
        role="outlet",
        backend="tuya-local",
        enabled=True,
        raw={"dps": {"1": True}, "device_id": "private-device-id"},
    )

    safe = status.to_dict()

    assert safe["raw_available"] is True
    assert "raw" not in safe
    assert "private-device-id" not in str(safe)
