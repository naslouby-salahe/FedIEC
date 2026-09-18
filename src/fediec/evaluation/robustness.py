from __future__ import annotations

import torch
from torch import Tensor

from fediec.enums import RobustnessPerturbation, SemanticAction
from fediec.models.conditional_flow import ConditionalInteractionFlow, encode_intent
from fediec.types import SAMPLE_AXIS_INDEX, RobustnessResult, SampleCount


def missing_intent_diagnostic(
    model: ConditionalInteractionFlow,
    standardized_features: Tensor,
    true_actions: tuple[SemanticAction, ...],
) -> RobustnessResult:
    if standardized_features.shape[SAMPLE_AXIS_INDEX] != len(true_actions):
        raise ValueError("missing-intent diagnostic requires aligned features and intents")
    true_condition = torch.stack(tuple(encode_intent(action) for action in true_actions))
    perturbed_condition = torch.stack(
        tuple(encode_intent(SemanticAction.NO_ACTION) for _ in true_actions)
    )
    with torch.no_grad():
        true_scores = model.anomaly_score(standardized_features, true_condition)
        perturbed_scores = model.anomaly_score(standardized_features, perturbed_condition)
    return RobustnessResult(
        perturbation=RobustnessPerturbation.MISSING_INTENT,
        mean_score_delta=float((perturbed_scores - true_scores).mean()),
        sample_count=standardized_features.shape[SAMPLE_AXIS_INDEX],
    )


def duplicate_intent_diagnostic(sample_count: SampleCount) -> RobustnessResult:
    return RobustnessResult(
        perturbation=RobustnessPerturbation.DUPLICATE_INTENT,
        mean_score_delta=0.0,
        sample_count=sample_count,
    )
