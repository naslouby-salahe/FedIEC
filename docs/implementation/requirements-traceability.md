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
| Conditional flow interface and fixed-budget Adam runner | `models.conditional_flow`, `training.runner` | 19-D target, fixed 3-D intent-only condition, six affine blocks, configured Adam | smoke-wired; confirmatory execution remains disabled |
| Baseline implementations | `models.baselines`, `baselines.contracts` | action-agnostic density, direct classifier, per-action One-Class SVM, shrinkage covariance score | smoke-wired; NO_ACTION source gated |
| Training-only transforms and shared scaler | `datasets.normalization` | configured `log1p` magnitude transforms; rate features untouched; fit only on supplied training rows | smoke-wired |
| Local, centralized, and FedAvg paths | `training.runner`, `training.federated` | shared conditional-flow training and sample-count-weighted simulated FedAvg accounting | tiny real-data smoke wired; confirmatory matrix not run |
| Primary protocol freeze | `datasets.freeze`, `workflows.preprocess` | physical clients, source groups, action/split counts, 19-feature schema, scarcity cohort, normalization, holdout, interfaces, seeds, statistics, and unavailable families | implemented for approved Mon(IoT)r primary tier |
| Counterfactual feasibility and artifact controls | `datasets.freeze` | per-family feasibility reasons and frozen audit pass rules in the primary manifest | source-feasibility freeze implemented; confirmatory generation remains disabled |
| Counterfactual generation and dependence-aware final statistics | future owners | primary feasibility freeze rejects every family | blocked by source feasibility / not started |
| No physical collection dependency | CLI/workflows/config/path/enums | migration audit | implemented |

The remaining deferred work is confirmatory execution and its source-gated
counterfactual/statistical protocol, not approval to collect new data.
