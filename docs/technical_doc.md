# FedIEC Technical Documentation

## 1. Purpose

This document defines the **technical structure, implementation rules, architecture constraints, testing rules, tooling, artifact conventions, and repository discipline** for FedIEC.

It is intentionally technical. The scientific protocol, research questions, methodology, experiment definitions, statistical design, and evidence rules remain authoritative in:

- `docs/FedIEC_Roadmap.md`

This file is authoritative for:

- repository structure;
- module responsibilities;
- configuration policy;
- enum and type policy;
- CLI and workflow wiring;
- static analysis;
- Graphify rules;
- testing organization;
- dead-code and deletion policy;
- data/output/result organization;
- serialization and provenance;
- code-quality constraints;
- change discipline.

The repository must remain **lean, explicit, typed, reproducible, and scientifically faithful**.

---

## 2. Authority and Change Rules

1. `docs/FedIEC_Roadmap.md` is the scientific source of truth.
2. `docs/technical_doc.md` is the technical and architectural source of truth.
3. `config.yaml` is the single runtime/research configuration source of truth.
4. Code must implement the roadmap; code must not silently redefine the protocol.
5. If implementation reality conflicts with the roadmap, surface the conflict rather than silently changing either side.
6. Scientific formulas, semantics, chronology, leakage rules, datasets, metrics, statistical methods, seed roles, exclusion semantics, and experiment meaning must not drift during refactoring.
7. Empirical quantities may change only when real evidence requires them; they must not be changed merely to make a test or experiment pass.
8. Do not add files, folders, abstractions, datasets, experiment families, configuration files, or infrastructure merely because they are conventional.
9. Any structural addition must have a clear responsibility that cannot reasonably belong to an existing module.
10. When the repository structure changes intentionally, update this document in the same change.
11. Do not create compatibility structure for hypothetical future needs.
12. Prefer the smallest architecture that preserves clear responsibilities and scientific correctness.

---

## 3. Locked Repository Structure

Empty package-marker `__init__.py` files may exist where Python packaging requires them. They are omitted below when they add no architectural meaning.

```text
FedIEC/
│
├── pyproject.toml
│   # Python package metadata, dependencies, and tool configuration.
│   # Ruff, Pyright, Pytest, coverage-related settings, and formatter settings live here.
│
├── README.md
│   # Short repository overview, installation instructions, and CLI examples.
│   # It must not duplicate the roadmap or become a second technical specification.
│
├── .gitignore
│   # Excludes raw/private data where needed, outputs, caches, local environments,
│   # generated Graphify/Semgrep temporary files, and other reproducible workspace material.
│
├── config.yaml
│   # The only committed scientific configuration YAML/YML file.
│   # Contains all configurable public-source, model, training,
│   # federated, experiment, evaluation, statistics, and reporting parameters.
│
├── docs/
│   ├── FedIEC_Roadmap.md
│   │   # Scientific source of truth.
│   │
│   ├── technical_doc.md
│   │   # This document: architecture, tree, tooling, coding, testing, and artifact rules.
│   │
│   ├── roadmap_changes.md
│   │   # Reasoning behind surgical roadmap updates (CLAUDE.md's change protocol).
│   │   # Explains why; the roadmap itself stays clean and current, not a changelog.
│   │
│   └── implementation/
│       # Human-authored implementation tracking: checklist, requirement
│       # traceability, dataset inventory/schema map, wiring map, decisions
│       # and blockers, verification status. Not a second architecture spec.
│
├── data/
│   └── raw/
│       ├── PingPong/
│       │   # Untouched external PingPong source material.
│       │
│       ├── TU Wien Philips Hue/
│       │   # Untouched TU Wien Philips Hue source material.
│       │
│       └── cic-iot-2022/
│           # Optional real-attack source material when present. On-disk name
│           # is lowercase-hyphen (verified), not the "CIC IoT 2022" spelling
│           # used in prose elsewhere in this document and the roadmap.
│           # It may support real-attack evaluation only if roadmap eligibility is established.
│
├── src/
│   └── fediec/
│       ├── __init__.py
│       │   # Package marker only; no hidden initialization logic.
│       │
│       ├── cli.py
│       │   # Thin Typer CLI.
│       │   # Parses CLI input and delegates each command to exactly one workflow.
│       │   # Contains no scientific/business implementation.
│       │
│       ├── config.py
│       │   # Loads config.yaml once and validates it into typed Pydantic v2 models.
│       │   # No other source module parses YAML directly.
│       │
│       ├── enums.py
│       │   # Central home for project-wide categorical enums:
│       │   # actions, datasets, splits, topologies, violation families, regimes,
│       │   # background strata, experiment names, statuses, and similar categories.
│       │
│       ├── types.py
│       │   # Central home for validated identifiers, constrained scalar types,
│       │   # domain records, typed aliases, and boundary-level value objects.
│       │
│       ├── paths.py
│       │   # Sole resolver from a RepositoryPathKey (enums.py) to a filesystem
│       │   # path. No other module constructs a known repository/dataset/
│       │   # output/result location by string concatenation.
│       │   # The root comes from FEDIEC_REPOSITORY_ROOT or an explicit working
│       │   # directory containing config.yaml; it never inspects source-file paths.
│       │
│       ├── artifacts.py
│       │   # Shared compact artifact IO, checksums, provenance metadata, manifests,
│       │   # config hashes, Git commit capture, and safe serialization conventions.
│       │
│       ├── datasets/
│       │   ├── pingpong/
│       │   │   └── dataset.py
│       │   │       # PingPong loading, independent intent/action mapping,
│       │   │       # eligibility checks, and mapping into shared FedIEC domain objects.
│       │   │
│       │   ├── tu_wien_philips_hue/
│       │   │   └── dataset.py
│       │   │       # TU Wien Philips Hue loading, repeated ON/OFF capture handling,
│       │   │       # metadata validation, and mechanism-replication mapping.
│       │   │
│       │   └── cic_iot_2022/
│       │       └── dataset.py
│       │           # Optional real-attack dataset loading and strict alignment eligibility.
│       │           # It must not manufacture missing intent/action alignment.
│       │
│       ├── preprocessing/
│       │   ├── interactions.py
│       │   │   # Converts raw intent/capture/session material into valid (B, I, E) observations
│       │   │   # and applies frozen interaction-level exclusion rules.
│       │   │
│       │   ├── features.py
│       │   │   # Extracts the locked pre-action and post-action network feature representation.
│       │   │
│       │   ├── splitting.py
│       │   │   # Builds chronological train/calibration/test partitions and transfer folds.
│       │   │
│       │   └── normalization.py
│       │       # Training-client-only feature transforms and shared scaler construction.
│       │
│       ├── counterfactuals/
│       │   ├── matching.py
│       │   │   # Training-derived calipers, donor hierarchy, context-distance matching,
│       │   │   # donor reuse tracking, and dependency metadata.
│       │   │
│       │   ├── generation.py
│       │   │   # Generates omission, substitution, uncommanded execution,
│       │   │   # excess execution, and temporally misaligned execution cases.
│       │   │
│       │   ├── validity.py
│       │   │   # Transition semantics, B→E boundary continuity, timestamp/order checks,
│       │   │   # and physical-timeline feasibility.
│       │   │
│       │   └── artifact_control.py
│       │       # Replacement/translation and EXCESS-composition artifact-control procedures.
│       │       # Scientific artifact control remains required even though no top-level audit/ exists.
│       │
│       ├── models/
│       │   ├── contract.py
│       │   │   # Main conditional contract model p(E | B, I).
│       │   │
│       │   └── baselines.py
│       │       # Execution-only, intent-only, direct action-classification,
│       │       # one-class, and simple statistical baselines.
│       │
│       ├── training/
│       │   ├── runner.py
│       │   │   # Shared deterministic neural training loop plus local and centralized regimes.
│       │   │   # Handles seeds, fixed schedules, checkpoints, and training summaries.
│       │   │
│       │   └── federated.py
│       │       # Flower client/server orchestration, FedAvg strategy,
│       │       # federated normalization statistics, and communication accounting.
│       │
│       ├── evaluation/
│       │   ├── metrics.py
│       │   │   # AUROC, AUPRC, F1, balanced accuracy, TPR/FPR,
│       │   │   # calibration metrics, and per-device/per-violation summaries.
│       │   │
│       │   ├── heterogeneity.py
│       │   │   # Cross-device/manufacturer/topology distribution comparisons.
│       │   │
│       │   ├── transfer.py
│       │   │   # Leave-one-device-out, topology-stratified, protocol-feature-ablation,
│       │   │   # and eligible leave-one-manufacturer-out evaluation.
│       │   │
│       │   ├── robustness.py
│       │   │   # Intent provenance jitter/delay/missing/duplicate robustness analysis.
│       │   │
│       │   └── security.py
│       │       # Counterfactual, physical-violation, and eligible real-attack evaluation.
│       │
│       ├── statistics/
│       │   ├── resampling.py
│       │   │   # Hierarchical bootstrap/resampling at the correct dependency levels.
│       │   │
│       │   └── comparison.py
│       │       # Paired effects, cluster-aware permutation/randomization,
│       │       # multiplicity correction, and final statistical comparisons.
│       │
│       ├── reporting/
│       │   ├── tables.py
│       │   │   # Generates manuscript/chapter-ready tabular artifacts.
│       │   │
│       │   ├── figures.py
│       │   │   # Generates manuscript/chapter-ready figures.
│       │   │
│       │   └── promotion.py
│       │       # Copies only finalized, provenance-complete evidence from outputs/ to results/.
│       │       # It does not generate claims or markdown reports.
│       │
│       └── workflows/
│           ├── doctor.py
│           │   # Fast environment, path, configuration, dependency, and dataset sanity checks.
│           │
│           ├── preprocess.py
│           │   # Raw data → interactions → features → splits → normalization artifacts.
│           │
│           ├── prepare.py
│           │   # Counterfactual preparation, manifests, dependency metadata,
│           │   # and physical/security experiment preparation.
│           │
│           ├── plan.py
│           │   # Resolves the configured experiment matrix without executing experiments.
│           │
│           ├── smoke.py
│           │   # Small end-to-end validation using minimal data and minimal compute.
│           │
│           ├── run.py
│           │   # Executes one named experiment/regime according to config.yaml.
│           │
│           ├── status.py
│           │   # Reports expected/completed/missing experiment cells and artifact state.
│           │
│           └── report.py
│               # Runs final statistics and produces compact candidate tables/figures.
│
├── tests/
│   ├── conftest.py
│   │   # Shared deterministic fixtures and test configuration.
│   │
│   ├── fixtures/
│   │   ├── raw/
│   │   │   # Tiny synthetic or legally redistributable raw examples only.
│   │   ├── processed/
│   │   │   # Tiny expected processed artifacts used for deterministic testing.
│   │   └── manifests/
│   │       # Minimal provenance/split/counterfactual manifests used by tests.
│   │
│   ├── unit/
│   │   ├── test_config.py
│   │   │   # Single-YAML loading, validation, defaults, and invalid configurations.
│   │   ├── test_enums_and_types.py
│   │   │   # Enum completeness, serialization boundaries, identifiers, and value objects.
│   │   ├── test_datasets.py
│   │   │   # Dataset-specific loading, schema mapping, and eligibility behavior.
│   │   ├── test_collection.py
│   │   │   # Scheduling, synchronization, settling, capture metadata, and physical-violation helpers.
│   │   ├── test_preprocessing.py
│   │   │   # Interaction construction, feature extraction, splits, and normalization.
│   │   ├── test_counterfactuals.py
│   │   │   # Matching, generation, validity, dependency, and artifact-control logic.
│   │   ├── test_models_and_training.py
│   │   │   # Model shapes, deterministic scoring, local/centralized training, and checkpoint behavior.
│   │   ├── test_federated.py
│   │   │   # Federated client/server behavior, FedAvg, normalization statistics, and communication metadata.
│   │   └── test_evaluation_and_statistics.py
│   │       # Metrics, transfer, robustness, security evaluation, resampling, and paired comparisons.
│   │
│   ├── integration/
│   │   ├── test_raw_to_features.py
│   │   │   # Raw capture + intent → valid interaction/feature artifact.
│   │   ├── test_counterfactual_pipeline.py
│   │   │   # Held-out raw material → valid counterfactual + provenance/dependency records.
│   │   ├── test_training_pipeline.py
│   │   │   # Processed benchmark → model → prediction artifact.
│   │   ├── test_federated_pipeline.py
│   │   │   # Tiny multi-client federated training path.
│   │   ├── test_transfer_pipeline.py
│   │   │   # Held-out-device/manufacturer path with no target leakage.
│   │   └── test_statistics_pipeline.py
│   │       # Prediction artifacts → dependency-aware final statistical summaries.
│   │
│   ├── protocol/
│   │   ├── test_collection_rules.py
│   │   │   # Collection/session/day, action randomization, settling, synchronization,
│   │   │   # device attribution, and NO_ACTION invariants.
│   │   ├── test_split_and_leakage_rules.py
│   │   │   # Chronology, partition isolation, scaler leakage, and calibration/test isolation.
│   │   ├── test_counterfactual_rules.py
│   │   │   # Frozen calipers, donor hierarchy, transitions, boundaries, timestamp ordering,
│   │   │   # EXCESS feasibility, and source dependency.
│   │   ├── test_zero_shot_rules.py
│   │   │   # Held-out devices/manufacturers contribute no forbidden training,
│   │   │   # normalization, calibration, or threshold information.
│   │   └── test_statistical_rules.py
│   │       # Seeds and generated observations are not treated as fake independent units.
│   │
│   ├── architecture/
│   │   ├── test_static_analysis.py
│   │   │   # Requires Ruff, Pyright, and Semgrep checks to pass.
│   │   │   # Custom Semgrep rules are created temporarily at runtime; no second YAML is committed.
│   │   ├── test_wiring.py
│   │   │   # Uses a fresh Graphify call graph to verify CLI → workflow → service → leaf wiring,
│   │   │   # reachable callable counts, leaf counts, and call depth.
│   │   ├── test_dead_code.py
│   │   │   # Detects unreachable implementation, stale aliases/shims, orphan modules,
│   │   │   # obsolete experiment paths, and disconnected functionality.
│   │   ├── test_dependencies.py
│   │   │   # Enforces allowed package dependency directions and prevents circular architecture.
│   │   ├── test_config_and_constants.py
│   │   │   # Enforces the YAML policy, central configuration access, and absence of hidden research constants.
│   │   ├── test_enums_and_types.py
│   │   │   # Enforces enum boundaries, typed service IO, and primitive-leak restrictions.
│   │   └── test_hygiene.py
│   │       # Detects TODO debt, forbidden generic modules, wrapper-only abstractions,
│   │       # accidental generated code, duplicated compatibility paths, and other repository drift.
│   │
│   └── e2e/
│       ├── test_smoke.py
│       │   # Tiny full pipeline through the public CLI.
│       ├── test_run.py
│       │   # Named experiment execution through the real CLI wiring.
│       └── test_report.py
│           # Final statistics/reporting path from compact test artifacts.
│
├── outputs/
│   ├── processed/
│   │   ├── pingpong/
│   │   │   # Compact derived PingPong data.
│   │   ├── tu-wien-philips-hue/
│   │   │   # Compact derived TU Wien data.
│   │   └── cic-iot-2022/
│   │       # Compact derived optional aligned real-attack data.
│   │
│   ├── benchmark/
│   │   ├── splits/
│   │   │   # Compact split assignments and fold manifests.
│   │   ├── counterfactuals/
│   │   │   # Compact generated counterfactual feature/timeline descriptors and provenance.
│   │   └── manifests/
│   │       # Frozen benchmark, matching, dependency, feasibility, and provenance manifests.
│   │
│   ├── runs/
│   │   └── <experiment>/<seed>/
│   │       ├── manifest.json
│   │       │   # Exact experiment/config/data/Git/seed provenance.
│   │       ├── model.safetensors
│   │       │   # Final reusable model checkpoint only when required.
│   │       ├── predictions.parquet
│   │       │   # Compact per-observation scores/predictions required for later statistics.
│   │       └── metrics.json
│   │           # Small convenience summary; never the only evidence source.
│   │
│   ├── analyses/
│   │   ├── scarcity/
│   │   │   # Compact derived scarcity summaries.
│   │   ├── heterogeneity/
│   │   │   # Compact device/manufacturer/topology summaries.
│   │   ├── transfer/
│   │   │   # Compact transfer/holdout summaries.
│   │   ├── provenance/
│   │   │   # Compact intent-provenance robustness summaries.
│   │   └── security/
│   │       # Compact counterfactual/physical/eligible real-attack summaries.
│   │
│   └── reports/
│       ├── tables/
│       │   # Candidate generated tables before final promotion.
│       └── figures/
│           # Candidate generated figures before final promotion.
│
└── results/
    ├── benchmark/
    │   ├── summary.parquet
    │   │   # Final benchmark composition and eligibility evidence.
    │   ├── exclusions.parquet
    │   │   # Final exclusion counts and frozen reasons.
    │   ├── counterfactuals.parquet
    │   │   # Final feasibility, dependency, and artifact-control summary.
    │
    ├── experiments/
    │   ├── intent-value/
    │   │   # Final p(E|B,I) versus p(E|B) evidence.
    │   ├── pre-context-value/
    │   │   # Final p(E|B,I) versus p(E|I) evidence.
    │   ├── federated-collaboration/
    │   │   # Final federated versus local evidence.
    │   ├── data-scarcity/
    │   │   # Final collaboration-under-scarcity evidence.
    │   ├── centralized-comparison/
    │   │   # Final centralized reference comparison.
    │   ├── heterogeneity/
    │   │   # Final device/manufacturer/topology heterogeneity evidence.
    │   ├── transfer/
    │   │   # Final LODO/topology/protocol/eligible LOMO evidence.
    │   ├── provenance-robustness/
    │   │   # Final intent-provenance robustness evidence.
    │   ├── observed-control-failures/
    │   │   # Final independently documented public-source failure evidence, when eligible.
    │   └── external-validation/
    │       # Final PingPong, TU Wien, and eligible real-attack evidence kept distinguishable.
    │
    ├── statistics/
    │   ├── effects.parquet
    │   │   # Final paired effect estimates.
    │   ├── confidence-intervals.parquet
    │   │   # Final hierarchical uncertainty estimates.
    │   ├── significance.parquet
    │   │   # Final permutation/randomization results and multiplicity adjustments.
    │   └── per-device.parquet
    │       # Final device-level effects retained explicitly.
    │
    ├── tables/
    │   # Tables actually intended for the chapter/manuscript.
    │
    └── figures/
        # Figures actually intended for the chapter/manuscript.
```

---

## 4. Explicitly Forbidden Repository Folders and Concepts

The following must **not** be introduced unless explicitly reconsidered later:

- `claims/`
- `claim_registry/`
- `claim-gates/`
- top-level `audit/`
- generic `utils/`
- generic `helpers/`
- generic `common/`
- generic `misc/`
- generic dumping-ground `core/`
- `legacy/` created merely to avoid deleting obsolete code
- second configuration directories
- `data/processed/`
- `data/interim/`
- generated markdown-report directories
- duplicate experiment-package trees that mirror configuration
- one source-code package per experiment when the experiment can be declarative
- separate files containing only one trivial wrapper around another function

Scientific procedures that the roadmap calls an *artifact audit* remain implemented under the owning scientific module, currently `counterfactuals/artifact_control.py`. Removing an `audit/` folder does not remove those scientific requirements.

No production code may exist solely to generate or enforce prose claims.

---

## 5. Minimalism and File-Splitting Rules

1. Separate responsibilities, not individual functions.
2. A new file requires a coherent independent responsibility.
3. Do not create a file merely because a class or function exists.
4. Merge tightly coupled logic when splitting it would produce wrapper files.
5. Split a file when it contains genuinely independent domains with different change reasons.
6. Avoid deep package nesting.
7. Avoid one-file packages unless the dataset/package identity itself is meaningful.
8. Dataset-specific packages are allowed because each external dataset has independent loading and eligibility semantics.
9. Experiment implementations should reuse shared scientific logic rather than duplicating it under experiment-specific folders.
10. Do not introduce abstraction layers without at least one real architectural purpose.
11. Prefer direct, readable call paths over patterns introduced only for design-pattern purity.
12. Do not create factories when normal typed construction is sufficient.
13. Do not create repository/service/manager classes unless they own real state or behavior that warrants the abstraction.
14. Do not keep aliases, redirects, compatibility wrappers, deprecated paths, or duplicate entry points without a demonstrated compatibility requirement.
15. Naming must describe scientific/technical meaning rather than arbitrary numbering.

---

## 6. Configuration Rules

### 6.1 YAML Policy

`config.yaml` is the only committed scientific configuration YAML/YML file.
`.semgrep.yml` is the sole permitted tooling-rule YAML file.

Therefore:

- no second experiment YAML;
- no dataset YAML;
- no test YAML;
- no duplicate local/default YAML;
- no YAML under `tests/`;
- no YAML under `docs/`;
- no CI YAML while this rule remains in force.

No other committed YAML/YML file is permitted without an explicit architecture decision.

### 6.2 Configuration Ownership

All configurable scientific/runtime values belong in `config.yaml`, including when applicable:

- paths;
- public-source identities, eligibility rules, and provenance controls;
- source-aware observation-window and source-group rules;
- feature parameters;
- split parameters;
- normalization parameters;
- model architecture;
- optimizer/training parameters;
- training seeds;
- FL parameters;
- experiment definitions;
- sample budgets;
- evaluation thresholds/procedures;
- statistical parameters;
- reporting parameters.

### 6.3 Configuration Access

1. Only `src/fediec/config.py` reads/parses `config.yaml`.
2. Pydantic v2 models validate all configuration.
3. The application uses one validated typed configuration object.
4. Source modules receive the configuration objects/sections they need.
5. No module re-opens the YAML independently.
6. No hidden environment-specific scientific constants.
7. No duplicated defaults in source code.
8. No duplicated values between CLI defaults and configuration unless the CLI option is intentionally overriding configuration.
9. An override must be explicit, visible, and recorded in artifact provenance.
10. Research parameters must not silently fall back after validation failure.
11. Unknown configuration keys should fail validation rather than be silently ignored when practical.

---

## 7. Constants and Magic Values

1. No scientific magic numbers in implementation code.
2. No repeated categorical magic strings.
3. Mathematical constants intrinsic to an algorithm may remain code constants when they are not configurable research choices.
4. Protocol choices belong in configuration or enums, not scattered literals.
5. Test values may use small explicit literals when they are clearly test fixtures rather than hidden production configuration.
6. Architecture tests must detect suspicious duplicated research constants.
7. Do not move every literal into config mechanically; centralize values that represent choices, protocol parameters, or repeated domain constants.

---

## 8. Enum Rules

`src/fediec/enums.py` is the central categorical vocabulary.

Use enums for stable closed categories such as:

- semantic action;
- dataset;
- split;
- topology;
- violation family;
- background activity stratum;
- training regime;
- experiment;
- run/artifact status;
- matching tier;
- eligibility/infeasibility category when closed and stable.

Rules:

1. Do not repeat domain categories as hardcoded strings.
2. Do not compare categorical state using raw string literals across module boundaries.
3. Do not create multiple enums for the same concept.
4. Do not scatter enum definitions across feature modules unless the enum is truly private to that module.
5. Avoid `.value` leakage throughout the codebase.
6. Serialization/deserialization boundaries may convert enum representations centrally.
7. Domain code should operate on enum members, not serialized strings.
8. CLI parsing should convert input to enums at the boundary.
9. Artifact IO should convert enums at the serialization boundary.
10. Architecture tests must detect categorical string drift where practical.

---

## 9. Type Rules

`src/fediec/types.py` owns reusable project-level validated types.

Rules:

1. Avoid `Any`.
2. Avoid `object` as application/domain IO.
3. Avoid raw `dict` as domain-level IO.
4. Avoid anonymous dictionary-shaped records between major layers.
5. Prefer typed dataclasses/Pydantic models/NamedTuples/value objects as appropriate.
6. Major module/service boundaries should not communicate using ambiguous primitive bundles.
7. IDs with distinct semantics should have distinct validated types where confusion would be dangerous.
8. Constrained numeric aliases belong in `types.py`, not scattered through modules.
9. Types such as `NonNegativeInt`, `PositiveInt`, `NonNegativeFloat`, `PositiveFloat`, `UnitInterval`, `OpenUnitInterval`, `FiniteFloat`, `SignedInt`, or equivalent project constrained aliases must not be redefined outside `types.py`.
10. Do not wrap values with pointless `float(...)`, `int(...)`, or `str(...)` calls merely to satisfy typing.
11. Fix type definitions and boundaries rather than masking them with casts.
12. Avoid broad `cast(...)` usage as a substitute for correct typing.
13. Do not use `.value` everywhere to escape enum typing.
14. Keep Polars/Pandas/raw-library types at data-processing boundaries; do not allow them to become the domain model by accident.
15. Pyright errors should be fixed at the source rather than suppressed without justification.
16. Type-ignore comments require a concrete documented technical reason.

---

## 10. Naming Rules

1. Use descriptive scientific names.
2. Do not use arbitrary labels such as `B1`, `B2`, `B3`, `Regime1`, `Exp1`, or similar identities.
3. Experiment identifiers exposed to CLI/config/artifacts use descriptive **kebab-case**.
4. Python modules/functions/classes use normal Python naming conventions.
5. Dataset package names use snake_case Python identifiers.
6. Raw dataset directories may preserve official/source dataset names.
7. Do not encode temporary dates or arbitrary version suffixes in stable module names.
8. Do not use names such as `new`, `old`, `final2`, `fixed`, `updated`, or `latest` for long-lived code paths.
9. Names must express purpose, not implementation history.

---

## 11. Dependency and Architecture Rules

The intended direction is approximately:

```text
cli
 ↓
workflows
 ↓
collection / preprocessing / counterfactuals / training / evaluation / statistics / reporting
 ↓
datasets / models / artifacts / config / enums / types
```

This is a conceptual direction, not permission for arbitrary cross-imports.

Rules:

1. `cli.py` is thin.
2. CLI commands delegate to workflows.
3. Workflows orchestrate; they do not become large scientific implementation modules.
4. Scientific modules own scientific logic.
5. Dataset modules must not import workflows.
6. Models must not import CLI/workflows.
7. Statistics must not depend on reporting presentation logic.
8. Reporting may consume finalized analysis/statistics artifacts but must not alter scientific results.
9. Tests may import production modules; production modules must never import tests.
10. Avoid circular dependencies.
11. Avoid dependency inversion that exists only to satisfy a pattern.
12. Shared enums are the lowest categorical layer; `types.py` may depend on
    them only to model canonical domain records. Both remain low-level and stable.
13. Architecture tests must enforce dependency directions.

---

## 12. CLI Rules

The preferred public CLI remains small and stable.

Primary commands:

```text
doctor
preprocess
prepare
plan
smoke
run <experiment>
status
report
```

Rules:

1. CLI commands must be idempotent where scientifically meaningful.
2. Re-running a completed command should reuse valid artifacts rather than silently recompute everything.
3. Destructive replacement requires an explicit option such as `--overwrite`.
4. `--overwrite` must not bypass scientific validation.
5. CLI code contains parsing and delegation, not implementation.
6. Each CLI command delegates to exactly one top-level workflow.
7. Workflows call typed domain/scientific functions.
8. Short diagnostic commands must stay short.
9. `plan` must not execute experiments.
10. `status` must inspect artifacts/configuration, not mutate them.
11. `doctor` must not alter the environment.
12. `smoke` uses tiny data/compute and never becomes confirmatory evidence.
13. Named experiments use descriptive identifiers.
14. CLI failures must return clear non-zero failures rather than silently continuing.
15. Command identity, resolved configuration, dataset identity, seed, and artifact reuse should be visible in logs.

---

## 13. Wiring Rules

Correct code that is not wired is incomplete.

For each public CLI command, the architecture must make it possible to trace:

```text
CLI
→ workflow
→ scientific/domain functions
→ leaf operations
```

Requirements:

1. Every public command must reach its intended workflow.
2. Every workflow must reach the intended implementation.
3. No workflow may stop at an obsolete wrapper.
4. Expected functions must be reachable from real entry points.
5. Library-only functions may remain intentionally unreachable from CLI only when their role is explicit.
6. Graphify must be run on the **current tree**, not reused from stale output.
7. For each CLI workflow, record/check:
   - reachable callable count;
   - reachable leaf callable count;
   - maximum call depth;
   - expected major modules reached.
8. Compare method/callable counts across refactors so large accidental drops are visible.
9. A refactor that suddenly removes a large reachable subtree requires investigation.
10. Tests must validate wiring as well as local function correctness.

---

## 14. Graphify Rules

Graphify is a required architecture-analysis tool.

Use it to inspect:

- CLI reachability;
- workflow reachability;
- call graph;
- orphan functions/classes;
- unexpectedly disconnected modules;
- CLI-to-leaf paths;
- method/callable counts;
- call depth;
- duplicate/parallel implementations;
- stale compatibility routes.

Rules:

1. Generate a fresh graph from the current checkout when performing architecture verification.
2. Do not trust an old Graphify export after source changes.
3. Do not commit large Graphify-generated reports by default.
4. Temporary Graphify artifacts belong in temporary runtime/test directories, not `docs/`.
5. Graphify is evidence for wiring/dead-code decisions, not an automatic deletion oracle.
6. Static reachability limitations must be considered for dynamic dispatch.
7. Verify suspicious Graphify findings with code search and tests before deletion.
8. `tests/architecture/test_wiring.py` owns automated Graphify wiring checks.
9. `tests/architecture/test_dead_code.py` may use Graphify evidence as one input to dead-code detection.

---

## 15. Static Analysis Rules

Required tooling:

- Ruff
- Pyright
- Semgrep
- Graphify
- architecture tests

### 15.1 Ruff

Ruff is responsible for fast Python linting and supported code-quality checks.

Rules:

1. Configure Ruff in `pyproject.toml`.
2. Fix violations instead of blanket suppression.
3. Do not add giant ignore lists to make CI/tests green.
4. File-specific ignores require a concrete reason.
5. Unused imports and obvious dead definitions should not remain.
6. Formatting/linting must not change scientific semantics.

### 15.2 Pyright

Pyright is the primary static type checker.

Rules:

1. Configure Pyright in `pyproject.toml`.
2. Keep code compatible with Pyright/Pylance.
3. Do not downgrade strictness merely to hide existing errors.
4. Fix root typing problems.
5. Avoid `# type: ignore` unless unavoidable and locally justified.
6. Architecture tests may invoke Pyright to guarantee the repository remains type-clean.

### 15.3 Semgrep

Semgrep is used for architecture/policy patterns not cleanly expressed by Ruff/Pyright.

Examples include:

- forbidden duplicate config access;
- forbidden enum `.value` leakage;
- forbidden raw dictionary domain IO;
- suspicious primitive wrappers/casts;
- forbidden feature-vector-only counterfactual splicing;
- suspicious test/calibration data passed into scaler fitting;
- forbidden post-hoc fallback/relaxation logic;
- suspicious hardcoded seed selection;
- forbidden direct test-result-driven model selection;
- forbidden duplicate legacy paths;
- forbidden claim/report-generation production code.

The committed `.semgrep.yml` is the canonical home for project Semgrep rules.

1. Keep it limited to static-analysis policy; it must not contain runtime or scientific configuration.
2. Built-in/registry Semgrep rules may be invoked directly where appropriate.
3. Architecture tests run Semgrep against the committed rule file.
4. Temporary Semgrep files must not be committed.
5. Semgrep failures must be fixed rather than globally suppressed without justification.

### 15.4 Required Fast Static Command Set

The exact command syntax may evolve with tool versions, but the architecture suite must effectively enforce:

```text
ruff check src tests
pyright src tests
semgrep <project rules>
pytest tests/architecture
```

---

## 16. Dead-Code, Removal, and Restoration Rules

Deletion requires evidence.

This rule exists because apparently unused code may actually be intended but not yet wired.

Before deleting code:

1. Check the roadmap.
2. Check this technical document.
3. Search call sites.
4. Inspect Graphify reachability.
5. Inspect CLI/workflow wiring.
6. Inspect configuration references.
7. Inspect tests.
8. Check whether the code is part of a planned but currently disconnected required workflow.
9. Prefer wiring/restoring required functionality before deleting it.
10. Confirm there is no dynamic registration/dispatch path that static tools missed.

Do not delete code merely because:

- one tool labels it unused;
- one test does not cover it;
- an import is currently absent;
- a refactor temporarily disconnected it.

Do delete code when evidence shows it is:

- obsolete;
- duplicated;
- superseded;
- a dead compatibility shim;
- an unused alias;
- a stale redirect;
- a wrapper with no independent responsibility;
- an abandoned implementation path;
- contrary to the roadmap.

After substantial deletions/refactors:

1. rerun Graphify;
2. rerun architecture tests;
3. rerun relevant unit tests;
4. rerun integration tests;
5. rerun E2E smoke;
6. compare reachable callable/leaf counts.

No deletion should silently remove scientific functionality.

---

## 17. No Compatibility-Shim Rule

Do not preserve bad architecture through compatibility layers unless there is an actual external compatibility requirement.

Avoid:

- renamed-function aliases kept indefinitely;
- duplicate import paths;
- redirect modules;
- deprecated wrappers;
- forwarding classes;
- old/new implementations side by side;
- version-suffixed implementations;
- stale adapters for code that no longer exists.

Prefer updating call sites and removing obsolete paths.

---

## 18. Dataset Rules

### 18.1 `data/` Is Raw Only

`data/` contains exactly:

```text
data/
└── raw/
```

Do not create:

- `data/processed/`
- `data/interim/`
- `data/cache/`
- `data/features/`
- `data/results/`

Derived material belongs in `outputs/`.

### 18.2 Raw Data

1. Raw data is immutable.
2. Do not rewrite source PCAP/CSV/metadata in place.
3. Do not silently rename source labels to make mapping easier.
4. Dataset-specific transformations belong in `src/fediec/datasets/...`.
5. Derived standardized representations belong in `outputs/processed/...`.
6. Keep external datasets logically separate.
7. Do not pool incompatible external datasets merely for better performance.
8. Do not select external devices/datasets based on observed model performance.
9. Do not infer intended action from target traffic when the scientific protocol requires independent intent provenance.
10. Restricted datasets are not redistributed merely for convenience.

### 18.3 Dataset Packages

Each dataset gets a dedicated package because its:

- raw schema;
- provenance;
- eligibility;
- action mapping;
- capture format;
- limitations

are dataset-specific.

Do not create a generic loader that hides these distinctions.

---

## 19. Scientific Protocol Invariants Enforced in Code/Tests

This document does not duplicate the full roadmap. The following are architecture-facing invariants that code/tests must protect.

### 19.1 Observation and Feature Semantics

1. Preserve the `(B, I, E)` contract semantics.
2. The main representation uses the locked pre-action and post-action network features defined by the roadmap.
3. Intent remains independently sourced.
4. Device identity, manufacturer identity, IP/MAC, or vendor identity must not become learned model features merely because they are available in metadata.
5. Metadata used for stratification/reporting must remain distinguishable from model inputs.
6. Do not change locked feature meaning after observing confirmatory results.

### 19.2 Splits and Leakage

1. Preserve chronological splitting.
2. Training/calibration/test partitions must not overlap.
3. Calibration/test observations must not affect training normalization.
4. Test observations must not drive model architecture/hyperparameter rescue.
5. Held-out zero-shot devices/manufacturers must not contribute forbidden normalization or calibration information.
6. Training-only quantities must remain training-only.
7. Architecture/protocol tests must explicitly guard these boundaries.

### 19.3 Normalization

1. The main scaler is derived only from eligible current training clients.
2. Federated sufficient statistics must not require raw pooling.
3. Local/centralized/federated comparisons use the protocol-defined comparable scaler.
4. A held-out device contributes no statistics to its zero-shot scaler.
5. Do not quietly switch normalization after seeing test results.

### 19.4 Model/Training Lock

1. The confirmatory model architecture is frozen before confirmatory evaluation.
2. No post-hoc architecture search on test performance.
3. No test-dependent early stopping/scheduler rescue.
4. Preserve all configured training seeds.
5. Do not select only successful seeds.
6. A failed seed is evidence about the configured procedure and must not disappear silently.
7. Smoke-test seeds/results are not confirmatory evidence.

### 19.5 Counterfactual Rules

1. No feature-vector-only splicing.
2. Counterfactual transformations must remain reproducible from raw held-out capture material and manifests.
3. No counterfactual is generated from training observations.
4. Calibration observations must not become anomaly samples.
5. Calipers/matching criteria are derived/frozen from allowed training information.
6. Do not relax matching because a convenient donor is unavailable.
7. Preserve the frozen matching hierarchy.
8. Transition semantics must be compatible.
9. B→E boundary continuity must be checked.
10. Internal timing/packet order must be preserved as required.
11. Do not repair impossible timestamp collisions with arbitrary epsilon jitter.
12. EXCESS composition must respect physical/raw-timeline feasibility.
13. Donor reuse must be tracked.
14. Generated observations sharing clean sources must preserve source-dependency metadata.
15. Failure/ineligibility gets a frozen reason rather than silent replacement with a looser rule.

### 19.6 Artifact-Control Procedures

The roadmap-required replacement/translation and EXCESS-composition controls remain mandatory.

They live under:

```text
src/fediec/counterfactuals/artifact_control.py
tests/unit/test_counterfactuals.py
tests/protocol/test_counterfactual_rules.py
```

They do **not** justify introducing a top-level `audit/` framework.

Security interpretation must not proceed as if a transformation were valid when its required artifact-control condition fails.

### 19.7 Public-Source Violation Boundaries

1. Generated counterfactuals are distinct from observed public-source events.
2. Preserve source, device, capture, and provenance identity.
3. Do not relabel counterfactuals as real attacks or observed failures.
4. Do not induce new failures or acquire new traffic.

### 19.8 External/Real-Attack Validation

1. PingPong is the first candidate for a public-source main study.
2. TU Wien Philips Hue is mechanism replication according to the roadmap, not proof of multi-device federation by itself.
3. CIC IoT 2022 or another real-attack dataset is used only when intent/device/time/attack/execution alignment requirements are satisfied.
4. If required real-attack alignment is absent, no code path may manufacture it.
5. Results remain distinguishable by source collection; incompatible sources are not pooled.

### 19.9 Statistical Units

1. Training seeds are repeated computational runs, not independent physical devices.
2. Generated observations sharing source material are not independent merely because multiple rows exist.
3. Preserve device → session → interaction/source-dependency structure where required.
4. Use dependency-aware hierarchical resampling/statistics.
5. Do not inflate sample size through donor reuse or generated derivatives.
6. Preserve per-device effects, not only pooled headline metrics.
7. Multiplicity handling must match the locked statistical protocol.

---

## 20. Testing Rules

### 20.1 Test Layers

Use five explicit layers:

```text
unit
integration
protocol
architecture
e2e
```

Each has a different purpose.

### 20.2 Unit Tests

Unit tests verify local correctness:

- deterministic transforms;
- enum/type validation;
- dataset parsing;
- feature extraction;
- matching;
- metrics;
- model construction;
- numerical behavior.

They should not simulate whole workflows unnecessarily.

### 20.3 Integration Tests

Integration tests verify module boundaries:

- raw → features;
- features → training;
- counterfactual generation;
- FL orchestration;
- transfer paths;
- statistical pipeline.

### 20.4 Protocol Tests

Protocol tests verify scientific validity.

A mathematically correct experiment can still be scientifically invalid. Protocol tests therefore enforce:

- chronology;
- leakage prevention;
- training-only normalization;
- zero-shot restrictions;
- counterfactual matching hierarchy;
- transition/boundary/timeline feasibility;
- source dependency;
- no calibration anomaly construction;
- no post-hoc fallback.

### 20.5 Architecture Tests

Architecture tests verify repository correctness:

- static analysis;
- CLI wiring;
- Graphify reachability;
- dead code;
- module dependency direction;
- YAML policy;
- central config access;
- enum policy;
- type/primitive boundary policy;
- forbidden generic modules;
- stale shims/aliases;
- TODO/unfinished-code drift;
- forbidden report/claim infrastructure.

### 20.6 End-to-End Tests

E2E tests verify actual user-facing CLI paths on tiny fixtures.

They must not run confirmatory-scale experiments.

### 20.7 Test Integrity

Never:

- skip a failing test to get green;
- disable a failing test without fixing/removing the obsolete requirement;
- add `xfail` merely to postpone a real regression;
- weaken assertions because implementation fails;
- mock away the behavior the test is supposed to verify;
- rewrite tests to mirror a bug.

When a test is obsolete because the roadmap/architecture intentionally changed, update or remove it explicitly and explain the architectural reason in the commit/change.

### 20.8 Runtime Budget

The normal development test suite should remain practical and target **≤ 5 minutes** on the normal development machine.

Therefore:

- tests use tiny fixtures;
- no real full training in unit/integration tests;
- no large public-dataset download in tests;
- no dependence on external internet in the normal suite;
- expensive experiments are not tests;
- use `pytest-xdist` where safe;
- use Hypothesis where it improves invariant coverage without exploding runtime.

---

## 21. Architecture-Test Responsibilities

### `test_static_analysis.py`

Must invoke/enforce:

- Ruff;
- Pyright;
- Semgrep;
- required source/test scope.

### `test_wiring.py`

Must use fresh Graphify information to verify:

- CLI commands;
- workflow mapping;
- major downstream modules;
- reachable callables;
- reachable leaves;
- maximum call depth;
- unexpected disconnections.

### `test_dead_code.py`

Must detect or flag:

- unreachable source;
- orphan modules;
- dead wrappers;
- stale compatibility code;
- duplicate implementation paths;
- abandoned aliases;
- old experiment plumbing.

It must not auto-delete.

### `test_dependencies.py`

Must enforce architectural import direction and absence of prohibited cycles.

### `test_config_and_constants.py`

Must verify:

- only `config.yaml` and `.semgrep.yml` are committed YAML/YML files;
- only `config.py` parses it;
- no duplicated research parameters;
- no hidden experiment seed lists;
- no second config source.

### `test_enums_and_types.py`

Must verify:

- enum use for closed project categories;
- constrained project types live in `types.py`;
- no domain `Any`/`object`/raw-dict leakage where prohibited;
- no widespread `.value` escape pattern;
- no pointless primitive conversion wrappers used to mask typing problems.

### `test_hygiene.py`

Must flag:

- TODO/FIXME placeholders that represent unfinished required work;
- generic dumping-ground modules;
- dead compatibility shims;
- generated source committed accidentally;
- duplicated implementation;
- obvious wrapper-only abstractions;
- claim/report/dependency-analysis infrastructure reintroduced into production source contrary to this document.

---

## 22. Code-Quality Rules

1. Use clear, boring, explicit Python.
2. Prefer existing well-maintained libraries over custom reimplementation.
3. Do not duplicate library functionality without a scientific/technical reason.
4. Prefer vectorized Polars/NumPy/PyTorch operations over slow Python loops where meaningful.
5. Avoid premature optimization that obscures correctness.
6. Avoid clever metaprogramming for normal research workflows.
7. Keep functions focused.
8. Keep side effects explicit.
9. Keep filesystem IO at clear boundaries.
10. Do not hide expensive operations inside properties or constructors.
11. Determinism must be explicit where required.
12. Randomness requires a controlled seed source.
13. No silent exception swallowing.
14. Broad `except Exception` requires a real boundary-level reason and must preserve useful error information.
15. Do not catch failures simply to continue with invalid scientific state.
16. Validate assumptions early at boundaries.
17. Do not silently coerce malformed research data into validity.
18. Invalid/ineligible observations receive explicit reasons when the roadmap requires them.

---

## 23. Comments and Docstrings

1. Do not add comments that merely narrate obvious code.
2. Do not add verbose generic docstrings to every function.
3. Comments/docstrings should explain:
   - scientific invariants;
   - non-obvious constraints;
   - why a seemingly simpler implementation is invalid;
   - external-format assumptions;
   - security/leakage-sensitive behavior.
4. Avoid AI-style explanatory filler.
5. Do not mention an AI assistant/agent in code comments or docstrings.
6. Do not generate large blocks of documentation that simply restate function names.
7. Documentation should read as project-authored technical writing.

---

## 24. Logging Rules

Use structured, concise logging, preferably through `structlog`.

Useful run-level fields include:

- command;
- experiment;
- configuration identity/hash;
- dataset;
- device/fold where relevant;
- seed;
- stage;
- progress;
- observation counts;
- feature dimensions;
- artifact reuse/cache status;
- important thresholds/calipers;
- eligibility/abstention/infeasibility counts;
- warnings;
- timing;
- final status;
- errors.

Rules:

1. Do not log every packet/row/observation.
2. Do not duplicate the same event in multiple logging systems.
3. Do not produce giant text logs.
4. Logs are operational diagnostics, not primary result evidence.
5. Logs stay in `outputs/` or runtime console, never `results/`.
6. Sensitive raw content must not be dumped into logs.

---

## 25. Serialization and Artifact Formats

Preferred formats:

- Parquet for tabular data;
- JSON for small manifests/metadata/summaries;
- SafeTensors for PyTorch model weights;
- PCAP/PCAPNG only as raw source capture material;
- standard image/vector formats for figures.

Rules:

1. Prefer Parquet over repeated CSV copies for internal tabular artifacts.
2. Do not use pickle for durable scientific artifacts.
3. Avoid opaque Python-specific serialization.
4. Every important durable artifact must be reproducible from raw data + config + code.
5. Durable artifacts should include or reference provenance metadata.
6. Artifact formats must remain readable without importing the entire training runtime.
7. Do not persist tensors/embeddings/intermediate arrays that can cheaply be recomputed unless there is a demonstrated runtime need.

---

## 26. Artifact Provenance

Important generated artifacts should record enough metadata to identify:

- experiment;
- dataset;
- dataset/source checksum or frozen source identity where feasible;
- split/fold;
- seed;
- resolved configuration hash;
- Git commit;
- model/regime;
- timestamp;
- parent/source artifact identities where relevant;
- software/environment identity when needed for reproducibility.

Generated counterfactuals additionally preserve the roadmap-required source/donor/dependency provenance.

Do not rely on filenames alone as provenance.

---

## 27. `outputs/` Rules

`outputs/` is a **reproducible workspace**, not a second raw-data store and not a manuscript archive.

### Allowed

- compact processed features;
- interaction tables;
- split manifests;
- scaler statistics;
- compact counterfactual descriptors/derived tables;
- provenance manifests;
- final run checkpoint when useful;
- predictions required for statistics;
- compact metric summaries;
- derived analyses;
- candidate figures/tables.

### Forbidden by Default

- copied raw PCAPs;
- duplicate raw datasets;
- every training checkpoint;
- per-batch tensor dumps;
- per-epoch prediction dumps without need;
- giant debug traces;
- redundant CSV + Parquet + JSON copies of the same table;
- bootstrap replicate dumps when only summaries are needed;
- caches that cannot be safely regenerated;
- repeated copies of identical artifacts under multiple experiment folders.

### Size Discipline

1. Raw source files stay in `data/raw/`.
2. Use compressed Parquet.
3. Store only row-level predictions needed for downstream statistics.
4. Keep only the final/reusable model checkpoint unless a scientific experiment explicitly studies training trajectory.
5. Do not persist optimizer states after a completed run unless required for intentional resume.
6. Do not save every FL round model.
7. Aggregate training history rather than storing enormous repeated state.
8. Generated intermediate artifacts should be deletable and reproducible.
9. Prefer manifests referencing source artifacts over physical duplication.
10. Output reuse should be checksum/config aware.

---

## 28. `results/` Rules

`results/` contains **small, final, manuscript/chapter evidence**.

It is not:

- a cache;
- a log store;
- a checkpoint store;
- raw data;
- a copy of all outputs;
- an experiment scratch directory;
- a claim registry.

Rules:

1. Results are promoted from reproducible `outputs/`.
2. Never hand-edit numerical result artifacts.
3. Final results retain provenance back to source outputs.
4. No raw PCAPs.
5. No ordinary model checkpoints.
6. No debug logs.
7. No smoke-test outputs.
8. No temporary bootstrap/permutation replicates unless the final analysis explicitly requires preserving them.
9. Preserve negative/inconclusive evidence rather than selecting only favorable runs.
10. Preserve failed/invalid run status where scientifically relevant.
11. Results must keep evidence distinguishable by public source.
12. Tables/figures in `results/` are the versions intended for the chapter/manuscript.
13. Promotion must never invent prose claims.
14. There is no `claim-gates/` folder.

---

## 29. Reporting Rules

1. Reporting code produces tables, figures, and compact structured summaries.
2. Production code must **not generate Markdown reports**.
3. Do not generate `report.md`, `claims.md`, audit markdown, or similar artifacts from code.
4. Human-authored documentation remains in `docs/`.
5. Reporting must not recompute or silently alter scientific data.
6. Tables/figures consume finalized structured artifacts.
7. Figure/table generation must be deterministic from finalized evidence where practical.
8. Do not place manuscript prose generation in the codebase.

---

## 30. Claims Rules

There is no production `claims/` package.

There is no:

- claim registry;
- executable prose claim engine;
- claim markdown generator;
- claim-gate artifact folder;
- claim-specific source hierarchy.

Scientific conclusions are written from the evidence and roadmap by the researcher.

Code/tests may enforce objective protocol conditions, eligibility, leakage rules, and statistical procedures, but they must not become a prose-claim management system.

---

## 31. No Top-Level Audit Framework

There is no top-level `audit/` source package and no `outputs/audits/` / `results/audits/` hierarchy.

This does **not** remove validation.

Validation belongs where the responsibility lives:

- dataset eligibility → dataset module;
- counterfactual artifact control → counterfactual module;
- leakage → protocol tests/preprocessing;
- wiring → architecture tests;
- type/config hygiene → architecture tests;
- statistical-unit correctness → statistics + protocol tests.

The word *audit* may still appear where it is the scientific term used by the roadmap, but it does not justify an architecture of generic audit infrastructure.

---

## 32. No Docker Rule

Do not add:

- `Dockerfile`;
- `docker-compose.yml`;
- Docker-based test requirements;
- Docker-only reproducibility instructions.

The normal development/runtime path is native Python/WSL/environment tooling.

Containerization may be reconsidered only if explicitly requested later.

---

## 33. Experiment Rules

1. Experiments are primarily declarative through `config.yaml`.
2. Do not create one package/module tree per experiment.
3. Reuse shared training/evaluation/statistics logic.
4. A genuinely new scientific algorithm may receive a new source module.
5. A new combination of existing algorithms/configuration does not justify new implementation duplication.
6. Experiment names use descriptive kebab-case.
7. Seeds are configuration, not manually chosen per run.
8. Do not select successful seeds.
9. Do not alter experiment configuration after seeing confirmatory results unless the roadmap explicitly permits a documented new exploratory analysis.
10. Exploratory and confirmatory artifacts must remain distinguishable.
11. Smoke tests are never promoted to confirmatory results.

---

## 34. Reproducibility Rules

1. Same raw inputs + same code + same config + same seed should reproduce the same deterministic stages within practical framework limits.
2. Source identities, frozen manifests, and split assignments must be preserved.
3. Split assignments must be materialized and reproducible.
4. Counterfactual donor assignment must be reproducible.
5. Training seeds must be recorded.
6. FL configuration must be recorded.
7. Data-scarcity sampling must be reproducible.
8. Holdout manifests must be reproducible.
9. Intent-provenance perturbations must be reproducible.
10. Figures/tables must trace back to structured result artifacts.
11. Do not depend on undocumented notebook state.
12. Notebooks should not become the authoritative implementation path.

---

## 35. Performance and Long-Running Work Rules

1. Do not block development by staring at long-running preprocessing commands.
2. When working interactively and safe to do so, launch long deterministic preprocessing/background tasks non-blocking and continue other independent verification work.
3. Return to the task when its artifacts are ready.
4. Do not repeatedly poll expensive commands without purpose.
5. Short commands such as `doctor`, `plan`, `status`, architecture checks, and targeted tests should remain fast.
6. Avoid recomputation when valid provenance-matched outputs already exist.
7. Expensive work must not be hidden inside imports or test collection.

---

## 36. Tooling and Preferred Libraries

Use established libraries where they fit the responsibility.

Preferred stack includes:

- Pydantic v2 — typed configuration/domain validation;
- Polars — tabular processing;
- Parquet — durable compact tabular artifacts;
- Pandera — dataframe/schema validation when useful;
- DuckDB — analytical querying when useful;
- PyTorch — neural modeling;
- Flower — federated orchestration;
- scikit-learn — conventional metrics/baselines/transforms where appropriate;
- SafeTensors — model weights;
- Typer — CLI;
- Rich — concise CLI presentation;
- structlog — structured logging;
- pytest — tests;
- Hypothesis — property/invariant testing where useful;
- pytest-xdist — parallel testing where safe;
- Ruff — lint/static quality;
- Pyright — typing;
- Semgrep — project policy/architecture patterns;
- Graphify — call-graph/reachability analysis.

A preferred library is not an excuse to add it when standard-library code is simpler and sufficient.

---

## 37. Git and Change Discipline

1. Use Git throughout implementation.
2. Prefer multiple coherent commits over one enormous mixed commit.
3. Commits should separate logically distinct changes where practical.
4. Do not add an AI/agent as author or co-author.
5. Do not add AI-generated co-author trailers.
6. Do not rewrite scientific history by deleting evidence of legitimate failed experiments.
7. Do not commit raw secrets, API keys, credentials, or machine-specific private configuration.
8. Do not commit generated caches.
9. Do not commit temporary Graphify/Semgrep files.
10. Do not commit large raw datasets unless repository policy explicitly allows them.
11. Do not perform unrelated cleanup in the same change merely because a file was opened.
12. Stay within requested scope.

---

## 38. Agent/Automation Change Rules

When an automated coding agent is used:

1. Read `docs/FedIEC_Roadmap.md` and `docs/technical_doc.md` before architectural changes.
2. Do not invent new architecture.
3. Do not create new folders “for cleanliness” without need.
4. Do not introduce claims infrastructure.
5. Do not introduce audit infrastructure.
6. Do not introduce extra YAML.
7. Do not introduce Docker.
8. Do not remove required code solely because it is currently unwired.
9. Restore/wire required functionality before deletion when evidence shows it belongs.
10. Validate wiring with Graphify and tests.
11. Fix partial/missing/broken implementation rather than merely documenting the gap.
12. Do not weaken tests to match implementation.
13. Do not silently change roadmap semantics.
14. If a scientific requirement is ambiguous, do not manufacture a new rule.
15. Keep changes focused.
16. Avoid spawning many independent implementations of the same problem.
17. Do not add AI attribution to code, docs, commits, or authorship.

---

## 39. Forbidden Patterns Summary

The following are repository smells and should fail review or architecture checks where practical:

```text
second *.yaml / *.yml file
generic utils.py / helpers.py / common.py / misc.py dumping ground
top-level claims/
claim_registry
claim-gates/
top-level audit/
outputs/audits/
results/audits/
Dockerfile / docker-compose
production Markdown report generator
hardcoded experiment strings scattered through code
hardcoded research constants outside config
domain IO as raw dict
Any/object used to avoid proper typing
repeated .value enum escape
pointless int()/float()/str() typing wrappers
broad casts masking bad types
duplicate old/new implementations
compatibility shims without actual compatibility need
dead aliases/redirect modules
wrapper-only classes/modules
unwired required functionality
deleting code only because one static tool says unused
feature-vector-only counterfactual splice
test/calibration leakage into training/scaling
zero-shot target statistics used during training/scaling
post-hoc matching relaxation
epsilon-jitter repair of infeasible counterfactual timestamps
selecting successful seeds only
performance-based external-device selection
raw PCAP duplication into outputs
per-epoch/per-round checkpoint explosions
logs in results/
smoke outputs in results/
hand-edited numerical results
AI-style filler comments/docstrings
AI/agent co-authorship
```

---

## 40. Definition of Done for a Code Change

A change is not complete merely because the edited unit test passes.

As applicable, completion requires:

1. implementation matches the roadmap;
2. implementation matches this technical document;
3. configuration remains centralized;
4. enums/types remain clean;
5. relevant unit tests pass;
6. relevant integration tests pass;
7. relevant protocol tests pass;
8. architecture tests pass;
9. Ruff passes;
10. Pyright passes;
11. Semgrep passes;
12. Graphify wiring is still correct after structural changes;
13. no required reachable subtree disappeared unexpectedly;
14. E2E smoke passes for workflow-impacting changes;
15. outputs remain compact;
16. provenance is preserved;
17. no new dead/duplicate/shim code remains;
18. docs are updated when architecture intentionally changed.

For large cleanup/refactoring work, use the sequence:

```text
understand roadmap + technical rules
→ inspect current wiring
→ restore/wire required functionality
→ remove proven dead/duplicate code
→ run Graphify
→ run targeted tests
→ run architecture/static checks
→ run integration/protocol tests
→ run E2E smoke
→ run full practical test suite
→ inspect final tree and artifact sizes
```

---

## 41. Repository Philosophy

FedIEC should remain:

```text
scientifically strict
+
architecturally simple
+
strongly typed
+
explicitly wired
+
compact on disk
+
reproducible
+
easy to audit through tests and tooling
```

The goal is **not** to maximize the number of modules, abstractions, tests, artifacts, or framework layers.

The goal is to make it difficult to:

- accidentally violate the scientific protocol;
- hide leakage;
- lose required functionality during refactoring;
- duplicate configuration;
- create type ambiguity;
- generate unreproducible evidence;
- bloat the repository;
- confuse workspace outputs with final evidence.

When there is a choice between clever architecture and a direct implementation that is easier to verify scientifically, prefer the direct implementation.
