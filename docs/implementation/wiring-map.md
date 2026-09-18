# Wiring Map

| CLI command | Workflow | Public-source responsibility | State |
| --- | --- | --- | --- |
| `doctor` | `workflows.doctor.run_doctor` | configuration and PingPong, TU Wien, CIC, and Mon(IoT)r source availability | read-only and implemented |
| `preprocess` | `workflows.preprocess.run_preprocess` | writes source-group split manifests; for Mon(IoT)r extracts the 19-D `X_interaction` target, writes the confound audit, and writes the final protocol-freeze manifest only after the audit passes | implemented, active representation/freeze path |
| `prepare` | `workflows.prepare.run_prepare` | writes the frozen counterfactual-feasibility manifest and fails closed if a source-feasible family appears without its raw-timeline generator | implemented for the current all-infeasible primary freeze |
| `plan` | `workflows.plan.resolve_plan` | configured experiment matrix | implemented |
| `smoke` | `workflows.smoke.run_smoke` | loads real Mon(IoT)r-derived 19-D rows, applies training-only transforms/scaling, and traverses local, centralized, FedAvg, baseline, heterogeneity, robustness, security-evaluation, counterfactual-gating, and reporting-table paths | implemented; no scientific score or result promotion |
| `run <experiment>` | `workflows.run.run_experiment` | confirmatory execution remains intentionally blocked until an explicit execution instruction; no B/E route is reachable | intentionally disabled |
| `status` | `workflows.status.resolve_status` | artifact status | implemented |
| `report` | `workflows.report.run_report` | inspects `outputs/runs/` for `predictions.parquet`; returns a structured `ReportSummary(has_confirmatory_run_artifacts=False, ...)` when none exist | implemented for the current no-confirmatory-artifacts state |

There is no `collect` route or physical-acquisition dependency. The
architecture suite verifies every command delegates to one workflow, the
`cli → workflows → {datasets, models, baselines, training, evaluation,
counterfactuals, statistics, reporting} → {enums, types, paths, config}`
import direction, and that no import cycle, active strict-B/E route, or
physical-collection route exists.

`counterfactuals.matching`, `counterfactuals.validity`,
`counterfactuals.artifact_control`, `evaluation.transfer`,
`statistics.resampling`, `statistics.comparison`, `reporting.figures`, and
`reporting.promotion` are real, unit-tested modules that are not yet reachable
from `cli.py`: each requires either a source-feasible violation family (none
currently frozen), a confirmatory run's `predictions.parquet` (none exist
while `run` is intentionally blocked), or at least four eligible devices at
non-smoke scale. `tests/architecture/test_dead_code.py`'s
`_UNREACHABLE_BUT_JUSTIFIED` records the narrow reason for each.
