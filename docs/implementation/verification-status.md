# Verification Status

Last run: 2026-09-17, this session.

| Check | Command | Result |
| --- | --- | --- |
| Ruff | `uv run ruff check src tests` | **PASS** — all checks passed |
| Pyright | `uv run pyright src tests` | **PASS** — 0 errors, 0 warnings |
| Semgrep | 4 custom rules (`.value` boundary, raw-dict IO, duplicate YAML parsing, broad `cast`), materialized at test-time, no committed `.semgrep.yml` | **PASS** — 0 findings against real `src/` |
| Pytest | `uv run pytest tests -q` | **PASS** — 9 passed (architecture layer, including the Ruff/Pyright/Semgrep subprocess checks themselves) |
| Graphify | AST-only pass on `src/fediec` (pure code, no semantic subagents needed) | **PASS** — 140 nodes, 396 edges, 18 communities, 0 import cycles |
| CLI smoke (`fediec doctor`, `fediec plan`) | manual | **PASS** — both run end-to-end against real config + real dataset paths |
| TU Wien Philips Hue adapter | `enumerate_raw_interactions()` | **PASS** — 10000/10000 real files, 5000/5000 ON/OFF |
| CIC IoT 2022 adapter | `enumerate_raw_interactions()` | **PASS** — 264 real interactions, 132/132 ON/OFF, only companion-app-triggered folders |
| PingPong adapter | `enumerate_raw_interactions()` | **PASS** — 2000 real interactions across 20 device/context units, exactly 1000/1000 ON/OFF (local-phone/same-vendor only) |

## Not yet run / not applicable at this phase

- `tests/unit`, `tests/integration`, `tests/protocol`, `tests/e2e`: empty
  (only fixture directories exist). This phase built the architecture
  foundation (config/enums/types/paths/CLI/doctor); the other four test
  layers land alongside the preprocessing/counterfactual/training/
  evaluation modules they're meant to verify, which are Prompt 2+ scope.
- `tests/architecture/test_wiring.py`, `test_dead_code.py`,
  `test_dependencies.py`, `test_hygiene.py`: not yet written.
  `test_enums_and_types.py`, `test_config_and_constants.py` and
  `test_static_analysis.py` exist and pass.

The ≤5-minute test-suite budget (technical_doc.md Sec. 20.8) is trivially
met right now (0.2s) — this will need active attention once real fixtures
and heavier layers land.
