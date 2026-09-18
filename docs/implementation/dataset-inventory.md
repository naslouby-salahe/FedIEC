# Dataset Inventory

`data/raw` is a shared external-data pool. FedIEC reads only the public
sources below and never alters raw bytes.

| Dataset | On-disk path | Availability | Candidate role | Eligibility readiness |
| --- | --- | --- | --- | --- |
| PingPong | `data/raw/PingPong/` | `PRESENT_AND_VALID` | source-dependence diagnostic | `VERIFIED_PROTOCOL` ON/OFF provenance, but inseparable continuous captures fail the clean-split gate |
| CIC IoT 2022 | `data/raw/cic-iot-2022/` | `PRESENT_AND_VALID` | secondary candidate | app-triggered LOCAL/LAN/WAN ON/OFF captures are `PARTIAL`: action semantics are documented, but no independent trigger boundary is documented |
| TU Wien Philips Hue | `data/raw/TU Wien Philips Hue/` | `PRESENT_AND_VALID` | mechanism replication | `REPLICATION_ONLY`: one device family, direct filename action/timestamp evidence |
| Mon(IoT)r / IMC 2019 | `data/raw/moniotr_imc19/` | `PRESENT_AND_VALID` | primary multi-device action-contract source | 19-feature capture-level audit and source-group split pass; strict B/E and NO_ACTION remain unavailable |

Adapter verification against the present files produced 2,000 PingPong
interactions (1,000 ON/1,000 OFF across 20 continuous capture groups), 264
CIC IoT 2022 interactions (132 ON/132 OFF across individual PCAP groups),
and 10,000 TU Wien interactions (5,000 ON/5,000 OFF, one PCAP per group).

The Mon(IoT)r adapter recognizes only directories exactly matching
`android_{lan,wan}_{on,off}`. It finds 9,986 non-empty labelled interaction
PCAPs (4,991 ON / 4,995 OFF), representing 26 physical device directory
identities across 296 device/context/action cells. The remaining interaction
PCAPs are deliberately outside the locked ON/OFF scope; empty captures are
excluded because they cannot establish an execution window.

No `FedIEC-Contracts` raw source is required, created, or consulted. Any
unrelated data in the shared pool are out of scope and remain untouched.

## Source evidence

- PingPong stores timestamp lines without an ON/OFF column. Its frozen official
  `SignatureGenerator.java` pointer (`uci-plrg/pingpong`
  `f3430ec011f8402654866dcf32552c6713ec953d`, line 126) documents strict
  ON/OFF alternation beginning with ON for the audited local-phone and
  same-vendor capture families.
- PingPong's original `TriggerTimesFileReader` declares timestamp text to be
  Los Angeles local time and converts it to UTC. The adapter now applies that
  conversion. A raw-header audit found that every selected continuous PCAP
  contains its complete source trigger range after conversion; PCAP timestamps
  have microsecond resolution. This supports source-clock alignment but cannot
  overcome the one-capture-group clean-split failure.
- CIC IoT 2022 maps the documented folder suffixes `*_ON` and `*_OFF` to
  action; Alexa and Google folders are excluded because they are not the
  required official-companion-app trigger evidence. The source does not
  document an intent timestamp or exact action boundary, so these records are
  `PARTIAL` rather than confirmatory action evidence.
- CIC's `Device List.xlsx` supplies companion-app and target-MAC metadata for
  all 15 selected directory identities. The mapped target MAC appears in the
  first Ethernet frame of all 264 selected PCAPs. This validates capture-to-
  device attribution, but it does not by itself make all packets in a capture
  target-device traffic; any future feature pipeline must filter by that MAC.
- TU Wien Philips Hue maps the anchored `_Turn_On` and `_Turn_Off` filename
  suffixes and parses capture time from the filename. Its co-located
  `armstate_labeled.csv` is unrelated and excluded.
- Mon(IoT)r records Android companion-app experiments in a dedicated
  device/action directory and uses one PCAP per experiment. The published
  Mon(IoT)r collection protocol supplies the action labels, while the raw
  artifact supplies the individual capture identity and packet timeline. This
  is `VERIFIED_PROTOCOL`, not `VERIFIED_DIRECT`: the distributed artifacts do
  not provide an independently recorded in-capture trigger instant.
- Mon(IoT)r's `iot-idle` archive is retained for provenance audit but is not
  mapped to `NO_ACTION`. Its actual leaf labels include `unctrl` (and one
  `ctrl1`), which do not independently establish an absence of action. No
  NO_ACTION evidence is therefore admitted from this source.

## Source order and pre-context confounding

- PingPong's frozen original protocol assigns alternating ON/OFF actions.
  Across the 20 capture contexts, chronological source labels have 1,000
  `TURN_ON -> TURN_OFF` and 980 `TURN_OFF -> TURN_ON` transitions, with no
  same-action transition. Pre-context interpretation is therefore structurally
  confounded and unavailable as an independent intent signal.
- TU Wien's filename timestamps likewise produce 5,000 `TURN_ON -> TURN_OFF`
  and 4,999 `TURN_OFF -> TURN_ON` transitions with no same-action transition.
  It is action-conditioned replication only and its pre-context comparison is
  descriptive at most.
- CIC has capture-start times but no independently documented trigger boundary;
  its action order is not a valid source-order input for B-context analysis.

The current typed records retain the source path as the immutable source
reference. The selected-input aggregate checksums and their source identities
are frozen in `source-identity-manifest.md`; they are source-drift detectors,
not claims about unrelated files in the shared raw-data pool.

## Clean-split source groups

The fixed `90/30/30` count previously present in `config.yaml` was stale and
has been removed. The frozen target is the roadmap's approximately 60/20/20
group-safe split, not an invented per-context count.

- PingPong: one continuous target-device detection capture contains each
  physical-device/context's alternating triggers. It is one inseparable source
  group; every ON or OFF context has 50 interactions, one group of 50, and
  fails the clean-split gate.
- CIC IoT 2022: official documentation states that each interaction has three
  packet captures. Each individual PCAP is therefore the source-capture group.
  `LOCAL`, `LAN`, and `WAN` are retained as distinct source contexts rather
  than pooled. Every available device/context/action cell has three groups of
  size one and receives the only leakage-safe three-way allocation, 1/1/1.
  The allocation is necessarily 33/33/33, not approximately 60/20/20, because
  groups are indivisible. It is not scientifically sufficient for the roadmap's
  thresholded or uncertainty-sensitive analyses: one calibration and one test
  trace per cell cannot establish those quantities, and CIC is `PARTIAL` for
  the independent-intent requirement in any event.
- TU Wien Philips Hue: each labeled PCAP is an individual source group. Its
  5,000 ON and 5,000 OFF captures split 3,000/1,000/1,000 per action context;
  it remains replication-only and cannot establish a multi-device primary
  result.
- Mon(IoT)r: an Android-labelled experiment PCAP is a genuine individual
  experiment capture and is therefore one source group. All 296 available
  device/context/action cells have at least three independent groups and can
  form overlap-free train/calibration/test partitions. The deterministic
  allocations are based on capture-start order and preserve whole PCAP groups.
  This succeeds the active capture-level split-structure gate. It does not
  establish the future strict B/E tier, an independent trigger boundary, or
  NO_ACTION evidence.

## Per-device/context audit

Counts below are per semantic action (`TURN_ON` and `TURN_OFF`) unless stated
otherwise. “Sufficient” means sufficient for the roadmap analysis named in the
last column; it does not substitute an invented lower threshold.

| Source | Physical device | Source context(s) | Interactions / groups / group sizes per action | Train / calibration / test | All partitions without overlap | Sufficient for required analysis |
| --- | --- | --- | --- | --- | --- | --- |
| PingPong | Amazon Plug | smarthome; standalone | 50 / 1 / [50] | 0 / 0 / 0 | No | No: clean-split gate fails |
| PingPong | D-Link Plug | smarthome; standalone | 50 / 1 / [50] | 0 / 0 / 0 | No | No: clean-split gate fails |
| PingPong | Sengled Bulb | smarthome; standalone | 50 / 1 / [50] | 0 / 0 / 0 | No | No: clean-split gate fails |
| PingPong | ST Plug | smarthome; standalone | 50 / 1 / [50] | 0 / 0 / 0 | No | No: clean-split gate fails |
| PingPong | TP-Link Bulb | smarthome; standalone | 50 / 1 / [50] | 0 / 0 / 0 | No | No: clean-split gate fails |
| PingPong | TP-Link Bulb White | standalone | 50 / 1 / [50] | 0 / 0 / 0 | No | No: clean-split gate fails |
| PingPong | TP-Link Camera | standalone | 50 / 1 / [50] | 0 / 0 / 0 | No | No: clean-split gate fails |
| PingPong | TP-Link Plug | smarthome; standalone | 50 / 1 / [50] | 0 / 0 / 0 | No | No: clean-split gate fails |
| PingPong | TP-Link Power Strip | standalone | 50 / 1 / [50] | 0 / 0 / 0 | No | No: clean-split gate fails |
| PingPong | TP-Link Two-Outlet Plug | standalone | 50 / 1 / [50] | 0 / 0 / 0 | No | No: clean-split gate fails |
| PingPong | Wemo Insight Plug | smarthome; standalone | 50 / 1 / [50] | 0 / 0 / 0 | No | No: clean-split gate fails |
| PingPong | Wemo Plug | smarthome; standalone | 50 / 1 / [50] | 0 / 0 / 0 | No | No: clean-split gate fails |
| CIC IoT 2022 | Amazon Plug | LAN; LOCAL; WAN | 3 / 3 / [1, 1, 1] | 1 / 1 / 1 | Yes | No: `PARTIAL` intent evidence and one calibration/test trace |
| CIC IoT 2022 | Atomi Coffee Maker | LAN; LOCAL; WAN | 3 / 3 / [1, 1, 1] | 1 / 1 / 1 | Yes | No: `PARTIAL` intent evidence and one calibration/test trace |
| CIC IoT 2022 | Globe Lamp | LAN; LOCAL; WAN | 3 / 3 / [1, 1, 1] | 1 / 1 / 1 | Yes | No: `PARTIAL` intent evidence and one calibration/test trace |
| CIC IoT 2022 | Gosund Plug - Center | LAN; LOCAL; WAN | 3 / 3 / [1, 1, 1] | 1 / 1 / 1 | Yes | No: `PARTIAL` intent evidence and one calibration/test trace |
| CIC IoT 2022 | Gosund Plug - Lower | LAN; LOCAL; WAN | 3 / 3 / [1, 1, 1] | 1 / 1 / 1 | Yes | No: `PARTIAL` intent evidence and one calibration/test trace |
| CIC IoT 2022 | Gosund Plug - Red | LAN; LOCAL; WAN | 3 / 3 / [1, 1, 1] | 1 / 1 / 1 | Yes | No: `PARTIAL` intent evidence and one calibration/test trace |
| CIC IoT 2022 | Gosund Plug - Roomba | LAN; LOCAL; WAN | 3 / 3 / [1, 1, 1] | 1 / 1 / 1 | Yes | No: `PARTIAL` intent evidence and one calibration/test trace |
| CIC IoT 2022 | Gosund Plug - Silver | LAN; LOCAL; WAN | 3 / 3 / [1, 1, 1] | 1 / 1 / 1 | Yes | No: `PARTIAL` intent evidence and one calibration/test trace |
| CIC IoT 2022 | Gosund Plug - Smart Board | LAN; LOCAL; WAN | 3 / 3 / [1, 1, 1] | 1 / 1 / 1 | Yes | No: `PARTIAL` intent evidence and one calibration/test trace |
| CIC IoT 2022 | Gosund Plug - Upper | LAN; LOCAL; WAN | 3 / 3 / [1, 1, 1] | 1 / 1 / 1 | Yes | No: `PARTIAL` intent evidence and one calibration/test trace |
| CIC IoT 2022 | Philips Hue Bridge | LAN; WAN | 3 / 3 / [1, 1, 1] | 1 / 1 / 1 | Yes | No: `PARTIAL` intent evidence and one calibration/test trace |
| CIC IoT 2022 | Tekin Plug 1 | LAN; LOCAL; WAN | 3 / 3 / [1, 1, 1] | 1 / 1 / 1 | Yes | No: `PARTIAL` intent evidence and one calibration/test trace |
| CIC IoT 2022 | Tekin Plug 2 | LAN; LOCAL; WAN | 3 / 3 / [1, 1, 1] | 1 / 1 / 1 | Yes | No: `PARTIAL` intent evidence and one calibration/test trace |
| CIC IoT 2022 | Yutron Plug 1 | LAN; LOCAL; WAN | 3 / 3 / [1, 1, 1] | 1 / 1 / 1 | Yes | No: `PARTIAL` intent evidence and one calibration/test trace |
| CIC IoT 2022 | Yutron Plug 2 | LAN; LOCAL; WAN | 3 / 3 / [1, 1, 1] | 1 / 1 / 1 | Yes | No: `PARTIAL` intent evidence and one calibration/test trace |
| TU Wien Philips Hue | Left Spot / Bridge Pro | labeled capture | 5,000 / 5,000 / 5,000 groups of one | 3,000 / 1,000 / 1,000 | Yes | Action-conditioned replication may be evaluated after its other gates; not sufficient for multi-device primary claims |
