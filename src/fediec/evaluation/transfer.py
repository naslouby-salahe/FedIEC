from __future__ import annotations

from torch import Tensor

from fediec.enums import TransferAnalysis
from fediec.evaluation.heterogeneity import protocol_identity_feature_indices
from fediec.types import (
    ZERO_FEATURE_VALUE,
    DeviceCount,
    DeviceId,
    MetricValue,
    SampleCount,
    TransferResult,
)

MINIMUM_HELD_OUT_DEVICE_FOLD_SUPPORT: DeviceCount = 4


def eligible_leave_one_device_out_devices(devices: tuple[DeviceId, ...]) -> tuple[DeviceId, ...]:
    if len(devices) < MINIMUM_HELD_OUT_DEVICE_FOLD_SUPPORT:
        return ()
    return tuple(sorted(set(devices)))


def mask_protocol_identity_features(standardized_features: Tensor) -> Tensor:
    masked = standardized_features.clone()
    masked[:, list(protocol_identity_feature_indices())] = ZERO_FEATURE_VALUE
    return masked


def build_transfer_result(
    analysis: TransferAnalysis,
    held_out_device: DeviceId | None,
    auroc: MetricValue,
    auprc: MetricValue,
    sample_count: SampleCount,
) -> TransferResult:
    return TransferResult(
        analysis=analysis,
        held_out_device=held_out_device,
        auroc=auroc,
        auprc=auprc,
        sample_count=sample_count,
    )
