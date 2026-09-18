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
    PublicSourceInteraction,
    RepositoryPath,
    SampleCount,
)


class ArtifactProvenance(DomainRecord):
    config_hash: ConfigHash
    git_commit: GitCommit
    created_at: datetime


class PreprocessProvenance(ArtifactProvenance):
    source_capture_count: SampleCount
    selected_input_digest: ArtifactChecksum


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


def build_preprocess_provenance(
    config_text: ConfigText,
    interactions: tuple[PublicSourceInteraction, ...],
) -> PreprocessProvenance:
    digest = hashlib.sha256()
    for interaction in sorted(interactions, key=lambda item: item.source_capture_id):
        checksum = compute_file_checksum(interaction.capture_path)
        digest.update(str(interaction.source_capture_id).encode("utf-8"))
        digest.update(checksum.encode("utf-8"))
    current = build_current_provenance(config_text)
    return PreprocessProvenance(
        config_hash=current.config_hash,
        git_commit=current.git_commit,
        created_at=current.created_at,
        source_capture_count=len(interactions),
        selected_input_digest=ArtifactChecksum(digest.hexdigest()),
    )


def write_json_manifest(path: RepositoryPath, manifest: DomainRecord) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(manifest.model_dump(mode="json"), indent=2, sort_keys=True),
        encoding="utf-8",
    )
