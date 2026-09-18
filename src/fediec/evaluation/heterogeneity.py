from __future__ import annotations

import numpy
from scipy.stats import energy_distance, wasserstein_distance
from torch import Tensor

from fediec.datasets.representation import interaction_feature_order
from fediec.enums import DistanceMetric, HeterogeneityStratum, NetworkExecutionFeature
from fediec.types import CheckDetail, Distance, FeatureIndex, HeterogeneityDistanceRecord

_PROTOCOL_IDENTITY_FEATURES: tuple[NetworkExecutionFeature, ...] = (
    NetworkExecutionFeature.TCP_FRACTION,
    NetworkExecutionFeature.UDP_FRACTION,
    NetworkExecutionFeature.UNIQUE_REMOTE_ENDPOINTS,
    NetworkExecutionFeature.UNIQUE_REMOTE_PORTS,
)


def protocol_identity_feature_indices() -> tuple[FeatureIndex, ...]:
    order = interaction_feature_order()
    return tuple(order.index(feature) for feature in _PROTOCOL_IDENTITY_FEATURES)


def _mean_marginal_distance(left: Tensor, right: Tensor, metric: DistanceMetric) -> Distance:
    if left.ndim != 2 or right.ndim != 2 or left.shape[1] != right.shape[1]:
        raise ValueError("heterogeneity distance requires aligned two-dimensional feature matrices")
    left_rows = left.detach().cpu().numpy()
    right_rows = right.detach().cpu().numpy()
    distance_function = (
        wasserstein_distance if metric is DistanceMetric.WASSERSTEIN else energy_distance
    )
    per_feature_distances = tuple(
        float(distance_function(left_rows[:, index], right_rows[:, index]))
        for index in range(left_rows.shape[1])
    )
    return float(numpy.mean(per_feature_distances))


def pairwise_group_distances(
    groups: tuple[tuple[CheckDetail, Tensor], ...],
    stratum: HeterogeneityStratum,
    feature_subset: CheckDetail,
) -> tuple[HeterogeneityDistanceRecord, ...]:
    ordered = tuple(sorted(groups, key=lambda group: group[0]))
    records: list[HeterogeneityDistanceRecord] = []
    for left_index, (left_key, left_tensor) in enumerate(ordered):
        for right_key, right_tensor in ordered[left_index + 1 :]:
            for metric in (DistanceMetric.WASSERSTEIN, DistanceMetric.ENERGY):
                distance = _mean_marginal_distance(left_tensor, right_tensor, metric)
                records.append(
                    HeterogeneityDistanceRecord(
                        stratum=stratum,
                        left_key=left_key,
                        right_key=right_key,
                        metric=metric,
                        distance=distance,
                        feature_subset=feature_subset,
                    )
                )
    return tuple(records)


def protocol_feature_distances(
    groups: tuple[tuple[CheckDetail, Tensor], ...],
    stratum: HeterogeneityStratum,
) -> tuple[HeterogeneityDistanceRecord, ...]:
    indices = list(protocol_identity_feature_indices())
    subset_groups = tuple((key, tensor[:, indices]) for key, tensor in groups)
    return pairwise_group_distances(
        subset_groups, stratum, feature_subset=CheckDetail("protocol_identity_features_15_18")
    )
