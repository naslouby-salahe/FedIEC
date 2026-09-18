from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor

from fediec.config import load_config
from fediec.enums import SemanticAction
from fediec.models.conditional_flow import ConditionalInteractionFlow
from fediec.training.runner import TrainingSummary, train_conditional_flow
from fediec.types import SAMPLE_AXIS_INDEX, RoundCount, SampleCount, SerializedByteCount


@dataclass(frozen=True)
class FederatedClientData:
    features: Tensor
    actions: tuple[SemanticAction, ...]


@dataclass(frozen=True)
class FederatedTrainingSummary:
    training: TrainingSummary
    uploaded_bytes: SerializedByteCount
    downloaded_bytes: SerializedByteCount


@dataclass(frozen=True)
class _FederatedClientResult:
    parameters: tuple[Tensor, ...]
    sample_count: SampleCount
    training: TrainingSummary


def _train_client(
    model: ConditionalInteractionFlow,
    client: FederatedClientData,
    global_parameters: tuple[Tensor, ...],
) -> _FederatedClientResult:
    local = ConditionalInteractionFlow(
        model.target_dimension,
        len(model.blocks),
        load_config().model.hidden_units_per_layer,
    )
    with torch.no_grad():
        for local_parameter, global_parameter in zip(
            local.parameters(), global_parameters, strict=True
        ):
            local_parameter.copy_(global_parameter)
    training = train_conditional_flow(
        local, client.features, client.actions, load_config().federated.local_epochs
    )
    return _FederatedClientResult(
        parameters=tuple(parameter.detach().clone() for parameter in local.parameters()),
        sample_count=client.features.shape[SAMPLE_AXIS_INDEX],
        training=training,
    )


def train_fedavg(
    model: ConditionalInteractionFlow,
    clients: tuple[FederatedClientData, ...],
    rounds: RoundCount,
) -> FederatedTrainingSummary:
    if not clients:
        raise ValueError("FedAvg requires at least one eligible physical-device client")
    uploaded = 0
    downloaded = 0
    latest: TrainingSummary | None = None
    for _ in range(rounds):
        global_parameters = tuple(parameter.detach().clone() for parameter in model.parameters())
        local_results = tuple(_train_client(model, client, global_parameters) for client in clients)
        total_rows = sum(result.sample_count for result in local_results)
        for result in local_results:
            latest = result.training
            uploaded += sum(
                parameter.numel() * parameter.element_size() for parameter in result.parameters
            )
            downloaded += sum(
                parameter.numel() * parameter.element_size() for parameter in global_parameters
            )
        with torch.no_grad():
            for parameter_index, global_parameter in enumerate(model.parameters()):
                global_parameter.copy_(
                    sum(
                        (
                            result.parameters[parameter_index] * (result.sample_count / total_rows)
                            for result in local_results
                        ),
                        torch.zeros_like(global_parameter),
                    )
                )
    if latest is None:
        raise RuntimeError("FedAvg did not execute a local training step")
    return FederatedTrainingSummary(
        training=TrainingSummary(
            model=model,
            parameter_count=latest.parameter_count,
            step_count=latest.step_count * len(clients) * rounds,
            elapsed_seconds=latest.elapsed_seconds,
        ),
        uploaded_bytes=uploaded,
        downloaded_bytes=downloaded,
    )
