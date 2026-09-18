# Verification Status

| Check | Result |
| --- | --- |
| Ruff | pass: final implementation-alignment check |
| Pyright | pass: 0 errors, 0 warnings |
| Pytest | pass: 55 checks, including capture-level interface, intent encoding, source identity, and confound-gate coverage |
| Semgrep | pass through committed `.semgrep.yml` and `tests/architecture/test_static_analysis.py` |
| Graphify | fresh AST extraction after primary-freeze and smoke wiring: 246 nodes and 5,688 edges |
| Engineering smoke | pass: frozen primary manifest, raw eligible-capture count, and synthetic 19-D/3-D conditional-flow shape validated; no scientific score was inspected. |
| `doctor` | pass: configuration and all three public sources present and valid |
| Adapter enumeration | pass: PingPong 2,000; CIC 264; TU Wien 10,000; Mon(IoT)r 9,986 non-empty Android ON/OFF typed interactions |
| Mon(IoT)r representation-confound audit | pass after the approved pre-model `PRE_MODEL_STRUCTURAL_DEGENERACY` correction: all 19 features are nonconstant and non-near-constant across 9,986 captures. Packet count range 1–1,388, byte range 60–487,293, capture-duration range 0–155.444 seconds; chronology, site/network contexts, action ordering, and source identity are recorded. |
| Mon(IoT)r primary protocol freeze | pass: 37 physical clients, 9,986 captures, 9,986 non-overlapping individual source groups; scarcity `{10,30,60}` is supported by a fixed 30-client pre-model common-support cohort and `FULL` retains all 37 clients. |
| Selected-input digest freeze | pass: aggregate SHA-256 digests recorded for all adapter-enumerated capture files |
| PingPong capture/trigger clock audit | pass: all 20 selected continuous PCAP ranges contain their converted UTC trigger ranges |
| Boundary regression coverage | pass: exact public-source enums, no collection scaffold, no production source introspection, exact `.value` boundaries, typed adapter contracts, and explicit CLI→workflow map |

No confirmatory experiment is run as part of this implementation-alignment phase.
