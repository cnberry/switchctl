# Troubleshooting

## Config is not found

Create `/usr/local/config/switchctl/config.json` from the public example, install the
private home-config inventory, or set `SWITCHCTL_CONFIG`. Repository-local runtime
configuration is intentionally unsupported.

## A local key is missing

Add the target's `local_key` to the private source configuration, run the
`home-config` bootstrap, and confirm `/usr/local/config/switchctl/config.json` is
owned by the operating user with mode `0600`. Never paste the key into logs.

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
