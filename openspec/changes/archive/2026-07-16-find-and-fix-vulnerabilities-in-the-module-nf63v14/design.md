## Context

module-ansible is an Ansible collection for managing IONOS Cloud infrastructure, distributed via Ansible Galaxy. It is used in automated CI/CD pipelines, often in shared environments where multiple users or services share a filesystem. A security audit identified 11 vulnerabilities: 2 critical (pickle RCE, unsafe subprocess), 4 high (path traversal read/write, insecure /tmp cache, bytes/str bug), 3 medium (stack trace disclosure, unvalidated getattr, unpinned deps), 2 low (resource leaks, cosmetic).

Key affected files:
- `plugins/inventory/inventory.py` — critical issues with cache and subprocess
- `plugins/modules/certificate.py`, `k8s_config.py`, `application_load_balancer_forwardingrule.py` — file path traversal
- `plugins/modules/volume.py`, `cube_server.py`, `server.py`, `vcpu_server.py` — stack trace exposure
- `plugins/module_utils/common_ionos_methods.py` — unsafe getattr
- `requirements.txt` — unpinned deps

## Goals / Non-Goals

**Goals:**
- Eliminate all critical and high severity vulnerabilities without breaking existing playbook interfaces
- Address medium severity issues (stack traces, getattr, unpinned deps)
- Maintain full backward compatibility for all existing `ansible_collections.ionoscloudsdk.ionoscloud` module calls

**Non-Goals:**
- Redesign module architecture or change public parameter names
- Add new IONOS Cloud features beyond security hardening
- Full supply-chain audit or SBOM generation
- Address the hardcoded HTTP URL in a comment (cosmetic only, no security impact)
- Replace resource-leak patterns with context managers across all files (addressed only in security-critical paths)

## Decisions

### 1. Replace pickle with JSON for inventory cache

**Decision**: Replace `pickle.load` / `pickle.dump` with `json.load` / `json.dump`. Cache data structure (host dict, inventory dict) is already JSON-serializable.

**Rationale**: Deserializing pickle from a file an attacker can write to is arbitrary code execution. JSON parsers execute no code.

**Alternatives considered**: `shelve` (same risk), `marshal` (same risk), `msgpack` (adds dependency). JSON is zero-dependency and sufficient.

**Cache schema**: `{"version": 1, "data": {...}, "inventory": {...}}`. Version field allows future migration without silent corruption.

The existing pickle already serializes `{'data': self.data, 'inventory': self.inventory}` (see `write_to_cache` at line 504 of `inventory.py`). The JSON schema preserves this structure exactly and adds a `version` wrapper:
- `data` = `self.data` — raw IONOS API fetch results; a dict with keys `datacenters`, `servers`, `volumes`, `lans`, `nics`, `images`, `locations`, `firewallrules`, each mapping to a list of serialized API objects
- `inventory` = `self.inventory` — the Ansible inventory dict; keys include `all` (hosts list), `_meta` (hostvars), plus dynamic group keys (datacenter IDs, location names, availability zones, security group names built in `build_inventory`)

### 2. Cache file location and permissions

**Decision**: Change default cache path from `/tmp/ansible-ionos.pkl` to `~/.ansible/tmp/ionos-inventory-cache.json`. Set file mode 0600 immediately after write using `os.chmod`.

**Rationale**: `/tmp` is world-writable. A local attacker can create a symlink at the cache path before the inventory plugin writes it (TOCTOU) or read a previously written cache file. User home directory is readable only by the owner.

**Backward compatibility**: If users have set `cache_dir` in their inventory config, that path is still used. The default path changes only. Cache miss on first run after upgrade causes a one-time re-fetch from the API — no data loss.

### 3. Subprocess safety for password scripts

**Decision**: Before invoking a password script via `subprocess.Popen`:
1. Resolve to canonical path with `os.path.realpath`
2. Assert `os.path.isfile(canonical)` — reject directories, devices, FIFOs
3. Assert `os.access(canonical, os.X_OK)` — reject non-executable files
4. Pass as a list `[canonical]` to `Popen`, not as a string (no `shell=True`)
5. Decode `stdout` with `.decode('utf-8').strip()` to fix the Python 3 bytes/str bug

**Rationale**: The existing `realpath` call alone does not prevent executing a malicious script placed at a legitimate path. `isfile` + `X_OK` checks add defense in depth. Passing a list prevents shell metacharacter injection.

### 4. Path traversal prevention for file-path parameters

**Decision**: For every module parameter that accepts a filesystem path for reading or writing:
1. Call `os.path.realpath(path)` to resolve symlinks
2. Assert `os.path.isfile(canonical)` for read paths; assert the parent directory exists and is a directory for write paths
3. Raise `AnsibleError` with a generic "invalid file path" message if checks fail

**Files affected**: `certificate.py` (3 params), `k8s_config.py` (1 param), `application_load_balancer_forwardingrule.py` (1 param).

**No prefix restriction**: These modules legitimately read certificates from arbitrary filesystem locations, so restricting to a specific prefix would break valid use cases. The `realpath` + `isfile` pair is the minimal effective guard.

**Alternatives considered**: Restricting to a configured base directory — rejected because certificate paths are legitimately system-wide (e.g., `/etc/letsencrypt/live/`).

### 5. Error message sanitization

**Decision**: Remove `exception=traceback.format_exc()` from all `module.fail_json` calls in `volume.py`, `cube_server.py`, `server.py`, `vcpu_server.py`. Keep the `msg` field intact.

**Rationale**: Stack traces expose internal file paths, line numbers, and code structure. They are not actionable by Ansible playbook authors and are a medium-severity information disclosure. Ansible's `ANSIBLE_DEBUG=1` or `-vvv` flag surfaces exception info for maintainers who need it.

**Alternatives considered**: Gating on `module._verbosity > 2` — rejected as more complex and not worth the branching overhead for what is purely defensive hardening.

### 6. Filter attribute key validation

**Decision**: In `common_ionos_methods.py`, validate each dot-separated key segment against `re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', key_part)` before calling `getattr`. Raise `AnsibleError("Invalid filter key: {key}")` on mismatch.

**Rationale**: Without validation, a filter key like `__class__.__subclasses__` allows accessing private Python internals. The valid attribute names on ionoscloud SDK objects are all snake_case identifiers.

### 7. Dependency version pinning

**Decision**: Add `>=` lower bounds to all unpinned entries in `requirements.txt`. Set lower bounds to the minimum version known to work and that does not have published CVEs. Do not add upper bounds beyond those already present.

**Rationale**: Unpinned deps allow installation of versions with known vulnerabilities. Lower bounds prevent downgrade attacks while remaining flexible for users who need newer versions.

## Risks / Trade-offs

- **Cache format change** → One-time cache miss and API re-fetch on first run after upgrade. Risk: zero data loss.
- **Default cache path change** → Users with scripts that reference `/tmp/ansible-ionos.pkl` will need to update their paths. Document in CHANGELOG.
- **Error message change** → Users who parse `exception` field in fail_json output will see it disappear. Intentional security improvement; document in CHANGELOG.
- **Subprocess isfile + X_OK checks** → Tighter validation may reject edge cases (e.g., password file is a symlink to an executable). `realpath` resolves symlinks before checking, so this is safe.
- **Dependency lower bounds** → Could conflict with user environments pinned to older versions. Only lower bounds are added; no new upper bounds introduced.

## Migration Plan

1. Apply all changes in a single PR targeting the `master` branch.
2. Bump the collection version per semver (patch bump — no interface changes).
3. Add `CHANGELOG` entry noting: cache format change, default cache path change, removal of `exception` field from fail_json.
4. No database migrations, no API changes, no rollback strategy needed.

## Resolved Questions

### Cache path deprecation warning
**Decision**: No pre-deprecation release. Ship the path change in a single patch bump with a CHANGELOG entry.

**Rationale**: The cache file is a runtime artifact created and consumed solely by the plugin — it is not user-authored config and is not referenced in playbooks. A deprecation warning would require a second release cycle for a file that most users never inspect. The CHANGELOG entry (task 9.1) is the appropriate communication channel. Users who have monitoring scripts watching `/tmp/ansible-ionos.pkl` will see a one-time cache miss on upgrade, which is self-correcting.

### Additional modules with user-supplied file paths
**Decision**: Task 3.3 requires a `grep -r 'open(' plugins/modules/` audit during implementation. Any additional `open(param, ...)` calls on user-supplied paths found by that audit SHALL receive the same `realpath` + `isfile` treatment before the PR is merged.
