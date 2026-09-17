from __future__ import annotations

import ast
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "fediec"

_UNREACHABLE_BUT_JUSTIFIED = {
    "artifacts": "checksum/provenance IO for future public-source preprocessing",
}


def _module_name(path: Path) -> str:
    relative = path.relative_to(SRC_ROOT)
    return str(relative.with_suffix("")).replace("/", ".").replace("\\", ".")


def _build_import_graph() -> dict[str, set[str]]:
    all_modules = {
        _module_name(path) for path in SRC_ROOT.rglob("*.py") if path.name != "__init__.py"
    }
    graph: dict[str, set[str]] = {}
    for path in sorted(SRC_ROOT.rglob("*.py")):
        if path.name == "__init__.py":
            continue
        node_name = _module_name(path)
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        edges: set[str] = set()
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom) or not node.module:
                continue
            if not node.module.startswith("fediec"):
                continue
            target = node.module.removeprefix("fediec.").removeprefix("fediec")
            if not target:
                continue
            resolved_any = False
            for alias in node.names:
                candidate = f"{target}.{alias.name}"
                if candidate in all_modules:
                    edges.add(candidate)
                    resolved_any = True
            if not resolved_any:
                edges.add(target)
        graph[node_name] = edges
    return graph


def _reachable_from(graph: dict[str, set[str]], start: str) -> set[str]:
    seen: set[str] = set()
    stack = [start]
    while stack:
        current = stack.pop()
        if current in seen or current not in graph:
            continue
        seen.add(current)
        stack.extend(graph[current])
    return seen


def test_every_module_is_reachable_from_cli_or_explicitly_justified() -> None:
    graph = _build_import_graph()
    reachable = _reachable_from(graph, "cli")
    unreachable = set(graph) - reachable - {"cli"}
    unjustified = {
        module for module in unreachable if module not in _UNREACHABLE_BUT_JUSTIFIED
    }
    assert not unjustified, (
        f"modules unreachable from cli.py with no documented justification: "
        f"{unjustified}. Either wire them in or add a narrow, justified "
        f"exemption to _UNREACHABLE_BUT_JUSTIFIED."
    )


def test_justified_exemptions_are_still_real_modules() -> None:
    existing = {_module_name(path) for path in SRC_ROOT.rglob("*.py") if path.name != "__init__.py"}
    stale = set(_UNREACHABLE_BUT_JUSTIFIED) - existing
    assert not stale, f"exemption list references modules that no longer exist: {stale}"
