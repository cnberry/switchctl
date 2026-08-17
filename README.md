<p align="center">
  <img src="docs/assets/switchctl-hero.jpg" alt="Illustration of a terminal controlling generic local switches" width="100%">
</p>

# switchctl

`switchctl` is a small Python CLI for inspecting and operating named switch-
backed endpoints. It provides one model for lights, media power, outlets, and
similar devices while keeping backend-specific network details in private local
configuration.

> [!WARNING]
> `switchctl` controls powered equipment over local integrations. Verify the
> selected endpoint and physical area, preserve working physical controls, and
> do not use this project for unattended safety-critical automation.

## What it does

- lists configured endpoints by name, role, room, or tag;
- reports state, reachability, and missing configuration;
- supports manual state and local Tuya-family switch backends;
- exposes compact human output and redacted JSON;
- provides role-neutral `on`/`off` and `enable`/`disable` verbs;
- requires `--yes` for every mutating command;
- reads device state again before reporting a local Tuya write result.

Python 3.11 or newer is required by the current implementation.

## Install

```bash
git clone https://github.com/cnberry/switchctl.git
cd switchctl
./script/install
```

`script/install` is the stable repository contract used by private deployment
automation. Today it installs the Python package with `pipx`; it can be replaced
by a Rust or binary installer later without changing callers. `just install`
uses the same contract.

## Configure private switches

Install the sanitized example outside the repository, then replace it with your
own endpoint inventory:

```bash
mkdir -p ~/.config/switchctl
install -m 600 config/switches.example.json ~/.config/switchctl/config.json
```

Set `SWITCHCTL_CONFIG=/path/to/config.json` or pass global `--config PATH` to
select another private file. Host addresses, device IDs, backend IDs, rooms,
names, notes, and tags are private deployment data and belong in a private
configuration repository.

Tuya local keys should not be committed even to a private repository. Use a
named environment reference in config:

```json
{
  "local_key_env": "SWITCHCTL_EXAMPLE_OUTLET_LOCAL_KEY"
}
```

Then supply that variable from a password manager before running the command.
The legacy inline `local_key` field remains supported for a tightly permissioned
local config file.

## Inspect state

```bash
switchctl list
switchctl list --role light
switchctl status example-outlet
switchctl doctor --all
switchctl config show
```

Add `--json` for structured output. Target JSON reports whether sensitive fields
are configured but does not print their values. Status JSON omits raw backend
responses, and `config show` redacts private deployment fields.

## Control switches

```bash
switchctl on example-outlet --yes
switchctl off example-outlet --yes
switchctl enable example-media-power --yes
switchctl disable example-media-power --yes
```

All write commands require an explicit selector or `--all` and refuse to run
without `--yes`, including single-target writes. Selectors that match several
targets fan out only after that explicit guard. See
[operations](docs/operations.md) for the full safety model.

## Runtime data

| Data | Default path | Git policy |
| --- | --- | --- |
| Switch inventory | `~/.config/switchctl/config.json` | Private config repo; no keys |
| Manual state | `~/.local/state/switchctl/manual-state.json` | Never commit |
| Tuya cloud extraction config | `~/.config/switchctl/tinytuya.json` | Never commit |
| Tuya local keys | Named environment variables or local config | Never commit |

Generated configuration and manual state files use mode `0600`.

## Reliability and scope

Local Tuya behavior depends on network reachability, the exact device ID and
key, protocol version, and datapoint mapping. `switchctl` intentionally avoids
cloud control during normal operation and does not claim compatibility with an
unvalidated device family.

See [protocol notes](docs/protocol.md), [troubleshooting](docs/troubleshooting.md),
the [Tuya onboarding runbook](runbooks/tuya-local-setup.md), and the
[roadmap](docs/roadmap.md).

## Control-tool family

- [`gatectl`](https://github.com/cnberry/gatectl) — MyQ gate and garage-door
  status with guarded open/close.
- [`poolctl`](https://github.com/cnberry/poolctl) — Pentair ScreenLogic status,
  cleaner, and delay control.
- [`hottubctl`](https://github.com/cnberry/hottubctl) — Sundance SmartTub
  temperature and freshness inspection.
- [`switchctl`](https://github.com/cnberry/switchctl) — named local switch
  status and guarded power control.

Current and future `*ctl` tools share small commands, private configuration,
readable output, safe JSON, guarded writes, post-write readback, a repo-owned
`script/install`, and explicit uncertainty.

## Development

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/ruff format --check switchctl tests
.venv/bin/ruff check switchctl tests
.venv/bin/detect-secrets scan --baseline .secrets.baseline
.venv/bin/pytest -q
```

Automated tests do not contact or operate real switches.

## License

`switchctl` is released under the [MIT License](LICENSE).
