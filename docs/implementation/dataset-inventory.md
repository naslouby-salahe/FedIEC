# Dataset Inventory

`data/raw` is a shared external-data pool. FedIEC reads only the public
sources below and never alters raw bytes.

| Dataset | On-disk path | Availability | Candidate role | Eligibility readiness |
| --- | --- | --- | --- | --- |
| PingPong | `data/raw/PingPong/` | `PRESENT_AND_VALID` | primary candidate | local-phone and same-vendor binary-device subsets have `VERIFIED_PROTOCOL` ON/OFF provenance; full-contract gate remains pending source-group and NO_ACTION review |
| CIC IoT 2022 | `data/raw/cic-iot-2022/` | `PRESENT_AND_VALID` | secondary candidate | app-triggered LOCAL/LAN/WAN ON/OFF captures are `ACTION_CONTRACT_ONLY` pending full eligibility audit |
| TU Wien Philips Hue | `data/raw/TU Wien Philips Hue/` | `PRESENT_AND_VALID` | mechanism replication | `REPLICATION_ONLY`: one device family, direct filename action/timestamp evidence |

Adapter verification against the present files produced 2,000 PingPong
interactions (1,000 ON/1,000 OFF across 20 source groups), 264 CIC IoT
2022 interactions (132 ON/132 OFF across 88 documented trigger groups),
and 10,000 TU Wien interactions (5,000 ON/5,000 OFF in one source group).

No `FedIEC-Contracts` raw source is required, created, or consulted. Any
unrelated data in the shared pool are out of scope and remain untouched.

## Source evidence

- PingPong stores timestamp lines without an ON/OFF column. Its official
  `SignatureGenerator.java` documents strict ON/OFF alternation beginning
  with ON for the audited local-phone and same-vendor capture families.
- CIC IoT 2022 maps the documented folder suffixes `*_ON` and `*_OFF` to
  action; Alexa and Google folders are excluded because they are not the
  required official-companion-app trigger evidence.
- TU Wien Philips Hue maps the anchored `_Turn_On` and `_Turn_Off` filename
  suffixes and parses capture time from the filename. Its co-located
  `armstate_labeled.csv` is unrelated and excluded.

The current typed records retain the source path as the immutable source
reference. A per-source checksum manifest is not yet frozen, so no checksum
is claimed; no expensive scan is repeated until the manifest owner exists.
