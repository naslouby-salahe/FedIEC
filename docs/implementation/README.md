# Implementation Tracking

Human-authored tracking docs for FedIEC implementation progress, kept
synchronized with the real repository state. These are not a second
architecture spec — `docs/technical_doc.md` remains authoritative for
structure/rules, `docs/FedIEC_Roadmap.md` for science.

- `master-checklist.md` — phase-by-phase completion checklist.
- `requirements-traceability.md` — roadmap/technical requirement -> implementation mapping.
- `decisions-and-blockers.md` — open questions, blockers, decisions made during implementation.
- `dataset-inventory.md` — what physically exists under `data/raw/`.
- `dataset-schema-map.md` — raw field -> canonical type/enum mapping per dataset.
- `source-identity-manifest.md` — frozen selected-input source identities and drift digests.
- `wiring-map.md` — CLI -> workflow -> leaf reachability (Graphify-backed).
- `verification-status.md` — latest Ruff/Pyright/Semgrep/test/Graphify results.
