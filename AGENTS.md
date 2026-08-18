# Repository guidance

## Purpose

`switchctl` is a terminal-first library and CLI for named switch-backed
endpoints. Keep configuration, selection, backends, service orchestration,
rendering, and CLI dispatch separate.

## Engineering principles

- Read state before adding or performing a write.
- Keep commands small, explicit, and scriptable.
- Require `--yes` for every mutating command.
- Report post-write device state instead of request acceptance alone.
- Keep real names, rooms, tags, hosts, device IDs, local keys, and cloud
  credentials outside the public repository.
- Never print local keys or raw backend payloads in default human or JSON output.
- Prefer local control and exact selection over broad automation magic.
- Test configuration, redaction, selection, rendering, backends, and guards
  without live hardware.
- Maintain `script/install` as the language-neutral installer contract. A future
  Rust migration changes that script, not the private bootstrap caller.
- Update `README.md`, `SKILL.md`, and relevant docs when behavior changes.

## Layout

- `switchctl/config.py` — private configuration and redaction
- `switchctl/models.py` — target and status data models
- `switchctl/selectors.py` — exact selector/filter behavior and write guard
- `switchctl/service.py` — backend selection and operation orchestration
- `switchctl/backends/` — manual and local Tuya implementations
- `switchctl/formatters.py` — compact human output
- `switchctl/cli.py` — command parser and dispatch
- `script/install` — stable installer entry point for deployment automation
- `tests/` — hardware-free unit tests

## Public/private boundary

Public files may contain documentation-only values such as `192.0.2.10` and
generic example names. Site inventory belongs in the private `home-config` repo.
Secrets may live in the private `home-config` configuration deployed mode `0600`,
but never in this public repository, logs, issues, or command output.
