# Security policy

`switchctl` handles local device keys and can operate powered equipment. Report
vulnerabilities privately through GitHub's security-advisory feature instead of
opening a public issue with site topology, device identifiers, local keys, cloud
credentials, raw responses, or exploit details.

Prefer named environment variables supplied by a password manager for Tuya
local keys. Keep TinyTuya cloud extraction credentials in a local mode-`0600`
file and never commit them, even to a private configuration repository.

This project uses unofficial local integrations and cannot provide safety,
availability, or security guarantees for connected equipment.
