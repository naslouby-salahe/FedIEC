# Verification Status

| Check | Result |
| --- | --- |
| Ruff | pass after public-source migration |
| Pyright | 0 errors, 0 warnings after migration |
| Pytest | 36 architecture checks pass after migration |
| Semgrep | pass through `tests/architecture/test_static_analysis.py` |
| Graphify | executable unavailable; architecture reachability tests pass, but this remains an environment blocker |
| `doctor` | pass: configuration and all three public sources present and valid |
| Adapter enumeration | pass: PingPong 2,000; CIC 264; TU Wien 10,000 typed interactions |

No confirmatory experiment is run as part of this foundation migration.
