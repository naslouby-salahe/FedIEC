from __future__ import annotations

import shutil
from pathlib import Path

from fediec.types import RepositoryPath


def promote_finalized_artifact(
    source_path: RepositoryPath, destination_path: RepositoryPath
) -> None:
    source = Path(source_path)
    if not source.is_file():
        raise ValueError(f"promotion source is not a file: {source}")
    destination = Path(destination_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
