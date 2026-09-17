from __future__ import annotations

from collections.abc import Callable

from pydantic import ValidationError

from fediec.config import load_config
from fediec.datasets.cic_iot_2022 import dataset as cic_iot_2022_dataset
from fediec.datasets.fediec_contracts import dataset as fediec_contracts_dataset
from fediec.datasets.pingpong import dataset as pingpong_dataset
from fediec.datasets.tu_wien_philips_hue import dataset as tu_wien_philips_hue_dataset
from fediec.enums import CheckKind, CheckStatus, DatasetAvailability, DatasetSource
from fediec.types import CheckDetail, DomainRecord

_DATASET_AVAILABILITY_CHECK_STATUS: dict[DatasetAvailability, CheckStatus] = {
    DatasetAvailability.PRESENT_AND_VALID: CheckStatus.PASS,
    DatasetAvailability.PRESENT_BUT_INCOMPLETE: CheckStatus.WARN,
    DatasetAvailability.PRESENT_BUT_SCHEMA_DRIFTED: CheckStatus.WARN,
    DatasetAvailability.PRESENT_BUT_CORRUPT: CheckStatus.FAIL,
    DatasetAvailability.MISSING_EXTERNAL: CheckStatus.WARN,
    DatasetAvailability.MISSING_CONTROLLED_BENCHMARK: CheckStatus.WARN,
}

_DATASET_AVAILABILITY_CHECK: dict[DatasetSource, Callable[[], DatasetAvailability]] = {
    DatasetSource.FEDIEC_CONTRACTS: fediec_contracts_dataset.describe_raw_availability,
    DatasetSource.PINGPONG: pingpong_dataset.describe_raw_availability,
    DatasetSource.TU_WIEN_PHILIPS_HUE: tu_wien_philips_hue_dataset.describe_raw_availability,
    DatasetSource.CIC_IOT_2022: cic_iot_2022_dataset.describe_raw_availability,
}

_CHECK_KIND_FOR_DATASET: dict[DatasetSource, CheckKind] = {
    DatasetSource.FEDIEC_CONTRACTS: CheckKind.DATASET_FEDIEC_CONTRACTS,
    DatasetSource.PINGPONG: CheckKind.DATASET_PINGPONG,
    DatasetSource.TU_WIEN_PHILIPS_HUE: CheckKind.DATASET_TU_WIEN_PHILIPS_HUE,
    DatasetSource.CIC_IOT_2022: CheckKind.DATASET_CIC_IOT_2022,
}


class DoctorCheckResult(DomainRecord):
    label: CheckKind
    status: CheckStatus
    detail: CheckDetail


class DoctorReport(DomainRecord):
    checks: tuple[DoctorCheckResult, ...]

    @property
    def overall_status(self) -> CheckStatus:
        statuses = {check.status for check in self.checks}
        if CheckStatus.FAIL in statuses:
            return CheckStatus.FAIL
        if CheckStatus.WARN in statuses:
            return CheckStatus.WARN
        return CheckStatus.PASS


def _check_configuration() -> DoctorCheckResult:
    try:
        config = load_config()
    except ValidationError as error:
        return DoctorCheckResult(
            label=CheckKind.CONFIGURATION,
            status=CheckStatus.FAIL,
            detail=CheckDetail(f"config.yaml failed validation: {error}"),
        )
    except OSError as error:
        return DoctorCheckResult(
            label=CheckKind.CONFIGURATION,
            status=CheckStatus.FAIL,
            detail=CheckDetail(f"config.yaml could not be read: {error}"),
        )
    return DoctorCheckResult(
        label=CheckKind.CONFIGURATION,
        status=CheckStatus.PASS,
        detail=CheckDetail(
            f"config.yaml valid: {len(config.training.seeds)} training seeds configured"
        ),
    )


def _check_dataset(dataset: DatasetSource) -> DoctorCheckResult:
    describe = _DATASET_AVAILABILITY_CHECK[dataset]
    availability = describe()
    status = _DATASET_AVAILABILITY_CHECK_STATUS[availability]
    return DoctorCheckResult(
        label=_CHECK_KIND_FOR_DATASET[dataset],
        status=status,
        detail=CheckDetail(availability.value),
    )


def run_doctor() -> DoctorReport:
    checks = (
        _check_configuration(),
        *(_check_dataset(dataset) for dataset in DatasetSource),
    )
    return DoctorReport(checks=checks)
