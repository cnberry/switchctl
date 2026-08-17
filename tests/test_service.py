import json

from switchctl.config import load_raw_config, write_default_config
from switchctl.service import SwitchService


def make_service(tmp_path):
    config_path = tmp_path / "config.json"
    write_default_config(config_path)
    config = load_raw_config(config_path)
    config["manual_state_path"] = str(tmp_path / "manual-state.json")
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return SwitchService(config_path)


def test_status_defaults_to_enabled(tmp_path):
    service = make_service(tmp_path)
    rows = service.status()
    assert len(rows) == 1
    assert all(row.enabled for row in rows)


def test_disable_one_target(tmp_path):
    service = make_service(tmp_path)
    rows = service.set_enabled(False, selector="example-media-power", yes=True)
    assert len(rows) == 1
    assert rows[0].id == "example-media-power"
    assert rows[0].enabled is False
    all_rows = service.status()
    by_id = {row.id: row.enabled for row in all_rows}
    assert by_id["example-media-power"] is False


def test_disable_one_requires_yes(tmp_path):
    service = make_service(tmp_path)
    try:
        service.set_enabled(False, selector="example-media-power")
    except Exception as exc:
        assert "--yes" in str(exc)
    else:
        raise AssertionError("expected safe mutation refusal")


def test_disable_requires_explicit_selection(tmp_path):
    service = make_service(tmp_path)
    try:
        service.set_enabled(False, yes=True)
    except Exception as exc:
        assert "explicit selector or --all" in str(exc)
    else:
        raise AssertionError("expected explicit selection refusal")


def test_disable_all_requires_yes(tmp_path):
    service = make_service(tmp_path)
    try:
        service.set_enabled(False, all_targets=True)
    except Exception as exc:
        assert "--yes" in str(exc)
    else:
        raise AssertionError("expected safe mutation refusal")


def test_disable_all(tmp_path):
    service = make_service(tmp_path)
    rows = service.set_enabled(False, all_targets=True, yes=True)
    assert len(rows) == 1
    assert all(row.enabled is False for row in rows)
