from __future__ import annotations

from datetime import datetime
from pathlib import Path

from fediec.enums import (
    DatasetAvailability,
    DatasetSource,
    NetworkCaptureSubdirectory,
    PingPongEligibleDevice,
    PingPongEvaluationSubtree,
    RawCaptureFileSuffix,
    SemanticAction,
)
from fediec.paths import resolve_dataset_raw_root, resolve_pingpong_evaluation_root
from fediec.types import DeviceId, DirectoryName, DomainRecord, RepositoryPath, WallClockTimestamp

_FIRST_TRIGGER_IS_ON = True

_ONOFF_SUFFIX = "-onoff"

_ELIGIBLE_EVALUATION_SUBTREES = (
    PingPongEvaluationSubtree.LOCAL_PHONE,
    PingPongEvaluationSubtree.SAME_VENDOR,
)

_CAPTURE_DIRECTORY_PRIORITY = (
    NetworkCaptureSubdirectory.WLAN1,
    NetworkCaptureSubdirectory.WLAN,
    NetworkCaptureSubdirectory.ETH0,
    NetworkCaptureSubdirectory.ETH1,
)


class RawTriggerInteraction(DomainRecord):
    device_id: DeviceId
    semantic_action: SemanticAction
    trigger_timestamp: WallClockTimestamp
    capture_path: RepositoryPath


def describe_raw_availability() -> DatasetAvailability:
    raw_root = resolve_dataset_raw_root(DatasetSource.PINGPONG)
    if not raw_root.exists() or not any(raw_root.iterdir()):
        return DatasetAvailability.MISSING_EXTERNAL
    return DatasetAvailability.PRESENT_AND_VALID


def _real_pcap_files(directory: Path) -> list[Path]:
    return sorted(
        path
        for path in directory.glob(f"*{RawCaptureFileSuffix.PCAP}")
        if not path.name.startswith("._")
    )


def _resolve_capture_path(capture_unit_directory: Path) -> RepositoryPath | None:
    for vantage_point in _CAPTURE_DIRECTORY_PRIORITY:
        candidates = _real_pcap_files(capture_unit_directory / vantage_point)
        if candidates:
            return RepositoryPath(candidates[0])
    for child in sorted(capture_unit_directory.iterdir()):
        if child.is_dir() and child.name != NetworkCaptureSubdirectory.TIMESTAMPS:
            candidates = _real_pcap_files(child)
            if candidates:
                return RepositoryPath(candidates[0])
    return None


def _parse_timestamps_file(path: Path) -> list[datetime]:
    timestamps: list[datetime] = []
    try:
        raw_text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw_text = path.read_text(encoding="latin-1")
    for line in raw_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        timestamps.append(datetime.strptime(stripped, "%m/%d/%Y %I:%M:%S %p"))
    return timestamps


def _enumerate_capture_units() -> list[tuple[DeviceId, Path]]:
    units: list[tuple[DeviceId, Path]] = []
    for subtree in _ELIGIBLE_EVALUATION_SUBTREES:
        subtree_root = resolve_pingpong_evaluation_root() / subtree
        if not subtree_root.exists():
            continue
        for capture_context_root in sorted(p for p in subtree_root.iterdir() if p.is_dir()):
            for candidate in sorted(
                capture_context_root.rglob(NetworkCaptureSubdirectory.TIMESTAMPS)
            ):
                if not candidate.is_dir():
                    continue
                capture_unit_directory = candidate.parent
                name = DirectoryName(capture_unit_directory.name)
                if name.endswith(_ONOFF_SUFFIX):
                    device_base = name[: -len(_ONOFF_SUFFIX)]
                else:
                    try:
                        PingPongEligibleDevice(name)
                    except ValueError:
                        continue
                    device_base = name
                device_id = DeviceId(f"{device_base}__{capture_context_root.name}")
                units.append((device_id, capture_unit_directory))
    return units


def enumerate_raw_interactions() -> tuple[RawTriggerInteraction, ...]:
    interactions: list[RawTriggerInteraction] = []
    for device_id, capture_unit_directory in _enumerate_capture_units():
        timestamp_files = sorted(
            path
            for path in (
                capture_unit_directory / NetworkCaptureSubdirectory.TIMESTAMPS
            ).glob(f"*{RawCaptureFileSuffix.TIMESTAMPS}")
            if not path.name.startswith("._")
        )
        if not timestamp_files:
            continue
        capture_path = _resolve_capture_path(capture_unit_directory)
        if capture_path is None:
            continue
        for timestamp_file in timestamp_files:
            for index, trigger_timestamp in enumerate(_parse_timestamps_file(timestamp_file)):
                is_on = (index % 2 == 0) == _FIRST_TRIGGER_IS_ON
                interactions.append(
                    RawTriggerInteraction(
                        device_id=device_id,
                        semantic_action=(
                            SemanticAction.TURN_ON if is_on else SemanticAction.TURN_OFF
                        ),
                        trigger_timestamp=WallClockTimestamp(trigger_timestamp),
                        capture_path=capture_path,
                    )
                )
    return tuple(interactions)
