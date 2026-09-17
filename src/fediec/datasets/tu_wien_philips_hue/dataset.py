from __future__ import annotations

import re
from datetime import datetime

from fediec.enums import (
    DatasetAvailability,
    DatasetSource,
    IntentProvenanceGrade,
    RawCaptureFileSuffix,
    SemanticAction,
    TuWienPolarityToken,
)
from fediec.paths import resolve_dataset_raw_root
from fediec.types import (
    DeviceId,
    InteractionId,
    PublicSourceInteraction,
    RepositoryPath,
    SourceCaptureId,
    SourceGroupId,
    WallClockTimestamp,
)

_TRIGGER_FILENAME_PATTERN = re.compile(
    r"^\d+_(?P<date>\d{8})_(?P<time>\d{6})_.*_Turn_(?P<polarity>On|Off)\.pcap$"
)

_POLARITY_TO_ACTION: dict[TuWienPolarityToken, SemanticAction] = {
    TuWienPolarityToken.ON: SemanticAction.TURN_ON,
    TuWienPolarityToken.OFF: SemanticAction.TURN_OFF,
}


def describe_raw_availability() -> DatasetAvailability:
    raw_root = resolve_dataset_raw_root(DatasetSource.TU_WIEN_PHILIPS_HUE)
    if not raw_root.exists() or not any(raw_root.iterdir()):
        return DatasetAvailability.MISSING_EXTERNAL
    return DatasetAvailability.PRESENT_AND_VALID


def enumerate_raw_interactions() -> tuple[PublicSourceInteraction, ...]:
    raw_root = resolve_dataset_raw_root(DatasetSource.TU_WIEN_PHILIPS_HUE)
    interactions: list[PublicSourceInteraction] = []
    for device_directory in sorted(p for p in raw_root.iterdir() if p.is_dir()):
        for capture_path in sorted(device_directory.glob(f"*{RawCaptureFileSuffix.PCAP}")):
            match = _TRIGGER_FILENAME_PATTERN.match(capture_path.name)
            if match is None:
                continue
            trigger_timestamp = datetime.strptime(
                f"{match['date']}_{match['time']}", "%Y%m%d_%H%M%S"
            )
            interactions.append(
                PublicSourceInteraction(
                    dataset_source=DatasetSource.TU_WIEN_PHILIPS_HUE,
                    interaction_id=InteractionId(capture_path.relative_to(raw_root).as_posix()),
                    device_id=DeviceId(device_directory.name),
                    source_capture_id=SourceCaptureId(capture_path.name),
                    source_group_id=SourceGroupId(device_directory.name),
                    semantic_action=_POLARITY_TO_ACTION[
                        TuWienPolarityToken(match["polarity"])
                    ],
                    trigger_timestamp=WallClockTimestamp(trigger_timestamp),
                    intent_provenance_grade=IntentProvenanceGrade.VERIFIED_DIRECT,
                    capture_path=RepositoryPath(capture_path),
                )
            )
    return tuple(interactions)
