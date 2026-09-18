from __future__ import annotations

from itertools import pairwise

from fediec.enums import InfeasibilityReason, TransitionClass, ViolationFamily
from fediec.types import MonotonicTimestamp

_SUBSTITUTION_COMPATIBLE_TRANSITIONS: frozenset[TransitionClass] = frozenset(
    {TransitionClass.OFF_TO_ON, TransitionClass.ON_TO_OFF}
)


def transition_compatible(
    transition: TransitionClass | None, family: ViolationFamily
) -> tuple[bool, InfeasibilityReason | None]:
    if family is not ViolationFamily.SUBSTITUTION:
        return True, None
    if transition is None or transition not in _SUBSTITUTION_COMPATIBLE_TRANSITIONS:
        return False, InfeasibilityReason.COUNTERFACTUAL_INFEASIBLE_TRANSITION
    return True, None


def timestamps_strictly_ordered(
    timestamps: tuple[MonotonicTimestamp, ...],
) -> tuple[bool, InfeasibilityReason | None]:
    for earlier, later in pairwise(timestamps):
        if later <= earlier:
            return False, InfeasibilityReason.COUNTERFACTUAL_INFEASIBLE_BOUNDARY
    return True, None


def physical_timeline_feasible(
    donor_span: tuple[MonotonicTimestamp, MonotonicTimestamp],
    recipient_span: tuple[MonotonicTimestamp, MonotonicTimestamp],
) -> tuple[bool, InfeasibilityReason | None]:
    donor_start, donor_end = donor_span
    recipient_start, recipient_end = recipient_span
    if donor_end < donor_start or recipient_end < recipient_start:
        return False, InfeasibilityReason.COUNTERFACTUAL_INFEASIBLE_PHYSICAL_TIMELINE
    return True, None
