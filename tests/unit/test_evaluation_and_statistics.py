from __future__ import annotations

import torch

from fediec.enums import (
    HeterogeneityStratum,
    LearningRegimeOutcome,
    ScoringMethod,
    SemanticAction,
)
from fediec.evaluation.heterogeneity import pairwise_group_distances
from fediec.statistics.comparison import holm_correction, paired_effect_estimate
from fediec.types import CheckDetail, DeviceId, InteractionId, PredictionRecord, SourceGroupId


def _records(
    device: str,
    seed: int,
    method: ScoringMethod,
    clean_scores: tuple[float, ...],
    violation_scores: tuple[float, ...],
) -> tuple[PredictionRecord, ...]:
    records: list[PredictionRecord] = []
    for index, score in enumerate((*clean_scores, *violation_scores)):
        is_violation = index >= len(clean_scores)
        records.append(
            PredictionRecord(
                interaction_id=InteractionId(f"{device}-{seed}-{method}-{index}"),
                device_id=DeviceId(device),
                source_group_id=SourceGroupId(f"{device}-{seed}-{index}"),
                semantic_action=SemanticAction.TURN_ON,
                seed=seed,
                scoring_method=method,
                regime=LearningRegimeOutcome.CENTRALIZED,
                is_violation=is_violation,
                score=score,
            )
        )
    return tuple(records)


def _two_device_two_seed_predictions(
    method: ScoringMethod, clean_scores: tuple[float, ...], violation_scores: tuple[float, ...]
) -> tuple[PredictionRecord, ...]:
    predictions: list[PredictionRecord] = []
    for device in ("device-a", "device-b"):
        for seed in (0, 1):
            predictions.extend(_records(device, seed, method, clean_scores, violation_scores))
    return tuple(predictions)


def test_holm_correction_matches_manual_step_down() -> None:
    adjusted = holm_correction((0.01, 0.02, 0.03))
    assert adjusted == (0.03, 0.04, 0.04)
    assert holm_correction(()) == ()


def test_paired_effect_estimate_favors_separable_method() -> None:
    left = _two_device_two_seed_predictions(
        ScoringMethod.INTENT_CONDITIONED_FLOW, (0.1, 0.2), (0.8, 0.9)
    )
    right = _two_device_two_seed_predictions(
        ScoringMethod.ACTION_AGNOSTIC_DENSITY, (0.4, 0.5), (0.45, 0.55)
    )
    estimate = paired_effect_estimate(left, right, CheckDetail("intent-value"))
    assert estimate.point_estimate > 0.2
    assert estimate.confidence_interval_low <= estimate.confidence_interval_high
    assert 0.0 <= estimate.permutation_p_value <= 1.0
    assert len(estimate.per_device_effects) == 2
    assert all(effect.effect > 0 for effect in estimate.per_device_effects)
    expected_unique = len({record.interaction_id for record in (*left, *right)})
    assert estimate.unique_source_interaction_count == expected_unique


def test_heterogeneity_distance_is_zero_for_identical_groups_and_positive_otherwise() -> None:
    same = torch.zeros((5, 3))
    groups_same = (
        (CheckDetail("a"), same),
        (CheckDetail("b"), same.clone()),
    )
    records_same = pairwise_group_distances(
        groups_same, HeterogeneityStratum.PHYSICAL_DEVICE, CheckDetail("all")
    )
    assert all(record.distance == 0.0 for record in records_same)

    different = torch.ones((5, 3)) * 10.0
    groups_different = (
        (CheckDetail("a"), same),
        (CheckDetail("b"), different),
    )
    records_different = pairwise_group_distances(
        groups_different, HeterogeneityStratum.PHYSICAL_DEVICE, CheckDetail("all")
    )
    assert all(record.distance > 0.0 for record in records_different)
