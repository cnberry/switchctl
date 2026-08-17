---
name: switchctl
description: Inspect and control named local switch-backed endpoints with the switchctl CLI. Use for endpoint inventory, status, reachability, diagnosis, and guarded on, off, enable, or disable operations.
---

# switchctl

Use the installed `switchctl` CLI instead of ad-hoc device or Tuya calls when a
command already exists.

## Safety rules

- Treat names, rooms, tags, hosts, device IDs, local keys, and raw payloads as
  private deployment data.
- Read state before a write when the exact endpoint or current state is unclear.
- Use `--yes` only after the selector, resulting target set, and action are clear.
- Report the post-write state returned by the backend.
- Never print or request a local key in chat; use the configured environment
  variable or local mode-`0600` config.
- Follow the Tuya onboarding runbook instead of improvising cloud extraction.

## Commands

```bash
switchctl list
switchctl status example-outlet
switchctl doctor --all
switchctl on example-outlet --yes
switchctl off example-outlet --yes
switchctl enable example-media-power --yes
switchctl disable example-media-power --yes
```

Add `--json` for redacted structured output. If a command fails, quote the short
error and do not claim the endpoint reached the requested state.
