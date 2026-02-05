# AGENTS.md

This repository is operated under strict agent control rules.

## Authority

Tests and Makefile targets define all behavior.
The agent has no authority to bypass them.

## Allowed Commands

The agent may execute ONLY the following commands:

- `make deps`
- `make install`
- `make test`

No other commands are permitted.

## Dependency Management

- All dependencies MUST be handled by `make deps`
- The agent MUST NOT:
  - invoke package managers directly (cargo, pip, npm, go, etc.)
  - download tools or libraries manually
  - modify lockfiles or dependency manifests

If a dependency is missing or incompatible, the agent must stop and request changes to `make deps`.

## Tooling and Installation

- All tool setup MUST be handled by `make install`
- The agent MUST NOT:
  - bootstrap tools inline
  - modify PATH or environment variables outside Makefile logic
  - assume tools are globally available

## Testing

- All verification MUST be performed via `make test`
- The agent MUST NOT:
  - run individual tests
  - filter or select tests
  - invoke test runners directly

Test results are authoritative.
