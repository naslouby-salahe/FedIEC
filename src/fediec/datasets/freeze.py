from __future__ import annotations

from collections import Counter

from fediec.config import load_config
from fediec.datasets.representation import interaction_feature_order
from fediec.enums import (
    ArtifactAuditFamily,
    CounterfactualFeasibility,
    DatasetSource,
    SplitPartition,
    ViolationFamily,
)
from fediec.types import (
    ArtifactControlRecord,
    CheckDetail,
    CleanSplitManifest,
    CounterfactualFeasibilityRecord,
    FrozenClientActionCount,
    ProtocolFreezeManifest,
    RepresentationConfoundAudit,
)


def build_protocol_freeze(
    split_manifest: CleanSplitManifest,
    representation_audit: RepresentationConfoundAudit,
) -> ProtocolFreezeManifest:
    if split_manifest.dataset_source is not DatasetSource.MONIOTR_IMC_2019:
        raise ValueError("only the approved Mon(IoT)r primary source can be frozen")
    if not representation_audit.passed:
        raise ValueError("protocol freeze requires a passing representation-confound audit")
    configuration = load_config()
    assignments = split_manifest.assignments
    count_by_client_action_partition = Counter(
        (assignment.device_id, assignment.semantic_action, assignment.partition)
        for assignment in assignments
    )
    client_actions = tuple(
        FrozenClientActionCount(
            device_id=device_id,
            semantic_action=action,
            training_count=count_by_client_action_partition[
                (device_id, action, SplitPartition.TRAINING)
            ],
            calibration_count=count_by_client_action_partition[
                (device_id, action, SplitPartition.CALIBRATION)
            ],
            test_count=count_by_client_action_partition[(device_id, action, SplitPartition.TEST)],
        )
        for device_id, action in sorted(
            {(assignment.device_id, assignment.semantic_action) for assignment in assignments}
        )
    )
    physical_clients = tuple(sorted({assignment.device_id for assignment in assignments}))
    actions = tuple(sorted({count.semantic_action for count in client_actions}))
    scarcity_clients = tuple(
        client
        for client in physical_clients
        if all(
            count_by_client_action_partition[(client, action, SplitPartition.TRAINING)]
            >= max(configuration.federated.scarcity_budgets)
            for action in actions
        )
    )
    supported_budgets = tuple(
        budget
        for budget in configuration.federated.scarcity_budgets
        if all(
            count_by_client_action_partition[(client, action, SplitPartition.TRAINING)] >= budget
            for client in scarcity_clients
            for action in actions
        )
    )
    return ProtocolFreezeManifest(
        dataset_source=DatasetSource.MONIOTR_IMC_2019,
        role=configuration.public_sources.moniotr_imc_2019.role,
        eligible_capture_count=len(assignments),
        eligible_physical_client_count=len(physical_clients),
        client_action_counts=client_actions,
        source_group_count=len({assignment.source_group_id for assignment in assignments}),
        source_group_overlap_free=len({assignment.source_group_id for assignment in assignments})
        == len(assignments),
        network_condition_treatment=CheckDetail(
            "LAN/WAN and VPN status remain source contexts; they are not client identities "
            "or model inputs"
        ),
        feature_order=interaction_feature_order(),
        context_dimension=configuration.model.context_dimension,
        supported_scarcity_budgets=supported_budgets,
        scarcity_eligible_client_count=len(scarcity_clients),
        full_eligible_client_count=len(physical_clients),
        holdout_definition=CheckDetail(
            "hold out one physical device instance; US and UK instances remain distinct"
        ),
        normalization_protocol=CheckDetail(
            "derive transforms from training partition only; share identical transforms across "
            "local, centralized, and federated comparisons"
        ),
        model_interface=CheckDetail("q_theta(X_interaction | I): target=19, intent condition=3"),
        baseline_interfaces=(
            CheckDetail("q(X_interaction)"),
            CheckDetail("q(X_interaction | I)"),
            CheckDetail("P(I | X_interaction)"),
            CheckDetail("per-action one-class q_a(X_interaction), NO_ACTION source-gated"),
        ),
        supported_violation_families=(),
        counterfactual_feasibility=(
            CounterfactualFeasibilityRecord(
                violation_family=ViolationFamily.OMISSION,
                feasibility=CounterfactualFeasibility.SOURCE_INFEASIBLE,
                reason=CheckDetail("requires independently matched NO_ACTION, unavailable"),
            ),
            CounterfactualFeasibilityRecord(
                violation_family=ViolationFamily.SUBSTITUTION,
                feasibility=CounterfactualFeasibility.SOURCE_INFEASIBLE,
                reason=CheckDetail(
                    "source transition compatibility is not independently documented"
                ),
            ),
            CounterfactualFeasibilityRecord(
                violation_family=ViolationFamily.UNCOMMANDED_EXECUTION,
                feasibility=CounterfactualFeasibility.SOURCE_INFEASIBLE,
                reason=CheckDetail("requires independently matched NO_ACTION, unavailable"),
            ),
            CounterfactualFeasibilityRecord(
                violation_family=ViolationFamily.EXCESS_EXECUTION,
                feasibility=CounterfactualFeasibility.ARTIFACT_AUDIT_INSUFFICIENT,
                reason=CheckDetail(
                    "natural concurrency and raw-timeline composition controls are not "
                    "source-verified"
                ),
            ),
            CounterfactualFeasibilityRecord(
                violation_family=ViolationFamily.REPLAY_OR_LATE_EXECUTION,
                feasibility=CounterfactualFeasibility.REPRESENTATION_UNOBSERVABLE,
                reason=CheckDetail(
                    "no independent trigger boundary supports late-execution alignment; "
                    "pure replay is unobservable"
                ),
            ),
        ),
        artifact_control_plan=(
            ArtifactControlRecord(
                artifact_audit_family=ArtifactAuditFamily.REPLACEMENT_TRANSLATION,
                feasibility=CounterfactualFeasibility.ARTIFACT_AUDIT_INSUFFICIENT,
                pass_rule=CheckDetail(
                    "A*=max(AUROC,1-AUROC); upper dependence-aware 95% CI <=0.60; "
                    "no device >0.70; no feature >0.65"
                ),
                reason=CheckDetail(
                    "no source-feasible replacement or translation family is frozen"
                ),
            ),
            ArtifactControlRecord(
                artifact_audit_family=ArtifactAuditFamily.EXCESS_COMPOSITION,
                feasibility=CounterfactualFeasibility.ARTIFACT_AUDIT_INSUFFICIENT,
                pass_rule=CheckDetail(
                    "raw no-op round-trip exactly reproduces features and all collision, "
                    "timing, shared-flow, and TCP diagnostics pass"
                ),
                reason=CheckDetail(
                    "natural-concurrency evidence is not yet sufficient for a source-feasible "
                    "composition audit"
                ),
            ),
        ),
        unavailable_analysis_reasons=(
            CheckDetail("NO_ACTION is not independently reconstructable"),
            CheckDetail("strict B/I/E requires a verified trigger boundary"),
            CheckDetail("replay and late-execution claims require unavailable timing evidence"),
            CheckDetail("counterfactual violation generation is not yet source-supported"),
        ),
        seeds=configuration.training.seeds,
        statistical_protocol=CheckDetail(
            "alpha=0.05; bootstrap_replicates=2000; report every configured seed"
        ),
        representation_confound_audit_passed=representation_audit.passed,
    )
