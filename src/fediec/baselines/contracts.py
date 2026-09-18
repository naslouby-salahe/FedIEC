from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BaselineInputContract:
    name: str
    target_dimension: int
    condition_dimension: int | None
    no_action_source_gated: bool


ACTION_AGNOSTIC_DENSITY = BaselineInputContract(
    name="q(X_interaction)",
    target_dimension=19,
    condition_dimension=None,
    no_action_source_gated=False,
)
INTENT_CONDITIONED_DENSITY = BaselineInputContract(
    name="q(X_interaction | I)",
    target_dimension=19,
    condition_dimension=3,
    no_action_source_gated=True,
)
DIRECT_ACTION_CLASSIFIER = BaselineInputContract(
    name="P(I | X_interaction)",
    target_dimension=19,
    condition_dimension=None,
    no_action_source_gated=True,
)
PER_ACTION_ONE_CLASS = BaselineInputContract(
    name="q_a(X_interaction)",
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
