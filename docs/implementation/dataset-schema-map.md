# Dataset Schema and Provenance Map

| Source | Raw convention | Canonical field | Type/enum | Rule and provenance | Validation | Eligibility relevance |
| --- | --- | --- | --- | --- | --- | --- |
| PingPong | audited `.timestamps` line | intent timestamp | `WallClockTimestamp` | parse documented timestamp format | parse must succeed | independent trigger boundary |
| PingPong | timestamp ordinal | semantic action | `SemanticAction` | documented strict alternation, first event ON; `VERIFIED_PROTOCOL` | audited subsets only | action provenance |
| PingPong | device/context path | device and source group | `DeviceId`, `SourceGroupId` | explicit binary-device allowlist and context path | no guessing | device/client identity |
| CIC IoT 2022 | `LOCAL/LAN/WAN_{ON,OFF}` directory | semantic action | `SemanticAction` | documented app-triggered folder encoding; `SOURCE_DOCUMENTED_PATH` | Alexa/Google excluded | action-contract gate |
| CIC IoT 2022 | first classic-PCAP record | intent boundary | `WallClockTimestamp` | read only validated classic-PCAP headers | reject unknown format | source timing |
| TU Wien Philips Hue | `_Turn_On`/`_Turn_Off` filename suffix | semantic action | `SemanticAction` | source filename label; `VERIFIED_DIRECT` | anchored filename parse | replication action evidence |
| TU Wien Philips Hue | filename date/time | intent timestamp | `WallClockTimestamp` | parse source naming convention | parse must succeed | replication timing |

`PublicSourceInteraction` retains dataset, interaction, device,
source-capture, source-group, action, timestamp, provenance grade, and the
immutable source reference. It carries checksum, manufacturer, category,
topology, and transition only when independently available. Adapters must
not infer state, transition, NO_ACTION, or intent from target-device traffic.
