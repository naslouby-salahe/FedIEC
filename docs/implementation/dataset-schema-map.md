# Dataset Schema and Provenance Map

| Source | Raw convention | Canonical field | Type/enum | Rule and provenance | Validation | Eligibility relevance |
| --- | --- | --- | --- | --- | --- | --- |
| PingPong | audited `.timestamps` line | intent timestamp | `WallClockTimestamp` | original `TriggerTimesFileReader` treats source text as `America/Los_Angeles` and converts to UTC | parse and timezone conversion must succeed | independent trigger boundary |
| PingPong | classic-PCAP record header | capture timeline | `WallClockTimestamp` | microsecond PCAP time range contains all audited UTC trigger timestamps | full source-trigger range check | establishes clock compatibility, not a split exemption |
| PingPong | timestamp ordinal | semantic action | `SemanticAction` | documented strict alternation, first event ON; `VERIFIED_PROTOCOL` | audited subsets only | action provenance |
| PingPong | device/context path | device, source context, and source group | `DeviceId`, `SourceContextId`, `SourceGroupId` | physical device is distinct from its context path | no guessing | device/client identity and split boundary |
| CIC IoT 2022 | `LOCAL/LAN/WAN_{ON,OFF}` directory | semantic action | `SemanticAction` | documented app-triggered folder encoding, but boundary provenance is incomplete; `PARTIAL` | Alexa/Google excluded | diagnostic replication only unless new source evidence upgrades it |
| CIC IoT 2022 | `LOCAL`, `LAN`, or `WAN` folder prefix | source context | `SourceContextId` | preserve original trigger method as a distinct condition | no pooling across contexts | 3-PCAP split unit per action/context |
| CIC IoT 2022 | `Device List.xlsx` MAC address | target-device filter identity | `DeviceId` -> source MAC mapping | directory identity maps to listed device; mapped MAC appears in every selected PCAP's first Ethernet frame | selected-PCAP source/destination check | feature pipeline must retain target-endpoint traffic only |
| CIC IoT 2022 | first classic-PCAP record | capture start, not intent boundary | `WallClockTimestamp` | read only validated classic-PCAP headers; do not promote to trigger time | reject unknown format | excludes B-context/exact-trigger claims pending source evidence |
| TU Wien Philips Hue | `_Turn_On`/`_Turn_Off` filename suffix | semantic action | `SemanticAction` | source filename label; `VERIFIED_DIRECT` | anchored filename parse | replication action evidence |
| TU Wien Philips Hue | filename date/time | intent timestamp | `WallClockTimestamp` | parse source naming convention | parse must succeed | replication timing |
| Mon(IoT)r / IMC 2019 | `android_{lan,wan}_{on,off}` path | semantic action and app transport context | `SemanticAction`, `SourceContextId` | original companion-app experiment hierarchy; `VERIFIED_PROTOCOL` | exact ON/OFF directory match only | action-conditioned candidate evidence |
| Mon(IoT)r / IMC 2019 | individual non-empty classic-PCAP | source capture/group and capture start | `SourceCaptureId`, `SourceGroupId`, `WallClockTimestamp` | one PCAP per original experiment | empty/malformed PCAP excluded | leakage-safe split unit, not an independent trigger instant |
| Mon(IoT)r / IMC 2019 | official `devices_{us,uk}.txt` collection map | target-device capture filter | `TargetDeviceMac` | original `tag-experiment` captures with `ether host $MAC` | US/UK map lookup; VPN suffix removed only for network condition | target attribution without traffic-derived identity |
| Mon(IoT)r / IMC 2019 | `iot-idle/*/{unctrl,ctrl1}` paths | no admitted `NO_ACTION` label | none | labels do not independently prove absence of a command | do not map to `NO_ACTION` | full three-context gate remains unavailable |

`PublicSourceInteraction` retains dataset, interaction, device,
source-capture, source-group, action, capture-start or trigger timestamp, target-device MAC, provenance grade, and the
immutable source reference. It carries checksum, manufacturer, category,
topology, and transition only when independently available. Adapters must
not infer state, transition, NO_ACTION, intent, or a trigger time from target-device traffic.
