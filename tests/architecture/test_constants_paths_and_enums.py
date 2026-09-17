from __future__ import annotations

import ast
import importlib
from enum import StrEnum
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src" / "fediec"
TESTS_ROOT = REPO_ROOT / "tests"
_FORBIDDEN_WORDS = ("roadmap", "technical_doc")
_MAGIC_CONTEXT_WORDS = {
    "threshold",
    "tolerance",
    "epsilon",
    "ratio",
    "fraction",
    "sample",
    "count",
    "epoch",
    "round",
    "seed",
    "batch",
    "quantile",
    "alpha",
    "rate",
    "budget",
    "window",
    "replicate",
}
_PATH_WORDS = {"outputs", "results", "data", "raw", "processed", "reports", "experiments"}


def _source_files() -> list[Path]:
    return sorted(
        path for path in SRC_ROOT.rglob("*.py") if path.name not in {"types.py", "config.py"}
    )


def _location(path: Path, line: int) -> str:
    try:
        return f"{path.relative_to(SRC_ROOT)}:{line}"
    except ValueError:
        return f"{path}:{line}"


def _has_magic_context(names: set[str]) -> bool:
    return any(word in name for name in names for word in _MAGIC_CONTEXT_WORDS)


def find_suspicious_magic_numbers(paths: list[Path]) -> list[str]:
    offenders: list[str] = []
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        parents = {
            id(child): parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)
        }
        for node in ast.walk(tree):
            if (
                not isinstance(node, ast.Constant)
                or isinstance(node.value, bool)
                or not isinstance(node.value, int | float | complex)
            ):
                continue
            context_names: set[str] = set()
            ancestor = parents.get(id(node))
            while ancestor is not None:
                if isinstance(
                    ancestor, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef | ast.Module
                ):
                    break
                if isinstance(ancestor, ast.Assign):
                    context_names |= {
                        target.id.lower()
                        for target in ancestor.targets
                        if isinstance(target, ast.Name)
                    }
                elif isinstance(ancestor, ast.AnnAssign) and isinstance(ancestor.target, ast.Name):
                    context_names.add(ancestor.target.id.lower())
                elif isinstance(ancestor, ast.keyword) and ancestor.arg is not None:
                    context_names.add(ancestor.arg.lower())
                ancestor = parents.get(id(ancestor))
            if _has_magic_context(context_names):
                offenders.append(f"{_location(path, node.lineno)} ({node.value!r})")
    return offenders


def _is_path_fragment(value: str) -> bool:
    return "/" in value or value.lower() in _PATH_WORDS


def find_hardcoded_path_fragments(paths: list[Path]) -> list[str]:
    offenders: list[str] = []
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "Path"
            ):
                candidates = node.args
            elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
                candidates = (node.right,)
            elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                candidates = (node.left, node.right)
            else:
                continue
            for candidate in candidates:
                if (
                    isinstance(candidate, ast.Constant)
                    and isinstance(candidate.value, str)
                    and _is_path_fragment(candidate.value)
                ):
                    offenders.append(f"{_location(path, candidate.lineno)} ({candidate.value!r})")
    return offenders


def _written_strenum_member_count(class_node: ast.ClassDef) -> int:
    return sum(
        isinstance(statement, ast.Assign)
        and any(isinstance(target, ast.Name) for target in statement.targets)
        for statement in class_node.body
    )


def test_no_suspicious_scientific_magic_numbers() -> None:
    assert not find_suspicious_magic_numbers(_source_files())


def test_no_hardcoded_repository_path_fragments() -> None:
    paths = [path for path in _source_files() if path.name != "enums.py"]
    assert not find_hardcoded_path_fragments(paths)


def test_strenum_members_do_not_silently_alias() -> None:
    enums_module = importlib.import_module("fediec.enums")
    tree = ast.parse((SRC_ROOT / "enums.py").read_text(encoding="utf-8"))
    offenders: list[str] = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef) or not any(
            isinstance(base, ast.Name) and base.id == "StrEnum" for base in node.bases
        ):
            continue
        enum_class = getattr(enums_module, node.name)
        if not issubclass(enum_class, StrEnum):
            continue
        written_count = _written_strenum_member_count(node)
        if len(enum_class) != written_count:
            offenders.append(
                f"{node.name}: wrote {written_count} names but has {len(enum_class)} unique members"
            )
    assert not offenders, f"StrEnum duplicate string values silently create aliases: {offenders}"


def find_forbidden_words(paths: list[Path]) -> list[str]:
    offenders: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        for word in _FORBIDDEN_WORDS:
            if word in text:
                offenders.append(f"{path}: contains '{word}'")
    return offenders


def test_no_roadmap_or_technical_doc_mentions_in_source() -> None:
    this_file = Path(__file__).resolve()
    paths = [
        path
        for path in (*SRC_ROOT.rglob("*.py"), *TESTS_ROOT.rglob("*.py"))
        if path.resolve() != this_file
    ]
    assert not find_forbidden_words(paths)


def _newtype_alias_names() -> set[str]:
    tree = ast.parse((SRC_ROOT / "types.py").read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name)
            and node.value.func.id == "NewType"
        ):
            names |= {target.id for target in node.targets if isinstance(target, ast.Name)}
    return names


def find_literal_collections_that_should_be_enums(paths: list[Path]) -> list[str]:
    alias_names = _newtype_alias_names()
    offenders: list[str] = []
    for path in paths:
        if path.name in {"types.py", "enums.py"}:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(
                node, ast.Tuple | ast.List | ast.Dict | ast.Set | ast.SetComp | ast.GeneratorExp
            ):
                continue
            literal_values: set[str] = set()
            for child in ast.walk(node):
                if not (
                    isinstance(child, ast.Call)
                    and isinstance(child.func, ast.Name)
                    and child.func.id in alias_names
                    and len(child.args) == 1
                ):
                    continue
                argument = child.args[0]
                if isinstance(argument, ast.Constant) and isinstance(argument.value, str):
                    literal_values.add(argument.value)
            if len(literal_values) >= 2:
                offenders.append(
                    f"{_location(path, node.lineno)}: {len(literal_values)} distinct "
                    f"literals via the same NewType alias — use a StrEnum"
                )
    return offenders


def test_no_closed_literal_vocabularies_hidden_in_newtype_aliases() -> None:
    assert not find_literal_collections_that_should_be_enums(_source_files())
