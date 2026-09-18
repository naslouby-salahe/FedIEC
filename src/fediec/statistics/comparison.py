from __future__ import annotations

from collections import Counter, defaultdict

import numpy
from numpy.random import default_rng

from fediec.config import load_config
from fediec.evaluation.metrics import area_under_roc
from fediec.statistics.resampling import device_sign_flip, resample_interaction_weights
from fediec.types import (
    CheckDetail,
    DeviceId,
    EffectSize,
    InteractionId,
    MetricValue,
    PairedEffectEstimate,
    PerDeviceEffect,
    PredictionRecord,
    Seed,
    SignificanceLevel,
)


def _weighted_auroc(
    records: tuple[PredictionRecord, ...], weights: Counter[InteractionId] | None = None
) -> MetricValue:
    kept = (
        records
        if weights is None
        else tuple(record for record in records if weights[record.interaction_id] > 0)
    )
    sample_weight = (
        None
        if weights is None
        else tuple(float(weights[record.interaction_id]) for record in kept)
    )
    if not kept:
        raise ValueError("AUROC requires both clean and violation observations")
    labels = tuple(record.is_violation for record in kept)
    scores = tuple(record.score for record in kept)
    return area_under_roc(labels, scores, sample_weight)


def _group_by_seed(
    records: tuple[PredictionRecord, ...],
) -> tuple[tuple[Seed, tuple[PredictionRecord, ...]], ...]:
    buckets: dict[Seed, list[PredictionRecord]] = defaultdict(list)
    for record in records:
        buckets[record.seed].append(record)
    return tuple((seed, tuple(group)) for seed, group in buckets.items())


def _group_by_device(
    records: tuple[PredictionRecord, ...],
) -> tuple[tuple[DeviceId, tuple[PredictionRecord, ...]], ...]:
    buckets: dict[DeviceId, list[PredictionRecord]] = defaultdict(list)
    for record in records:
        buckets[record.device_id].append(record)
    return tuple((device, tuple(group)) for device, group in buckets.items())


def holm_correction(p_values: tuple[SignificanceLevel, ...]) -> tuple[SignificanceLevel, ...]:
    if not p_values:
        return ()
    order = sorted(range(len(p_values)), key=lambda index: p_values[index])
    total = len(p_values)
    adjusted = [0.0] * total
    running_max = 0.0
    for rank, index in enumerate(order):
        running_max = max(running_max, min(1.0, (total - rank) * p_values[index]))
        adjusted[index] = running_max
    return tuple(adjusted)


def paired_effect_estimate(
    left: tuple[PredictionRecord, ...],
    right: tuple[PredictionRecord, ...],
    comparison_label: CheckDetail,
) -> PairedEffectEstimate:
    if not left or not right:
        raise ValueError("a paired effect estimate requires non-empty prediction sets")
    left_method = left[0].scoring_method
    right_method = right[0].scoring_method
    seeds = tuple(sorted({record.seed for record in left}))
    if seeds != tuple(sorted({record.seed for record in right})):
        raise ValueError("a paired comparison requires identical seed sets for both methods")

    point_estimate: EffectSize = _weighted_auroc(left) - _weighted_auroc(right)

    left_by_seed = dict(_group_by_seed(left))
    right_by_seed = dict(_group_by_seed(right))
    seed_effects = tuple(
        _weighted_auroc(left_by_seed[seed]) - _weighted_auroc(right_by_seed[seed])
        for seed in seeds
    )

    left_by_device = dict(_group_by_device(left))
    right_by_device = dict(_group_by_device(right))
    device_deltas: dict[DeviceId, EffectSize] = {}
    for device in tuple(sorted(set(left_by_device) & set(right_by_device))):
        try:
            device_deltas[device] = _weighted_auroc(left_by_device[device]) - _weighted_auroc(
                right_by_device[device]
            )
        except ValueError:
            continue
    per_device_effects = tuple(
        PerDeviceEffect(
            device_id=device,
            effect=delta,
            sample_count=len(left_by_device[device]),
        )
        for device, delta in sorted(device_deltas.items())
    )

    statistics_config = load_config().statistics
    rng = default_rng(int(seeds[0]))
    bootstrap_deltas: list[EffectSize] = []
    for _ in range(statistics_config.bootstrap_replicates):
        weights = resample_interaction_weights(left, rng)
        try:
            bootstrap_deltas.append(
                _weighted_auroc(left, weights) - _weighted_auroc(right, weights)
            )
        except ValueError:
            continue
    if bootstrap_deltas:
        confidence_low, confidence_high = numpy.percentile(bootstrap_deltas, (2.5, 97.5))
    else:
        confidence_low = confidence_high = point_estimate

    observed_cluster_statistic = (
        float(numpy.mean(tuple(device_deltas.values()))) if device_deltas else point_estimate
    )
    permutation_rng = default_rng(int(seeds[0]) + 1)
    devices = tuple(sorted(device_deltas))
    exceed_total = 0
    permutation_replicates = statistics_config.bootstrap_replicates
    if devices:
        for _ in range(permutation_replicates):
            signs_by_device = dict(device_sign_flip(devices, permutation_rng))
            permuted = float(
                numpy.mean(
                    tuple(device_deltas[device] * signs_by_device[device] for device in devices)
                )
            )
            if abs(permuted) >= abs(observed_cluster_statistic):
                exceed_total += 1
        permutation_p_value = min(1.0, (exceed_total + 1) / (permutation_replicates + 1))
    else:
        permutation_p_value = 1.0

    unique_interaction_ids = {
        record.source_dependency_cluster or record.interaction_id for record in (*left, *right)
    }

    return PairedEffectEstimate(
        comparison_label=comparison_label,
        left_method=left_method,
        right_method=right_method,
        point_estimate=point_estimate,
        confidence_interval_low=float(confidence_low),
        confidence_interval_high=float(confidence_high),
        permutation_p_value=permutation_p_value,
        seed_effects=seed_effects,
        per_device_effects=per_device_effects,
        unique_source_interaction_count=len(unique_interaction_ids),
    )


def apply_holm_correction(
    estimates: tuple[PairedEffectEstimate, ...],
) -> tuple[PairedEffectEstimate, ...]:
    adjusted = holm_correction(tuple(estimate.permutation_p_value for estimate in estimates))
    return tuple(
        estimate.model_copy(update={"holm_adjusted_p_value": adjusted_value})
        for estimate, adjusted_value in zip(estimates, adjusted, strict=True)
    )


__all__ = [
    "apply_holm_correction",
    "holm_correction",
    "paired_effect_estimate",
]
