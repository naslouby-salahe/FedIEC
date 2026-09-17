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
- **PingPong ON/OFF polarity is recovered from the official PingPong tool
  source**, not from the released `.timestamps` files themselves (which
  merge ON/OFF before the file is derived). `SignatureGenerator.java`
  lines 123-126 (`github.com/uci-plrg/pingpong`) show the tool assumes
  strict alternation starting with ON, and its documentation confirms this
  matches the actual collection protocol. Applied in
  `pingpong/dataset.py` for `local-phone/`/`same-vendor/`; see Roadmap
  Sec. 28.1.
- **PingPong device eligibility uses an explicit allowlist**, not a
  suffix heuristic — verified against every real directory name under
  `evaluation-datasets/{local-phone,same-vendor}/`. Devices with
  non-binary semantics (thermostats, alarms, locks, sprinklers, cameras,
  bulb color/intensity) are excluded by name, not inferred.

## Open Blockers

1. **PingPong `remote-phone/`, `ifttt/`, `public-dataset/` not yet
   covered.** The alternation convention (resolved, see above) should
   still apply mechanically, but their intent-provenance chain (Roadmap
   Sec. 28 criterion 3, "official Android-app interaction") has not been
   separately verified — `ifttt` is a third-party automation service, and
   `public-dataset`'s original trigger mechanism belongs to the IMC'19
   paper's methodology, not PingPong's own collection.
2. **FedIEC-Contracts does not exist.** It is the mandatory controlled
   benchmark (Roadmap Sec. 14) and must be collected via the Android
   harness + gateway capture pipeline, neither of which is built yet
   (`workflows/collect.py` is wired but raises `NotImplementedError`
   honestly rather than faking success). This is expected at this phase;
   the raw-benchmark directory contract
   (`captures/`, `intent-logs/`, `session-manifests/`, `device-metadata/`)
   is frozen in `paths.py` / `RepositoryPathKey` so `doctor` can check for
   it once collection begins.
