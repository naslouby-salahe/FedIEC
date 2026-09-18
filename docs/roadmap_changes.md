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

## 2026-09-17 — PingPong ON/OFF polarity blocker resolved (Sec. 28.1)

**Why:** Sec. 28.1 (added earlier the same day) documented that PingPong's
released `timestamps` files don't carry per-line ON/OFF polarity. Rather
than leave this as a standing blocker, the official PingPong tool source
(`github.com/uci-plrg/pingpong`) was inspected directly.
`SignatureGenerator.java` lines 123-126 show the tool itself assumes
strict alternation starting with ON, and its class-level documentation
confirms this is the actual data-collection protocol ("events ON and OFF
were generated alternately... using the automation scripts"), not an
algorithmic inference the tool makes from packet content. This closes the
criterion-2 gap for `local-phone/` and `same-vendor/` with source-level
evidence rather than a guess. `remote-phone/`, `ifttt/`, and
`public-dataset/` remain open (different provenance chain, criterion 3,
not yet checked).

**Nature of the change:** resolves a previously-documented blocker with
verified external evidence; does not alter any threshold, does not affect
already-collected FedIEC-Contracts data (none exists yet), and follows the
same "never guess" discipline the earlier entry established.

## 2026-09-18 — Mon(IoT)r IMC 2019 acquired-source boundary (Sec. 13)

**Why:** The official IMC 2019 archives were acquired under their data-sharing
agreement and audited locally. The raw hierarchy has individual Android
companion-app `on`/`off` experiment PCAPs, so each non-empty PCAP is a genuine
source group rather than an invented device-wide session. However, inspection
also established that the artifact does not include an independent in-capture
trigger instant, while the nominal idle hierarchy uses `unctrl`/`ctrl1` labels
that do not prove absence of control action. The source therefore cannot be
silently upgraded to the full three-context protocol.

**Nature of the change:** adds a source-specific application of existing
eligibility gates. It does not change any requirement, select a primary source,
or rely on model performance.

## 2026-09-18 — Holm correction family scope for pre-context (Sec. 66)

**Why:** Sec. 66 said Holm correction applies "across the three confirmatory
hypothesis comparisons," while Sec. 68 has always said pre-context value is
unavailable in the current empirical tier. Confirmatory-trial multiplicity
practice (FDA/EMA gatekeeping-procedure guidance) treats the corrected family
as the hypotheses actually tested; a hypothesis excluded before any result is
inspected, by a pre-specified data-feasibility criterion, is not a member of
that family and is not assigned a correction slot. Re-audited all four raw
datasets (including official upstream repos/papers for Mon(IoT)r, PingPong,
and CIC) for a missed NO_ACTION/idle-segmentation signal that could activate
pre-context; none exists — Mon(IoT)r's `unctrl` idle traffic is confirmed
(via the same bounded-duration filename convention the interaction captures
use) to be an unsegmented continuous daily trace, not a set of discrete
capture instances, so building NO_ACTION from it would require inventing a
window boundary the source does not provide.

**Nature of the change:** clarifies Sec. 66's family scope to match Sec. 68's
existing (unchanged) unavailability statement; does not add, remove, or
weaken any statistical procedure, and does not affect any already-computed
result since no confirmatory execution has occurred.

## 2026-09-18 — Comparison 1 primary outcome under zero-feasible-families (Sec. 67)

**Why:** Sec. 67 tied Comparison 1's primary outcome exclusively to "the
locked source-feasible artifact-controlled contract-violation suite," which
requires at least one of the 5 raw-timeline violation families (OMISSION,
SUBSTITUTION, UNCOMMANDED_EXECUTION, EXCESS_EXECUTION, REPLAY/LATE) to be
source-feasible. The frozen primary manifest records all 5 as
`SOURCE_INFEASIBLE`/`REPRESENTATION_UNOBSERVABLE`, so Comparison 1 as
literally worded was unrunnable, not merely untested. Sec. 55 (Direct
Contract Metric) already defines a separate, genuine-data-only test of the
same underlying claim — intent conditioning changes the model's score — by
scoring one real capture under its true intent versus a swapped incorrect
intent. No raw traffic is modified; no evidence is fabricated. Amending Sec.
67 to use this as the primary outcome under the current tier keeps
Comparison 1 in the confirmatory family instead of dropping it to two total
comparisons, while explicitly not claiming it as evidence of violation
detection (Sec. 67 now states the two formulations are not interchangeable,
and the violation-detection claim gates in Sections 80–81 are unchanged).

**Nature of the change:** activates an already-specified, previously-inert
roadmap section (Sec. 55) as a substitute primary outcome for one
comparison, gated on the same source-feasibility state the roadmap already
tracks. Does not lower the AUROC bar, does not fabricate a violation
population, does not touch Sections 80/81's claim gates, and does not affect
any already-computed result since no confirmatory execution has occurred.

## 2026-09-18 — Counterfactual/NO_ACTION search closed (no roadmap edit)

**Why:** Beyond the original 4-dataset audit (Sec. 13 decision record), this
round re-checked all 4 datasets' full raw trees, their official upstream
repositories/papers (Mon(IoT)r's `NEU-SNS/intl-iot`, PingPong's
`uci-plrg/pingpong`, CIC's official UNB page), and two additional
independent public datasets (UNSW-IoTraffic 2025, and Sivanathan 2020's
Belkin/LiFX boot/active/idle traces). UNSW-IoTraffic's own release notes
state "No ground-truth annotations of events or interactions are provided";
Sivanathan 2020 has no public dataset release (thesis-derived, no
repository/download link in the paper). None of the 6 candidates supports
an independently-documented per-device/per-context idle segmentation or
transition boundary. This closes the search for this project phase; the
counterfactual-feasibility freeze in `datasets/freeze.py` is confirmed
correct on the broadest evidence gathered so far.

**Nature of the change:** none — no roadmap wording changed by this entry.
Recorded so the search isn't silently re-litigated from scratch next phase.
