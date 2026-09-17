from __future__ import annotations

import struct
from datetime import UTC, datetime
from pathlib import Path

from fediec.enums import DatasetAvailability, DatasetSource, SemanticAction
from fediec.paths import resolve_dataset_raw_root
from fediec.types import DeviceId, DomainRecord, RepositoryPath, WallClockTimestamp

# Verified against real files under
# data/raw/cic-iot-2022/3-Interactions/<category>/<device>/: each device
# directory has trigger-method subfolders. LOCAL_/LAN_/WAN_ prefixes are
# official-companion-app triggers (Roadmap Sec. 16 intent-provenance
# requirement); ALEXA_/GOOGLE_ are voice-assistant triggers and are
# excluded — a voice command is not an official Android companion-app
# interaction.
_ELIGIBLE_TRIGGER_METHOD_PREFIXES: tuple[str, ...] = ("LOCAL_", "LAN_", "WAN_")

_POLARITY_SUFFIX_TO_ACTION: dict[str, SemanticAction] = {
    "ON": SemanticAction.TURN_ON,
    "OFF": SemanticAction.TURN_OFF,
}

# Classic (non-pcapng) libpcap global-header magic numbers: little/big
# endian, microsecond/nanosecond resolution. pcapng is not present in this
# dataset (verified via `file` on real captures) and is intentionally
# unsupported here rather than guessed at.
_PCAP_MAGIC_TO_FORMAT: dict[bytes, tuple[str, float]] = {
    b"\xd4\xc3\xb2\xa1": ("<", 1e-6),
    b"\xa1\xb2\xc3\xd4": (">", 1e-6),
    b"\x4d\x3c\xb2\xa1": ("<", 1e-9),
    b"\xa1\xb2\x3c\x4d": (">", 1e-9),
}


class RawTriggerInteraction(DomainRecord):
    device_id: DeviceId
    semantic_action: SemanticAction
    trigger_timestamp: WallClockTimestamp
    capture_path: RepositoryPath


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


def enumerate_raw_interactions() -> tuple[RawTriggerInteraction, ...]:
    raw_root = resolve_dataset_raw_root(DatasetSource.CIC_IOT_2022)
    interactions_root = Path(raw_root) / "3-Interactions"
    interactions: list[RawTriggerInteraction] = []
    for category_directory in sorted(p for p in interactions_root.iterdir() if p.is_dir()):
        for device_directory in sorted(p for p in category_directory.iterdir() if p.is_dir()):
            for trigger_directory in sorted(
                p for p in device_directory.iterdir() if p.is_dir()
            ):
                prefix, _, polarity = trigger_directory.name.partition("_")
                trigger_method = f"{prefix}_"
                if trigger_method not in _ELIGIBLE_TRIGGER_METHOD_PREFIXES:
                    continue
                semantic_action = _POLARITY_SUFFIX_TO_ACTION.get(polarity)
                if semantic_action is None:
                    continue
                for capture_path in sorted(trigger_directory.glob("*.pcap")):
                    typed_capture_path = RepositoryPath(capture_path)
                    interactions.append(
                        RawTriggerInteraction(
                            device_id=DeviceId(device_directory.name),
                            semantic_action=semantic_action,
                            trigger_timestamp=read_pcap_first_packet_timestamp(
                                typed_capture_path
                            ),
                            capture_path=typed_capture_path,
                        )
                    )
    return tuple(interactions)
