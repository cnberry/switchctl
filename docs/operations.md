# Operations and safety

## Read before write

Use `switchctl list`, `status`, or `doctor` before a write when the selector,
target set, current state, or backend readiness is unclear. Every write requires
`--yes`; the flag confirms intent, not physical safety.

## Selection

Targets can be selected by exact ID or normalized name, or filtered by room,
role, and repeatable tags. A selector can intentionally match a shared tag and
therefore several endpoints. Inspect the resulting inventory before using a
broad write. Mutations require at least one selector/filter or an explicit
`--all`; an unqualified write is refused even when `--yes` is present.

## Write sequence

`on`, `off`, `enable`, and `disable` share the same internal boolean state:

1. load private configuration;
2. resolve the requested target set;
3. require `--yes`;
4. verify backend configuration and reachability;
5. perform the backend write; and
6. report state returned after the write.

The manual backend updates a private local state file. The Tuya backend sends a
local LAN command and immediately requests device status again.

## Live validation

Automated tests never contact hardware. Before a release that changes a backend,
validate supervised status, off/on/off or disable/enable/disable behavior, and
the final readback on a disposable or otherwise safe endpoint.
