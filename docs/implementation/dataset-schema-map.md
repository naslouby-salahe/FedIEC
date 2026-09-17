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

## PingPong — partial, blocked on action-polarity verification

| raw field | raw dtype | canonical field | canonical type | mapping rule | validation | eligibility relevance | evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| device directory name (e.g. `tplink-plug`) | path segment | `device_id` | `DeviceId` | verbatim | non-empty | Roadmap Sec. 28 device identity | inspected, not yet coded |
| `.timestamps` file line (`MM/DD/YYYY HH:MM:SS AM/PM`) | text | `trigger_timestamp` | `WallClockTimestamp` | `datetime.strptime(..., "%m/%d/%Y %I:%M:%S %p")` | must parse | intent timestamp | format verified against real file, parser not yet written |
| — | — | `semantic_action` | `SemanticAction` | **UNRESOLVED** — no on/off polarity marker found in the timestamp file or any README in this checkout | — | Roadmap Sec. 28 criterion 2 ("trigger order/timestamps can distinguish ON from OFF") is currently **not established** for these devices | see `decisions-and-blockers.md` |
| `eth0/*.pcap`, `wlan1/*.pcap`, `vpn/*.pcap`, `event/*.pcap` | PCAP | `capture_path` (candidate, multiple per interaction) | `RepositoryPath` | one of several capture vantage points per device | needs disambiguation of which vantage point is the gateway-equivalent capture | Roadmap Sec. 17 (gateway-only capture) | inspected, mapping rule not yet frozen |

No PingPong adapter code exists yet; `describe_raw_availability()` is
presence-only. Full field mapping and eligibility per Roadmap Sec. 28
follow once the action-polarity blocker is resolved.

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
