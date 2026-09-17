from __future__ import annotations

from datetime import datetime
from pathlib import Path

from fediec.enums import DatasetAvailability, DatasetSource, SemanticAction
from fediec.paths import resolve_dataset_raw_root
from fediec.types import (
    DeviceId,
    DirectoryName,
    DomainRecord,
    RepositoryPath,
    WallClockTimestamp,
)

# ON/OFF polarity is not stored per-line in PingPong's raw .timestamps
# files. It is recovered from PingPong's own official tool source
# (github.com/uci-plrg/pingpong, SignatureGenerator.java lines 123-126):
#
#   // Tag each trigger with "ON" or "OFF", assuming that the first
#   // trigger is an "ON" and that they alternate.
#   userActions.add(new UserAction(
#       i % 2 == 0 ? Type.TOGGLE_ON : Type.TOGGLE_OFF, triggerTimes.get(i)));
#
# and the class-level doc comment: "The events ON and OFF were generated
# alternately for 100 times using the automation scripts." This is the
# verified ground-truth convention the dataset was collected under, not a
# heuristic guess.
_FIRST_TRIGGER_IS_ON = True

# Verified against real directory names under
# data/raw/PingPong/evaluation-datasets/{local-phone,same-vendor}/. Only
# capture-unit directories with genuine binary ON/OFF semantics are
# included (Roadmap Sec. 4 scope: TURN_ON/TURN_OFF only). Directories such
# as *-intensity, *-color, *-mode, *-quickrun, *-photo, *-watch, and
# ambiguous single-purpose devices without an explicit "-onoff" marker
# (ring-alarm, kwikset-doorlock, nest-thermostat, roomba-vacuum-robot,
# dlink-siren, arlo-camera, ecobee-thermostat-*, blossom-sprinkler-*,
# rachio-sprinkler-*) are deliberately excluded rather than guessed at.
_ELIGIBLE_BARE_DEVICE_DIRECTORIES: frozenset[DirectoryName] = frozenset(
    DirectoryName(name)
    for name in (
        "amazon-plug",
        "dlink-plug",
        "st-plug",
        "tplink-plug",
        "tplink-power-strip",
        "tplink-two-outlet-plug",
        "wemo-insight-plug",
        "wemo-plug",
    )
)
_ONOFF_SUFFIX = "-onoff"

# remote-phone/, ifttt/, and public-dataset/ collections are not yet
# included: their intent-provenance chain (Roadmap Sec. 16 "official
# Android companion application") needs separate verification before
# eligibility (ifttt is a third-party automation service, and
# public-dataset's original trigger mechanism is documented by the IMC'19
# paper, not by PingPong itself).
_ELIGIBLE_EVALUATION_SUBTREES: tuple[DirectoryName, ...] = (
    DirectoryName("local-phone"),
    DirectoryName("same-vendor"),
)

_CAPTURE_DIRECTORY_PRIORITY: tuple[DirectoryName, ...] = (
    DirectoryName("wlan1"),
    DirectoryName("wlan"),
    DirectoryName("eth0"),
    DirectoryName("eth1"),
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
    # macOS AppleDouble sidecar files ("._name.pcap") are not real data;
    # verified present in this checkout, excluded here.
    return sorted(path for path in directory.glob("*.pcap") if not path.name.startswith("._"))


def _resolve_capture_path(capture_unit_directory: Path) -> RepositoryPath | None:
    for vantage_point in _CAPTURE_DIRECTORY_PRIORITY:
        candidates = _real_pcap_files(capture_unit_directory / vantage_point)
        if candidates:
            return RepositoryPath(candidates[0])
    for child in sorted(capture_unit_directory.iterdir()):
        if child.is_dir() and child.name != "timestamps":
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


def _enumerate_capture_units(raw_root: Path) -> list[tuple[DeviceId, Path]]:
    units: list[tuple[DeviceId, Path]] = []
    for subtree in _ELIGIBLE_EVALUATION_SUBTREES:
        subtree_root = raw_root / "evaluation-datasets" / subtree
        if not subtree_root.exists():
            continue
        for capture_context_root in sorted(p for p in subtree_root.iterdir() if p.is_dir()):
            for candidate in sorted(capture_context_root.rglob("timestamps")):
                if not candidate.is_dir():
                    continue
                capture_unit_directory = candidate.parent
                name = DirectoryName(capture_unit_directory.name)
                if name.endswith(_ONOFF_SUFFIX):
                    device_base = name[: -len(_ONOFF_SUFFIX)]
                elif name in _ELIGIBLE_BARE_DEVICE_DIRECTORIES:
                    device_base = name
                else:
                    continue
                device_id = DeviceId(f"{device_base}__{capture_context_root.name}")
                units.append((device_id, capture_unit_directory))
    return units


def enumerate_raw_interactions() -> tuple[RawTriggerInteraction, ...]:
    raw_root = Path(resolve_dataset_raw_root(DatasetSource.PINGPONG))
    interactions: list[RawTriggerInteraction] = []
    for device_id, capture_unit_directory in _enumerate_capture_units(raw_root):
        # macOS AppleDouble sidecar files ("._name.timestamps") are not
        # real data; verified present in this checkout, excluded here.
        timestamp_files = sorted(
            path
            for path in (capture_unit_directory / "timestamps").glob("*.timestamps")
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
