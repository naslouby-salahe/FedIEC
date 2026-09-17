from __future__ import annotations

import structlog
import typer
from rich.console import Console
from rich.table import Table

from fediec.enums import (
    CheckStatus,
    CliCommand,
    ExperimentName,
    LogEvent,
    RunStatus,
    TableColumn,
    TerminalColor,
)
from fediec.workflows import collect as collect_workflow
from fediec.workflows import doctor as doctor_workflow
from fediec.workflows import plan as plan_workflow
from fediec.workflows import prepare as prepare_workflow
from fediec.workflows import preprocess as preprocess_workflow
from fediec.workflows import report as report_workflow
from fediec.workflows import run as run_workflow
from fediec.workflows import smoke as smoke_workflow
from fediec.workflows import status as status_workflow

app = typer.Typer(add_completion=False, no_args_is_help=True)
# typer.Argument's overloaded stub is partially-unknown under Pyright strict
# mode (a third-party stub gap, not a project typing error).
_EXPERIMENT_ARGUMENT = typer.Argument(  # pyright: ignore[reportUnknownMemberType]
    ..., help="Named experiment to run."
)
console = Console()
logger = structlog.get_logger()

_CHECK_STATUS_STYLE: dict[CheckStatus, TerminalColor] = {
    CheckStatus.PASS: TerminalColor.GREEN,
    CheckStatus.WARN: TerminalColor.YELLOW,
    CheckStatus.FAIL: TerminalColor.RED,
}

_RUN_STATUS_STYLE: dict[RunStatus, TerminalColor] = {
    RunStatus.PENDING: TerminalColor.YELLOW,
    RunStatus.RUNNING: TerminalColor.BLUE,
    RunStatus.COMPLETED: TerminalColor.GREEN,
    RunStatus.FAILED: TerminalColor.RED,
}


@app.command()
def doctor() -> None:
    logger.info(LogEvent.DOCTOR_START)
    report = doctor_workflow.run_doctor()
    table = Table(title=f"fediec {CliCommand.DOCTOR.value}")
    table.add_column(TableColumn.CHECK)
    table.add_column(TableColumn.STATUS)
    table.add_column(TableColumn.DETAIL)
    for check in report.checks:
        style = _CHECK_STATUS_STYLE[check.status]
        table.add_row(check.label, f"[{style}]{check.status.value}[/{style}]", check.detail)
    console.print(table)
    logger.info(LogEvent.DOCTOR_DONE, overall_status=report.overall_status.value)
    if report.overall_status == CheckStatus.FAIL:
        raise typer.Exit(code=1)


@app.command()
def collect() -> None:
    logger.info(LogEvent.COLLECT_START)
    collect_workflow.run_collect()


@app.command()
def preprocess() -> None:
    logger.info(LogEvent.PREPROCESS_START)
    preprocess_workflow.run_preprocess()


@app.command()
def prepare() -> None:
    logger.info(LogEvent.PREPARE_START)
    prepare_workflow.run_prepare()


@app.command()
def plan() -> None:
    logger.info(LogEvent.PLAN_START)
    experiment_plan = plan_workflow.resolve_plan()
    table = Table(title=f"fediec {CliCommand.PLAN.value}")
    table.add_column(TableColumn.EXPERIMENT)
    table.add_column(TableColumn.SEED)
    for cell in experiment_plan.cells:
        table.add_row(cell.experiment.value, str(cell.seed))
    console.print(table)
    logger.info(LogEvent.PLAN_DONE, cell_count=len(experiment_plan.cells))


@app.command()
def smoke() -> None:
    logger.info(LogEvent.SMOKE_START)
    smoke_workflow.run_smoke()


@app.command(name="run")
def run_command(
    experiment: ExperimentName = _EXPERIMENT_ARGUMENT,
) -> None:
    logger.info(LogEvent.RUN_START, experiment=experiment.value)
    run_workflow.run_experiment(experiment)


@app.command()
def status() -> None:
    logger.info(LogEvent.STATUS_START)
    status_report = status_workflow.resolve_status()
    table = Table(title=f"fediec {CliCommand.STATUS.value}")
    table.add_column(TableColumn.EXPERIMENT)
    table.add_column(TableColumn.SEED)
    table.add_column(TableColumn.STATUS)
    for cell_status in status_report.cells:
        style = _RUN_STATUS_STYLE[cell_status.status]
        table.add_row(
            cell_status.cell.experiment.value,
            str(cell_status.cell.seed),
            f"[{style}]{cell_status.status.value}[/{style}]",
        )
    console.print(table)
    logger.info(LogEvent.STATUS_DONE, cell_count=len(status_report.cells))


@app.command()
def report() -> None:
    logger.info(LogEvent.REPORT_START)
    report_workflow.run_report()


if __name__ == "__main__":
    app()
