# Master Checklist — Prompt 1 (Data-Ground-Truth Audit, Enums/Types Foundation, Traceability, Repository Bootstrap)

```text
[x] complete source-of-truth read (CLAUDE.md, roadmap, technical_doc)
[x] real data/raw recursively inventoried (PingPong, TU Wien Philips Hue, cic-iot-2022)
[x] schemas/dtypes/value domains inspected — TU Wien, PingPong (local-phone/same-vendor), CIC IoT 2022 complete
[~] PCAP characteristics inspected where applicable — filenames/dirs yes; CIC's global+first-record header read for timestamps, no full packet-level parse
[x] dataset schema drift checked (TU Wien armstate_labeled.csv stray file found)
[~] missing datasets resolved as far as required/possible — PingPong remote-phone/ifttt/public-dataset intent-provenance still open, documented not guessed
[x] FedIEC-Contracts creation path complete if raw benchmark not yet collected — directory contract frozen in paths.py/RepositoryPathKey, doctor checks it
[x] dataset-inventory current
[x] dataset-schema-map current
[x] enums centralized (src/fediec/enums.py)
[x] path enum exists (RepositoryPathKey) + resolver (paths.py)
[x] types/aliases centralized (src/fediec/types.py)
[x] primitive signature ban passes (test_enums_and_types.py)
[x] no Any/object/raw dict domain IO
[x] no unnecessary .value (grep-verified during this session)
[x] no unnecessary float/int/str wrappers (grep-verified)
[x] no broad casts
[x] constants centralized (no scientific magic numbers introduced — config.yaml carries all locked roadmap numeric parameters)
[x] path handling centralized (paths.py sole owner)
[x] no hardcoded repository path strings outside paths.py/enums.py
[x] config centralized (config.py, one FediecConfig object, load_config() called internally — never injected as a parameter, test_config_and_constants.py enforces this)
[x] one YAML/YML only (config.yaml; test_config_and_constants.py enforces)
[~] dataset adapters match real schemas — TU Wien Philips Hue, CIC IoT 2022 and PingPong (local-phone/same-vendor): full adapters, verified against real files (10000/10000, 264, and 2000 interactions respectively). PingPong remote-phone/ifttt/public-dataset not yet covered (open intent-provenance question). FedIEC-Contracts: directory-contract scaffold only (no data to adapt yet)
[x] doctor checks dataset/schema readiness (real, read-only, verified against actual disk state)
[x] CLI/workflows wired (all 9 commands; unimplemented ones raise explicit NotImplementedError naming the missing module, never fake success)
[~] five test layers present — architecture layer only; unit/integration/protocol/e2e are Prompt 2+ scope (nothing to test yet beyond what architecture tests already cover)
[ ] schema drift tests present — not yet (needs frozen fixtures from the now-working adapters)
[x] architecture rule tests present (test_enums_and_types.py, test_config_and_constants.py, test_static_analysis.py)
[x] fresh Graphify clean (140 nodes, 396 edges, 0 cycles)
[x] duplication audit clean (no duplicate enums/types/constants found)
[x] Ruff clean
[x] Pyright clean
[x] Semgrep clean (4 custom rules, materialized at test-time, 0 findings)
[x] tests clean (9/9 passing)
[x] .gitignore audited/updated (tool caches, graphify-out/, outputs/ workspace)
[x] Git diff/status clean and intentional (see commits)
[x] docs/implementation matches reality
[x] three audit passes completed (source/architecture, tool/test, final re-audit) — see below
```

## Audit Pass Log

**Pass A (source/architecture):** grepped for `.value`, casts, magic
numbers, hardcoded paths, duplicate enums/types across `src/fediec` after
each module was written; found and fixed primitive leaks in
`artifacts.py`/`paths.py`/`workflows/*.py` before they landed.

**Pass B (tool/test):** ran `ruff check`, `pyright`, `pytest
tests/architecture`, and a manual CLI smoke (`fediec doctor`, `fediec
plan`) after every structural change; fixed every failure before moving
on (duplicate enum members, a B008 Typer lint, a Pandera-adjacent Pyright
strict-mode generic-inference gap).

**Pass C (final re-audit):** re-ran the full command set
(`ruff`/`pyright`/`pytest`) one more time after the last edit in this
session — all clean (see `verification-status.md`) — and re-ran Graphify
fresh from the final tree.

## Explicitly deferred to later prompts (not silently skipped)

- Android intent-logging harness, gateway capture pipeline, FedIEC-Contracts
  collection (`workflows/collect.py`).
- Feature extraction, splitting, normalization (`workflows/preprocess.py`).
- Counterfactual matching/generation (`workflows/prepare.py`).
- Model, training, federated, evaluation, statistics, reporting modules
  and their corresponding CLI workflows (`run`, `smoke`, `report`).
- PingPong `remote-phone/`, `ifttt/`, `public-dataset/` intent-provenance
  verification and adapter extension (polarity convention itself is
  resolved — Roadmap Sec. 28.1 — only the companion-app provenance chain
  for these three subtrees remains open).
- `test_wiring.py`, `test_dead_code.py`, `test_dependencies.py`,
  `test_hygiene.py`.
- unit/integration/protocol/e2e test layers.
