# Verification Status

| Check | Result |
| --- | --- |
| Ruff | pass after public-source migration |
| Pyright | 0 errors, 0 warnings after migration |
| Pytest | 45 architecture checks pass after public-source boundary hardening |
| Semgrep | pass through committed `.semgrep.yml` and `tests/architecture/test_static_analysis.py` |
| Graphify | fresh AST extraction: 168 nodes and 743 edges; 0 exact duplicate edges. Architecture tests separately confirm no import cycles and CLI/workflow wiring |
| `doctor` | pass: configuration and all three public sources present and valid |
| Adapter enumeration | pass: PingPong 2,000; CIC 264; TU Wien 10,000 typed interactions |
| Boundary regression coverage | pass: exact public-source enums, no collection scaffold, no production source introspection, exact `.value` boundaries, typed adapter contracts, and explicit CLI→workflow map |

No confirmatory experiment is run as part of this foundation migration.
