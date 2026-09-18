# Wiring Map

| CLI command | Workflow | Public-source responsibility | State |
| --- | --- | --- | --- |
| `doctor` | `workflows.doctor.run_doctor` | configuration and PingPong, TU Wien, CIC, and Mon(IoT)r source availability | read-only and implemented |
| `preprocess` | `workflows.preprocess.run_preprocess` | writes source-group split manifests; for Mon(IoT)r extracts the 19-D `X_interaction` target, writes the confound audit, and writes the final protocol-freeze manifest only after the audit passes | implemented, active representation/freeze path |
| `prepare` | `workflows.prepare.run_prepare` | writes the frozen counterfactual-feasibility manifest and fails closed if a source-feasible family appears without its raw-timeline generator | implemented for the current all-infeasible primary freeze |
| `plan` | `workflows.plan.resolve_plan` | configured experiment matrix | implemented |
| `smoke` | `workflows.smoke.run_smoke` | loads real Mon(IoT)r-derived 19-D rows, applies training-only transforms/scaling, and traverses local, centralized, FedAvg, baseline, and provenance-freeze paths | implemented; no scientific score or result promotion |
| `run <experiment>` | `workflows.run.run_experiment` | confirmatory execution remains intentionally blocked until an explicit execution instruction; no B/E route is reachable | intentionally disabled |
| `status` | `workflows.status.resolve_status` | artifact status | implemented |
| `report` | `workflows.report.run_report` | future structured results | intentionally unimplemented |

There is no `collect` route or physical-acquisition dependency. Fresh Graphify
AST extraction on the reconciled tree reports 808 nodes and 2,056 edges. The
architecture suite verifies every command delegates to one workflow and that no
import cycle, active strict-B/E route, or physical-collection route exists.
The current fresh Graphify AST extraction reports 872 nodes and 4,434 edges.
Graphify output is ignored rather than committed.
