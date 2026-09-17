# Master Checklist — Public-Source Foundation

- [x] Scientific and technical sources of truth reconciled to the
  public-dataset-only roadmap.
- [x] Shared raw-data pool scoped without altering out-of-scope bytes.
- [x] PingPong, CIC IoT 2022, and TU Wien Philips Hue availability and
  source-specific action mappings audited.
- [x] Physical-acquisition scaffold removed from configuration, CLI,
  workflows, adapters, enums, paths, and documentation.
- [x] Dataset role, eligibility, provenance, replay/late subtype, and
  source-group matching enums centralized.
- [x] `doctor` remains read-only and audits public-source readiness only.
- [x] Configuration remains one YAML parsed only by `config.py`.
- [x] Architecture test suite, Ruff, and Pyright pass after the migration.
- [x] Fresh Graphify AST extraction completed; generated output is ignored.
- [ ] Freeze checksums/source manifests and complete eligibility gates before
  confirmatory preprocessing.
- [ ] Implement derived-corpus construction without fabricating unavailable
  intent, state, transition, or NO_ACTION metadata.

No confirmatory experiment has been run in this phase.
