from __future__ import annotations

from fediec.enums import DatasetAvailability, DatasetSource
from fediec.paths import resolve_dataset_raw_root


def describe_raw_availability() -> DatasetAvailability:
    raw_root = resolve_dataset_raw_root(DatasetSource.CIC_IOT_2022)
    if not raw_root.exists() or not any(raw_root.iterdir()):
        return DatasetAvailability.MISSING_EXTERNAL
    return DatasetAvailability.PRESENT_AND_VALID
