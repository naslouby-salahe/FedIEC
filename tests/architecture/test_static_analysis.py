from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SEMGREP_RULES = REPO_ROOT / ".semgrep.yml"
SEMGREP_EXECUTABLE = Path(sys.executable).with_name("semgrep")


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
    result = subprocess.run(
        [
            str(SEMGREP_EXECUTABLE),
            "scan",
            "--config",
            str(SEMGREP_RULES),
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
