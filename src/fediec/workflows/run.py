from __future__ import annotations

from fediec.baselines.contracts import active_baseline_contracts
from fediec.config import load_config
from fediec.enums import ExperimentName
from fediec.models.conditional_flow import build_conditional_interaction_flow


def run_experiment(experiment: ExperimentName) -> None:
    configuration = load_config()
    configured_model = configuration.model
    model = build_conditional_interaction_flow(configuration.training.seeds[0])
    baselines = active_baseline_contracts()
    if (
        model.target_dimension != configured_model.interaction_dimension
        or model.context_dimension != configured_model.context_dimension
    ):
        raise RuntimeError("active model contract does not match config.yaml's model dimensions")
    if any(
        contract.target_dimension != configured_model.interaction_dimension
        for contract in baselines
    ):
        raise RuntimeError("baseline target contracts do not match the active representation")
    raise RuntimeError(
        f"confirmatory execution for '{experiment}' is not started by protocol freeze; "
        "run an engineering smoke first and obtain an explicit execution instruction"
    )
