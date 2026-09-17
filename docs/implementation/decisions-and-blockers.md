# Decisions and Blockers

## Decisions

- FedIEC is a public-dataset-only computational study. Existing raw bytes
  are immutable; no physical acquisition, app automation, gateway capture,
  or induced-failure workflow is a confirmatory dependency.
- PingPong local-phone and same-vendor binary-device subsets use the
  documented alternating-polarity convention. Other PingPong subtrees are
  excluded until their own provenance audit succeeds.
- CIC voice-assistant folders are excluded. Only documented companion-app
  interaction folders are candidate material.
- TU Wien Philips Hue is a replication source and is not evidence for a
  multi-device federated claim by itself.

## Open scientific gates

1. Determine whether each PingPong candidate exposes enough independent
   source-group and passive-background evidence for the complete context
   protocol; do not reconstruct missing `NO_ACTION` data.
2. Complete CIC IoT 2022 device/source-group eligibility evidence before
   promoting it beyond `ACTION_CONTRACT_ONLY`.
3. Evaluate attack material only if intent, device, timing, attack interval,
   and execution alignment are independently documented.
