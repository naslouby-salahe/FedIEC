from __future__ import annotations

from typer.testing import CliRunner

from fediec.cli import app


def test_plan_is_available_through_the_public_cli_without_execution() -> None:
    result = CliRunner().invoke(app, ["plan"])
    assert result.exit_code == 0, result.output
    assert "intent-value" in result.output
