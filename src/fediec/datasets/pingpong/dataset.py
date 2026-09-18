from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from fediec.enums import (
    DatasetAvailability,
    DatasetSource,
    IntentProvenanceGrade,
    NetworkCaptureSubdirectory,
    PingPongEligibleDevice,
    PingPongEvaluationSubtree,
    RawCaptureFileSuffix,
    SemanticAction,
    SourceGroupKind,
    SourceTimeZone,
)
from fediec.paths import resolve_dataset_raw_root, resolve_pingpong_evaluation_root
from fediec.types import (
    DeviceId,
    DirectoryName,
    InteractionId,
    PublicSourceInteraction,
    RepositoryPath,
    SourceCaptureId,
    SourceContextId,
    SourceGroupId,
    WallClockTimestamp,
)

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


def parse_source_timestamps_file(path: Path) -> list[datetime]:
    timestamps: list[datetime] = []
    try:
        raw_text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw_text = path.read_text(encoding="latin-1")
    for line in raw_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        local_timestamp = datetime.strptime(stripped, "%m/%d/%Y %I:%M:%S %p")
        timestamps.append(
            local_timestamp.replace(tzinfo=ZoneInfo(SourceTimeZone.AMERICA_LOS_ANGELES)).astimezone(
                UTC
            )
        )
    return timestamps


def _resolve_capture_unit_device_id(capture_unit_directory: Path) -> DeviceId | None:
    name = DirectoryName(capture_unit_directory.name)
    if name.endswith(_ONOFF_SUFFIX):
        return DeviceId(name[: -len(_ONOFF_SUFFIX)])
    try:
        PingPongEligibleDevice(name)
    except ValueError:
        return None
    return DeviceId(name)


def _iter_capture_unit_directories(capture_context_root: Path) -> tuple[Path, ...]:
    return tuple(
        candidate.parent
        for candidate in sorted(
            capture_context_root.rglob(NetworkCaptureSubdirectory.TIMESTAMPS)
        )
        if candidate.is_dir()
    )


def _capture_units_in_context(
    capture_context_root: Path,
) -> tuple[tuple[DeviceId, SourceContextId, Path], ...]:
    source_context_id = SourceContextId(capture_context_root.name)
    units: list[tuple[DeviceId, SourceContextId, Path]] = []
    for capture_unit_directory in _iter_capture_unit_directories(capture_context_root):
        device_id = _resolve_capture_unit_device_id(capture_unit_directory)
        if device_id is None:
            continue
        units.append((device_id, source_context_id, capture_unit_directory))
    return tuple(units)


def _iter_capture_context_roots() -> tuple[Path, ...]:
    roots: list[Path] = []
    for subtree in _ELIGIBLE_EVALUATION_SUBTREES:
        subtree_root = resolve_pingpong_evaluation_root() / subtree
        if not subtree_root.exists():
            continue
        roots.extend(sorted(p for p in subtree_root.iterdir() if p.is_dir()))
    return tuple(roots)


def _enumerate_capture_units() -> tuple[tuple[DeviceId, SourceContextId, Path], ...]:
    return tuple(
        unit
        for capture_context_root in _iter_capture_context_roots()
        for unit in _capture_units_in_context(capture_context_root)
    )


def enumerate_raw_interactions() -> tuple[PublicSourceInteraction, ...]:
    raw_root = resolve_dataset_raw_root(DatasetSource.PINGPONG)
    interactions: list[PublicSourceInteraction] = []
    for device_id, source_context_id, capture_unit_directory in _enumerate_capture_units():
        timestamp_files = sorted(
            path
            for path in (capture_unit_directory / NetworkCaptureSubdirectory.TIMESTAMPS).glob(
                f"*{RawCaptureFileSuffix.TIMESTAMPS}"
            )
            if not path.name.startswith("._")
        )
        if not timestamp_files:
            continue
        capture_path = _resolve_capture_path(capture_unit_directory)
        if capture_path is None:
            continue
        for timestamp_file in timestamp_files:
            for index, trigger_timestamp in enumerate(parse_source_timestamps_file(timestamp_file)):
                is_on = (index % 2 == 0) == _FIRST_TRIGGER_IS_ON
                interactions.append(
                    PublicSourceInteraction(
                        dataset_source=DatasetSource.PINGPONG,
                        interaction_id=InteractionId(
                            f"{capture_unit_directory.relative_to(raw_root).as_posix()}:{index}"
                        ),
                        device_id=device_id,
                        source_capture_id=SourceCaptureId(
                            capture_path.relative_to(raw_root).as_posix()
                        ),
                        source_group_id=SourceGroupId(
                            capture_path.relative_to(raw_root).as_posix()
                        ),
                        source_group_kind=SourceGroupKind.CONTINUOUS_CAPTURE,
                        source_context_id=source_context_id,
                        semantic_action=(
                            SemanticAction.TURN_ON if is_on else SemanticAction.TURN_OFF
                        ),
                        capture_start_timestamp=None,
                        trigger_timestamp=WallClockTimestamp(trigger_timestamp),
                        intent_provenance_grade=IntentProvenanceGrade.VERIFIED_PROTOCOL,
                        capture_path=capture_path,
                    )
                )
    return tuple(interactions)
