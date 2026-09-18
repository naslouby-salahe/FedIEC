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
- The clean-split target is approximately 60/20/20 at genuine source-group
  granularity. No fixed per-context count is a protocol gate.
- Mon(IoT)r is the approved primary source for the active capture-level
  interaction-consistency tier. PingPong fails its clean-split gate, CIC has
  sparse `PARTIAL` evidence, and TU Wien is replication-only.
- The active formulation is `p(X_interaction | I)`. Mon(IoT)r's lack of an
  in-capture trigger instant excludes only the future strict B/E tier; its
  `unctrl`/`ctrl1` idle labels remain insufficient for `NO_ACTION`.
- Mon(IoT)r is `FULL_CONTRACT_ELIGIBLE` only for the active two-action,
  complete-capture tier. This does not imply eligibility for strict B/E,
  NO_ACTION-dependent, timing-alignment, transition-dependent, or
  raw-composition counterfactual claims.
- The primary freeze records every counterfactual family as source-infeasible,
  representation-unobservable, or artifact-audit-insufficient until independent
  source evidence permits a raw-timeline transformation. This is a protocol
  boundary, not a model-performance decision.

## Open scientific gates

1. PingPong's continuous per-context capture groups fail the clean-split gate;
   do not split trigger rows across that capture.
2. CIC IoT 2022 has three independent one-PCAP groups per physical-device,
   trigger-method, and action context. Its 1/1/1 allocation is leakage-safe
   but does not meet the approximately 60/20/20 target and is not scientifically
   sufficient for the roadmap's thresholded or uncertainty-sensitive analyses.
   No smaller numerical requirement is being invented to override that result.
3. CIC's interaction directories and device list independently support action
   semantics and official companion-app identity. The device list supplies a
   target-MAC mapping; its mapped MAC appears in the first Ethernet frame of
   every selected PCAP. A future feature pipeline must still filter complete
   captures to that target endpoint. The source does not document a control-trigger timestamp. The
   first PCAP packet is a capture-start timestamp, not an independently valid
   trigger boundary; CIC is `PARTIAL` and must not support B-context or
   exact-trigger analyses until a source-backed boundary rule is established.
4. Evaluate attack material only if intent, device, timing, attack interval,
   and execution alignment are independently documented.
5. No source has a frozen three-context `NO_ACTION` procedure at this stage.
   PingPong has timestamped continuous traces but fails source-group splitting;
   CIC publishes idle material but lacks an independently documented action
   boundary for matching it to interaction contexts; TU Wien's labeled action
   captures do not independently label non-action intervals. All NO_ACTION-
   dependent and B-context analyses therefore remain unavailable.
6. The currently auditable source order is alternating for PingPong and TU
   Wien, so pre-context cannot be interpreted as an independent predictor of
   intent for those sources. CIC's capture-start order is not an action-order
   substitute. No source supports a confirmatory B-context comparison.
7. The former source-capture-start-to-first-target-packet feature was constant
   over all 9,986 eligible captures. It was removed as
   `PRE_MODEL_STRUCTURAL_DEGENERACY` before model execution, with user-approved
   protocol amendment. No filename timestamp replacement is allowed without
   authoritative source documentation.
8. The amended 19-feature Mon(IoT)r audit passes global constant and
   near-constant checks. Source/site/network-condition and collection-order
   metadata remain audit/reporting strata rather than model inputs; no raw
   identity enters the active representation.
9. Prompt 3 requires a source-feasible counterfactual and artifact-audit smoke,
   but the frozen primary manifest records no source-feasible family: omission
   and uncommanded execution require independently matched `NO_ACTION`,
   substitution requires independently documented transition compatibility,
   EXCESS requires verified natural concurrency and composition controls, and
   replay/late execution is unobservable without a verified boundary. Generating
   one to satisfy a smoke criterion would violate the active protocol. The
   counterfactual smoke requirement is therefore blocked by public
   data/provenance rather than implemented with a synthetic substitute.

## Source-of-truth cleanup still required

The roadmap remains scientifically authoritative, but it contains residual
superseded wording that must not be implemented: Section 36 calls the active
representation “20 network features” while enumerating 19 and then explicitly
locks 19; Section 40 repeats “20 source-defined interaction-capture features”;
Section 55 uses the obsolete `s(E,B,I)` notation; Sections 25.2, 57, 84, 86,
87, and 101 retain B-context/caliper, B/E extraction, timing-jitter, logging-
delay, or `W_d` language without consistently marking it future-secondary.
The active code path remains `(X_interaction, I)` with 19 features; no B/E,
`W_d`, command timestamp, or `NO_ACTION` dependency is activated by these
residual passages.
