from __future__ import annotations

from dataclasses import dataclass

from fediec.types import BaselineName, Dimension


@dataclass(frozen=True)
class BaselineInputContract:
    name: BaselineName
    target_dimension: Dimension
    condition_dimension: Dimension | None
    no_action_source_gated: bool


ACTION_AGNOSTIC_DENSITY = BaselineInputContract(
    name=BaselineName("q(X_interaction)"),
    target_dimension=19,
    condition_dimension=None,
    no_action_source_gated=False,
)
INTENT_CONDITIONED_DENSITY = BaselineInputContract(
    name=BaselineName("q(X_interaction | I)"),
    target_dimension=19,
    condition_dimension=3,
    no_action_source_gated=True,
)
DIRECT_ACTION_CLASSIFIER = BaselineInputContract(
    name=BaselineName("P(I | X_interaction)"),
    target_dimension=19,
    condition_dimension=None,
    no_action_source_gated=True,
)
PER_ACTION_ONE_CLASS = BaselineInputContract(
    name=BaselineName("q_a(X_interaction)"),
    target_dimension=19,
    condition_dimension=None,
    no_action_source_gated=True,
)


def active_baseline_contracts() -> tuple[BaselineInputContract, ...]:
    return (
        ACTION_AGNOSTIC_DENSITY,
        INTENT_CONDITIONED_DENSITY,
        DIRECT_ACTION_CLASSIFIER,
        PER_ACTION_ONE_CLASS,
    )
