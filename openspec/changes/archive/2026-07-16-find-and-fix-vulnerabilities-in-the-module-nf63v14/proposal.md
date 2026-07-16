## Why

The module-ansible collection contains critical and high-severity security vulnerabilities in the inventory plugin (insecure pickle deserialization, unsafe subprocess execution, world-writable cache in `/tmp`) and in several modules (path traversal on user-supplied file paths, full stack traces in error responses). These expose users in shared or automated environments to remote code execution and arbitrary file read/write. Fixing them now prevents exploitation before the collection's next major release cycle.

## What Changes

- Replace `pickle` cache serialization with JSON in `plugins/inventory/inventory.py`; set cache file permissions to 0600; move default cache path from `/tmp` to `~/.ansible/tmp/`
- Add `isfile` and `os.X_OK` checks before subprocess execution of password scripts; pass path as a list to `Popen`; fix Python 3 bytes/str decode
- Add `os.path.realpath` + `os.path.isfile` validation for all file-path module parameters in `certificate.py` (`certificate_file`, `certificate_chain_file`, `private_key_file`), `k8s_config.py` (`config_file`), and `application_load_balancer_forwardingrule.py` (the `certificate_file`, `private_key_file`, `certificate_chain_file` dict keys within the `new_server_certificates` parameter)
- Remove `exception=traceback.format_exc()` from all `module.fail_json` calls in `volume.py`, `cube_server.py`, `server.py`, `vcpu_server.py`
- Add lower-bound version constraints to all unpinned entries in `requirements.txt`
- Add alphanumeric key validation before `getattr` in `plugins/module_utils/common_ionos_methods.py`

## Capabilities

### New Capabilities
- `inventory-plugin-security`: Safe cache serialization (JSON), restrictive file permissions (0600), user-home cache path, validated subprocess invocation for password scripts
- `module-path-traversal`: Path canonicalization and traversal prevention for file-path parameters in certificate, k8s_config, and ALB forwarding rule modules
- `error-information-disclosure`: Sanitized error messages — `fail_json` calls omit stack traces
- `dependency-integrity`: Lower-bound version pins on all requirements entries
- `filter-attribute-safety`: Validated attribute key access in the common inventory filter utility

### Modified Capabilities
- (none — no existing specs in `openspec/specs/`)

## Impact

- `plugins/inventory/inventory.py` — cache serialization format, file permissions, subprocess validation, bytes decode fix
- `plugins/modules/certificate.py` — `certificate_file`, `certificate_chain_file`, `private_key_file` path validation
- `plugins/modules/k8s_config.py` — `config_file` write path validation
- `plugins/modules/application_load_balancer_forwardingrule.py` — certificate file path validation
- `plugins/modules/volume.py`, `cube_server.py`, `server.py`, `vcpu_server.py` — `fail_json` error sanitization
- `plugins/module_utils/common_ionos_methods.py` — filter key validation
- `requirements.txt` — version pin lower bounds
