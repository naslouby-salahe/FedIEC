from __future__ import annotations

from pathlib import Path

from fediec.artifacts import write_json_manifest
from fediec.enums import CounterfactualFeasibility, DatasetSource, RepositoryPathSegment
from fediec.paths import (
    resolve_counterfactual_feasibility_manifest_path,
    resolve_processed_dataset_directory,
)
from fediec.types import ProtocolFreezeManifest


def run_prepare() -> None:
    freeze_path = (
        Path(resolve_processed_dataset_directory(DatasetSource.MONIOTR_IMC_2019))
        / RepositoryPathSegment.PROTOCOL_FREEZE_MANIFEST_FILE
    )
    freeze = ProtocolFreezeManifest.model_validate_json(freeze_path.read_text(encoding="utf-8"))
    if any(
        record.feasibility is CounterfactualFeasibility.SOURCE_FEASIBLE
        for record in freeze.counterfactual_feasibility
    ):
        raise RuntimeError(
            "a source-feasible counterfactual requires its frozen raw-timeline generator"
        )
    write_json_manifest(resolve_counterfactual_feasibility_manifest_path(), freeze)
