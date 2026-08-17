# Protocol and model notes

`switchctl` models each controlled item as a named endpoint with a semantic role
and a backend. Internal state is one boolean `enabled` value; role-specific
verbs are presentation aliases.

## Manual backend

The manual backend stores boolean state in a mode-`0600` JSON file. It is useful
for policy-backed or externally enacted endpoints but does not itself operate
network hardware.

## Tuya local backend

The Tuya backend uses `tinytuya` in-process for LAN status and setpoint calls.
Required private fields are host, device ID, local key, and switch datapoint;
protocol version defaults to 3.3. Local keys are read from the private
mode-`0600` configuration and are never included in command output.

The backend checks TCP reachability before protocol calls. A set operation reads
status again and returns the state from that response. Device families and
datapoints vary, so compatibility must be validated per device.

## Output boundary

Default target JSON includes booleans showing which private fields are
configured, not their values. Status JSON omits raw backend responses. Config
display redacts paths, hosts, backend IDs, device IDs, and inline local keys.
