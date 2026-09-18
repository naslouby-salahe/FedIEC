from __future__ import annotations

from fediec.enums import CounterfactualFeasibility, ViolationFamily
from fediec.types import CounterfactualFeasibilityRecord, PublicSourceInteraction


class NotSourceFeasibleError(RuntimeError):
    pass


def generate_counterfactual(
    family: ViolationFamily,
    feasibility_record: CounterfactualFeasibilityRecord,
    donor_interaction: PublicSourceInteraction,
) -> PublicSourceInteraction:
    if feasibility_record.violation_family is not family:
        raise ValueError("feasibility record does not describe the requested violation family")
    if feasibility_record.feasibility is not CounterfactualFeasibility.SOURCE_FEASIBLE:
        raise NotSourceFeasibleError(
            f"{family}: {feasibility_record.feasibility}; {feasibility_record.reason}"
        )
    raise NotImplementedError(
        f"{family} was declared source-feasible for donor "
        f"{donor_interaction.source_capture_id} but no raw-timeline generator is wired"
    )
