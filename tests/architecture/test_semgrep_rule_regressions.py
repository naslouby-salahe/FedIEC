from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SEMGREP_RULES = REPO_ROOT / ".semgrep.yml"
SEMGREP_CASES = REPO_ROOT / "tests" / "architecture" / "semgrep_cases.py"
SEMGREP_EXECUTABLE = Path(sys.executable).with_name("semgrep")

_REQUIRED_RULE_IDS = {
    "no-primitive-function-boundary",
    "no-nested-primitive-function-boundary",
    "no-generic-constrained-alias-outside-types",
    "no-runtime-source-introspection",
    "no-physical-collection-scaffold",
    "no-type-ignore-suppression",
}


def test_semgrep_boundary_rules_reject_known_violations() -> None:
    result = subprocess.run(
        [
            str(SEMGREP_EXECUTABLE),
            "scan",
            "--config",
            str(SEMGREP_RULES),
            "--json",
            str(SEMGREP_CASES),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    findings = json.loads(result.stdout)["results"]
    found_rule_ids = {finding["check_id"] for finding in findings}
    assert found_rule_ids >= _REQUIRED_RULE_IDS
    findings_by_rule = {
        rule_id: [finding for finding in findings if finding["check_id"] == rule_id]
        for rule_id in _REQUIRED_RULE_IDS
    }
    assert len(findings_by_rule["no-primitive-function-boundary"]) >= 4
    assert len(findings_by_rule["no-nested-primitive-function-boundary"]) >= 6
    assert len(findings_by_rule["no-generic-constrained-alias-outside-types"]) >= 8
