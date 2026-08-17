set shell := ["bash", "-cu"]

venv := ".venv"
python := venv + "/bin/python"
pip := venv + "/bin/pip"
pytest := venv + "/bin/pytest"

default:
    just --list

setup:
    python3 -m venv {{venv}}
    {{pip}} install -e ".[dev]"

install:
    ./script/install

reinstall:
    ./script/install

test:
    {{venv}}/bin/ruff format --check switchctl tests
    {{venv}}/bin/ruff check switchctl tests
    {{venv}}/bin/detect-secrets scan --baseline .secrets.baseline
    PYTHONPATH=. {{python}} -m pytest -q

test-integration:
    if [ -x {{python}} ]; then PYTHONPATH=. {{python}} -m switchctl.cli --help >/dev/null; elif command -v switchctl >/dev/null; then switchctl --help >/dev/null; else echo 'no dev env or installed switchctl; run just setup or just install' >&2; exit 1; fi
    if [ -x {{python}} ]; then PYTHONPATH=. {{python}} -m switchctl.cli status --help >/dev/null; elif command -v switchctl >/dev/null; then switchctl status --help >/dev/null; else echo 'no dev env or installed switchctl; run just setup or just install' >&2; exit 1; fi
    if [ -x {{python}} ]; then PYTHONPATH=. {{python}} -m switchctl.cli doctor --help >/dev/null; elif command -v switchctl >/dev/null; then switchctl doctor --help >/dev/null; else echo 'no dev env or installed switchctl; run just setup or just install' >&2; exit 1; fi
    if [ -x {{python}} ]; then PYTHONPATH=. {{python}} -m switchctl.cli on --help >/dev/null; elif command -v switchctl >/dev/null; then switchctl on --help >/dev/null; else echo 'no dev env or installed switchctl; run just setup or just install' >&2; exit 1; fi
    if [ -x {{python}} ]; then PYTHONPATH=. {{python}} -m switchctl.cli disable --help >/dev/null; elif command -v switchctl >/dev/null; then switchctl disable --help >/dev/null; else echo 'no dev env or installed switchctl; run just setup or just install' >&2; exit 1; fi
    if [ -x {{python}} ]; then PYTHONPATH=. {{python}} -m switchctl.cli config show --help >/dev/null; elif command -v switchctl >/dev/null; then switchctl config show --help >/dev/null; else echo 'no dev env or installed switchctl; run just setup or just install' >&2; exit 1; fi

test-all:
    just test
    just test-integration

config-init:
    switchctl config init

config-show:
    switchctl config show

list:
    switchctl list

status:
    switchctl status

doctor:
    switchctl doctor

lights:
    switchctl list --role light

tvs:
    switchctl list --role tv

on target:
    switchctl on {{target}} --yes

off target:
    switchctl off {{target}} --yes

enable target:
    switchctl enable {{target}} --yes

disable target:
    switchctl disable {{target}} --yes

scan:
    if [ ! -x {{python}} ]; then echo 'missing dev env; run just setup before just scan' >&2; exit 1; fi
    {{python}} -m tinytuya scan
