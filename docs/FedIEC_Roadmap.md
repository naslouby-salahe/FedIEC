# FedIEC Research Roadmap

## Research Identity

**Acronym:** **FedIEC**

**Short title:**
**FedIEC: Federated Intent–Execution Contracts for Mobile-Controlled IoT Security**

**Full title:**
**FedIEC: Federated Intent–Execution Contract Learning for Cross-Layer Anomaly Detection in Mobile-Controlled IoT Networks**

### One-Sentence Research Identity

FedIEC investigates whether explicit control actions recorded during existing mobile-controlled IoT experiments can be treated as **runtime execution contracts**, whether violations of those contracts can be detected from the resulting IoT network behavior, and whether the underlying contract knowledge can be learned collaboratively across heterogeneous real devices represented in public datasets using federated learning.

### Evidence Model

FedIEC is a **public-dataset-only computational study**. It does not require the researcher to purchase, operate, automate, modify or physically interfere with IoT devices.

The core evidence comes from previously collected real-device traces whose action provenance and device identity can be independently verified from dataset metadata, collection documentation or original tooling.

### Protocol-Hardening Principle

Counterfactual evidence is valid only when the detector cannot exploit the mechanics used to construct the counterfactual. The locked protocol therefore treats intent provenance, raw-capture coverage, donor matching, transition semantics where observable, source-capture provenance, packet-timeline feasibility, transformation-specific artifact audits, donor dependence and statistical effective sample size as first-class validity conditions.

If a required property cannot be established from the source dataset, the observation or violation family is reported as unavailable or infeasible. Missing metadata are never reconstructed from the target traffic merely to preserve a planned claim.

---

# 1. Research Motivation

Existing IoT network anomaly detectors primarily ask:

```math
Is this network behavior unusual?
```

or model an unconditional execution distribution:

```math
q_0(X_{\text{interaction}})
```

where `X_interaction` represents a complete attributable source-defined interaction capture.

This formulation ignores information that is often available immediately before the device acts:

> **What was the device actually instructed to do?**

Existing mobile-controlled IoT datasets can provide an external source of such information when the original control action was independently recorded.

A mobile companion application may issue an explicit action:

```text
TURN_ON
TURN_OFF

```

and the controlled IoT device subsequently produces a network execution.

FedIEC therefore treats a mobile-issued action as a runtime **execution contract**.

The security question becomes:

> Given an independently recorded action, is the complete attributable interaction capture compatible with that action under the source collection protocol?

---

# 2. Core Concept

For the current four-dataset empirical study, define for every interaction:

```math
I
```

as the externally recorded intended action,

```math
X_{\text{interaction}}
```

as the complete attributable source-defined interaction capture. It may include traffic recorded before the command; it is never called exclusively post-command execution.

The main contract model estimates:

```math
p(X_{\text{interaction}} \mid I)
```

rather than only:

```math
q_0(X_{\text{interaction}})
```

The anomaly score is:

```math
s(X_{\text{interaction}},I)=-\log p(X_{\text{interaction}}\mid I)
```

A high score means:

> The observed source-defined interaction capture is improbable given the independently recorded action.

The stricter formulation \(p(E\mid B,I)\) remains a source-capability and future-secondary formulation only. It is not an active confirmatory analysis for the current four-dataset study because none supplies a usable primary strict population with independently supported B/E boundaries.

---

# 3. Why This Is an Execution Contract

The word **contract** has a precise operational meaning in FedIEC.

For the current empirical tier, an intent–interaction contract states that when:

```text
a known action I

```

is independently recorded; its complete attributable source-defined interaction capture should belong to an admissible distribution:

No preceding context is required in the current empirical tier.


```math
\mathcal C_I
```

The contract therefore does not prescribe one exact packet sequence.

Instead, it defines a learned admissible region:

```math
X_{\text{interaction}} \in \mathcal C_I
```

A contract violation occurs when:

```math
X_{\text{interaction}} \notin \mathcal C_I
```

or when an action-like execution occurs without a corresponding recorded intent.

This accommodates encrypted traffic, protocol variation, retransmissions, cloud-mediated communication, timing variability, and differences between physical devices represented in real-device traces.

---

# 4. Research Scope

The confirmatory semantic actions are:

```text
TURN_ON
TURN_OFF

```

A source may additionally support:

```text
NO_ACTION

```

`NO_ACTION` is not treated as a third semantic device action or a universal class.

It represents a source-defined capture interval in which no mobile control action was independently established.

Where independently reconstructable and suitably matched, it may support secondary analyses distinguishing:

```text
expected execution after ON
expected execution after OFF
ordinary behavior when no command occurred

```

without inferring the intended action from network traffic. Sources without it remain eligible for ON/OFF interaction-contract analyses.

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

They may be explored only after the locked ON/OFF study is complete and only when public-source provenance supports them.

---

# 5. Intent Provenance Requirement

The intended action must come from an **independent control-plane source recorded by the original data collection**.

Allowed sources are:

1. dataset metadata generated during the original controlled interaction;
2. an explicitly recorded mobile-app interaction or trigger log;
3. source filenames or directory structure whose ON/OFF semantics are documented by the original collection protocol;
4. original dataset tooling that deterministically maps recorded trigger order to semantic action;
5. another independently logged control event with equivalent provenance.

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

This separation is fundamental. Otherwise the model would be validating a label that was derived from the same evidence it is supposed to verify.

Every dataset receives an **intent-provenance grade** before model evaluation:

```text
VERIFIED_DIRECT        explicit action label/timestamp from source collection
VERIFIED_PROTOCOL      semantic action recoverable from documented original protocol/tooling
PARTIAL                action known but timestamp/boundary provenance incomplete
INELIGIBLE             action inferred from target traffic or provenance cannot be established
```

Only `VERIFIED_DIRECT` and `VERIFIED_PROTOCOL` observations may support the main confirmatory contract claims. `PARTIAL` data may be used only for explicitly labeled diagnostic replication if the corresponding analysis does not require the missing provenance field.

---

# 6. Mobile Application Role

The mobile companion application is a first-class part of the security setting but is **not executed, reverse engineered or automated by the researcher in the confirmatory study**.

Its role in the original source collection is:

```text
Mobile companion app
        ↓
Explicit user/control action
        ↓
Externally recorded intent provenance
        ↓
IoT network execution captured by the source dataset
        ↓
FedIEC execution-contract verification
```

The mobile application therefore supplies **action provenance through the source dataset**.

FedIEC investigates whether this previously recorded provenance supplies security information that network behavior alone does not provide.

No claim is made that FedIEC extracts intent from arbitrary mobile applications at runtime.

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

The narrower gap investigated is whether **independently recorded mobile-side intent from existing real-device datasets can serve as provenance for a probabilistic source-defined interaction contract, modeled as \(p(X_{\text{interaction}}\mid I)\), that is learned collaboratively across heterogeneous device clients, tested against source-feasible artifact-controlled semantic violation classes, and evaluated under leakage-safe unseen-device transfer without target-device normalization or calibration leakage.**

The target contribution therefore requires the joint presence of:

```text
independent mobile-intent provenance
+
complete attributable source-defined interaction capture
+
artifact-controlled contract counterfactuals
+
real physical-device identities represented in public traces
+
federated learning
+
data-scarcity collaboration analysis
+
device heterogeneity characterization
+
genuine unseen-device transfer
+
manufacturer/topology transfer only where source metadata support it
```

The research question is not whether ON/OFF traffic can be recognized. It is whether the **relationship between independently observed intent and resulting execution** can be learned as a transferable security contract and whether federation provides measurable value when individual device clients have limited contract data.

No absolute claim such as:

```text
first ever
never previously considered
completely novel
first action-aware IoT detector
```

is permitted until the final pre-submission literature audit.

The public-dataset-only design deliberately gives up the stronger claim of a newly collected physical benchmark and the stronger claim of experimentally induced physical control-path anomalies.

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
and, where available, pre-action behavioral context
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

For each family, state both the representation observability boundary and the **source-dataset feasibility boundary**. A theoretically meaningful violation that cannot be constructed without unsupported metadata is reported as unavailable rather than forced into the evaluation.

## Contribution C — Public Real-Device Contract Corpus and Provenance Audit

Construct a reproducible **derived evaluation corpus and manifest layer** from eligible public real-device traces containing, where available:

```text
dataset identity
physical device identity
manufacturer/category metadata
network-topology metadata when documented
intent label
source capture/session identifier
complete attributable interaction capture
semantic action
pre/post state metadata when documented
clean/violation status
counterfactual provenance
source-file checksum/reference
```

This is **not claimed as a newly captured traffic dataset**. The contribution is the harmonized eligibility, provenance, split and transformation protocol over existing traces.

## Contribution D — Artifact-Controlled Contract Evaluation

Counterfactuals are generated from held-out raw captures under frozen source-aware matching, transition compatibility where observable, source-capture provenance checks and raw-timeline feasibility rules. Transformation-specific artifact audits are mandatory so apparent security performance cannot be explained by splice, merge, timestamp, flow-state or donor-selection artifacts.

## Contribution E — Federated Contract Learning

Evaluate whether contract knowledge can be learned collaboratively with:

```text
one dataset-identified physical device = one federated client
```

while keeping the FL interface restricted to model updates and determine when collaboration is useful as local clean-contract data become scarce.

The study is an FL simulation over public datasets; it does not claim operational privacy or a live distributed deployment.

## Contribution F — Cross-Device and Cross-Dataset Transfer

Evaluate whether a contract learned from other device clients can recognize valid and invalid intent–execution relationships on a held-out physical device absent from model training, normalization and main zero-shot calibration.

Where metadata and sample counts permit, add manufacturer-stratified or topology-stratified analysis. Replicate the formulation on a second public dataset without silently pooling incompatible collections.

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
some public datasets fail full-contract eligibility
some device types transfer poorly
ON/OFF distinction is weak for one device
NO_ACTION cannot be reconstructed for one source
manufacturer/topology metadata are unavailable
```

Such results restrict the permitted claims but do not remove:

```text
the security task
the provenance and eligibility protocol
the derived public-data evaluation corpus
the violation taxonomy
the artifact-controlled evaluation protocol
the federated scarcity analysis
the cross-device analysis
the empirical observability/transfer boundaries
```

A source dataset is never promoted, excluded or redefined based on model performance.

---

# 11. Research Questions

## RQ1 — Contract Information

Does knowledge of independently recorded mobile intent improve execution-consistency detection beyond execution-only network modeling?

## RQ2 — Pre-Execution Context (Future Secondary Tier)

For a future source with independently supported B/E boundaries, does \(p(E\mid B,I)\) improve on \(p(E\mid I)\)? This question is not part of the current confirmatory study.

## RQ3 — Violation Differentiation

How well can the same clean-trained contract model detect the following **where each family is source-feasible and passes its artifact audit**:

```text
omission
substitution
uncommanded execution
excess execution
replay/late execution where observable
```

without being trained on those violations and without exploiting counterfactual-generation artifacts?

## RQ4 — Federated Learnability

Can intent–execution contracts be learned collaboratively across naturally different physical device clients represented in public IoT traces?

## RQ5 — Heterogeneity and Collaboration Need

How do contract distributions vary across device clients and, where documented, manufacturers or network-control settings, and under what local-data scarcity levels does federation provide measurable benefit over isolated learning?

## RQ6 — Cross-Device Generalization

Can a federated contract model trained without one physical-device client identify valid and invalid intent–execution relationships on that device using no target-device training, normalization or main zero-shot calibration information?

## RQ7 — Security Relevance

Do artifact-controlled contract counterfactuals and, where valid aligned public evidence exists, observed attack/control-failure traces produce measurable contract violations under a frozen clean-trained detector?

## RQ8 — Intent-Provenance Robustness

How sensitive is contract verification to realistic imperfections in the recorded intent channel such as timestamp jitter, logging delay, missing intents and duplicate intents?

## RQ9 — Transfer Boundary

How much of unseen-device performance is explained by semantic transfer versus protocol/dataset mismatch, and does the formulation remain meaningful when independently replicated on another eligible real-device dataset?

---

# 12. Main Hypothesis Structure

Two comparisons are confirmatory where their source-feasibility gates pass. No replacement hypothesis is introduced for unavailable immediate pre-action context.

## Hypothesis 1 — Intent Value

Compare:

```math
p(X_{\text{interaction}}\mid I)
```

against:

```math
q_0(X_{\text{interaction}})
```

This isolates the contribution of explicit intent.

## Hypothesis 2 — Collaborative Value

Compare:

```text
federated contract learning

```

against:

```text
isolated local contract learning

```

using identical eligible public-device client populations and architectures.

Other comparisons are required baselines or secondary analyses but are not added to the confirmatory hypothesis family.

---

# 13. Dataset Hierarchy

FedIEC uses a **public-dataset-only evidence hierarchy**.

Dataset roles are assigned from audited source capability before model results are inspected; no source has an automatic primary role. Mon(IoT)r received explicit pre-model approval for the active interaction-contract tier only:

```text
Mon(IoT)r / IMC 2019: approved primary multi-device interaction-contract source
CIC IoT 2022: sparse independent-capture replication / protocol-mode contrast
TU Wien Philips Hue: large-sample single-device-family replication only
PingPong: provenance and sequential-source diagnostic; not eligible for capture-level interaction contracts
```

Dataset priority is based only on **protocol eligibility**, not on model performance.

No dataset is promoted to primary without explicit approval. Datasets are not pooled.

Each collection keeps its own capture semantics and source dependence.

TU Wien Philips Hue is a single-device-family replication source and cannot establish multi-device federation by itself.

Mon(IoT)r / IMC 2019 has separate Android companion-app ON/OFF experiment PCAPs, individually auditable capture groups and a complete attributable capture representation. Its release lacks a per-capture command instant and independently reconstructable matched NO_ACTION captures; it is approved only for the active ON/OFF interaction-contract tier after passing the representation-confound gate. It does not support strict B/I/E, universal NO_ACTION, replay/late-execution, or strong uncommanded-execution claims.

The pre-experiment primary freeze contains 9,986 eligible non-empty ON/OFF captures from 37 physical-device clients and 9,986 non-overlapping individual source groups. LAN/WAN and VPN remain source contexts rather than clients; US and UK instances remain distinct physical clients. The frozen 19-feature representation, source-group split manifests, normalization rule, holdout definition, interfaces, seeds, statistical procedure, and source-gated unavailable families must be re-audited if source filtering, feature definition, client identity, capture selection, or network-condition treatment changes.

---

# 14. Public-Dataset Main-Study Eligibility

A dataset can support the current **interaction-contract main study** only if the required evidence exists before any model result is inspected.

Minimum source requirements:

```text
multiple identifiable real physical IoT devices
independently documented TURN_ON and TURN_OFF semantics
raw packet traces or equivalent packet-timeline material
independently verifiable ON/OFF provenance
unambiguous device attribution
complete attributable source-defined interaction capture
non-overlapping train/calibration/test construction possible
sufficient per-device interactions for local and federated comparison
```

`NO_ACTION` is source-dependent and secondary; it is required only for an analysis that explicitly uses it.

A dataset receives one of:

```text
FULL_CONTRACT_ELIGIBLE
ACTION_CONTRACT_ONLY
REPLICATION_ONLY
ATTACK_ALIGNMENT_ONLY
INELIGIBLE
```

`FULL_CONTRACT_ELIGIBLE` supports the complete source-defined \((X_{\text{interaction}},I)\) protocol and all source-feasible analyses. It does not imply availability of strict B/E analysis or NO_ACTION.

`ACTION_CONTRACT_ONLY` supports ON/OFF interaction-conditioned analyses but not claims requiring valid NO_ACTION, exact timing, or unavailable violation families.

`REPLICATION_ONLY` supports a narrower mechanism replication such as large-sample action-conditioned consistency.

`ATTACK_ALIGNMENT_ONLY` supports only a separately reported attack-aligned analysis.

No minimum manufacturer/category quota is imposed merely to preserve the original hardware-acquisition design. Instead, the exact device, manufacturer, category and topology coverage of every public source is reported transparently.

The main federated claim requires at least **four eligible physical-device clients** after all provenance and split gates. If fewer than four remain, FedIEC may still evaluate the contract formulation but does not make a broad multi-device federated learnability claim.

---

# 15. Dataset and Device Inclusion Rule

Every source and device is selected by frozen technical eligibility rules before model evaluation.

A device may be excluded only for reasons such as:

```text
intent provenance cannot be verified
device identity is ambiguous
required raw capture is unavailable or corrupted
ON/OFF semantics cannot be established independently
incomplete attributable interaction-capture coverage
insufficient samples for the declared analysis
train/test separation cannot be made without source overlap
traffic cannot be attributed to the target device
```

A device may **not** be excluded because:

```text
its distributions overlap
its model performance is poor
its behavior differs strongly from other devices
it reduces federated performance
it produces inconvenient results
it weakens a transfer claim
```

Every exclusion is recorded in a dataset/device eligibility manifest with a frozen reason.

No source is replaced with a more favorable dataset after confirmatory results are observed.

---

# 16. Public Intent-Provenance Audit

No Android automation harness is built for the confirmatory study.

For every candidate dataset, audit the original collection documentation, metadata and tooling to establish:

```text
how the action was generated
whether an official companion app was used
how TURN_ON versus TURN_OFF is encoded
how the trigger timestamp/boundary is recorded
whether action order is deterministic or randomized
whether multiple triggers can overlap one capture
whether device state is documented
whether NO_ACTION intervals can be identified independently
```

Every eligible interaction records:

```text
dataset_id
source_capture_id
device_id
semantic_action
intent_timestamp_or_boundary
intent_provenance_grade
original_metadata_reference
original_tool/protocol reference when needed
source checksum or immutable file reference
```

The semantic action is taken from source provenance **before** the target-device network execution is evaluated.

If polarity is recovered from original tooling rather than an explicit field, the exact source rule and code/documentation pointer are frozen in the manifest.

Provenance-robustness experiments perturb copied metadata after clean corpus construction; they never replace or rewrite the original source label.

---

# 17. Raw Capture and Device-Attribution Audit

FedIEC does not collect new network traffic.

For every candidate source, the raw-data audit establishes:

```text
capture file structure
capture time basis and timestamp resolution
target-device identifiers available for filtering
whether phone/controller traffic is co-captured
capture start/end coverage relative to trigger time
whether multiple devices share one capture
whether individual interaction boundaries are explicit or reconstructable
whether packets before and after the trigger are available
```

The **detection model uses only traffic attributable to the target IoT device**.

Controller/phone traffic may be inspected only for provenance verification when allowed by the source and is not supplied as a learned feature.

The public dataset may reside centrally on the research machine. Client separation is therefore an experimental partitioning construct representing source-device silos; it is not evidence of operational raw-data isolation in deployment.

---

# 18. Dataset Characterization and Protocol Lock

Before confirmatory model results are inspected, perform a **training-only dataset characterization stage** for every candidate primary source.

This replaces the original physical-device pilot.

The characterization stage is used only to:

```text
verify provenance reconstruction
verify target-device attribution
characterize complete attributable source-capture coverage
freeze the source-defined interaction-capture representation
characterize source timestamp resolution
identify source capture/session grouping
characterize background intervals available for NO_ACTION
verify action-transition metadata where available
measure natural packet timing and collision behavior
freeze source-capture provenance descriptors
freeze EXCESS composition feasibility rules if EXCESS is source-feasible
detect preprocessing/capture anomalies
```

All numerical quantities that could leak test behavior are computed from the training partition only after the source-aware split is frozen.

The characterization stage fixes **procedures**, not favorable model parameters.

If a dataset cannot support a required procedure, its eligibility status is narrowed rather than modifying the procedure after observing detection results.

---

# 19. Observation Windows

For each independently recorded ON/OFF interaction, construct \(X_{\text{interaction}}\) from the complete source-defined capture attributable to the target device. Capture start and end come from the original source artifact, not an inferred command time.

Source capture duration and timing semantics may differ across datasets. Results are within-source and cross-dataset results are replications, never pooled as one protocol.

No missing pre-trigger or post-trigger traffic is fabricated, padded, or inferred. A strict \(B,E\) construction is permitted only in a future secondary tier when a source independently supports its trigger boundary and coverage.

---

# 20. NO_ACTION Windows

`NO_ACTION` is secondary and retained only when it can be reconstructed from source material without inferring intent from target-device traffic and without confounding it with capture duration, scope, or collection procedure.

An eligible `NO_ACTION` pseudo-event requires:

```text
no recorded mobile/control trigger in the frozen exclusion interval
complete attributable source-defined capture coverage
target device remains attributable
no known controlled-action overlap
no attack/intervention label active unless explicitly used in a separate study
```

It receives:

```text
IntentContext = NO_ACTION
```

## Background Activity Stratification

If enough eligible background material exists, partition training-only `NO_ACTION` windows by a simple packet/byte activity score into:

```text
BACKGROUND_SILENT
BACKGROUND_LOW_ACTIVITY
BACKGROUND_ACTIVE_BURST
```

The cut points are learned only from the training partition and frozen before test evaluation.

The confirmatory test set should contain representation from all available strata, but no fixed 50/50/50 quota is imposed when the original dataset does not contain that amount of background behavior.

`BACKGROUND_ACTIVE_BURST` should include legitimate spontaneous traffic where the source permits it, such as keep-alives, cloud synchronization, NTP/DNS-related activity or routine telemetry.

The activity stratum is metadata, not a model feature.

If valid matched `NO_ACTION` cannot be reconstructed, all NO_ACTION-dependent analyses are unavailable; the dataset may still support ON/OFF interaction-contract analysis.

---

# 21. Eligible Corpus Size

FedIEC does not prescribe a new collection size because no new traffic is collected.

After eligibility filtering, report for every dataset and device:

```text
number of raw source captures
number of verified TURN_ON interactions
number of verified TURN_OFF interactions
number of reconstructable NO_ACTION windows
number with complete attributable interaction-capture coverage
number with independently supported strict B/E coverage, if any
number excluded and reason
number retained for train/calibration/test
```

The primary dataset must contain enough eligible observations to support:

```text
local training
federated training
clean calibration
held-out testing
source-aware counterfactual construction
leave-one-device-out where claimed
```

No source interaction is duplicated merely to satisfy a planned sample count.

The effective evidence size of generated counterfactuals is always reported through unique source interactions and source-dependency clusters, not only generated-row count.

---

# 22. Clean Split

The split is **source-aware and leakage-resistant**.

Within each dataset and device × intent context, use chronological ordering when trustworthy source timestamps exist.

Where the dataset is organized into capture/session groups rather than a continuous chronology, use a deterministic blocked split that keeps one source capture group entirely inside one partition.

The target proportions are:

```text
training    ≈ 60%
calibration ≈ 20%
test        ≈ 20%
```

subject to source-group integrity and minimum sample requirements.

The exact counts are frozen in a split manifest before model evaluation.

Forbidden:

```text
randomly splitting packets from the same interaction
placing one repeated/source capture in multiple partitions
choosing split boundaries based on model performance
using test observations to increase a sparse training client
```

If timestamps are available, the blocked split preserves chronology. If only source-group identities are available, a deterministic group ordering is documented and used consistently.

---

# 23. Source-Order and Dependence Control

FedIEC inherits the original collection order; it does not attempt to redesign that order retrospectively.

For every source, document whether actions were collected using:

```text
alternation
randomized order
blocked ON/OFF runs
separate files per action
unknown order
```

If deterministic alternation or collection blocks make the pre-action state predictive of the next action, this is treated as a **source confound** and handled explicitly rather than hidden.

Required controls where feasible:

```text
report action-transition frequencies
stratify or match by known pre-state/previous action when metadata exist
report source-order and collection-condition confounds
do not use source order as an intent proxy
```

A dataset whose source protocol makes RQ2 fundamentally uninterpretable may still support the other FedIEC questions.

No source trace is reordered to create artificial independence.

---

# 24. Contract-Violation Taxonomy

FedIEC evaluates five distinct failure semantics, but every family is subject to an explicit **observability, source-feasibility and artifact-control boundary**. A violation family is not credited merely because a synthetic transformation is easy to distinguish.

## 24.1 Omission

```text
Intent exists
The source-defined interaction capture is inconsistent with the declared intent
```

A diagnostic omission counterfactual may replace a held-out commanded capture with a matched legitimate `NO_ACTION` capture from the same device only when a source-valid construction exists.

Otherwise omission is diagnostic-only or unavailable for that dataset.

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

The donor execution comes from the same physical device.

When source metadata provide physical pre-state or transition class, the donor must be transition-compatible with the recipient context. When state metadata are absent and transition compatibility cannot be established from independent source metadata, substitution is marked unavailable for that device rather than inferred from network traffic.

## 24.3 Uncommanded Execution

```text
No mobile intent exists
Action-like execution occurs
```

This family is unavailable for strong claims in the current evidence because it requires a valid matched `NO_ACTION` recipient.

The evaluation must include active-background `NO_ACTION` controls where source data permit so the detector cannot solve the task as silence-versus-activity classification.

## 24.4 Excess Execution

```text
Expected execution occurs
but an additional legitimate-looking device-network effect is present
```

The diagnostic construction, where source-feasible, combines a held-out commanded capture with an independently captured legitimate active-background burst from the same device.

It is not random packet noise and not naïve feature-vector addition.

### Raw-Timeline Requirement

An `EXCESS_EXECUTION` composite is admissible only if:

```text
both components are raw held-out traces from the same physical device
internal packet order and offsets are preserved
no arbitrary epsilon timestamp repair is used
new timestamp-collision/ultra-short-gap artifacts remain inside training-derived envelopes
no incompatible shared-flow/TCP state is created
source-capture provenance and raw-timeline integrity remain compatible
identical raw-to-feature extraction is rerun after composition
```

Raw transport identifiers and sequence information may be used by the feasibility checker only; they never become learned features.

If the public source does not contain suitable active-background material or cannot support the composition audit, `EXCESS_EXECUTION` is `SOURCE_INFEASIBLE` or `ARTIFACT_AUDIT_INSUFFICIENT` and cannot support a claim.

### Natural-Concurrency Boundary

If the same background-behavior class is already an ordinary component of clean commanded execution, it is not labeled excess. It becomes a hard clean/concurrency control.

## 24.5 Replay or Late Execution

A pure replay of a valid execution can be mathematically indistinguishable from a genuine execution under the locked feature representation.

FedIEC therefore separates two cases.

### Detectable late / temporally misaligned execution

This family is unavailable without an independently valid timing boundary. A source with such a boundary may evaluate it only as a future strict-tier analysis.

### Pure replay observability limit

If replay preserves the final execution representation and occurs under an indistinguishable context, the current representation contains no information with which to distinguish it from a valid execution.

Such cases are reported as:

```text
REPRESENTATION_UNOBSERVABLE
```

and cannot support a replay-detection claim.

---

# 25. Artifact-Controlled Violation Evaluation

Violation evaluation is based on **public-source held-out traces only**.

There is no mandatory physically induced Level-B experiment.

## Level A — Artifact-Controlled Contract Counterfactuals

Mandatory for every counterfactual-based claim.

Generated only from held-out observations and raw captured timelines.

No counterfactual is created by directly concatenating already-extracted feature vectors.

A generated counterfactual is eligible for a semantic claim only when its family-specific source-feasibility and transformation audit pass.

### 25.1 Frozen Counterfactual Metadata

Before donor assignment, every eligible held-out clean interaction records all source-supported metadata needed for matching:

```text
dataset_id
physical device id
manufacturer/category where documented
topology where documented
source capture/session group
source timestamp/order
semantic intent
intent-provenance grade
pre-state/post-state where independently documented
transition class where independently documented
source-capture representation and provenance signature
source chronology and collection-condition metadata where available
capture timestamp resolution
background-activity stratum where applicable
```

Missing metadata remain missing; they are not inferred from the execution under evaluation.

### 25.2 Frozen B-Context Distance and Common-Support Caliper

The distance definition is frozen before main model evaluation.

After the clean split, compute the numerical common-support caliper from the **training partition only** for every device with sufficient support.

For device `i`:

```math
c_i = Q_{0.95}(d_{B,\mathrm{NN}})
```

A donor is admissible only when:

```math
d_B(B_{recipient},B_{donor}) \le c_i
```

If the source cannot support a stable device-specific caliper, that device/family is marked insufficient rather than borrowing held-out information.

### 25.3 Source-Aware Matching Hierarchy

The original physical-collection day hierarchy is replaced by a hierarchy grounded in whatever grouping the public source actually exposes.

For each dataset, freeze one hierarchy before model evaluation, for example:

```text
Tier 1: same physical device + same source capture/session group
Tier 2: same physical device + nearest distinct source group under documented chronology
Tier 3: same physical device + another eligible group within the frozen source rule
Otherwise: NO_VALID_COUNTERFACTUAL
```

If the source has no meaningful session grouping, use source capture IDs and deterministic timestamp/order proximity instead of inventing sessions or days.

At every tier, require all family-specific compatibility, B-caliper, provenance and boundary rules that can be established independently.

The exact hierarchy is frozen separately per dataset and released in the manifest.

### 25.4 Transition-Semantics Compatibility

For substitution, use independent physical-state/transition metadata when available.

If the recipient transition semantics cannot be established without analyzing the target execution itself, do not use transition-sensitive substitution for that observation.

Record:

```text
TRANSITION_VERIFIED
TRANSITION_NOT_AVAILABLE
COUNTERFACTUAL_INFEASIBLE_TRANSITION
```

Only verified transitions support transition-specific claims.

### 25.5 Strict B/E Boundary Rule — Future Secondary Tier

The current capture-level tier does not use B/E boundary continuity. Where a future raw source contains an independently supported boundary around `t_I`, compute a frozen raw descriptor summarizing:

```text
target-device flows active across the boundary
transport protocol / connection-state class
recent packet-direction/activity pattern
endpoint/flow continuity class
background activity crossing the boundary
```

The descriptor is matching metadata only and never a model input.

A donor that creates an artificial disappearance or appearance of a continuing flow/background rhythm is rejected.

If boundary continuity cannot be evaluated because the source capture does not include the necessary raw context, the corresponding transformation is unavailable.

### 25.6 Temporal Alignment Rule

Donor executions are transformed only at raw timestamp/packet level.

When translated to a new pseudo-intent time:

```text
preserve internal packet offsets
preserve source-capture activity span
preserve capture-relative first-packet latency unless timing is the violation
preserve internal packet order
recompute all timing features after transformation
never splice only aggregate features
never repair infeasible transforms with arbitrary epsilon jitter
```

### 25.7 Donor Assignment, Reuse and Dependence

Counterfactual generation uses deterministic matching manifests.

Within each violation family:

```text
a clean interaction cannot be both recipient and donor in the same generated row
donor reuse is minimized and capped by a frozen rule
a donor is never duplicated merely to increase sample count
all source clean interaction IDs are recorded
```

Create a `source_dependency_cluster` by linking generated observations that share any source clean interaction. Connected components are resampled together in the hierarchical analysis.

### 25.8 EXCESS Composition Rule

`EXCESS_EXECUTION` is the only planned family that composes two packet timelines.

The background donor is aligned according to the frozen dataset-specific background rule. Internal timing is preserved.

Mandatory diagnostics before feature extraction include:

```text
new exact-timestamp collision count/rate
new ultra-short inter-arrival count/rate
minimum positive inter-arrival by direction
shared active transport-flow count
TCP sequence/acknowledgment compatibility where shared flows exist
packet-order preservation for each source component
raw-timeline feasibility status
```

Diagnostics are compared with clean training-derived natural envelopes.

A candidate outside the frozen envelope is rejected, not clipped or jittered.

### 25.9 Artifact Audit A — Replacement/Translation

This audit covers:

```text
OMISSION
SUBSTITUTION
UNCOMMANDED_EXECUTION
TEMPORALLY_MISALIGNED_EXECUTION
```

Construct semantic-preserving controls using the same transformation machinery but a donor execution with the **same semantic intent** as the recipient.

A dedicated artifact classifier attempts to distinguish genuine held-out clean interactions from transformed semantic-preserving controls using the final execution representation without intent.

### 25.10 Artifact Audit B — EXCESS Composition

Passing Audit A does not validate `EXCESS_EXECUTION`.

Where enough naturally concurrent clean action+background observations exist, compare them with synthetically recomposed allowed-concurrency controls produced by the same merge path.

A no-op round-trip test is mandatory: running the composition pipeline with no added packets must reproduce the original extracted feature vector exactly.

If suitable clean concurrency controls do not exist, EXCESS is `ARTIFACT_AUDIT_INSUFFICIENT` for that device/source.

### 25.11 Frozen Artifact-Audit Pass Criterion

For each artifact-audit family define:

```math
A^*=\max(AUROC,1-AUROC)
```

with frozen tolerance:

```math
\delta_{artifact}=0.10
```

The audit passes only if all applicable conditions hold on held-out audit data:

```text
upper bound of the 95% dependence-aware CI for A* <= 0.60
no individual-device A* > 0.70
no single final model feature has pooled univariate A* > 0.65
all mandatory raw-timeline feasibility diagnostics pass
```

If the source sample size is too small to evaluate a criterion meaningfully, the result is `ARTIFACT_AUDIT_INSUFFICIENT`, not PASS.

### 25.12 Main Counterfactual Constructions

Where source-feasible:

```text
OMISSION: correct intent + matched legitimate NO_ACTION execution
SUBSTITUTION: correct intent + verified-compatible opposite-action execution
UNCOMMANDED_EXECUTION: NO_ACTION + matched legitimate action execution
EXCESS_EXECUTION: commanded execution + feasible legitimate active background composition
REPLAY_OR_LATE_EXECUTION: legitimate execution translated into a later matched NO_ACTION context
```

These observations are called:

```text
contract counterfactuals
```

not:

```text
cyberattacks
malware
real compromises
physically induced failures
```

## Level B — Dataset-Grounded Observed Divergences

Optional.

If a public dataset contains independently documented failed commands, delayed commands, unintended actions or comparable control-path anomalies, evaluate them separately without synthetic transformation.

The event must have independent ground truth for intended action and observed outcome.

Absence of such events does not invalidate the main FedIEC study and does not trigger new physical data collection.

---

# 26. Real-Attack Claim Boundary

A contract counterfactual is never called an attack.

A dataset-grounded control failure is not automatically called malware.

A real-attack claim requires all of:

```text
actual attack activity independently documented
+
known legitimate intent
+
known attack-active interval or bounded alignment
+
isolatable target-device execution
```

If these conditions cannot be established from the public source:

> FedIEC makes no real-attack detection claim for that dataset.

No live attack is generated by the researcher as part of this chapter.

---

# 27. PingPong — Sequential-Source Diagnostic

PingPong contains real smart-home devices and independently auditable companion-app trigger ordering, but each device/context continuous capture contains many alternating interactions and is one inseparable source group.

The evaluation uses only devices/capture subsets for which semantic action can be mapped independently and unambiguously to:

```text
TURN_ON
TURN_OFF
```

No action is inferred from target-device network traffic.

PingPong fails the clean-split gate for capture-level interaction contracts: its genuine source group cannot populate train, calibration and test without overlap. It is not a primary or replication population for \(p(X_{\text{interaction}}\mid I)\); it remains a provenance and source-order diagnostic.

PingPong is not treated as a novel dataset contribution of FedIEC.

---

# 28. PingPong Eligibility

A PingPong device/capture subset is eligible only when:

1. the device has clearly documented ON and OFF triggers;
2. trigger order/timestamps distinguish ON from OFF under the original protocol;
3. the relevant traffic was generated through an eligible mobile-control pathway;
4. sufficient raw capture surrounds the trigger for the declared analysis;
5. device identity is unambiguous;
6. training, calibration and evaluation traces can be separated without source overlap;
7. required background/no-action intervals are available for any claim that depends on `NO_ACTION`.

All eligible devices are retained.

No performance-based device selection is allowed.

## 28.1 Verified Polarity Convention

The acquired release does not store ON/OFF polarity per line in every `timestamps` file. Where the original PingPong collection/tooling defines alternating trigger polarity, that documented source convention may be used as `VERIFIED_PROTOCOL` provenance.

The exact original tool revision/source pointer and the mapping rule are frozen in the provenance manifest.

This rule applies only to capture families for which the original collection documentation supports it. `remote-phone`, `ifttt`, `public-dataset` or other subsets require their own provenance audit and are not automatically promoted to eligibility.

Devices with non-binary or ambiguous semantics remain outside the confirmatory ON/OFF study.

---

# 29. Replication Dataset — TU Wien Philips Hue

The TU Wien Philips Hue dataset is a large-sample action-conditioned replication source.

The acquired material contains repeated labeled ON/OFF captures with action polarity encoded in capture naming/documentation.

Its role is:

```text
large-sample replication of action-conditioned consistency
```

It tests whether the FedIEC formulation remains meaningful over thousands of repeated executions from one physical-device family.

Because it does not provide a multi-device client population by itself, it cannot establish:

```text
federated heterogeneity benefit
leave-one-device-out transfer
manufacturer generalization
multi-client fairness
```

TU Wien has no independently supported strict B/E boundary or matched NO_ACTION population. It remains a large-sample single-device-family ON/OFF interaction-contract replication.

---

# 30. CIC IoT 2022 — Sparse Independent-Capture Replication

CIC IoT 2022 provides sparse individually captured app-triggered ON/OFF interactions: three independent captures per device/context/action where eligible. It is an independent-capture replication and protocol-mode contrast, not the primary multi-device federated population.

Use only interaction subsets whose trigger semantics satisfy the independent intent-provenance rule.

The raw material separates several app-triggered ON/OFF pathways in directory structure such as:

```text
LOCAL_ON / LOCAL_OFF
LAN_ON / LAN_OFF
WAN_ON / WAN_OFF
```

Voice-assistant folders such as `ALEXA_*` or `GOOGLE_*` are outside the locked mobile-companion-app confirmatory scope unless the research scope is explicitly changed before protocol lock.

The current source material does not establish a per-interaction trigger boundary. It may use complete attributable captures for the approved interaction tier but not strict B/E claims.

CIC IoT 2022 may support:

```text
independent replication
cross-dataset robustness
source-feasible ON/OFF interaction-contract replication
```

but each role is gated separately by provenance, capture coverage and split feasibility.

---

# 31. Cross-Dataset Replication Rule

FedIEC does not treat different public collections as interchangeable samples from one homogeneous population.

The primary rule is:

```text
train/evaluate within one dataset
replicate the protocol independently on another dataset
compare effect direction and failure boundaries
```

Raw samples from Mon(IoT)r, PingPong, CIC IoT 2022 and TU Wien are not pooled into one confirmatory FL population. Each uses its own audited source-capture semantics and physical-device client population.

Cross-dataset reporting includes:

```text
source-defined capture representation
source-specific eligibility counts
source-specific feature availability
source-specific provenance grade
source-specific FL client count
source-specific effect estimates
```

A successful replication strengthens external validity. A failed replication is reported as a dataset/collection boundary rather than silently excluded.

---

# 32. Public-Dataset Failure Rule

Failure of one public dataset does **not** invalidate FedIEC.

A source may fail the full protocol because of:

```text
ambiguous intent labels
insufficient ON/OFF samples
uncertain mobile trigger provenance
missing complete attributable interaction-capture coverage
missing NO_ACTION material
incompatible capture boundaries
missing physical-device identity
insufficient independent capture groups
licensing/access limitations
```

Eligibility rules are never weakened because a preferred dataset would otherwise be unusable.

If no candidate dataset passes the full multi-device main-study gate, the chapter must narrow its claims to the contract components that the evidence actually supports; it does not revert to acquiring physical devices as an unplanned rescue.

---

# 33. Optional Real-Attack Dataset

CIC IoT 2022 or another suitable public dataset may support a real-attack analysis only if the following can be established directly:

1. intended legitimate action;
2. corresponding physical device;
3. intent timestamp or bounded trigger interval;
4. attack-active interval;
5. target-device execution during that interval.

If any condition is missing, the dataset cannot support the real-attack claim.

Attack-aligned evaluation is optional and remains separate from the counterfactual contract benchmark.

No attack label is reverse-engineered from the contract score itself.

---

# 34. Unit of Analysis

The current empirical contract observation is:

```math
(X_{\text{interaction}},I)
```

where:

```text
I = independently observed mobile intent
X_interaction = complete attributable source-defined interaction capture
```

Every observation additionally carries non-feature metadata required for dependence-aware analysis:

```text
dataset_id
device_id
manufacturer/category where documented
network_topology where documented
source_capture_id
source_group_id / session_id where documented
source timestamp/order
interaction_id
intent_provenance_grade
background_activity_stratum if NO_ACTION
physical pre-state/post-state where independently documented
```

For `NO_ACTION`:

```text
I = NO_ACTION
```

with a source-defined capture interval independently known to contain no control trigger under the locked rule.

Packets/interactions are not treated as independent inferential replicates when they share a source capture, source session/group, or donor/recipient material.

---

# 35. Network Attribution

Only packets attributable to the target IoT endpoint in the source capture are included in the model features.

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

Every complete attributable interaction capture produces exactly 20 network features:

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
19. capture activity span between first and last attributed target-device packet.

If no target-device packet occurs:

```text
packet/byte counts = 0
active span = 0
```

The active representation contains 19 features. The former capture-start-to-first-target-packet latency feature was removed with reason `PRE_MODEL_STRUCTURAL_DEGENERACY`: it was constant across all 9,986 attributable Mon(IoT)r captures under the approved capture-level definition. The filename timestamp was not adopted because its meaning is not independently documented by the source. This correction was made before any model execution or performance result. Capture activity span is not execution duration.

## Representation-Confound Gate

Before any model execution, audit every feature by dataset, physical device, source context and source chronology for constant or near-constant values, capture-procedure domination, trivial source identifiers, obvious ON/OFF collection shortcuts, and site/network-condition shortcuts. The audit explicitly includes packet/byte counts, source-capture duration, and capture activity span. A structurally degenerate or scientifically invalid feature is reported before experiments with the smallest pre-registered correction proposed; no feature is removed because of model performance. The future strict B/I/E tier may use true command-relative latency only when an eligible source supplies a verified trigger boundary.

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

Therefore pure replay that preserves the 19-feature representation may be unobservable and must be treated according to Section 24.5.

### Raw-Metadata Quality-Control Boundary

Fields excluded from the contract model may still be inspected **offline and deterministically** for counterfactual validity. In particular, raw 5-tuples, TCP sequence/acknowledgment state, packet timestamps and capture-resolution metadata may be used only to:

```text
validate source-capture provenance where required
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
X_{\text{interaction}} \in \mathbb{R}^{19}
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
C=I
```

and the target is \(X_{\text{interaction}}\). `NO_ACTION` is included only in analyses for a source that independently supports it.

No raw identifier enters `C`.

---

# 38. Invalid Interaction Rule

An observation is removed from a specific analysis before splitting/modeling if:

```text
intent provenance is missing or ambiguous
target device is ambiguous
required raw capture is corrupted
required complete attributable interaction-capture coverage is incomplete
source capture has an unresolved control/procedure confound under the representation-confound gate
traffic attribution fails
action is outside the locked semantic scope
source split integrity cannot be preserved
NO_ACTION provenance cannot be established for a NO_ACTION-dependent analysis
```

Exclusion counts and frozen reasons are published.

An interaction is not removed because it is difficult for the model.

A clean held-out interaction may remain in the corpus but be ineligible for one specific violation family. Counterfactual ineligibility is recorded using a frozen reason such as:

```text
NO_VALID_COUNTERFACTUAL
SOURCE_METADATA_INSUFFICIENT
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

For each feature, the scaler statistics are computed exclusively from the union of the **training partitions of the currently eligible public-device training clients**.

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
p(X_{\text{interaction}}\mid I)
```

The context vector contains:

```text
3-dimensional intent context

```

The transformed variable contains:

```text
20 source-defined interaction-capture features

```

The contract score is:

```math
s_{\text{contract}}(X_{\text{interaction}},I) = -\log p(X_{\text{interaction}}\mid I)
```

Higher scores indicate greater contract inconsistency.

---

# 41. Model Architecture

The primary conditional flow uses:

```text
19-dimensional interaction-capture target
3-dimensional intent conditioning context
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

# 43. Required Baseline 1 — Action-Agnostic Density

The first baseline estimates:

```math
q_0(X_{\text{interaction}})
```

Intent conditioning is removed.

Its anomaly score is:

```math
s_0(X_{\text{interaction}})=-\log q_0(X_{\text{interaction}})
```

This baseline tests whether independently recorded mobile intent contributes information beyond action-agnostic capture density.

---

# 44. Required Baseline 2 — Intent-Conditioned Density

The second baseline estimates:

```math
q_\theta(X_{\text{interaction}}\mid I)
```

using the same 19-dimensional capture representation and intent-only conditioning as the primary interface.

This is the current primary conditional-density model, retained here to make its interface explicit.

---

# 45. Required Baseline 3 — Direct Action Classification

A discriminative model estimates:

```math
r_\phi(I\mid X_{\text{interaction}})
```

The inconsistency score is:

```math
1-r_\phi(I\mid X_{\text{interaction}})
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

```

using the same fixed interaction-capture representation. Add `NO_ACTION` only where independently reconstructable for that source.

The default baseline is:

```text
One-Class SVM

```

This approximates a conventional command/event-conditioned behavioral detector without federation-specific contract modeling.

---

# 47. Required Baseline 5 — Simple Statistical Contract

For every supported action context, estimate a training-only multivariate profile over \(X_{\text{interaction}}\).

Use a shrinkage covariance estimator and Mahalanobis-style score.

This establishes whether a deep conditional density model is necessary at all.

---

# 48. Required Learning Regimes

The primary contract model is evaluated under three regimes on the same eligible device population.

## Local

Each dataset-defined physical-device client trains exclusively on its own training observations.

## Centralized

All eligible training observations from participating device clients are pooled for an upper-reference training regime.

Calibration and test observations are excluded.

## Federated

Each dataset-defined physical device is treated as one simulated federated client.

The server aggregates model updates with FedAvg.

The same architecture, optimizer, eligible observations and shared training-client normalization rule are used across regimes.

The federated implementation is an experimental simulation over public data, not a live deployment of training software on the original IoT devices.

---

# 49. Federated Configuration

The main FL configuration is:

```text
client = dataset-identified physical IoT device
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

The main study is deliberately a small federation over real-device partitions reconstructed from public traces. It does not claim massive-client scalability, real-network orchestration or on-device training feasibility.

---

# 50. Why FedAvg Remains the Main Aggregator

The scientific question is not:

```text
Which FL optimizer maximizes accuracy?
```

The main question is whether execution-contract knowledge can be collaboratively learned across heterogeneous real-device partitions and whether collaboration provides value when local contract data are limited.

FedAvg therefore remains the fixed reference aggregator.

FedProx, FedYogi, Ditto, FedBN, clustered FL or other alternatives are outside the confirmatory study.

This prevents novelty from drifting into optimizer comparison.

If heterogeneous contract learning fails, alternative FL methods may be discussed as future work but are not introduced post hoc to rescue confirmatory performance.

---

# 51. Training-Budget Comparability and Local-Data Scarcity

For the full-data comparison use comparable optimization exposure:

```text
local model = fixed full-data epoch budget
centralized model = same fixed epoch budget
federated model = fixed rounds × 1 local epoch
```

The exact epoch/round budget is frozen before confirmatory execution.

Final-round parameters are used.

Test performance is never used for checkpoint selection.

## Mandatory Data-Scarcity Collaboration Curve

Repeat local-versus-federated comparison using nested per-device/per-context training budgets drawn only from the training partition:

```text
n = 10
n = 30
n = 60 where every participating client supports it
FULL = all eligible training observations
```

A numerical scarcity level is included only when all device clients in that comparison can supply at least that many independent eligible training interactions for the relevant context. Missing levels are reported rather than filled by duplication.

The subset rule is frozen and source-group aware. For the approved Mon(IoT)r primary tier, `{10,30,60}` uses the fixed 30-client pre-model common-support cohort; `FULL` retains all 37 eligible physical clients. No client is selected or excluded using model performance.

For every available budget report:

```text
local AUROC/AUPRC
federated AUROC/AUPRC
paired federation-minus-local effect
per-device effect
simulated communication cost
```

The `FULL` condition is the confirmatory collaborative comparison. The scarcity curve supports only claims explicitly referencing data scarcity.

---

# 52. Calibration Threshold

Threshold selection is not a research variable.

For a trained detector and participating client with sufficient clean calibration data:

```math
\tau_i=Q_{0.95}(S_{i,\mathrm{cal}})
```

where calibration scores come exclusively from clean genuine contracts in the calibration partition.

Violation samples never influence thresholds.

Threshold-free metrics remain primary.

If a client has insufficient calibration observations for a stable local threshold, use the pre-registered shared training-client calibration rule or mark the threshold-based metric unavailable; do not borrow test labels.

---

# 53. Zero-Shot Threshold and Normalization Rule

During true leave-one-device-out evaluation, no data from the held-out physical-device client may determine:

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

The held-out device's test data are transformed using that retained-client scaler without adaptation.

A separate secondary experiment may allow held-out-device **benign calibration only** after the model and global scaler are frozen.

This is explicitly reported as:

**calibration-only adaptation**

and must not be confused with zero-shot transfer.

No held-out-device feature normalization is allowed in the main zero-shot result.

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
eligible contract violations
```

They are reported:

```text
overall
per violation type
per physical-device client
per semantic action
per public dataset
```

Cross-dataset metrics are not pooled unless explicitly justified by a separate meta-analytic summary.

---

# 55. Direct Contract Metric

For every clean execution:

```math
(X_{\text{interaction}},I)
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

Report performance separately for every source-feasible family:

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

A strong aggregate metric cannot hide failure or source infeasibility in one category.

For every family report:

```text
number source-feasible
number infeasible and frozen reason
matching-tier distribution
B-context distance distribution relative to the frozen caliper
donor-reuse distribution
source-dependency-cluster count
family-specific artifact-audit status
AUROC
AUPRC
TPR at locked threshold
per-device results
per-dataset availability
```

A representation-unobservable pure replay is a valid negative finding and is never counted as a detected family.

---

# 58. Clean False-Alarm Analysis

For every physical-device client report:

```text
clean FPR
clean score distribution
95th-percentile threshold where available
```

For `NO_ACTION`, when source-feasible, report FPR separately for available background strata:

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

Where manufacturer or network-topology metadata are trustworthy and sufficiently populated, report descriptive subgroup FPR without turning sparse groups into confirmatory claims.

This directly checks that the model has not learned a trivial silence-versus-activity rule.

---

# 59. Contract Heterogeneity Analysis

For each semantic context available in the primary dataset:

```text
NO_ACTION where valid
TURN_ON
TURN_OFF
```

quantify how execution distributions differ across physical-device clients.

At minimum report pairwise:

```text
Wasserstein distance
energy distance
```

on the shared training-client standardized representation.

Also report where metadata support it:

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
which device clients share semantics
which remain distributionally distinct
whether transfer failures may be protocol/source-driven
```

No manufacturer or topology label is invented when the public source does not provide defensible metadata.

---

# 60. Cross-Device and Cross-Manufacturer Generalization

## Leave-One-Device-Out — Main Zero-Shot Protocol

For every eligible device `k` in the primary multi-device dataset:

1. remove all observations of device `k` from model training;
2. remove all observations of device `k` from normalization-statistic computation;
3. remove all observations of device `k` from retained-client threshold calibration;
4. federatively train on the remaining device clients;
5. compute the shared scaler from retained training clients only;
6. compute the main zero-shot threshold from retained-client clean calibration only;
7. evaluate clean and eligible violated contracts on device `k` without target adaptation.

Repeat until every eligible physical-device client has been held out once.

This is genuine unseen-device evaluation **within the source dataset**.

## Source/Topology-Stratified Interpretation

Where network-control topology is documented independently, label and report held-out results by topology.

Where it is not documented, report the source dataset/device identity and do not infer topology from target traffic solely to create a subgroup claim.

## Protocol-Feature Sensitivity

Repeat leave-one-device-out evaluation without features 15–18:

```text
TCP fraction
UDP fraction
unique remote endpoints
unique remote ports
```

This determines whether cross-device results are driven heavily by protocol identity.

## Leave-One-Manufacturer-Out

Perform a secondary leave-one-manufacturer-out evaluation only if:

```text
manufacturer metadata are independently documented
>= 3 manufacturers are represented
remaining training fold has >= 4 physical clients
remaining training fold contains >= 2 manufacturers
```

All devices from the held-out manufacturer are excluded from training, scaling and threshold construction.

If these conditions are not met, manufacturer transfer is simply not claimed.

---

# 61. Cross-Dataset Validation

After the primary dataset protocol is frozen, repeat the same **research formulation** on the next eligible public source.

The purpose is not to pool incompatible datasets.

The purpose is to ask:

> Does independently recorded mobile intent remain useful for execution-contract verification under a different real-device collection protocol?

Cross-dataset validation reports source-specific observation windows, client counts, available violation families, feature availability and provenance quality.

A second dataset need not support every primary analysis to provide useful external evidence, but unsupported components are marked explicitly.

---

# 62. Dataset-Grounded Security-Relevance Evaluation

FedIEC does **not** require physically inducing new failures on devices.

Security relevance is evaluated through three evidence levels:

```text
Level A: artifact-controlled contract counterfactuals from held-out real-device traces
Level B: observed control failures/divergences already documented in a public dataset, if any
Level C: attack-aligned public traces satisfying Section 26, if any
```

Level A is mandatory for counterfactual-based security claims.

Levels B and C are optional because they depend on available public ground truth.

No absence of Level B/C data triggers hardware acquisition or live attack generation.

The final wording must distinguish clearly among:

```text
counterfactual contract violations
observed control failures
real attacks
```

---

# 63. Real-Attack Evaluation

If a valid attack-aligned public dataset is available, evaluate:

```text
clean execution under known intent
versus
attacked execution under the same known intent
```

The applicable primary score remains:

```math
-\log p(X_{\text{interaction}}\mid I)
```

Metrics:

```text
AUROC
AUPRC
TPR at fixed clean-calibration threshold
detection delay if temporally meaningful
```

Real-attack results remain separate from counterfactual results.

If aligned ground truth is unavailable, this section is reported as not evaluated rather than replaced by a synthetic attack claim.

---

# 64. Systems Metrics

For simulated federated training report:

```text
number of rounds
convergence curve
model parameter count
model size
bytes exchanged by the FL protocol per client
total simulated communication bytes
wall-clock training time
peak host memory if measured
```

These are **simulation/system accounting metrics**, not measurements from the original IoT hardware or networks.

No unsupported claims are made about:

```text
battery consumption
Android inference latency
microcontroller feasibility
embedded-device RAM
energy consumption
live WAN latency
on-device training time
```

unless a future separate deployment study measures them directly.

---

# 65. Statistical Unit and Dependence Structure

Training seeds are **not independent experimental units**.

They measure optimization variability only.

For genuine public-source observations, the dependence hierarchy is:

```text
dataset
  └── physical device
       └── source capture/session group where available
            └── interaction / contract observation
                 └── repeated model-seed predictions
```

If a source does not define sessions, use the smallest defensible original capture group instead of inventing a session label.

For generated counterfactuals, every row records:

```text
recipient_source_id
donor_source_id(s)
artifact/control family
generation family
source_dependency_cluster
```

The `source_dependency_cluster` is the connected component obtained by linking generated observations that share any clean source interaction.

Primary uncertainty must never treat multiple derivatives of one source interaction as independent evidence.

For every method:

1. preserve predictions for every interaction and seed;
2. compute seed-specific metrics to describe optimization variability;
3. preserve pairing across compared methods;
4. resample at device/source-group/source-dependency levels supported by the data;
5. report per-device effects in addition to the population summary;
6. report the number of unique physical source interactions underlying every pooled counterfactual result.

Generated sample count is never reported as though it were the number of independent source observations.

---

# 66. Statistical Procedure

For each of the three confirmatory comparisons report:

```text
paired effect estimate
95% paired dependence-aware bootstrap confidence interval
paired cluster-aware randomization/permutation p-value
effect distribution across training seeds
per-device effect
unique-source count for every counterfactual-based result
```

For genuine observations, the bootstrap resamples the highest defensible source units available in the primary dataset:

```text
1. physical devices
2. source capture/session groups within devices, where multiple groups exist
3. interactions within groups
```

For generated counterfactual observations, the lowest level is replaced by `source_dependency_cluster` when shared-source dependence exists.

If the number of device clients is too small for stable population-level hierarchical inference, report exact device-level effects and conservative small-sample intervals/tests rather than pretending large-sample asymptotics apply.

Model seeds remain nested repeated realizations and are summarized separately from physical-device evidence.

Use:

```math
\alpha=0.05
```

Holm correction is applied across the three confirmatory hypothesis comparisons.

Artifact audits use the same dependence-aware principle but apply the pre-registered equivalence-style `A*` criterion from Section 25.

No new significance test is introduced after results are inspected.

---

# 67. Confirmatory Comparison 1 — Intent Value

Compare \(q(X_{\text{interaction}}\mid I)\) versus \(q_0(X_{\text{interaction}})\).

Primary outcome:

```math
\Delta AUROC
```

using the locked source-feasible artifact-controlled contract-violation suite.

The primary effect and uncertainty are computed with the hierarchical procedure in Section 66.

Where source-feasible, background-active `NO_ACTION` observations, replacement/translation controls and—where `EXCESS_EXECUTION` is included—composition controls must be included so the result cannot be explained by silence/activity or transformation artifacts.

---

# 68. Pre-Context Value — Future Secondary Tier

No current dataset executes a primary strict \(p(E\mid B,I)\) population. This comparison is unavailable in the current empirical protocol and may be activated only for a future source with independently supported trigger boundaries and complete B/E coverage.

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

under the `FULL` eligible training-data condition.

Primary outcome:

```math
\Delta AUROC
```

using the dependence-aware procedure in Section 66.

## Mandatory Secondary Scarcity Analysis

Repeat the comparison at every common supported budget among:

```text
n ∈ {10, 30, 60, FULL}
```

per device and semantic context.

Report the federation-minus-local curve and, where at least three numerical levels exist, an area-under-scarcity-curve summary.

A claim that federation is especially useful under local data scarcity requires consistent evidence across the pre-registered available scarcity levels; it cannot be inferred from the full-data comparison alone.

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

This comparison quantifies the federation penalty within the same public-device population.

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
all available NO_ACTION background strata
OMISSION
SUBSTITUTION
UNCOMMANDED_EXECUTION
EXCESS_EXECUTION where source-feasible
TEMPORALLY_MISALIGNED_EXECUTION
semantic-preserving artifact controls
```

Report not only aggregate AUROC but also clean/background FPR, AUPRC per violation family, and classifier calibration.

This answers:

> Is contract verification providing information beyond simply recognizing which action the traffic resembles, especially for open-set/composite executions?

If the classifier performs equivalently or better across this full suite, that result is reported directly.

---

# 72. Required Ablations and Robustness Analyses

The following analyses are pre-registered and mandatory when the underlying source supports them.

## Remove Intent

```math
p(X_{\text{interaction}}\mid I) \rightarrow q_0(X_{\text{interaction}})
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

when at least four eligible device clients support the fold.

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

Using the same frozen model and original source captures, perturb copied intent metadata only:

```text
missing intent: true command relabeled as NO_ACTION for diagnostic evaluation
duplicate intent: duplicate same intent within a frozen interval
```

Timing perturbation is unavailable in the current capture-level tier because no per-capture command boundary is invented. A future strict-tier source may define such a robustness analysis from independently recorded timing.

## Counterfactual Artifact Controls

Report separately:

```text
replacement/translation artifact audit
EXCESS composition artifact audit where feasible
per-feature artifact detectability diagnostics
raw-timeline feasibility diagnostics
matching-tier/caliper diagnostics
source-dependency counts
```

A violation family whose required transformation-specific audit is infeasible or fails cannot support a counterfactual claim for that family.

No additional ablation becomes mandatory after test results are observed.

---

# 73. Derived Evaluation Corpus Contribution Gate

FedIEC no longer claims a newly collected physical benchmark.

The **derived public-data evaluation corpus and protocol** is considered a valid contribution if:

1. every retained dataset/device has an explicit frozen eligibility status;
2. intent provenance is documented independently of evaluated target traffic;
3. raw source identities/checksums or immutable references are recorded;
4. device identities and capture attribution are auditable;
5. source-aware train/calibration/test manifests contain no overlap;
6. source-defined interaction-capture construction is reproducible from raw source material;
7. all available counterfactual violation definitions are reproducible from held-out traces;
8. matching/caliper/boundary rules are frozen before main violation results;
9. donor assignment/reuse and source-dependency manifests are frozen;
10. every claimed transformation family passes its required artifact audit;
11. source-infeasible families are disclosed rather than replaced by weaker post-hoc transformations;
12. processing code and derived metadata manifests are releaseable where licensing permits.

A negative model result does not invalidate a correctly constructed evaluation protocol.

The contribution must be described as a **derived/harmonized evaluation layer over existing public real-device datasets**, not as a newly captured IoT traffic dataset.

---

# 74. Contract-Signal Claim Gate

The statement:

> Explicit mobile intent provides a useful network execution-consistency signal.

requires on the primary eligible dataset:

1. median intent-conditioned interaction-contract AUROC ≥ 0.70;
2. lower bound of the 95% dependence-aware confidence interval > 0.50;
3. direct contract-consistency accuracy ≥ 0.70 where the paired metric is defined;
4. intent-conditioned model outperforming the action-agnostic density baseline in the confirmatory paired analysis;
5. every transformation-specific artifact audit required by the evaluated violation suite passing its frozen criterion;
6. background-active `NO_ACTION` FPR reported whenever valid active-background windows exist.

If these conditions fail, the signal is reported as weak or unsupported under the evaluated source conditions.

---

# 75. Pre-Context Claim Gate — Future Secondary Tier

No pre-context claim is available for the current four-dataset empirical study. A future strict \(p(E\mid B,I)\) source requires independently supported B/E boundaries, complete coverage, a source-order audit and a pre-registered paired comparison before this gate can be activated.

---

# 76. Federated Learnability Claim Gate

The statement:

> Intent–execution contracts can be learned collaboratively across heterogeneous real-device clients represented in public IoT traces.

requires:

1. at least four eligible physical-device clients in the primary source;
2. successful execution in at least 8 of 10 predetermined training seeds;
3. federated median macro-AUROC ≥ 0.70;
4. all clients use the shared training-client normalization rule;
5. per-device results are reported;
6. exact device/manufacturer/category coverage is disclosed rather than implied.

This claim does **not** require federation to outperform local learning.

It is a computational federated-learning claim, not evidence of a live distributed IoT deployment.

---

# 77. Federated Benefit and Scarcity Claim Gate

The statement:

> Federation improves contract verification over isolated local learning.

for the full-data condition requires:

```text
median paired AUROC improvement >= 0.02
95% paired dependence-aware confidence interval excludes 0
Holm-adjusted cluster-aware p < 0.05
```

The stronger statement:

> Federation is particularly useful when individual device clients have limited contract data.

additionally requires the pre-registered available scarcity levels from `{10,30,60,FULL}` to show a consistent positive federation-minus-local effect at low-data levels with uncertainty reported.

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

> The learned contract semantics generalize to unseen physical-device clients within the evaluated public source.

requires:

1. genuine leave-one-device-out evaluation;
2. no held-out-device data used for model training;
3. no held-out-device data used to compute normalization statistics;
4. no held-out-device calibration used for the main zero-shot threshold;
5. median held-out-device AUROC ≥ 0.70;
6. individual results reported for every held-out device;
7. protocol-feature ablation reported;
8. source/dataset boundary stated explicitly.

Failure on one device remains visible.

A separate statement about unseen-manufacturer transfer is permitted only when manufacturer metadata and fold size satisfy Section 60 and the holdout independently passes the same no-leakage rules.

No arbitrary-device or arbitrary-manufacturer generalization claim is permitted.

---

# 80. Violation-Coverage Claim Gate

The statement:

> FedIEC detects multiple classes of intent–execution contract violation.

requires median AUROC ≥ 0.70 for at least three distinct pre-registered **source-feasible and observable** violation families, with dependence-aware uncertainty reported.

A counterfactual family counts only if:

```text
its frozen source/matching/boundary rules were satisfied
its required transformation-specific artifact audit passed
its effective evidence size is reported by unique source interactions/source-dependency clusters
no post-hoc donor-rule relaxation was used
```

For `EXCESS_EXECUTION`, the dedicated composition audit must pass; replacement/translation audit success alone is insufficient.

`PURE_REPLAY_REPRESENTATION_LIMIT` cannot be counted as a detected family unless the locked representation contains an independent differentiating observable.

A source-infeasible family is reported as unavailable, not as a failed detector.

---

# 81. Public-Trace Security-Relevance Gate

The original physically induced security-relevance gate is removed.

The permitted main statement is:

> FedIEC distinguishes source-feasible intent–execution contract violations constructed from held-out real-device traces under artifact-controlled transformations.

This requires:

```text
>= 3 source-feasible violation families where possible
frozen clean-trained model/scaler/threshold
family-specific artifact audits passed
median AUROC >= 0.70 for each claimed family
source dependency reported
```

A stronger statement about **observed control-path failures** requires independently documented failure events already present in a public dataset.

Counterfactual results alone must not be generalized to physically realized attacks or failures.

---

# 82. Real-Attack Claim Gate

The statement:

> FedIEC detects attack-induced intent–execution divergence in the evaluated public trace set.

requires:

1. independently known legitimate intent;
2. actual attack activity independently documented;
3. attack/intent temporal alignment;
4. isolatable target-device execution;
5. median AUROC ≥ 0.70;
6. median TPR ≥ 0.70 at the locked clean-calibration threshold.

Without these conditions, no real-attack claim is made.

---

# 83. Privacy Claim Boundary

The public-dataset-only implementation **does not demonstrate operational privacy**.

The permitted statement is:

> The simulated FL protocol is implemented with device-partitioned training and an FL interface that exchanges model updates rather than examples during training.

However, the researcher has downloaded and stores the public raw datasets centrally for preprocessing and experimentation.

Therefore FedIEC does not claim:

```text
that raw traces physically remained on independent devices
deployment-grade data locality
differential privacy
secure aggregation
homomorphic encryption
membership-inference resistance
gradient-inversion resistance
formal leakage bounds
```

Federation is studied as a collaborative-learning methodology over natural device partitions, not as proof of a privacy-preserving deployment.

---

# 84. Threat Model

The main detector assumes:

```text
source intent provenance is trustworthy for eligible interactions
public raw captures are not maliciously altered after acquisition
training device clients are benign
server follows FedAvg correctly
```

The main study detects divergence between declared intent and observed execution.

It does not defend against an attacker who simultaneously forges both the intent-provenance record and the network execution consistently.

It also does not study training-time poisoning or malicious FL clients.

## Provenance Reliability Boundary

Trusted does not mean perfect.

The main clean corpus uses the source intent timestamp/boundary as recorded or deterministically reconstructed from original tooling. Mandatory robustness analysis evaluates sensitivity to:

```text
timestamp jitter
logging delay
missing intent records
duplicate intent records
```

This characterizes brittleness of the provenance channel without redefining those perturbations as adversarial compromise.

## Dataset-Trust Boundary

FedIEC assumes the original dataset documentation correctly describes device identity and trigger generation. Where source documentation is ambiguous, the corresponding evidence is downgraded or excluded rather than resolved by traffic-based inference.

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
randomly splitting packets from the same interaction across train/test
placing the same source capture/group in multiple partitions
normalization from held-out-device calibration/test data in zero-shot evaluation
normalization from calibration or test observations in the main protocol
model selection using test AUROC
threshold selection from violations or attacks
using device identity as a learned feature
using manufacturer as a learned feature
using IP/MAC as a learned feature
using mobile/controller payload contents as a learned feature
deriving intended action from target-device traffic
selecting datasets or clients based on model performance
selecting violation types after observing results
selecting successful seeds only
changing dataset priority after evaluation
altering violation generation after seeing detector scores
fabricating missing pre-action context
inventing NO_ACTION from low-traffic windows without independent trigger absence
using deterministic source order as an unreported intent proxy
feature-vector splicing for counterfactual generation
using unsupported physical-state assumptions for substitution
relaxing the frozen B-context caliper because no convenient donor exists
ignoring an unresolved source-capture provenance or flow/background mismatch
repairing timestamp collisions with arbitrary epsilon jitter
accepting EXCESS timing/flow artifacts outside the clean training-derived envelope
using replacement/translation audit as evidence that EXCESS composition is artifact-free
changing artifact-audit tolerances after viewing model results
replicating/reusing donors merely to increase sample count
failing to account statistically for generated observations sharing clean sources
silently dropping devices with source/protocol mismatch
claiming live privacy or hardware deployment from a public-data simulation
```

Any violation blocks the corresponding claim until corrected or explicitly downgraded.

---

# 87. Derived-Corpus Integrity Rules

Every retained clean interaction records:

```text
dataset ID
source file/capture reference and checksum where permitted
interaction ID
device/manufacturer/category metadata where documented
source group/session metadata where documented
intent provenance grade
semantic action
source trigger timestamp/boundary
pre/post physical state where independently documented
raw capture coverage status
B/E extraction status
split assignment
```

Every generated contract violation additionally records:

```text
recipient source clean interaction ID
donor source clean interaction ID(s)
source group identifiers
matching tier
transition-compatibility status where applicable
source-capture provenance status
transformation type and violation family
transformation seed if stochastic
temporal alignment transformation
EXCESS composition offset where applicable
shared-flow/TCP compatibility where applicable
raw timing/collision diagnostics where applicable
resulting intent context
resulting execution source
artifact-audit family and status
source_dependency_cluster
```

No counterfactual is generated from training observations.

No calibration observation becomes a violation sample.

No feature-vector-only splice is permitted.

Every transformed sample must be reproducible from source raw material and a manifest.

Missing source metadata produce a frozen insufficiency reason rather than an inferred replacement field.

---

# 88. Reproducibility Requirements

Release where licensing permits:

```text
dataset acquisition instructions
source/version/checksum manifest
intent-provenance audit manifest
device eligibility manifest
raw capture parsing code
feature extraction code
source-aware split manifests
NO_ACTION reconstruction rules where applicable
shared-normalization sufficient-statistic code
counterfactual matching code
deterministic donor-assignment/reuse manifests
transition-semantics checker where metadata support it
source-capture provenance checker
EXCESS raw-timeline composition/feasibility checker
counterfactual-generation manifests
replacement/translation artifact-audit code
EXCESS composition artifact-audit code
source-dependency-cluster manifests
model configs
training seeds
FL configs
data-scarcity sampling manifests
leave-one-device/manufacturer manifests
intent-provenance perturbation manifests
dependence-aware statistical-analysis code
result tables
figure-generation code
```

For restricted public datasets, release:

```text
acquisition instructions
processing manifests
checksums where permitted
derived non-sensitive metadata
source file mapping without redistributed protected raw data
```

Do **not** list Android automation, live capture, device-acquisition or physical-intervention scripts because they are no longer part of the study.

---

# 89. Negative Results

The protocol explicitly permits the following conclusions.

## Intent Adds Little

If the full contract model does not improve over execution-only modeling:

> Explicit mobile intent did not provide sufficient additional detection information under the evaluated conditions.

The derived evaluation protocol remains valid.

## Pre-Context Tier Unavailable

The current empirical study makes no pre-action-context claim. A future source with independently supported B/E boundaries may activate the strict-tier comparison under Section 75.

## Action Classification Is Enough

If direct action classification matches or exceeds contract density modeling across the **full** background and violation suite:

> The evaluated problem can be handled more simply as action-recognition consistency under these conditions.

No artificial superiority claim is made.

## Federation Adds No Benefit

If FL does not improve over local learning, including under the scarcity curve:

> Collaborative training did not provide measurable benefit under the evaluated public-device distributions and sample budgets.

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
independent mobile-intent provenance audit over existing data
public-source eligibility and harmonization protocol
structured violation taxonomy with observability/source-feasibility boundaries
artifact-controlled counterfactual generation protocol
federated device-partition evaluation protocol
data-scarcity collaboration analysis
zero-shot normalization-safe transfer protocol
protocol/source transfer analysis
empirical characterization of which violations and semantics transfer
```

Model superiority controls **which performance claims are permitted**.

Dataset limitations control **which protocol components are supportable**.

Neither justifies inventing missing provenance, collecting unplanned hardware evidence, or strengthening claims beyond the public traces.

---

# 91. Experimental Execution Order

```text
Final literature and novelty audit through current submission date
        ↓
Acquire/download candidate public datasets under their access terms
        ↓
Freeze source versions/checksums
        ↓
Audit intent provenance for PingPong, CIC IoT 2022 and TU Wien
        ↓
Audit physical-device identity, raw capture coverage and source grouping
        ↓
Assign dataset/device eligibility statuses before model evaluation
        ↓
Approve primary confirmatory dataset using the frozen priority + eligibility rule
        ↓
Freeze dataset-specific complete-capture representation and source-capture integrity procedure from source characterization
        ↓
Construct source-aware train/calibration/test manifests
        ↓
Characterize NO_ACTION only where independently supportable and matched
        ↓
Freeze feature extraction
        ↓
Freeze shared training-client normalization
        ↓
Generate clean training/calibration/test artifacts
        ↓
Run the representation-confound audit and compute only source-feasible timing envelopes
        ↓
Freeze deterministic source-aware donor matching and source-capture provenance rules
        ↓
Generate semantic-preserving replacement/translation controls
        ↓
Run replacement/translation artifact audit
        ↓
Generate EXCESS composition controls where source-feasible
        ↓
Run EXCESS composition artifact audit where source-feasible
        ↓
Generate source-feasible artifact-controlled counterfactual suite
        ↓
Build/freeze source-dependency-cluster manifests
        ↓
Run simple statistical baseline
        ↓
Run one-class baseline
        ↓
Run action-agnostic density model
        ↓
Run intent-conditioned capture-density model
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
Run supported n={10,30,60,FULL} data-scarcity comparison
        ↓
Run leave-one-device-out evaluation
        ↓
Run protocol-feature/source-stratified transfer analysis
        ↓
Run leave-one-manufacturer-out only where eligible
        ↓
Run intent-provenance robustness analysis
        ↓
Run independent protocol replication on the next eligible dataset
        ↓
Audit optional real-attack alignment
        ↓
Run real-attack evaluation only if valid
        ↓
Run locked dependence-aware statistical analysis
        ↓
Apply claim gates
        ↓
Write conclusions only from passed gates
```

---

# 92. Explicitly Out of Scope

The confirmatory chapter does not include:

```text
purchasing IoT devices
building a physical smart-home testbed
new packet capture from owned devices
Android UIAutomator / ADB / Appium automation
live companion-app interaction logging
physical command blocking/interruption experiments
secondary-controller physical interventions
live attack generation
automatic APK reverse engineering
automatic semantic-intent extraction from app code
LLM-based intent extraction
voice-assistant commands
actions beyond ON/OFF in the confirmatory scope
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

These may belong to later work but are not required to complete FedIEC.

---

# 93. Relationship to the PhD Thesis

FedIEC remains directly within the doctoral research domain:

```text
collaborative security detection
+
federated learning
+
real IoT devices represented in network datasets
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

The public-dataset-only design changes the **evidence acquisition method**, not the core research domain.

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

Alternative public-data/protocol-oriented title:

> **From Mobile Intent to IoT Execution: Federated Contract Verification Across Public Real-Device Traces**

---

# 96. Proposed Chapter Contribution Statement

The chapter should position its contribution as follows:

> Mobile-controlled IoT security has already been studied through application/user-action context, network behavior, stateful policy enforcement and semantic consistency. FedIEC does not claim the mobile-action-to-network link itself as novel. Instead, it formulates independently recorded mobile intent and a complete attributable source-defined interaction capture as a probabilistic runtime interaction contract. The chapter contributes a provenance- and eligibility-controlled evaluation protocol over public real-device traces, source-feasible artifact-controlled intent–capture counterfactuals, a federated conditional-learning protocol with explicit local-data-scarcity analysis, and leakage-safe unseen-device transfer evaluation with independent cross-dataset replication. It does not claim a newly collected physical benchmark or experimentally induced device failures.

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
Raw traffic remained on independent physical clients in this experiment.
FedIEC demonstrates a live federated IoT deployment.
FedIEC created a new raw physical-device dataset.
Contract counterfactuals are cyberattacks.
Contract counterfactuals are malware.
Pure replay is detectable from the locked representation.
FedIEC generalizes to arbitrary IoT devices.
FedIEC generalizes across manufacturers unless the manufacturer holdout gate passes.
FedIEC is deployable on constrained IoT hardware.
Public-dataset device partitions prove real-world privacy.
```

These statements either contradict the study design or exceed the evidence.

---

# 98. Safe Novelty Wording

Before the final literature audit, use:

> **To the best of the literature reviewed through the current audit date, we did not identify prior work that jointly evaluates independently recorded mobile control intent and complete attributable source-defined interaction captures as a probabilistic IoT interaction contract, learns that contract federatively across natural device partitions from public real-device traces, evaluates source-feasible artifact-controlled intent–capture violations, and tests leakage-safe unseen-device transfer with independent cross-dataset replication.**

The final manuscript must name the closest prior UI/user-action-to-network and semantic enforcement systems rather than implying this relationship was previously unexplored.

After the final audit, this wording may be narrowed further.

It must not be strengthened without evidence.

---

# 99. Proposal-Stage Deliverables

Before the chapter proposal deadline, complete:

```text
current-through-2026 novelty audit
explicit closest-work collision table
final problem formulation
public-dataset evidence hierarchy
PingPong provenance/eligibility audit
CIC IoT 2022 provenance/eligibility audit
TU Wien replication-role audit
device/source eligibility manifest
observation-window and B/E coverage protocol
NO_ACTION reconstruction feasibility audit
violation taxonomy + source-feasibility/observability table
counterfactual anti-artifact protocol
source-aware split specification
zero-shot normalization specification
dependence-aware statistics specification including shared-source clusters
model/baseline specification
final chapter outline
preliminary FedIEC architecture figure
```

Full experimental results are desirable but are not required for the proposal.

---

# 100. Post-Proposal Experimental Deliverables

After proposal submission:

```text
freeze public dataset versions and eligibility manifests
freeze primary confirmatory dataset
freeze source-aware clean splits
freeze observation-window protocol
pass replacement/translation artifact audit for claimed families
pass EXCESS composition audit wherever EXCESS is claimed
generate source-feasible counterfactual suite
complete local/centralized/federated experiments
complete 10 training seeds
complete supported {10,30,60,FULL} scarcity curve
complete leave-one-device-out analysis
complete protocol-feature/source transfer analysis
complete leave-one-manufacturer-out only where feasible
complete intent-provenance robustness analysis
complete independent public-dataset replication
complete optional attack-aligned evaluation only if valid
complete dependence-aware statistical analysis
freeze tables and figures
```

---

# 101. Execution Timeline

## September 17–30, 2026

```text
current-through-2026 novelty audit
closest-work collision matrix
freeze candidate public-dataset priority
complete/verify PingPong acquisition and provenance audit
complete CIC IoT 2022 source/provenance audit
complete TU Wien source/provenance audit
implement raw capture parser + device attribution
implement feature extractor
implement source-aware eligibility manifests
implement counterfactual generator design
```

## October 1–10, 2026

```text
audit raw B/E coverage
freeze candidate dataset-specific W_d procedures
freeze source-group split rules
freeze NO_ACTION reconstruction rules where feasible
freeze shared-normalization protocol
freeze counterfactual matching metric and boundary descriptor
run preprocessing smoke tests
```

## October 11–23, 2026

```text
complete primary-dataset eligibility decision before model results
build initial derived clean corpus
run replacement/translation artifact-control smoke tests
run EXCESS composition smoke tests where feasible
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
freeze clean train/calibration/test manifests
compute training-only B-context calipers and timing envelopes
run transformation-specific artifact audits
freeze donor/source-dependency manifests
freeze source-feasible violation suite
complete baseline experiments
complete primary local/centralized/federated runs
```

## November 21–December 15, 2026

```text
complete all 10 training seeds
complete data-scarcity curve
leave-one-device-out
protocol-feature/source-stratified transfer analysis
leave-one-manufacturer-out where eligible
intent-provenance robustness
independent second-dataset replication
optional attack-aligned evaluation if eligibility passes
dependence-aware statistics
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
source-feasibility and observability-boundary discussion
```

## January 11–15, 2027

```text
final novelty audit through submission date
citation audit
claim-gate audit
counterfactual artifact-audit review
zero-shot leakage audit
statistical-unit audit
public-source provenance audit
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
public-source trust boundary
pre/post context
contract
observability boundary
source-feasibility boundary
violation taxonomy
```

## 4. Public Datasets and Derived FedIEC Evaluation Corpus

Describe:

```text
PingPong
CIC IoT 2022
TU Wien Philips Hue
source versions and licensing
intent-provenance audit
device eligibility
raw capture coverage
source-aware splits
NO_ACTION reconstruction where feasible
observation-window rules
counterfactual matching/calipers and boundary controls
artifact audits
reproducibility manifests
```

## 5. Federated Contract Learning

Describe:

```math
p(X_{\text{interaction}}\mid I)
```

shared training-client normalization, local/centralized/federated regimes and data-scarcity protocol.

## 6. Experimental Methodology

Describe baselines, metrics, seeds, dependence-aware statistics, provenance robustness and claim gates.

## 7. Results

Present:

```text
intent value
future strict-tier pre-context analysis only where an eligible source supports it
federated performance
data-scarcity collaboration curve
heterogeneity
violation-specific results
background false alarms
transformation-specific artifact audits
```

## 8. Cross-Device and Cross-Dataset Validation

Present:

```text
leave-one-device-out
protocol-feature ablation
manufacturer/topology analysis where metadata support it
independent replication dataset
```

## 9. Security-Relevance Evaluation

Present:

```text
artifact-controlled contract counterfactuals
observed control failures if public ground truth exists
real attacks only where alignment gate passes
```

Keep these evidence levels separate.

## 10. Discussion and Limitations

Discuss:

```text
trusted source provenance
provenance jitter sensitivity
public-dataset selection boundaries
device/manufacturer scope
ON/OFF semantic scope
missing pre-action/background data
counterfactual realism
pure-replay observability limit
protocol/source transfer boundary
federation scale
simulation-vs-deployment boundary
formal privacy limitations
```

## 11. Reproducibility and Future Research

Discuss code/manifests, dataset acquisition instructions and future extension to new physical collection only as optional later work.

## 12. Conclusion

State only claims that pass the locked gates.

---

# 103. Final Contribution Hierarchy

The final chapter should prioritize contributions in this order.

### Contribution 1 — Problem Formulation

**Probabilistic intent–execution contract verification for mobile-controlled IoT using independently observed intent and available pre-action context.**

### Contribution 2 — Public-Data Provenance and Evaluation Protocol

**A reproducible eligibility, provenance, split and harmonization protocol that turns existing real-device mobile-control traces into device-partitioned intent–execution contract observations without deriving intent from target traffic.**

### Contribution 3 — Artifact-Controlled Violation Protocol

**A source-aware transformation methodology with common-support matching, boundary/timeline validation, donor-dependence control and explicit source-feasibility/observability limits.**

### Contribution 4 — Federated Methodology

**A federated conditional execution model with a pre-registered data-scarcity analysis establishing when collaborative learning helps relative to isolated local training.**

### Contribution 5 — Generalization Evidence

**Leakage-safe leave-one-device-out and protocol-feature sensitivity analysis, plus manufacturer/topology analysis where metadata permit and independent cross-dataset replication.**

### Contribution 6 — Empirical Security Findings

**A violation-specific characterization identifying which classes of execution divergence are detectable, provenance-sensitive, source-infeasible, representation-unobservable or difficult to generalize.**

The chapter's novelty therefore does not rest exclusively on the conditional flow outperforming a baseline or on creating new hardware data.

---

# 104. Intended Scientific Contribution

If the relevant claim gates pass, the strongest permitted contribution is:

> **FedIEC formulates mobile-controlled IoT security as federated probabilistic intent–interaction contract learning rather than claiming novelty for the already-studied link between user actions and network behavior. It links independently recorded mobile intent with complete attributable source-defined interaction captures from public real-device traces; constructs a reproducible provenance- and eligibility-controlled evaluation corpus; evaluates source-feasible artifact-controlled contract violations; learns contracts locally, centrally and federatively; quantifies when federation helps under local data scarcity; and tests leakage-safe unseen-device transfer with independent cross-dataset replication.**

If model-performance gates fail, the contribution is narrowed to the formulation, public-data protocol, artifact-controlled evaluation methodology and empirically demonstrated feasibility/transfer boundaries.

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
a new physical IoT testbed
a live federated deployment
```

FedIEC investigates a narrower systems question:

> **Can independently recorded mobile intent define a probabilistic interaction contract over complete attributable source-defined captures, verified collaboratively using natural device partitions from public real-device traces; when does federation add value under limited local data; and which parts of that contract remain transferable to unseen devices and independent datasets without target-domain leakage?**

That is the research identity around which the proposal, implementation, experiments and final chapter should remain aligned.

---

# 106. Final Protocol-Lock Audit

Before the first confirmatory result is interpreted, every applicable item below must be PASS.

## Novelty Integrity

```text
closest UI/user-action-to-network prior work named explicitly
current-through-submission-date literature search complete
novelty wording does not rely on action→network linkage alone
no newly collected physical benchmark claim
federated contribution includes data-scarcity question
```

## Public-Source Integrity

```text
candidate source versions/checksums frozen
primary-dataset selection based on pre-model eligibility only
intent provenance grade frozen for every retained interaction
device identity auditable
complete attributable interaction-capture coverage audited
source capture/session grouping frozen
NO_ACTION reconstruction independently justified where used
source-aware train/calibration/test split has no overlap
missing metadata are not inferred from target traffic
```

## Counterfactual Integrity

```text
raw-window transformations only
representation-confound audit completed and frozen
source-aware donor hierarchy frozen
transition semantics required only where independently verifiable
strict B/E boundary checks used only for a future strict-tier source
internal timing and packet order preserved
no epsilon-jitter repair of infeasible timestamps
EXCESS uses legitimate active background material where source-feasible
EXCESS raw-timeline collision/short-gap/shared-flow checks pass
replacement/translation artifact audit passes for every claimed family
EXCESS composition artifact audit passes wherever EXCESS is claimed
artifact equivalence tolerance frozen before main results
donor reuse cap and source_dependency_cluster manifests frozen
pure replay observability limit disclosed
source-infeasible families remain unavailable rather than relaxed
```

## Federated / Transfer Integrity

```text
at least four eligible physical-device clients for main federated claim
shared scaler derived only from current training clients
held-out device contributes no normalization statistics
held-out device contributes no main zero-shot threshold data
data-scarcity manifests frozen
leave-one-device-out complete where claim is made
protocol-feature ablation complete
manufacturer/topology claims made only with independently documented metadata
independent dataset replication kept separate from primary training unless pre-registered otherwise
```

## Simulation / Privacy Integrity

```text
public datasets acknowledged as centrally stored by the researcher
federated experiment described as simulation over device partitions
no claim that raw traces physically stayed on independent devices
no formal privacy claim
no live deployment claim
no hardware feasibility claim
```

## Security-Relevance Integrity

```text
counterfactual violations never called real attacks
observed public control failures claimed only with independent ground truth
real attacks claimed only when intent + attack interval + device execution alignment pass
no physically induced failure claim
```

## Statistical Integrity

```text
seeds treated as optimization variability, not independent physical experiments
source/device/capture dependence preserved
all generated observations retain recipient/donor source IDs
shared-source generated observations grouped into source_dependency_clusters
paired dependence-aware bootstrap/permutation procedure implemented
artifact audits use equivalence-style A* criterion
Holm family fixed to the active confirmatory comparisons
per-device effects and unique-source counts always reported
small client counts handled conservatively
```

## Claim Integrity

```text
all claim gates evaluated mechanically
negative results retained
source/protocol confounds separated from semantic conclusions
representation-unobservable failures reported as limits
source-infeasible analyses reported as unavailable
no post-hoc rescue of model, features, datasets, devices, actions or violation definitions
```

Any PARTIAL or FAIL item must be resolved before the corresponding confirmatory claim is made. If it cannot be resolved, the claim is narrowed rather than the protocol weakened.
