# inventory-plugin-security Specification

## Purpose
TBD - created by archiving change find-and-fix-vulnerabilities-in-the-module-nf63v14. Update Purpose after archive.
## Requirements
### Requirement: Cache uses JSON serialization
The inventory plugin SHALL serialize and deserialize cache data using JSON, not pickle. The cache file SHALL be written with a `{"version": 1, "data": {...}, "inventory": {...}}` schema.

#### Scenario: Cache is written as JSON
- **WHEN** the inventory plugin writes a cache file after a successful API fetch
- **THEN** the file SHALL contain valid JSON and SHALL NOT contain pickle binary data

#### Scenario: Cache is read as JSON
- **WHEN** the inventory plugin reads an existing cache file
- **THEN** it SHALL parse the file with `json.load` and SHALL NOT call `pickle.load` under any circumstances

#### Scenario: Corrupt or non-JSON cache file
- **WHEN** the cache file exists but contains invalid JSON
- **THEN** the plugin SHALL discard the cache, log a warning, and re-fetch from the API

### Requirement: Cache file has restrictive permissions
The inventory plugin SHALL create cache files with mode 0600 (owner read/write only). If an existing cache file has mode other than 0600, the plugin SHALL warn and continue.

#### Scenario: New cache file created
- **WHEN** the inventory plugin writes a new cache file
- **THEN** the file's Unix permissions SHALL be 0600

#### Scenario: Cache directory is world-writable
- **WHEN** the configured cache directory is world-writable (e.g., `/tmp`)
- **THEN** the plugin SHALL emit a warning message indicating the directory is insecure and continue

### Requirement: Default cache path is in user home directory
The default cache file path SHALL be `~/.ansible/tmp/ionos-inventory-cache.json`. The `~` SHALL be resolved via `os.path.expanduser`. Users MAY override this via the `cache_dir` inventory configuration option.

#### Scenario: Default cache path used
- **WHEN** no `cache_dir` is set in the inventory config
- **THEN** the cache file SHALL be written to `~/.ansible/tmp/ionos-inventory-cache.json`

#### Scenario: Custom cache_dir set
- **WHEN** `cache_dir` is set to a non-empty string in the inventory config
- **THEN** the cache file SHALL be written inside that directory

### Requirement: Password script execution is validated before invocation
Before executing a password script, the inventory plugin SHALL:
1. Resolve the path to its canonical form via `os.path.realpath`
2. Verify the resolved path refers to a regular file (`os.path.isfile`)
3. Verify the file is executable by the current process (`os.access(path, os.X_OK)`)
4. Pass the path as a list argument to `subprocess.Popen` (not as a shell string)

#### Scenario: Valid executable password script
- **WHEN** the configured password script path resolves to a regular, executable file
- **THEN** the plugin SHALL invoke it via `Popen([canonical_path])` and read stdout

#### Scenario: Password script path is a directory
- **WHEN** the resolved path is a directory
- **THEN** the plugin SHALL raise `AnsibleError` with a descriptive message and SHALL NOT invoke subprocess

#### Scenario: Password script is not executable
- **WHEN** the resolved path is a regular file but lacks execute permission
- **THEN** the plugin SHALL raise `AnsibleError` and SHALL NOT invoke subprocess

### Requirement: Password script stdout is decoded as UTF-8 string
The inventory plugin SHALL decode subprocess stdout bytes to a UTF-8 string before performing string operations (strip, comparison).

#### Scenario: Script outputs ASCII password
- **WHEN** the password script writes a password to stdout with a trailing newline
- **THEN** the plugin SHALL decode with `.decode('utf-8').strip()` and use the result as the password string

#### Scenario: Script outputs non-UTF-8 bytes
- **WHEN** the password script stdout cannot be decoded as UTF-8
- **THEN** the plugin SHALL raise `AnsibleError` indicating the encoding error

