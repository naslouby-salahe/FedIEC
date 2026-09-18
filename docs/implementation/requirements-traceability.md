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
| Calibration threshold and clean-FPR metric | `evaluation.metrics` | configured clean-calibration quantile and scalar locked-threshold metrics | real-data smoke wired; no violation performance interpreted |
| Primary protocol freeze | `datasets.freeze`, `workflows.preprocess` | physical clients, source groups, action/split counts, 19-feature schema, scarcity cohort, normalization, holdout, interfaces, seeds, statistics, and unavailable families | implemented for approved Mon(IoT)r primary tier |
| Counterfactual feasibility and artifact controls | `datasets.freeze` | per-family feasibility reasons and frozen audit pass rules in the primary manifest | source-feasibility freeze implemented; confirmatory generation remains disabled |
| Counterfactual matching/validity/artifact-control math | `counterfactuals.matching`, `counterfactuals.validity`, `counterfactuals.artifact_control` | caliper/tier ranking, transition/timestamp/physical-timeline checks, dependence-aware equivalence-style A* audit | implemented and unit-tested; unreachable from CLI until a family is source-feasible (justified exemption) |
| Counterfactual generation gate | `counterfactuals.generation` | fails closed with `NotSourceFeasibleError` for every currently frozen family; smoke exercises the gate on real data | implemented, wired into smoke |
| Dependence-aware paired statistics | `statistics.resampling`, `statistics.comparison` | three-level hierarchical bootstrap, device-cluster sign-flip permutation, Holm-Bonferroni correction | implemented and unit-tested; unreachable from CLI until confirmatory run artifacts exist (justified exemption) |
| Heterogeneity distances | `evaluation.heterogeneity` | mean marginal Wasserstein/energy distance, full and protocol-identity-feature (15-18) subsets | implemented, unit-tested, and real-data smoke-wired |
| Transfer analysis (LODO, protocol-feature ablation) | `evaluation.transfer` | eligible-device-count gate (>=4), protocol-identity-feature masking for the frozen 19-D architecture | implemented; unreachable from CLI at smoke scale (justified exemption) |
| Intent-provenance robustness diagnostics | `evaluation.robustness` | missing-intent condition perturbation, duplicate-intent dedup diagnostic; no command-timing boundary invented | implemented, real-data smoke-wired |
| Security/counterfactual evaluation suite | `evaluation.security` | reports per-family evaluated/unavailable status directly from the frozen manifest | implemented, real-data smoke-wired |
| Reporting tables/figures/promotion | `reporting.tables`, `reporting.figures`, `reporting.promotion` | Parquet comparison/per-device/heterogeneity tables, dependency-free SVG seed-effect figure, outputs-to-results promotion | tables implemented and real-data smoke-wired; figures/promotion implemented and unit-reachable, awaiting confirmatory paired-comparison data (justified exemption) |
| `report` workflow | `workflows.report` | inspects `outputs/runs/` for `predictions.parquet`; returns a structured `ReportSummary` when none exist instead of raising | implemented for the current no-confirmatory-artifacts state |
| No physical collection dependency | CLI/workflows/config/path/enums | migration audit | implemented |

The remaining deferred work is confirmatory execution and its source-gated
counterfactual/statistical protocol, not approval to collect new data.
