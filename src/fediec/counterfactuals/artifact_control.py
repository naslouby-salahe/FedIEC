from __future__ import annotations

import numpy
from numpy.random import default_rng

from fediec.config import load_config
from fediec.enums import ArtifactAuditFamily
from fediec.evaluation.metrics import area_under_roc
from fediec.types import (
    A_STAR_EQUIVALENCE_MIDPOINT,
    P95_QUANTILE,
    ArtifactControlAudit,
    ArtifactDetectabilityBound,
    DeviceId,
    Score,
)


def _a_star(
    genuine_scores: tuple[Score, ...], transformed_scores: tuple[Score, ...]
) -> ArtifactDetectabilityBound:
    if not genuine_scores or not transformed_scores:
        raise ValueError("an artifact-control audit requires genuine and transformed scores")
    labels = (False,) * len(genuine_scores) + (True,) * len(transformed_scores)
    scores = genuine_scores + transformed_scores
    auroc = area_under_roc(labels, scores)
    return max(auroc, 1.0 - auroc)


def run_artifact_control_audit(
    artifact_audit_family: ArtifactAuditFamily,
    genuine_scores_by_device: tuple[tuple[DeviceId, tuple[Score, ...]], ...],
    transformed_scores_by_device: tuple[tuple[DeviceId, tuple[Score, ...]], ...],
    feature_a_stars: tuple[ArtifactDetectabilityBound, ...],
) -> ArtifactControlAudit:
    genuine_by_device = dict(genuine_scores_by_device)
    transformed_by_device = dict(transformed_scores_by_device)
    devices = tuple(sorted(set(genuine_by_device) & set(transformed_by_device)))
    if not devices:
        raise ValueError("artifact-control audit requires matched genuine/transformed devices")
    all_genuine = tuple(score for device in devices for score in genuine_by_device[device])
    all_transformed = tuple(score for device in devices for score in transformed_by_device[device])
    overall_a_star = _a_star(all_genuine, all_transformed)
    device_a_stars = {
        device: _a_star(genuine_by_device[device], transformed_by_device[device])
        for device in devices
    }
    max_device_a_star = max(device_a_stars.values())
    max_feature_a_star = max(feature_a_stars) if feature_a_stars else overall_a_star

    counterfactuals_config = load_config().counterfactuals
    statistics_config = load_config().statistics
    upper_ci_threshold = (
        A_STAR_EQUIVALENCE_MIDPOINT + counterfactuals_config.artifact_audit_tolerance
    )
    rng = default_rng(0)
    bootstrap_a_stars: list[ArtifactDetectabilityBound] = []
    for _ in range(statistics_config.bootstrap_replicates):
        resampled_devices = rng.choice(devices, size=len(devices), replace=True)
        genuine_pool = tuple(
            score for device in resampled_devices for score in genuine_by_device[device]
        )
        transformed_pool = tuple(
            score for device in resampled_devices for score in transformed_by_device[device]
        )
        try:
            bootstrap_a_stars.append(_a_star(genuine_pool, transformed_pool))
        except ValueError:
            continue
    confidence_interval_high = (
        float(numpy.percentile(bootstrap_a_stars, P95_QUANTILE * 100))
        if bootstrap_a_stars
        else overall_a_star
    )

    passed = (
        confidence_interval_high <= upper_ci_threshold
        and max_device_a_star <= counterfactuals_config.artifact_audit_max_individual_device_a_star
        and max_feature_a_star <= counterfactuals_config.artifact_audit_max_per_feature_a_star
    )
    return ArtifactControlAudit(
        artifact_audit_family=artifact_audit_family,
        a_star=overall_a_star,
        confidence_interval_high=confidence_interval_high,
        max_device_a_star=max_device_a_star,
        max_feature_a_star=max_feature_a_star,
        passed=passed,
    )
