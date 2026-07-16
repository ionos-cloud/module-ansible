## Why

The `module-ansible` inventory plugin uses `pickle` for cache serialization with a default cache path of `/tmp`, creating a trivially exploitable remote-code-execution vector; additionally, file handles are opened without context managers throughout the codebase, leaking resources. These are concrete, exploitable issues present in the current `master` branch that must be addressed before the next Ansible Galaxy release.

## What Changes

- Replace `pickle` serialization in `plugins/inventory/inventory.py` with `json` to eliminate insecure deserialization
- Change default `cache_path` in `inventory.ini` from `/tmp` to `~/.cache/ansible-ionos` to remove the world-writable attack surface
- Set restrictive file permissions (`0600`) on the written cache file so other local users cannot tamper with it
- Add a permission check on `inventory.ini` when it contains credential fields (`token`, `username`, or `password`) and warn if the file is group/world-readable
- Replace all bare `open(...)` calls used for reading certificate/key files with `with` statement context managers (`plugins/modules/certificate.py`, `plugins/modules/application_load_balancer_forwardingrule.py`, `plugins/inventory/inventory.py`)
- Remove the `six` Python 2/3 compatibility dependency from `inventory.py`; use `configparser` from the Python 3 stdlib directly

## Capabilities

### New Capabilities

- `inventory-cache-security`: Cache file serialization format (pickle → JSON), default cache location, and cache file permissions at write time
- `credential-file-security`: Permission check on `inventory.ini` when credential fields are populated; warn on group/world-readable file
- `resource-management`: All file handles opened for certificates, private keys, and cache files MUST be managed via context managers

### Modified Capabilities

## Impact

- `plugins/inventory/inventory.py` — core change; cache format changes from binary pickle to JSON (existing `.pkl` caches will not be readable; they will be discarded and regenerated on first run)
- `plugins/inventory/inventory.ini` — default `cache_path` value changes
- `plugins/modules/certificate.py` — context manager refactor
- `plugins/modules/application_load_balancer_forwardingrule.py` — context manager refactor
- `requirements.txt` — `six` is not currently listed; after removing its import from `inventory.py`, a repo-wide grep SHALL confirm no other file imports `six`; if a subsequent commit has added it, it SHALL be removed
- Tests under `tests/` that assert on cache file format or path defaults will need updating
