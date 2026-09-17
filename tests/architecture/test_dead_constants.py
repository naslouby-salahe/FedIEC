"""Flags module-level constants defined in src/fediec but never referenced
anywhere else. types.py and enums.py are excluded: they exist specifically
to declare domain vocabulary ahead of its first consumer."""

from __future__ import annotations

import ast
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "fediec"
_EXEMPT_MODULES = {"types.py", "enums.py"}

# Individual constants that are real, needed infrastructure ahead of
# their first caller (mirrors test_function_reachability.py's exemption
# for the function that is their only intended consumer).
_CONSTANT_LEVEL_EXEMPTIONS: set[tuple[str, str]] = set()


def _module_level_constant_names(tree: ast.Module) -> list[tuple[str, int]]:
    names: list[tuple[str, int]] = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            names.extend(
                (target.id, node.lineno)
                for target in node.targets
                if isinstance(target, ast.Name) and not target.id.startswith("__")
            )
        elif (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and not node.target.id.startswith("__")
        ):
            names.append((node.target.id, node.lineno))
    return names


def _reference_count(tree: ast.Module, name: str) -> int:
    count = 0
    for node in ast.walk(tree):
        matches_name = isinstance(node, ast.Name) and node.id == name
        matches_attribute = isinstance(node, ast.Attribute) and node.attr == name
        if matches_name or matches_attribute:
            count += 1
    return count


def test_no_dead_module_level_constants() -> None:
    offenders: list[str] = []
    for path in sorted(SRC_ROOT.rglob("*.py")):
        if path.name in _EXEMPT_MODULES:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        module = path.stem
        for name, lineno in _module_level_constant_names(tree):
            if (module, name) in _CONSTANT_LEVEL_EXEMPTIONS:
                continue
            # Definition site itself counts as one reference (the Name
            # target of the Assign/AnnAssign); anything <= 1 means no
            # other use exists in this file.
            if _reference_count(tree, name) <= 1:
                offenders.append(f"{path.relative_to(SRC_ROOT)}:{lineno} defines unused '{name}'")
    assert not offenders, offenders
