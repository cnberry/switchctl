# Troubleshooting

## Config is not found

Create `~/.config/switchctl/config.json` from the public example, install the
private home-ops inventory, or set `SWITCHCTL_CONFIG`. Repository-local runtime
configuration is intentionally unsupported.

## A local key is missing

If the target uses `local_key_env`, load that exact environment variable from a
password manager in the process running `switchctl`. Inline keys remain
supported only for local mode-`0600` configuration.

## A device is unreachable

Confirm the device is powered, on the expected LAN or VLAN, and listening on the
configured port. DHCP changes are a common cause; prefer a reservation without
putting the resulting address in the public repo.

## State is wrong after a write

The Tuya backend reports the status read after its command. Check the configured
datapoint and protocol version, then validate against a known-safe device. Do not
retry a broad selector in a loop.

## A write is refused

Every mutation requires an explicit selector/filter or `--all`, plus `--yes`,
even when the selector currently matches one target. Inspect the target set
before retrying.
