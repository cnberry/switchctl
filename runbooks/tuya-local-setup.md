# Tuya local onboarding

Use this runbook to onboard a disposable or otherwise safe Tuya-family switch
for local control. Vendor portals and `tinytuya` can change, so verify their
current instructions before creating cloud resources.

## Private values required

- device LAN address and port;
- device ID;
- local key;
- protocol version; and
- switch datapoint, commonly but not universally `1`.

Names, addresses, identifiers, and room metadata belong in the private
`home-ops` inventory. Local and cloud keys do not belong in Git at all.

## 1. Pair a test device

Pair the endpoint with a supported Tuya-family app on the intended 2.4 GHz
network. Use a temporary, generic vendor-side label while discovering it.

## 2. Create and link a Tuya developer project

At [Tuya's IoT platform](https://iot.tuya.com), create a project in the region
matching the app account, link that account, and enable the minimum APIs needed
to enumerate the test device and retrieve its local-control metadata.

If the portal requires an API IP allowlist, add only the current public address
for the extraction machine and remove it when it is no longer needed.

## 3. Store extraction credentials locally

Save TinyTuya cloud extraction credentials only in:

```text
~/.config/switchctl/tinytuya.json
```

Use the format expected by the installed `tinytuya` release and set mode `0600`.
Do not put this file in `home-ops` or any other Git repository.

## 4. Discover and extract

From a switchctl development environment:

```bash
just setup
just scan
```

Use TinyTuya's documented wizard when cloud-assisted key extraction is needed.
Keep generated `devices.json`, `snapshot.json`, and `tuya-raw.json` local; they
are ignored by this repository but can still contain sensitive metadata.

If an allowlisted IPv4 project is reached over IPv6 and the provider rejects the
request, constrain the extraction client to IPv4 using current TinyTuya guidance
rather than copying an environment-specific script into public documentation.

## 5. Record private inventory

Add the endpoint to private `home-ops` switch configuration with its meaningful
local name, role, room, host, device ID, local key, protocol version, and
datapoint:

```json
{
  "local_key": "replace-with-local-key"
}
```

Keep that repository private and deploy the config with mode `0600`.

## 6. Validate local control

Install the complete private config and run:

```bash
switchctl status example-outlet
switchctl off example-outlet --yes
switchctl on example-outlet --yes
switchctl off example-outlet --yes
```

Use the real private target ID locally; public examples remain generic. Record
only sanitized outcomes in issues, commits, or release notes.
