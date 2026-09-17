from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from fediec.types import (
    ArtifactChecksum,
    ConfigHash,
    ConfigText,
    DomainRecord,
    GitCommit,
    RepositoryPath,
)


class ArtifactProvenance(DomainRecord):
    config_hash: ConfigHash
    git_commit: GitCommit
    created_at: datetime


def compute_file_checksum(path: RepositoryPath) -> ArtifactChecksum:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return ArtifactChecksum(digest.hexdigest())


def compute_config_hash(config_text: ConfigText) -> ConfigHash:
    return ConfigHash(hashlib.sha256(config_text.encode("utf-8")).hexdigest())


def resolve_git_commit() -> GitCommit:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return GitCommit(completed.stdout.strip())


def build_current_provenance(config_text: ConfigText) -> ArtifactProvenance:
    return ArtifactProvenance(
        config_hash=compute_config_hash(config_text),
        git_commit=resolve_git_commit(),
        created_at=datetime.now(UTC),
    )


def write_json_manifest(path: RepositoryPath, manifest: DomainRecord) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(manifest.model_dump(mode="json"), indent=2, sort_keys=True),
        encoding="utf-8",
    )
