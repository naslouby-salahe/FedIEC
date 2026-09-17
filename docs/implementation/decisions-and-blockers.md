# Decisions and Blockers

## Decisions

- **CIC IoT 2022 real on-disk directory name is `cic-iot-2022`**, not the
  roadmap's prose spelling `CIC IoT 2022`. `fediec.paths` maps
  `DatasetSource.CIC_IOT_2022` to the verified real name; the roadmap prose
  spelling is left unchanged (it is descriptive text, not a path).
- **`data/raw` is a symlink into a multi-project shared data pool**
  (`/home/naslouby/Projects/datp-shared-data/raw`), not a FedIEC-private
  directory. Only `FedIEC-Contracts/`, `PingPong/`, `TU Wien Philips Hue/`,
  `cic-iot-2022/` within it are FedIEC's concern; everything else in that
  pool belongs to other projects and must not be touched or referenced.
- **A `paths.py` module was added** (not in the original `technical_doc.md`
  locked tree) as the sole path-resolution owner, per technical_doc.md
  Sec. "Centralized Path Handling": "introduce the smallest justified
  module and update docs/technical_doc.md in the same change." Tree
  updated accordingly.
- **`docs/implementation/` was added**, also not in the original locked
  tree; this is the explicit deliverable of this prompt, and
  `technical_doc.md`'s tree section is updated in the same change.

## Open Blockers

1. **PingPong action polarity is unresolved.** The raw `.timestamps` files
   record trigger times but not which trigger was ON vs OFF. No README,
   script, or manifest in this checkout documents the convention (checked:
   dataset root `README`, `evaluation-datasets/public-dataset/smarthome/`
   scripts `format-timestamps.py` and `underline_to_colon.py` — neither
   documents polarity). Resolving this requires either the original
   PingPong paper/companion scripts (not present in this checkout) or a
   pcap-derived device-state heuristic verified against a known ground
   truth. No `SemanticAction` is assigned for PingPong until this is
   resolved — guessing an alternation convention would violate the
   "never implement an expected value without verifying the real source"
   rule.
2. **CIC IoT 2022 trigger timestamps are not in a separate log** — they
   must be read from each pcap's own first-packet capture time. The
   adapter needs a lightweight pcap-header reader; not yet implemented.
3. **FedIEC-Contracts does not exist.** It is the mandatory controlled
   benchmark (Roadmap Sec. 14) and must be collected via the Android
   harness + gateway capture pipeline, neither of which is built yet
   (`workflows/collect.py` is wired but raises `NotImplementedError`
   honestly rather than faking success). This is expected at this phase;
   the raw-benchmark directory contract
   (`captures/`, `intent-logs/`, `session-manifests/`, `device-metadata/`)
   is frozen in `paths.py` / `RepositoryPathKey` so `doctor` can check for
   it once collection begins.
