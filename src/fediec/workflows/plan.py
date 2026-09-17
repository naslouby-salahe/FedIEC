from __future__ import annotations

from fediec.config import load_config
from fediec.enums import ExperimentName
from fediec.types import DomainRecord, Seed


class ExperimentPlanCell(DomainRecord):
    experiment: ExperimentName
    seed: Seed


class ExperimentPlan(DomainRecord):
    cells: tuple[ExperimentPlanCell, ...]


def resolve_plan() -> ExperimentPlan:
    config = load_config()
    cells = tuple(
        ExperimentPlanCell(experiment=experiment, seed=seed)
        for experiment in ExperimentName
        for seed in config.training.seeds
    )
    return ExperimentPlan(cells=cells)
