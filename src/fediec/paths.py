from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fediec.enums import (
    DatasetRawDirectoryName,
    DatasetRawSubpath,
    DatasetSource,
    ExperimentName,
    RepositoryPathKey,
    RepositoryPathSegment,
)
from fediec.types import RepositoryPath, Seed


@lru_cache(maxsize=1)
def _repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


_DATASET_SOURCE_DIRECTORY_NAME: dict[DatasetSource, DatasetRawDirectoryName] = {
    DatasetSource.PINGPONG: DatasetRawDirectoryName.PINGPONG,
    DatasetSource.TU_WIEN_PHILIPS_HUE: DatasetRawDirectoryName.TU_WIEN_PHILIPS_HUE,
    DatasetSource.CIC_IOT_2022: DatasetRawDirectoryName.CIC_IOT_2022,
}


def resolve_path(key: RepositoryPathKey) -> RepositoryPath:
    root = _repository_root()
    seg = RepositoryPathSegment
    match key:
        case RepositoryPathKey.REPO_ROOT:
            resolved = root
        case RepositoryPathKey.DOCS_ROOT:
            resolved = root / seg.DOCS
        case RepositoryPathKey.DOCS_IMPLEMENTATION_ROOT:
            resolved = Path(resolve_path(RepositoryPathKey.DOCS_ROOT)) / seg.IMPLEMENTATION
        case RepositoryPathKey.DATA_ROOT:
            resolved = root / seg.DATA
        case RepositoryPathKey.DATA_RAW_ROOT:
            resolved = Path(resolve_path(RepositoryPathKey.DATA_ROOT)) / seg.RAW
        case RepositoryPathKey.DATA_RAW_PINGPONG:
            resolved = resolve_dataset_raw_root(DatasetSource.PINGPONG)
        case RepositoryPathKey.DATA_RAW_TU_WIEN_PHILIPS_HUE:
            resolved = resolve_dataset_raw_root(DatasetSource.TU_WIEN_PHILIPS_HUE)
        case RepositoryPathKey.DATA_RAW_CIC_IOT_2022:
            resolved = resolve_dataset_raw_root(DatasetSource.CIC_IOT_2022)
        case RepositoryPathKey.OUTPUTS_ROOT:
            resolved = root / seg.OUTPUTS
        case RepositoryPathKey.OUTPUTS_PROCESSED_ROOT:
            resolved = Path(resolve_path(RepositoryPathKey.OUTPUTS_ROOT)) / seg.PROCESSED
        case RepositoryPathKey.OUTPUTS_BENCHMARK_ROOT:
            resolved = Path(resolve_path(RepositoryPathKey.OUTPUTS_ROOT)) / seg.BENCHMARK
        case RepositoryPathKey.OUTPUTS_RUNS_ROOT:
            resolved = Path(resolve_path(RepositoryPathKey.OUTPUTS_ROOT)) / seg.RUNS
        case RepositoryPathKey.OUTPUTS_ANALYSES_ROOT:
            resolved = Path(resolve_path(RepositoryPathKey.OUTPUTS_ROOT)) / seg.ANALYSES
        case RepositoryPathKey.OUTPUTS_REPORTS_ROOT:
            resolved = Path(resolve_path(RepositoryPathKey.OUTPUTS_ROOT)) / seg.REPORTS
        case RepositoryPathKey.RESULTS_ROOT:
            resolved = root / seg.RESULTS
        case RepositoryPathKey.RESULTS_BENCHMARK_ROOT:
            resolved = Path(resolve_path(RepositoryPathKey.RESULTS_ROOT)) / seg.BENCHMARK
        case RepositoryPathKey.RESULTS_EXPERIMENTS_ROOT:
            resolved = Path(resolve_path(RepositoryPathKey.RESULTS_ROOT)) / seg.EXPERIMENTS
        case RepositoryPathKey.RESULTS_STATISTICS_ROOT:
            resolved = Path(resolve_path(RepositoryPathKey.RESULTS_ROOT)) / seg.STATISTICS
        case RepositoryPathKey.RESULTS_TABLES_ROOT:
            resolved = Path(resolve_path(RepositoryPathKey.RESULTS_ROOT)) / seg.TABLES
        case RepositoryPathKey.RESULTS_FIGURES_ROOT:
            resolved = Path(resolve_path(RepositoryPathKey.RESULTS_ROOT)) / seg.FIGURES
        case RepositoryPathKey.CONFIG_FILE:
            resolved = root / seg.CONFIG_FILE
    return RepositoryPath(resolved)


def resolve_dataset_raw_root(dataset: DatasetSource) -> RepositoryPath:
    directory_name = _DATASET_SOURCE_DIRECTORY_NAME[dataset]
    data_raw_root = resolve_path(RepositoryPathKey.DATA_RAW_ROOT)
    return RepositoryPath(Path(data_raw_root) / directory_name)


def resolve_cic_iot_2022_interactions_root() -> RepositoryPath:
    cic_root = resolve_dataset_raw_root(DatasetSource.CIC_IOT_2022)
    return RepositoryPath(Path(cic_root) / DatasetRawSubpath.CIC_IOT_2022_INTERACTIONS)


def resolve_pingpong_evaluation_root() -> RepositoryPath:
    pingpong_root = resolve_dataset_raw_root(DatasetSource.PINGPONG)
    return RepositoryPath(Path(pingpong_root) / DatasetRawSubpath.PINGPONG_EVALUATION_DATASETS)


def resolve_output_run_directory(experiment: ExperimentName, seed: Seed) -> RepositoryPath:
    runs_root = resolve_path(RepositoryPathKey.OUTPUTS_RUNS_ROOT)
    return RepositoryPath(Path(runs_root) / experiment.value / f"{seed}")


def resolve_run_manifest_path(experiment: ExperimentName, seed: Seed) -> RepositoryPath:
    run_directory = resolve_output_run_directory(experiment, seed)
    return RepositoryPath(Path(run_directory) / RepositoryPathSegment.RUN_MANIFEST_FILE)


def resolve_processed_dataset_directory(dataset: DatasetSource) -> RepositoryPath:
    processed_root = resolve_path(RepositoryPathKey.OUTPUTS_PROCESSED_ROOT)
    slug = _DATASET_SOURCE_DIRECTORY_NAME[dataset].lower().replace(" ", "-")
    return RepositoryPath(Path(processed_root) / slug)
