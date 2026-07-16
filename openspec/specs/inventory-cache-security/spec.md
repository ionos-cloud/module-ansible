# inventory-cache-security Specification

## Purpose
TBD - created by archiving change find-and-fix-vulnerabilities-in-the-module-nruay5i. Update Purpose after archive.
## Requirements
### Requirement: Cache uses JSON serialization
The inventory plugin SHALL serialize cache data to JSON, not pickle. The cache file SHALL be named `ansible-ionos.json`. The inventory plugin SHALL NOT create or read files with the `.pkl` extension.

#### Scenario: Cache written on fresh run
- **WHEN** the inventory script runs with `cache_max_age > 0` and no valid cache exists
- **THEN** the script writes a JSON file at `<cache_path>/ansible-ionos.json` containing the fetched API data

#### Scenario: Cache read on subsequent run within TTL
- **WHEN** the inventory script runs and `<cache_path>/ansible-ionos.json` exists and is within `cache_max_age` seconds old
- **THEN** the script reads and deserializes the JSON file without making API calls

#### Scenario: Corrupt or non-JSON cache file
- **WHEN** the cache file exists but cannot be parsed as valid JSON (`json.JSONDecodeError`)
- **THEN** the script discards the cache, fetches from the API, and overwrites the cache file with fresh JSON

#### Scenario: Cache file unreadable or missing at read time
- **WHEN** `load_from_cache()` raises `OSError` (e.g., the file was deleted between `is_cache_valid()` and the read, or a permission error occurs)
- **THEN** the script falls through to a full API fetch and writes a fresh cache file, identical to the `JSONDecodeError` fallback path

#### Scenario: Legacy pkl file present
- **WHEN** a file named `ansible-ionos.pkl` exists at the cache path
- **THEN** the script ignores it completely and does not attempt to load it

#### Scenario: is_cache_valid returns False when only legacy pkl exists
- **WHEN** `ansible-ionos.pkl` exists at the cache path and no `ansible-ionos.json` file is present
- **THEN** `is_cache_valid()` SHALL return `False`, triggering a full API fetch rather than treating the legacy file as a valid cache

### Requirement: Cache file written with restrictive permissions
The inventory plugin SHALL create and overwrite the cache file with permissions `0600` (owner read/write only), regardless of the process umask. Because `O_CREAT` does not change permissions on an already-existing file, the implementation SHALL use an atomic write-then-rename strategy: write to a sibling temp file at mode `0600` using `os.open`, then call `os.rename` to replace the final path atomically.

#### Scenario: New cache file created
- **WHEN** the inventory script writes the cache file for the first time
- **THEN** the resulting file has mode `0600` and is owned by the running user

#### Scenario: Existing cache file overwritten
- **WHEN** the inventory script refreshes a cache file that already exists on disk
- **THEN** the implementation writes to a `.tmp` sibling file at mode `0600` and renames it over the existing file, ensuring the final file has mode `0600` regardless of the original file's permissions

#### Scenario: Successful cache write does not raise FileNotFoundError
- **WHEN** `write_to_cache()` completes without error (rename succeeds)
- **THEN** the `finally` cleanup block SHALL NOT call `os.unlink` on the temp path, because the rename has already moved it to the final destination; the implementation SHALL guard the unlink with a `renamed` flag that is set only after `os.rename` returns

### Requirement: Default cache path is user-specific
The default value of `cache_path` in `inventory.ini` SHALL be `~/.cache/ansible-ionos`. The script SHALL expand `~` to the running user's home directory at runtime. The script SHALL create the directory with mode `0700` if it does not exist.

#### Scenario: Default cache path used
- **WHEN** `cache_path` is not overridden in `inventory.ini` or environment
- **THEN** cache files are written to `~/.cache/ansible-ionos/ansible-ionos.json`

#### Scenario: Cache directory does not exist
- **WHEN** the resolved cache directory does not exist
- **THEN** the script creates it with mode `0700` before writing the cache file

