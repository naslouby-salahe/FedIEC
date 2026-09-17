"""Custom Semgrep rule bodies, materialized to a temp YAML file at test time
by test_static_analysis.py (technical_doc.md Sec. 15.3: no committed
.semgrep.yml under the one-YAML rule).
"""

from __future__ import annotations

# Files where converting an enum to its serialized value is a genuine
# boundary (CLI display/logging, filesystem path segments, an
# error-message string naming the unimplemented experiment) rather than an
# escape from enum typing.
_VALUE_BOUNDARY_EXCLUDES = [
    "src/fediec/cli.py",
    "src/fediec/paths.py",
    "src/fediec/workflows/doctor.py",
    "src/fediec/workflows/run.py",
]

RULES: dict[str, object] = {
    "rules": [
        {
            "id": "no-enum-value-outside-boundary",
            "languages": ["python"],
            "message": (
                "Enum '.value' used outside a declared serialization/display "
                "boundary. Operate on the enum member itself; convert to "
                "'.value' only at a genuine CLI/logging/filesystem boundary."
            ),
            "severity": "ERROR",
            "pattern": "$X.value",
            "paths": {"exclude": _VALUE_BOUNDARY_EXCLUDES},
        },
        {
            "id": "no-raw-dict-domain-io",
            "languages": ["python"],
            "message": (
                "Raw 'dict' used as a function parameter/return type. Domain/"
                "service/workflow contracts must use a typed record from "
                "types.py, not a raw dictionary."
            ),
            "severity": "ERROR",
            "patterns": [
                {
                    "pattern-either": [
                        {"pattern": "def $F(...) -> dict: ..."},
                        {"pattern": "def $F(...) -> dict[...]: ..."},
                        {"pattern": "def $F($X: dict, ...): ..."},
                        {"pattern": "def $F($X: dict[...], ...): ..."},
                    ]
                }
            ],
            "paths": {"exclude": ["src/fediec/types.py"]},
        },
        {
            "id": "no-duplicate-yaml-parsing",
            "languages": ["python"],
            "message": (
                "yaml.safe_load called outside config.py. Only config.py may "
                "parse config.yaml (technical_doc.md Sec. 6.3)."
            ),
            "severity": "ERROR",
            "pattern": "yaml.safe_load(...)",
            "paths": {"exclude": ["src/fediec/config.py"]},
        },
        {
            "id": "no-broad-cast",
            "languages": ["python"],
            "message": (
                "typing.cast(...) used. Fix the underlying type instead of "
                "casting past it (technical_doc.md Sec. 9)."
            ),
            "severity": "ERROR",
            "pattern": "cast(...)",
        },
    ]
}
