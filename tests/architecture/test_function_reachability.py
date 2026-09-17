"""Every function/method defined in src/fediec must be reachable, directly
or transitively, from a CLI command in cli.py.

This is a name-reference heuristic, not full interprocedural analysis: a
defined function is "referenced" if its name appears anywhere else in
src/fediec as a Name or an attribute access (covers direct calls,
dict-of-callables entries like _DATASET_AVAILABILITY_CHECK, and property
access). The known limitation is that two functions sharing a name in
different modules are indistinguishable to this check — a real duplicate
name could mask one dead sibling. Given this codebase's flat one-name-
per-responsibility style, that risk is low; test_dead_code.py's
module-level reachability check plus this one together cover the
practical cases.
"""

from __future__ import annotations

import ast
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "fediec"

# Modules that are themselves not yet reachable from cli.py (see
# test_dead_code.py) are skipped here too, rather than duplicating that
# exemption reasoning at the function level.
_MODULE_LEVEL_EXEMPTIONS = {"artifacts"}

# Individual functions that are real, needed infrastructure ahead of their
# first caller: the output-directory layout they implement is already
# part of the locked repository tree, and the preprocess workflow that
# will call this (not built yet) needs it unchanged from day one.
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
    """Returns (module, function_name, lineno) for every non-dunder,
    non-CLI-command function/method definition."""
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
    """Counts every Name/Attribute identifier occurrence across all of
    src/fediec, including the definition sites themselves (a defined
    function referenced only by its own `def` line has count 1, which
    this test treats as unreferenced)."""
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
