from __future__ import annotations

import ast
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "fediec"
TYPES_MODULE = SRC_ROOT / "types.py"

_FORBIDDEN_PARAMETER_RETURN_ANNOTATIONS = {"int", "float", "str", "object", "Any"}

# The eight generic constrained-primitive aliases defined in types.py.
# These must only ever be *referenced* inside types.py (to build a semantic
# alias); every other module must use a semantically named alias instead,
# even when two aliases share the same underlying constraint.
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


def test_no_forbidden_primitive_variable_annotations_outside_types_py() -> None:
    """Catches module/class-level annotated assignments such as
    `_STYLE: dict[Status, str] = {...}`, which function-signature scanning
    alone does not see."""
    offenders: list[str] = []
    for path in _iter_source_files():
        if path == TYPES_MODULE:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.AnnAssign):
                continue
            for name in _annotation_names(node.annotation):
                if name in _FORBIDDEN_PARAMETER_RETURN_ANNOTATIONS:
                    location = f"{path.relative_to(SRC_ROOT)}:{node.lineno}"
                    offenders.append(f"{location} uses raw '{name}'")
    assert not offenders, (
        "Raw float/int/str/object/Any are forbidden in module/class-level "
        f"variable annotations outside types.py: {offenders}"
    )


def test_generic_constrained_aliases_never_referenced_outside_types_py() -> None:
    """NonNegativeInt/PositiveInt/etc. exist only to build named semantic
    aliases in types.py. Every other module must import and use one of
    those semantic aliases, never the generic alias directly."""
    offenders: list[str] = []
    for path in _iter_source_files():
        if path == TYPES_MODULE:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id in _GENERIC_CONSTRAINED_ALIAS_NAMES:
                location = f"{path.relative_to(SRC_ROOT)}:{node.lineno}"
                offenders.append(f"{location} references '{node.id}'")
    assert not offenders, (
        "Generic constrained-primitive aliases must only be referenced "
        f"inside types.py; use a semantic alias instead: {offenders}"
    )


def test_no_string_literal_log_event_names() -> None:
    """Log event names must come from enums.LogEvent, not ad hoc strings,
    so every event identity is centralized and greppable."""
    offenders: list[str] = []
    for path in _iter_source_files():
        if path == TYPES_MODULE:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr in _LOGGER_METHODS
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "logger"
            ):
                continue
            if node.args and isinstance(node.args[0], ast.Constant) and isinstance(
                node.args[0].value, str
            ):
                offenders.append(f"{path.relative_to(SRC_ROOT)}:{node.lineno}")
    assert not offenders, (
        f"logger.*() event name must be an enums.LogEvent member, not a raw string: {offenders}"
    )


def test_no_string_literal_table_columns() -> None:
    """CLI table column headers must come from enums.TableColumn."""
    offenders: list[str] = []
    for path in _iter_source_files():
        if path == TYPES_MODULE:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "add_column"
            ):
                continue
            if node.args and isinstance(node.args[0], ast.Constant) and isinstance(
                node.args[0].value, str
            ):
                offenders.append(f"{path.relative_to(SRC_ROOT)}:{node.lineno}")
    assert not offenders, (
        f".add_column() header must be an enums.TableColumn member, not a raw string: {offenders}"
    )
