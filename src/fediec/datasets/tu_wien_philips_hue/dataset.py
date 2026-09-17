from __future__ import annotations

import re
from datetime import datetime

from fediec.enums import (
    DatasetAvailability,
    DatasetSource,
    RawCaptureFileSuffix,
    SemanticAction,
    TuWienPolarityToken,
)
from fediec.paths import resolve_dataset_raw_root
from fediec.types import DeviceId, DomainRecord, RepositoryPath, WallClockTimestamp

_TRIGGER_FILENAME_PATTERN = re.compile(
    r"^\d+_(?P<date>\d{8})_(?P<time>\d{6})_.*_Turn_(?P<polarity>On|Off)\.pcap$"
)

_POLARITY_TO_ACTION: dict[TuWienPolarityToken, SemanticAction] = {
    TuWienPolarityToken.ON: SemanticAction.TURN_ON,
    TuWienPolarityToken.OFF: SemanticAction.TURN_OFF,
}


class RawTriggerInteraction(DomainRecord):
    device_id: DeviceId
    semantic_action: SemanticAction
    trigger_timestamp: WallClockTimestamp
    capture_path: RepositoryPath


def describe_raw_availability() -> DatasetAvailability:
    raw_root = resolve_dataset_raw_root(DatasetSource.TU_WIEN_PHILIPS_HUE)
    if not raw_root.exists() or not any(raw_root.iterdir()):
        return DatasetAvailability.MISSING_EXTERNAL
    return DatasetAvailability.PRESENT_AND_VALID


def enumerate_raw_interactions() -> tuple[RawTriggerInteraction, ...]:
    raw_root = resolve_dataset_raw_root(DatasetSource.TU_WIEN_PHILIPS_HUE)
    interactions: list[RawTriggerInteraction] = []
    for device_directory in sorted(p for p in raw_root.iterdir() if p.is_dir()):
        for capture_path in sorted(device_directory.glob(f"*{RawCaptureFileSuffix.PCAP}")):
            match = _TRIGGER_FILENAME_PATTERN.match(capture_path.name)
            if match is None:
                continue
            trigger_timestamp = datetime.strptime(
                f"{match['date']}_{match['time']}", "%Y%m%d_%H%M%S"
            )
            interactions.append(
                RawTriggerInteraction(
                    device_id=DeviceId(device_directory.name),
                    semantic_action=_POLARITY_TO_ACTION[
                        TuWienPolarityToken(match["polarity"])
                    ],
                    trigger_timestamp=WallClockTimestamp(trigger_timestamp),
                    capture_path=RepositoryPath(capture_path),
                )
            )
    return tuple(interactions)
