from __future__ import annotations

from pathlib import Path

import torch

from fediec.datasets.moniotr_imc_2019.dataset import enumerate_raw_interactions
from fediec.enums import DatasetRole, DatasetSource, RepositoryPathSegment, SemanticAction
from fediec.models.conditional_flow import build_conditional_interaction_flow, encode_intent
from fediec.paths import resolve_processed_dataset_directory
from fediec.types import ProtocolFreezeManifest


def run_smoke() -> None:
    freeze_path = (
        Path(resolve_processed_dataset_directory(DatasetSource.MONIOTR_IMC_2019))
        / RepositoryPathSegment.PROTOCOL_FREEZE_MANIFEST_FILE
    )
    frozen = ProtocolFreezeManifest.model_validate_json(
        freeze_path.read_text(encoding="utf-8")
    )
    if (
        frozen.role is not DatasetRole.PRIMARY_INTERACTION_CONTRACT
        or not frozen.representation_confound_audit_passed
    ):
        raise RuntimeError(
            "engineering smoke requires the approved passing primary protocol freeze"
        )
    if len(enumerate_raw_interactions()) != frozen.eligible_capture_count:
        raise RuntimeError("raw eligible-capture identity no longer matches the frozen protocol")
    model = build_conditional_interaction_flow()
    target = torch.zeros((1, model.target_dimension))
    condition = encode_intent(SemanticAction.TURN_ON).unsqueeze(0)
    if model.log_probability(target, condition).shape != (1,):
        raise RuntimeError("conditional-flow structural smoke failed")
