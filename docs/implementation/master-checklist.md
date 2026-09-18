# Master Checklist — Public-Source Foundation

- [x] Scientific and technical sources of truth reconciled to the
  public-dataset-only roadmap.
- [x] Shared raw-data pool scoped without altering out-of-scope bytes.
- [x] PingPong, CIC IoT 2022, TU Wien Philips Hue, and Mon(IoT)r IMC 2019 availability and
  source-specific action mappings audited.
- [x] Physical-acquisition scaffold removed from configuration, CLI,
  workflows, adapters, enums, paths, and documentation.
- [x] Dataset role, eligibility, provenance, replay/late subtype, and
  source-group matching enums centralized.
- [x] `doctor` remains read-only and audits public-source readiness only.
- [x] Only `config.yaml` provides runtime/scientific configuration; committed
  `.semgrep.yml` is limited to static-analysis rules.
- [x] Architecture test suite, Ruff, and Pyright pass after the migration.
- [x] Unit, integration, protocol, architecture, and E2E test layers exercise
  the current public-source foundation.
- [x] Fresh Graphify AST extraction completed; generated output is ignored.
- [x] Replace stale fixed split counts with deterministic source-aware
  approximately 60/20/20 clean-split manifests.
- [x] Freeze selected-input source identities and aggregate checksums before
  confirmatory preprocessing.
- [x] Complete eligibility gates before confirmatory preprocessing; Mon(IoT)r is
  `FULL_CONTRACT_ELIGIBLE` for the active capture-level tier only.
- [x] Implement the active capture-level derived representation without
  fabricating unavailable intent, state, transition, trigger, B/E, or NO_ACTION metadata.
- [x] Add the pre-model representation-confound gate and frozen 19-D/3-D model
  interface; model execution remains disabled pending primary-role approval.
- [x] Mark B-context and NO_ACTION-dependent analyses unavailable where no
  source-backed procedure exists; do not fabricate missing intervals.
- [x] Audit source order and mark pre-context comparisons unavailable or
  descriptive where alternation/boundary provenance confounds interpretation.
- [x] Freeze the per-family counterfactual source-feasibility matrix and
  artifact-control pass rules; no source-infeasible family is generated.
- [x] Build the `counterfactuals/` (matching, validity, artifact_control,
  generation), `statistics/` (resampling, comparison), and `reporting/`
  (tables, figures, promotion) packages required by the locked repository
  structure; `generation.py` fails closed for every currently frozen family.
- [x] Build `evaluation/heterogeneity.py`, `evaluation/transfer.py`,
  `evaluation/robustness.py`, and `evaluation/security.py`.
- [x] Wire `smoke` to exercise heterogeneity distances (device, action, and
  protocol-identity-feature subsets), the missing/duplicate-intent robustness
  diagnostics, the security-evaluation suite, and the counterfactual-gating
  fail-closed path, all on real derived Mon(IoT)r rows.
- [x] Wire `report` to inspect `outputs/runs/` for confirmatory prediction
  artifacts and report their absence structurally instead of raising
  `NotImplementedError`.
- [x] Add unit tests for `statistics.comparison` (Holm correction, paired
  effect estimate), `evaluation.heterogeneity`, and the `counterfactuals`
  package (matching, validity, artifact-control pass/fail, generation gating).

No confirmatory experiment has been run in this phase. The counterfactual
generation/artifact-control smoke requirement remains correctly blocked by
public source feasibility (every family is `SOURCE_INFEASIBLE` or
`REPRESENTATION_UNOBSERVABLE` in the frozen primary manifest); smoke proves
the fail-closed gate instead of fabricating a family.

- [x] Counterfactual/NO_ACTION feasibility search closed for this phase: the
  original 4 datasets, their official upstream repos/papers, and 2
  additional independent candidates (UNSW-IoTraffic 2025, Sivanathan 2020)
  all checked; none supports a source-feasible family. See decisions 11-12.
- [x] Comparison 1's primary outcome amended to the Sec. 55 Direct Contract
  Metric (genuine-data-only, no counterfactuals) for the current tier;
  Comparison 3 unaffected; the artifact-controlled violation-detection claim
  (Sections 80-81) and Contribution D remain unavailable this round.

Prompt 4 is unblocked on this evidence: the confirmatory hypothesis family
for this round is Comparison 1 (intent value, via Sec. 55) and Comparison 3
(federated collaboration), Holm-corrected across those two.
