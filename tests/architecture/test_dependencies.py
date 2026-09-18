from __future__ import annotations

import ast
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "fediec"

_ALLOWED_IMPORT_PREFIXES: dict[str, tuple[str, ...]] = {
    "enums": (),
    "types": ("enums",),
    "paths": ("enums", "types"),
    "artifacts": ("enums", "types"),
    "config": ("enums", "types", "paths"),
    "datasets": ("enums", "types", "paths", "config"),
    "workflows": (
        "enums",
        "types",
        "paths",
        "config",
        "datasets",
        "models",
        "baselines",
        "training",
        "artifacts",
        "workflows",
    ),
    "cli": ("enums", "types", "workflows"),
}


def _module_key(relative_path: Path) -> str:
    return relative_path.with_suffix("").parts[0]


def _stripped_module(dotted: str) -> str | None:
    if dotted == "fediec":
        return ""
    if dotted.startswith("fediec."):
        return dotted.removeprefix("fediec.")
    return None


def test_import_direction_is_respected() -> None:
    offenders: list[str] = []
    for path in sorted(SRC_ROOT.rglob("*.py")):
        relative = path.relative_to(SRC_ROOT)
        if relative.name == "__init__.py":
            continue
        key = _module_key(relative)
        allowed = _ALLOWED_IMPORT_PREFIXES.get(key)
        if allowed is None:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom) or node.module is None:
                continue
            stripped = _stripped_module(node.module)
            if stripped is None:
                continue
            imported_key = stripped.split(".")[0] if stripped else ""
            if imported_key == key:
                continue
            if not any(stripped.startswith(prefix) for prefix in allowed):
                offenders.append(
                    f"{relative}:{node.lineno} imports '{node.module}' (not allowed for '{key}')"
                )
    assert not offenders, offenders


def test_nothing_in_src_imports_tests() -> None:
    offenders: list[str] = []
    for path in sorted(SRC_ROOT.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if module == "tests" or module.startswith("tests."):
                    offenders.append(f"{path.relative_to(SRC_ROOT)}:{node.lineno}")
            elif isinstance(node, ast.Import):
                if any(
                    alias.name == "tests" or alias.name.startswith("tests.") for alias in node.names
                ):
                    offenders.append(f"{path.relative_to(SRC_ROOT)}:{node.lineno}")
    assert not offenders, f"production code must never import tests: {offenders}"


def test_nothing_imports_cli() -> None:
    offenders: list[str] = []
    for path in sorted(SRC_ROOT.rglob("*.py")):
        if path.name == "cli.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            imports_cli_module = node.module == "fediec.cli"
            imports_cli_attribute = node.module == "fediec" and any(
                alias.name == "cli" for alias in node.names
            )
            if imports_cli_module or imports_cli_attribute:
                offenders.append(f"{path.relative_to(SRC_ROOT)}:{node.lineno}")
    assert not offenders, f"cli.py must not be imported by any other module: {offenders}"


def _build_import_graph() -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}
    for path in sorted(SRC_ROOT.rglob("*.py")):
        relative = path.relative_to(SRC_ROOT)
        if relative.name == "__init__.py":
            continue
        node_name = str(relative.with_suffix("")).replace("/", ".").replace("\\", ".")
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        edges: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                stripped = _stripped_module(node.module)
                if stripped:
                    edges.add(stripped)
        graph[node_name] = edges
    return graph


def _find_cycle(graph: dict[str, set[str]]) -> list[str] | None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, path: list[str]) -> list[str] | None:
        if node in visiting:
            return [*path, node]
        if node in visited or node not in graph:
            return None
        visiting.add(node)
        for neighbor in graph[node]:
            result = visit(neighbor, [*path, node])
            if result is not None:
                return result
        visiting.discard(node)
        visited.add(node)
        return None

    for start in graph:
        cycle = visit(start, [])
        if cycle is not None:
            return cycle
    return None


def test_no_circular_imports() -> None:
    cycle = _find_cycle(_build_import_graph())
    assert cycle is None, f"circular import detected: {' -> '.join(cycle or [])}"
