from __future__ import annotations

import struct
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from itertools import pairwise
from pathlib import Path
from typing import BinaryIO

from fediec.enums import NetworkExecutionFeature, RepresentationConfoundAxis, StructByteOrder
from fediec.types import (
    FIRST_PACKET_INDEX,
    LAST_PACKET_INDEX,
    MEDIAN_QUANTILE,
    NEAR_CONSTANT_VARIANCE_THRESHOLD,
    P95_QUANTILE,
    TOTAL_BYTE_COUNT_FEATURE_INDEX,
    TOTAL_PACKET_COUNT_FEATURE_INDEX,
    ZERO_BYTE_COUNT,
    ZERO_FEATURE_VALUE,
    ZERO_PACKET_COUNT,
    ByteCount,
    CheckDetail,
    Duration,
    FeatureIndex,
    FeatureValue,
    FeatureVariance,
    FeatureVectors,
    InteractionFeatureVector,
    InteractionId,
    MonotonicTimestamp,
    NetworkFeatureName,
    PacketCount,
    PcapTimestampScale,
    PublicSourceInteraction,
    RemoteTransportPortCount,
    RepresentationConfoundAudit,
    RepresentationStratifiedVariation,
    TargetDeviceMac,
)

_PCAP_FORMATS: dict[bytes, tuple[StructByteOrder, PcapTimestampScale]] = {
    b"\xd4\xc3\xb2\xa1": (StructByteOrder.LITTLE, 1e-6),
    b"\xa1\xb2\xc3\xd4": (StructByteOrder.BIG, 1e-6),
    b"\x4d\x3c\xb2\xa1": (StructByteOrder.LITTLE, 1e-9),
    b"\xa1\xb2\x3c\x4d": (StructByteOrder.BIG, 1e-9),
}


def _mac_text(value: bytes) -> TargetDeviceMac:
    return TargetDeviceMac(":".join(f"{part:x}" for part in value))


def _mean(values: tuple[FeatureValue, ...]) -> FeatureValue:
    return sum(values) / len(values) if values else ZERO_FEATURE_VALUE


def _standard_deviation(values: tuple[FeatureValue, ...]) -> FeatureValue:
    if len(values) < 2:
        return ZERO_FEATURE_VALUE
    mean = _mean(values)
    return (sum((value - mean) ** 2 for value in values) / len(values)) ** 0.5


def _quantile(values: tuple[FeatureValue, ...], quantile: FeatureValue) -> FeatureValue:
    if not values:
        return ZERO_FEATURE_VALUE
    ordered = sorted(values)
    index = round((len(ordered) - 1) * quantile)
    return ordered[index]


@dataclass
class _PacketAccumulator:
    timestamps: list[MonotonicTimestamp]
    outbound_sizes: list[FeatureValue]
    inbound_sizes: list[FeatureValue]
    remote_endpoints: set[bytes]
    remote_ports: set[RemoteTransportPortCount]
    tcp_count: PacketCount
    udp_count: PacketCount
    total_bytes: ByteCount


def _new_packet_accumulator() -> _PacketAccumulator:
    return _PacketAccumulator(
        timestamps=[],
        outbound_sizes=[],
        inbound_sizes=[],
        remote_endpoints=set(),
        remote_ports=set(),
        tcp_count=ZERO_PACKET_COUNT,
        udp_count=ZERO_PACKET_COUNT,
        total_bytes=ZERO_BYTE_COUNT,
    )


def _read_pcap_global_header(
    handle: BinaryIO, interaction_id: InteractionId
) -> tuple[StructByteOrder, PcapTimestampScale]:
    global_header = handle.read(24)
    if len(global_header) != 24 or global_header[:4] not in _PCAP_FORMATS:
        raise ValueError(f"{interaction_id}: unsupported classic PCAP")
    return _PCAP_FORMATS[global_header[:4]]


def _iter_pcap_records(
    handle: BinaryIO,
    byte_order: StructByteOrder,
    scale: PcapTimestampScale,
    interaction_id: InteractionId,
) -> Iterator[tuple[MonotonicTimestamp, bytes]]:
    while record_header := handle.read(16):
        if len(record_header) != 16:
            raise ValueError(f"{interaction_id}: truncated PCAP record header")
        seconds, fraction, captured_length, _ = struct.unpack(f"{byte_order}IIII", record_header)
        frame = handle.read(captured_length)
        if len(frame) != captured_length:
            raise ValueError(f"{interaction_id}: truncated PCAP frame")
        yield seconds + fraction * scale, frame


def _process_ip_packet(accumulator: _PacketAccumulator, frame: bytes, outbound: bool) -> None:
    ip_start = 14
    ihl = (frame[ip_start] & 0x0F) * 4
    if ihl < 20 or len(frame) < ip_start + ihl:
        return
    protocol = frame[ip_start + 9]
    source_ip = frame[ip_start + 12 : ip_start + 16]
    destination_ip = frame[ip_start + 16 : ip_start + 20]
    accumulator.remote_endpoints.add(destination_ip if outbound else source_ip)
    if protocol == 6:
        accumulator.tcp_count += 1
    if protocol == 17:
        accumulator.udp_count += 1
    transport_start = ip_start + ihl
    if protocol in {6, 17} and len(frame) >= transport_start + 4:
        source_port, destination_port = struct.unpack(
            "!HH", frame[transport_start : transport_start + 4]
        )
        accumulator.remote_ports.add(destination_port if outbound else source_port)


def _process_packet(
    accumulator: _PacketAccumulator,
    frame: bytes,
    timestamp: MonotonicTimestamp,
    target_device_mac: TargetDeviceMac,
) -> None:
    if len(frame) < 14:
        return
    destination, source, ethertype = frame[:6], frame[6:12], frame[12:14]
    if _mac_text(source) != target_device_mac and _mac_text(destination) != target_device_mac:
        return
    accumulator.timestamps.append(timestamp)
    accumulator.total_bytes += len(frame)
    outbound = _mac_text(source) == target_device_mac
    (accumulator.outbound_sizes if outbound else accumulator.inbound_sizes).append(len(frame))
    if ethertype != b"\x08\x00" or len(frame) < 34:
        return
    _process_ip_packet(accumulator, frame, outbound)


def _build_feature_vector(accumulator: _PacketAccumulator) -> InteractionFeatureVector:
    packet_count = len(accumulator.timestamps)
    inter_arrival = tuple(
        later - earlier for earlier, later in pairwise(accumulator.timestamps)
    )
    duration = (
        accumulator.timestamps[LAST_PACKET_INDEX] - accumulator.timestamps[FIRST_PACKET_INDEX]
        if accumulator.timestamps
        else ZERO_FEATURE_VALUE
    )
    return InteractionFeatureVector(
        values=(
            packet_count,
            len(accumulator.outbound_sizes),
            len(accumulator.inbound_sizes),
            accumulator.total_bytes,
            sum(accumulator.outbound_sizes),
            sum(accumulator.inbound_sizes),
            _mean(tuple(accumulator.outbound_sizes)),
            _standard_deviation(tuple(accumulator.outbound_sizes)),
            _mean(tuple(accumulator.inbound_sizes)),
            _standard_deviation(tuple(accumulator.inbound_sizes)),
            _mean(inter_arrival),
            _standard_deviation(inter_arrival),
            _quantile(inter_arrival, MEDIAN_QUANTILE),
            _quantile(inter_arrival, P95_QUANTILE),
            accumulator.tcp_count / packet_count if packet_count else ZERO_FEATURE_VALUE,
            accumulator.udp_count / packet_count if packet_count else ZERO_FEATURE_VALUE,
            len(accumulator.remote_endpoints),
            len(accumulator.remote_ports),
            duration,
        )
    )


def extract_interaction_features(
    interaction: PublicSourceInteraction,
) -> InteractionFeatureVector:
    if interaction.target_device_mac is None:
        raise ValueError(f"{interaction.interaction_id}: target device MAC is unavailable")
    accumulator = _new_packet_accumulator()
    with Path(interaction.capture_path).open("rb") as handle:
        byte_order, scale = _read_pcap_global_header(handle, interaction.interaction_id)
        for timestamp, frame in _iter_pcap_records(
            handle, byte_order, scale, interaction.interaction_id
        ):
            _process_packet(accumulator, frame, timestamp, interaction.target_device_mac)
    return _build_feature_vector(accumulator)


def interaction_feature_order() -> tuple[NetworkExecutionFeature, ...]:
    return tuple(NetworkExecutionFeature)


def constant_feature_indices(vectors: FeatureVectors) -> tuple[FeatureIndex, ...]:
    if not vectors:
        raise ValueError("representation-confound audit requires at least one interaction vector")
    return tuple(
        index
        for index in range(len(NetworkExecutionFeature))
        if len({vector.values[index] for vector in vectors}) == 1
    )


def require_nonconstant_representation(vectors: FeatureVectors) -> None:
    if constant_indices := constant_feature_indices(vectors):
        features = tuple(NetworkExecutionFeature)
        names = tuple(NetworkFeatureName(features[index]) for index in constant_indices)
        raise ValueError(f"representation-confound gate failed: constant features {names}")


def _variance(values: tuple[FeatureValue, ...]) -> FeatureVariance:
    if len(values) < 2:
        return ZERO_FEATURE_VALUE
    mean = _mean(values)
    return sum((value - mean) ** 2 for value in values) / len(values)


def _capture_duration_seconds(interaction: PublicSourceInteraction) -> Duration:
    with Path(interaction.capture_path).open("rb") as handle:
        global_header = handle.read(24)
        if len(global_header) != 24 or global_header[:4] not in _PCAP_FORMATS:
            raise ValueError(f"{interaction.interaction_id}: unsupported classic PCAP")
        byte_order, scale = _PCAP_FORMATS[global_header[:4]]
        first_timestamp: MonotonicTimestamp | None = None
        last_timestamp: MonotonicTimestamp | None = None
        while record_header := handle.read(16):
            if len(record_header) != 16:
                raise ValueError(f"{interaction.interaction_id}: truncated PCAP record header")
            seconds, fraction, captured_length, _ = struct.unpack(
                f"{byte_order}IIII", record_header
            )
            if len(handle.read(captured_length)) != captured_length:
                raise ValueError(f"{interaction.interaction_id}: truncated PCAP frame")
            timestamp = seconds + fraction * scale
            first_timestamp = timestamp if first_timestamp is None else first_timestamp
            last_timestamp = timestamp
    return (
        last_timestamp - first_timestamp
        if first_timestamp is not None and last_timestamp
        else ZERO_FEATURE_VALUE
    )


def _stratified_variation(
    axis: RepresentationConfoundAxis,
    labels: tuple[CheckDetail, ...],
    vectors: FeatureVectors,
) -> RepresentationStratifiedVariation:
    grouped: defaultdict[CheckDetail, list[InteractionFeatureVector]] = defaultdict(list)
    for label, vector in zip(labels, vectors, strict=True):
        grouped[label].append(vector)
    constant_by_stratum = tuple(
        constant_feature_indices(tuple(group)) for group in grouped.values()
    )
    universally_constant = tuple(
        NetworkFeatureName(tuple(NetworkExecutionFeature)[index])
        for index in range(len(NetworkExecutionFeature))
        if constant_by_stratum and all(index in constants for constants in constant_by_stratum)
    )
    return RepresentationStratifiedVariation(
        axis=axis,
        stratum_count=len(grouped),
        strata_with_constant_features=sum(bool(item) for item in constant_by_stratum),
        universally_constant_features=universally_constant,
    )


def audit_representation(
    interactions: tuple[PublicSourceInteraction, ...],
    vectors: FeatureVectors,
) -> RepresentationConfoundAudit:
    if not interactions or len(interactions) != len(vectors):
        raise ValueError("representation-confound audit requires matched interactions and vectors")
    feature_order = interaction_feature_order()
    variances = tuple(
        _variance(tuple(vector.values[index] for vector in vectors))
        for index in range(len(NetworkExecutionFeature))
    )
    constant = tuple(
        NetworkFeatureName(feature_order[index])
        for index, variance in enumerate(variances)
        if variance == ZERO_FEATURE_VALUE
    )
    near_constant = tuple(
        NetworkFeatureName(feature_order[index])
        for index, variance in enumerate(variances)
        if ZERO_FEATURE_VALUE < variance <= NEAR_CONSTANT_VARIANCE_THRESHOLD
    )
    capture_durations = tuple(_capture_duration_seconds(item) for item in interactions)
    timestamps = tuple(item.capture_start_timestamp for item in interactions)
    contexts = tuple(sorted({item.source_context_id for item in interactions}))
    sources = tuple(sorted({item.dataset_source for item in interactions}))
    chronology = tuple(
        CheckDetail(timestamp.date().isoformat())
        if isinstance(timestamp, datetime)
        else CheckDetail("unknown")
        for timestamp in timestamps
    )
    stratified_variation = (
        _stratified_variation(
            RepresentationConfoundAxis.DATASET,
            tuple(CheckDetail(item.dataset_source) for item in interactions),
            vectors,
        ),
        _stratified_variation(
            RepresentationConfoundAxis.PHYSICAL_DEVICE,
            tuple(CheckDetail(item.device_id) for item in interactions),
            vectors,
        ),
        _stratified_variation(
            RepresentationConfoundAxis.SOURCE_CONTEXT,
            tuple(CheckDetail(item.source_context_id) for item in interactions),
            vectors,
        ),
        _stratified_variation(
            RepresentationConfoundAxis.SOURCE_CHRONOLOGY, chronology, vectors
        ),
        _stratified_variation(
            RepresentationConfoundAxis.SEMANTIC_ACTION,
            tuple(CheckDetail(item.semantic_action) for item in interactions),
            vectors,
        ),
    )
    return RepresentationConfoundAudit(
        dataset_source=interactions[0].dataset_source,
        feature_order=tuple(NetworkFeatureName(item) for item in feature_order),
        feature_variances=variances,
        constant_features=constant,
        near_constant_features=near_constant,
        packet_count_range=(
            min(vector.values[TOTAL_PACKET_COUNT_FEATURE_INDEX] for vector in vectors),
            max(vector.values[TOTAL_PACKET_COUNT_FEATURE_INDEX] for vector in vectors),
        ),
        byte_count_range=(
            min(vector.values[TOTAL_BYTE_COUNT_FEATURE_INDEX] for vector in vectors),
            max(vector.values[TOTAL_BYTE_COUNT_FEATURE_INDEX] for vector in vectors),
        ),
        capture_duration_range=(min(capture_durations), max(capture_durations)),
        chronology_available=all(timestamp is not None for timestamp in timestamps),
        site_or_lab_identities=contexts,
        network_conditions=contexts,
        action_collection_ordering_available=len(
            {item.semantic_action for item in interactions}
        )
        > 1,
        source_identities=sources,
        stratified_variation=stratified_variation,
        passed=not constant and not near_constant,
    )


def require_representation_audit_pass(audit: RepresentationConfoundAudit) -> None:
    if not audit.passed:
        raise ValueError(
            "representation-confound gate failed: "
            f"constant={audit.constant_features}; near_constant={audit.near_constant_features}"
        )
