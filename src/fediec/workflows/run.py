from __future__ import annotations

from fediec.baselines.contracts import active_baseline_contracts
from fediec.enums import ExperimentName
from fediec.models.conditional_flow import build_conditional_interaction_flow


def run_experiment(experiment: ExperimentName) -> None:
    model = build_conditional_interaction_flow()
    baselines = active_baseline_contracts()
    if model.target_dimension != 19 or model.context_dimension != 3:
        raise RuntimeError("active model contract is not 19-D target / 3-D intent")
    if any(contract.target_dimension != 19 for contract in baselines):
        raise RuntimeError("baseline target contracts do not match the active representation")
    raise RuntimeError(
        f"confirmatory execution for '{experiment}' is not started by protocol freeze; "
        "run an engineering smoke first and obtain an explicit execution instruction"
    )
