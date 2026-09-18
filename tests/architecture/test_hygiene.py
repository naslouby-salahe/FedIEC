from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src" / "fediec"
TESTS_ROOT = REPO_ROOT / "tests"

_TODO_PATTERN = re.compile(r"\b(TODO|FIXME|XXX)\b")

_GENERIC_DUMPING_GROUND_STEMS = {"utils", "helpers", "common", "misc", "core"}

_FORBIDDEN_TOP_LEVEL_NAMES = {"claims", "claim_registry", "claim-gates", "audit"}

_STALE_NAME_MARKERS = ("_new", "_old", "_v2", "_final2", "_fixed", "_updated", "_latest")


def _all_py_files() -> list[Path]:
    return sorted({*SRC_ROOT.rglob("*.py"), *TESTS_ROOT.rglob("*.py")})


def test_no_todo_fixme_markers() -> None:
    this_file = Path(__file__).resolve()
    offenders: list[str] = []
    for path in _all_py_files():
        if path.resolve() == this_file:
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if _TODO_PATTERN.search(line):
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{lineno}")
    assert not offenders, f"unresolved TODO/FIXME/XXX markers: {offenders}"


def test_no_generic_dumping_ground_modules() -> None:
    offenders = [
        str(path.relative_to(REPO_ROOT))
        for path in SRC_ROOT.rglob("*.py")
        if path.stem in _GENERIC_DUMPING_GROUND_STEMS
    ]
    assert not offenders, f"generic dumping-ground module names are forbidden: {offenders}"


def test_no_forbidden_top_level_packages() -> None:
    offenders = [name for name in _FORBIDDEN_TOP_LEVEL_NAMES if (SRC_ROOT / name).exists()]
    assert not offenders, f"forbidden top-level packages present: {offenders}"


def test_no_docker_files() -> None:
    offenders = [
        str(path.relative_to(REPO_ROOT))
        for path in REPO_ROOT.rglob("*")
        if path.name in {"Dockerfile", "docker-compose.yml", "docker-compose.yaml"}
        and ".venv" not in path.parts
    ]
    assert not offenders, f"Docker is forbidden in this repository: {offenders}"


def test_no_stale_version_suffixed_module_names() -> None:
    offenders = [
        str(path.relative_to(REPO_ROOT))
        for path in SRC_ROOT.rglob("*.py")
        if any(marker in path.stem.lower() for marker in _STALE_NAME_MARKERS)
    ]
    assert not offenders, f"stale/versioned module names are forbidden: {offenders}"
