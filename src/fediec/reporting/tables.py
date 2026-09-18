from __future__ import annotations

from pathlib import Path

import polars

from fediec.types import (
    CheckDetail,
    HeterogeneityDistanceRecord,
    PairedEffectEstimate,
    PerDeviceEffect,
    RepositoryPath,
)


def write_comparison_effects_table(
    estimates: tuple[PairedEffectEstimate, ...], path: RepositoryPath
) -> None:
    frame = polars.DataFrame(
        {
            "comparison_label": [str(estimate.comparison_label) for estimate in estimates],
            "left_method": [str(estimate.left_method) for estimate in estimates],
            "right_method": [str(estimate.right_method) for estimate in estimates],
            "point_estimate": [estimate.point_estimate for estimate in estimates],
            "confidence_interval_low": [
                estimate.confidence_interval_low for estimate in estimates
            ],
            "confidence_interval_high": [
                estimate.confidence_interval_high for estimate in estimates
            ],
            "permutation_p_value": [estimate.permutation_p_value for estimate in estimates],
            "holm_adjusted_p_value": [estimate.holm_adjusted_p_value for estimate in estimates],
            "unique_source_interaction_count": [
                estimate.unique_source_interaction_count for estimate in estimates
            ],
        }
    )
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    frame.write_parquet(Path(path))


def write_per_device_effects_table(
    comparison_label: CheckDetail, effects: tuple[PerDeviceEffect, ...], path: RepositoryPath
) -> None:
    frame = polars.DataFrame(
        {
            "comparison_label": [str(comparison_label)] * len(effects),
            "device_id": [str(effect.device_id) for effect in effects],
            "effect": [effect.effect for effect in effects],
            "sample_count": [effect.sample_count for effect in effects],
        }
    )
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    frame.write_parquet(Path(path))


def write_heterogeneity_distances_table(
    records: tuple[HeterogeneityDistanceRecord, ...], path: RepositoryPath
) -> None:
    frame = polars.DataFrame(
        {
            "stratum": [str(record.stratum) for record in records],
            "left_key": [str(record.left_key) for record in records],
            "right_key": [str(record.right_key) for record in records],
            "metric": [str(record.metric) for record in records],
            "distance": [record.distance for record in records],
            "feature_subset": [str(record.feature_subset) for record in records],
        }
    )
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    frame.write_parquet(Path(path))
