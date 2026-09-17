from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src" / "fediec"
CONFIG_MODULE = SRC_ROOT / "config.py"


def test_only_config_yaml_is_committed() -> None:
    yaml_files = [
        path
        for path in REPO_ROOT.rglob("*.y*ml")
        if ".venv" not in path.parts and path.name != "config.yaml"
    ]
    assert not yaml_files, f"config.yaml must be the only committed YAML file: {yaml_files}"


def test_only_config_py_parses_yaml() -> None:
    offenders: list[str] = []
    for path in SRC_ROOT.rglob("*.py"):
        if path == CONFIG_MODULE:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) and any(alias.name == "yaml" for alias in node.names):
                offenders.append(f"{path.relative_to(SRC_ROOT)}:{node.lineno}")
            if isinstance(node, ast.ImportFrom) and node.module == "yaml":
                offenders.append(f"{path.relative_to(SRC_ROOT)}:{node.lineno}")
    assert not offenders, f"Only config.py may import yaml, found in: {offenders}"


def _config_type_names(annotation: ast.expr | None) -> list[str]:
    if annotation is None:
        return []
    names: list[str] = []
    for node in ast.walk(annotation):
        if isinstance(node, ast.Name):
            names.append(node.id)
        elif isinstance(node, ast.Attribute):
            names.append(node.attr)
    return names


def test_config_models_do_not_cross_function_boundaries() -> None:
    offenders: list[str] = []
    for path in SRC_ROOT.rglob("*.py"):
        if path == CONFIG_MODULE:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                continue
            annotations = (
                *(argument.annotation for argument in node.args.posonlyargs),
                *(argument.annotation for argument in node.args.args),
                *(argument.annotation for argument in node.args.kwonlyargs),
                node.args.vararg.annotation if node.args.vararg else None,
                node.args.kwarg.annotation if node.args.kwarg else None,
                node.returns,
            )
            for annotation in annotations:
                for name in _config_type_names(annotation):
                    if name == "FediecConfig" or name.endswith("Section"):
                        offenders.append(
                            f"{path.relative_to(SRC_ROOT)}:{node.lineno} "
                            f"({node.name}) references config type '{name}'"
                        )
    assert not offenders, (
        f"Config sections must be read via load_config() inside the function body: {offenders}"
    )
