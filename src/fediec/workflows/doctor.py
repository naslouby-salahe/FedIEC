from __future__ import annotations

from collections.abc import Callable

from pydantic import ValidationError

from fediec.config import load_config
from fediec.datasets.cic_iot_2022 import dataset as cic_iot_2022_dataset
from fediec.datasets.moniotr_imc_2019 import dataset as moniotr_imc_2019_dataset
from fediec.datasets.pingpong import dataset as pingpong_dataset
from fediec.datasets.tu_wien_philips_hue import dataset as tu_wien_philips_hue_dataset
from fediec.enums import CheckKind, CheckStatus, DatasetAvailability, DatasetSource
from fediec.types import CheckDetail, DatasetAssessment, DomainRecord

_DATASET_AVAILABILITY_CHECK_STATUS: dict[DatasetAvailability, CheckStatus] = {
    DatasetAvailability.PRESENT_AND_VALID: CheckStatus.PASS,
    DatasetAvailability.PRESENT_BUT_INCOMPLETE: CheckStatus.WARN,
    DatasetAvailability.PRESENT_BUT_SCHEMA_DRIFTED: CheckStatus.WARN,
    DatasetAvailability.PRESENT_BUT_CORRUPT: CheckStatus.FAIL,
    DatasetAvailability.MISSING_EXTERNAL: CheckStatus.WARN,
    DatasetAvailability.ACCESS_RESTRICTED: CheckStatus.WARN,
}

_DATASET_AVAILABILITY_CHECK: dict[DatasetSource, Callable[[], DatasetAvailability]] = {
    DatasetSource.PINGPONG: pingpong_dataset.describe_raw_availability,
    DatasetSource.TU_WIEN_PHILIPS_HUE: tu_wien_philips_hue_dataset.describe_raw_availability,
    DatasetSource.CIC_IOT_2022: cic_iot_2022_dataset.describe_raw_availability,
    DatasetSource.MONIOTR_IMC_2019: moniotr_imc_2019_dataset.describe_raw_availability,
}

_CHECK_KIND_FOR_DATASET: dict[DatasetSource, CheckKind] = {
    DatasetSource.PINGPONG: CheckKind.DATASET_PINGPONG,
    DatasetSource.TU_WIEN_PHILIPS_HUE: CheckKind.DATASET_TU_WIEN_PHILIPS_HUE,
    DatasetSource.CIC_IOT_2022: CheckKind.DATASET_CIC_IOT_2022,
    DatasetSource.MONIOTR_IMC_2019: CheckKind.DATASET_MONIOTR_IMC_2019,
}


class DoctorCheckResult(DomainRecord):
    label: CheckKind
    status: CheckStatus
    detail: CheckDetail | None = None
    availability: DatasetAvailability | None = None
    assessment: DatasetAssessment | None = None


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


def _resolve_dataset_assessment(dataset_source: DatasetSource) -> DatasetAssessment:
    public_sources = load_config().public_sources
    match dataset_source:
        case DatasetSource.PINGPONG:
            configured = public_sources.pingpong
        case DatasetSource.CIC_IOT_2022:
            configured = public_sources.cic_iot_2022
        case DatasetSource.TU_WIEN_PHILIPS_HUE:
            configured = public_sources.tu_wien_philips_hue
        case DatasetSource.MONIOTR_IMC_2019:
            configured = public_sources.moniotr_imc_2019
    return DatasetAssessment(
        dataset_source=dataset_source,
        role=configured.role,
        eligibility=configured.eligibility,
        intent_provenance_grade=configured.intent_provenance,
    )


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
    assessment = _resolve_dataset_assessment(dataset)
    status = _DATASET_AVAILABILITY_CHECK_STATUS[availability]
    return DoctorCheckResult(
        label=_CHECK_KIND_FOR_DATASET[dataset],
        status=status,
        availability=availability,
        assessment=assessment,
    )


def run_doctor() -> DoctorReport:
    checks = (
        _check_configuration(),
        *(_check_dataset(dataset) for dataset in DatasetSource),
    )
    return DoctorReport(checks=checks)
