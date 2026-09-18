from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

import torch
from torch import Tensor
from torch.optim.adam import adam

from fediec.config import load_config
from fediec.enums import SemanticAction
from fediec.models.conditional_flow import ConditionalInteractionFlow, encode_intent
from fediec.types import Duration, EpochCount, ModelParameterCount, TrainingStepCount


@dataclass(frozen=True)
class TrainingSummary:
    model: ConditionalInteractionFlow
    parameter_count: ModelParameterCount
    step_count: TrainingStepCount
    elapsed_seconds: Duration


def intent_tensor(actions: tuple[SemanticAction, ...]) -> Tensor:
    return torch.stack(tuple(encode_intent(action) for action in actions))


def train_conditional_flow(
    model: ConditionalInteractionFlow,
    features: Tensor,
    actions: tuple[SemanticAction, ...],
    epochs: EpochCount,
) -> TrainingSummary:
    configuration = load_config().training
    if features.shape[0] != len(actions):
        raise ValueError("training features and independently recorded intents must align")
    if features.shape[0] == 0:
        raise ValueError("conditional-flow training requires clean source interactions")
    parameters = tuple(model.parameters())
    exp_averages = tuple(torch.zeros_like(parameter) for parameter in parameters)
    exp_average_squares = tuple(torch.zeros_like(parameter) for parameter in parameters)
    step_tensors = tuple(torch.zeros((), dtype=torch.float32) for _ in parameters)
    started = perf_counter()
    contexts = intent_tensor(actions)
    steps = 0
    for _ in range(epochs):
        model.zero_grad()
        loss = -model.log_probability(features, contexts).mean()
        torch.autograd.backward((loss,))
        torch.nn.utils.clip_grad_norm_(model.parameters(), configuration.gradient_norm_clip)
        gradients = tuple(parameter.grad for parameter in parameters)
        if any(gradient is None for gradient in gradients):
            raise RuntimeError("conditional-flow Adam requires gradients for every parameter")
        with torch.no_grad():
            adam(
                list(parameters),
                [gradient for gradient in gradients if gradient is not None],
                list(exp_averages),
                list(exp_average_squares),
                [],
                list(step_tensors),
                foreach=False,
                capturable=False,
                differentiable=False,
                fused=False,
                amsgrad=False,
                beta1=configuration.adam_beta1,
                beta2=configuration.adam_beta2,
                lr=configuration.learning_rate,
                weight_decay=configuration.weight_decay,
                eps=configuration.adam_epsilon,
                maximize=False,
            )
        steps += 1
    return TrainingSummary(
        model=model,
        parameter_count=sum(parameter.numel() for parameter in model.parameters()),
        step_count=steps,
        elapsed_seconds=perf_counter() - started,
    )
