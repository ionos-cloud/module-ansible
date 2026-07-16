# module-path-traversal Specification

## Purpose
TBD - created by archiving change find-and-fix-vulnerabilities-in-the-module-nf63v14. Update Purpose after archive.
## Requirements
### Requirement: File-path parameters are canonicalized before use
Any module parameter that accepts a filesystem path for reading or writing SHALL be resolved to its canonical absolute path via `os.path.realpath` before any file operation is performed.

Affected parameters and modules:
- `certificate.py`: `certificate_file`, `certificate_chain_file`, `private_key_file`
- `application_load_balancer_forwardingrule.py`: the `certificate_file`, `private_key_file`, and `certificate_chain_file` dict keys within each element of the `new_server_certificates` module parameter
- `k8s_config.py`: `config_file`

#### Scenario: Path with relative components is read
- **WHEN** a module parameter contains a path with `..` components (e.g., `../../etc/passwd`)
- **THEN** the module SHALL resolve it via `os.path.realpath` before opening, resulting in the canonical absolute path

#### Scenario: Symlink path is resolved
- **WHEN** a module parameter contains a path that is a symlink
- **THEN** the module SHALL resolve the symlink to its target via `os.path.realpath` before opening

### Requirement: Read file-path parameters must reference regular files
Before reading a file specified by a module parameter, the module SHALL verify that the resolved canonical path refers to a regular file (`os.path.isfile`). If the check fails, the module SHALL call `module.fail_json` with a message indicating the path is invalid and SHALL NOT open the file.

#### Scenario: Valid certificate file path
- **WHEN** `certificate_file` resolves to an existing regular file
- **THEN** the module SHALL read its contents and proceed normally

#### Scenario: Certificate file path is a directory
- **WHEN** `certificate_file` resolves to a directory
- **THEN** the module SHALL call `module.fail_json(msg="Invalid file path: not a regular file")` and SHALL NOT attempt to open it

#### Scenario: Certificate file does not exist
- **WHEN** `certificate_file` resolves to a path that does not exist
- **THEN** the module SHALL call `module.fail_json(msg="File not found: <path>")` and SHALL NOT attempt to open it

### Requirement: Write file-path parameters must have a valid parent directory
Before writing to a path specified by a module parameter (`config_file` in `k8s_config.py`), the module SHALL verify that the parent directory of the resolved canonical path exists and is a directory (`os.path.isdir`). If the check fails, the module SHALL call `module.fail_json` with a descriptive message and SHALL NOT write the file.

#### Scenario: Valid kubeconfig write path
- **WHEN** `config_file` resolves to a path whose parent directory exists
- **THEN** the module SHALL write the kubeconfig content to that path

#### Scenario: Kubeconfig write path has non-existent parent directory
- **WHEN** `config_file` resolves to a path whose parent directory does not exist
- **THEN** the module SHALL call `module.fail_json(msg="Parent directory does not exist: <dir>")` and SHALL NOT write the file

#### Scenario: Kubeconfig write path is under a world-writable directory
- **WHEN** `config_file` resolves to a path inside a world-writable directory (e.g., `/tmp`)
- **THEN** the module SHALL proceed with the write (user explicitly chose this path) but SHALL emit a warning via `module.warn`

