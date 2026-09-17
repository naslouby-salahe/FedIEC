# Dataset Inventory (Prompt 1)

`data/raw` is a symlink to `/home/naslouby/Projects/datp-shared-data/raw`, a
data pool shared across multiple unrelated PhD projects. Only the four
subdirectories below are relevant to FedIEC; the rest of that pool
(Edge-IIoTset, Gotham2025, N-BaIoT, TON-IoT, CICIoMT2024, EMBER2024, LAMDA,
CIC_IOT_Dataset2023, HITL-IoT, clamav-signatures, ...) is out of scope and
was not inspected.

| Dataset | Real on-disk path | Size | File count | Availability |
| --- | --- | --- | --- | --- |
| FedIEC-Contracts | `data/raw/FedIEC-Contracts/` | — | 0 | `MISSING_CONTROLLED_BENCHMARK` — collected, not downloaded (Roadmap Sec. 14-23). No fabricated data exists. |
| PingPong | `data/raw/PingPong/` | 41G | 1088 | `PRESENT_AND_VALID` (presence-level; deep schema map below is partial) |
| TU Wien Philips Hue | `data/raw/TU Wien Philips Hue/` | 51M | 10001 | `PRESENT_AND_VALID` — fully verified, adapter implemented |
| CIC IoT 2022 | `data/raw/cic-iot-2022/` (note: real dir name is lowercase-hyphen, **not** `CIC IoT 2022` as the roadmap prose spells it — verified, not assumed) | 65G | 5817 | `PRESENT_AND_VALID` (presence-level; deep schema map below is partial) |

`fediec.workflows.doctor.run_doctor()` reproduces this table live from
`fediec.datasets.*.dataset.describe_raw_availability()`.

## TU Wien Philips Hue — fully verified

Single device folder `Left_Spot_device__device_Bridge_Pro_20260420_184347/`
(a Hue spot light behind a "Bridge Pro" hub), containing exactly 10000
`.pcap` files named:

```text
{4-digit index}_{yyyymmdd}_{hhmmss}_{device label}_Turn_{On|Off}.pcap
```

5000 `Turn_On` + 5000 `Turn_Off`, confirmed by direct enumeration
(`fediec.datasets.tu_wien_philips_hue.dataset.enumerate_raw_interactions()`).
Trigger timestamp is directly encoded in the filename (local time, second
precision); no separate timestamp log file is needed.

`armstate_labeled.csv` at the dataset root is a **stray file from an
unrelated arm/disarm security-system dataset** (columns:
`label,TO-lengths,total-t,IAT,packet-amount`; labels `arm_home`,
`disarm`, `arm_away`) — not part of this Hue source, intentionally excluded
from enumeration, and not TU Wien Philips Hue data. Flagged as schema drift
at the dataset-root level, not device-level drift.

## PingPong — structure verified, action-polarity mapping open

Layout: `evaluation-datasets/{same-vendor,local-phone,ifttt,public-dataset,remote-phone}/{smarthome,standalone}/<device>/{eth0,wlan1,vpn,event,timestamps}/`.

Each device directory (e.g. `tplink-plug`) has a `timestamps/` folder with
one `.timestamps` file of plain-text trigger times
(`11/09/2018 08:17:31 AM`, one per line, no explicit ON/OFF column) and
sibling `eth0`/`wlan1`/`vpn`/`event` folders holding raw `.pcap` captures.
Binary devices (plugs) have one `-onoff`-style timestamp series per
device; multi-function devices (e.g. `tplink-bulb`) split into
`{device}-onoff/`, `{device}-color/`, `{device}-intensity/` subfolders.

**Open item (recorded in `decisions-and-blockers.md`):** the raw
`.timestamps` file does not itself state ON vs OFF per line — no README or
script found in this checkout documents whether entries alternate
ON/OFF/ON/OFF or another convention. No adapter code assigns
`SemanticAction` for PingPong until this is verified against the original
PingPong paper/scripts or pcap-derived device state; guessing is
explicitly forbidden by the working rules.

`negative-datasets/{YourThings,UNB,UNSW}/` are non-smart-home background
traffic corpora bundled with PingPong for its own negative-class
evaluation — not intent-labeled, out of scope for FedIEC's ON/OFF
contract task.

## CIC IoT 2022 — structure verified, adapter not yet built

`manifest.json` confirms all 6 top-level archives (`1-Power` .. `6-Attacks`)
were fully downloaded from `cicresearch.ca`. `Readme.txt` documents the six
experiments; `3-Interactions/Readme.txt` and per-category `Readme.txt`
files document interaction methods per device.

`3-Interactions/Home Automation/<device>/` directories (e.g.
`Gosund Plug - Center/`) contain per-trigger-method subfolders:
`LOCAL_ON`, `LOCAL_OFF`, `LAN_ON`, `LAN_OFF`, `WAN_ON`, `WAN_OFF` (companion
app over LAN/WAN — matches Roadmap Sec. 16's "official companion
application" intent-provenance requirement) and `ALEXA_ON/OFF`,
`GOOGLE_ON/OFF` (voice assistant — **not** an official companion-app
interaction per the roadmap, must be excluded from FedIEC eligibility).
Each subfolder holds 3 `.pcap` files (repeated captures), no per-trigger
timestamp file — the trigger timestamp must come from each pcap's own
first-packet time, which is a raw-capture read, not filename metadata.

`6-Attacks/{1-Flood,2-RTSP Brute Force,...}/<device>/` holds attacker-tool
traffic (`Nmap`, `Hydra`) per victim device — potential real-attack
alignment source for Roadmap Sec. 33, contingent on establishing intent
timestamp + attack-interval + execution alignment per device, not yet
attempted.

**Not yet built:** the directory-walking adapter that turns
`LOCAL_ON/LAN_ON/WAN_ON/OFF` folders into `RawTriggerInteraction` records
(mirroring the TU Wien adapter), and the pcap-first-packet-timestamp
extraction it needs. Recorded as remaining work, not fabricated.
