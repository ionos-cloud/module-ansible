# filter-attribute-safety Specification

## Purpose
TBD - created by archiving change find-and-fix-vulnerabilities-in-the-module-nf63v14. Update Purpose after archive.
## Requirements
### Requirement: Filter keys are validated before attribute access
The `common_ionos_methods.py` filter utility SHALL validate each dot-separated segment of a filter key against the pattern `^[a-zA-Z_][a-zA-Z0-9_]*$` before calling `getattr`. If any segment does not match, the utility SHALL raise `AnsibleError` with a message identifying the invalid key segment. It SHALL NOT call `getattr` with the unvalidated segment.

#### Scenario: Valid snake_case filter key
- **WHEN** a filter key such as `"properties.name"` is passed to the filter utility
- **THEN** each segment (`properties`, `name`) SHALL match the validation pattern and `getattr` SHALL be called for each

#### Scenario: Filter key contains dunder attribute
- **WHEN** a filter key such as `"__class__"` or `"properties.__dict__"` is passed
- **THEN** the utility SHALL raise `AnsibleError("Invalid filter key segment: __class__")` and SHALL NOT call `getattr`

#### Scenario: Filter key contains shell metacharacters or dots only
- **WHEN** a filter key such as `"name; rm -rf /"` or `".."` is passed
- **THEN** the utility SHALL raise `AnsibleError` identifying the invalid segment and SHALL NOT call `getattr`

### Requirement: Traversal stops at leaf values without further getattr calls
When walking a dot-separated filter key, if `getattr` on a key segment returns a value whose type is `str`, `int`, `float`, `bool`, `bytes`, `list`, or `dict`, the utility SHALL compare that value directly to the filter value and SHALL NOT call `getattr` on it for any remaining key segments.

#### Scenario: Filter traverses to a leaf string value
- **WHEN** the key path is `"properties.name"` and `getattr(item, "properties").name` is a `str`
- **THEN** the utility SHALL compare that string directly to the filter value and SHALL NOT call `getattr` on the string

#### Scenario: Leaf type encountered mid-key-path with remaining segments pending
- **WHEN** the key path is `"properties.name.extra"` and traversal of the first two segments yields a `str` value with one segment (`"extra"`) still pending
- **THEN** the utility SHALL return `False` and SHALL NOT call `getattr` on the string value for the remaining segment

#### Scenario: Intermediate attribute is None
- **WHEN** `getattr` on an intermediate key segment returns `None`
- **THEN** the utility SHALL return `False` (non-matching) and SHALL NOT call `getattr` on `None` or raise an exception

