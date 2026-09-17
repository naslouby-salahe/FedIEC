"""Requires Ruff, Pyright, and Semgrep checks to pass (technical_doc.md
Sec. 21). Custom Semgrep rules are materialized at runtime; no second YAML
is committed (Sec. 6.1, Sec. 15.3)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

from tests.architecture.semgrep_rules import RULES

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_ruff_passes() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "src", "tests"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_pyright_passes() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pyright", "src", "tests"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_semgrep_custom_rules_pass() -> None:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False
    ) as rules_file:
        yaml.safe_dump(RULES, rules_file)
        rules_path = Path(rules_file.name)
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "semgrep",
                "scan",
                "--config",
                str(rules_path),
                "--json",
                "--error",
                "src",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        findings_json: str = result.stdout or '{"results": []}'
        finding_count = len(json.loads(findings_json)["results"])
        assert finding_count == 0, findings_json
    finally:
        rules_path.unlink(missing_ok=True)
