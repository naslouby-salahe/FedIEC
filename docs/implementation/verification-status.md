# Verification Status

| Check | Result |
| --- | --- |
| Ruff | pass: `ruff check src tests` clean after the statistics/evaluation/counterfactuals/reporting build-out |
| Pyright | pass: 0 errors, 0 warnings on `src tests` |
| Pytest | pass: 72 checks across unit, integration, protocol, architecture, and E2E layers; adds `statistics.comparison` (Holm correction, paired effect estimate), `evaluation.heterogeneity`, and `counterfactuals` (matching, validity, artifact-control pass/fail, generation gating) unit coverage |
| Semgrep | pass through committed `.semgrep.yml` and `tests/architecture/test_static_analysis.py`: 0 findings across 55 tracked files |
| Wiring/reachability | pass: `test_wiring.py`, `test_dead_code.py`, `test_function_reachability.py`, and `test_dependencies.py` verify CLI→workflow delegation, module reachability (with narrow, documented exemptions for pre-confirmatory-data future-tier code), and the `cli → workflows → {datasets, models, baselines, training, evaluation, counterfactuals, statistics, reporting} → {enums, types, paths, config}` import direction |
| Engineering smoke | pass: `fediec smoke` used real derived Mon(IoT)r capture rows, locked transforms/training-only scaler, local and centralized flow training, simulated FedAvg, all four baselines, device/action/protocol-identity-feature heterogeneity distances, missing/duplicate-intent robustness diagnostics, the security-evaluation suite, and the counterfactual-generation fail-closed gate. No score or performance result was interpreted. |
| `preprocess`/`prepare`/`status`/`report` (real run) | pass: executed against real raw data for all four public sources; `report` correctly reports `has_confirmatory_run_artifacts=False` since `run` remains intentionally blocked |
| `doctor` | pass: configuration and all three public sources present and valid |
| Adapter enumeration | pass: PingPong 2,000; CIC 264; TU Wien 10,000; Mon(IoT)r 9,986 non-empty Android ON/OFF typed interactions |
| Mon(IoT)r representation-confound audit | pass after the approved pre-model `PRE_MODEL_STRUCTURAL_DEGENERACY` correction: all 19 features are nonconstant and non-near-constant across 9,986 captures. Packet count range 1–1,388, byte range 60–487,293, capture-duration range 0–155.444 seconds; chronology, site/network contexts, action ordering, and source identity are recorded. |
| Mon(IoT)r primary protocol freeze | pass: 37 physical clients, 9,986 captures, 9,986 non-overlapping individual source groups; scarcity `{10,30,60}` is supported by a fixed 30-client pre-model common-support cohort and `FULL` retains all 37 clients. |
| Selected-input digest freeze | pass: aggregate SHA-256 digests recorded for all adapter-enumerated capture files |
| PingPong capture/trigger clock audit | pass: all 20 selected continuous PCAP ranges contain their converted UTC trigger ranges |
| Boundary regression coverage | pass: exact public-source enums, no collection scaffold, no production source introspection, exact `.value` boundaries, typed adapter contracts, and explicit CLI→workflow map |

No confirmatory experiment is run as part of this implementation-alignment phase.
