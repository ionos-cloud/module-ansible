## ADDED Requirements

### Requirement: fail_json calls do not include stack traces
All `module.fail_json` calls in the collection's modules SHALL NOT include the `exception` keyword argument. The `msg` field SHALL contain a human-readable error description without internal file paths or line numbers.

Affected modules: `volume.py`, `cube_server.py`, `server.py`, `vcpu_server.py`.

#### Scenario: API call raises an exception
- **WHEN** an ionoscloud API call raises an exception inside a module
- **THEN** the module SHALL call `module.fail_json(msg=<error_message>)` WITHOUT passing `exception=traceback.format_exc()`

#### Scenario: Unexpected exception during module execution
- **WHEN** an unexpected Python exception occurs during module execution
- **THEN** the module SHALL call `module.fail_json(msg="An unexpected error occurred: <exception type>")` and SHALL NOT include the full traceback in the response

### Requirement: Error message strings are derived solely from exception attributes
When constructing the `msg` argument for `module.fail_json`, modules SHALL use only exception attributes such as `str(e)` or `e.message`. Modules SHALL NOT manually concatenate traceback text, `traceback.format_exc()` output, or similar formatted call-stack strings into the `msg` argument.

#### Scenario: ionoscloud SDK exception is caught
- **WHEN** an ionoscloud SDK call raises an exception inside a module
- **THEN** the module SHALL pass `msg=str(e)` (or equivalent exception attribute) to `module.fail_json` and SHALL NOT concatenate traceback text into that string

#### Scenario: Ansible debug mode is active
- **WHEN** Ansible is invoked with `-vvv` or `ANSIBLE_DEBUG=1`
- **THEN** Ansible's own debug infrastructure MAY expose stack traces; the module itself still SHALL NOT add them to `fail_json`
