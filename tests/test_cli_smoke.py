import json

from switchctl import cli


def test_import_cli_module():
    import switchctl.cli  # noqa: F401


def test_config_init_writes_default_config(tmp_path, capsys):
    config_path = tmp_path / "config.json"

    rc = cli.main(["--config", str(config_path), "config", "init"])

    assert rc == 0
    assert config_path.exists()
    assert capsys.readouterr().out.strip() == str(config_path)


def test_config_show_prints_default_config(tmp_path, capsys):
    config_path = tmp_path / "config.json"

    rc = cli.main(["--config", str(config_path), "config", "show"])

    assert rc == 0
    stdout = capsys.readouterr().out
    assert '"targets"' in stdout
    assert '"example-media-power"' in stdout
    assert '"<redacted>"' in stdout


def test_doctor_json_uses_status_shape(monkeypatch, capsys):
    class FakeRow:
        def to_dict(self):
            return {"id": "example-media-power", "state": "ok"}

    class FakeService:
        def __init__(self, config_path):
            self.config_path = config_path

        def doctor(self, **kwargs):
            assert kwargs == {
                "selector": None,
                "room": None,
                "role": "tv",
                "tags": None,
                "all_targets": True,
            }
            return [FakeRow()]

    monkeypatch.setattr(cli, "SwitchService", FakeService)

    rc = cli.main(["doctor", "--role", "tv", "--all", "--json"])

    assert rc == 0
    assert json.loads(capsys.readouterr().out) == [{"id": "example-media-power", "state": "ok"}]
