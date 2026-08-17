import stat

from switchctl.config import default_config, load_targets, redacted_config, write_default_config


def test_default_config_has_expected_targets(tmp_path):
    path = tmp_path / "config.json"
    write_default_config(path)
    raw, targets = load_targets(path)
    assert raw["manual_state_path"]
    assert [target.id for target in targets] == ["example-media-power"]
    assert stat.S_IMODE(path.stat().st_mode) == 0o600


def test_default_config_shape():
    config = default_config()
    assert "manual_state_path" in config
    assert len(config["targets"]) == 1


def test_local_key_can_come_from_named_environment(monkeypatch, tmp_path):
    monkeypatch.setenv("SWITCHCTL_EXAMPLE_OUTLET_LOCAL_KEY", "environment-only")
    path = tmp_path / "config.json"
    path.write_text(
        '{"targets": [{"id": "example-outlet", "name": "Example", '
        '"role": "outlet", "backend": "tuya-local", '
        '"local_key_env": "SWITCHCTL_EXAMPLE_OUTLET_LOCAL_KEY"}]}'
    )
    _, targets = load_targets(path)
    outlet = next(target for target in targets if target.id == "example-outlet")
    assert outlet.local_key == "environment-only"


def test_redacted_config_hides_private_fields():
    config = {
        "manual_state_path": "/private/state.json",
        "targets": [
            {
                "id": "example",
                "host": "192.0.2.10",
                "device_id": "device-id",
                "local_key": "local-key",
            }
        ],
    }
    safe = redacted_config(config)
    assert safe["manual_state_path"] == "<redacted>"
    assert safe["targets"][0]["host"] == "<redacted>"
    assert safe["targets"][0]["device_id"] == "<redacted>"
    assert safe["targets"][0]["local_key"] == "<redacted>"
