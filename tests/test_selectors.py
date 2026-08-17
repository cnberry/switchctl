from switchctl.models import SwitchTarget
from switchctl.selectors import select_targets


def sample_targets():
    return [
        SwitchTarget(
            id="media-power",
            name="Media Power",
            room="media-room",
            role="tv",
            backend="manual",
        ),
        SwitchTarget(
            id="alpha-light",
            name="Alpha Light",
            room="zone-a",
            role="light",
            backend="tuya-local",
            tags=["outdoor", "group-a"],
        ),
        SwitchTarget(
            id="beta-light",
            name="Beta Light",
            room="zone-a",
            role="light",
            backend="tuya-local",
            tags=["group-a"],
        ),
    ]


def test_select_by_id():
    rows = select_targets(sample_targets(), selector="media-power")
    assert [row.id for row in rows] == ["media-power"]


def test_select_by_role():
    rows = select_targets(sample_targets(), role="light")
    assert [row.id for row in rows] == ["alpha-light", "beta-light"]


def test_select_by_name_alias():
    rows = select_targets(sample_targets(), selector="Alpha Light")
    assert [row.id for row in rows] == ["alpha-light"]


def test_select_by_shared_tag_alias():
    rows = select_targets(sample_targets(), selector="group-a")
    assert [row.id for row in rows] == ["alpha-light", "beta-light"]
