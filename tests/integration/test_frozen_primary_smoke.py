from __future__ import annotations

from fediec.workflows.smoke import run_smoke


def test_frozen_primary_artifact_matches_current_public_source_contract() -> None:
    run_smoke()
