from __future__ import annotations

from pathlib import Path

from fediec.enums import RepositoryPathKey
from fediec.paths import resolve_path
from fediec.types import ReportSummary


def run_report() -> ReportSummary:
    runs_root = Path(resolve_path(RepositoryPathKey.OUTPUTS_RUNS_ROOT))
    has_confirmatory_run_artifacts = runs_root.is_dir() and any(
        runs_root.glob("*/*/predictions.parquet")
    )
    if not has_confirmatory_run_artifacts:
        return ReportSummary(
            has_confirmatory_run_artifacts=False,
            comparisons=(),
            generated_table_paths=(),
            generated_figure_paths=(),
        )
    raise NotImplementedError(
        "confirmatory run artifacts were found under outputs/runs/, but the report "
        "workflow's predictions.parquet read path is not yet wired; implement it "
        "against the run.py prediction-artifact schema once confirmatory execution "
        "is unblocked"
    )
