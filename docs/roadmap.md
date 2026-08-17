# Roadmap

## Proven surface

- private target inventory with environment-backed local keys
- exact and filtered selection by name, room, role, and tag
- manual and local Tuya status
- guarded on/off and enable/disable operations
- post-write Tuya readback
- redacted human and JSON output

## Next

- expand mocked Tuya tests for timeout, malformed-response, and failure paths;
- define stable JSON schema notes and structured error categories;
- validate more device families without broadening writes speculatively;
- publish signed standalone binaries during the planned Rust migration.

## Installer direction

Deployment automation calls `script/install`, never a language-specific package
manager. The current script creates a system venv; a Rust migration should replace it with
a verified binary or `cargo` installation while preserving that entry point.

## Out of scope by default

- cloud control during normal operation;
- public site inventory or any tracked local/cloud key;
- unattended safety-critical automation;
- arbitrary backend or datapoint writes without validation.
