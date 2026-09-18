from __future__ import annotations

import struct
from datetime import UTC, datetime
from pathlib import Path

from fediec.enums import (
    CicPolarityToken,
    CicTriggerMethod,
    DatasetAvailability,
    DatasetSource,
    IntentProvenanceGrade,
    RawCaptureFileSuffix,
    SemanticAction,
    SourceGroupKind,
    StructByteOrder,
)
from fediec.paths import resolve_cic_iot_2022_interactions_root, resolve_dataset_raw_root
from fediec.types import (
    DeviceId,
    InteractionId,
    PcapTimestampScale,
    PublicSourceInteraction,
    RepositoryPath,
    SourceCaptureId,
    SourceContextId,
    SourceGroupId,
    WallClockTimestamp,
)

_ELIGIBLE_TRIGGER_METHODS = frozenset(
    {CicTriggerMethod.LOCAL, CicTriggerMethod.LAN, CicTriggerMethod.WAN}
)

_POLARITY_TOKEN_TO_ACTION: dict[CicPolarityToken, SemanticAction] = {
    CicPolarityToken.ON: SemanticAction.TURN_ON,
    CicPolarityToken.OFF: SemanticAction.TURN_OFF,
}

_PCAP_MAGIC_TO_FORMAT: dict[bytes, tuple[StructByteOrder, PcapTimestampScale]] = {
    b"\xd4\xc3\xb2\xa1": (StructByteOrder.LITTLE, 1e-6),
    b"\xa1\xb2\xc3\xd4": (StructByteOrder.BIG, 1e-6),
    b"\x4d\x3c\xb2\xa1": (StructByteOrder.LITTLE, 1e-9),
    b"\xa1\xb2\x3c\x4d": (StructByteOrder.BIG, 1e-9),
}


def describe_raw_availability() -> DatasetAvailability:
    raw_root = resolve_dataset_raw_root(DatasetSource.CIC_IOT_2022)
    if not raw_root.exists() or not any(raw_root.iterdir()):
        return DatasetAvailability.MISSING_EXTERNAL
    return DatasetAvailability.PRESENT_AND_VALID


def read_pcap_first_packet_timestamp(capture_path: RepositoryPath) -> WallClockTimestamp:
    with Path(capture_path).open("rb") as handle:
        header = handle.read(24)
        if len(header) < 24:
            raise ValueError(f"{capture_path}: truncated pcap global header")
        magic = header[:4]
        if magic not in _PCAP_MAGIC_TO_FORMAT:
            raise ValueError(f"{capture_path}: unsupported capture format (magic {magic!r})")
        endianness, second_scale = _PCAP_MAGIC_TO_FORMAT[magic]
        record_header = handle.read(16)
        if len(record_header) < 16:
            raise ValueError(f"{capture_path}: pcap has no packet records")
        ts_sec, ts_fraction = struct.unpack(f"{endianness}II", record_header[:8])
        epoch_seconds = ts_sec + ts_fraction * second_scale
        return WallClockTimestamp(datetime.fromtimestamp(epoch_seconds, tz=UTC))


def _resolve_trigger_action(
    trigger_directory: Path,
) -> tuple[SemanticAction, SourceContextId] | None:
    prefix, _, polarity = trigger_directory.name.partition("_")
    try:
        trigger_method = CicTriggerMethod(f"{prefix}_")
    except ValueError:
        return None
    if trigger_method not in _ELIGIBLE_TRIGGER_METHODS:
        return None
    try:
        polarity_token = CicPolarityToken(polarity)
    except ValueError:
        return None
    return (
        _POLARITY_TOKEN_TO_ACTION[polarity_token],
        SourceContextId(prefix.removesuffix("_").lower()),
    )


def _interaction_for_capture(
    interactions_root: Path,
    device_directory: Path,
    capture_path: Path,
    semantic_action: SemanticAction,
    source_context_id: SourceContextId,
) -> PublicSourceInteraction:
    typed_capture_path = RepositoryPath(capture_path)
    relative_capture = capture_path.relative_to(interactions_root).as_posix()
    return PublicSourceInteraction(
        dataset_source=DatasetSource.CIC_IOT_2022,
        interaction_id=InteractionId(relative_capture),
        device_id=DeviceId(device_directory.name),
        source_capture_id=SourceCaptureId(relative_capture),
        source_group_id=SourceGroupId(relative_capture),
        source_group_kind=SourceGroupKind.INDIVIDUAL_CAPTURE,
        source_context_id=source_context_id,
        semantic_action=semantic_action,
        capture_start_timestamp=read_pcap_first_packet_timestamp(typed_capture_path),
        intent_provenance_grade=IntentProvenanceGrade.PARTIAL,
        capture_path=typed_capture_path,
    )


def _records_for_trigger_directory(
    interactions_root: Path, device_directory: Path, trigger_directory: Path
) -> tuple[PublicSourceInteraction, ...]:
    resolved = _resolve_trigger_action(trigger_directory)
    if resolved is None:
        return ()
    semantic_action, source_context_id = resolved
    return tuple(
        _interaction_for_capture(
            interactions_root, device_directory, capture_path, semantic_action, source_context_id
        )
        for capture_path in sorted(trigger_directory.glob(f"*{RawCaptureFileSuffix.PCAP}"))
    )


def _iter_device_trigger_directories(interactions_root: Path) -> tuple[tuple[Path, Path], ...]:
    return tuple(
        (device_directory, trigger_directory)
        for category_directory in sorted(p for p in interactions_root.iterdir() if p.is_dir())
        for device_directory in sorted(p for p in category_directory.iterdir() if p.is_dir())
        for trigger_directory in sorted(p for p in device_directory.iterdir() if p.is_dir())
    )


def enumerate_raw_interactions() -> tuple[PublicSourceInteraction, ...]:
    interactions_root = resolve_cic_iot_2022_interactions_root()
    return tuple(
        record
        for device_directory, trigger_directory in _iter_device_trigger_directories(
            interactions_root
        )
        for record in _records_for_trigger_directory(
            interactions_root, device_directory, trigger_directory
        )
    )
