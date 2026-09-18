from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor

from fediec.config import load_config
from fediec.datasets.representation import interaction_feature_order
from fediec.enums import NetworkExecutionFeature
from fediec.types import FeatureVectors


@dataclass(frozen=True)
class TrainingOnlyScaler:
    mean: Tensor
    standard_deviation: Tensor


def feature_tensor(vectors: FeatureVectors) -> Tensor:
    return torch.tensor(tuple(vector.values for vector in vectors), dtype=torch.float32)


def apply_locked_transforms(values: Tensor) -> Tensor:
    transformed = values.clone()
    magnitude_features = set(load_config().features.log1p_magnitude_features)
    for index, feature in enumerate(interaction_feature_order()):
        if feature in magnitude_features:
            transformed[:, index] = torch.log1p(transformed[:, index])
    return transformed


def fit_training_only_scaler(training_values: Tensor) -> TrainingOnlyScaler:
    if training_values.ndim != 2 or training_values.shape[0] == 0:
        raise ValueError("training-only scaler requires at least one two-dimensional training row")
    training_mean = training_values.mean(dim=0)
    population_variance = ((training_values - training_mean) ** 2).mean(dim=0)
    standard_deviation = population_variance.sqrt().clamp_min(torch.finfo(torch.float32).eps)
    return TrainingOnlyScaler(mean=training_mean, standard_deviation=standard_deviation)


def transform_with_scaler(values: Tensor, scaler: TrainingOnlyScaler) -> Tensor:
    if values.ndim != 2 or values.shape[1] != scaler.mean.shape[0]:
        raise ValueError("feature matrix does not match the locked scaler schema")
    return (values - scaler.mean) / scaler.standard_deviation


def has_only_locked_log_transforms() -> bool:
    allowed = set(load_config().features.log1p_magnitude_features)
    rates = set(load_config().features.rate_features)
    return not allowed.intersection(rates) and all(
        feature in set(NetworkExecutionFeature) for feature in allowed
    )
