from __future__ import annotations

from fediec.enums import ExperimentName


def run_experiment(experiment: ExperimentName) -> None:
    raise NotImplementedError(
        f"run is not yet implemented for '{experiment.value}': the model/"
        "training/evaluation modules (Roadmap Sec. 40-51) have not been built."
    )
