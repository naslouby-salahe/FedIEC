# Requirements Traceability

| Requirement | Owner | Evidence | Status |
| --- | --- | --- | --- |
| Public-source hierarchy and immutable raw inputs | `datasets/`, `doctor` | dataset inventory | implemented |
| Source availability states | `DatasetAvailability` | `doctor` reports every public source | implemented |
| Dataset role and eligibility gate | `DatasetRole`, `DatasetEligibility` | schema map and decisions | foundation implemented |
| Independent intent provenance | dataset-specific adapters, `IntentProvenanceGrade` | schema map | foundation implemented |
| Locked ON/OFF actions | `SemanticAction` | adapter mappings | implemented |
| Replay/late taxonomy | `ViolationFamily`, `ReplayLateExecutionSubtype` | enum audit | implemented |
| Source-aware matching | `MatchingTier` | source-group tier definitions | foundation implemented |
| Derived public evaluation corpus | future preprocessing owner | no fabricated fields rule | not started |
| Feature extraction, splitting, counterfactuals, model/training, FL, statistics | future owners | no confirmatory runs | not started |
| No physical collection dependency | CLI/workflows/config/path/enums | migration audit | implemented |

Traceability currently contains 10 requirements: 7 implemented/foundation
implemented and 3 not started. The latter are intentionally deferred work,
not approval to collect new data.
