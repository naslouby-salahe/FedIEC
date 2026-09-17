from __future__ import annotations

import ast
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "fediec"

_MODULE_LEVEL_EXEMPTIONS = {"artifacts"}

_FUNCTION_LEVEL_EXEMPTIONS = {("paths", "resolve_processed_dataset_directory")}


def _module_name(path: Path) -> str:
    relative = path.relative_to(SRC_ROOT)
    return str(relative.with_suffix("")).replace("/", ".").replace("\\", ".")


def _is_cli_command(function_node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return any(
        isinstance(decorator, ast.Call)
        and isinstance(decorator.func, ast.Attribute)
        and decorator.func.attr == "command"
        for decorator in function_node.decorator_list
    )


def _defined_functions(paths: list[Path]) -> list[tuple[str, str, int]]:
    definitions: list[tuple[str, str, int]] = []
    for path in paths:
        module = _module_name(path)
        if module in _MODULE_LEVEL_EXEMPTIONS:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                continue
            if node.name.startswith("__") and node.name.endswith("__"):
                continue
            if module == "cli" and _is_cli_command(node):
                continue
            definitions.append((module, node.name, node.lineno))
    return definitions


def _all_referenced_names(paths: list[Path]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                counts[node.id] = counts.get(node.id, 0) + 1
            elif isinstance(node, ast.Attribute):
                counts[node.attr] = counts.get(node.attr, 0) + 1
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                counts[node.name] = counts.get(node.name, 0) + 1
    return counts


def test_every_function_is_referenced_beyond_its_own_definition() -> None:
    paths = sorted(SRC_ROOT.rglob("*.py"))
    definitions = _defined_functions(paths)
    reference_counts = _all_referenced_names(paths)
    offenders = [
        f"{module}.py:{lineno} defines '{name}' which is never referenced elsewhere"
        for module, name, lineno in definitions
        if reference_counts.get(name, 0) <= 1 and (module, name) not in _FUNCTION_LEVEL_EXEMPTIONS
    ]
    assert not offenders, offenders
