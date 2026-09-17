# Wiring Map

## Fresh Graphify pass (2026-09-17, `src/fediec`, AST-only — pure code corpus)

```text
140 nodes, 396 edges, 18 communities (1 thin omitted)
0 import cycles
```

God nodes (most-connected — the intended shared low-level layer):
`DomainRecord` (34 edges), `RepositoryPathKey` (22), `DatasetSource` (19),
`ExperimentName`/`ModelArchitectureKind`/`Optimizer`/`ActivationFunction`/
`TensorDType`/`AggregationRule`/`ClientWeighting` (14 each).

This matches the intended dependency direction: `types.py`'s
`DomainRecord` and `paths.py`'s `RepositoryPathKey`/`enums.py`'s
`DatasetSource` sit at the bottom of the stack and are referenced
everywhere, with zero cycles back up into workflows/CLI. Full report kept
locally at `graphify-out/GRAPH_REPORT.md` (not committed — generated
Graphify output, per technical_doc.md Sec. 14 rule 3).

## CLI -> workflow -> leaf (manual cross-check against the graph above)

| CLI command | workflow | reachable major modules | status |
| --- | --- | --- | --- |
| `doctor` | `workflows.doctor.run_doctor` | `config`, `datasets.{fediec_contracts,pingpong,tu_wien_philips_hue,cic_iot_2022}.dataset` | real, read-only, verified end-to-end |
| `collect` | `workflows.collect.run_collect` | (none yet) | wired, raises `NotImplementedError` honestly — no Android/capture pipeline built |
| `preprocess` | `workflows.preprocess.run_preprocess` | (none yet) | wired, raises `NotImplementedError` honestly |
| `prepare` | `workflows.prepare.run_prepare` | (none yet) | wired, raises `NotImplementedError` honestly |
| `plan` | `workflows.plan.resolve_plan` | `config` | real, verified end-to-end (10 experiments x 10 seeds = 100 cells) |
| `smoke` | `workflows.smoke.run_smoke` | (none yet) | wired, raises `NotImplementedError` honestly |
| `run <experiment>` | `workflows.run.run_experiment` | (none yet) | wired, raises `NotImplementedError` honestly |
| `status` | `workflows.status.resolve_status` | `workflows.plan`, `paths` | real, read-only, verified end-to-end |
| `report` | `workflows.report.run_report` | (none yet) | wired, raises `NotImplementedError` honestly |

No workflow silently no-ops or fakes success; every unimplemented command
fails loudly with a specific `NotImplementedError` naming the missing
scientific module and roadmap section.
