# Changelog

## 7.8.1 (Security)

### Breaking Changes
- **Cache format change**: The inventory plugin (`plugins/inventory/inventory.py`) no longer uses
  pickle for its cache. The cache is now stored as JSON. Old `.pkl` cache files will not be read;
  delete them before upgrading.
- **Default cache path change**: The default cache file path changed from the current working
  directory (`./ansible-ionos.pkl`) to `~/.ansible/tmp/ionos-inventory-cache.json`. The parent
  directory is created automatically with mode `0700`.

### Security Fixes
- **Inventory cache (CWE-502)**: Replaced `pickle` serialization with JSON to eliminate the risk
  of arbitrary code execution via a tampered cache file. The cache file is now written with mode
  `0600`; a warning is emitted at runtime if the cache directory or file has world-writable
  permissions.
- **Inventory subprocess (CWE-78)**: The password-script execution path now validates that the
  resolved path is a regular file and is executable before passing it as a list argument to
  `subprocess.Popen`, preventing shell injection. Script output is decoded as UTF-8 with an
  explicit error on invalid bytes.
- **Path traversal – certificate modules (CWE-22)**: `plugins/modules/certificate.py` and
  `plugins/modules/application_load_balancer_forwardingrule.py` now call `os.path.realpath` and
  `os.path.isfile` on every user-supplied file path before opening it.
- **Path traversal – k8s_config (CWE-22)**: `plugins/modules/k8s_config.py` now validates the
  resolved write path and emits a warning if the parent directory is world-writable.
- **Exception leakage removed**: `exception=traceback.format_exc()` removed from all
  `module.fail_json` calls in `volume.py`, `cube_server.py`, `server.py`, and `vcpu_server.py`
  to prevent internal tracebacks from being returned to the Ansible controller output.
- **Filter attribute safety (CWE-20)**: The `get_method_from_filter` function in
  `plugins/module_utils/common_ionos_methods.py` now validates each key segment against
  `^[a-zA-Z_][a-zA-Z0-9_]*$`, returns `False` on `None` intermediates instead of raising
  `AttributeError`, and short-circuits when a leaf type is encountered.

### Dependency Updates
- `requirements.txt`: Added minimum version lower bounds for `cryptography>=41.0.0`,
  `PyYAML>=6.0`, `chevron>=0.14.0`, `ansible>=8.0.0`, and `ionoscloud>=6.0.2`.
