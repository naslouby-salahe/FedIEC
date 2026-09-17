# FedIEC Research Roadmap

## Research Identity

**Acronym:** **FedIEC**

**Short title:**
**FedIEC: Federated Intent–Execution Contracts for Mobile-Controlled IoT Security**

**Full title:**
**FedIEC: Federated Intent–Execution Contract Learning for Cross-Layer Anomaly Detection in Mobile-Controlled IoT Networks**

### One-Sentence Research Identity

FedIEC investigates whether explicit control actions issued through mobile companion applications can be treated as **runtime execution contracts**, whether violations of those contracts can be detected from the resulting IoT network behavior, and whether the underlying contract knowledge can be learned collaboratively across heterogeneous physical IoT devices using federated learning.

### Protocol-Hardening Principle

Counterfactual evidence is valid only when the detector cannot exploit the mechanics used to construct the counterfactual. The locked protocol therefore treats donor matching, transition semantics, B→E continuity, packet-timeline feasibility, transformation-specific artifact audits, donor dependence and statistical effective sample size as first-class validity conditions. If a valid transformation cannot be constructed under the frozen rules, the observation is reported as infeasible; the matching rules are never weakened to manufacture a positive result.

---

# 1. Research Motivation

Existing IoT network anomaly detectors primarily ask:

```math
Is this network behavior unusual?
```

or model an unconditional execution distribution:

```math
p(E)
```

where `E` represents observed IoT network behavior.

This formulation ignores information that is often available immediately before the device acts:

> **What was the device actually instructed to do?**

Mobile-controlled IoT systems provide an external source of such information.

A mobile companion application may issue an explicit action:

```text
TURN_ON
TURN_OFF

```

and the controlled IoT device subsequently produces a network execution.

FedIEC therefore treats a mobile-issued action as a runtime **execution contract**.

The security question becomes:

> Given the action that was explicitly requested and the network state immediately before that request, is the execution that follows compatible with what should have happened?

---

# 2. Core Concept

For every interaction, define:

```math
I
```

as the externally recorded intended action,

```math
B
```

as the network behavior immediately before the action,

and:

```math
E
```

as the network execution observed after the action.

The main contract model estimates:

```math
p(E \mid B,I)
```

rather than only:

```math
p(E)
```

or:

```math
p(E \mid I)
```

The anomaly score is:

```math
s(E,B,I)=-\log p(E\mid B,I)
```

A high score means:

> The observed execution is improbable given both the previous network context and the action that was explicitly requested.

---

# 3. Why This Is an Execution Contract

The word **contract** has a precise operational meaning in FedIEC.

An intent–execution contract states that when:

```text
a known action I

```

is issued under:

```text
a preceding execution context B

```

the resulting network behavior should belong to an admissible execution distribution:

```math
\mathcal C_I(B)
```

The contract therefore does not prescribe one exact packet sequence.

Instead, it defines a learned admissible region:

```math
E \in \mathcal C_I(B)
```

A contract violation occurs when:

```math
E \notin \mathcal C_I(B)
```

or when an action-like execution occurs without a corresponding recorded intent.

This accommodates encrypted traffic, protocol variation, retransmissions, cloud-mediated communication, timing variability, and differences between physical devices.

---

# 4. Research Scope

The confirmatory semantic actions are:

```text
TURN_ON
TURN_OFF

```

A third context is included:

```text
NO_ACTION

```

`NO_ACTION` is not treated as a third semantic device action.

It represents a time window in which no mobile control action was issued.

This enables FedIEC to distinguish:

```text
expected execution after ON
expected execution after OFF
ordinary behavior when no command occurred

```

without inferring the intended action from network traffic.

Other semantic actions such as:

```text
ARM
DISARM
OPEN
CLOSE
STREAM
CHANGE_VOLUME
CHANGE_COLOR
CONFIGURE
QUERY_STATUS

```

are outside the confirmatory study.

They may be explored only after the locked ON/OFF study is complete.

---

# 5. Intent Provenance Requirement

The intended action must come from an **independent control-plane source**.

Allowed sources are:

1. an experimental Android automation harness;
2. an explicitly recorded mobile-app interaction;
3. dataset metadata generated during the original controlled interaction;
4. another independently logged control event with equivalent provenance.

The intended action must never be inferred retrospectively from:

```text
packet lengths
packet timing
traffic direction
device responses
predicted action labels
network signatures

```

of the execution being evaluated.

This separation is fundamental.

Otherwise the model would be validating a label that was derived from the same evidence it is supposed to verify.

---

# 6. Mobile Application Role

The mobile companion application is a first-class part of the security setting but is **not itself reverse engineered in the confirmatory study**.

Its role is:

```text
Mobile companion app
        ↓
Explicit user/control action
        ↓
Externally logged intent
        ↓
IoT network execution
        ↓
Execution-contract verification

```

The mobile application therefore provides **action provenance**.

FedIEC investigates whether this provenance supplies security information that network behavior alone does not provide.

---

# 7. State-of-the-Art Boundary

The novelty claim must not rest on any of the following ideas individually.

## Companion-App Behavioral Analysis

Existing research already shows that mobile companion applications expose valuable information about IoT communication and device behavior.

Therefore:

> Using companion applications to understand IoT behavior is not itself novel.

## UI/User-Action to Network-Behavior Linkage

Prior work has already linked explicit smartphone or application-side user actions to subsequent network behavior for security policy generation and flow attribution. This includes, at minimum, the following collision anchors that must be discussed directly in the final related-work section:

```text
Chuluundorj, Liu, Shue — Generating Stateful Policies for IoT Device Security with Cross-Device Sensors — IEEE NoF 2022 — DOI 10.1109/NoF55974.2022.9942547
Liu et al. — By Your Command: Extracting the User Actions that Create Network Flows in Android — IEEE NoF 2023 — DOI 10.1109/NoF58724.2023.10302820
```

Therefore:

> Linking a mobile/user action to later network activity is not itself novel.

FedIEC must be positioned against these works by emphasizing the different research object: probabilistic execution-contract verification under independently logged intent, heterogeneous federated learning, structured violation semantics, and unseen-device transfer.

## Command-Associated Network Behavior

Existing work has associated user/device commands with characteristic network responses and device-event signatures.

Therefore:

> Observing that ON/OFF commands generate recognizable network behavior is not itself novel.

## Semantic Smart-Home Anomaly Detection

Existing approaches already reason over semantic correlations, device interactions, action fingerprints, expected state transitions, and intended/unintended physical behavior.

Therefore:

> Semantic consistency checking is not itself novel.

## Federated IoT Detection

Federated learning has already been applied to IoT malware and anomaly detection.

Therefore:

> Applying FedAvg to IoT traffic is not itself novel.

## Personalized or Logic-Aware Federated Learning

Federated systems that preserve client-specific knowledge or incorporate logical properties also exist outside this precise security problem.

Therefore:

> Adding client semantics or personalization to FL is not, by itself, a defensible novelty claim.

## Novelty-Audit Rule

The final novelty audit must search literature through the actual submission date, not stop at the current corpus. At minimum it must explicitly search for combinations of:

```text
mobile intent + IoT network execution
user action + IoT traffic + security enforcement
cross-layer semantic anomaly detection
runtime policy / contract verification for IoT
federated semantic anomaly detection
federated cross-device behavior learning
unseen-device semantic transfer
conditional density / generative modeling of IoT actions
```

Any newly discovered collision narrows the claim wording; it does not justify weakening the experimental protocol.

---

# 8. Precise Research Gap

The reviewed literature contains the individual ingredients:

```text
mobile companion-app behavior
+
explicit user-action / UI-to-network linkage
+
command/event network signatures
+
semantic IoT anomaly detection
+
execution/state consistency checking
+
federated IoT anomaly detection
+
cross-device learning
```

FedIEC does not claim novelty from merely combining these labels.

The narrower gap investigated is whether **independently recorded mobile-side intent can serve as provenance for a probabilistic network execution contract, modeled as \(p(E\mid B,I)\), that is learned collaboratively across naturally heterogeneous physical IoT devices, tested against artifact-controlled semantic violation classes and physically realized control-path anomalies, and evaluated under genuine unseen-device and unseen-manufacturer transfer without target-domain normalization leakage.**

The target contribution therefore requires the joint presence of:

```text
independent mobile intent provenance
+
pre-action behavioral context
+
post-action execution
+
artifact-controlled contract counterfactuals
+
physically realized violations
+
natural physical-device clients
+
federated learning
+
data-scarcity collaboration analysis
+
heterogeneity and topology characterization
+
genuine unseen-device transfer
+
where possible unseen-manufacturer transfer
```

The research question is not whether ON/OFF traffic can be recognized. It is whether the **relationship between independently observed intent and resulting execution** can be learned as a transferable security contract and whether federation provides measurable value when individual devices have limited contract data.

No absolute claim such as:

```text
first ever
never previously considered
completely novel
first action-aware IoT detector
```

is permitted until the final pre-submission literature audit.

---

# 9. Novelty Architecture

FedIEC is intentionally designed so that novelty does **not** depend on one experimental result.

The project has six contribution layers.

## Contribution A — Security Task

Define **intent–execution contract verification** as a cross-layer IoT security task.

The problem is not merely:

```text
classify ON versus OFF
```

or:

```text
detect unusual traffic
```

but:

```text
verify whether execution is legitimate
relative to independently observed mobile intent
and the pre-action behavioral context
```

## Contribution B — Violation Taxonomy and Observability Boundary

Define and evaluate distinct contract-violation families:

```text
OMISSION
SUBSTITUTION
UNCOMMANDED_EXECUTION
EXCESS_EXECUTION
REPLAY_OR_LATE_EXECUTION
```

For each family, state what is observable under the locked feature representation. A theoretically meaningful violation that is not identifiable from the available observables is reported as an **observability limit**, not forced into a positive detection claim.

## Contribution C — Synchronized Physical Benchmark

Create a reproducible physical-device benchmark containing:

```text
mobile intent
physical device identity
manufacturer and category metadata
network-topology metadata
intent timestamp
session/day identifier
pre-action network context
post-action network execution
semantic action
pre/post physical state where observable
clean/violation status
violation type
counterfactual provenance
```

## Contribution D — Artifact-Controlled Contract Evaluation

Counterfactuals are generated from held-out raw windows under frozen common-support calipers, deterministic session/day matching, recipient-state transition compatibility, B→E boundary-continuity checks and raw-timeline feasibility rules. Replacement/translation transformations and EXCESS composition are audited separately so apparent security performance cannot be explained by splice, merge, timestamp, flow-state or donor-selection artifacts.

## Contribution E — Federated Contract Learning

Evaluate whether contract knowledge can be learned collaboratively with:

```text
one physical device = one federated client
```

without centrally pooling raw interaction traces, and determine when collaboration is useful as local clean-contract data become scarce.

## Contribution F — Cross-Device and Cross-Manufacturer Transfer

Evaluate whether a contract learned from other physical devices can recognize valid and invalid intent–execution relationships on a physical device absent from model training, and where device coverage permits, on a manufacturer absent from training.

No single contribution is sufficient by itself to support every proposed claim.

Together they define the FedIEC contribution space.

---

# 10. Novelty-Survival Principle

The chapter remains scientifically useful even if the main model does not produce a large improvement.

The following outcomes do **not** invalidate the entire project:

```text
conditional density model ≈ direct action classifier
federated model ≈ local models
federated model < centralized model
some violation types are difficult to detect
some device types transfer poorly
ON/OFF distinction is weak for one device

```

Such results restrict the permitted claims but do not remove:

```text
the security task
the benchmark
the violation taxonomy
the evaluation protocol
the cross-device analysis
the empirical boundary finding

```

This is a non-negotiable design objective.

---

# 11. Research Questions

## RQ1 — Contract Information

Does knowledge of independently recorded mobile intent improve execution-consistency detection beyond execution-only network modeling?

## RQ2 — Pre-Execution Context

Does conditioning on the network context immediately before the mobile action improve contract verification beyond modeling:

```math
p(E\mid I)
```

alone, after eliminating command-order and settling-tail confounds?

## RQ3 — Violation Differentiation

How well can the same clean-trained contract model detect:

```text
omission
substitution
uncommanded execution
excess execution
replay/late execution where observable
```

without being trained on those violations and without exploiting counterfactual-generation artifacts?

## RQ4 — Federated Learnability

Can intent–execution contracts be learned collaboratively across naturally different physical IoT devices?

## RQ5 — Heterogeneity and Collaboration Need

How do contract distributions vary across devices, manufacturers and network topologies, and under what local-data scarcity levels does federation provide measurable benefit over isolated learning?

## RQ6 — Cross-Device Generalization

Can a federated contract model trained without one physical device identify valid and invalid intent–execution relationships on that device using no target-device training, calibration or normalization information in the main zero-shot result?

## RQ7 — Security Relevance

Do physically induced control-path anomalies and, where valid ground truth exists, real attack scenarios produce measurable contract violations under a frozen clean-trained detector?

## RQ8 — Intent-Provenance Robustness

How sensitive is contract verification to realistic intent-provenance imperfections such as timestamp jitter, logging delay, missing intents and duplicate intents?

## RQ9 — Transfer Boundary

How much of unseen-device performance is explained by semantic transfer versus protocol/topology mismatch, and does transfer remain meaningful within topology-matched groups and, where supported, under leave-one-manufacturer-out evaluation?

---

# 12. Main Hypothesis Structure

Exactly three comparisons are confirmatory.

## Hypothesis 1 — Intent Value

Compare:

```math
p(E\mid B,I)
```

against:

```math
p(E\mid B)
```

This isolates the contribution of explicit intent.

## Hypothesis 2 — Context Value

Compare:

```math
p(E\mid B,I)
```

against:

```math
p(E\mid I)
```

This determines whether the **change from the preceding behavioral state** contains useful information beyond the old action-conditioned formulation.

## Hypothesis 3 — Collaborative Value

Compare:

```text
federated contract learning

```

against:

```text
isolated local contract learning

```

using identical client populations and architectures.

Other comparisons are required baselines or secondary analyses but are not added to the confirmatory hypothesis family.

---

# 13. Dataset Hierarchy

The revised evidence hierarchy is:

```text
Mandatory controlled FedIEC benchmark
        ↓
PingPong external device-event validation
        ↓
TU Wien Philips Hue mechanism replication
        ↓
CIC IoT 2022 or another valid aligned dataset
for optional real-attack validation

```

The controlled benchmark is no longer a contingency.

It is a core contribution.

Public datasets provide independent replication and external validity.

A public dataset may not replace the controlled benchmark simply because it produces stronger model performance.

---

# 14. Mandatory Controlled Benchmark

The controlled benchmark is provisionally named:

**FedIEC-Contracts**

The confirmatory benchmark contains **at least six physical consumer IoT devices**, with a target of eight where acquisition and stable control are feasible before protocol lock.

Minimum requirements:

```text
K >= 6 physical devices
target K = 8
>= 3 manufacturers
>= 3 device categories
official Android companion application
explicit ON function
explicit OFF function
network traffic observable at controlled gateway
device identity unambiguous
mobile action timestamp recordable independently
```

Device categories should include at least three of:

```text
smart bulb
smart plug
smart switch
smart power strip
other binary-actuation consumer IoT device
```

Network-control topology is recorded for every device using a locked metadata label such as:

```text
LOCAL_WLAN
CLOUD_MEDIATED
HYBRID_OR_OTHER
```

Where acquisition permits, the benchmark should contain at least two devices in each topology represented by the main transfer claims.

The collection must span multiple independent sessions. For every device, the 150 observations per intent context are distributed across:

```text
>= 5 collection sessions
>= 3 distinct collection days
```

so statistical uncertainty is not based solely on repeated model seeds from one capture session.

Device brands, categories and topologies are selected before confirmatory model evaluation and never selected based on performance.

---

# 15. Device Replacement Rule

A device may be replaced before the main collection only if it fails a technical eligibility criterion such as:

```text
cannot reliably connect to the test network
official Android application unavailable
ON/OFF control not reproducible
traffic cannot be attributed to the device
mobile action cannot be timestamped independently
device becomes defective

```

A device may **not** be replaced because:

```text
its distributions overlap
its model performance is poor
its behavior differs strongly from other devices
it reduces federated performance
it produces inconvenient results

```

Replacement occurs before confirmatory collection.

---

# 16. Android Control Harness

Actions are generated through the vendor's official Android companion application.

The preferred automation order is:

```text
Android UIAutomator / ADB
        ↓
Appium if required
        ↓
manually triggered action with independently logged timestamp
only if reliable automation is impossible
```

Every action record contains:

```text
interaction_id
device_id
session_id
collection_day
app_package
semantic_action
intent_timestamp_monotonic
intent_timestamp_wall_clock
trigger_start_timestamp
trigger_completion_timestamp if observable
automation/manual source
capture_id
expected pre-state
observed post-state where measurable
```

The semantic label is recorded by the experimental harness before or at the time the action is triggered.

No network classifier is used to generate the label.

Clock alignment between the Android intent logger and gateway capture is checked at session start and session end. A session is invalid if synchronization error exceeds the pilot-locked tolerance.

The harness must also support a provenance-robustness replay mode in which recorded intent timestamps can be deterministically perturbed **after clean collection** for the pre-registered timestamp-jitter analysis. These perturbations never replace the original trusted timestamps.

---

# 17. Network Capture Architecture

The controlled environment contains:

```text
Android phone
        ↓
controlled Wi-Fi access point / gateway
        ↓
physical IoT device
        ↓
Internet / vendor cloud if required

```

Packet captures are collected at the controlled gateway.

Both phone and IoT traffic may be retained for provenance and debugging.

The **detection model itself uses only traffic attributed to the target IoT device**.

Mobile-phone payloads are not model inputs.

This prevents the model from trivially reading the outgoing command or learning vendor-specific mobile identifiers.

---

# 18. Pilot Phase

Before confirmatory collection, perform an excluded pilot on **every core device**:

```text
20 TURN_ON interactions per device
20 TURN_OFF interactions per device
>= 60 minutes passive/background monitoring per device
```

Pilot observations are used only to:

```text
verify automation
verify capture attribution
estimate device settling latency
freeze the inter-action separation rule
determine the fixed pre/post observation-window length W
characterize routine background activity for NO_ACTION strata
verify device state transitions
verify repeated ON->ON and OFF->OFF behavior where supported
measure Android↔gateway timestamp synchronization error
measure capture timestamp resolution and raw packet-order stability
record the effective gateway/link capture characteristics needed for physical-timeline checks
characterize natural short-gap/inter-arrival behavior and packet-timestamp collision rates
characterize naturally occurring action-plus-background concurrency
freeze the raw B→E boundary-continuity descriptor and matching procedure
freeze the pre-action-context distance metric and caliper-construction procedure
freeze the EXCESS_EXECUTION composition/serialization feasibility checks
classify device network-control topology
detect collection bugs
```

For device `i`, define the pilot-derived conservative settling latency:

```math
L_{settle,i}
```

as the upper locked bound after which command-related traffic has returned to the device's steady background regime.

Pilot samples are never used for:

```text
main model training
threshold calibration
confirmatory testing
model selection
claim support
```

After the pilot, `W`, settling rules, timestamp tolerance, background-activity strata, collection-state rules, counterfactual matching hierarchy, boundary-continuity definition, raw-timeline feasibility checks and artifact-audit tolerance are frozen.

The pilot fixes **procedures**, not confirmatory thresholds derived from held-out data. Any data-dependent context caliper or natural-timing envelope used later is computed from the clean **training partition only** after the chronological split and before violation scores are inspected.

---

# 19. Observation Windows

For each intent timestamp:

```math
t_I
```

construct:

```math
B = [t_I-W,\;t_I)
```

and:

```math
E = [t_I,\;t_I+W)
```

where:

```text
B = pre-action behavioral context
E = post-action execution
```

`W` is frozen after the excluded pilot.

The same `W` is used for every device in the confirmatory benchmark unless a technical impossibility is documented during the pilot before any confirmatory samples are inspected.

No per-device window tuning is permitted after confirmatory data are inspected.

## Settling-Integrity Rule

The pre-action context of a command must not contain the decaying execution tail of the preceding controlled action.

For consecutive controlled intents at `t_j` and `t_{j+1}` on device `i`, require:

```math
t_{j+1}-t_j \ge 2W + L_{settle,i}
```

Equivalently, once the previous post-action window ends at `t_j+W`, no new controlled intent is issued until at least:

```math
W + L_{settle,i}
```

additional time has elapsed.

This guarantees that:

```math
[t_{j+1}-W,\;t_{j+1})
```

represents a steady pre-action context rather than command-tail contamination.

Any interaction violating the frozen separation rule is excluded before splitting and the reason is recorded.

---

# 20. NO\_ACTION Windows

Dedicated background windows are collected for every physical device.

They satisfy:

```text
no mobile control intent in ±W
no controlled action tail intersects B or E
device remains connected
device remains in its ordinary operating environment
no deliberate violation is occurring
```

They receive:

```text
IntentContext = NO_ACTION
```

## Stratified Background Sampling

`NO_ACTION` must not collapse into a trivial all-zero "idle" class.

During the excluded pilot, background windows are partitioned into three locked activity strata using a training-independent activity score based only on packet/byte volume:

```text
BACKGROUND_SILENT
BACKGROUND_LOW_ACTIVITY
BACKGROUND_ACTIVE_BURST
```

The 150 confirmatory `NO_ACTION` windows per device are allocated equally:

```text
50 silent
50 low-activity
50 active-background
```

`BACKGROUND_ACTIVE_BURST` windows are aligned to spontaneous legitimate traffic such as:

```text
keep-alives
vendor cloud synchronization
NTP/DNS-related activity where attributable to the device
routine telemetry/status traffic
other recurring benign background bursts
```

without any corresponding mobile command.

Pseudo-event timestamps for active-background windows are placed using the frozen pilot rule so that the burst is meaningfully represented in `B`, `E`, or across their boundary rather than sampled only from network silence.

The activity stratum is metadata, not a model feature.

Performance and false alarms must be reported separately for all three `NO_ACTION` strata.

---

# 21. Clean Collection Size

For each device collect:

```text
150 TURN_ON interactions
150 TURN_OFF interactions
150 NO_ACTION windows
```

Therefore, for `K` physical devices:

```math
N_{clean}=K\times3\times150=450K
```

The minimum confirmatory benchmark with `K=6` contains:

```math
2700
```

clean contract observations.

The target `K=8` benchmark contains:

```math
3600
```

clean contract observations.

The clean dataset is fixed before violation-generation experiments begin.

---

# 22. Clean Split

Within every:

```text
device × intent context
```

the chronological split is:

| Partition | Samples per device × context |
| --- | ---: |
| Training | 90 |
| Calibration | 30 |
| Test | 30 |

For `K` devices:

```text
Training    = 270K
Calibration = 90K
Clean test  = 90K
```

At the mandatory minimum `K=6`:

```text
Training    = 1620
Calibration = 540
Clean test  = 540
```

No random train/calibration/test split is used.

No repeated interaction may cross partitions.

Each partition must retain representation from multiple collection sessions where sample counts permit. Session identifiers are preserved so the statistical analysis can cluster interactions correctly.

---

# 23. Collection Order

Large homogeneous ON-only or OFF-only blocks are forbidden, but deterministic ON/OFF alternation is also forbidden because it can make the next intent predictable from the previous physical/network state.

The confirmatory sequence uses a **constrained randomized action schedule** generated before collection.

The schedule must:

```text
respect the frozen settling-integrity rule
balance TURN_ON and TURN_OFF counts across sessions
randomize action order subject to physical-state validity
include repeated ON->ON and OFF->OFF requests where the official app/device accepts them reliably
interleave NO_ACTION collection across sessions and days
avoid selecting actions based on observed network traces or model scores
```

Repeated same-state commands are retained as the same semantic action, not introduced as new labels. Their purpose is to prevent the pre-action state from deterministically revealing the next intent and to force the model to use the full `(B,I)` relationship.

For every action transition type, report the number of observations, including:

```text
OFF -> ON
ON -> OFF
ON -> ON where supported
OFF -> OFF where supported
```

The collection design reduces:

```text
temporal drift confounding
cloud-condition confounding
firmware-session confounding
collection-order confounding
previous-action leakage
state-to-intent determinism
```

The exact randomization seed and generated action schedule are released.

---

# 24. Contract-Violation Taxonomy

FedIEC evaluates five distinct failure semantics, but every family is subject to an explicit **observability, physical-feasibility and artifact-control boundary**. A violation family is not credited merely because a synthetic transformation is easy to distinguish.

## 24.1 Omission

```text
Intent exists
Expected execution is absent within W
```

Example:

```text
TURN_ON requested
device remains behaviorally idle within W
```

An execution that occurs only after `W` is not distinguishable from omission **inside the original intent window alone**. Late execution therefore requires the separate temporally misaligned evaluation defined in 24.5.

`OMISSION` counterfactuals use matched legitimate `NO_ACTION` execution material and must pass the replacement/translation artifact audit in Section 25.

## 24.2 Substitution

```text
Intent exists
Execution is compatible with a different legitimate action
```

Example:

```text
TURN_ON requested
execution corresponds to TURN_OFF
```

Substitution is defined relative to the **recipient physical pre-state**. The donor execution must come from the same physical device and from a donor pre-state equivalent to the recipient pre-state for the substituted action. Therefore the donor's observed transition class under the substituted action must be exactly the transition class that the substituted action would induce from the recipient pre-state.

Examples:

```text
recipient pre-state OFF + substituted TURN_OFF
    -> donor must be an OFF -> OFF execution, not ON -> OFF

recipient pre-state ON + substituted TURN_OFF
    -> donor must be an ON -> OFF execution, not OFF -> OFF
```

This rule prevents a model from detecting a physically impossible state-transition signature rather than an intent–execution mismatch.

## 24.3 Uncommanded Execution

```text
No mobile intent exists
Action-like execution occurs
```

Example:

```text
NO_ACTION recorded
device exhibits a normal TURN_ON-like execution
```

Evaluation must include background-active `NO_ACTION` windows so the detector cannot solve this task as silence-versus-activity classification.

The donor action execution must satisfy the same context, session, boundary-continuity and temporal-alignment rules used elsewhere in Section 25.

## 24.4 Excess Execution

```text
Expected execution occurs
but an additional legitimate-looking device-network effect is present
```

The mandatory Level-A construction is **not random packet noise** and is **not a naïve PCAP overlay**.

For a clean held-out action execution, combine its raw packet timeline with a held-out, active, legitimate `NO_ACTION` background burst from the same device only after the pair passes the matching and physical-timeline feasibility rules in Section 25. The complete 20-feature `E` window is then re-extracted from the resulting raw timeline.

The intended semantic composition is:

```text
valid commanded execution
+
valid uncommanded background behavior
```

rather than arbitrary corruption.

### Physical-Timeline Requirement

An `EXCESS_EXECUTION` composite is admissible only if all of the following hold before feature extraction:

```text
both components are raw held-out captures from the same physical device
the background donor satisfies the locked session/day hierarchy and B-context caliper
internal packet order and internal packet offsets of both components are preserved
no packet timestamp is manually epsilon-jittered to force feasibility
no newly introduced timestamp-collision pattern exceeds the clean training-derived envelope
no newly introduced ultra-short inter-arrival pattern exceeds the clean training-derived envelope
no conflicting TCP stream state or incompatible packet ordering is created across a shared transport flow
components sharing an active TCP 5-tuple are rejected unless continuation compatibility is mechanically verified
raw B→E boundary continuity remains compatible with the recipient context
the transformed timeline passes the frozen raw-timeline feasibility checker
```

Raw transport identifiers, TCP sequence/acknowledgment information and timestamp-resolution diagnostics may be used **only** by this feasibility checker. They never become contract-model features.

If any check fails, the candidate is recorded as:

```text
COUNTERFACTUAL_INFEASIBLE_PHYSICAL_TIMELINE
```

and is not repaired by arbitrary timestamp perturbation.

### Natural-Concurrency Boundary

Before an overlay is labeled `EXCESS_EXECUTION`, clean training data are checked for naturally occurring action-plus-background overlap using a frozen training-only rule.

If the same background-behavior class is already an ordinary component of clean commanded execution, it is **not** labeled excess. It is retained as a hard clean/concurrency control.

This prevents routine concurrency from being mislabeled as a contract violation.

`EXCESS_EXECUTION` is permitted to support a Level-A claim only if the dedicated composition artifact audit in Section 25 is feasible and passes.

## 24.5 Replay or Late Execution

A pure replay of a valid execution can be mathematically indistinguishable from a genuine execution under the locked 20-feature representation because the features do not include absolute time, cryptographic state or packet sequence identifiers.

FedIEC therefore separates two cases.

### Detectable late / temporally misaligned execution

A valid held-out execution is shifted into a later `NO_ACTION` pseudo-event window with no immediately preceding matching intent. The detector is tested on whether valid-looking execution is inconsistent with the contemporaneous `(B,I=NO_ACTION)` contract.

The shifted execution must satisfy the same frozen session/day matching, B-context caliper, boundary-continuity and temporal-alignment requirements in Section 25. A donor that breaks an unresolved recipient-side flow or background rhythm is infeasible rather than an easy anomaly.

### Pure replay observability limit

If replay preserves the same 20-dimensional `E` representation and occurs under an indistinguishable `B`, the current representation contains no information with which to distinguish it from a valid execution.

Such cases are reported as:

```text
REPRESENTATION_UNOBSERVABLE
```

and cannot support a replay-detection claim.

FedIEC must never imply cryptographic or sequence-aware replay detection unless additional observables are explicitly added before protocol lock.

---

# 25. Two-Level Violation Evaluation

Violation evaluation has two clearly separated levels.

## Level A — Artifact-Controlled Contract Counterfactuals

Mandatory.

Generated only from held-out observations and raw captured windows.

No counterfactual is created by directly concatenating already-extracted feature vectors.

A generated counterfactual is eligible for a semantic claim only when its **family-specific transformation audit** passes.

### 25.1 Frozen Counterfactual Metadata

Before donor assignment, every eligible held-out clean interaction receives the following metadata from clean capture material:

```text
physical device
manufacturer/category/topology metadata
session ID and collection day
semantic intent
physical pre-state and observed post-state where available
transition class induced by the action from that pre-state
pre-action B feature vector
raw B→E boundary-continuity signature
active raw transport-flow summary around t_I
capture timestamp-resolution metadata
background-activity stratum where applicable
```

These metadata are used for matching and artifact checks only. Raw identifiers and transport state do not enter the learned contract representation.

### 25.2 Frozen B-Context Distance and Common-Support Caliper

The **distance definition** is frozen during the excluded pilot.

After the chronological split, the numerical caliper is computed from the clean **training partition only**.

For each device, use the transformed/standardized `B` representation and compute a training-only nearest-neighbor distance distribution among observations satisfying the same locked physical-state/topology compatibility rules used by the relevant counterfactual family.

Define:

```math
c_i = Q_{0.95}(d_{B,\mathrm{NN}})
```

where `c_i` is the device-specific common-support caliper.

A donor is admissible only when:

```math
d_B(B_{recipient}, B_{donor}) \le c_i
```

A nearest donor **outside** the caliper is not accepted merely because it is the closest available observation.

If the training partition cannot support a stable device-specific caliper under the frozen minimum-support rule, that device/family is marked insufficient for Level-A counterfactual generation rather than borrowing held-out information.

### 25.3 Deterministic Session/Day Matching Hierarchy

The phrase `where feasible` is not permitted in donor matching.

Every main-suite donor must satisfy the following hierarchy in order:

```text
Tier 1: same physical device + same session
Tier 2: same physical device + different session on the same collection day
Tier 3: same physical device + adjacent collection day with |Δday| = 1
Otherwise: NO_VALID_COUNTERFACTUAL
```

At every tier, the donor must also satisfy:

```text
same network-control topology
family-specific physical-state/transition compatibility
B-context distance within the frozen device caliper
B→E boundary-continuity compatibility
all split/provenance rules
```

The algorithm always chooses the **lowest available tier first**. Within a tier it minimizes the frozen B-context distance, with deterministic tie-breaking from a pre-registered generation seed.

No donor search is expanded to more distant days after seeing model scores or after a family performs poorly.

The selected tier is recorded for every generated observation and reported by device and violation family.

### 25.4 Transition-Semantics Compatibility

For `SUBSTITUTION`, simple physical feasibility is insufficient.

Let the recipient physical pre-state be `S_r`, the declared action be `I_r`, and the substituted action be `I_s`.

The donor execution must have been generated from a donor pre-state equivalent to `S_r` for `I_s` so that:

```text
transition_class(donor execution under I_s)
=
transition_class(I_s applied to recipient pre-state S_r)
```

Thus state-changing and state-maintaining signatures are never transplanted into a recipient context in which that substituted action would have the opposite transition semantics.

Impossible or transition-mismatched candidates are recorded as:

```text
COUNTERFACTUAL_INFEASIBLE_TRANSITION
```

They are not used as easy anomalies.

### 25.5 B→E Boundary-Continuity Rule

Similarity of aggregate `B` features alone is not enough.

A frozen raw boundary descriptor is computed in a pilot-locked neighborhood around `t_I`. It summarizes only matching metadata needed to detect discontinuities, including where observable:

```text
whether target-device flows remain active across the boundary
transport protocol and connection-state class
recent packet-direction/activity pattern
endpoint/flow continuity class
presence of a background burst that begins in B and continues into E
```

The descriptor is never a model input.

If recipient `B` contains an unresolved target-device flow or multi-part background activity crossing `t_I`, the donor `E` must provide a compatible continuation under the frozen rule. Otherwise the transformation is:

```text
COUNTERFACTUAL_INFEASIBLE_BOUNDARY
```

This prevents the detector from exploiting an artificial disappearance or appearance of a session/background rhythm at the splice boundary.

### 25.6 Temporal-Boundary Alignment Rule

Donor executions are transformed at the raw timestamp/packet-window level.

When an execution is translated to a new pseudo-intent time:

```text
preserve all internal packet offsets
preserve donor execution duration
preserve relative first-packet latency unless the violation definition explicitly changes timing
preserve internal packet order
recompute all inter-arrival and latency features after transformation
never splice only aggregate feature vectors
never repair an infeasible transform by arbitrary epsilon timestamp jitter
```

These checks prevent discontinuities at `t_I` or transformation mechanics from becoming the detection signal.

### 25.7 Donor Assignment, Reuse and Dependence

Counterfactual generation uses deterministic matching manifests.

Within each violation family and each artifact-audit family:

```text
a clean interaction cannot be both recipient and donor for the same generated observation
donor reuse is capped at one use per family whenever a valid one-to-one assignment exists
if exact one-to-one assignment is impossible, the pre-registered maximum reuse cap is applied and recorded
a donor is never duplicated merely to increase sample count
```

The implementation uses deterministic minimum-cost matching under the frozen tier/caliper constraints rather than independent greedy sampling when this changes donor reuse.

Every generated observation records all source clean interaction IDs.

For inferential analyses that pool generated observations, create a `source_dependency_cluster` by linking any derived observations that share a source clean interaction. Connected components of this source-sharing graph are resampled together in the hierarchical analysis in Section 66.

This prevents donor reuse or counterfactual multiplication from inflating the effective sample size.

### 25.8 EXCESS_EXECUTION Physical-Timeline Composition Rule

`EXCESS_EXECUTION` is the only mandatory family that **composes two packet timelines** rather than replacing/translating one execution.

The composition algorithm therefore has an additional frozen validation layer.

The background donor is aligned using the pilot-locked active-background pseudo-event rule; its internal timing is preserved. After alignment, the raw timelines are merged only if all Section 24.4 physical-timeline checks pass.

Mandatory pre-feature diagnostics include:

```text
new exact-timestamp collision count and rate
new ultra-short inter-arrival count and rate
minimum positive inter-arrival by direction
shared active transport-flow count
TCP sequence/acknowledgment compatibility where a shared TCP flow exists
packet-order preservation for each source component
raw-timeline feasibility-check status
```

The collision/short-gap diagnostics are compared with frozen clean training-derived natural envelopes. They are quality-control diagnostics only and are not detector inputs.

A candidate outside the locked natural envelope is rejected, not clipped or jittered.

### 25.9 Artifact Audit A — Replacement/Translation Transformations

This audit covers transformation mechanics used by:

```text
OMISSION
SUBSTITUTION
UNCOMMANDED_EXECUTION
TEMPORALLY_MISALIGNED_EXECUTION
```

Construct **semantic-preserving replacement/translation controls** by pairing a recipient `(B,I)` with a different held-out execution of the **same intended action**, using exactly the same tier, state/transition, B-caliper, boundary-continuity and temporal-alignment rules used for violation generation.

A dedicated artifact classifier attempts to distinguish:

```text
genuine clean held-out interactions
versus
semantic-preserving replacement/translation controls
```

using the same final 20 execution features but without the intent label.

### 25.10 Artifact Audit B — EXCESS Composition

Passing Audit A does **not** validate `EXCESS_EXECUTION`.

A separate composition audit must exercise the same two-timeline merge path used by `EXCESS_EXECUTION`.

The preferred semantic-preserving control compares:

```text
genuine clean commanded interactions containing naturally observed legitimate action+background concurrency
versus
synthetically recomposed legitimate action+background controls
```

The synthetic controls use a background-behavior class that the training-only natural-concurrency rule has explicitly designated as **allowed clean concurrency**, not as excess.

Genuine and synthetic composites are matched by:

```text
device
action
recipient pre-state / transition semantics
session/day tier
B-context caliper
background-activity class
boundary-continuity class
```

The identical EXCESS merge, serialization and feasibility checker is used.

A deterministic empty-donor/no-op round-trip test is also mandatory: applying the composition pipeline with no added packets must reproduce the original extracted feature vector exactly. This is a code-integrity check, not a substitute for the composition artifact audit.

If there are insufficient naturally concurrent clean controls to run Audit B for a device, `EXCESS_EXECUTION` on that device is labeled:

```text
ARTIFACT_AUDIT_INSUFFICIENT
```

and cannot support a Level-A EXCESS claim. Physically realized Level-B excess-like mechanisms remain eligible if independently grounded.

### 25.11 Frozen Artifact-Audit Pass Criterion

For each artifact-audit family separately, define orientation-free artifact detectability:

```math
A^*=\max(AUROC,1-AUROC)
```

with frozen tolerance:

```math
\delta_{artifact}=0.10
```

The audit passes only if all conditions hold on held-out audit data:

```text
upper bound of the 95% hierarchical CI for A* <= 0.60
no individual-device A* > 0.70
no single final model feature has pooled univariate A* > 0.65
all mandatory raw-timeline feasibility diagnostics pass
```

This is an equivalence-style artifact criterion: the protocol must provide evidence that transformation detectability is close to chance within the pre-registered tolerance. Merely obtaining a non-significant difference or a confidence interval that happens to include 0.50 is insufficient.

If any criterion fails, the corresponding transformation family is considered detectably artificial and must be corrected **before** confirmatory violation results for that family are interpreted.

Audit thresholds and repair rules are fixed before main contract results are inspected.

### 25.12 Mandatory Level-A Constructions

```text
OMISSION: correct intent + matched legitimate NO_ACTION execution
SUBSTITUTION: correct intent + transition-compatible opposite-action execution
UNCOMMANDED_EXECUTION: NO_ACTION + matched legitimate action execution
EXCESS_EXECUTION: correct action execution + physically feasible active legitimate NO_ACTION background composition
REPLAY_OR_LATE_EXECUTION: valid execution shifted into a later matched NO_ACTION window
```

Training data remain untouched.

These observations evaluate the **contract mechanism** and are called:

```text
contract counterfactuals
```

not:

```text
cyberattacks
malware
real compromises
```

## Level B — Physically Induced Violations

Mandatory for the final confirmatory chapter unless a scenario is impossible across every eligible device for a documented technical reason.

The study must realize at least **three pre-registered physical control-path violation mechanisms**, and at least **two distinct mechanisms must produce analyzable observations on at least three core devices**.

Priority mechanisms are:

```text
command delivery interruption / blocked command
secondary-controller or out-of-band action
uncommanded physical state change where safely reproducible
delayed command execution
rapid contradictory command
```

Only scenarios reproducible without unsafe modification of devices are included.

These experiments determine whether the contract formulation survives outside recombined traces.

A failure to realize the minimum physical set narrows the chapter to mechanism/benchmark claims and blocks broad security-relevance wording.

---

# 26. Real-Attack Claim Boundary

A contract counterfactual is never called an attack.

A physically induced control-path failure is not automatically called malware.

A real-attack claim requires:

```text
actual attack activity
+
known legitimate intent
+
known attack-active interval
+
isolatable target-device execution

```

If these conditions cannot be established:

> FedIEC makes no real-attack detection claim.

---

# 27. External Dataset 1 — PingPong

PingPong is the first external validation candidate because it provides:

```text
physical smart-home devices
official Android companion applications
trigger timestamps
device-event network traces
multiple device functionalities
natural physical devices

```

The external evaluation uses only devices for which the semantic action can be mapped independently and unambiguously to:

```text
TURN_ON
TURN_OFF

```

No action is inferred from network traffic.

PingPong is not treated as a novel dataset contribution of FedIEC.

Its role is independent replication.

---

# 28. PingPong Eligibility

A PingPong physical device is eligible only when:

1. the device has clearly documented ON and OFF triggers;
2. the trigger order/timestamps can distinguish ON from OFF;
3. official Android-app interaction generated the relevant traffic;
4. sufficient valid captures remain for evaluation;
5. device identity is unambiguous;
6. training and evaluation traces can be separated without overlap.

All eligible devices are used.

No performance-based device selection is allowed.

---

# 29. External Dataset 2 — TU Wien Philips Hue

The TU Wien Philips Hue dataset remains a useful large-scale mechanism dataset.

It contains repeated labeled ON/OFF captures.

Its revised role is:

```text
large-sample replication of action-conditioned consistency

```

rather than proof of federated heterogeneity.

It tests whether the contract formulation remains valid under thousands of repeated executions of the same physical-device family.

It does not establish multi-device federation by itself.

---

# 32. Public-Dataset Failure Rule

Failure of an external dataset does **not** invalidate FedIEC.

The mandatory controlled benchmark supplies the core evidence.

External datasets may fail because of:

```text
ambiguous intent labels
insufficient ON/OFF samples
uncertain mobile trigger provenance
incompatible capture boundaries
missing physical-device identity
licensing/access limitations

```

Eligibility rules are never weakened because an external dataset would otherwise be unusable.

---

# 33. Optional Real-Attack Dataset

CIC IoT 2022 or another suitable dataset may be used only if the following can be established directly:

1. intended legitimate action;
2. corresponding physical device;
3. intent timestamp or bounded interval;
4. attack-active interval;
5. target-device execution during that interval.

If any condition is missing, the dataset cannot support the real-attack claim.

---

# 34. Unit of Analysis

The basic contract observation is:

```math
(B,I,E)
```

where:

```text
B = pre-intent network context
I = independently observed mobile intent
E = post-intent device execution
```

Every observation additionally carries non-feature metadata required for dependence-aware analysis:

```text
device_id
manufacturer
category
network_topology
session_id
collection_day
interaction_id
background_activity_stratum if NO_ACTION
physical pre-state/post-state where observable
```

For `NO_ACTION`:

```text
I = NO_ACTION
```

with a pseudo-event timestamp selected under the locked stratified-background rule.

Packets/interactions are not treated as independent inferential replicates. Device and session structure is preserved through all statistical analysis.

---

# 35. Network Attribution

Only packets attributable to the target IoT endpoint are included in the model features.

The following are retained only as metadata and never used as learned features:

```text
IP address
MAC address
device name
manufacturer
model name
hostname
domain string
application package
client ID

```

This prevents device or vendor memorization from becoming the detection mechanism.

---

# 36. Fixed Network Feature Set

Every observation window produces exactly 20 network-execution features:

1. total packet count;
2. outbound packet count;
3. inbound packet count;
4. total bytes;
5. outbound bytes;
6. inbound bytes;
7. mean outbound packet size;
8. standard deviation of outbound packet size;
9. mean inbound packet size;
10. standard deviation of inbound packet size;
11. mean packet inter-arrival time;
12. standard deviation of packet inter-arrival time;
13. median packet inter-arrival time;
14. 95th-percentile packet inter-arrival time;
15. fraction of TCP packets;
16. fraction of UDP packets;
17. number of unique remote endpoints;
18. number of unique remote transport ports;
19. latency from observation-window start to first target-device packet;
20. active span between first and last target-device packet.

If no target-device packet occurs:

```text
packet/byte counts = 0
active span = 0
first-packet latency = W
```

The same definition is used for pre- and post-action windows.

## Feature-Scope Boundary

These features intentionally exclude:

```text
absolute wall-clock time
packet payload
IP/MAC identity
manufacturer/device identity
DNS/domain strings
TCP sequence numbers
application-layer command tokens
cryptographic state
```

Therefore pure replay that preserves the 20-feature representation may be unobservable and must be treated according to Section 24.5.

### Raw-Metadata Quality-Control Boundary

Fields excluded from the contract model may still be inspected **offline and deterministically** for counterfactual validity. In particular, raw 5-tuples, TCP sequence/acknowledgment state, packet timestamps and capture-resolution metadata may be used only to:

```text
validate B→E boundary continuity
validate transition/capture provenance
reject physically impossible EXCESS compositions
detect synthetic timestamp/flow artifacts
reproduce transformation manifests
```

They are never supplied to the learned detector, threshold rule, contract score, model-selection procedure or main evaluation features.

## Protocol-Mismatch Risk

Features 15–18 can encode transport/topology differences rather than semantic action effects. They remain in the locked main representation because protocol usage is part of real network execution, but every cross-device transfer result must be stratified by the topology metadata from Section 14 and accompanied by the protocol-feature ablation in Section 72.

Reviewers must be able to distinguish:

```text
semantic transfer failure
from
trivial transport/topology mismatch
```

---

# 37. Contract Representation

For each observation:

```math
B \in \mathbb{R}^{20}
```

and:

```math
E \in \mathbb{R}^{20}
```

Intent is represented as a three-state context:

```text
NO_ACTION
TURN_ON
TURN_OFF

```

using a fixed one-hot representation.

The main conditional context is therefore:

```math
C=[B,I]
```

and the target is:

```math
E
```

No raw identifier enters `C`.

---

# 38. Invalid Interaction Rule

An observation is removed before splitting if:

```text
intent timestamp missing
intent ambiguous
target device ambiguous
capture corrupted
capture overlaps another controlled action
device disconnects unexpectedly before the interaction
capture clock synchronization fails
traffic attribution fails
action is not one of the locked semantic actions

```

Exclusion counts and reasons are published.

An interaction is not removed because it is difficult for the model.

A clean held-out interaction may remain in the benchmark but be ineligible for one specific Level-A violation family. Counterfactual ineligibility is recorded using a frozen reason such as:

```text
NO_VALID_COUNTERFACTUAL
COUNTERFACTUAL_INFEASIBLE_TRANSITION
COUNTERFACTUAL_INFEASIBLE_BOUNDARY
COUNTERFACTUAL_INFEASIBLE_PHYSICAL_TIMELINE
ARTIFACT_AUDIT_INSUFFICIENT
```

Such observations are not silently discarded and are never replaced with looser matching rules after results are observed.

---

# 39. Feature Transformation

Non-negative magnitude features receive:

```math
x'=\log(1+x)
```

where appropriate.

Rate/fraction features are not log transformed.

## Shared Training-Client Normalization

The main confirmatory protocol uses **one training-population scaler per training fold**, not per-client test-time normalization.

For each feature, the scaler statistics are computed exclusively from the union of the **training partitions of the currently eligible training clients**.

In the federated regime, the required sufficient statistics are aggregated without pooling raw windows. In centralized analysis, the exact same resulting scaler is used. The local-model baseline also receives the same shared scaler, making the local comparison conservative because local models obtain common preprocessing statistics but no other clients' training examples.

Continuous features are standardized as:

```math
z=\frac{x-\mu_{train\_clients}}{\sigma_{train\_clients}}
```

Calibration and test observations never influence the scaler.

For leave-one-device-out evaluation, the scaler is recomputed using only the retained training clients. The held-out device contributes **no** training, calibration or test statistics to the zero-shot scaler.

This rule eliminates the zero-shot normalization paradox and target-domain leakage.

A secondary sensitivity analysis may compare shared z-score scaling with a training-only robust quantile/rank transform, but it cannot replace the locked main scaler after results are observed.

---

# 40. Main Contract Model

The primary model is a **conditional normalizing flow** estimating:

```math
p(E\mid B,I)
```

The context vector contains:

```text
20 pre-action features
+
3-dimensional intent context

```

The transformed variable contains:

```text
20 post-action execution features

```

The contract score is:

```math
s_{\text{contract}}(E,B,I) = -\log p(E\mid B,I)
```

Higher scores indicate greater contract inconsistency.

---

# 41. Model Architecture

The primary conditional flow uses:

```text
20-dimensional execution target
23-dimensional conditioning context
6 affine coupling blocks
alternating feature masks
2 hidden layers per conditioner
64 hidden units per layer
ReLU activations
bounded scale output
standard multivariate Gaussian base distribution

```

The architecture is frozen before confirmatory execution.

No architecture search is performed on test performance.

---

# 42. Training Configuration

All neural experiments use:

```text
optimizer = Adam
learning_rate = 1e-3
batch_size = 64
weight_decay = 0
gradient_norm_clip = 5
dtype = float32
training_seeds = 0..9

```

No test-dependent scheduler or early stopping is allowed.

Training duration is fixed before confirmatory execution.

---

# 43. Required Baseline 1 — Execution Only

The first baseline estimates:

```math
p(E\mid B)
```

The intent context is removed.

Its anomaly score is:

```math
s(E,B)=-\log p(E\mid B)
```

This baseline tests whether the mobile-side intent contributes information beyond network context alone.

---

# 44. Required Baseline 2 — Old FedIEC Formulation

The second baseline estimates:

```math
p(E\mid I)
```

without the pre-action context.

This baseline is especially important because it corresponds to the original FedIEC formulation.

It tests whether the revised contract formulation provides information beyond merely conditioning execution on an action label.

---

# 45. Required Baseline 3 — Direct Action Classification

A discriminative model estimates:

```math
P(I\mid B,E)
```

The inconsistency score is:

```math
1-P(I\mid B,E)
```

for the declared action.

This tests the simpler interpretation:

> Infer what action the traffic resembles and compare it with the declared intent.

The classifier is evaluated on the **same complete test suite** as the contract model, not only on easy closed-set substitutions.

Mandatory reporting includes:

```text
AUROC and AUPRC overall
AUROC/AUPRC per violation type
clean FPR at the locked threshold
FPR for BACKGROUND_SILENT
FPR for BACKGROUND_LOW_ACTIVITY
FPR for BACKGROUND_ACTIVE_BURST
performance on EXCESS_EXECUTION
performance on temporally misaligned execution
calibration error / Brier score on genuine clean action labels
```

This prevents a closed-set action classifier from appearing sufficient merely because it recognizes ON versus OFF while remaining overconfident on background or composite executions.

FedIEC may not claim that probabilistic contract modeling is superior unless the full evidence supports that statement.

---

# 46. Required Baseline 4 — Per-Action One-Class Model

Train a simple one-class detector independently for:

```text
TURN_ON
TURN_OFF
NO_ACTION

```

using the same fixed execution representation.

The default baseline is:

```text
One-Class SVM

```

This approximates a conventional command/event-conditioned behavioral detector without federation-specific contract modeling.

---

# 47. Required Baseline 5 — Simple Statistical Contract

For every action context, estimate a training-only multivariate statistical profile.

Use a shrinkage covariance estimator and Mahalanobis-style score.

This establishes whether a deep conditional density model is necessary at all.

---

# 48. Required Learning Regimes

The primary contract model is evaluated under three regimes.

## Local

Each physical-device client trains exclusively on its own training observations.

## Centralized

All eligible training observations are pooled.

Calibration and test observations are excluded.

## Federated

Each physical device is one client.

The server aggregates model updates with FedAvg.

The same architecture and optimizer are used in all three regimes.

---

# 49. Federated Configuration

The main FL configuration is:

```text
client = physical IoT device
aggregation = FedAvg
weighting = local training sample count
participation = all eligible clients
local_epochs = 1
communication_rounds = 100
batch_size = 64
seeds = 0..9
normalization = shared training-client scaler from Section 39
```

No client is removed because of poor performance.

No alternative aggregation rule is introduced after seeing results.

The main study is deliberately a small cross-device/cross-gateway federation over real physical clients; it does not claim massive-client scalability.

---

# 50. Why FedAvg Remains the Main Aggregator

The scientific question is not:

```text
Which FL optimizer maximizes accuracy?
```

The main question is whether execution-contract knowledge can be collaboratively learned across real heterogeneous physical devices and whether collaboration provides value when local contract data are limited.

FedAvg therefore remains the fixed reference aggregator.

FedProx, FedYogi, Ditto, FedBN, clustered FL, or other alternatives are outside the confirmatory study.

This prevents the novelty from drifting into optimizer comparison.

If heterogeneous contract learning fails, alternative FL methods may be discussed as future work, but they are not introduced post hoc to rescue confirmatory performance.

---

# 51. Training-Budget Comparability and Local-Data Scarcity

For the full-data comparison use:

```text
local model = 100 epochs
centralized model = 100 epochs
federated model = 100 rounds × 1 local epoch
```

This preserves approximate exposure parity.

Final-round parameters are used.

Test performance is never used for checkpoint selection.

## Mandatory Data-Scarcity Collaboration Curve

To determine whether federation contributes scientifically rather than merely reproducing a centralized-style model over distributed clients, repeat the local-versus-federated comparison using nested training budgets per device **and per semantic context**:

```text
n = 10
n = 30
n = 60
n = 90
```

The subset rule is frozen before evaluation and preserves session diversity through deterministic session-stratified sampling from the training partition only.

For every budget report:

```text
local AUROC/AUPRC
federated AUROC/AUPRC
paired federation-minus-local effect
per-device effect
communication cost
```

The full `n=90` condition remains the confirmatory comparison. The scarcity curve is a mandatory secondary analysis supporting only claims that explicitly reference data scarcity.

---

# 52. Calibration Threshold

Threshold selection is not a research variable.

For a trained detector and client:

```math
\tau_i = Q_{0.95}(S_{i,\text{cal}})
```

where calibration scores come exclusively from **clean genuine contracts**.

Violation samples never influence thresholds.

Threshold-free metrics remain primary.

---

# 53. Zero-Shot Threshold and Normalization Rule

During true leave-one-device-out evaluation, no data from the held-out physical device may determine either:

```text
model parameters
normalization/scaling statistics
main zero-shot calibration threshold
```

For each held-out device `k`:

```text
scaler = computed only from retained clients' training partitions
threshold = computed only from retained clients' clean calibration scores
```

The held-out device's test data are transformed using that training-client scaler without adaptation.

A separate secondary experiment may allow:

```text
held-out-device benign calibration only
```

for threshold adaptation after the global scaler and model are already frozen.

This is explicitly reported as:

**calibration-only adaptation**

and must not be confused with zero-shot transfer.

No held-out-device feature normalization is allowed even in this secondary calibration-only adaptation unless it is declared as a separate target-adaptation experiment outside the zero-shot claim.

---

# 54. Primary Metrics

Primary detection metrics are:

```text
AUROC
AUPRC

```

for:

```text
clean genuine contracts
versus
contract violations

```

They are reported:

```text
overall
per violation type
per physical device
per semantic action

```

---

# 55. Direct Contract Metric

For every clean execution:

```math
(B,I,E)
```

construct valid counterfactual contracts where applicable.

Report the fraction satisfying:

```math
s(E,B,I) < s(E,B,\tilde I)
```

for an incorrect intent:

```math
\tilde I
```

and equivalent paired checks for omission/uncommanded relations.

This directly tests whether the correct contract receives the lower anomaly score.

---

# 56. Threshold-Based Metrics

At the fixed calibration threshold report:

```text
Macro-F1
Balanced Accuracy
TPR
FPR
Precision

```

These are secondary to AUROC and AUPRC.

---

# 57. Violation Coverage

Report performance separately for:

```text
OMISSION
SUBSTITUTION
UNCOMMANDED_EXECUTION
EXCESS_EXECUTION
REPLAY_OR_LATE_EXECUTION
```

Within `REPLAY_OR_LATE_EXECUTION`, separate:

```text
TEMPORALLY_MISALIGNED_EXECUTION
PURE_REPLAY_REPRESENTATION_LIMIT
```

A strong aggregate metric cannot hide failure on one violation category.

For every family report:

```text
number feasible
number infeasible and frozen reason
matching-tier distribution
B-context distance distribution relative to the frozen caliper
donor-reuse distribution and source-dependency-cluster count
family-specific artifact-audit status
AUROC
AUPRC
TPR at locked threshold
per-device results
physical-realization status where applicable
```

A representation-unobservable pure replay is a valid negative finding and is never counted as a detected family.

---

# 58. Clean False-Alarm Analysis

For every physical client report:

```text
clean FPR
clean score distribution
95th-percentile threshold
```

For `NO_ACTION`, report FPR separately for:

```text
BACKGROUND_SILENT
BACKGROUND_LOW_ACTIVITY
BACKGROUND_ACTIVE_BURST
```

Across clients report:

```text
macro-average FPR
median FPR
worst-client FPR
P10 detection performance
CV(FPR)
```

Also report FPR by network-topology group.

This keeps the study aligned with heterogeneous-device fairness concerns and directly checks that the model has not learned a trivial silence-versus-activity rule.

---

# 59. Contract Heterogeneity Analysis

For each semantic context:

```text
NO_ACTION
TURN_ON
TURN_OFF
```

quantify how execution distributions differ across physical clients.

At minimum report pairwise:

```text
Wasserstein distance
energy distance
```

on the shared training-client standardized representation.

Also report:

```text
action separation within each client
within-manufacturer versus cross-manufacturer distances
within-topology versus cross-topology distances
protocol-feature distances for features 15–18
data-scarcity federation benefit versus heterogeneity
```

This allows interpretation of:

```text
when federation helps
when federation hurts
which devices share semantics
which devices remain distributionally distinct
whether transfer failures are semantic or protocol-driven
```

No new heterogeneity metric is invented unless required.

---

# 60. Cross-Device and Cross-Manufacturer Generalization

## Leave-One-Device-Out — Main Zero-Shot Protocol

For every device `k`:

1. remove all observations of device `k` from model training;
2. remove all observations of device `k` from normalization-statistic computation;
3. remove all observations of device `k` from training-client calibration;
4. federatively train on the remaining devices;
5. compute the shared scaler from retained training clients only;
6. compute the main zero-shot threshold from retained training-client calibration only;
7. evaluate clean and violated contracts on device `k` without target adaptation.

Repeat until every physical device has been held out once.

This is genuine unseen-physical-device evaluation.

## Topology-Stratified Interpretation

Every held-out result is labeled by the held-out device's network-control topology.

Report separately:

```text
within-topology transfer
cross-topology transfer
LOCAL_WLAN holdouts
CLOUD_MEDIATED holdouts
HYBRID_OR_OTHER holdouts where present
```

A transfer failure dominated by transport/topology mismatch must not be described as proof that semantic contracts do not transfer.

## Protocol-Feature Sensitivity

Repeat leave-one-device-out evaluation without features 15–18:

```text
TCP fraction
UDP fraction
unique remote endpoints
unique remote ports
```

This is a mandatory pre-registered ablation used to determine whether cross-device results are driven by protocol identity.

## Leave-One-Manufacturer-Out

With at least three manufacturers, perform a secondary leave-one-manufacturer-out evaluation whenever the remaining training fold contains at least three physical clients and at least two manufacturers.

All devices from the held-out manufacturer are excluded from training, scaling and threshold construction.

This analysis is reported separately from leave-one-device-out and supports only manufacturer-transfer claims.

---

# 61. External Cross-Device Validation

Where PingPong data permit, repeat the same concept across an independent collection.

The purpose is not to pool incompatible datasets.

The purpose is to ask:

> Does the same intent–execution contract formulation remain meaningful outside the controlled FedIEC environment?

External results are reported separately from the core benchmark.

---

# 62. Physically Induced Violation Evaluation

Physical control-path violations are **mandatory security-relevance evidence**, not an optional embellishment.

Before confirmatory modeling, pre-register at least three technically plausible mechanisms from:

```text
command delivery interruption / blocked command
secondary-controller command
uncommanded state change
delayed command execution
rapid contradictory command
temporary network interruption
```

At least two distinct mechanisms must yield analyzable observations on at least three core physical devices for the chapter to make the physically realized security-relevance claim.

Each scenario records:

```text
intended mobile action
actual intervention
physical pre-state
physical post-state where observable
device identity
manufacturer/category/topology
session ID
intervention timestamp
network capture
expected contract effect
whether the scenario corresponds to omission/substitution/uncommanded/excess/late semantics
```

The same frozen clean-trained detector, scaler and threshold are used.

No retraining or threshold tuning on induced violations is permitted.

If a pre-registered mechanism is technically impossible on a device, the failure is recorded and does not justify substituting a new easier mechanism after observing scores.

---

# 63. Real-Attack Evaluation

If a valid attack-aligned dataset is available, evaluate:

```text
clean execution under known intent
versus
attacked execution under the same known intent

```

The primary score remains:

```math
-\log p(E\mid B,I)
```

Metrics:

```text
AUROC
AUPRC
TPR at fixed threshold
detection delay if temporally meaningful

```

Real-attack results remain separate from counterfactual and induced-failure results.

---

# 64. Systems Metrics

For federated training report:

```text
number of rounds
convergence curve
model parameter count
model size
bytes transmitted per client
total transmitted bytes
wall-clock training time

```

No unsupported claims are made about:

```text
battery consumption
Android inference latency
microcontroller feasibility
embedded-device RAM
energy consumption

```

unless those quantities are directly measured.

---

# 65. Statistical Unit and Dependence Structure

Training seeds are **not independent experimental units**.

They measure optimization variability only.

For genuine physical observations, the dependence hierarchy is:

```text
physical device
  └── collection session/day
       └── interaction / contract observation
            └── repeated model-seed predictions
```

For generated Level-A counterfactuals, each observation may depend on more than one clean source interaction. Every generated row therefore records:

```text
recipient_source_id
donor_source_id(s)
artifact/control family
generation_family
source_dependency_cluster
```

The `source_dependency_cluster` is the connected component obtained by linking generated observations that share any clean source interaction.

Primary uncertainty must never treat multiple derivatives of one source interaction as independent evidence.

For every method:

1. preserve predictions for every interaction and seed;
2. compute seed-specific metrics to describe training variability;
3. aggregate genuine-observation effects with paired hierarchical resampling over devices → sessions → interactions;
4. aggregate counterfactual effects with paired hierarchical resampling over devices → sessions → `source_dependency_cluster`;
5. keep all method comparisons paired on the same resampled evidence units;
6. report per-device effects in addition to the population summary;
7. report the number of unique physical source interactions underlying every pooled counterfactual result.

Seed-only confidence intervals or seed-only Wilcoxon tests are not permitted as the primary inferential analysis.

Generated sample count is never reported as though it were the number of independent physical observations.

---

# 66. Statistical Procedure

For each of the three confirmatory comparisons report:

```text
paired effect estimate
95% paired hierarchical bootstrap confidence interval
paired cluster-aware randomization/permutation p-value
effect distribution across training seeds
per-device effect
unique-source count for every counterfactual-based result
```

For genuine physical observations, the hierarchical bootstrap resamples:

```text
1. physical devices
2. sessions within resampled devices
3. interactions within resampled sessions
```

For generated Level-A counterfactual observations, the third level is replaced by:

```text
3. source_dependency_clusters within resampled sessions
```

All derived observations inside a selected source-dependency cluster are carried together.

The evaluation metric is recomputed from the resampled evidence units.

Model seeds remain nested repeated realizations and are averaged within each bootstrap replicate for the primary estimand; the full seed spread is reported separately.

Use:

```math
\alpha=0.05
```

Holm correction is applied across the three confirmatory hypothesis comparisons.

For small-sample sensitivity, also report an unadjusted device-level paired sign/permutation analysis without treating it as a replacement for the hierarchical result.

For artifact audits, use the same dependence-aware hierarchy but evaluate the pre-registered equivalence-style `A*` criterion from Section 25 rather than substituting a null-hypothesis failure-to-reject argument.

No new significance test is introduced after results are inspected.

---

# 67. Confirmatory Comparison 1 — Intent Value

Compare:

```math
p(E\mid B,I)
```

versus:

```math
p(E\mid B)
```

Primary outcome:

```math
\Delta AUROC
```

using the locked artifact-controlled contract-violation suite.

The primary effect and uncertainty are computed with the hierarchical procedure in Section 66.

Background-active `NO_ACTION` observations, replacement/translation controls and—where `EXCESS_EXECUTION` is included in the evaluated suite—composition controls must be included so the result cannot be explained by silence/activity or transformation artifacts.

---

# 68. Confirmatory Comparison 2 — Pre-Context Value

Compare:

```math
p(E\mid B,I)
```

versus:

```math
p(E\mid I)
```

Primary outcome:

```math
\Delta AUROC
```

This tests whether pre-action context contributes information beyond action conditioning after the settling-integrity and randomized-order controls prevent `B` from trivially encoding the previous command tail or deterministic next action.

The primary effect and uncertainty are computed with the hierarchical procedure in Section 66.

---

# 69. Confirmatory Comparison 3 — Federated Collaboration

Compare:

```text
federated full-contract model
```

against:

```text
client-local full-contract models
```

under the full `n=90` per-device/per-context training budget.

Primary outcome:

```math
\Delta AUROC
```

using the hierarchical procedure in Section 66.

## Mandatory Secondary Scarcity Analysis

Repeat the comparison at:

```text
n ∈ {10, 30, 60, 90}
```

per device and semantic context.

Report the federation-minus-local curve and an area-under-scarcity-curve summary.

A claim that federation is especially useful under local data scarcity requires the effect to be supported across the pre-registered scarcity levels; it cannot be inferred from the full-data comparison alone.

---

# 70. Centralized Comparison

Compare:

```text
federated full-contract model

```

against:

```text
centralized full-contract model

```

This comparison quantifies the federation penalty.

The federated model is not required to outperform centralized learning.

No superiority framing is used unless the data actually support it.

---

# 71. Discriminative Baseline Comparison

The action classifier is reported separately from the confirmatory family.

Compare:

```text
conditional contract likelihood
```

against:

```text
direct action recognition
```

using the complete evaluation suite:

```text
clean commanded interactions
all three NO_ACTION background strata
OMISSION
SUBSTITUTION
UNCOMMANDED_EXECUTION
EXCESS_EXECUTION
TEMPORALLY_MISALIGNED_EXECUTION
semantic-preserving artifact controls
```

Report not only aggregate AUROC but also clean/background FPR, AUPRC per violation family, and classifier calibration.

This answers:

> Is contract verification providing information beyond simply recognizing which action the traffic resembles, especially for open-set/composite executions?

If the classifier performs equivalently or better across this full suite, that result is reported directly.

---

# 72. Required Ablations and Robustness Analyses

The following analyses are pre-registered and mandatory.

## Remove Intent

```math
p(E\mid B,I) \rightarrow p(E\mid B)
```

## Remove Pre-Execution Context

```math
p(E\mid B,I) \rightarrow p(E\mid I)
```

## Remove Federation

```text
federated
→
local
```

## Remove Device Exposure

```text
standard participating-client evaluation
→
leave-one-device-out
```

## Remove Protocol-Identity Features

Remove features 15–18:

```text
TCP fraction
UDP fraction
unique remote endpoints
unique remote ports
```

and repeat leave-one-device-out evaluation.

## Intent-Provenance Robustness

Using the same frozen model and original captures, perturb only the recorded intent provenance:

```text
timestamp jitter: ±0.10W, ±0.25W, ±0.50W
logging delay: +0.10W, +0.25W, +0.50W
missing intent: true command relabeled as NO_ACTION for diagnostic evaluation
duplicate intent: duplicated same action within the locked refractory interval
```

For timestamp perturbations, `B` and `E` are re-extracted from raw capture around the perturbed timestamp; feature vectors are not manually edited.

Report performance degradation as a function of provenance error.

## Counterfactual Artifact Controls

Report separately:

```text
replacement/translation artifact audit
EXCESS composition artifact audit
per-feature artifact detectability diagnostics
raw-timeline EXCESS feasibility diagnostics
matching-tier/caliper diagnostics
source-dependency counts
```

A violation family whose required transformation-specific audit is infeasible or fails cannot be used to support a Level-A claim for that family.

No additional ablation becomes mandatory after test results are observed.

---

# 73. Benchmark Contribution Gate

The dataset contribution does **not** depend on model accuracy.

FedIEC-Contracts is considered a valid benchmark contribution if:

1. at least six physical devices pass eligibility;
2. at least three manufacturers and three device categories are represented;
3. network-control topology is recorded for every device;
4. every device has the required multi-session/multi-day coverage;
5. intent provenance is independent of evaluated network execution;
6. all required clean observations are collected;
7. timestamps are synchronized within the locked tolerance;
8. settling-integrity rules are satisfied;
9. `NO_ACTION` background strata meet their locked quotas;
10. no split overlap exists;
11. capture attribution is auditable;
12. all five counterfactual violation definitions are reproducible where observable;
13. the B-context metric, training-only caliper procedure and deterministic session/day hierarchy are frozen;
14. transition-semantics compatibility and B→E boundary-continuity checks are implemented and audited;
15. EXCESS raw-timeline physical-feasibility checks are implemented before feature extraction;
16. donor assignment/reuse rules and source-dependency manifests are frozen;
17. the replacement/translation artifact audit passes for every family relying on it;
18. the EXCESS composition audit passes wherever Level-A EXCESS is claimed;
19. artifact equivalence tolerances are fixed before main violation results are inspected;
20. metadata and generation scripts are documented;
21. infeasible transformations, exclusions and collection failures are disclosed rather than replaced by looser post-hoc matching.

A negative model result does not invalidate a correctly constructed benchmark.

---

# 74. Contract-Signal Claim Gate

The statement:

> Explicit mobile intent provides a useful network execution-consistency signal.

requires on the mandatory controlled benchmark:

1. median full-contract AUROC ≥ 0.70;
2. lower bound of the 95% hierarchical confidence interval > 0.50;
3. direct contract-consistency accuracy ≥ 0.70;
4. full-contract model outperforming the execution-only baseline in the confirmatory paired analysis;
5. every transformation-specific artifact audit required by the pooled violation suite passing its frozen criterion;
6. background-active `NO_ACTION` FPR reported and not hidden inside a pooled result.

If these conditions fail, the signal is reported as weak or unsupported.

---

# 75. Pre-Context Claim Gate

The statement:

> Modeling execution relative to preceding network context improves intent-conditioned verification.

requires against:

```math
p(E\mid I)
```

all of:

```text
median paired AUROC improvement >= 0.02
95% hierarchical paired confidence interval excludes 0
Holm-adjusted cluster-aware p < 0.05
settling-integrity audit passes
constrained-random action-order audit passes
```

If not satisfied, pre-action context remains an evaluated design choice rather than a claimed contribution.

---

# 76. Federated Learnability Claim Gate

The statement:

> Intent–execution contracts can be learned collaboratively across heterogeneous physical IoT clients.

requires:

1. at least six core physical clients included;
2. at least three manufacturers and three device categories represented;
3. successful execution in at least 8 of 10 predetermined training seeds;
4. federated median macro-AUROC ≥ 0.70;
5. all clients use the shared training-client normalization rule;
6. per-device results are reported, including topology metadata.

This claim does **not** require federation to outperform local learning.

---

# 77. Federated Benefit and Scarcity Claim Gate

The statement:

> Federation improves contract verification over isolated local learning.

for the full-data condition requires:

```text
median paired AUROC improvement >= 0.02
95% hierarchical paired confidence interval excludes 0
Holm-adjusted cluster-aware p < 0.05
```

The stronger statement:

> Federation is particularly useful when individual devices have limited contract data.

additionally requires the pre-registered `n ∈ {10,30,60,90}` scarcity curve to show a consistent positive federation-minus-local effect at the low-data levels with uncertainty reported.

Otherwise federation is described as:

```text
learnable but not beneficial
comparable
worse
or inconclusive
```

according to the evidence.

---

# 78. Centralized-Parity Claim Gate

The statement:

> Federated contract learning approaches centralized performance.

requires:

```math
|\text{median AUROC}_{FL} - \text{median AUROC}_{CEN}| \leq 0.03
```

alongside overlapping uncertainty consistent with the stated parity interpretation.

A non-significant superiority test alone does not establish parity.

---

# 79. Unseen-Device and Manufacturer Claim Gate

The statement:

> The learned contract semantics generalize to unseen physical IoT devices.

requires:

1. genuine leave-one-device-out evaluation;
2. no held-out-device data used for model training;
3. no held-out-device data used to compute normalization statistics;
4. no held-out-device calibration used for the main zero-shot threshold;
5. median held-out-device AUROC ≥ 0.70;
6. individual results reported for every held-out device;
7. topology-stratified results reported;
8. protocol-feature ablation reported.

Failure on one device remains visible.

A separate statement about **unseen-manufacturer transfer** is permitted only if the leave-one-manufacturer-out protocol in Section 60 is feasible and independently passes an equivalent AUROC ≥ 0.70 criterion without held-out-manufacturer training, scaling or calibration information.

---

# 80. Violation-Coverage Claim Gate

The statement:

> FedIEC detects multiple classes of intent–execution contract violation.

requires median AUROC ≥ 0.70 for at least three distinct pre-registered **observable** violation families, with the 95% hierarchical uncertainty reported.

A Level-A family counts toward this statement only if:

```text
its frozen matching/transition/boundary rules were satisfied
its required transformation-specific artifact audit passed
its effective evidence size is reported by unique source interactions/source-dependency clusters
no post-hoc donor-rule relaxation was used
```

For `EXCESS_EXECUTION`, the dedicated composition artifact audit must pass; success of the replacement/translation audit alone is insufficient.

Claims identify exactly which families satisfy the gate.

`PURE_REPLAY_REPRESENTATION_LIMIT` cannot be counted as a detected family unless the locked representation actually contains a differentiating observable.

No blanket claim is made for violation types that fail or are artifact-audit insufficient.

---

# 81. Physically Induced Security-Relevance Gate

The statement:

> The contract score responds to physically realized control-path anomalies.

requires:

```text
>= 2 distinct physically realized violation mechanisms
analyzable on >= 3 core physical devices
independent ground truth
frozen clean-trained model
frozen scaler and threshold
median AUROC >= 0.70 for each claimed physical mechanism
```

Counterfactual violations cannot satisfy this gate.

If the minimum physical mechanism coverage is not achieved, the final work may still claim the contract formulation and counterfactual benchmark contribution but must not generalize those results to physically realized security anomalies.

---

# 82. Real-Attack Claim Gate

The statement:

> FedIEC detects attack-induced intent–execution divergence.

requires:

1. independently known legitimate intent;
2. actual attack activity;
3. attack/intent temporal alignment;
4. median AUROC ≥ 0.70;
5. median TPR ≥ 0.70 at the locked clean-calibration threshold.

Without these conditions, no real-attack claim is made.

---

# 83. Privacy Claim Boundary

The permitted statement is:

> Raw interaction traces remain at their originating client during federated training.

FedIEC does not claim formal privacy because the confirmatory study does not implement or evaluate:

```text
differential privacy
secure aggregation
homomorphic encryption
membership inference
gradient inversion
formal leakage bounds

```

Data locality is described as a structural property, not a formal privacy guarantee.

---

# 84. Threat Model

The main detector assumes:

```text
mobile intent log is trusted at collection time
gateway capture is trusted
training clients are benign
server follows FedAvg correctly
```

The main study detects divergence between intent and execution.

It does not defend against an attacker who simultaneously compromises:

```text
the intent-provenance source
and
the observed network execution
```

such that both are forged consistently.

That is an explicit trust boundary.

## Provenance Reliability Boundary

Trusted does not mean perfect.

The main clean benchmark requires intent timestamps within the locked synchronization tolerance, while the mandatory robustness analysis evaluates sensitivity to:

```text
timestamp jitter
logging delay
missing intent records
duplicate intent records
```

This characterizes operational brittleness of the provenance channel without redefining those perturbations as adversarial compromise.

---

# 85. Model-Stability Rule

A run fails only for numerical or execution failure such as:

```text
NaN loss
infinite loss
invalid parameters
unrecoverable training crash

```

Failed seeds remain recorded.

Seeds are not silently replaced.

If more than two of ten seeds fail for one method:

> The method is experimentally unstable under the locked configuration.

Hyperparameters are not changed to rescue confirmatory results.

---

# 86. Explicit Leakage and Confounding Prohibitions

The following are forbidden:

```text
randomly splitting repeated captures across train/test
normalization from held-out-device calibration/test data in zero-shot evaluation
normalization from any calibration or test observations in the main protocol
model selection using test AUROC
threshold selection from violations
threshold selection from attacks
using device identity as a learned feature
using manufacturer as a learned feature
using IP/MAC as a learned feature
using mobile payload contents as a feature
deriving intended action from target traffic
selecting clients based on model performance
selecting violation types after observing results
selecting successful seeds only
changing dataset priority after evaluation
altering violation generation after seeing detector scores
deterministic ON/OFF alternation in confirmatory collection
allowing prior command tails to overlap a later B window
feature-vector splicing for counterfactual generation
using impossible physical-state transitions as substitution counterfactuals
using a donor whose transition semantics are inconsistent with the recipient pre-state
relaxing the frozen B-context caliper because no convenient donor exists
searching beyond the frozen session/day matching hierarchy
using a nearest donor that lies outside common support
ignoring an unresolved B→E flow/background continuation mismatch
repairing timestamp collisions with arbitrary epsilon jitter
accepting an EXCESS merge that creates incompatible shared-flow/TCP state
accepting EXCESS timing artifacts outside the clean training-derived envelope
using the replacement/translation artifact audit as evidence that EXCESS composition is artifact-free
changing artifact-audit tolerances after viewing contract-model results
replicating or repeatedly reusing donors merely to increase sample count
failing to account statistically for generated observations sharing clean sources
sampling NO_ACTION almost exclusively from zero-traffic periods
silently dropping devices with protocol/topology mismatch
```

Any violation of these rules blocks the corresponding claim until corrected or explicitly downgraded.

---

# 87. Benchmark Integrity Rules

Every clean interaction records:

```text
interaction ID
device/manufacturer/category/topology
session/day
intent provenance
semantic action
pre/post physical state where observable
transition class
timestamp synchronization status
settling-rule status
raw capture reference
capture timestamp resolution / capture provenance
```

Every generated contract violation additionally records:

```text
recipient source clean interaction ID
donor source clean interaction ID(s)
donor/recipient session IDs and collection days
matching tier
B-context distance
frozen device caliper
transition-compatibility result
B→E boundary-continuity result
transformation type and violation family
transformation seed if stochastic
temporal alignment transformation
EXCESS composition offset where applicable
shared-flow/TCP compatibility result where applicable
raw timing/collision feasibility diagnostics where applicable
resulting intent context
resulting execution source
artifact-audit family and status
source_dependency_cluster
```

No counterfactual is generated from training observations.

No calibration observation becomes an anomaly sample.

No feature-vector-only splice is permitted.

Every transformed sample must be reproducible from raw held-out capture material and a manifest.

Matching failure produces a frozen infeasibility reason rather than a relaxed donor rule.

Replacement/translation and EXCESS-composition artifact audits are completed before the corresponding counterfactual security results are interpreted.

---

# 88. Reproducibility Requirements

Release where licensing permits:

```text
collection scripts
Android automation scripts
constrained-random action schedules and seeds
settling-latency estimation code
background-activity stratification rules
capture-processing code
feature extraction
network-topology metadata definitions
split manifests
shared-normalization sufficient-statistic code
counterfactual matching code
training-only B-context caliper construction code
deterministic donor-assignment and reuse manifests
transition-semantics compatibility checker
B→E boundary-continuity checker
EXCESS raw-timeline composition and physical-feasibility checker
counterfactual-generation manifests
replacement/translation artifact-audit code
EXCESS composition artifact-audit code
source-dependency-cluster manifests
physical-violation manifests
model configs
training seeds
FL configs
data-scarcity sampling manifests
leave-one-device/manufacturer manifests
intent-provenance perturbation manifests
hierarchical statistical-analysis code
result tables
figure-generation code
```

For restricted external datasets, release:

```text
dataset acquisition instructions
checksums where permitted
processing manifests
derived non-sensitive metadata
```

rather than redistributing protected raw data.

---

# 89. Negative Results

The protocol explicitly permits the following conclusions.

## Intent Adds Little

If the full contract model does not improve over execution-only modeling:

> Explicit mobile intent did not provide sufficient additional detection information under the evaluated conditions.

The benchmark remains valid.

## Pre-Context Adds Little

If:

```math
p(E\mid B,I)
```

does not outperform:

```math
p(E\mid I)
```

then pre-action context is not claimed as beneficial.

## Action Classification Is Enough

If direct action classification matches or exceeds contract density modeling across the **full** background and violation suite:

> The evaluated problem can be handled more simply as action-recognition consistency under these conditions.

No artificial superiority claim is made.

## Federation Adds No Benefit

If FL does not improve over local learning, including under the scarcity curve:

> Collaborative training did not provide measurable benefit under the evaluated device distributions and sample budgets.

The result remains relevant to heterogeneous FL-IoT research.

## Unseen-Device Transfer Fails

If held-out devices perform poorly:

> Intent–execution contracts are device- or environment-dependent under the evaluated representation.

Topology-stratified and protocol-feature ablations determine whether the failure is semantic or driven primarily by transport mismatch.

## Provenance Is Fragile

If modest timestamp or logging errors cause large degradation:

> Contract verification depends on high-quality intent provenance and synchronization under the evaluated design.

## Pure Replay Is Unobservable

If the feature representation cannot distinguish pure replay from valid execution:

> Replay detection requires additional temporal, sequence, cryptographic or application-layer observables beyond the locked feature set.

This is an observability result, not a failed experiment.

---

# 90. Why Negative Results No Longer Destroy the Novelty

The revised project does not define novelty as:

```text
FedIEC AUROC > baseline AUROC
```

The independent research objects are:

```text
cross-layer execution-contract task
independent mobile-intent provenance protocol
settling- and background-controlled physical benchmark
structured violation taxonomy with observability boundaries
artifact-controlled counterfactual generation protocol
physically induced violation protocol
federated evaluation protocol
data-scarcity collaboration analysis
zero-shot normalization-safe transfer protocol
topology/protocol transfer analysis
empirical characterization of which violations and semantics transfer
```

Model superiority controls **which performance claims are permitted**.

It does not determine whether the research question, benchmark or empirically demonstrated boundary exists.

---

# 91. Experimental Execution Order

```text
Final literature and novelty audit through current submission date
        ↓
Acquire >= 6 eligible IoT devices (target 8)
        ↓
Freeze manufacturer/category/topology coverage
        ↓
Request external datasets
        ↓
Implement Android intent logger
        ↓
Implement gateway capture pipeline
        ↓
Run excluded pilot on every core device
        ↓
Freeze W, settling latency, clock tolerance, NO_ACTION strata and action randomization
        ↓
Generate constrained-random collection schedules
        ↓
Collect all clean FedIEC-Contracts observations across multiple sessions/days
        ↓
Audit timestamps, settling integrity, state transitions and device attribution
        ↓
Freeze chronological splits
        ↓
Freeze feature extraction
        ↓
Freeze shared training-client normalization procedure
        ↓
Generate clean training/calibration/test artifacts
        ↓
Compute training-only B-context calipers and natural timing envelopes
        ↓
Freeze deterministic donor matching, transition and B→E boundary rules
        ↓
Generate semantic-preserving replacement/translation controls
        ↓
Run replacement/translation artifact audit
        ↓
Generate semantic-preserving EXCESS composition controls
        ↓
Run EXCESS composition artifact audit
        ↓
Correct only the failing transformation generator if its pre-registered audit criterion fails
        ↓
Generate mandatory family-specific artifact-controlled counterfactual suite
        ↓
Build and freeze source-dependency-cluster manifests
        ↓
Freeze violation manifests
        ↓
Implement and pre-register >= 3 physical violation mechanisms
        ↓
Run simple statistical baseline
        ↓
Run one-class baseline
        ↓
Run execution-only conditional model
        ↓
Run original p(E|I) model
        ↓
Run action-classification baseline
        ↓
Run full local contract models
        ↓
Run full centralized contract model
        ↓
Run full federated contract model
        ↓
Complete all 10 training seeds
        ↓
Run n={10,30,60,90} data-scarcity comparison
        ↓
Run leave-one-device-out evaluation
        ↓
Run topology-stratified and protocol-feature-ablation transfer analysis
        ↓
Run leave-one-manufacturer-out where feasible
        ↓
Run intent-provenance robustness analysis
        ↓
Run mandatory physically induced violations
        ↓
Audit PingPong eligibility
        ↓
Run external validation
        ↓
Audit real-attack alignment
        ↓
Run real-attack evaluation only if valid
        ↓
Run locked hierarchical statistical analysis
        ↓
Apply claim gates
        ↓
Write conclusions only from passed gates
```

---

# 92. Explicitly Out of Scope

The confirmatory chapter does not include:

```text
automatic APK reverse engineering
automatic semantic-intent extraction from app code
LLM-based intent extraction
voice-assistant commands
actions beyond ON/OFF
malware-family classification
payload inspection
federated poisoning
Byzantine aggregation
robust aggregation comparison
formal privacy mechanisms
differential privacy
secure aggregation
homomorphic encryption
large-scale client-dropout simulation
energy benchmarking
microcontroller deployment
Android on-device model deployment
post-hoc feature selection
post-hoc action selection
post-hoc architecture search
post-hoc hyperparameter rescue

```

These belong to later work.

---

# 93. Relationship to the PhD Thesis

FedIEC remains directly within the doctoral research domain:

```text
collaborative security detection
+
federated learning
+
physical IoT devices
+
heterogeneous client behavior
+
anomaly detection
+
cross-device generalization

```

It extends the thesis perspective by introducing a new information source:

```text
explicit mobile-side control intent

```

rather than changing the research field.

The project therefore remains substantially closer to:

```text
federated IoT anomaly/malware detection

```

than to:

```text
general Android vulnerability analysis

```

---

# 94. Fit to the Book Call

FedIEC directly intersects the chapter call through:

```text
Mobile and IoT security
Mobile application security
Hybrid and runtime security analysis
Behavioral malware/anomaly analysis
Machine learning for mobile security
Federated learning security and privacy
Cloud-connected mobile application security
Automated security testing
Mobile security metrics and benchmarking
Novel security frameworks
Reproducible security research

```

The mobile companion application is not an artificial framing device.

It supplies the independently observed control intent on which the execution contract is based.

---

# 95. Proposed Chapter Title

Primary title:

> **Federated Intent–Execution Contracts for Securing Mobile-Controlled IoT Systems**

Alternative title:

> **FedIEC: Cross-Layer Federated Anomaly Detection from Mobile Intent to IoT Execution**

Alternative benchmark-oriented title:

> **From Mobile Intent to IoT Execution: A Federated Benchmark and Framework for Runtime Contract Verification**

---

# 96. Proposed Chapter Contribution Statement

The chapter should position its contribution as follows:

> Mobile-controlled IoT security has already been studied through application/user-action context, network behavior, stateful policy enforcement and semantic consistency. FedIEC does not claim the mobile-action-to-network link itself as novel. Instead, it formulates independently logged mobile intent and pre-action network context as a probabilistic runtime execution contract over the device's subsequent network behavior. The chapter contributes a synchronized multi-device, multi-manufacturer physical benchmark; artifact-controlled and physically realized intent–execution violations; a federated conditional-learning protocol with explicit local-data-scarcity analysis; and leakage-safe unseen-device/manufacturer transfer evaluation that separates semantic generalization from protocol/topology mismatch.

---

# 97. Claims That Must Not Appear Without Evidence

Do not write:

```text
FedIEC is the first intent-aware IoT detector.
FedIEC is the first work linking mobile actions to IoT network behavior.
No previous work relates commands to network behavior.
No previous system detects command-execution mismatch.
No previous work uses semantics for IoT anomaly detection.
Federated learning guarantees privacy.
Contract violations are malware.
Counterfactual violations are attacks.
Pure replay is detectable from the locked 20 features.
FedIEC generalizes to arbitrary IoT devices.
FedIEC generalizes across manufacturers unless the manufacturer holdout gate passes.
FedIEC is deployable on constrained IoT hardware.
A seed-level significance test proves population-level physical generalization.
```

These statements are either contradicted by prior research or exceed the evidence.

---

# 98. Safe Novelty Wording

Before the final literature audit, use:

> **To the best of the literature reviewed through the current audit date, we did not identify prior work that jointly evaluates independently logged mobile control intent and pre-action context as a probabilistic IoT network execution contract, learns that contract federatively across naturally heterogeneous physical devices, evaluates artifact-controlled and physically realized intent–execution violations, and tests leakage-safe unseen-device transfer while explicitly separating semantic transfer from protocol/topology mismatch.**

The final manuscript must name the closest prior UI/user-action-to-network and semantic enforcement systems rather than implying this relationship was previously unexplored.

After the final audit, this wording may be narrowed further.

It must not be strengthened without evidence.

---

# 99. Proposal-Stage Deliverables

Before the October 24 proposal deadline, complete:

```text
current-through-2026 novelty audit
explicit closest-work collision table
final problem formulation
benchmark protocol
>=6-device acquisition/eligibility plan
manufacturer/category/topology coverage plan
violation taxonomy + observability table
transformation-specific counterfactual anti-artifact protocol (replacement/translation + EXCESS composition)
Android intent-logging prototype
gateway capture smoke test
at least one-device pilot
settling-integrity prototype
NO_ACTION activity-stratification prototype
zero-shot normalization specification
hierarchical statistics specification including shared-source dependency clusters
final chapter outline
preliminary figure of FedIEC architecture
```

Full experimental results are desirable but are not required for the proposal.

---

# 100. Post-Proposal Experimental Deliverables

After proposal submission:

```text
complete >=6-device clean collection across required sessions/days
freeze benchmark
pass the replacement/translation artifact audit and pass the EXCESS-composition audit for every device/family used to support Level-A EXCESS; otherwise mark ARTIFACT_AUDIT_INSUFFICIENT
generate artifact-controlled violation suite
complete local/centralized/federated experiments
complete 10 training seeds
complete n={10,30,60,90} scarcity curve
complete leave-one-device-out analysis
complete topology/protocol transfer analysis
complete leave-one-manufacturer-out where feasible
complete intent-provenance robustness analysis
complete mandatory physically induced violation study
complete public-dataset replication
complete hierarchical statistical analysis
freeze tables and figures
```

---

# 101. Execution Timeline

## September 17–30, 2026

```text
current-through-2026 novelty audit
closest-work collision matrix
hardware selection/acquisition for >=6 core devices
manufacturer/category/topology coverage lock
PingPong access request
Android automation harness
capture pipeline
feature extractor
counterfactual generator design including calipers, transition semantics, B→E continuity and EXCESS physical-timeline checks
```

## October 1–10, 2026

```text
pilot available core devices
estimate W and per-device settling latency
freeze timestamp tolerance
freeze NO_ACTION background strata
freeze constrained-random action scheduler
freeze shared-normalization protocol
freeze counterfactual matching metric, boundary descriptor and physical-timeline feasibility procedures
begin clean collection where devices pass pilot
```

## October 11–23, 2026

```text
complete enough controlled collection for feasibility evidence
run replacement/translation and EXCESS-composition artifact-control smoke tests
run model smoke experiments
prepare figures
write 1,000–2,000 word proposal
final proposal audit
```

## October 24, 2026

```text
submit chapter proposal
```

## October 25–November 20, 2026

```text
complete all core-device pilots if any remained
complete >=6-device multi-session clean dataset
freeze benchmark
compute training-only B-context calipers and timing envelopes
run replacement/translation artifact audit
run EXCESS composition artifact audit for every device intended to support a Level-A EXCESS claim; otherwise record ARTIFACT_AUDIT_INSUFFICIENT
freeze donor/source-dependency manifests
freeze artifact-controlled violation benchmark
complete baseline experiments
complete primary local/centralized/federated runs
```

## November 21–December 15, 2026

```text
complete all 10 training seeds
complete data-scarcity curve
leave-one-device-out
protocol-feature and topology-stratified transfer analysis
leave-one-manufacturer-out where feasible
intent-provenance robustness
external dataset experiments
mandatory physical violation experiments
hierarchical statistics
```

## December 16–31, 2026

```text
freeze results
generate final figures/tables
draft methodology/results/discussion
```

## January 1–10, 2027

```text
complete >=10,000-word chapter
limitations
related work
reproducibility appendix
observability-boundary discussion
```

## January 11–15, 2027

```text
final novelty audit through submission date
citation audit
claim-gate audit
transformation-specific counterfactual artifact-audit review
zero-shot leakage audit
statistical-unit audit
language cleanup
double-anonymization audit
submission-format audit
```

## January 16, 2027

```text
submit full chapter
```

---

# 102. Proposed Chapter Structure

## 1. Introduction

Motivate the gap between independently observed mobile intent and verified IoT execution without claiming that action-to-network linkage itself is new.

## 2. Background and Related Work

Cover:

```text
mobile companion-app analysis
UI/user-action to network-flow attribution
stateful smartphone/IoT security policies
device-event traffic signatures
semantic smart-home anomaly detection
interaction/state verification
federated IoT detection
```

Explicitly position against the closest prior systems identified in Section 7.

## 3. Threat Model and Intent–Execution Contracts

Define:

```text
intent provenance
pre/post context
contract
trust assumptions
observability boundary
violation taxonomy
```

## 4. FedIEC-Contracts Benchmark

Describe:

```text
devices/manufacturers/categories/topologies
Android harness
capture topology
settling-integrity rule
stratified NO_ACTION collection
constrained-random action schedule
sessions/days
splits
counterfactual matching/calipers and boundary controls
replacement/translation artifact audit
EXCESS composition/physical-timeline artifact audit
physical violations
reproducibility
```

## 5. Federated Contract Learning

Describe:

```math
p(E\mid B,I)
```

shared training-client normalization, local/centralized/federated regimes and data-scarcity protocol.

## 6. Experimental Methodology

Describe baselines, metrics, seeds, hierarchical statistics, provenance robustness and claim gates.

## 7. Results

Present:

```text
intent value
pre-context value
federated performance
data-scarcity collaboration curve
heterogeneity
violation-specific results
background false alarms
transformation-specific counterfactual artifact audits
```

## 8. Cross-Device and External Validation

Present:

```text
leave-one-device-out
topology-stratified transfer
protocol-feature ablation
leave-one-manufacturer-out where feasible
PingPong
other eligible public data
```

## 9. Security-Relevance Evaluation

Present mandatory physical violations and real attacks only where evidence supports them.

## 10. Discussion and Limitations

Discuss:

```text
trusted mobile intent
provenance jitter sensitivity
device/manufacturer scope
ON/OFF semantic scope
counterfactual realism
pure-replay observability limit
protocol/topology transfer boundary
federation scale
formal privacy limitations
```

## 11. Reproducibility and Future Research

Discuss dataset/code release and extension to richer actions and richer temporal/sequence observables.

## 12. Conclusion

State only claims that pass the locked gates.

---

# 103. Final Contribution Hierarchy

The final chapter should prioritize contributions in this order.

### Contribution 1 — Problem Formulation

**Probabilistic intent–execution contract verification for mobile-controlled IoT using independently observed intent and pre-action context.**

### Contribution 2 — Benchmark

**A synchronized multi-device, multi-manufacturer mobile-intent / IoT-execution benchmark with settling-controlled contexts, activity-stratified background data and reproducible transition- and boundary-compatible violations.**

### Contribution 3 — Counterfactual and Physical Security Protocol

**A transformation-specific artifact-controlled violation-generation methodology—with physical-timeline validation for composite executions—paired with physically realized control-path anomalies and explicit representation-observability limits.**

### Contribution 4 — Federated Methodology

**A federated conditional execution model with a pre-registered data-scarcity analysis establishing when collaborative learning helps relative to isolated local training.**

### Contribution 5 — Generalization Evidence

**Leakage-safe leave-one-device-out, topology-stratified and, where feasible, leave-one-manufacturer-out protocols establishing how far contract semantics transfer.**

### Contribution 6 — Empirical Security Findings

**A violation-specific characterization identifying which classes of execution divergence are detectable, provenance-sensitive, protocol-dependent, representation-unobservable or difficult to generalize.**

The contribution order is intentional.

The chapter's novelty therefore does not rest exclusively on the conditional flow outperforming a baseline.

---

# 104. Intended Scientific Contribution

If the relevant claim gates pass, the strongest permitted contribution is:

> **FedIEC formulates mobile-controlled IoT security as federated probabilistic intent–execution contract learning rather than claiming novelty for the already-studied link between user actions and network behavior. It links independently recorded mobile intent, steady pre-action behavioral context, and post-action network execution; constructs a synchronized heterogeneous physical-device benchmark with artifact-controlled and physically realized violation mechanisms; learns contracts locally, centrally and federatively; quantifies when federation helps under local data scarcity; and evaluates leakage-safe unseen-device/manufacturer transfer while separating semantic generalization from protocol/topology mismatch.**

If model-performance gates fail, the contribution is narrowed to the benchmark, formulation, artifact-controlled protocol, physical evaluation where completed, and empirical limits demonstrated by the study.

---

# 105. Final Research Identity

FedIEC is **not**:

```text
another FedAvg IDS
another ON/OFF traffic classifier
another device fingerprinting method
another Android static-analysis framework
another semantic smart-home rule checker
a claim that mobile actions have never been linked to IoT traffic
```

FedIEC investigates a narrower systems question:

> **Can independently observed mobile intent and pre-action state define a probabilistic runtime contract against which heterogeneous IoT execution is verified collaboratively; when does federation add value under limited local data; and which parts of that contract remain transferable across devices, manufacturers and network topologies without target-domain leakage?**

That is the research identity around which the proposal, implementation, experiments and final chapter should remain aligned.

---

# 106. Final Protocol-Lock Audit

Before the first confirmatory result is inspected, the roadmap is considered locked only if every item below is PASS.

## Novelty Integrity

```text
closest UI/user-action-to-network prior work named explicitly
current-through-submission-date literature search complete
novelty wording does not rely on action→network linkage alone
federated contribution includes data-scarcity question
```

## Collection Integrity

```text
K >= 6, >= 3 manufacturers, >= 3 categories
network topology recorded
>= 5 sessions and >= 3 days per device
W frozen
L_settle frozen per device
inter-command interval >= 2W + L_settle
constrained-random action schedules frozen
NO_ACTION 50/50/50 activity strata satisfied per device
clock synchronization within tolerance
```

## Counterfactual Integrity

```text
raw-window transformations only
training-only B-context calipers computed and frozen
deterministic Tier-1/Tier-2/Tier-3 session/day hierarchy enforced with no farther fallback
transition semantics matched to recipient physical pre-state
B→E boundary-continuity checks pass
internal timing and packet order preserved
no epsilon-jitter repair of infeasible timestamps
EXCESS uses legitimate active NO_ACTION burst, not random noise
EXCESS raw-timeline collision/short-gap/shared-flow checks pass
replacement/translation artifact audit passes
EXCESS composition artifact audit passes wherever Level-A EXCESS is claimed
artifact equivalence tolerance frozen before main results
donor reuse cap and source_dependency_cluster manifests frozen
late execution evaluated in a matched later NO_ACTION context
pure replay observability limit disclosed
```

## Federated / Transfer Integrity

```text
shared scaler derived only from current training clients
held-out device contributes no normalization statistics
held-out device contributes no main zero-shot threshold data
data-scarcity curve manifests frozen
leave-one-device-out complete
protocol-feature ablation complete
topology-stratified reporting complete
leave-one-manufacturer-out executed where eligibility permits
```

## Security-Relevance Integrity

```text
>= 3 physical mechanisms pre-registered
>= 2 mechanisms analyzable on >= 3 devices for physical-security claim
frozen model/scaler/threshold used for physical violations
real attacks kept separate and claimed only with valid ground truth
```

## Statistical Integrity

```text
seeds treated as optimization variability, not independent experiments
session/device dependence preserved
all generated observations retain recipient/donor source IDs
shared-source generated observations grouped into source_dependency_clusters
hierarchical paired bootstrap resamples source_dependency_clusters for Level-A counterfactual results
cluster-aware paired significance procedure implemented
artifact audits use equivalence-style A* criterion, not failure-to-reject reasoning
Holm family fixed to the three confirmatory comparisons
per-device effects and unique-source counts always reported
```

## Claim Integrity

```text
all claim gates evaluated mechanically
negative results retained
protocol/topology confounds separated from semantic conclusions
representation-unobservable failures reported as limits
no post-hoc rescue of model, features, devices, actions or violation definitions
```

Any PARTIAL or FAIL item must be resolved before the corresponding confirmatory claim is made. If it cannot be resolved, the claim is narrowed rather than the protocol weakened.
