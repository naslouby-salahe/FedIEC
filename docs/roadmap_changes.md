# Roadmap Changes

Records the reasoning behind surgical updates to `docs/FedIEC_Roadmap.md`,
per `CLAUDE.md`'s scientific-methodology change protocol. This file
explains *why*; the roadmap itself stays clean and current, not a
changelog.

## 2026-09-17 — External-dataset acquisition constraints grounded in the roadmap (Sec. 28, 29, 33)

**Why:** Direct inspection of the actually-acquired raw data (via the
`data/raw` symlink into the shared data pool) surfaced three facts with
direct protocol consequences that were not previously visible from the
roadmap text alone:

1. **PingPong (Sec. 28):** the acquired release merges ON and OFF event
   captures together before deriving its timestamp files, per its own
   documented preprocessing (`README`, `format-timestamps.py`,
   `underline_to_colon.py`). Existing eligibility criterion 2 ("the
   trigger order/timestamps can distinguish ON from OFF") is therefore
   **not automatically satisfied** by the data as released — it requires
   an explicit polarity-verification step that does not yet exist. Added
   Sec. 28.1 to make this an explicit, checkable precondition rather than
   an implicit assumption that would otherwise silently fail or get
   guessed at later.
2. **TU Wien Philips Hue (Sec. 29):** the opposite situation — ON/OFF
   polarity is directly and unambiguously encoded in each capture's
   filename, verified against all 10000 real files (5000/5000 split).
   Documented so this source is never mistakenly treated as needing the
   same verification step as PingPong.
3. **CIC IoT 2022 (Sec. 33):** the real interaction directories separate
   companion-app-triggered polarity from voice-assistant triggers by
   folder name. Documented which subfolders satisfy the existing Sec. 16
   companion-app intent-provenance requirement (`LOCAL_`/`LAN_`/`WAN_`)
   and which do not (`ALEXA_`/`GOOGLE_`), so this exclusion is decided
   once, from the protocol, rather than re-derived ad hoc by whoever
   writes the adapter.

**Nature of the change:** these are not new experimental decisions,
threshold changes, or protocol weakenings — they ground existing,
unchanged eligibility criteria against the concrete shape of the data
actually available, so future implementation work (and future readers of
the roadmap) don't have to re-discover them from scratch or, worse,
implement an incorrect assumption. No confirmatory result has been
inspected; this is pre-collection data-acquisition audit work.
