from __future__ import annotations

from fediec.enums import RunStatus
from fediec.paths import resolve_run_manifest_path
from fediec.types import DomainRecord
from fediec.workflows.plan import ExperimentPlanCell, resolve_plan


class ExperimentCellStatus(DomainRecord):
    cell: ExperimentPlanCell
    status: RunStatus


class StatusReport(DomainRecord):
    cells: tuple[ExperimentCellStatus, ...]


def _cell_status(cell: ExperimentPlanCell) -> RunStatus:
    manifest_path = resolve_run_manifest_path(cell.experiment, cell.seed)
    return RunStatus.COMPLETED if manifest_path.exists() else RunStatus.PENDING


def resolve_status() -> StatusReport:
    plan = resolve_plan()
    cells = tuple(ExperimentCellStatus(cell=cell, status=_cell_status(cell)) for cell in plan.cells)
    return StatusReport(cells=cells)
