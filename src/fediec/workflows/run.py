from __future__ import annotations

from fediec.enums import ExperimentName


def run_experiment(experiment: ExperimentName) -> None:
    raise NotImplementedError(
        f"run is not yet implemented for '{experiment}': the model/"
        "training/evaluation modules have not been built."
    )
