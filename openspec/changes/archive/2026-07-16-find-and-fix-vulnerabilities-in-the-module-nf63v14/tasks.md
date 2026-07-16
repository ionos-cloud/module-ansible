## 1. Inventory Plugin — Cache Security

- [ ] 1.1 Replace `pickle.load` with `json.load` in `plugins/inventory/inventory.py`; update cache read to expect `{"version": 1, "data": ..., "inventory": ...}` schema; handle `json.JSONDecodeError` with a warning and cache miss
- [ ] 1.2 Replace `pickle.dump` with `json.dump` in `plugins/inventory/inventory.py`; write the version-tagged schema; call `os.chmod(cache_file, 0o600)` immediately after write
- [ ] 1.3 Change default `cache_filename` from `/tmp/ansible-ionos.pkl` to `os.path.expanduser("~/.ansible/tmp/ionos-inventory-cache.json")`; ensure parent directory `~/.ansible/tmp/` is created with `os.makedirs(..., exist_ok=True)` and mode 0700
- [ ] 1.4 Add a warning log when the resolved cache directory is world-writable (`stat.S_IWOTH`)
- [ ] 1.5 In `load_from_cache`, stat the cache file after opening and check `stat.S_IMODE(os.stat(cache_filename).st_mode) != 0o600`; if the mode differs, emit a warning via `display.warning` before proceeding with the read

## 2. Inventory Plugin — Subprocess Safety

- [ ] 2.1 Before `Popen` call in password script execution: resolve path with `os.path.realpath`; assert `os.path.isfile`; assert `os.access(path, os.X_OK)`; raise `AnsibleError` with a clear message if either check fails
- [ ] 2.2 Change `Popen(this_path, ...)` to `Popen([canonical_path], ...)` to prevent shell injection
- [ ] 2.3 Decode `stdout` bytes: replace `stdout.strip('\r\n')` with `stdout.decode('utf-8').strip()`; handle `UnicodeDecodeError` with `AnsibleError`

## 3. Module Path Traversal — Certificate and ALB

- [ ] 3.1 In `plugins/modules/certificate.py`: for `certificate_file`, `certificate_chain_file`, and `private_key_file`, call `os.path.realpath` and `os.path.isfile` before `open()`; call `module.fail_json` with a generic "invalid file path" message if either check fails
- [ ] 3.2 In `plugins/modules/application_load_balancer_forwardingrule.py`: apply the same `realpath` + `isfile` validation to the `certificate_file`, `private_key_file`, and `certificate_chain_file` dict keys within each element of the `new_server_certificates` parameter (see `create_certificate` function)
- [ ] 3.3 Audit `plugins/modules/` for any other `open(param, ...)` calls on user-supplied paths; apply the same pattern where found

## 4. Module Path Traversal — k8s_config Write Path

- [ ] 4.1 In `plugins/modules/k8s_config.py`: resolve `config_file` with `os.path.realpath`; check `os.path.isdir(os.path.dirname(canonical))` before `open(..., 'w')`; call `module.fail_json` if the parent directory does not exist
- [ ] 4.2 Add `module.warn(...)` if the resolved parent directory has world-writable permissions

## 5. Error Message Sanitization

- [ ] 5.1 In `plugins/modules/volume.py`: remove `exception=traceback.format_exc()` from all `module.fail_json` calls; remove unused `import traceback` if it becomes orphaned
- [ ] 5.2 In `plugins/modules/cube_server.py`: same removal as 5.1
- [ ] 5.3 In `plugins/modules/server.py`: same removal as 5.1
- [ ] 5.4 In `plugins/modules/vcpu_server.py`: same removal as 5.1
- [ ] 5.5 Grep remaining modules for `traceback.format_exc()` and remove any other occurrences

## 6. Filter Attribute Safety

- [ ] 6.1 In `plugins/module_utils/common_ionos_methods.py`, import `re` and add a helper that validates each key segment with `re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', segment)`
- [ ] 6.2 In the filter traversal loop, call the validator on each `key_part` before `getattr`; raise `AnsibleError` on invalid segments
- [ ] 6.3 Handle the case where an intermediate `getattr` result is `None` by returning `False` (non-matching) instead of raising `AttributeError`
- [ ] 6.4 In the traversal loop, after each `getattr` call check `isinstance(current, (str, int, float, bool, bytes, list, dict))`; if the result is a leaf type, compare it directly to the filter value, short-circuit the remaining key segments, and do not call `getattr` on the leaf value

## 7. Dependency Version Pinning

- [ ] 7.1 Research minimum CVE-free versions for `cryptography`, `PyYAML`, `chevron`, and `ansible` (check PyPI advisories / OSV)
- [ ] 7.2 Update `requirements.txt` to add `>=<version>` lower bounds for all unpinned packages
- [ ] 7.3 Update `requirements.txt` entries that have only upper bounds (e.g., `ionoscloud<7`) to also include a `>=` lower bound
- [ ] 7.4 Verify the updated requirements install cleanly in a fresh virtualenv: `pip install -r requirements.txt`

## 8. Testing and Verification

- [ ] 8.1 Run the existing test suite: `pytest tests/` — confirm no regressions
- [ ] 8.2 Write a unit test for the JSON cache read/write path; assert the old pickle path is never called
- [ ] 8.3 Write a unit test for the password script validation logic covering: valid script, directory path, non-executable file, non-UTF-8 output
- [ ] 8.4 Write unit tests for `certificate.py`, `application_load_balancer_forwardingrule.py`, and `k8s_config.py` path validation; for each module cover: valid path, traversal path (`../../etc/passwd`), missing file/directory, and symlink-resolved canonical path; for ALB also cover each of `certificate_file`, `private_key_file`, `certificate_chain_file` within a `new_server_certificates` element; for `k8s_config.py` cover write-path traversal where the resolved parent directory escapes the intended directory
- [ ] 8.5 Write unit tests for `common_ionos_methods.py` filter validation covering: valid key, dunder key, metacharacter key, None intermediate

## 9. Documentation and Release

- [ ] 9.1 Add CHANGELOG entry documenting: cache format change (pickle→JSON), default cache path change, removal of `exception` field from fail_json, new `requirements.txt` lower bounds
- [ ] 9.2 Bump collection version in `galaxy.yml` per semver (patch bump)
