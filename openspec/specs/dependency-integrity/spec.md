# dependency-integrity Specification

## Purpose
TBD - created by archiving change find-and-fix-vulnerabilities-in-the-module-nf63v14. Update Purpose after archive.
## Requirements
### Requirement: All dependencies have lower-bound version constraints
Every entry in `requirements.txt` SHALL specify a lower-bound version constraint using `>=`. Entries that currently have only an upper-bound constraint (e.g., `ionoscloud<7`) SHALL also have a lower bound added (e.g., `ionoscloud>=6.1.0,<7`). Entries with no version constraint at all SHALL have a `>=` lower bound added.

#### Scenario: Dependency installed without version specifier
- **WHEN** `requirements.txt` lists a package with no version specifier (e.g., `cryptography`)
- **THEN** the entry SHALL be updated to include a `>=` lower bound (e.g., `cryptography>=3.4.0`)

#### Scenario: Dependency installed with only upper-bound constraint
- **WHEN** `requirements.txt` lists a package with only an upper bound (e.g., `ionoscloud<7`)
- **THEN** the entry SHALL be updated to include both a lower bound and the existing upper bound (e.g., `ionoscloud>=6.1.0,<7`)

#### Scenario: Dependency already has both bounds
- **WHEN** `requirements.txt` lists a package with both `>=` and `<` constraints
- **THEN** the entry SHALL remain unchanged

### Requirement: Lower-bound versions are free of known CVEs
The lower-bound version selected for each dependency SHALL be a version that does not have a published CVE at the time of the change. The minimum version SHALL be the oldest release that meets both functional requirements and has no known critical or high CVEs.

#### Scenario: Package version has a published CVE
- **WHEN** a candidate lower-bound version has a known CVE rated critical or high
- **THEN** the lower bound SHALL be set to the next version that resolves that CVE

#### Scenario: No CVE-free version is available below the currently installed version
- **WHEN** all versions below the currently installed version have known CVEs
- **THEN** the lower bound SHALL be set to the currently used minimum known-good version

