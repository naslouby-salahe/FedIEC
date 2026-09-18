# Frozen Public-Source Identity Manifest

Frozen on 2026-09-17 before any model evaluation. Each digest below is a
SHA-256 Merkle-style digest over the sorted selected capture records:
`repository-relative capture path`, byte size, and that capture's SHA-256.
It intentionally covers only adapter-enumerated candidate inputs, not
unrelated files in the shared external raw-data pool.

| Dataset | Selected captures | Aggregate input digest | Release/source reference | Role |
| --- | ---: | --- | --- | --- |
| PingPong | 20 continuous capture PCAPs | `c99c59fb21580867c394a44ac51ae1add110293d4e3611d90be5ca53572c0c1c` | official `uci-plrg/pingpong` commit `f3430ec011f8402654866dcf32552c6713ec953d`, `SignatureGenerator.java` line 126 | source-dependence diagnostic; clean-split ineligible |
| CIC IoT 2022 | 264 individual interaction PCAPs | `c60d63c64157d90c66a9b9afab49c0f28f973e7255e8931b533e93d2777a6aba` | CIC IoT Dataset 2022 interaction release; official dataset page documents three captures per interaction | secondary candidate, `PARTIAL` intent provenance |
| TU Wien Philips Hue | 10,000 individually labeled PCAPs | `ccbffafb221c735c59bdf1a2c60861dfb547a13814bdc242a5647a1e87b6caf5` | acquired TU Wien Philips Hue release | action-conditioned replication only |
| Mon(IoT)r / IMC 2019 | 10,100 raw Android ON/OFF-path PCAPs; 9,986 non-empty adapter records | `56018d542b4c31c1f7f3240b17968abf93bbf60b06cfe4adcaa2b1b1bdf90ed5` | official IMC 2019 interaction archive; archive SHA-256 `f622fe4b1f7a294df3a248bd6827193848d0d532c86f12fd157f3261b0fc0cbb` | approved primary for active capture-level action consistency |

The aggregate digest is a drift detector, not a replacement for public source
citations or a license assertion. No license term is inferred from the local
copy. A run must refuse to reuse a source-dependent artifact when its selected
capture digest, code identity, or configuration identity differs from the
corresponding frozen provenance record.

The acquired PingPong data-only copy does not contain the original polarity
tool, so the frozen upstream source pointer above is the authority for the
`VERIFIED_PROTOCOL` rule. Its `i % 2 == 0` assignment maps the first timestamp
to `TOGGLE_ON` and the next to `TOGGLE_OFF`; FedIEC applies that rule only to
the audited binary ON/OFF capture families. It is not reconstructed from
target traffic.

The Mon(IoT)r aggregate is over sorted Android ON/OFF-path PCAP names and their
individual SHA-256 values. Its separately acquired idle archive has SHA-256
`612fdc85b9f42a7d86b38d9b0b4cd27022b1eb8e39425aff129d862d4517e179`.
Neither archive is tracked by Git or disclosed through this manifest.
