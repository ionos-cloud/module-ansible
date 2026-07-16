# credential-file-security Specification

## Purpose
TBD - created by archiving change find-and-fix-vulnerabilities-in-the-module-nruay5i. Update Purpose after archive.
## Requirements
### Requirement: Warn when credential file is group- or world-readable
The inventory plugin SHALL check the file permissions of `inventory.ini` at startup. If the file contains a non-empty value for `token`, `username`, or `password` AND the file is readable by group or other (mode bits include `S_IRGRP` or `S_IROTH`), the plugin SHALL emit a warning to stderr. The plugin SHALL continue execution after the warning.

The `<path>` token in the warning message SHALL be the resolved absolute path of the config file, obtained via `os.path.abspath(config_path)` at the time the check is performed. It SHALL NOT be the raw configured string (which may be relative or contain `~`). This ensures tests can assert an exact, predictable message without path-resolution ambiguity.

#### Scenario: Credentials present and file too permissive
- **WHEN** `inventory.ini` contains a non-empty `token`, `username`, or `password` field
- **AND** the file mode includes group-read or world-read permission
- **THEN** the plugin writes a warning to stderr of the form: `WARNING: inventory.ini contains credentials and is readable by other users (mode: <octal>). Consider running: chmod 600 <path>` where `<path>` is `os.path.abspath(config_path)`

#### Scenario: Credentials present and file permissions are acceptable
- **WHEN** `inventory.ini` contains a non-empty `token`, `username`, or `password` field
- **AND** the file mode is `0600` or stricter
- **THEN** no warning is emitted and execution continues normally

#### Scenario: No credentials in file
- **WHEN** `inventory.ini` has empty `token`, `username`, and `password` fields (credentials provided via environment variables)
- **THEN** no permission warning is emitted regardless of file mode

### Requirement: Python 2 compatibility shim removed from inventory plugin
The inventory plugin SHALL NOT import the `six` library. All Python 2/3 compatibility code in `inventory.py` SHALL be replaced with Python 3 standard library equivalents. Specifically, `configparser.ConfigParser` SHALL be used directly without branching on `six.PY3`.

#### Scenario: Inventory script executed under Python 3
- **WHEN** the inventory script is executed with Python 3.8 or later
- **THEN** it runs without importing `six` and without `ImportError`

#### Scenario: `six` not installed in the environment
- **WHEN** `six` is not installed
- **THEN** the inventory script imports and runs successfully

