"""Verifies CLI -> workflow wiring: every public command exists, maps to
exactly one workflow call, and every workflow module is actually
reachable from the CLI."""

from __future__ import annotations

import ast
from pathlib import Path

from fediec.cli import app
from fediec.enums import CliCommand

REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_MODULE = REPO_ROOT / "src" / "fediec" / "cli.py"
WORKFLOWS_ROOT = REPO_ROOT / "src" / "fediec" / "workflows"


def _registered_command_names() -> set[str]:
    names: set[str] = set()
    for command in app.registered_commands:
        if command.name:
            names.add(command.name)
        elif command.callback is not None:
            names.add(command.callback.__name__)
    return names


def test_registered_cli_commands_match_locked_public_cli() -> None:
    registered = _registered_command_names()
    expected = {member.value for member in CliCommand}
    assert registered == expected, (registered, expected)


def _workflow_call_targets(function_node: ast.FunctionDef) -> set[str]:
    targets: set[str] = set()
    for node in ast.walk(function_node):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id.endswith("_workflow")
        ):
            targets.add(node.func.value.id)
    return targets


def test_each_cli_command_delegates_to_exactly_one_workflow() -> None:
    tree = ast.parse(CLI_MODULE.read_text(encoding="utf-8"), filename=str(CLI_MODULE))
    command_functions = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and any(
            isinstance(decorator, ast.Call)
            and isinstance(decorator.func, ast.Attribute)
            and decorator.func.attr == "command"
            for decorator in node.decorator_list
        )
    ]
    assert command_functions, "no @app.command() functions found in cli.py"
    offenders: list[str] = []
    for function_node in command_functions:
        targets = _workflow_call_targets(function_node)
        if len(targets) != 1:
            offenders.append(f"{function_node.name}: delegates to {sorted(targets)}")
    assert not offenders, offenders


def test_every_workflow_module_is_imported_and_called_by_cli() -> None:
    workflow_modules = {
        path.stem
        for path in WORKFLOWS_ROOT.glob("*.py")
        if path.stem != "__init__"
    }
    tree = ast.parse(CLI_MODULE.read_text(encoding="utf-8"), filename=str(CLI_MODULE))
    imported_aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.ImportFrom)
            and node.module == "fediec.workflows"
            and node.names
        ):
            alias = node.names[0]
            imported_aliases[alias.asname or alias.name] = alias.name

    called_aliases: set[str] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
        ):
            called_aliases.add(node.func.value.id)

    imported_modules = set(imported_aliases.values())
    called_modules = {
        imported_aliases[alias] for alias in called_aliases if alias in imported_aliases
    }
    missing_import = workflow_modules - imported_modules
    missing_call = imported_modules - called_modules
    assert not missing_import, f"workflow modules never imported by cli.py: {missing_import}"
    assert not missing_call, f"workflow modules imported but never called by cli.py: {missing_call}"
