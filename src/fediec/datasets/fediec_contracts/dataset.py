from __future__ import annotations

from fediec.enums import DatasetAvailability, DatasetSource
from fediec.paths import (
    resolve_dataset_raw_root,
    resolve_fediec_contracts_required_raw_directories,
)


def describe_raw_availability() -> DatasetAvailability:
    raw_root = resolve_dataset_raw_root(DatasetSource.FEDIEC_CONTRACTS)
    if not raw_root.exists():
        return DatasetAvailability.MISSING_CONTROLLED_BENCHMARK
    if any(
        not required_directory.is_dir()
        for required_directory in resolve_fediec_contracts_required_raw_directories()
    ):
        return DatasetAvailability.PRESENT_BUT_INCOMPLETE
    return DatasetAvailability.PRESENT_AND_VALID
