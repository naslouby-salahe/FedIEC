from __future__ import annotations

import ast
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "fediec"
TYPES_MODULE = SRC_ROOT / "types.py"

_FORBIDDEN_PARAMETER_RETURN_ANNOTATIONS = {"int", "float", "str", "object", "Any"}

_EXEMPT_MODULES: frozenset[Path] = frozenset()


def _iter_source_files() -> list[Path]:
    return sorted(p for p in SRC_ROOT.rglob("*.py") if p not in _EXEMPT_MODULES)


def _constrained_field_calls(tree: ast.Module) -> list[ast.Call]:
    calls: list[ast.Call] = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "Field"
            and any(
                keyword.arg in {"ge", "gt", "le", "lt", "allow_inf_nan"}
                for keyword in node.keywords
            )
        ):
            calls.append(node)
    return calls


def test_constrained_alias_definitions_only_in_types_py() -> None:
    offenders: list[str] = []
    for path in _iter_source_files():
        if path == TYPES_MODULE:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for call in _constrained_field_calls(tree):
            offenders.append(f"{path.relative_to(SRC_ROOT)}:{call.lineno}")
    assert not offenders, (
        "Constrained numeric aliases (Field(ge=/gt=/le=/lt=/allow_inf_nan=)) "
        f"must live only in types.py, found in: {offenders}"
    )


def test_newtype_definitions_only_in_types_py() -> None:
    offenders: list[str] = []
    for path in _iter_source_files():
        if path == TYPES_MODULE:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "NewType"
            ):
                offenders.append(f"{path.relative_to(SRC_ROOT)}:{node.lineno}")
    assert not offenders, f"NewType(...) must live only in types.py, found in: {offenders}"


def _annotation_names(annotation: ast.expr | None) -> list[str]:
    if annotation is None:
        return []
    names: list[str] = []
    for node in ast.walk(annotation):
        if isinstance(node, ast.Name):
            names.append(node.id)
    return names


def test_no_forbidden_primitive_signatures_outside_types_py() -> None:
    offenders: list[str] = []
    for path in _iter_source_files():
        if path == TYPES_MODULE:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                continue
            annotations = [
                *(arg.annotation for arg in node.args.args),
                *(arg.annotation for arg in node.args.kwonlyargs),
                node.returns,
            ]
            for annotation in annotations:
                for name in _annotation_names(annotation):
                    if name in _FORBIDDEN_PARAMETER_RETURN_ANNOTATIONS:
                        offenders.append(
                            f"{path.relative_to(SRC_ROOT)}:{node.lineno} "
                            f"({node.name}) uses raw '{name}'"
                        )
    assert not offenders, (
        "Raw float/int/str/object/Any are forbidden as function/method "
        f"parameter or return annotations outside types.py: {offenders}"
    )
