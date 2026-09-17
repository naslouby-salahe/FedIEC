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

1. **PingPong action polarity — root cause confirmed, still unresolved.**
   `evaluation-datasets/public-dataset/smarthome/README` documents
   PingPong's own preprocessing: "we copy the PCAP files from the LAN
   folders for both ON and OFF events... into `wemo-insight-plug/wlan`",
   then merge with `mergecap` and derive the timestamp list from `ls -1`
   on the merged folder. PingPong **intentionally discards ON/OFF
   polarity** during its own packaging because its event-signature
   detection algorithm is polarity-agnostic. This is not a documentation
   gap on our side — the released `.timestamps` files structurally cannot
   distinguish ON from OFF. The `local-phone/` folders (PingPong's own
   collection) share the identical folder shape and very likely the same
   merge-and-discard pattern, though no pre-merge per-event files remain
   to confirm this directly. Recorded in `docs/FedIEC_Roadmap.md` Sec.
   28.1. Resolving this requires either the original IMC'19 per-event
   pcaps (separate ON/OFF directories, before PingPong's merge step —
   would need to be sourced from `moniotrlab.ccis.neu.edu/imc19`) or a
   pcap-content heuristic verified against independent ground truth. No
   `SemanticAction` is assigned for PingPong until one of these exists —
   guessing an alternation convention would violate the "never implement
   an expected value without verifying the real source" rule.
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
