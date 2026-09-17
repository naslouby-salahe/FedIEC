# Requirements Traceability — Prompt 1 Scope

Full roadmap-wide traceability (collection through reporting) is built out
incrementally as each area is implemented; a requirement with no
implementation owner yet is listed as `not started` rather than omitted,
so the table stays a complete map of the roadmap rather than a log of
finished work.

| Requirement | Source | Dataset dep. | Config | Enum/type | Owner (impl.) | CLI/workflow | Tests | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Locked semantic actions {NO_ACTION, TURN_ON, TURN_OFF} | Roadmap Sec. 4 | — | — | `SemanticAction` | `enums.py` | — | `test_enums_and_types.py` (indirect, via primitive-ban coverage) | done |
| Violation taxonomy (5 families + observability limit) | Roadmap Sec. 24 | — | — | `ViolationFamily` | `enums.py` | — | none yet | enum done, logic not started |
| Network topology labels | Roadmap Sec. 14 | — | — | `NetworkTopology` | `enums.py` | — | none yet | enum done, collection not started |
| ≥6 devices / ≥3 manufacturers / ≥3 categories | Roadmap Sec. 14 | FedIEC-Contracts | `project.*` | — | `config.yaml`/`config.py` | `doctor` (readiness only) | none yet | config done, benchmark not collected |
| Clean collection counts (150/150/150 per device) | Roadmap Sec. 21 | FedIEC-Contracts | `collection.*` | — | `config.yaml` | — | none yet | config done, collection not started |
| Chronological split 90/30/30 | Roadmap Sec. 22 | FedIEC-Contracts | `split.*` | `SplitPartition` | `config.yaml`/`enums.py` | — | none yet | config+enum done, splitting not started |
| 20-feature network representation | Roadmap Sec. 36 | all four | `features.*` | — | `config.yaml` | — | none yet | config done, extraction not started |
| Shared training-client normalization | Roadmap Sec. 39 | — | — | — | not started | — | none yet | not started |
| Conditional normalizing flow architecture | Roadmap Sec. 40-41 | — | `model.*` | `ModelArchitectureKind` | `config.yaml`/`enums.py` | — | none yet | config done, model not implemented |
| Training config (Adam, lr, seeds 0-9, etc.) | Roadmap Sec. 42 | — | `training.*` | `Optimizer`, `TensorDType` | `config.yaml`/`enums.py` | — | none yet | config done, training loop not implemented |
| FedAvg / federated config | Roadmap Sec. 49 | — | `federated.*` | `AggregationRule`, `ClientWeighting` | `config.yaml`/`enums.py` | — | none yet | config done, FL not implemented |
| Data-scarcity curve n∈{10,30,60,90} | Roadmap Sec. 51 | — | `federated.scarcity_budgets` | — | `config.yaml` | — | none yet | config done, analysis not started |
| Counterfactual caliper/audit tolerances | Roadmap Sec. 25.2, 25.11 | — | `counterfactuals.*` | — | `config.yaml` | — | none yet | config done, matching not implemented |
| Statistical alpha/bootstrap | Roadmap Sec. 66 | — | `statistics.*` | — | `config.yaml` | — | none yet | config done, statistics not implemented |
| PingPong external validation | Roadmap Sec. 27-28 | PingPong | — | `DatasetSource.PINGPONG` | `datasets/pingpong/dataset.py` | `doctor` | none yet (unit test pending) | **adapter implemented and verified** for local-phone/same-vendor — 2000 real interactions, 1000/1000 ON/OFF; remote-phone/ifttt/public-dataset not yet covered |
| TU Wien Philips Hue mechanism replication | Roadmap Sec. 29 | TU Wien Philips Hue | — | `DatasetSource.TU_WIEN_PHILIPS_HUE` | `datasets/tu_wien_philips_hue/dataset.py` | `doctor` | none yet (unit test pending) | **full adapter implemented and verified against all 10000 real files** |
| CIC IoT 2022 optional real-attack | Roadmap Sec. 33 | cic-iot-2022 | — | `DatasetSource.CIC_IOT_2022` | `datasets/cic_iot_2022/dataset.py` | `doctor` | none yet (unit test pending) | **full adapter implemented and verified** — 264 real interactions, 132/132 ON/OFF, companion-app-only |
| Repository/CLI foundation (doctor/collect/preprocess/prepare/plan/smoke/run/status/report) | technical_doc.md Sec. 12 | — | — | — | `cli.py`, `workflows/*.py` | all 9 commands | manual CLI smoke this session | `doctor`/`plan`/`status` real; others wired + honestly `NotImplementedError` |
| One-YAML rule | technical_doc.md Sec. 6.1 | — | `config.yaml` | — | `config.py` | — | `test_config_and_constants.py` | done |
| Config accessed only via `load_config()`, never injected | technical_doc.md Sec. 6.3 (user-clarified this session) | — | — | — | `config.py` | — | `test_config_and_constants.py` | done |
| Primitive-signature ban outside `types.py` | technical_doc.md Sec. 21 | — | — | — | `types.py` | — | `test_enums_and_types.py` | done |
| Path centralization | technical_doc.md Sec. 7 | — | — | `RepositoryPathKey` | `paths.py` | — | none yet | done (module + enum); dedicated test not yet written |

All rows for scientific modules beyond this phase (collection execution,
preprocessing, counterfactuals, models, training, evaluation, statistics,
reporting, and their five-layer test coverage) remain `not started` and are
explicit Prompt 2+ scope, not silently dropped.
