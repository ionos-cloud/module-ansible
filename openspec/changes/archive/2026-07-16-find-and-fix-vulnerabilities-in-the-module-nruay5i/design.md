## Context

The `IonosCloudInventory` class in `plugins/inventory/inventory.py` caches API responses to disk using Python's `pickle` module. The default cache path is `/tmp` (set in `inventory.ini:37`). A local attacker can write a crafted `ansible-ionos.pkl` to `/tmp` before the script runs, causing arbitrary code execution when `pickle.load()` is called (`inventory.py:498`). This is a CVSS 8.8 (local) vulnerability — exploitable on any shared system (CI runners, jump hosts) running the inventory script.

Separately, `certificate.py` (lines 238, 239, 276, 277, 293) and `application_load_balancer_forwardingrule.py` (lines 387–389) open files for reading without `with` blocks. On CPython this is generally safe due to reference counting, but it is non-idiomatic, fails linting, and could leak descriptors under PyPy or in exception paths.

The `six` library import in `inventory.py` is a remnant of Python 2 support. Python 2 reached EOL in January 2020; carrying the dependency increases the attack surface and signals unmaintained compatibility code.

**Stakeholders:** SDK team (owners), users running inventory on shared/multi-tenant hosts.

## Goals / Non-Goals

**Goals:**
- Eliminate the pickle RCE vector by switching to JSON serialization
- Make the default cache location user-specific and not world-writable
- Restrict written cache file permissions to `0600`
- Emit a runtime warning when `inventory.ini` is group- or world-readable and contains credentials
- Replace all unclosed `open()` calls with `with` context managers
- Remove the `six` import from `inventory.py`

**Non-Goals:**
- Encrypting cache content at rest
- Migrating existing `.pkl` cache files (they are discarded silently on first run)
- Changing the public API or parameter names of any Ansible module
- Auditing dependencies beyond `six` in `inventory.py`

## Decisions

**JSON over pickle for cache serialization**
The cache stores only API-returned data (dicts and lists of primitives). JSON covers this completely and is safe against deserialization attacks. No custom class instances are stored; the switch is lossless.
- Alternative: `msgpack` — faster, binary-safe, but adds a dependency and still requires trusting the source. Rejected.
- Alternative: signed pickle — adds `hmac`, introduces key management. Overkill for local cache. Rejected.

**Default cache path: `~/.cache/ansible-ionos/`**
`os.path.expanduser('~/.cache/ansible-ionos')` is user-specific, typically mode `700`. Avoids the shared `/tmp` attack surface without requiring root or custom configuration.
- Alternative: Keep `/tmp` and just restrict file permissions — insufficient; an attacker can pre-create the file before the script runs (TOCTOU).
- Alternative: Disable cache by default (`cache_max_age = 0`) — already the default in `inventory.ini`. The path change is still needed for users who enable caching.

**Cache file written via atomic rename from a mode `0600` temp file**
Using `open(..., 'w')` creates the file with the process umask applied, which may be too permissive. `O_CREAT` with an explicit mode only sets permissions for newly created files — it does **not** change permissions on an existing file opened with `O_TRUNC`. To enforce `0600` on both new and existing cache files, the implementation SHALL:

1. Write the JSON content to a sibling temp file (`<cache_path>/ansible-ionos.json.tmp`) using `os.open` with `O_CREAT | O_WRONLY | O_TRUNC` (no `O_EXCL`) at mode `0o600`. Omitting `O_EXCL` allows a stale `.tmp` left by a crashed prior run to be silently overwritten; the cache directory is `0700` so other users cannot pre-create the file.
2. Call `os.rename(tmp_path, final_path)` to atomically replace the destination.

On POSIX, `os.rename` is atomic within the same filesystem. The temp file is always `0600` (new file, umask bypassed), so the final file inherits those permissions. A `renamed = False` flag is set to `True` only after `os.rename` returns successfully. In a `finally` block, `os.unlink(tmp_path)` is called only if `not renamed` — after a successful rename the temp path no longer exists and calling `os.unlink` on it would raise `FileNotFoundError`.

- Alternative: `os.unlink` + recreate — removes the file first, then creates fresh with `O_CREAT`. Leaves a short window where the file does not exist; a concurrent reader sees a cache miss. Rejected in favour of atomic rename.
- Alternative: post-write `chmod(path, 0o600)` — simpler but not atomic; there is a window between the write and the chmod where another process can read the file at the original (possibly permissive) mode. Rejected.

**Credential file permission check is a warning, not a hard failure**
Some CI environments intentionally use permissive permissions. A hard failure would break existing pipelines. A warning to stderr is the least-surprise approach and follows the pattern used by `ssh`.

**Remove `six`, use stdlib `configparser` directly**
`configparser.ConfigParser` (capitalized) is available in Python 3.2+; Ansible requires Python 3.8+. No compatibility shim is needed. After the import is removed from `inventory.py`, a full-repo grep for `import six` / `from six` SHALL be run; if no other file imports `six`, it SHALL be removed from `requirements.txt` if present (currently it is not listed there).

## Risks / Trade-offs

- **Cache format break** → Mitigation: on `json.JSONDecodeError` or missing file, silently fall back to a full API fetch and rewrite. No user action needed.
- **`~/.cache/` may not exist on all systems** → Mitigation: `os.makedirs(cache_dir, mode=0o700, exist_ok=True)` before writing.
- **Stale `.tmp` file from a crashed run** → Mitigated by omitting `O_EXCL`; `O_TRUNC` silently overwrites a leftover temp file rather than raising `FileExistsError` before the `finally` cleanup can run. The cache directory is `0700`, so only the owning user can create files there — the security property that `O_EXCL` would have provided is already covered by directory permissions.
- **Linting tools may flag `os.fdopen` pattern as unusual** → Acceptable; add a brief inline comment.

## Migration Plan

1. Merge the change to `master`.
2. On first run after upgrade, if `ansible-ionos.pkl` exists at the old path, it will not be found at the new path — a fresh API call occurs and the new JSON cache is written to `~/.cache/ansible-ionos/ansible-ionos.json`.
3. Users with `cache_path` overridden in `inventory.ini` are unaffected by the path change but will still get the format switch; the `.pkl` at their custom path will be ignored (not found under the new `.json` filename).
4. Rollback: revert the commit; old pkl caches will be read again normally.

## Open Questions

- Should the `.pkl` file at the old default path be proactively deleted on first run to avoid confusion? (Current answer: no — do not touch files we did not create.)
- Is there a CI test that writes to `/tmp/ansible-ionos.pkl`? Needs verification during implementation.
