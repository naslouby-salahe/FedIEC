from __future__ import annotations

import ast
import tokenize
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src" / "fediec"
TESTS_ROOT = REPO_ROOT / "tests"

_ALLOWED_COMMENT_PREFIXES = ("pyright:", "type:", "noqa", "pragma:")


def _all_py_files() -> list[Path]:
    return sorted({*SRC_ROOT.rglob("*.py"), *TESTS_ROOT.rglob("*.py")})


def find_forbidden_comments(paths: list[Path]) -> list[str]:
    offenders: list[str] = []
    for path in paths:
        with path.open("rb") as handle:
            tokens = tokenize.tokenize(handle.readline)
            for token in tokens:
                if token.type != tokenize.COMMENT:
                    continue
                body = token.string.lstrip("#").strip()
                if body.startswith(_ALLOWED_COMMENT_PREFIXES):
                    continue
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{token.start[0]}")
    return offenders


_DocumentableNode = ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef


def _has_docstring(node: _DocumentableNode) -> bool:
    body = node.body
    return bool(
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    )


def find_forbidden_docstrings(paths: list[Path]) -> list[str]:
    offenders: list[str] = []
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        if _has_docstring(tree):
            offenders.append(f"{path.relative_to(REPO_ROOT)}:1 (module docstring)")
        for node in ast.walk(tree):
            is_documentable = isinstance(
                node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef
            )
            if is_documentable and _has_docstring(node):  # type: ignore[arg-type]
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{node.lineno} ({node.name})")
    return offenders


def test_no_comments() -> None:
    this_file = Path(__file__).resolve()
    paths = [path for path in _all_py_files() if path.resolve() != this_file]
    assert not find_forbidden_comments(paths)


def test_no_docstrings() -> None:
    assert not find_forbidden_docstrings(_all_py_files())
