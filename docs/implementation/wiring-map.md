# Wiring Map

| CLI command | Workflow | Public-source responsibility | State |
| --- | --- | --- | --- |
| `doctor` | `workflows.doctor.run_doctor` | configuration and PingPong, TU Wien, CIC source availability | read-only and implemented |
| `preprocess` | `workflows.preprocess.run_preprocess` | future public-source interaction/feature preparation | intentionally unimplemented |
| `prepare` | `workflows.prepare.run_prepare` | future derived-corpus counterfactual preparation | intentionally unimplemented |
| `plan` | `workflows.plan.resolve_plan` | configured experiment matrix | implemented |
| `smoke` | `workflows.smoke.run_smoke` | future minimal public-source pipeline | intentionally unimplemented |
| `run <experiment>` | `workflows.run.run_experiment` | future experiment execution | intentionally unimplemented |
| `status` | `workflows.status.resolve_status` | artifact status | implemented |
| `report` | `workflows.report.run_report` | future structured results | intentionally unimplemented |

There is no `collect` route or physical-acquisition dependency. Architecture
reachability tests pass after the migration. A fresh Graphify report remains
pending because no Graphify executable or installable package is available
in this environment.
