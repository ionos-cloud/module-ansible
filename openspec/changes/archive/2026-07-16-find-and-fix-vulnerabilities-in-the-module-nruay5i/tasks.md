## 1. Inventory Cache — Replace pickle with JSON

- [ ] 1.1 Remove `import pickle` from `plugins/inventory/inventory.py`
- [ ] 1.2 Add `import json` to `plugins/inventory/inventory.py`
- [ ] 1.3 Update `self.cache_filename` to use the `.json` extension instead of `.pkl`
- [ ] 1.4 Rewrite `write_to_cache()` to serialize with `json.dumps` and write via atomic rename: open a sibling `.tmp` file with `os.open(tmp_path, O_CREAT | O_WRONLY | O_TRUNC, 0o600)` (no `O_EXCL` — a stale `.tmp` from a crashed prior run must not block the next run), write via `os.fdopen`, then set `renamed = False`, call `os.rename(tmp_path, final_path)`, set `renamed = True`; in a `finally` block call `os.unlink(tmp_path)` only if `not renamed` — after a successful rename the temp path no longer exists and unlinking it would raise `FileNotFoundError`
- [ ] 1.5 Rewrite `load_from_cache()` to open the JSON file with a `with` block and deserialize with `json.loads`; catch both `json.JSONDecodeError` and `OSError` and fall through to a full API fetch in each case
- [ ] 1.6 Update `is_cache_valid()` to check for the `.json` filename

## 2. Inventory Cache — Default path and directory permissions

- [ ] 2.1 Change the default `cache_path` value in `inventory.ini` from `/tmp` to `~/.cache/ansible-ionos`
- [ ] 2.2 In `IonosCloudInventory.__init__`, expand `~` in `self.cache_path` using `os.path.expanduser` before building `self.cache_filename`
- [ ] 2.3 Before writing the cache, call `os.makedirs(cache_dir, mode=0o700, exist_ok=True)` to ensure the directory exists with safe permissions

## 3. Credential File Permission Check

- [ ] 3.1 Add `import stat` to `plugins/inventory/inventory.py`
- [ ] 3.2 In `read_settings()`, after reading credentials from `inventory.ini`, stat the file with `os.stat`
- [ ] 3.3 If any of `token`, `username`, or `password` are non-empty AND the file mode has `stat.S_IRGRP` or `stat.S_IROTH` set, write a warning to `sys.stderr` with the file path and current mode in octal

## 4. Remove `six` dependency from inventory.py

- [ ] 4.1 Remove `import six` and `from six.moves import configparser` from `plugins/inventory/inventory.py`
- [ ] 4.2 Add `import configparser` (stdlib) at the top of the file
- [ ] 4.3 Remove the `if six.PY3: ... else: configparser.SafeConfigParser()` branch; use `configparser.ConfigParser()` unconditionally
- [ ] 4.4 Verify no other `six` references remain in `inventory.py`
- [ ] 4.5 Run `grep -rn "import six\|from six" plugins/` across the full repo; if no other file imports `six`, check `requirements.txt` — if `six` appears there, remove it

## 5. Context Managers — inventory.py

- [ ] 5.1 Rewrite `read_password_file()` non-executable branch to use `with open(this_path, 'rb') as f:` instead of a bare `open`
- [ ] 5.2 Ensure `write_to_cache()` and `load_from_cache()` file handles (from task 1) also use context managers (covered by tasks 1.4 and 1.5, verify here)

## 6. Context Managers — certificate.py

- [ ] 6.1 Replace the five bare `open(...)` calls in `plugins/modules/certificate.py` (lines 238, 239, 276, 277, 293) with `with open(...) as f: content = f.read()` patterns

## 7. Context Managers — application_load_balancer_forwardingrule.py

- [ ] 7.1 Replace the three bare `open(...)` calls in `plugins/modules/application_load_balancer_forwardingrule.py` (lines 387–389) with `with open(...) as f: content = f.read()` patterns

## 8. Tests

- [ ] 8.1 Update any tests that assert on cache filename (`.pkl` → `.json`) or default `cache_path` value (`/tmp` → `~/.cache/ansible-ionos`)
- [ ] 8.2 Add a unit test for `load_from_cache()` that verifies a crafted malicious pickle file at the cache path is NOT loaded (i.e., the `.pkl` file is ignored)
- [ ] 8.3 Add a unit test for `write_to_cache()` that verifies the written file has mode `0600`
- [ ] 8.4 Add a unit test for the credential file permission warning: set `config_path` to an absolute path string, mock `os.stat` to return a group-readable mode, and assert the warning written to stderr contains `os.path.abspath(config_path)` as the exact path token (not a relative or `~`-prefixed string)
- [ ] 8.5 Add a unit test for the "six not installed" scenario: insert `sys.modules['six'] = None` before importing `inventory.py` and assert no `ImportError` is raised and `configparser.ConfigParser` is used directly
- [ ] 8.6 Add a unit test for `is_cache_valid()` that creates only a legacy `ansible-ionos.pkl` at the cache path (no `ansible-ionos.json`) and asserts `is_cache_valid()` returns `False`
- [ ] 8.7 Add a unit test for `write_to_cache()` that runs the function to completion on valid data and asserts no `FileNotFoundError` is raised — verifying the `finally` block does not call `os.unlink` on the temp path after a successful `os.rename`
