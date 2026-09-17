from __future__ import annotations

import ast
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "fediec"
TYPES_MODULE = SRC_ROOT / "types.py"
_FORBIDDEN_PRIMITIVES = {"int", "float", "str", "object", "Any"}
_GENERIC_CONSTRAINED_ALIAS_NAMES = {
    "NonNegativeInt",
    "PositiveInt",
    "SignedInt",
    "NonNegativeFloat",
    "PositiveFloat",
    "FiniteFloat",
    "UnitInterval",
    "OpenUnitInterval",
}
_LOGGER_METHODS = {"info", "warning", "error", "debug"}


def _iter_source_files() -> list[Path]:
    return sorted(SRC_ROOT.rglob("*.py"))


def _location(path: Path, line: int) -> str:
    try:
        return f"{path.relative_to(SRC_ROOT)}:{line}"
    except ValueError:
        return f"{path}:{line}"


def _annotation_names(annotation: ast.expr | None) -> list[str]:
    return (
        [node.id for node in ast.walk(annotation) if isinstance(node, ast.Name)]
        if annotation
        else []
    )


def _call_name(call: ast.Call) -> str | None:
    return (
        call.func.id
        if isinstance(call.func, ast.Name)
        else call.func.attr
        if isinstance(call.func, ast.Attribute)
        else None
    )


def _trees(paths: list[Path]):
    for path in paths:
        if path != TYPES_MODULE:
            yield path, ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def find_constrained_alias_definitions(paths: list[Path]) -> list[str]:
    return [
        _location(path, node.lineno)
        for path, tree in _trees(paths)
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and _call_name(node) == "Field"
        and any(key.arg in {"ge", "gt", "le", "lt", "allow_inf_nan"} for key in node.keywords)
    ]


def find_newtype_definitions(paths: list[Path]) -> list[str]:
    return [
        _location(path, node.lineno)
        for path, tree in _trees(paths)
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and _call_name(node) == "NewType"
    ]


def find_forbidden_primitive_signatures(paths: list[Path]) -> list[str]:
    offenders: list[str] = []
    for path, tree in _trees(paths):
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                continue
            annotations = (
                *(arg.annotation for arg in node.args.posonlyargs),
                *(arg.annotation for arg in node.args.args),
                *(arg.annotation for arg in node.args.kwonlyargs),
                node.args.vararg.annotation if node.args.vararg else None,
                node.args.kwarg.annotation if node.args.kwarg else None,
                node.returns,
            )
            for annotation in annotations:
                for name in _annotation_names(annotation):
                    if name in _FORBIDDEN_PRIMITIVES:
                        offenders.append(
                            f"{_location(path, node.lineno)} ({node.name}) uses raw '{name}'"
                        )
    return offenders


def find_forbidden_primitive_variable_annotations(paths: list[Path]) -> list[str]:
    return [
        f"{_location(path, node.lineno)} uses raw '{name}'"
        for path, tree in _trees(paths)
        for node in ast.walk(tree)
        if isinstance(node, ast.AnnAssign)
        for name in _annotation_names(node.annotation)
        if name in _FORBIDDEN_PRIMITIVES
    ]


def find_generic_constrained_alias_references(paths: list[Path]) -> list[str]:
    return [
        f"{_location(path, node.lineno)} references '{node.id}'"
        for path, tree in _trees(paths)
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and node.id in _GENERIC_CONSTRAINED_ALIAS_NAMES
    ]


def find_string_literal_log_event_names(paths: list[Path]) -> list[str]:
    return [
        _location(path, node.lineno)
        for path, tree in _trees(paths)
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in _LOGGER_METHODS
        and node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    ]


def find_string_literal_table_columns(paths: list[Path]) -> list[str]:
    return [
        _location(path, node.lineno)
        for path, tree in _trees(paths)
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "add_column"
        and node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    ]


def test_constrained_alias_definitions_only_in_types_py() -> None:
    assert not find_constrained_alias_definitions(_iter_source_files())


def test_newtype_definitions_only_in_types_py() -> None:
    assert not find_newtype_definitions(_iter_source_files())


def test_no_forbidden_primitive_signatures_outside_types_py() -> None:
    assert not find_forbidden_primitive_signatures(_iter_source_files())


def test_no_forbidden_primitive_variable_annotations_outside_types_py() -> None:
    assert not find_forbidden_primitive_variable_annotations(_iter_source_files())


def test_generic_constrained_aliases_never_referenced_outside_types_py() -> None:
    assert not find_generic_constrained_alias_references(_iter_source_files())


def test_no_string_literal_log_event_names() -> None:
    assert not find_string_literal_log_event_names(_iter_source_files())


def test_no_string_literal_table_columns() -> None:
    assert not find_string_literal_table_columns(_iter_source_files())
