from __future__ import annotations

from dataclasses import dataclass

import numpy
import torch
from sklearn.metrics import average_precision_score, roc_auc_score
from torch import Tensor

from fediec.config import load_config
from fediec.types import MINIMUM_DENOMINATOR, MetricValue, SampleWeight, Score


def area_under_roc(
    labels: tuple[bool, ...],
    scores: tuple[Score, ...],
    sample_weight: tuple[SampleWeight, ...] | None = None,
) -> MetricValue:
    label_array = numpy.asarray(labels, dtype=float)
    if label_array.min() == label_array.max():
        raise ValueError("AUROC requires both clean and violation observations")
    weight_array = numpy.asarray(sample_weight, dtype=float) if sample_weight else None
    return float(
        roc_auc_score(label_array, numpy.asarray(scores, dtype=float), sample_weight=weight_array)
    )


def area_under_precision_recall(
    labels: tuple[bool, ...],
    scores: tuple[Score, ...],
    sample_weight: tuple[SampleWeight, ...] | None = None,
) -> MetricValue:
    label_array = numpy.asarray(labels, dtype=float)
    if label_array.min() == label_array.max():
        raise ValueError("AUPRC requires both clean and violation observations")
    weight_array = numpy.asarray(sample_weight, dtype=float) if sample_weight else None
    return float(
        average_precision_score(
            label_array, numpy.asarray(scores, dtype=float), sample_weight=weight_array
        )
    )


def calibration_threshold(clean_calibration_scores: Tensor) -> Tensor:
    if clean_calibration_scores.ndim != 1 or clean_calibration_scores.shape[0] == 0:
        raise ValueError("threshold calibration requires clean one-dimensional score observations")
    return torch.quantile(clean_calibration_scores, load_config().calibration.threshold_quantile)


@dataclass(frozen=True)
class ThresholdMetricSummary:
    balanced_accuracy: Tensor
    true_positive_rate: Tensor
    false_positive_rate: Tensor
    precision: Tensor


def threshold_metrics(
    anomaly_scores: Tensor, anomaly_labels: Tensor, threshold: Tensor
) -> ThresholdMetricSummary:
    if anomaly_scores.ndim != 1 or anomaly_labels.shape != anomaly_scores.shape:
        raise ValueError(
            "threshold metrics require aligned one-dimensional score and label tensors"
        )
    predictions = anomaly_scores >= threshold
    positives = anomaly_labels.to(dtype=torch.bool)
    negatives = ~positives
    true_positive = (predictions & positives).sum()
    false_positive = (predictions & negatives).sum()
    false_negative = ((~predictions) & positives).sum()
    true_negative = ((~predictions) & negatives).sum()
    positive_denominator = (true_positive + false_negative).clamp_min(MINIMUM_DENOMINATOR)
    negative_denominator = (true_negative + false_positive).clamp_min(MINIMUM_DENOMINATOR)
    precision_denominator = (true_positive + false_positive).clamp_min(MINIMUM_DENOMINATOR)
    true_positive_rate = true_positive / positive_denominator
    false_positive_rate = false_positive / negative_denominator
    precision = true_positive / precision_denominator
    return ThresholdMetricSummary(
        balanced_accuracy=(true_positive_rate + (1 - false_positive_rate)) / 2,
        true_positive_rate=true_positive_rate,
        false_positive_rate=false_positive_rate,
        precision=precision,
    )
