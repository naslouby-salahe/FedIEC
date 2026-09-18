from __future__ import annotations

from pathlib import Path

import pytest

from fediec.counterfactuals.artifact_control import run_artifact_control_audit
from fediec.counterfactuals.generation import NotSourceFeasibleError, generate_counterfactual
from fediec.counterfactuals.matching import compute_caliper, rank_donor_candidates, within_caliper
from fediec.counterfactuals.validity import (
    physical_timeline_feasible,
    timestamps_strictly_ordered,
    transition_compatible,
)
from fediec.enums import (
    ArtifactAuditFamily,
    CounterfactualFeasibility,
    DatasetSource,
    InfeasibilityReason,
    IntentProvenanceGrade,
    MatchingTier,
    SemanticAction,
    SourceGroupKind,
    TransitionClass,
    ViolationFamily,
)
from fediec.types import (
    CheckDetail,
    CounterfactualFeasibilityRecord,
    DeviceId,
    DonorCandidate,
    InteractionId,
    PublicSourceInteraction,
    RepositoryPath,
    SourceCaptureId,
    SourceContextId,
    SourceGroupId,
)


def test_compute_caliper_selects_the_configured_quantile() -> None:
    caliper = compute_caliper(
        (1.0, 2.0, 3.0, 4.0, 5.0), SemanticAction.TURN_ON, quantile=0.8
    )
    assert caliper.caliper_value == 4.0


def test_rank_donor_candidates_prefers_closer_tier_over_closer_distance() -> None:
    far_same_group = DonorCandidate(
        donor_source_capture_id=SourceCaptureId("far"),
        matching_tier=MatchingTier.TIER_1_SAME_SOURCE_GROUP,
        context_distance=10.0,
    )
    near_other_group = DonorCandidate(
        donor_source_capture_id=SourceCaptureId("near"),
        matching_tier=MatchingTier.TIER_3_OTHER_ELIGIBLE_SOURCE_GROUP,
        context_distance=0.1,
    )
    ranked = rank_donor_candidates((near_other_group, far_same_group))
    assert ranked[0].donor_source_capture_id == SourceCaptureId("far")


def test_within_caliper_boundary() -> None:
    caliper = compute_caliper((1.0, 2.0, 3.0), SemanticAction.TURN_OFF, quantile=0.5)
    inside = DonorCandidate(
        donor_source_capture_id=SourceCaptureId("inside"),
        matching_tier=MatchingTier.TIER_1_SAME_SOURCE_GROUP,
        context_distance=caliper.caliper_value,
    )
    outside = DonorCandidate(
        donor_source_capture_id=SourceCaptureId("outside"),
        matching_tier=MatchingTier.TIER_1_SAME_SOURCE_GROUP,
        context_distance=caliper.caliper_value + 1.0,
    )
    assert within_caliper(caliper, inside)
    assert not within_caliper(caliper, outside)


def test_transition_compatible_only_gates_substitution() -> None:
    assert transition_compatible(TransitionClass.OFF_TO_ON, ViolationFamily.SUBSTITUTION) == (
        True,
        None,
    )
    incompatible, reason = transition_compatible(
        TransitionClass.ON_TO_ON, ViolationFamily.SUBSTITUTION
    )
    assert not incompatible
    assert reason is InfeasibilityReason.COUNTERFACTUAL_INFEASIBLE_TRANSITION
    assert transition_compatible(None, ViolationFamily.OMISSION) == (True, None)


def test_timestamps_strictly_ordered_rejects_collisions() -> None:
    assert timestamps_strictly_ordered((1.0, 2.0, 3.0)) == (True, None)
    ok, reason = timestamps_strictly_ordered((1.0, 1.0, 2.0))
    assert not ok
    assert reason is InfeasibilityReason.COUNTERFACTUAL_INFEASIBLE_BOUNDARY


def test_physical_timeline_feasible_rejects_inverted_spans() -> None:
    assert physical_timeline_feasible((0.0, 1.0), (0.0, 1.0)) == (True, None)
    ok, reason = physical_timeline_feasible((1.0, 0.0), (0.0, 1.0))
    assert not ok
    assert reason is InfeasibilityReason.COUNTERFACTUAL_INFEASIBLE_PHYSICAL_TIMELINE


def test_artifact_control_audit_passes_for_indistinguishable_distributions() -> None:
    genuine = (
        (DeviceId("d1"), (0.1, 0.2, 0.3, 0.4, 0.5)),
        (DeviceId("d2"), (0.15, 0.25, 0.35, 0.45, 0.55)),
    )
    transformed = (
        (DeviceId("d1"), (0.12, 0.22, 0.32, 0.42, 0.52)),
        (DeviceId("d2"), (0.17, 0.27, 0.37, 0.47, 0.57)),
    )
    audit = run_artifact_control_audit(
        ArtifactAuditFamily.REPLACEMENT_TRANSLATION, genuine, transformed, ()
    )
    assert audit.passed


def test_artifact_control_audit_fails_for_separable_distributions() -> None:
    genuine = (
        (DeviceId("d1"), (0.0, 0.0, 0.0, 0.0, 0.0)),
        (DeviceId("d2"), (0.0, 0.0, 0.0, 0.0, 0.0)),
    )
    transformed = (
        (DeviceId("d1"), (10.0, 10.0, 10.0, 10.0, 10.0)),
        (DeviceId("d2"), (10.0, 10.0, 10.0, 10.0, 10.0)),
    )
    audit = run_artifact_control_audit(
        ArtifactAuditFamily.REPLACEMENT_TRANSLATION, genuine, transformed, ()
    )
    assert not audit.passed


def test_generate_counterfactual_fails_closed_for_infeasible_family() -> None:
    record = CounterfactualFeasibilityRecord(
        violation_family=ViolationFamily.OMISSION,
        feasibility=CounterfactualFeasibility.SOURCE_INFEASIBLE,
        reason=CheckDetail("requires independently matched NO_ACTION, unavailable"),
    )
    donor = _minimal_interaction()
    with pytest.raises(NotSourceFeasibleError):
        generate_counterfactual(ViolationFamily.OMISSION, record, donor)


def test_generate_counterfactual_rejects_mismatched_family() -> None:
    record = CounterfactualFeasibilityRecord(
        violation_family=ViolationFamily.OMISSION,
        feasibility=CounterfactualFeasibility.SOURCE_INFEASIBLE,
        reason=CheckDetail("requires independently matched NO_ACTION, unavailable"),
    )
    donor = _minimal_interaction()
    with pytest.raises(ValueError):
        generate_counterfactual(ViolationFamily.SUBSTITUTION, record, donor)


def _minimal_interaction() -> PublicSourceInteraction:
    return PublicSourceInteraction(
        dataset_source=DatasetSource.MONIOTR_IMC_2019,
        interaction_id=InteractionId("i1"),
        device_id=DeviceId("d1"),
        source_capture_id=SourceCaptureId("c1"),
        source_group_id=SourceGroupId("g1"),
        source_group_kind=SourceGroupKind.INDIVIDUAL_CAPTURE,
        source_context_id=SourceContextId("ctx1"),
        semantic_action=SemanticAction.TURN_ON,
        intent_provenance_grade=IntentProvenanceGrade.VERIFIED_PROTOCOL,
        capture_path=RepositoryPath(Path("/nonexistent.pcap")),
    )
