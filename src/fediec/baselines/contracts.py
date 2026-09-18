from __future__ import annotations

from dataclasses import dataclass

from fediec.config import load_config
from fediec.enums import ScoringMethod
from fediec.types import Dimension


@dataclass(frozen=True)
class BaselineInputContract:
    name: ScoringMethod
    target_dimension: Dimension
    condition_dimension: Dimension | None
    no_action_source_gated: bool


def active_baseline_contracts() -> tuple[BaselineInputContract, ...]:
    model = load_config().model
    return (
        BaselineInputContract(
            name=ScoringMethod.ACTION_AGNOSTIC_DENSITY,
            target_dimension=model.interaction_dimension,
            condition_dimension=None,
            no_action_source_gated=False,
        ),
        BaselineInputContract(
            name=ScoringMethod.INTENT_CONDITIONED_FLOW,
            target_dimension=model.interaction_dimension,
            condition_dimension=model.context_dimension,
            no_action_source_gated=True,
        ),
        BaselineInputContract(
            name=ScoringMethod.DIRECT_ACTION_CLASSIFIER,
            target_dimension=model.interaction_dimension,
            condition_dimension=None,
            no_action_source_gated=True,
        ),
        BaselineInputContract(
            name=ScoringMethod.PER_ACTION_ONE_CLASS,
            target_dimension=model.interaction_dimension,
            condition_dimension=None,
            no_action_source_gated=True,
        ),
    )
