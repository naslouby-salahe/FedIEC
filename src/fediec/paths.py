from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fediec.enums import DatasetRawDirectoryName, DatasetSource, ExperimentName, RepositoryPathKey
from fediec.types import (
    CaptureId,
    FileName,
    RepositoryPath,
    Seed,
    SessionId,
)


@lru_cache(maxsize=1)
def _repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


_DATASET_SOURCE_DIRECTORY_NAME: dict[DatasetSource, DatasetRawDirectoryName] = {
    DatasetSource.FEDIEC_CONTRACTS: DatasetRawDirectoryName.FEDIEC_CONTRACTS,
    DatasetSource.PINGPONG: DatasetRawDirectoryName.PINGPONG,
    DatasetSource.TU_WIEN_PHILIPS_HUE: DatasetRawDirectoryName.TU_WIEN_PHILIPS_HUE,
    DatasetSource.CIC_IOT_2022: DatasetRawDirectoryName.CIC_IOT_2022,
}


def resolve_path(key: RepositoryPathKey) -> RepositoryPath:
    root = _repository_root()
    match key:
        case RepositoryPathKey.REPO_ROOT:
            resolved = root
        case RepositoryPathKey.DOCS_ROOT:
            resolved = root / "docs"
        case RepositoryPathKey.DOCS_IMPLEMENTATION_ROOT:
            resolved = root / "docs" / "implementation"
        case RepositoryPathKey.DATA_ROOT:
            resolved = root / "data"
        case RepositoryPathKey.DATA_RAW_ROOT:
            resolved = root / "data" / "raw"
        case RepositoryPathKey.DATA_RAW_FEDIEC_CONTRACTS:
            resolved = resolve_dataset_raw_root(DatasetSource.FEDIEC_CONTRACTS)
        case RepositoryPathKey.DATA_RAW_PINGPONG:
            resolved = resolve_dataset_raw_root(DatasetSource.PINGPONG)
        case RepositoryPathKey.DATA_RAW_TU_WIEN_PHILIPS_HUE:
            resolved = resolve_dataset_raw_root(DatasetSource.TU_WIEN_PHILIPS_HUE)
        case RepositoryPathKey.DATA_RAW_CIC_IOT_2022:
            resolved = resolve_dataset_raw_root(DatasetSource.CIC_IOT_2022)
        case RepositoryPathKey.OUTPUTS_ROOT:
            resolved = root / "outputs"
        case RepositoryPathKey.OUTPUTS_PROCESSED_ROOT:
            resolved = root / "outputs" / "processed"
        case RepositoryPathKey.OUTPUTS_BENCHMARK_ROOT:
            resolved = root / "outputs" / "benchmark"
        case RepositoryPathKey.OUTPUTS_RUNS_ROOT:
            resolved = root / "outputs" / "runs"
        case RepositoryPathKey.OUTPUTS_ANALYSES_ROOT:
            resolved = root / "outputs" / "analyses"
        case RepositoryPathKey.OUTPUTS_REPORTS_ROOT:
            resolved = root / "outputs" / "reports"
        case RepositoryPathKey.RESULTS_ROOT:
            resolved = root / "results"
        case RepositoryPathKey.RESULTS_BENCHMARK_ROOT:
            resolved = root / "results" / "benchmark"
        case RepositoryPathKey.RESULTS_EXPERIMENTS_ROOT:
            resolved = root / "results" / "experiments"
        case RepositoryPathKey.RESULTS_STATISTICS_ROOT:
            resolved = root / "results" / "statistics"
        case RepositoryPathKey.RESULTS_TABLES_ROOT:
            resolved = root / "results" / "tables"
        case RepositoryPathKey.RESULTS_FIGURES_ROOT:
            resolved = root / "results" / "figures"
        case RepositoryPathKey.CONFIG_FILE:
            resolved = root / "config.yaml"
        case RepositoryPathKey.DATA_RAW_FEDIEC_CONTRACTS_CAPTURES:
            resolved = resolve_dataset_raw_root(DatasetSource.FEDIEC_CONTRACTS) / "captures"
        case RepositoryPathKey.DATA_RAW_FEDIEC_CONTRACTS_INTENT_LOGS:
            resolved = resolve_dataset_raw_root(DatasetSource.FEDIEC_CONTRACTS) / "intent-logs"
        case RepositoryPathKey.DATA_RAW_FEDIEC_CONTRACTS_SESSION_MANIFESTS:
            resolved = (
                resolve_dataset_raw_root(DatasetSource.FEDIEC_CONTRACTS) / "session-manifests"
            )
        case RepositoryPathKey.DATA_RAW_FEDIEC_CONTRACTS_DEVICE_METADATA:
            resolved = resolve_dataset_raw_root(DatasetSource.FEDIEC_CONTRACTS) / "device-metadata"
    return RepositoryPath(resolved)


def resolve_dataset_raw_root(dataset: DatasetSource) -> RepositoryPath:
    directory_name = _DATASET_SOURCE_DIRECTORY_NAME[dataset]
    return RepositoryPath(_repository_root() / "data" / "raw" / directory_name)


def resolve_cic_iot_2022_interactions_root() -> RepositoryPath:
    return RepositoryPath(resolve_dataset_raw_root(DatasetSource.CIC_IOT_2022) / "3-Interactions")


def resolve_pingpong_evaluation_root() -> RepositoryPath:
    return RepositoryPath(resolve_dataset_raw_root(DatasetSource.PINGPONG) / "evaluation-datasets")


_RUN_MANIFEST_FILENAME = FileName("manifest.json")

_FEDIEC_CONTRACTS_REQUIRED_RAW_PATH_KEYS: tuple[RepositoryPathKey, ...] = (
    RepositoryPathKey.DATA_RAW_FEDIEC_CONTRACTS_CAPTURES,
    RepositoryPathKey.DATA_RAW_FEDIEC_CONTRACTS_INTENT_LOGS,
    RepositoryPathKey.DATA_RAW_FEDIEC_CONTRACTS_SESSION_MANIFESTS,
    RepositoryPathKey.DATA_RAW_FEDIEC_CONTRACTS_DEVICE_METADATA,
)


def resolve_output_run_directory(experiment: ExperimentName, seed: Seed) -> RepositoryPath:
    runs_root = resolve_path(RepositoryPathKey.OUTPUTS_RUNS_ROOT)
    return RepositoryPath(Path(runs_root) / experiment.value / f"{seed}")


def resolve_run_manifest_path(experiment: ExperimentName, seed: Seed) -> RepositoryPath:
    run_directory = resolve_output_run_directory(experiment, seed)
    return RepositoryPath(Path(run_directory) / _RUN_MANIFEST_FILENAME)


def resolve_processed_dataset_directory(dataset: DatasetSource) -> RepositoryPath:
    processed_root = resolve_path(RepositoryPathKey.OUTPUTS_PROCESSED_ROOT)
    slug = _DATASET_SOURCE_DIRECTORY_NAME[dataset].lower().replace(" ", "-")
    return RepositoryPath(Path(processed_root) / slug)


def resolve_capture_reference(
    dataset: DatasetSource, session_id: SessionId, capture_id: CaptureId
) -> RepositoryPath:
    dataset_root = resolve_dataset_raw_root(dataset)
    return RepositoryPath(Path(dataset_root) / session_id / f"{capture_id}.pcap")


def resolve_fediec_contracts_required_raw_directories() -> tuple[RepositoryPath, ...]:
    return tuple(resolve_path(key) for key in _FEDIEC_CONTRACTS_REQUIRED_RAW_PATH_KEYS)
