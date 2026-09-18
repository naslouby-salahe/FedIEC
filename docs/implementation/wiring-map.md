# Wiring Map

| CLI command | Workflow | Public-source responsibility | State |
| --- | --- | --- | --- |
| `doctor` | `workflows.doctor.run_doctor` | configuration and PingPong, TU Wien, CIC, and Mon(IoT)r source availability | read-only and implemented |
| `preprocess` | `workflows.preprocess.run_preprocess` | writes source-group split manifests; for Mon(IoT)r extracts the 19-D `X_interaction` target, writes the confound audit, and writes the final protocol-freeze manifest only after the audit passes | implemented, active representation/freeze path |
| `prepare` | `workflows.prepare.run_prepare` | future derived-corpus counterfactual preparation | intentionally unimplemented |
| `plan` | `workflows.plan.resolve_plan` | configured experiment matrix | implemented |
| `smoke` | `workflows.smoke.run_smoke` | validates the frozen primary artifact against raw capture count and 19-D/3-D conditional-flow shapes using a synthetic tensor only | implemented; no scientific score or experiment |
| `run <experiment>` | `workflows.run.run_experiment` | confirmatory execution remains intentionally blocked until an explicit execution instruction; no B/E route is reachable | intentionally disabled |
| `status` | `workflows.status.resolve_status` | artifact status | implemented |
| `report` | `workflows.report.run_report` | future structured results | intentionally unimplemented |

There is no `collect` route or physical-acquisition dependency. Fresh Graphify
AST extraction on the reconciled tree reports 808 nodes and 2,056 edges. The
architecture suite verifies every command delegates to one workflow and that no
import cycle, active strict-B/E route, or physical-collection route exists.
Graphify output is ignored rather than committed.
