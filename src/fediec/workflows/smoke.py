from __future__ import annotations

import json
from pathlib import Path

from fediec.config import load_config
from fediec.datasets.moniotr_imc_2019.dataset import enumerate_raw_interactions
from fediec.datasets.normalization import (
    apply_locked_transforms,
    feature_tensor,
    fit_training_only_scaler,
    has_only_locked_log_transforms,
    transform_with_scaler,
)
from fediec.enums import (
    DatasetRole,
    DatasetSource,
    RepositoryPathSegment,
    SemanticAction,
    SplitPartition,
)
from fediec.models.baselines import (
    action_agnostic_scores,
    direct_action_scores,
    fit_baselines,
    mahalanobis_scores,
    per_action_one_class_scores,
)
from fediec.models.conditional_flow import build_conditional_interaction_flow, encode_intent
from fediec.paths import resolve_processed_dataset_directory
from fediec.training.federated import FederatedClientData, train_fedavg
from fediec.training.runner import train_conditional_flow
from fediec.types import (
    CleanSplitManifest,
    DeviceId,
    InteractionFeatureVector,
    ProtocolFreezeManifest,
    PublicSourceInteraction,
)


def _load_smoke_training_rows(
    interactions: tuple[PublicSourceInteraction, ...],
    vectors: tuple[InteractionFeatureVector, ...],
    manifest: CleanSplitManifest,
) -> tuple[
    tuple[InteractionFeatureVector, ...], tuple[SemanticAction, ...], tuple[DeviceId, ...]
]:
    assignments = {assignment.interaction_id: assignment for assignment in manifest.assignments}
    candidates = tuple(
        (interaction, vector)
        for interaction, vector in zip(interactions, vectors, strict=True)
        if assignments[interaction.interaction_id].partition is SplitPartition.TRAINING
    )
    devices = tuple(sorted({interaction.device_id for interaction, _ in candidates}))
    selected_devices = tuple(
        device
        for device in devices
        if all(
            sum(
                interaction.device_id == device and interaction.semantic_action is action
                for interaction, _ in candidates
            )
            >= load_config().smoke.samples_per_device_action
            for action in (SemanticAction.TURN_ON, SemanticAction.TURN_OFF)
        )
    )[:2]
    if len(selected_devices) != 2:
        raise RuntimeError("real-data smoke requires two eligible physical-device clients")
    selected = tuple(
        item
        for device in selected_devices
        for action in (SemanticAction.TURN_ON, SemanticAction.TURN_OFF)
        for item in tuple(
            candidate
            for candidate in candidates
            if candidate[0].device_id == device and candidate[0].semantic_action is action
        )[: load_config().smoke.samples_per_device_action]
    )
    return (
        tuple(vector for _, vector in selected),
        tuple(interaction.semantic_action for interaction, _ in selected),
        tuple(interaction.device_id for interaction, _ in selected),
    )


def run_smoke() -> None:
    freeze_path = (
        Path(resolve_processed_dataset_directory(DatasetSource.MONIOTR_IMC_2019))
        / RepositoryPathSegment.PROTOCOL_FREEZE_MANIFEST_FILE
    )
    frozen = ProtocolFreezeManifest.model_validate_json(freeze_path.read_text(encoding="utf-8"))
    if (
        frozen.role is not DatasetRole.PRIMARY_INTERACTION_CONTRACT
        or not frozen.representation_confound_audit_passed
    ):
        raise RuntimeError(
            "engineering smoke requires the approved passing primary protocol freeze"
        )
    if len(enumerate_raw_interactions()) != frozen.eligible_capture_count:
        raise RuntimeError("raw eligible-capture identity no longer matches the frozen protocol")
    interactions = enumerate_raw_interactions()
    vectors = tuple(
        InteractionFeatureVector(values=tuple(values))
        for values in json.loads(
            (
                Path(resolve_processed_dataset_directory(DatasetSource.MONIOTR_IMC_2019))
                / RepositoryPathSegment.INTERACTION_FEATURES_FILE
            ).read_text(encoding="utf-8")
        )
    )
    splits = CleanSplitManifest.model_validate_json(
        (
            Path(resolve_processed_dataset_directory(DatasetSource.MONIOTR_IMC_2019))
            / RepositoryPathSegment.CLEAN_SPLIT_MANIFEST_FILE
        ).read_text(encoding="utf-8")
    )
    smoke_vectors, actions, devices = _load_smoke_training_rows(interactions, vectors, splits)
    transformed = apply_locked_transforms(feature_tensor(smoke_vectors))
    scaler = fit_training_only_scaler(transformed)
    standardized = transform_with_scaler(transformed, scaler)
    local_model = build_conditional_interaction_flow()
    local_rows = tuple(index for index, device in enumerate(devices) if device == devices[0])
    local_features = standardized[list(local_rows)]
    local_actions = tuple(actions[index] for index in local_rows)
    smoke_settings = load_config().smoke
    train_conditional_flow(
        local_model, local_features, local_actions, smoke_settings.training_epochs
    )
    centralized_model = build_conditional_interaction_flow()
    train_conditional_flow(centralized_model, standardized, actions, smoke_settings.training_epochs)
    clients = tuple(
        FederatedClientData(
            features=standardized[
                [index for index, candidate in enumerate(devices) if candidate == device]
            ],
            actions=tuple(
                action
                for action, candidate in zip(actions, devices, strict=True)
                if candidate == device
            ),
        )
        for device in tuple(sorted(set(devices)))
    )
    federated_model = build_conditional_interaction_flow()
    train_fedavg(federated_model, clients, load_config().smoke.federated_rounds)
    baselines = fit_baselines(standardized, actions)
    if not has_only_locked_log_transforms():
        raise RuntimeError("configured log transforms include a locked rate feature")
    baseline_scores = (
        action_agnostic_scores(baselines, standardized),
        direct_action_scores(baselines, standardized, actions),
        per_action_one_class_scores(baselines, standardized, actions),
        mahalanobis_scores(baselines, standardized, actions),
    )
    if any(scores.shape != (len(actions),) for scores in baseline_scores):
        raise RuntimeError("baseline smoke scores do not align to real source rows")
    condition = encode_intent(SemanticAction.TURN_ON).unsqueeze(0)
    if centralized_model.log_probability(standardized[:1], condition).shape != (1,):
        raise RuntimeError("conditional-flow structural smoke failed")
