# Requirements Traceability

| Requirement | Owner | Evidence | Status |
| --- | --- | --- | --- |
| Public-source hierarchy and immutable raw inputs | `datasets/`, `doctor` | dataset inventory | implemented |
| Source availability states | `DatasetAvailability` | `doctor` reports every public source | implemented |
| Selected-input source identities and checksums | source identity manifest | pinned aggregate capture digests | implemented |
| Dataset role and eligibility gate | `DatasetRole`, `DatasetEligibility` | schema map and decisions | foundation implemented |
| Independent intent provenance | dataset-specific adapters, `IntentProvenanceGrade` | schema map | foundation implemented |
| Locked ON/OFF actions | `SemanticAction` | adapter mappings | implemented |
| Replay/late taxonomy | `ViolationFamily`, `ReplayLateExecutionSubtype` | enum audit | implemented |
| Source-aware matching | `MatchingTier` | source-group tier definitions | foundation implemented |
| Active `(X_interaction, I)` corpus | `datasets.representation`, `workflows.preprocess` | one 19-feature target per attributable capture; no B/E or fabricated trigger | implemented, execution gated by confound audit |
| Representation-confound audit | `datasets.representation.audit_representation` | variances, degenerate timing/capture features, duration, chronology, context and source metadata | implemented, fail closed |
| Conditional flow interface | `models.conditional_flow` | 19-D target and fixed 3-D intent-only condition | implemented; no experiment runner enabled |
| Baseline input contracts | `baselines.contracts` | `q(X)`, `q(X|I)`, `P(I|X)`, per-action one-class | implemented; NO_ACTION source gated |
| Primary protocol freeze | `datasets.freeze`, `workflows.preprocess` | physical clients, source groups, action/split counts, 19-feature schema, scarcity cohort, normalization, holdout, interfaces, seeds, statistics, and unavailable families | implemented for approved Mon(IoT)r primary tier |
| Counterfactuals, FL, statistics | future owners | no confirmatory runs | not started |
| No physical collection dependency | CLI/workflows/config/path/enums | migration audit | implemented |

The remaining deferred work is confirmatory execution and its source-gated
counterfactual/statistical protocol, not approval to collect new data.
