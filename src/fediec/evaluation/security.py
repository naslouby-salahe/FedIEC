from __future__ import annotations

from fediec.enums import CounterfactualFeasibility
from fediec.types import ProtocolFreezeManifest, SecurityEvaluationSummary, SecurityFamilyEvaluation


def evaluate_security_suite(freeze: ProtocolFreezeManifest) -> SecurityEvaluationSummary:
    families = tuple(
        SecurityFamilyEvaluation(
            violation_family=record.violation_family,
            feasibility=record.feasibility,
            evaluated=record.feasibility is CounterfactualFeasibility.SOURCE_FEASIBLE,
            reason=record.reason,
        )
        for record in freeze.counterfactual_feasibility
    )
    return SecurityEvaluationSummary(families=families)
