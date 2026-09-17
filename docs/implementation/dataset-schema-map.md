# Dataset Schema Map (Prompt 1)

## TU Wien Philips Hue — complete

| raw field | raw dtype | canonical field | canonical type | mapping rule | validation | eligibility relevance | evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| parent directory name | path segment | `device_id` | `DeviceId` | verbatim directory name | must exist, non-empty | one device per directory; multiple directories would be multiple devices | `tests/unit` (pending, see master-checklist) |
| filename `_Turn_On`/`_Turn_Off` suffix | path segment | `semantic_action` | `SemanticAction` | `On` -> `TURN_ON`, `Off` -> `TURN_OFF` | regex-anchored full match, no partial | required for every clean interaction | `enumerate_raw_interactions()` unit-verified against real 10000 files |
| filename `{yyyymmdd}_{hhmmss}` | path segment | `trigger_timestamp` | `WallClockTimestamp` | `datetime.strptime(..., "%Y%m%d_%H%M%S")` | must parse | intent timestamp (Roadmap Sec. 16) | verified |
| `.pcap` file itself | PCAP | `capture_path` | `RepositoryPath` | direct file reference | file exists | source for B/E feature extraction (Prompt 2) | verified |

`armstate_labeled.csv` at the dataset root: **not mapped, not FedIEC data**
(unrelated arm/disarm dataset accidentally co-located; excluded).

## PingPong — adapter implemented (local-phone/same-vendor), verified

| raw field | raw dtype | canonical field | canonical type | mapping rule | validation | eligibility relevance | evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| device+context directory name (e.g. `tplink-plug` under `smarthome`/`standalone`) | path segment | `device_id` | `DeviceId` | `f"{device}__{context}"` | matched against an explicit evidence-based allowlist (see `pingpong/dataset.py`), not guessed | Roadmap Sec. 28 device identity | implemented, 20 real device/context units enumerated |
| `.timestamps` file line (`MM/DD/YYYY HH:MM:SS AM/PM`) | text | `trigger_timestamp` | `WallClockTimestamp` | `datetime.strptime(..., "%m/%d/%Y %I:%M:%S %p")` | must parse; file read with a `latin-1` fallback for non-UTF-8 lines verified in real files | intent timestamp | implemented, verified against real files |
| trigger index within its `.timestamps` file | int (0-based) | `semantic_action` | `SemanticAction` | `index % 2 == 0 -> TURN_ON else TURN_OFF`, per PingPong's own `SignatureGenerator.java` lines 123-126 (Roadmap Sec. 28.1) | none needed — this is the documented collection protocol, not an inference | Roadmap Sec. 28 criterion 2 — **satisfied** for `local-phone`/`same-vendor` | verified: 2000 interactions, exactly 1000/1000 ON/OFF |
| `wlan1/*.pcap` (preferred), falling back to `wlan`/`eth0`/`eth1`/any other sibling directory | PCAP | `capture_path` | `RepositoryPath` | first vantage point found in priority order | AppleDouble `._*` sidecar files excluded (verified present in this checkout) | Roadmap Sec. 17 (gateway-only capture) | implemented; vantage-point choice is provisional, not yet protocol-locked |

`remote-phone/`, `ifttt/`, and `public-dataset/` are not yet covered by
the adapter (separate intent-provenance verification needed for each —
see `decisions-and-blockers.md`).

## CIC IoT 2022 — partial, adapter not yet built

| raw field | raw dtype | canonical field | canonical type | mapping rule | validation | eligibility relevance | evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| category directory (e.g. `Home Automation`) | path segment | (metadata only, not a canonical field) | — | — | — | device category context | inspected |
| device directory (e.g. `Gosund Plug - Center`) | path segment | `device_id` | `DeviceId` | verbatim | non-empty | device identity | inspected |
| trigger-method directory (`LOCAL_ON`/`LOCAL_OFF`/`LAN_ON`/`LAN_OFF`/`WAN_ON`/`WAN_OFF`) | path segment | `semantic_action` + companion-app eligibility flag | `SemanticAction` | `*_ON` -> `TURN_ON`, `*_OFF` -> `TURN_OFF`; `LOCAL_`/`LAN_`/`WAN_` = companion-app eligible, matches Roadmap Sec. 16 | must be one of the 6 app-triggered folder names | required — companion-app provenance | inspected against real `Gosund Plug - Center` folder |
| trigger-method directory (`ALEXA_ON`/`ALEXA_OFF`/`GOOGLE_ON`/`GOOGLE_OFF`) | path segment | excluded (voice assistant, not companion app) | — | — | — | Roadmap Sec. 16 requires official Android companion app; voice trigger does not qualify | inspected |
| `.pcap` file (3 per trigger-method folder) | PCAP | `capture_path` | `RepositoryPath` | direct file reference | file exists | source for B/E feature extraction | inspected |
| trigger timestamp | — | `trigger_timestamp` | `WallClockTimestamp` | read from each pcap's raw global+first-record header (`read_pcap_first_packet_timestamp()`) | classic-pcap magic number checked; raises on pcapng/unknown format rather than guessing | intent timestamp | implemented, verified against 264 real files |
| `6-Attacks/<mechanism>/<device>/*.pcap` | PCAP | potential real-attack alignment source (Roadmap Sec. 33) | — | not attempted | needs intent+attack-interval+execution alignment per device | Sec. 33 optional real-attack claim | inspected, not attempted |

**Adapter implemented**: `fediec.datasets.cic_iot_2022.dataset.enumerate_raw_interactions()`,
verified against real `3-Interactions/Home Automation/` data (264
interactions, 132/132 ON/OFF, all from `LOCAL_`/`LAN_`/`WAN_` folders
only).
