from __future__ import annotations

import json
from pathlib import Path

from fediec.config import load_config
from fediec.datasets.cic_iot_2022.dataset import enumerate_raw_interactions as cic_interactions
from fediec.datasets.freeze import build_protocol_freeze
from fediec.datasets.moniotr_imc_2019.dataset import (
    enumerate_raw_interactions as moniotr_interactions,
)
from fediec.datasets.pingpong.dataset import enumerate_raw_interactions as pingpong_interactions
from fediec.datasets.representation import (
    audit_representation,
    extract_interaction_features,
    require_representation_audit_pass,
)
from fediec.datasets.splits import build_clean_split
from fediec.datasets.tu_wien_philips_hue.dataset import (
    enumerate_raw_interactions as hue_interactions,
)
from fediec.enums import DatasetSource, RepositoryPathSegment
from fediec.paths import resolve_processed_dataset_directory
from fediec.types import PublicSourceInteraction, RepositoryPath


def _interactions(dataset_source: DatasetSource) -> tuple[PublicSourceInteraction, ...]:
    match dataset_source:
        case DatasetSource.PINGPONG:
            return pingpong_interactions()
        case DatasetSource.CIC_IOT_2022:
            return cic_interactions()
        case DatasetSource.TU_WIEN_PHILIPS_HUE:
            return hue_interactions()
        case DatasetSource.MONIOTR_IMC_2019:
            return moniotr_interactions()


def run_preprocess() -> None:
    for dataset_source in DatasetSource:
        split = load_config().split
        manifest = build_clean_split(
            dataset_source,
            _interactions(dataset_source),
            (split.training_proportion, split.calibration_proportion, split.test_proportion),
        )
        directory = resolve_processed_dataset_directory(dataset_source)
        target = RepositoryPath(Path(directory) / RepositoryPathSegment.CLEAN_SPLIT_MANIFEST_FILE)
        Path(target).parent.mkdir(parents=True, exist_ok=True)
        Path(target).write_text(
            manifest.model_dump_json(indent=2),
            encoding="utf-8",
        )
        if dataset_source is not DatasetSource.MONIOTR_IMC_2019:
            continue
        interactions = _interactions(dataset_source)
        vectors = tuple(extract_interaction_features(item) for item in interactions)
        audit = audit_representation(interactions, vectors)
        audit_target = Path(directory) / RepositoryPathSegment.REPRESENTATION_CONFOUND_AUDIT_FILE
        audit_target.write_text(audit.model_dump_json(indent=2), encoding="utf-8")
        require_representation_audit_pass(audit)
        feature_target = Path(directory) / RepositoryPathSegment.INTERACTION_FEATURES_FILE
        feature_target.write_text(json.dumps(vectors), encoding="utf-8")
        freeze = build_protocol_freeze(manifest, audit)
        freeze_target = Path(directory) / RepositoryPathSegment.PROTOCOL_FREEZE_MANIFEST_FILE
        freeze_target.write_text(freeze.model_dump_json(indent=2), encoding="utf-8")
